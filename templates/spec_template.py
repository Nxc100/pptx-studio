"""Minimal deck spec — copy next to your project's assets/ folder, fill the TODOs, run:
    PYTHONIOENCODING=utf-8 python spec.py out/deck.pptx [--theme wabi_sabi]
Full worked example (30 slides, every archetype): examples/ba_wujie/spec.py ; API: references/archetypes.md"""
import os, sys, argparse
SKILL = r'C:\Users\21738\.claude\skills\pptx-studio'          # TODO: adjust if the skill lives elsewhere
sys.path.insert(0, os.path.join(SKILL, 'scripts'))
from studio import Deck

ap = argparse.ArgumentParser(); ap.add_argument('out', nargs='?', default='out/deck.pptx')
ap.add_argument('--theme', default='medieval_pastoral'); ap.add_argument('--assets', default='assets')
a = ap.parse_args()
d = Deck(a.theme, assets=a.assets, brand='TODO 项目名', brand_en='TODO ENGLISH LINE',
         meta=dict(title='TODO', author='TODO', subject='TODO'))

d.cover(title='TODO 项目名', subtitle='TODO 风格 · 类型', en_line='TODO ENGLISH SUBTITLE',
        info=[('主讲人', 'TODO'), ('学　号', 'TODO'), ('项目地点', 'TODO')], photo='photos/TODO.jpg')
d.contents([('01', '前期分析', 'Analysis', 'TODO · TODO'), ('02', '方案设计', 'Design', 'TODO'),
            ('03', '效果图', 'Renderings', 'TODO'), ('04', '总结', 'Summary', 'TODO')], photo='photos/TODO.jpg')
d.section('01', 'One', '前期分析', 'Analysis', 'photos/TODO.jpg', items='TODO · TODO', poem='TODO', mark='TODO')
d.text_image('设计说明', 'Statement', 'TODO 一句话主张', ['TODO 段落一', 'TODO 段落二'], 'photos/TODO.jpg',
             items=[('项目地点', 'TODO'), ('设计风格', 'TODO')])
# … add archetypes here (overview, location_levels, poi_map, chart_page, persona, pillars, moodboard, palette,
#   materials, plan_annotated, plan_legend, model3d, zones, flows, room, gallery_grid, board, summary)
d.thanks('photos/TODO.jpg', footer='TODO 项目名 | 作者')
print('saved', d.save(a.out), d.n, 'slides')
