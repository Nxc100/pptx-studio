"""Example spec: 'Ba · 无界森居' 30-slide interior design proposal (欧洲中世纪田园风, 成都武侯区).
Reproduces the delivered deck.  python spec.py [out.pptx] [--theme medieval_pastoral] [--assets DIR]
Copy this file as the starting point for a new deck: keep the structure, replace the content."""
import os, sys, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'scripts'))
from studio import Deck

ap = argparse.ArgumentParser()
ap.add_argument('out', nargs='?', default=os.path.join(HERE, 'out', 'deck.pptx'))
ap.add_argument('--theme', default='medieval_pastoral')
ap.add_argument('--assets', default=os.path.join(HERE, 'assets'))
a = ap.parse_args()

d = Deck(a.theme, assets=a.assets, brand='Ba · 无界森居', brand_en='MEDIEVAL PASTORAL INTERIOR',
         meta=dict(title='Ba · 无界森居 —— 欧洲中世纪田园风住宅室内设计', author='刘诗云',
                   subject='室内设计方案汇报 · 四川省成都市武侯区', keywords='欧洲中世纪田园风; 室内设计; 武侯区'))
PL, PC, OFF = 'photos/plan_line_c.png', 'photos/plan_color_c.png', (14, 14)   # plans cropped 14px (clipped dims)

# ---------------------------------------------------------------- opening
d.cover(title=[dict(text='Ba', latin=True, italic=True), dict(text=' · 无界森居')],
        subtitle='欧洲中世纪田园风  ·  住宅室内空间设计',
        en_line='BOUNDLESS FOREST DWELLING — A MEDIEVAL PASTORAL HOME IN CHENGDU',
        kicker='2026  ·  INTERIOR DESIGN PROPOSAL',
        info=[('主讲人', '刘诗云'), ('学　号', '20240073294'), ('项目地点', '四川省成都市武侯区')],
        photo='photos/living1.jpg', focus=(0.56, 0.5),
        note='封面：Ba·无界森居——欧洲中世纪田园风住宅室内设计。')
d.contents([('01', '前期分析', 'Preliminary Analysis', '项目概况 · 区位 · 气候 · 人群 · 理念 · 风格 · 色彩 · 材质'),
            ('02', '平面布置', 'Spatial Planning', '平面布置 · 彩色平面 · 3D 鸟瞰 · 功能分区 · 动线分析'),
            ('03', '效果图展示', 'Renderings', '客厅 · 饭厅 · 主卧 · 书房兼客房 · 儿童房'),
            ('04', '展板设计', 'Exhibition Board', '展板排版 · 设计总结')],
           photo='photos/dining2.jpg', focus=(0.72, 0.45), note='目录：四个部分。')

# ---------------------------------------------------------------- part 1
d.section('01', 'One', '前期分析', 'Preliminary Analysis', 'photos/living2.jpg', (0.62, 0.5),
          items='项目概况 · 区位分析 · 气候分析 · 人群分析\n设计理念 · 风格定位 · 色彩分析 · 材质分析',
          poem='Where the meadow meets the hearth.', mark='PASTORAL')
d.overview('项目概况', 'Project Overview · 设计说明',
           stats=[('12.26×12.00', 'm', '户型外轮廓尺寸'), ('三室两厅', '', '一卫 · 干湿分离'), ('11', '个', '功能空间')],
           facts=[('项目名称', 'Ba · 无界森居'), ('项目地点', '四川省成都市武侯区'), ('项目类型', '城市平层住宅 · 年轻三口之家'), ('设计风格', '欧洲中世纪田园风')],
           paragraph='本案是一套为年轻三口之家打造的城市平层住宅。设计以“无界森居”为题，把欧洲中世纪乡村庄园中的罗马拱券、红砖、仿古砖、碎花布艺与铁艺灯具带入都市居所；'
                     '以连续的拱形门洞代替封闭的门扇，让玄关、饭厅、客厅与休闲区彼此贯通，使阳光、绿意与家人的日常在同一屋檐下自由流动。',
           photos=[('photos/living2.jpg', (0.35, 0.5), '客厅'), ('photos/dining1.jpg', (0.3, 0.5), '饭厅'), ('photos/master_bed.jpg', (0.45, 0.5), '主卧')])
