# Analyzing a reference deck (and the user's draft)

```
python S/scripts/analyze_deck.py ref.pptx out/ref --brief      # report.md + grid-*.jpg
python S/scripts/analyze_deck.py draft.pptx out/draft --brief
```
Read `report.md` top section first (size, theme colours/fonts, used layouts + their decor images, master background,
transitions), then the grids, then only the slide sections you need. Typical findings and what to do with them:

| look for | where in report | carry over as |
|---|---|---|
| background texture / decor images on layouts | "Layouts (used)" images, master bg | theme `deco.paper`, corner decor |
| repeated photo frame shape (custGeom cloud, arch, circle) | slide rows `pic custGeom` | theme `frame` |
| title font, size, colour; English captions | text rows `fonts=[...]` | theme fonts, chrome |
| palette | theme colours + srgbClr fills | theme colours (re-tuned to the new style) |
| slide types | layout names (封面页/目录页/过渡页/内容页/结尾页) | archetype mix |
| animation vocabulary | "Animation vocabulary" + timelines | Timeline recipes (animation.md) |
| per-letter title animation | `by-letter` | `letters` effect on cover/section |
| transitions | slide/layout/master transition fields | theme transitions (reference templates often define them only on unused layouts → effectively none; you can do better) |
| page count & section structure | slide list | outline |

## Design brief template (write this before coding; ~10 lines)
```
Reference: <deck> — paper texture + <motif>; palette <hexes>; head font <x>; frames <shape>; decor <…>;
  animation: title wipe-left 0.5s, images ascend 1s, cover title by-letter; transitions: <none/…>.
Draft gaps: <missing pages>, <wrong text>, <leftover template slides>, <mislabelled titles>.
Target style: <style> → palette <…>, frame <…>, motifs <…>, transitions <…>.
Outline: <n> slides: …
Assets: photos <list>, crops <list>, 3D <maps/plan>, board yes/no.
Assumptions to tell the user: <personas, data sources>.
```

## Draft content audit
* Every material (render/plan/texture) should appear somewhere; every page title should match its content.
* Text that contradicts the materials (e.g. "日系面包店" text in a European home deck) gets rewritten.
* Remove leftover template pages (icon libraries, placeholder "请输入标题").
* Proposal decks normally need: 项目概况, 区位 (macro→micro), 气候, 人群/人物设定, 设计理念, 风格定位, 色彩, 材质,
  平面布置, 彩色平面, 功能分区, 动线, 效果图 per room, 展板, 总结.
* Facts: keep to well-known, checkable statements; mark approximations ("约", "示意", "近似值").
