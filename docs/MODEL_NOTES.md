# 模型说明与检查记录

[返回首页](../README.md)

本记录对应 2026-10-20 整理的文件快照。SHA-256 和文件大小见 [model-manifest.json](model-manifest.json)。原始六个 CAD 文件未被修改、重命名或移动。

## 检查依据

本次直接读取了原生文件中可提取的命名数据流，包括装配组件实例树、文档元数据及内嵌 PNG。识别出的压缩数据流均经过长度及 CRC-32 核对后才用于读取信息。

整理环境未提供可用的 SOLIDWORKS，因此未执行 CAD 打开、重建、配合求解或几何测量。下列记录区分“文件内保存的信息”和“软件实际运行的结果”。

| 项目 | 结果 / 范围 |
| --- | --- |
| 原生文件 | 1 个装配体、5 个零件，合计 1,440,718 字节 |
| 装配保存配置 | `默认` |
| 装配引用的零件种类 | 5 类，对应根目录五个同名零件文件 |
| 已保存组件实例 | 外圈 1、内圈 1、滚珠 8、钢球架 2、紧固件 8，共 20 个 |
| 组件状态 | 上述保存实例均标记为未压缩、未隐藏且计入 BOM |
| 预览 | 6 个文件均提取到有效的原始 PNG，尺寸均为 640 × 480 |
| 文件内元数据 | 六个文件均记录 `Application=SOLIDWORKS`、`AppVersion=23.0000`、`swVersion=13000` |
| 实际兼容版本 | 未在 SOLIDWORKS 中验证，不由上述元数据字段直接承诺 |

实例数按保存的 `swXmlContents/COMPINSTANCETREE` 中 `swReference` 记录统计；`swSuppressed=NO` 且 `swExcludeFromBOM=NO` 的记录计入上表。单个 `.SLDPRT` 的文件数量不等于装配中的实例数量。

## 组件关系

外圈、内圈、滚珠、两件钢球架和紧固件共同组成当前轴承装配。预览中可观察到环形套圈、滚动体和保持架结构。紧固件的外观类似铆接连接零件，但仓库保留原名“紧固件”，不将其声明为某一标准规格件。

文件名“滚珠”“钢球架”用于识别模型，不代表已经验证材料为轴承钢。表面颜色也不作为材料、热处理或表面处理的依据。

当前没有经复核的尺寸表、工程图、配合清单或建模过程记录。因此不把从外观推测的尺寸、标准型号、建模命令顺序或“完全约束”状态写作既定事实。

## 预览来源

| 对应原生文件 | 原始内嵌预览 |
| --- | --- |
| [滚珠轴承.SLDASM](../滚珠轴承.SLDASM) | [assembly.png](../assets/previews/assembly.png) |
| [轴承外圈.SLDPRT](../轴承外圈.SLDPRT) | [outer-ring.png](../assets/previews/outer-ring.png) |
| [轴承内圈.SLDPRT](../轴承内圈.SLDPRT) | [inner-ring.png](../assets/previews/inner-ring.png) |
| [滚珠.SLDPRT](../滚珠.SLDPRT) | [ball.png](../assets/previews/ball.png) |
| [钢球架.SLDPRT](../钢球架.SLDPRT) | [cage.png](../assets/previews/cage.png) |
| [紧固件.SLDPRT](../紧固件.SLDPRT) | [fastener.png](../assets/previews/fastener.png) |

预览来自每个原生文件的 `PreviewPNG` 数据流，提取后保持 PNG 字节不变。图片反映最后保存的视角和显示状态，不能替代对当前几何和配合状态的检查。内圈等预览保留了草图或坐标标记。

## 在 SOLIDWORKS 中完成的复核建议

以下工作尚未完成，可在实际验证后勾选并记录结果：

- [ ] 记录 SOLIDWORKS 年份版本及 Service Pack。
- [ ] 在独立文件夹打开装配，确认引用只指向交付文件夹中的零件。
- [ ] 完整重建，记录是否有特征错误或警告。
- [ ] 检查配合、自由度、压缩状态及实际 BOM 数量。
- [ ] 检查干涉、间隙和运动关系。
- [ ] 核对尺寸、单位、材料及设计意图。
- [ ] 如作为制造资料，另行完成工程图、公差及工艺审查。

建议使用“查找引用 / Find References”核对实际路径，并用“Pack and Go”准备可移交的文件集。官方说明：[Find References](https://help.solidworks.com/2024/English/SolidWorks/Sldworks/HIDD_FINDREFERENCES_HELP.htm)、[复制 SOLIDWORKS 装配项目](https://blogs.solidworks.com/products/solidworks/duplicating-a-solidworks-assembly-project/)。

## 分享与格式扩展

当前快照只提供原生零件和装配体，没有 STEP、STL、工程图、动画或仿真报告。后续可由原始模型导出 STEP 用于跨软件交流，再核对装配结构和几何是否完整。STL 通常用于网格用途，不能替代原生特征及装配关系。

原生文件中存在历史保存路径及旧模型名称等元数据。整理时未将原始路径复制到文档，也未直接改写二进制文件。若希望清理这类信息，应在 SOLIDWORKS 中检查属性、引用及保存结果，并重新检查完整文件集。

技术性容器读取方法参考开源项目的[原始容器研究记录](https://github.com/blussyya/sldprt-format-research/blob/main/docs/format/container.md)。这些研究用于读取快照信息，不代表 SOLIDWORKS 官方兼容性认证。