d.location_levels('区位分析', 'Location · 中国 › 四川 › 成都 › 武侯', [
    ('3d/map_china.png', '中国 · 四川', '四川省，简称“川”或“蜀”，省会成都，位于中国西南部、长江上游，自古享有“天府之国”的美誉。'),
    ('3d/map_sichuan.png', '四川 · 成都', '成都位于四川盆地西部、成都平原腹地，是国家中心城市与西部重要的经济、文化中心。'),
    ('3d/map_chengdu.png', '成都 · 武侯区', '武侯区地处成都中心城区西南部，北连青羊区，东隔锦江毗邻锦江区，南接高新区与双流区，位于绕城高速以内；人民南路城市中轴贯穿其间，是老城核心向南延伸的关键过渡带。')],
    callout=dict(meta='3d/map_chengdu_meta.json', pin='武侯区', text='项目所在 · 武侯区'))
d.poi_map('区位分析', 'Location · 武侯区周边配套', '3d/map_wuhou.png', '3d/map_wuhou_meta.json',
          pois=[('landmark', '武侯祠·锦里', '三国文化圣地与古街，城市历史文脉'), ('graduation-cap', '四川大学望江校区', '百年学府，浓厚的人文书香氛围'),
                ('hospital', '华西医院', '西部顶级医疗资源，就医便利'), ('trees', '望江楼公园', '锦江畔竹林园景，城市绿肺'),
                ('coffee', '玉林街区', '市井烟火与慢生活的成都日常'), ('compass', '桐梓林', '成熟的国际化社区，多元文化交融')],
          center=('武侯区', 'WUHOU DISTRICT'), nudge={'四川大学望江校区': (-0.07, 0), '望江楼公园': (0.07, 0)},
          neighbors=[('北 · 青羊区', 0.0, -0.03), ('东 · 锦江区', 0.92, 0.32), ('南 · 高新区 / 双流区', 0.28, 1.0)],
          insight=('设计启示', 'DESIGN INSIGHT', '老城文脉与国际化社区在此交汇，为“都市里的中世纪田园居所”提供了包容的文化土壤。'))
M = [f'{i}月' for i in range(1, 13)]
d.chart_page('气候分析', 'Climate · 成都 · 亚热带湿润季风气候',
             line_chart=('月平均气温（℃）', M, [5.6, 7.9, 11.9, 17.0, 21.4, 23.9, 25.6, 25.2, 21.6, 17.2, 12.3, 7.2], '0.0'),
             bar_chart=('月降水量（mm）', M, [8, 11, 21, 48, 82, 118, 224, 206, 121, 37, 14, 5]),
             stats=[('thermometer', '≈16', '℃', '年平均气温'), ('cloud-rain', '≈900', 'mm', '年降水量'), ('sun', '≈1100', 'h', '年日照时数'), ('droplets', '≈80', '%', '年均相对湿度')],
             responses=[('潮湿多雨', '饭厅、卫浴、阳台选用仿古砖与仿古石材，防潮防滑；布艺选可拆洗棉麻。'), ('日照偏少', '奶油白墙面提亮空间，吊灯 + 壁灯 + 台灯组合 2700K 暖光。'),
                        ('夏季闷热', '连续拱形门洞形成穿堂风，饭厅吊扇灯辅助通风。'), ('冬季阴冷', '实木地板、厚织物与壁炉造型带来温暖的触感与心理暖意。')],
             source='数据：成都市多年月平均值（近似），用于设计趋势参考')
d.persona('人群分析', 'Persona · 年轻三口之家的田园梦想',
          people=[('user', '林先生 · 36 岁', '建筑工程师', '阅读 · 黑胶唱片 · 周末下厨', '安静的阅读与办公角落'),
                  ('flower-2', '苏女士 · 34 岁', '花艺师', '钢琴 · 花艺 · 复古布艺', '钢琴休闲区与充足收纳'),
                  ('baby', '朵朵 · 6 岁', '小学一年级', '童话 · 粉色 · 画画', '安全又梦幻的城堡卧室')],
          extra_line=('偶有长辈探访小住', '→ 书房兼客房，书柜之间放下一张客床'),
          day=[('07:30', '卡座早餐', '饭厅'), ('09:00', '居家办公', '书房'), ('15:00', '花艺午茶', '阳台'), ('18:30', '长桌晚餐', '饭厅'), ('20:00', '钢琴与绘本', '休闲区'), ('22:00', '安眠', '卧室')],
          mapping=[('阅读 / 办公', '书房兼客房 · 拱形书柜'), ('钢琴 / 花艺', '客厅休闲区 · 钢琴角'), ('童话 / 安全', '儿童房 · 帷幔城堡床'),
                   ('家庭团聚', '开放饭厅 · 窗边卡座'), ('收纳', '主卧衣帽间 · 玄关柜'), ('仪式感', '壁炉电视墙 · 烛台吊灯')])
