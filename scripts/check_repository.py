#!/usr/bin/env python3
"""Check repository files without opening or modifying native CAD models."""

import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
from urllib.parse import unquote, urlsplit
import zlib


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path("docs/model-manifest.json")
CAD_SUFFIXES = {".sldprt", ".sldasm", ".slddrw"}
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "Backup", "AutoRecover"}


def repo_path(root, relative):
    """Reject manifest paths that point outside the repository."""
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ValueError(f"Expected a nonempty repository path: {relative!r}")
    path = (root / relative).resolve()
    if Path(relative).is_absolute() or not path.is_relative_to(root.resolve()):
        raise ValueError(f"Path is outside repository: {relative!r}")
    return path


def read_manifest(root):
    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1:
        raise ValueError("Unsupported manifest schema_version")
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        raise ValueError("Manifest must contain a nonempty files list")
    seen = set()
    previews = set()
    for entry in files:
        if not isinstance(entry, dict):
            raise ValueError("Each manifest file entry must be an object")
        path = entry.get("path")
        preview = entry.get("preview")
        repo_path(root, path)
        repo_path(root, preview)
        if path in seen or preview in previews:
            raise ValueError("Duplicate model path or preview mapping in manifest")
        seen.add(path)
        previews.add(preview)
        suffix = Path(path).suffix.lower()
        expected_kind = "assembly" if suffix == ".sldasm" else "part" if suffix == ".sldprt" else "drawing"
        if suffix not in CAD_SUFFIXES or entry.get("kind") != expected_kind:
            raise ValueError(f"Invalid CAD extension or kind: {path}")
    return manifest


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_error(path):
    """Validate PNG chunk boundaries and CRCs, without rendering geometry."""
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "invalid PNG signature"
    pos = 8
    first = True
    while pos + 12 <= len(data):
        size = struct.unpack_from(">I", data, pos)[0]
        end = pos + 12 + size
        if end > len(data):
            return "truncated PNG chunk"
        kind = data[pos + 4:pos + 8]
        payload = data[pos + 8:pos + 8 + size]
        crc = struct.unpack_from(">I", data, pos + 8 + size)[0]
        if zlib.crc32(kind + payload) != crc:
            return "PNG chunk CRC mismatch"
        if first:
            if kind != b"IHDR" or size != 13:
                return "missing PNG IHDR"
            width, height = struct.unpack_from(">II", payload)
            if not width or not height:
                return "invalid PNG dimensions"
            first = False
        if kind == b"IEND":
            return None if size == 0 and end == len(data) else "invalid PNG ending"
        pos = end
    return "missing PNG IEND"


def included_files(root):
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if SKIP_DIRS.intersection(relative.parts) or path.name.startswith("~$"):
            continue
        if path.is_file():
            yield path


def check_repository(root, manifest):
    errors = []
    expected = {entry["path"] for entry in manifest["files"]}
    actual = {
        path.relative_to(root).as_posix()
        for path in included_files(root) if path.suffix.lower() in CAD_SUFFIXES
    }
    for extra in sorted(actual - expected):
        errors.append(f"CAD file missing from manifest: {extra}")
    for entry in manifest["files"]:
        model = repo_path(root, entry["path"])
        preview = repo_path(root, entry["preview"])
        if not model.is_file():
            errors.append(f"Missing CAD file: {entry['path']}")
        else:
            if model.stat().st_size != entry.get("size_bytes"):
                errors.append(f"Size mismatch: {entry['path']}")
            if sha256(model) != entry.get("sha256"):
                errors.append(f"SHA-256 mismatch: {entry['path']}")
        if not preview.is_file():
            errors.append(f"Missing preview: {entry['preview']}")
        else:
            if sha256(preview) != entry.get("preview_sha256"):
                errors.append(f"SHA-256 mismatch: {entry['preview']}")
            problem = png_error(preview)
            if problem:
                errors.append(f"{problem}: {entry['preview']}")

    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)")
    for document in included_files(root):
        if document.suffix.lower() != ".md":
            continue
        text = document.read_text(encoding="utf-8")
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        targets = link_pattern.findall(text)
        targets += re.findall(r'(?:src|href)="([^"]+)"', text)
        for target in targets:
            parts = urlsplit(target.strip("<>"))
            if parts.scheme or parts.netloc or not parts.path:
                continue
            relative = unquote(parts.path)
            linked = (document.parent / relative).resolve()
            if not linked.is_relative_to(root.resolve()) or not linked.exists():
                errors.append(f"Broken local link in {document.relative_to(root)}: {target}")
    return errors


def refresh_manifest(root, manifest, snapshot_date):
    """Refresh only sizes and hashes after the maintainer reviews real changes."""
    for entry in manifest["files"]:
        model = repo_path(root, entry["path"])
        preview = repo_path(root, entry["preview"])
        if not model.is_file() or not preview.is_file():
            raise ValueError(f"Cannot refresh missing model or preview: {entry['path']}")
        problem = png_error(preview)
        if problem:
            raise ValueError(f"Cannot refresh invalid preview: {problem}")
        entry["size_bytes"] = model.stat().st_size
        entry["sha256"] = sha256(model)
        entry["preview_sha256"] = sha256(preview)
    # Check links and file inventory before writing any update.
    errors = check_repository(root, manifest)
    if errors:
        raise ValueError("Cannot refresh:\n" + "\n".join(errors))
    manifest["snapshot_date"] = snapshot_date
    (root / MANIFEST).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="Refresh reviewed file hashes and sizes")
    parser.add_argument("--date", help="Snapshot date for --refresh, as YYYY-MM-DD (default: Asia/Shanghai today)")
    args = parser.parse_args()
    if args.date and not args.refresh:
        parser.error("--date requires --refresh")
    try:
        manifest = read_manifest(ROOT)
        if args.refresh:
            today = datetime.now(timezone(timedelta(hours=8))).date().isoformat()
            snapshot_date = date.fromisoformat(args.date or today).isoformat()
            refresh_manifest(ROOT, manifest, snapshot_date)
            print("Refreshed sizes, hashes and snapshot date. BOM and previews are not generated.")
        errors = check_repository(ROOT, manifest)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {len(manifest['files'])} CAD files, their previews, hashes and local Markdown links.")
    print("CAD rebuilds, mates and geometry are not checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
