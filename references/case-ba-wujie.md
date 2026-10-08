# Case study: "Ba · 无界森居" (2026-10, first run of this pipeline)

**Ask**: analyse a reference deck (29 slides, sage-green 新中式/侘寂 cafe proposal: paper texture, bamboo corners,
海棠 cloud frames, title wipe/ascend/by-letter animations) and rebuild the student's 15-slide draft of a
欧洲中世纪田园风 apartment (成都武侯区) so it matches or beats the reference; add missing 区位分析 with three.js
illustrations; use the 13 materials (7 renders, 3 plans, 3 floor textures).

**Findings**: reference = 5 layouts (封面/目录/过渡/内容/结尾), entrance-only animations auto-playing, transitions
defined only on unused layouts (so none). Draft = mismatched texts (风格页写"日系面包店"), 区位页 titled 平面布局图,
no 气候/人群/理念/材质/动线/展板, two leftover icon-library slides, no animations.

**Decisions**: palette parchment F4EDE0 + olive 5E6B3D + terracotta B0623A + antique gold B08D57; Romanesque arch
frames (echo of the reference's cloud frames, and of the renders' arches); olive/lavender/rose watercolours, Gothic
quatrefoil, wax seal; Noto Serif SC + Microsoft YaHei + Palatino; transitions curtains / page curl / gallery /
prestige with fade fallback; 30 slides in 4 parts (see examples/ba_wujie/spec.py).

**Parallelism**: fork A rendered 3D maps (China/Sichuan/Chengdu/Wuhou + 6 POIs) and the 3D plan/zones/hero
(~9 min); fork B made paper, botanicals, ornaments, 138 icons (~13 min); main thread wrote the engine + slides.
A QA subagent reviewed all 30 renders once (found 14 issues, all fixed).

**Issues hit (now handled by the toolkit)**: duplicate master `<p:bg>`; spacing+alpha clipping; rotated text clipping;
negative animation offsets; clipped plan dimension text; badge overlaps; orphan characters; folio collisions;
validator network error on core.xml.

**Deliverables**: new deck (same file name, original backed up), PDF, A1 board JPG (4965×3507).
With this toolkit the same deck = spec.py (~250 lines) + 3D configs + one build/QA loop.