d.pillars('设计理念', 'Concept · 无界 · 森 · 居', '把一座中世纪的乡间庄园，轻轻放进成都的城市楼宇之间。', [
    ('无', '无界', 'BOUNDLESS', 'crops/arch_brick.jpg', '以连续的罗马拱券代替封闭门扇，玄关—饭厅—客厅—休闲区一气呵成：空间无界，家人无隔。'),
    ('森', '森', 'FOREST', 'crops/floral.jpg', '碎花布艺、绿植花艺、原木与赤陶，把田野、森林与花园的气息带进室内，在城市中重拾自然。'),
    ('居', '居', 'DWELLING', 'crops/fireplace.jpg', '以壁炉、烛台吊灯与长餐桌为家的中心，营造温暖、安定、可以传承的家庭生活。')])
d.moodboard('风格定位', 'Style · 欧洲中世纪田园风', [('欧洲中世纪', 'primary_dk'), ('田园风', 'accent')], 'MEDIEVAL  PASTORAL  STYLE',
            '源自欧洲中世纪乡村庄园与农舍：厚重的拱券与砖石、温润的原木、手工铁艺与花卉布艺，质朴而有仪式感。本案在保留其古典语汇的同时弱化繁复装饰，以暖调大地色营造舒适的现代居家氛围。',
            ['拱券', '红砖', '仿古砖', '碎花', '铁艺', '原木'],
            [('crops/arch_brick.jpg', '罗马拱券', '红砖饰面拱门'), ('crops/chandelier.jpg', '铁艺吊灯', '石膏雕花灯盘'), ('crops/window_arch.jpg', '拱形窗格', '装饰镜与烛台'),
             ('crops/floral.jpg', '碎花布艺', '玫瑰缠枝纹样'), ('crops/iron_shelf.jpg', '铁艺花架', '卷草纹铁艺'), ('crops/bookshelf_arch.jpg', '拱形书柜', '嵌入式壁龛'),
             ('crops/tiffany.jpg', '彩绘玻璃', '蒂凡尼台灯'), ('crops/wood_chair.jpg', '曲木家具', '原木手作质感')])
d.palette('色彩分析', 'Colour · 温暖的大地色与花园色',
          '以奶油白与原木色为底，胡桃木压稳地面，赤陶、酒红、玫瑰粉与橄榄绿如花园般小面积点缀——温暖、怀旧而不沉闷。',
          [('F1E7D8', '奶油白', '墙面 · 天花'), ('E3CDAE', '暖杏', '石膏线 · 柜体'), ('C99A6B', '蜂蜜原木', '家具 · 门窗'), ('6E4B35', '胡桃木', '地板'),
           ('B0623A', '赤陶红', '仿古砖 · 红砖'), ('7E2E2B', '勃艮第酒红', '壁炉墙 · 入户门'), ('C98E84', '玫瑰粉', '碎花布艺'), ('6E7B4B', '橄榄绿', '绿植 · 墙面')],
          [(0.6, 'E3CDAE', '主色 60% · 奶油白 / 暖杏', 'ink'), (0.3, '8A6244', '辅色 30% · 原木 / 胡桃木', 'white'), (0.1, 'B0623A', '点缀 10%', 'white')],
          '点缀色：赤陶红 · 勃艮第酒红 · 玫瑰粉 · 橄榄绿——以布艺、软装与绿植的形式出现，可随季节更换。',
          'photos/living2.jpg', focus=(0.12, 0.5))
d.materials('材质分析', 'Material · 自然、手作与时间的痕迹', [
    ('photos/mat_living.jpg', 'crops/use_living.jpg', '胡桃色实木地板', '客厅 · 休闲区', '长条错缝铺贴，木纹自然温润，脚感舒适，与暖光相互映衬。'),
    ('photos/mat_dining.jpg', 'crops/use_dining.jpg', '米黄仿古砖 · 角花拼贴', '饭厅 · 门厅', '八角砖配深色小角花，斜向铺贴并以马赛克波打线收边，耐磨防滑。'),
    ('photos/mat_bath.jpg', 'crops/use_bath.jpg', '灰白仿古石材', '卫浴 · 厨房 · 阳台', '不规则长短拼铺的石灰石质感，哑光防滑，适应成都潮湿气候。')],
    subs=[('crops/sub_brick.jpg', '红砖饰面', '拱门 · 局部墙面'), ('crops/sub_fabric.jpg', '棉麻碎花布艺', '沙发 · 窗帘 · 坐垫'),
          ('crops/sub_iron.jpg', '手工铁艺', '吊灯 · 花架'), ('crops/sub_wood.jpg', '原木 / 曲木', '家具 · 门窗')])

