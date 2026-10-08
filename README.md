# pptx-studio 使用说明

把本次"Ba · 无界森居"PPT 改造的全过程沉淀成了一套**可复用的工具包 + Claude Code 技能**。
下次做 PPT 时，内容写成一份约 250 行的"内容清单（spec）"，版式、动画、页面切换、配色主题全部由脚本生成，
质量与本次一致，耗费的 token 大约只有本次的一小部分。

## 下次怎么用（最省事）

技能已安装到 `C:\Users\21738\.claude\skills\pptx-studio\`，Claude Code 会在你提出做 PPT / 改造 PPT 时自动调用。
直接这样说即可：

> 用 pptx-studio，参考 `XX参考.pptx` 的视觉和动画，把 `XX.pptx` 改造成"新中式"风格，素材在 `XX素材/`，
> 补充区位分析（地址：XX省XX市XX区）。

Claude 会按 SKILL.md 的 7 步流程执行：素材盘点 → 参考稿分析（一条命令出报告）→ 选/派生主题 →
并行生成素材（3D 区位图、3D 户型、展板）→ 写 spec → 构建 + 渲染 + 自动查错 → 交付（备份原稿、同名覆盖、导出 PDF 与展板图）。

## 目录

| 路径 | 作用 |
|---|---|
| `SKILL.md` | 技能入口：流程、质量标准、已解决的坑、省 token 方法 |
| `references/` | 详细文档：版式 API（archetypes）、主题与风格配方（design-system）、动画与切换（animation）、素材与 3D（assets）、质检（qa）、参考稿分析（reference-analysis）、本次案例（case-ba-wujie） |
| `scripts/studio/` | 核心库：`Deck` 类 22 种带动画的版式 + OOXML 引擎 |
| `scripts/analyze_deck.py` | 一条命令分析参考稿/草稿：版式、字体、配色、每页动画时间线 + 缩略图 |
| `scripts/render_deck.py` | PPT → PDF → 每页图片 + 九宫格总览（视觉检查） |
| `scripts/check_deck.py` | 结构检查：动画目标、切换、备注、字体、LibreOffice 裁切陷阱 |
| `scripts/assets/` | 纸纹背景、主题一键派生/重新着色、图标、水彩植物与金色饰纹、照片处理 |
| `scripts/three/` | three.js：任意行政区 3D 区位图（含定位针、POI）、由彩平图生成 3D 户型与分区图 |
| `scripts/board/` + `templates/board_a1.html` | A1 展板模板与高清渲染 |
| `themes/` | 已有主题：`medieval_pastoral`（欧洲中世纪田园，本次）、`wabi_sabi`（侘寂，一键派生演示） |
| `examples/ba_wujie/` | 本次完整 spec（可一键重建 30 页）、3D 配置、各版式预览图 |

## 常用命令（在本目录下）

```bash
set PYTHONIOENCODING=utf-8
python examples/ba_wujie/spec.py out/deck.pptx                      # 重建本次的 PPT
python examples/ba_wujie/spec.py out/deck_wabi.pptx --theme wabi_sabi  # 同内容换成侘寂风
python scripts/analyze_deck.py 参考.pptx out/ref --brief             # 分析参考稿
python scripts/render_deck.py out/deck.pptx out/r                    # 渲染检查
python scripts/check_deck.py out/deck.pptx --fonts                   # 结构检查
python scripts/assets/derive_theme.py --from medieval_pastoral --to 新主题 ...   # 派生新风格（见 references/design-system.md）
```

## 换风格

`references/design-system.md` 里有 8 种风格配方（欧式田园、侘寂、新中式、北欧、法式复古、现代轻奢、工业风、日式原木），
每种都给出了色板、相框形状、装饰母题和切换方式。颜色类变化用 `derive_theme.py` 一条命令完成。
如果装饰的造型也要变（例如把橄榄枝换成竹子），用 `render_svg.py` 生成新的装饰图，或让 Claude 派一个子代理去画，文件名保持不变即可。

## 依赖

Python（python-pptx、Pillow、numpy、opencv、PyMuPDF、playwright + chromium）、LibreOffice，以及思源宋体（Noto Serif SC）。
3D 渲染和下载图标需要联网（three.js CDN、unpkg）。
