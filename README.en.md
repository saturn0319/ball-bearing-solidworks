# Ball Bearing · SOLIDWORKS Modeling & Assembly

[简体中文](README.md) · [Model notes](docs/MODEL_NOTES.md) · [Publishing guide](docs/PUBLISHING.md) · [Rights notice](LICENSE)

A personal mechanical CAD project showcasing a ball bearing and its component assembly. The repository contains the native SOLIDWORKS assembly, five distinct part files, and previews extracted from the actual model files.

![Original saved preview of the ball bearing assembly](assets/previews/assembly.png)

> All six previews are the original PNG images embedded in the CAD files, without re-rendering. This is a public portfolio repository with all rights reserved; see [LICENSE](LICENSE).

## Included models

| Component | Native file | Instances in saved default configuration |
| --- | --- | ---: |
| Outer ring | [轴承外圈.SLDPRT](轴承外圈.SLDPRT) | 1 |
| Inner ring | [轴承内圈.SLDPRT](轴承内圈.SLDPRT) | 1 |
| Ball | [滚珠.SLDPRT](滚珠.SLDPRT) | 8 |
| Cage component | [钢球架.SLDPRT](钢球架.SLDPRT) | 2 |
| Fastener | [紧固件.SLDPRT](紧固件.SLDPRT) | 8 |
| **Total** | **5 distinct part files** | **20** |

Assembly entry point: [滚珠轴承.SLDASM](滚珠轴承.SLDASM).

Quantities come from the component instance tree saved inside the assembly, counting unsuppressed instances included in the BOM. They have not been regenerated or verified in a live SOLIDWORKS session.

## Part gallery

| Outer ring | Inner ring |
| :---: | :---: |
| ![Outer ring](assets/previews/outer-ring.png) | ![Inner ring](assets/previews/inner-ring.png) |
| Ball | Cage component |
| ![Ball](assets/previews/ball.png) | ![Cage component](assets/previews/cage.png) |

<details>
<summary>Fastener preview</summary>

![Fastener](assets/previews/fastener.png)

</details>

Some saved previews include sketch or coordinate markers from the model's last saved display state.

## Opening the assembly

1. Clone or download the entire repository. Extract downloaded ZIP files first.
2. Keep all six native CAD files together and preserve their original Chinese filenames.
3. Open `滚珠轴承.SLDASM` in a compatible SOLIDWORKS installation.
4. Select the saved `默认` (default) configuration, inspect component loading, and perform a full rebuild with `Ctrl + Q`.
5. If a reference is missing, point the assembly to the matching local part file using the reference settings in the open dialog.

The exact saved release and compatible software versions still require confirmation in SOLIDWORKS. Raw version fields are documented in the [model notes](docs/MODEL_NOTES.md); they are not a compatibility guarantee.

Download the part files together with the assembly. See the official [SOLIDWORKS Find References documentation](https://help.solidworks.com/2024/English/SolidWorks/Sldworks/HIDD_FINDREFERENCES_HELP.htm) for reference inspection.

## Repository contents

- Root directory: the original assembly and all five part files.
- [assets/previews](assets/previews): six original embedded PNG previews.
- [docs/MODEL_NOTES.md](docs/MODEL_NOTES.md): inspection evidence, scope, and pending CAD validation.
- [docs/model-manifest.json](docs/model-manifest.json): file sizes, SHA-256 hashes, quantities, and preview mapping.
- [docs/PUBLISHING.md](docs/PUBLISHING.md): repository name, description, topics, and upload instructions.
- [scripts/check_repository.py](scripts/check_repository.py): optional repository integrity checks using only the Python standard library.
- [.github](.github): integrity workflow and issue / pull request templates.

The six native CAD files total approximately **1.37 MiB**. Ordinary Git is sufficient for this file set; Git LFS is not configured.

## Integrity checks

With Python 3.10 or newer:

```bash
python scripts/check_repository.py
```

The script checks CAD and preview presence, recorded SHA-256 hashes, and local file links in Markdown. The same checks run on GitHub Actions for pushes and pull requests. No third-party Python packages are needed.

These checks do not open SOLIDWORKS, solve mates, or validate geometry. See [CONTRIBUTING.md](CONTRIBUTING.md) before changing models or refreshing the manifest.

## Validation status

The native file set, saved component tree, and embedded previews have been inspected. Rebuilds, mate solving, interference checks, dimensions, materials, tolerances, and load capacity have not been verified in SOLIDWORKS.

Engineering drawings, neutral-format exports, exploded views, and motion studies are not included in this snapshot. Future additions should come from the original CAD model and be checked before publication. This repository is a modeling portfolio, without a claim of manufacturing readiness.

## Feedback and rights

Use Issues to report missing files, opening problems, or documentation mistakes. Include your software version, affected file, and reproduction steps. Read the [contribution guide](CONTRIBUTING.md) before submitting changes.

**All rights reserved.** Public visibility does not grant additional permission to modify, redistribute, or commercially use the contents. Applicable law and rights under GitHub's Terms of Service are unaffected. See [LICENSE](LICENSE) and GitHub's official [repository licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).