# ---------------------------------------------------------------- part 2
d.section('02', 'Two', '平面布置', 'Spatial Planning', 'photos/master_bed.jpg', (0.42, 0.5),
          items='平面布置图 · 彩色平面图 · 三维户型鸟瞰\n功能分区 · 动线分析', poem='Every arch opens onto home.', mark='HEARTH')
d.plan_annotated('平面布置图', 'Floor Plan · 三室两厅一卫', PL, offset=OFF, rooms=[
    ('客厅', (930, 700)), ('休闲区', (530, 520)), ('餐厅', (395, 740)), ('厨房', (300, 640)), ('门厅', (530, 840)), ('主卧', (800, 1020)),
    ('衣帽间', (665, 900)), ('小孩房', (950, 400)), ('书房 / 客房', (300, 380)), ('卫浴', (520, 380)), ('阳台', (1075, 970)), ('楼梯间', (250, 960))],
    dims=[('12 260', '总面宽 mm'), ('12 000', '总进深 mm'), ('3 180', '主卧开间 mm'), ('2 260', '阳台面宽 mm')],
    points=['公共核心：门厅—客厅—休闲区—餐厅—厨房连成公共区，拱门串联。', '私密分区：三间卧室分置户型角部，远离入口与公共活动。', '辅助配套：卫浴干湿分离，主卧配衣帽间，阳台紧邻客厅。'])
d.plan_legend('彩色平面图', 'Colour Plan · 以材质界定空间', PC, [
    ('crops/fl_walnut.jpg', '胡桃木长条地板', '客厅 · 休闲区'), ('crops/fl_herring.jpg', '人字拼木地板', '主卧 · 小孩房 · 书房'),
    ('crops/fl_tile.jpg', '米黄仿古砖拼花', '餐厅 · 门厅'), ('crops/fl_stone.jpg', '灰白仿古石材', '卫浴 · 厨房 · 阳台')],
    note_text='公共区以温润木地板连成一体；湿区与阳台用防滑石材；餐厅与门厅以仿古砖拼花自成一区——不设门槛，用“地面的语言”划分空间。')
ROOMS3D = ['客厅', '休闲区', '餐厅', '厨房', '门厅', '主卧', '衣帽间', '小孩房', '书房/客房', '卫浴', '阳台']
d.model3d('三维户型鸟瞰', '3D Axonometric · 三维模型鸟瞰', '3d/plan3d.png', '3d/plan3d_meta.json', ROOMS3D,
          '依据彩色平面图提取墙体并搭建三维模型（three.js 渲染）：去掉屋顶与上半墙体，像打开一座玩偶屋，直观呈现各空间的尺度、材质与相互关系。',
          [('door-open', '拱门串联', '入户后经门厅进入公共核心，客厅、休闲区与餐厅视线贯通。'), ('layers', '材质分区', '木地板、仿古砖与石材在三维中清晰可辨，地面即是分区。'),
           ('sun', '采光通风', '客厅与卧室沿外墙展开、开窗充分；阳台引入自然光与绿意。')])
d.zones('功能分区', 'Zoning · 动静分区', '3d/plan3d_zones.png', '3d/plan3d_zones_meta.json',
        {'客厅': 0, '休闲区': 0, '餐厅': 0, '门厅': 0, '厨房': 0, '主卧': 1, '小孩房': 1, '书房/客房': 1, '卫浴': 2, '衣帽间': 2, '阳台': 2},
        [('动区', 'ACTIVE ZONE', 'E8B99A', '客厅 · 休闲区 · 餐厅 · 门厅 · 厨房', '位于户型中部，彼此以拱门贯通，承载会客、用餐、娱乐等家庭公共活动。'),
         ('静区', 'QUIET ZONE', 'B7C09F', '主卧 · 小孩房 · 书房兼客房', '分置户型角部，与公共区之间以走道或衣帽间缓冲，安静私密。'),
         ('辅助区', 'SERVICE ZONE', 'E3CF9F', '卫浴 · 衣帽间 · 阳台 · 楼梯间', '贴近使用空间布置，干湿分离、收纳集中，服务动静两区。')])
