# GitHub 上传与仓库设置

[返回首页](../README.md)

## 推荐名称

```text
ball-bearing-solidworks
```

名称直接说明“滚珠轴承”和“SOLIDWORKS”，便于作为个人作品集展示。

中文展示名称：**滚珠轴承 · SOLIDWORKS 三维建模与装配**。

## 仓库简介

适合粘贴到 GitHub 的 Description：

```text
基于 SOLIDWORKS 的滚珠轴承三维建模与装配项目，包含内外圈、滚珠、保持架及紧固件的原生模型、装配体、真实预览和项目文档。
```

如果希望使用英文：

```text
A SOLIDWORKS ball bearing modeling and assembly project with native CAD files, component previews, a saved component inventory, and documentation.
```

## 建议 Topics

```text
solidworks
cad
3d-modeling
mechanical-design
mechanical-engineering
ball-bearing
assembly
portfolio
```

这些主题符合当前交付内容；未提供仿真、工程图或 3D 打印验证，因此不添加对应主题。

## 上传前状态

- 中英文 README、真实预览、文件清单、Git 忽略规则、二进制属性和版权声明已备齐。
- 原生模型保留在根目录，避免因整理目录破坏已有引用。
- 此仓库采用“保留所有权利、公开展示”，不要在 GitHub 创建页面另外添加 MIT 等开放许可证。
- GitHub Actions 配置已提供，只有实际上传后才能看到平台上的运行结果。
- CAD 的实际打开和完整重建仍需在 SOLIDWORKS 中确认，状态已在首页披露。

## 推荐上传方法：Git

1. 在 GitHub 创建空仓库，名称填写 `ball-bearing-solidworks`。如希望作品公开可选 Public；不要额外初始化 README、`.gitignore` 或许可证，以免与本地文件冲突。
2. 在本项目根目录打开终端，执行：

```bash
git init
git branch -M main
git add .
git status
git diff --cached --stat
git commit -m "Add ball bearing CAD project and documentation"
```

3. 检查暂存内容包含 `.github`、`.gitignore`、`.gitattributes`、六个 CAD 文件和 `assets/previews`，然后设置本项目的远程地址并推送：

```bash
git remote add origin https://github.com/saturn0319/ball-bearing-solidworks.git
git push -u origin main
```

4. 在仓库 About 区域粘贴简介并设置 Topics。首页会自动读取 `README.md`。
5. 查看 Actions 中的 `Repository integrity` 是否通过；再完整下载一次仓库，在 SOLIDWORKS 中核对引用。

项目仓库：[saturn0319/ball-bearing-solidworks](https://github.com/saturn0319/ball-bearing-solidworks)。上述命令用于首次从本地 Git 上传；若仓库已包含项目，请先克隆仓库，再提交后续修改。

## 可选：浏览器上传

也可在空仓库的上传页面提交工作区文件。请确认文件夹结构完整，特别是以点开头的文件和 `.github` 文件夹。浏览器若无法完整保留这些文件，使用上面的 Git 方法。

不要仅上传一个压缩包，否则首页文档、预览和文件浏览体验都会受影响。原生装配体和五个零件应作为普通仓库文件一起上传。

## 后续发布作品版本

实际完成 CAD 检查后，可建立首个 Release，例如 `v1.0.0`，说明所用 SOLIDWORKS 版本、检查结果及新增的中性格式文件。当前不预填“重建通过”“无干涉”或“可直接制造”等未经验证的结果。

GitHub 对公开仓库的查看与 Fork 等平台行为仍有相应条款。公开展示并不等于采用开放许可证，参见 [GitHub 官方许可说明](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)。
