"""
Build src/data/animals.json from an inline curated list of 50 representative species.

Each tuple field order:
  id, wiki_title, name_cn, name_en, name_latin, class, habitat, region,
  lat, lon, status, emoji, diet, desc

status:  LC=无危  NT=近危  VU=易危  EN=濒危  CR=极危
diet:    carnivore (肉食) | herbivore (草食) | omnivore (杂食)
         | insectivore (食虫) | piscivore (食鱼)

Usage:
  python scripts/build_animals.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "src", "data", "animals.json")

FIELDS = (
    "id wiki_title name_cn name_en name_latin class habitat region "
    "lat lon status emoji diet desc"
).split()

ANIMALS = [
    # ---- 极地(北极 + 南极) ----
    ("polar-bear", "Polar_bear", "北极熊", "Polar Bear", "Ursus maritimus",
     "哺乳纲", "极地", "北极", 84.0, 0.0, "VU", "🐻‍❄️", "carnivore",
     "世界上最大的陆地食肉动物,生活在北极海冰上,主食海豹。海冰融化导致栖息地大幅缩减。"),
    ("arctic-fox", "Arctic_fox", "北极狐", "Arctic Fox", "Vulpes lagopus",
     "哺乳纲", "极地", "北极", 78.0, -20.0, "LC", "🦊", "omnivore",
     "冬季纯白、夏季褐色的小型狐狸,能在 -50℃ 极寒中生存。脚底长毛防滑保暖。"),
    ("walrus", "Walrus", "海象", "Walrus", "Odobenus rosmarus",
     "哺乳纲", "极地", "北极", 75.0, -90.0, "VU", "🦭", "carnivore",
     "拥有标志性长牙的大型鳍足类,用獠牙在冰上打洞、防御捕食者。雄性可重达 2 吨。"),
    ("emperor-penguin", "Emperor_penguin", "帝企鹅", "Emperor Penguin", "Aptenodytes forsteri",
     "鸟纲", "极地", "南极", -77.0, 167.0, "NT", "🐧", "piscivore",
     "世界上最大的企鹅。雄性在南极最严酷的冬季孵蛋,长达两个月不进食。"),

    # ---- 北美(7) ----
    ("mountain-lion", "Cougar", "美洲狮", "Mountain Lion", "Puma concolor",
     "哺乳纲", "森林", "北美", 40.0, -107.0, "LC", "🦁", "carnivore",
     "美洲分布最广的大猫,从加拿大育空到南美巴塔哥尼亚。独居夜行,伏击狩猎。"),
    ("grizzly-bear", "Grizzly_bear", "灰熊", "Grizzly Bear", "Ursus arctos horribilis",
     "哺乳纲", "森林", "北美", 60.0, -140.0, "LC", "🐻", "omnivore",
     "北美棕熊亚种,洛矶山脉与阿拉斯加森林之王。秋季捕食洄游鲑鱼,冬季冬眠。"),
    ("bald-eagle", "Bald_eagle", "白头海雕", "Bald Eagle", "Haliaeetus leucocephalus",
     "鸟纲", "湿地", "北美", 50.0, -100.0, "LC", "🦅", "piscivore",
     "美国国鸟,翼展可达 2.3 米。20 世纪 DDT 污染几近灭绝,经保护已恢复。"),
    ("american-bison", "American_bison", "美洲野牛", "American Bison", "Bison bison",
     "哺乳纲", "草原", "北美", 45.0, -103.0, "NT", "🦬", "herbivore",
     "北美大平原巨兽,曾达 6000 万头,因屠杀骤减至千余,现保护恢复至约 50 万。"),
    ("gray-wolf", "Wolf", "灰狼", "Gray Wolf", "Canis lupus",
     "哺乳纲", "森林", "北美", 55.0, -110.0, "LC", "🐺", "carnivore",
     "犬科顶级捕食者,群居社会结构严密。曾分布北半球大部,现仅余北美与欧亚部分地区。"),
    ("moose", "Moose", "驼鹿", "Moose", "Alces alces",
     "哺乳纲", "森林", "北美", 62.0, -150.0, "LC", "🫎", "herbivore",
     "现存最大鹿科动物,雄性肩高 2 米、鹿角宽达 1.8 米。喜欢沼泽湿地、吃水生植物。"),
    ("raccoon", "Raccoon", "浣熊", "Raccoon", "Procyon lotor",
     "哺乳纲", "森林", "北美", 38.0, -77.0, "LC", "🦝", "omnivore",
     "戴黑色眼罩的「洗手熊」,前爪极其灵巧,可拧瓶盖开门把。已扩张至欧亚多国。"),

    # ---- 南美(6) ----
    ("sloth", "Three-toed_sloth", "三趾树懒", "Three-toed Sloth", "Bradypus tridactylus",
     "哺乳纲", "森林", "南美", -3.0, -60.0, "LC", "🦥", "herbivore",
     "亚马逊雨林居民,每分钟仅移 2 米,一周下树排便一次。毛上共生藻类天然伪装。"),
    ("jaguar", "Jaguar", "美洲豹", "Jaguar", "Panthera onca",
     "哺乳纲", "森林", "南美", -10.0, -55.0, "NT", "🐆", "carnivore",
     "美洲最大猫科动物,咬合力是大型猫科之最,能咬穿凯门鳄头骨与海龟壳。"),
    ("capybara", "Capybara", "水豚", "Capybara", "Hydrochoerus hydrochaeris",
     "哺乳纲", "湿地", "南美", -15.0, -60.0, "LC", "🐹", "herbivore",
     "世界上最大的啮齿类,半水生,以「佛系」姿态与所有动物和睦相处而成网红。"),
    ("llama", "Llama", "美洲驼", "Llama", "Lama glama",
     "哺乳纲", "山地", "南美", -16.0, -68.0, "LC", "🦙", "herbivore",
     "安第斯山脉的高原驮兽,印加文明的「骆驼」。性情温和,但被惹急了会吐口水。"),
    ("toucan", "Toco_toucan", "巨嘴鸟", "Toco Toucan", "Ramphastos toco",
     "鸟纲", "森林", "南美", -10.0, -50.0, "LC", "🦜", "omnivore",
     "南美热带雨林的标志,巨大空腔喙占体长 1/3,既能调温也能威慑、吃水果。"),
    ("green-anaconda", "Green_anaconda", "绿森蚺", "Green Anaconda", "Eunectes murinus",
     "爬行纲", "湿地", "南美", -5.0, -65.0, "LC", "🐍", "carnivore",
     "世界最重的蛇,长 5-6 米、重达 250 公斤。栖息亚马逊沼泽,伏击鳄类与水豚。"),

    # ---- 欧洲(3) ----
    ("red-fox", "Red_fox", "赤狐", "Red Fox", "Vulpes vulpes",
     "哺乳纲", "森林", "欧洲", 50.0, 10.0, "LC", "🦊", "omnivore",
     "全球分布最广的食肉目动物,适应力极强,从欧洲森林到伦敦街头都有踪迹。"),
    ("european-bison", "European_bison", "欧洲野牛", "European Bison", "Bison bonasus",
     "哺乳纲", "森林", "欧洲", 52.5, 23.5, "NT", "🐂", "herbivore",
     "欧洲最大陆生动物,20 世纪一度野外灭绝,经动物园繁育重新引入波兰原始森林。"),
    ("eurasian-lynx", "Eurasian_lynx", "欧亚猞猁", "Eurasian Lynx", "Lynx lynx",
     "哺乳纲", "森林", "欧洲", 60.0, 25.0, "LC", "🐈", "carnivore",
     "中型猫科,耳尖黑色簇毛、短尾,擅长在深雪中追猎狍子与兔。"),

    # ---- 非洲(10) ----
    ("african-elephant", "African_elephant", "非洲象", "African Bush Elephant", "Loxodonta africana",
     "哺乳纲", "草原", "非洲", -1.3, 36.8, "EN", "🐘", "herbivore",
     "陆地现存最大动物,成年体重 6 吨。复杂的社会结构与长期记忆,因象牙盗猎而濒危。"),
    ("giraffe", "Giraffe", "长颈鹿", "Giraffe", "Giraffa camelopardalis",
     "哺乳纲", "草原", "非洲", -3.0, 35.0, "VU", "🦒", "herbivore",
     "最高的陆生动物,雄性可达 5.5 米。45 厘米深紫色舌头、心脏重达 11 公斤。"),
    ("lion", "Lion", "狮子", "Lion", "Panthera leo",
     "哺乳纲", "草原", "非洲", -2.0, 35.0, "VU", "🦁", "carnivore",
     "「草原之王」,唯一群居的大型猫科。母狮负责狩猎、公狮护卫领地与幼崽。"),
    ("leopard", "Leopard", "豹", "Leopard", "Panthera pardus",
     "哺乳纲", "草原", "非洲", -5.0, 30.0, "VU", "🐆", "carnivore",
     "九条命的大猫,可拖动两倍体重的猎物上树。从非洲到俄罗斯远东都有分布。"),
    ("cheetah", "Cheetah", "猎豹", "Cheetah", "Acinonyx jubatus",
     "哺乳纲", "草原", "非洲", -3.0, 36.0, "VU", "🐱", "carnivore",
     "陆地最快动物,3 秒加速到 100 km/h,但仅能维持 20 秒。爪不能完全收缩。"),
    ("zebra", "Plains_zebra", "平原斑马", "Plains Zebra", "Equus quagga",
     "哺乳纲", "草原", "非洲", -2.0, 34.0, "NT", "🦓", "herbivore",
     "非洲草原标志性条纹马,每只斑纹独一无二。条纹可迷惑天敌、驱赶舌蝇。"),
    ("hippopotamus", "Hippopotamus", "河马", "Hippopotamus", "Hippopotamus amphibius",
     "哺乳纲", "湿地", "非洲", -1.0, 31.0, "VU", "🦛", "herbivore",
     "陆地第三大动物,看似温和实则非洲最致命大型动物之一。每天泡水 16 小时。"),
    ("white-rhinoceros", "Ceratotherium_simum", "白犀牛", "White Rhinoceros", "Ceratotherium simum",
     "哺乳纲", "草原", "非洲", -25.0, 28.0, "NT", "🦏", "herbivore",
     "现存第二大陆地动物,北方亚种仅存 2 头雌性。武装巡逻仍难阻角的盗猎。"),
    ("chimpanzee", "Chimpanzee", "黑猩猩", "Chimpanzee", "Pan troglodytes",
     "哺乳纲", "森林", "非洲", 0.0, 25.0, "EN", "🐵", "omnivore",
     "与人类基因相似度 98.8%,会用工具捕白蚁、打猎、识别自己镜像。"),
    ("mountain-gorilla", "Mountain_gorilla", "山地大猩猩", "Mountain Gorilla", "Gorilla beringei beringei",
     "哺乳纲", "森林", "非洲", -1.5, 29.5, "EN", "🦍", "herbivore",
     "现存最大灵长目,只生活在卢旺达、刚果与乌干达的火山雨林,野外仅 1000 余只。"),

    # ---- 亚洲(10) ----
    ("giant-panda", "Giant_panda", "大熊猫", "Giant Panda", "Ailuropoda melanoleuca",
     "哺乳纲", "森林", "亚洲", 30.5, 103.0, "VU", "🐼", "herbivore",
     "中国特有物种,99% 食物为竹子,但消化系统仍是食肉动物结构。"),
    ("siberian-tiger", "Siberian_tiger", "西伯利亚虎", "Siberian Tiger", "Panthera tigris altaica",
     "哺乳纲", "森林", "亚洲", 45.0, 135.0, "EN", "🐅", "carnivore",
     "现存最大猫科,生活在俄罗斯远东与中国东北针叶林。野外仅存约 500 只。"),
    ("orangutan", "Bornean_orangutan", "红毛猩猩", "Bornean Orangutan", "Pongo pygmaeus",
     "哺乳纲", "森林", "亚洲", 1.0, 114.0, "CR", "🦧", "omnivore",
     "唯一亚洲大型类人猿,与人类基因相似度 97%。因棕榈油产业砍伐而极度濒危。"),
    ("snow-leopard", "Snow_leopard", "雪豹", "Snow Leopard", "Panthera uncia",
     "哺乳纲", "山地", "亚洲", 35.0, 85.0, "VU", "🐆", "carnivore",
     "高山雪线之王,生活在 3000-5500 米的中亚山脉。粗厚长尾既保暖又平衡。"),
    ("asian-elephant", "Asian_elephant", "亚洲象", "Asian Elephant", "Elephas maximus",
     "哺乳纲", "森林", "亚洲", 12.0, 78.0, "EN", "🐘", "herbivore",
     "比非洲象略小,雌性通常无外露象牙。被驯化已逾 4000 年,印度文化的象征。"),
    ("indian-rhinoceros", "Indian_rhinoceros", "印度犀", "Indian Rhinoceros", "Rhinoceros unicornis",
     "哺乳纲", "湿地", "亚洲", 27.0, 84.0, "VU", "🦏", "herbivore",
     "印度与尼泊尔湿地的「独角兽」,皮肤厚褶如铠甲。鼻角粉末在亚洲传统医学中价值连城。"),
    ("king-cobra", "King_cobra", "眼镜王蛇", "King Cobra", "Ophiophagus hannah",
     "爬行纲", "森林", "亚洲", 15.0, 100.0, "VU", "🐍", "carnivore",
     "世界最长毒蛇,长达 5.5 米。主食其它蛇类,毒液一次注射量可杀死大象。"),
    ("red-panda", "Red_panda", "小熊猫", "Red Panda", "Ailurus fulgens",
     "哺乳纲", "森林", "亚洲", 28.0, 90.0, "EN", "🐾", "herbivore",
     "喜马拉雅东侧山林精灵,独立科。同样吃竹但与大熊猫无亲缘,毛茸大尾保暖。"),
    ("bactrian-camel", "Bactrian_camel", "双峰驼", "Bactrian Camel", "Camelus bactrianus",
     "哺乳纲", "沙漠", "亚洲", 42.0, 95.0, "CR", "🐪", "herbivore",
     "戈壁沙漠的「船」,两个驼峰储脂、可一周不饮水。野生种群不足 1000 只。"),
    ("komodo-dragon", "Komodo_dragon", "科莫多巨蜥", "Komodo Dragon", "Varanus komodoensis",
     "爬行纲", "森林", "亚洲", -8.5, 119.5, "EN", "🦎", "carnivore",
     "世界最大蜥蜴,3 米长 70 公斤。咬合带毒,可猎杀水牛。仅生活在印尼几座岛。"),

    # ---- 澳洲(5) ----
    ("red-kangaroo", "Red_kangaroo", "红袋鼠", "Red Kangaroo", "Osphranter rufus",
     "哺乳纲", "草原", "澳洲", -25.0, 134.0, "LC", "🦘", "herbivore",
     "澳大利亚最大有袋类,跳跃时速 70 km、一跃 9 米。育儿袋可同时养不同阶段幼崽。"),
    ("koala", "Koala", "考拉", "Koala", "Phascolarctos cinereus",
     "哺乳纲", "森林", "澳洲", -33.0, 150.0, "VU", "🐨", "herbivore",
     "澳洲东岸的有袋树栖动物,一天睡 20 小时,只吃桉树叶。2019 山火后种群骤减。"),
    ("platypus", "Platypus", "鸭嘴兽", "Platypus", "Ornithorhynchus anatinus",
     "哺乳纲", "湿地", "澳洲", -35.0, 148.0, "NT", "🦫", "carnivore",
     "鸭嘴+海狸尾+水獭脚+下蛋的哺乳动物。雄性后腿带毒刺。澳洲东部河流原住民。"),
    ("tasmanian-devil", "Tasmanian_devil", "袋獾", "Tasmanian Devil", "Sarcophilus harrisii",
     "哺乳纲", "森林", "澳洲", -42.0, 146.5, "EN", "😈", "carnivore",
     "塔斯马尼亚岛特有的有袋食肉动物,叫声凄厉故得名「魔鬼」。面部肿瘤病威胁存续。"),
    ("emu", "Emu", "鸸鹋", "Emu", "Dromaius novaehollandiae",
     "鸟纲", "草原", "澳洲", -28.0, 135.0, "LC", "🪶", "omnivore",
     "澳洲特有,世界第二大鸟,身高 1.9 米。不能飞但奔跑时速 50 公里。"),

    # ---- 海洋(5) ----
    ("blue-whale", "Blue_whale", "蓝鲸", "Blue Whale", "Balaenoptera musculus",
     "哺乳纲", "海洋", "海洋", -50.0, -150.0, "EN", "🐋", "carnivore",
     "地球史上最大动物,长 30 米、重 200 吨,心脏如小汽车。19 世纪捕鲸几近灭绝。"),
    ("orca", "Orca", "虎鲸", "Orca", "Orcinus orca",
     "哺乳纲", "海洋", "海洋", 60.0, -150.0, "LC", "🐳", "carnivore",
     "「杀人鲸」实为大型海豚,顶级海洋捕食者,会团队捕猎甚至袭击大白鲨。"),
    ("whale-shark", "Whale_shark", "鲸鲨", "Whale Shark", "Rhincodon typus",
     "鱼纲", "海洋", "海洋", 0.0, 80.0, "EN", "🦈", "piscivore",
     "现存最大鱼类,长 12 米,与名字相反性情极温和,滤食浮游生物与小鱼。"),
    ("great-white-shark", "Great_white_shark", "大白鲨", "Great White Shark", "Carcharodon carcharias",
     "鱼纲", "海洋", "海洋", -34.5, 19.0, "VU", "🦈", "carnivore",
     "顶级海洋捕食者,可达 6 米。能跃出水面攻击海豹,因电影《大白鲨》而臭名远扬。"),
    ("sea-turtle", "Green_sea_turtle", "绿海龟", "Green Sea Turtle", "Chelonia mydas",
     "爬行纲", "海洋", "海洋", 18.0, -77.0, "EN", "🐢", "herbivore",
     "全球热带海域分布,寿命超 80 年。雌性回到自己出生的沙滩产卵,误食塑料致死频发。"),
]


def build():
    items = []
    for tup in ANIMALS:
        items.append(dict(zip(FIELDS, tup)))
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(items)} animals -> {OUT}")


if __name__ == "__main__":
    build()