d.flows('动线分析', 'Circulation · 三条动线 · 分流有序', PL, offset=OFF, entry=(530, 1010, '入户'), flows=[
    ('家庭成员动线', 'primary', 'sysDash', [[(530, 1010), (530, 900), (532, 770), (610, 700), (760, 680), (790, 560), (785, 480), (800, 400)],
                                        [(610, 700), (650, 790), (690, 870), (780, 930)], [(560, 640), (520, 520), (470, 470), (420, 420), (380, 380)]],
     '入户 → 门厅 → 客厅 → 各卧室与书房；回家路径短而顺，经公共区自然分流至私密区。'),
    ('访客动线', 'line', None, [[(545, 1010), (545, 900), (548, 770), (640, 660), (760, 630), (860, 640)], [(530, 760), (440, 790), (360, 800)]],
     '入户 → 门厅 → 客厅 / 餐厅；访客止步于公共区，不进入卧室。'),
    ('家务动线', 'accent', 'dash', [[(515, 1010), (515, 900), (490, 760), (420, 715), (360, 650), (345, 560)], [(900, 720), (1000, 700), (1060, 760), (1075, 860)]],
     '入户 → 餐厅 → 厨房，采购物品直达；客厅 → 阳台完成晾晒，路径简短。')],
    summary=('动静分离　洁污分流', '三条动线以门厅为共同起点后迅速分流，彼此交叉少；公共活动集中在中部，私密空间不受打扰。'))

# ---------------------------------------------------------------- part 3
d.section('03', 'Three', '效果图展示', 'Renderings', 'photos/dining1.jpg', (0.2, 0.5),
          items='客厅 · 饭厅 · 主卧 · 书房兼客房 · 儿童房', poem='Rooms that bloom like a cottage garden.', mark='GARDEN')
R = dict(keyplan=PC, offset=OFF)
d.room('客厅 · 角度一', 'Living Room · View I', 'photos/living1.jpg', rect=(600, 470, 1040, 800), side='right', **R, points=[
    ('lamp-ceiling', '城堡般的顶面', '弧形石膏吊顶与放射状雕花灯盘，中心悬挂黑色铁艺烛台吊灯，再现中世纪大厅的仪式感。'),
    ('palette', '温柔的墙面', '浅玫瑰灰墙面，铜质烛台壁灯与错落的木框照片墙记录家的故事。'),
    ('sofa', '布艺与木作', '玫瑰碎花布艺沙发、曲木扶手椅与原木格栅茶几，松弛而有温度。'), ('layers', '温润的地面', '胡桃色实木地板，与暖光相互映衬。')])
d.room('客厅 · 角度二', 'Living Room · View II', 'photos/living2.jpg', rect=(600, 470, 1040, 800), side='left', **R,
       details=['crops/chandelier.jpg', 'crops/fireplace.jpg'], points=[
    ('home', '壁炉电视墙', '勃艮第酒红墙面 + 拱形文化砖壁炉造型 + 原木搁板，“炉火即家”。'),
    ('book-open', '尖拱壁龛', '两侧嵌入式尖拱书架陈列书籍与旧物，呼应哥特式窗洞。'),
    ('door-open', '拱门序列', '远处拱形门洞与格栅木门串联休闲区与饭厅，空间层层递进。')])
d.room('饭厅 · 角度一', 'Dining Room · View I', 'photos/dining1.jpg', rect=(230, 690, 470, 890), side='right', **R, points=[
    ('brick-wall', '红砖拱券', '红砖饰面的罗马拱门界定玄关与饭厅，以门洞代替门扇。'), ('wind', '吊扇灯', '木叶吊扇灯兼顾照明与通风，回应成都夏季的闷热。'),
    ('flower-2', '马赛克与卡座', '绿色花砖马赛克墙裙配窗边碎花卡座，阳光餐厅的明快一角。'), ('sprout', '铁艺花架', '卷草纹铁艺搁架与照片墙，点缀绿植与小摆件。')])
d.room('饭厅 · 角度二', 'Dining Room · View II', 'photos/dining2.jpg', rect=(230, 690, 470, 890), side='left', **R,
       details=['crops/window_arch.jpg', 'crops/arch_brick.jpg'], points=[
    ('castle', '拱形窗格镜', '装饰镜模仿中世纪拱窗，扩展视觉深度。'), ('sparkles', '餐边仪式感', '印花柜门、红色长烛台与一束黄玫瑰，让每一餐都有仪式。'),
    ('door-open', '双拱框景', '透过两重拱门望向厨房，形成层层框景。'), ('gem', '仿古砖拼花', '八角砖斜铺，配深色角花与波打线。')])
d.room('主卧', 'Master Bedroom', 'photos/master_bed.jpg', rect=(735, 800, 970, 1080), side='right', focus=(0.45, 0.5), **R, points=[
    ('flower', '缠枝花卉墙纸', '浅蓝灰缠枝花卉墙纸，安静柔和，适合休憩。'), ('lamp-ceiling', '层次暖光', '水晶铁艺吊灯 + 蒂凡尼彩绘玻璃台灯，光线温暖而富有层次。'),
    ('bed-double', '欧式白色家具', '白色雕花床、斗柜与整墙衣柜，收纳充足。'), ('door-open', '拱门与油画', '拱形门洞衔接衣帽间；床头一幅田园风景油画。')])
d.room('书房兼客房', 'Study & Guest Room', 'photos/second_bed.jpg', rect=(245, 195, 445, 440), side='left', **R, details=['crops/bookshelf_arch.jpg'], points=[
    ('palette', '鼠尾草绿墙面', '低饱和的鼠尾草绿，安静而有书卷气。'), ('book-open', '三联拱形书柜', '嵌入式拱形书柜，收纳与展示兼顾。'),
    ('shirt', 'X 形格栅衣柜', '原木 X 形格栅配压花玻璃，典型的乡间农舍语汇。'), ('sun', '碎花罗马帘', '窗边书桌配碎花罗马帘，阅读观景两相宜；长辈来访可留宿。')])
d.room('儿童房', "Children's Room", 'photos/kids.jpg', rect=(735, 170, 1040, 440), side='right', focus=(0.5, 0.45), **R, points=[
    ('castle', '城堡公主床', '粉色帷幔上下铺，满足童话想象，也方便小伙伴留宿。'), ('gem', '花边拱龛', '波浪花边的拱形壁龛，收纳与展示童年的宝贝。'),
    ('flower-2', '碎花墙纸', '奶黄底小碎花墙纸，温暖而不刺激。'), ('heart', '安全与成长', '圆角家具与软包，留言板记录成长点滴。')])

# ---------------------------------------------------------------- part 4 + closing
d.section('04', 'Four', '展板设计', 'Exhibition Board', 'photos/second_bed.jpg', (0.62, 0.5),
          items='展板排版 · 设计总结', poem='A home, written in arches and flowers.', mark='DWELLING')
d.board('展板设计', 'Exhibition Board · A1 横版', 'board/board.jpg',
        [('map-pin', '项目与区位', '标题、项目信息与三级区位图'), ('layers', '平面与分区', '三维鸟瞰、动静分区与设计理念'),
         ('palette', '风格与色材', '风格元素、配色比例与材质样板'), ('sparkles', '效果图', '七张空间效果图串联完整居家体验')],
        [('规格', 'A1 横版 841 × 594 mm'), ('配色', '羊皮纸底 · 橄榄绿 · 赤陶')])
d.summary('设计总结', 'Summary · 无界森居', '让每一道拱门，都通向家的温度。', 'EVERY ARCH OPENS ONTO THE WARMTH OF HOME', [
    ('door-open', '空间 · 无界', '拱门串联公共核心，卧室分置角部，动静分离、流线清晰。', 'crops/arch_brick.jpg'),
    ('castle', '风格 · 中世纪田园', '拱券、红砖、铁艺与碎花，古典语汇的现代表达。', 'crops/window_arch.jpg'),
    ('palette', '色彩 · 大地与花园', '奶油白与原木打底，赤陶、酒红、玫瑰与橄榄点缀。', 'crops/floral.jpg'),
    ('leaf', '材质 · 自然手作', '实木、仿古砖、石材、棉麻与铁艺，经得起时间。', 'crops/iron_shelf.jpg')])
d.thanks('photos/dining2.jpg', focus=(0.72, 0.45),
         footer=[dict(text='Ba · 无界森居', font='head', bold=True, color='accent'), dict(text='　|　刘诗云　20240073294')])
print('saved', d.save(a.out), d.n, 'slides')
