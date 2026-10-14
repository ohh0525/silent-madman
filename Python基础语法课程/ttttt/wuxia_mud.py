# -*- coding: utf-8 -*-
"""
=====================================================================
  迷你武侠 MUD 游戏  ——  Python 语法教学演示（函数 / 类 / 异常 / 表达式 / 类型）
=====================================================================
 运行：  python wuxia_mud.py            # 正常玩，全程手动输入
        python wuxia_mud.py --demo      # 自动演示，不需要输入

 这份代码不是"写游戏"，而是"用游戏讲语法"。每个功能都对应一个知识点：

   知识点              在代码里的位置
   ------------------------------------------------------------------
   1. 变量与数据类型    文件开头的全局数据 + show_type_lesson()
                        str 姓名 / int 血量 / float 攻击系数 / bool 存活
                        list 招式列表 / dict 招式书 / tuple 姓名表 / None 无
   2. 表达式与运算符    calc_damage()、render_bar()、resolve_hit()
                        算术 + - * / // % 、比较 > <=、逻辑 and or not
                        三元表达式、成员 in、格式化 f"{...:.1f}"
   3. 函数定义与调用    全篇。无返回值 / 返回单个值 / 返回元组 / 带默认参数
                        / 可变数量参数 *args（见 show_type_lesson 的 log 打印）
   4. 类与对象          Skill（招式）、Fighter（战斗单位）
   5. 继承              Hero（主角）与 Monster（怪物）都继承自 Fighter
   6. 异常处理          自定义异常家族 + try / except / else / finally / raise
   7. 控制流            while 战斗回合、for 关卡推进、if/elif 菜单分支
=====================================================================
"""

import random
import sys

# =====================================================================
# 第 0 节：全局数据 —— 顺手展示三种容器类型
# =====================================================================

XING = ("赵", "钱", "孙", "李", "周", "吴", "郑", "王", "慕容", "欧阳")   # tuple 元组：姓，内容固定不改
MING = ["天", "龙", "无", "忌", "云", "飞", "尘", "语", "风", "雪"]        # list 列表：名，可以增删改

SKILL_BOOK = {          # dict 字典：招式名 -> (威力, 内力消耗)，按键取值
    "回风拂柳剑": (12, 6),
    "打狗棒法": (15, 8),
    "一阳指": (18, 10),
    "金钟罩": (14, 7),
    "流云掌": (11, 5),
    "夺命连环腿": (17, 9),
}

MONSTER_BOOK = {        # dict 套 dict：怪物的模板数据
    "山贼":       {"hp": 42,  "mp": 12, "atk": 7.0,  "gold": 12},
    "黑风寨二当家": {"hp": 60,  "mp": 20, "atk": 9.0,  "gold": 20},
    "唐门刺客":    {"hp": 75,  "mp": 30, "atk": 11.0, "gold": 30},
    "魔教长老":    {"hp": 95,  "mp": 40, "atk": 13.0, "gold": 45},
    "武林盟主":    {"hp": 130, "mp": 60, "atk": 15.0, "gold": 99},
}

WEATHER = None          # None 类型：表示"没有值"，这里表示"今天没有特殊天气"


# =====================================================================
# 第 1 节：异常处理 —— 先定义自己的异常家族
# =====================================================================
# 思路：先写一个父异常 WuXiaError，其余都继承它。
# 这样调用方可以只写一句 except WuXiaError 就抓住所有游戏内错误。

class WuXiaError(Exception):
    """所有游戏异常的父类（继承内置的 Exception）"""

    def __init__(self, msg):
        super().__init__(msg)   # 交给父类保存信息
        self.msg = msg          # 自己再存一份，方便打印

    def __str__(self):
        return self.msg


class NotEnoughMp(WuXiaError):
    """内力不够，放不出招式"""


class NoPotion(WuXiaError):
    """药囊空空，没药可喝了"""


# 想加新的游戏错误？照上面这样再写一个子类就行，比如：
# class BattleOver(WuXiaError):
#     """战斗已经分出胜负，不该再出手"""


# =====================================================================
# 第 2 节：类与对象（一）—— Skill 招式
# =====================================================================

class Skill:
    """一个招式对象：有名字、威力、内力消耗"""

    def __init__(self, name, power, cost):
        # 下面三个都是"实例属性"，类型分别是 str / int / int
        self.name = name
        self.power = power
        self.cost = cost

    def __str__(self):
        """print(skill) 时显示的内容（特殊方法，也就是常说的魔术方法）"""
        return f"{self.name}（威力{self.power} · 耗内力{self.cost}）"

    def __repr__(self):
        return f"Skill('{self.name}')"


# =====================================================================
# 第 3 节：类与对象（二）—— Fighter 战斗单位，Hero 与 Monster 都是它的子类
# =====================================================================

class Fighter:
    """所有会打架的角色的共同部分（父类）"""

    def __init__(self, name, hp, mp, atk):
        self.name = name                 # str
        self.max_hp = hp                 # int 血量上限
        self.hp = hp                     # int 当前血量
        self.max_mp = mp                 # int 内力上限
        self.mp = mp                     # int 当前内力
        self.atk = atk                   # float 攻击系数
        self.skills = []                 # list 会的招式（里面装 Skill 对象）
        self.alive = True                # bool 是否活着

    # ---------- 三个"只读计算属性"，用来演示表达式 ----------
    @property
    def hp_ratio(self):
        """血量百分比，float；注意除号 / 得到小数，不用写 float() 转换"""
        return self.hp / self.max_hp

    @property
    def mp_ratio(self):
        return self.mp / self.max_mp

    @property
    def power_level(self):
        """综合战力 = 血 + 内力*0.5 + 攻击*3，演示算术表达式与运算符优先级"""
        return self.hp + self.mp * 0.5 + self.atk * 3

    # ---------- 行为方法 ----------
    def is_alive(self):
        """返回 bool：还活着吗"""
        return self.hp > 0

    def take_damage(self, dmg):
        """挨打：扣血并保证不为负，返回实际掉了多少血"""
        before = self.hp
        self.hp = max(0, self.hp - dmg)      # max() 防止血量为负
        self.alive = self.hp > 0
        return before - self.hp

    def spend_mp(self, cost):
        """花内力；不够就抛异常 —— 这是异常处理最典型的用法"""
        if cost > self.mp:
            raise NotEnoughMp(f"{self.name}内力不足（需要{cost}，只剩{self.mp}）")
        self.mp -= cost

    def restore_mp(self, amount):
        """调息回内力，演示 min() 封顶"""
        self.mp = min(self.max_mp, self.mp + amount)
        return self.mp

    def learn(self, skill):
        """学招式：已经会的就不重复学。
        返回学到的 Skill 对象；重复则返回 None（None 也是返回值的一种）"""
        known = [s.name for s in self.skills]    # 列表推导式：取出所有已会招式的名字
        if skill.name in known:                  # 成员运算符 in
            return None
        self.skills.append(skill)                # 列表追加元素
        return skill

    def pick_skill(self):
        """随机挑一个招式；不会招式就返回 None"""
        return random.choice(self.skills) if self.skills else None

    def status_line(self):
        """输出一行状态条，里面用到格式化表达式和对齐"""
        return (f"{self.name:<10} 气血 {render_bar(self.hp, self.max_hp)} "
                f"{self.hp:>3}/{self.max_hp:<3}  "
                f"内力 {render_bar(self.mp, self.max_mp, 12)} {self.mp:>3}/{self.max_mp:<3}")


class Hero(Fighter):
    """主角：比普通 Fighter 多了等级、经验、药囊、银两"""

    def __init__(self, name, hp=70, mp=30, atk=9.0):
        super().__init__(name, hp, mp, atk)   # 先把父类的初始化做掉
        self.level = 1                        # int
        self.exp = 0                          # int
        self.gold = 0                         # int
        self.potions = 3                      # int 药囊数量
        self.crit_rate = 0.15                 # float 暴击率

    def drink_potion(self):
        """喝药：没药就抛异常，让菜单去处理"""
        if self.potions <= 0:
            raise NoPotion(f"{self.name}摸了摸腰间，药囊已经空了")
        self.potions -= 1
        heal = int(self.max_hp * 0.35) + 8
        self.hp = min(self.max_hp, self.hp + heal)
        return heal

    def gain_exp(self, amount):
        """获得经验，够 30 点就升级。返回 True 表示升级了"""
        self.exp += amount
        if self.exp >= self.level * 30:
            self.level_up()
            return True
        return False

    def level_up(self):
        """升级：属性成长，并回满状态"""
        self.level += 1
        self.max_hp += 18
        self.max_mp += 6
        self.atk += 1.2                     # float 加法
        self.crit_rate = round(self.crit_rate + 0.02, 2)   # round 保留两位小数
        self.hp = self.max_hp
        self.mp = self.max_mp

    def show_detail(self):
        """一份角色面板，演示小数格式化与百分号格式化"""
        print("  +-------- 角色面板 --------")
        print(f"  | {self.name} · 第{self.level}级 · 银两{self.gold} · 经验{self.exp}/{self.level * 30}")
        print(f"  | 气血 {self.hp}/{self.max_hp}   内力 {self.mp}/{self.max_mp}")
        print(f"  | 攻击 {self.atk:.1f}   暴击 {self.crit_rate:.0%}   "
              f"药囊 {self.potions}   战力 {self.power_level:.1f}")
        for i, s in enumerate(self.skills, start=1):   # enumerate 带编号遍历
            print(f"  | 招式{i}：{s}")
        print("  +---------------------------")


class Monster(Fighter):
    """怪物：由模板生成，也有自己的出手逻辑"""

    def __init__(self, name, template):
        super().__init__(name, template["hp"], template["mp"], template["atk"])
        self.gold = template["gold"]

    def think(self, hero):
        """决定这一回合做什么，返回一个说明字符串。
        逻辑：内力够就优先进攻招式（打得更疼），否则普通攻击。
        说明：hero 当前未用到，是预留的接口参数 —— 将来可以"看主角残血就更凶狠"，
              现在先保留，让调用处不必再改。"""
        skill = self.pick_skill()
        if skill is not None:
            try:
                self.spend_mp(skill.cost)       # 内力不够会抛异常
                return skill
            except NotEnoughMp:
                pass                            # 抓到了但不报错：安静降级为普通攻击
        return None                             # None 表示普通攻击


# =====================================================================
# 第 4 节：工具函数 —— 展示"函数可以有返回值 / 有默认参数 / 返回元组"
# =====================================================================

def render_bar(cur, mx, width=18):
    """把数值画成进度条字符串。演示：整除 // 、乘除表达式、字符串乘法"""
    filled = int(cur / mx * width)      # 百分比 * 宽度 -> 需要几个实心格
    filled = max(0, min(width, filled))  # 夹在 0 ~ width 之间，防止越界
    return "#" * filled + "-" * (width - filled)


def roll_name():
    """随机造一个江湖名字，返回 str。random.choice 从序列里随机取一个"""
    return random.choice(XING) + random.choice(MING) + random.choice(MING)


def roll_skill():
    """从招式书里随机抽一个招式，返回 Skill 对象"""
    name = random.choice(list(SKILL_BOOK.keys()))
    power, cost = SKILL_BOOK[name]      # 元组解包
    return Skill(name, power, cost)


def calc_damage(base_atk, skill_power=0, crit=False, defend=0):
    """
    伤害计算：完整的表达式演示。
      base_atk     : float 基础攻击
      skill_power  : int   招式附加威力，默认 0
      crit         : bool  是否暴击
      defend       : int   对方防御（减伤）
    返回 int 伤害值，最小为 1。
    """
    raw = base_atk * (0.85 + random.random() * 0.30) + skill_power - defend
    if crit:                        # bool 直接当条件用
        raw *= 1.8
    return max(1, int(raw))         # int() 显式类型转换


def resolve_hit(attacker, defender, skill=None):
    """
    判定一次出手是否命中。
    返回元组 (是否命中, 伤害, 是否暴击) —— 一个函数返回多个值，其实是返回元组。

    说明：defender 当前未参与计算（命中率只与进攻方和招式有关），
          保留它是为了接口对称，将来要加"按对方闪避/格挡修正"时不必改调用处。
    """
    miss_rate = 0.10 if skill is None else 0.18      # 三元表达式
    if random.random() < miss_rate:
        return (False, 0, False)                     # 未命中

    crit_rate = attacker.crit_rate if hasattr(attacker, "crit_rate") else 0.12
    crit = random.random() < crit_rate
    power = 0 if skill is None else skill.power
    dmg = calc_damage(attacker.atk, power, crit)
    return (True, dmg, crit)


def log(*args):
    """可变参数演示：*args 把任意多个参数收成一个元组，再逐个打印"""
    print(*args)


def pause(msg, io):
    """等待玩家按回车。演示"函数把另一个对象（io）当参数传进来"的写法"""
    io.raw(msg)


# =====================================================================
# 第 5 节：输入器 —— 集中演示 try / except 读入校验
# =====================================================================

class InputSource:
    """统一管理输入。--demo 模式下不读键盘，自动喂预设选项，方便课堂上快速演示"""

    def __init__(self, demo=False):
        self.demo = demo
        # 自动演示用的剧本：2=出招, 1=普攻, 3=调息, 4=喝药（循环使用）
        self.queue = [2, 1, 1, 4, 1, 2, 1, 3, 2, 1, 4, 1, 2, 2, 1, 1, 3, 2, 1] * 8

    def raw(self, prompt=""):
        """读取自由输入（名字、回车确认等）。演示模式一律当作「直接回车」"""
        if self.demo:
            print(f"{prompt}〔自动演示：回车〕")
            return ""
        return input(prompt)

    def choose(self, prompt, valid, default=None):
        """
        读取并校验一个菜单选项 —— 全文件里异常处理最值得看的一段。
        正常模式：int() 转换失败会抛 ValueError，被 except 抓住，提示后重来，最多三次。
        演示模式：直接从剧本里取下一个数字，不再读键盘。
        """
        if self.demo:
            choice = self.queue.pop(0) if self.queue else min(valid)   # 剧本用完就用第一个动作
            if choice not in valid:                                     # 越界就用 in 判断兜住
                choice = min(valid)
            print(f"{prompt}{choice}   〔自动演示〕")
            return choice

        for _ in range(3):                       # 最多给三次机会
            text = self.raw(prompt).strip()      # strip() 去掉首尾空格
            try:
                number = int(text)               # 这一步可能抛 ValueError
            except ValueError:
                print(f"  ·  「{text}」不是一个数字，请重新选择。（已捕获 ValueError）")
                continue                         # 跳过本次循环剩下的部分，重新输入
            if number not in valid:              # 没抛异常也不代表合法，还要自己判断范围
                print(f"  ·  只能输入 {' / '.join(str(v) for v in valid)} 哦。")
                continue
            return number

        print("  ·  连续输错三次，系统帮你选了一个。")
        return default if default is not None else min(valid)   # 三元表达式兜底


# =====================================================================
# 第 6 节：开局 —— 创建主角
# =====================================================================

def create_hero(io):
    """创建角色：演示 while True + 异常 + 输入校验的组合"""
    print("\n【创建你的角色】")
    print("  直接回车 = 随机取一个江湖名号，也可以自己输入（2~8 个字）")

    while True:
        name = io.raw("名号 > ").strip()     # raw() 内部处理了"读键盘 / 演示模式"的区别

        if not name:                       # 空字符串是"假值"，not "" 为 True
            name = roll_name()
            print(f"  天意如此，你就叫「{name}」吧。")
            break
        if len(name) > 8:
            print("  ·  名字太长了，江湖人记不住（最多 8 个字）。")
            continue
        break

    hero = Hero(name)
    while len(hero.skills) < 2:            # 反复随机，直到学会两招不重复的
        hero.learn(roll_skill())

    print("\n  你从山门走下，腰悬长剑。")
    hero.show_detail()
    return hero


def build_monsters():
    """按顺序生成 5 关的对手，返回列表（函数返回 list）"""
    stages = []
    for name, template in MONSTER_BOOK.items():
        monsters_per_stage = 2 if name in ("山贼", "黑风寨二当家") else 1
        for i in range(monsters_per_stage):
            title = name if monsters_per_stage == 1 else f"{name}{'甲乙丙丁'[i]}"
            stages.append(Monster(title, template))
    return stages


# =====================================================================
# 第 7 节：战斗系统
# =====================================================================

def show_menu(hero):
    """打印行动菜单，顺带显示自己的状态和会的招式"""
    print("\n" + "=" * 50)
    print(hero.status_line())
    print("  你会的招式：" + "、".join(str(s) for s in hero.skills))   # join 把列表拼成字符串
    print("  1.普通攻击(不耗内力)   2.运功出招   3.调息回内力")
    print(f"  4.饮酒疗伤(剩{hero.potions}颗)   5.三十六计走为上")
    print("=" * 50)


def hero_turn(hero, foe, io):
    """
    玩家回合：菜单 -> 选动作 -> 出错就回到菜单。
    except 里处理"动作无法完成"的情况，而不是让程序崩掉。
    """
    while True:
        show_menu(hero)
        choice = io.choose("你的选择 > ", [1, 2, 3, 4, 5], default=1)

        try:
            if choice == 1:
                name, hit, dmg, crit = strike(hero, foe, None)
                report(hero, foe, name, hit, dmg, crit)
                return "fight"

            elif choice == 2:
                skill = hero.pick_skill()
                if skill is None:
                    print("  ·  你还不会任何招式，只能用拳头。")
                    continue
                hero.spend_mp(skill.cost)           # 内力不够 -> 抛 NotEnoughMp
                name, hit, dmg, crit = strike(hero, foe, skill)
                report(hero, foe, name, hit, dmg, crit)
                return "fight"

            elif choice == 3:
                got = 6 + hero.level * 2
                hero.restore_mp(got)
                print(f"  ·  {hero.name}盘膝坐下，吐纳一周天，内力恢复 {got} 点。")
                return "rest"

            elif choice == 4:
                healed = hero.drink_potion()        # 没药 -> 抛 NoPotion
                print(f"  ·  {hero.name}仰头饮下疗伤药酒，气血恢复 {healed} 点。")
                return "drink"

            else:
                if random.random() < 0.55 + hero.level * 0.03:
                    print(f"  ·  {hero.name}施展轻功，一道烟似的消失在夜色里。")
                    return "flee"
                lost = int(hero.max_hp * 0.12)
                hero.take_damage(lost)
                print(f"  ·  转身太急，被{foe.name}在后背拍了一掌，掉了 {lost} 点气血！")
                return "fight"

        except (NotEnoughMp, NoPotion) as err:      # 一次抓住两种异常
            print(f"  ·  {err}")                    # 用 __str__ 打印异常内容
            continue                                # 回菜单重新选
        except WuXiaError as err:                   # 兜底：父类异常放最后
            print(f"  ·  出了点意外：{err}")
            continue


def strike(attacker, defender, skill):
    """一次出手，返回 (招式名, 是否命中, 伤害, 是否暴击) —— 注意返回了 4 个值"""
    hit, dmg, crit = resolve_hit(attacker, defender, skill)   # 元组解包
    if hit:
        defender.take_damage(dmg)
    return (skill.name if skill else "普通攻击", hit, dmg, crit)


def report(attacker, defender, name, hit, dmg, crit):
    """把一次攻击的结果打印出来"""
    if not hit:
        print(f"  ·  {attacker.name}一招「{name}」打出，被{defender.name}侧身闪开了。")
        return
    if crit:
        print(f"  ·  ★ 暴击！{attacker.name}一招「{name}」正中要害，{defender.name}吐血倒退 {dmg} 点！")
    else:
        print(f"  ·  {attacker.name}一招「{name}」命中，{defender.name}掉了 {dmg} 点气血。")


def monster_turn(monster, hero):
    """怪物回合，返回它用的招式名（可能为 None 表示普通攻击）"""
    skill = monster.think(hero)
    name, hit, dmg, crit = strike(monster, hero, skill)
    report(monster, hero, name, hit, dmg, crit)
    return name


def battle(hero, foe, stage, io):
    """
    一场战斗的主循环。
    返回 "win" / "lose" / "flee"。
    这里用 try / finally 保证不管怎么结束，都会打印一句收尾的话。
    """
    print("\n" + "★" * 50)
    print(f"  第 {stage} 战：{hero.name}  VS  {foe.name}")
    print("★" * 50)

    try:
        rounds = 0
        while hero.is_alive() and foe.is_alive():
            rounds += 1
            print(f"\n--- 第 {rounds} 回合 ---")
            print(foe.status_line())

            result = hero_turn(hero, foe, io)
            if result == "flee":
                return "flee"
            if not foe.is_alive():
                return "win"

            monster_turn(foe, hero)
            if not hero.is_alive():
                return "lose"

        # 循环正常走完（理论上上面的 return 已经先返回了）
        return "win" if hero.is_alive() else "lose"

    finally:
        # finally 无论如何都会执行，适合做收尾
        print(f"\n  〔{hero.name} 剩 {hero.hp} 点气血，{foe.name} 剩 {foe.hp} 点气血〕")


# =====================================================================
# 第 8 节：教学彩蛋 —— 一屏看懂变量类型
# =====================================================================

def show_type_lesson(hero):
    """把游戏里真实用到的数据拿出来看一眼类型，比干讲 type() 好懂"""
    print("\n【顺手看一眼：你的角色由哪些类型组成】")
    samples = [
        ("name",       hero.name,              "str   字符串：名字"),
        ("hp",         hero.hp,                "int   整数：气血"),
        ("atk",        hero.atk,               "float 小数：攻击系数"),
        ("alive",      hero.alive,             "bool  布尔：是否存活"),
        ("skills",     hero.skills[0],         "list  列表：招式可以有几个"),
        ("level",      hero.level,             "int   整数：等级"),
        ("crit_rate",  hero.crit_rate,         "float 小数：暴击率"),
        ("SKILL_BOOK", "…6 个招式…",            "dict  字典：按名字查威力"),
        ("XING",       XING,                   "tuple 元组：姓氏表不可改"),
        ("WEATHER",    WEATHER,                "None  空值：今天没有天气事件"),
    ]
    for key, value, tip in samples:            # 解包列表里的三元组
        print(f"  {key:<10} = {str(value)[:26]:<28} {tip}")
    print(f"\n  举个表达式：气血百分比 = {hero.hp} / {hero.max_hp} = {hero.hp_ratio:.1%}（float）")
    print(f"  再举个表达式：还能喝几口药 = 3 - {3 - hero.potions} = {hero.potions}（int）")


# =====================================================================
# 第 9 节：主流程
# =====================================================================

def show_banner():
    print("=" * 50)
    print("        江  湖  行  ·  迷你武侠 MUD 演示版")
    print("=" * 50)
    print("  你是初入江湖的少侠，前方五道关卡等着你。")
    print("  打得过就打，打不过就调息、喝药、或者跑。")
    print("-" * 50)


def main():
    demo = "--demo" in sys.argv            # 成员运算符 in
    io = InputSource(demo=demo)

    show_banner()
    hero = create_hero(io)
    show_type_lesson(hero)

    monsters = build_monsters()
    print(f"\n  前方共 {len(monsters)} 个对手，一路小心。")

    cleared = 0                            # int：已通关卡数
    for stage, foe in enumerate(monsters, start=1):
        outcome = battle(hero, foe, stage, io)

        if outcome == "flee":
            print(f"\n  {hero.name}退到山神庙歇了一夜，第二天继续赶路……")
            hero.restore_mp(hero.max_mp)
            hero.hp = min(hero.max_hp, hero.hp + 20)
            pause("（按回车继续闯关）", io)
            continue

        if outcome == "lose":
            print("\n" + "=" * 50)
            print(f"  {hero.name}力竭倒地…… 江湖路远，来日再战。")
            print(f"  本次共击败 {cleared} 名对手，等级 {hero.level}。")
            print("=" * 50)
            return                              # 结束程序

        # 以下是 win 的情况
        cleared += 1
        hero.gold += foe.gold
        print(f"\n  ✔ 击败{foe.name}！获得 {foe.gold} 两银子。")

        upgraded = hero.gain_exp(18 + stage * 4)
        if upgraded:
            print(f"  ★ 修为突破 —— 升到第 {hero.level} 级！")
        if random.random() < 0.6:               # 60% 概率捡到新招式
            new_skill = hero.learn(roll_skill())
            if new_skill is not None:           # 判断返回值是 None 还是对象
                print(f"  ★ 从{foe.name}身上搜到秘籍，习得「{new_skill.name}」！")
            else:
                print(f"  ·  从{foe.name}身上搜到一本秘籍，可惜你早已练熟。")
        hero.potions += 1
        hero.hp = min(hero.max_hp, hero.hp + int(hero.max_hp * 0.25))
        hero.show_detail()
        pause("（按回车继续）", io)

    print("\n" + "★" * 50)
    print(f"  你连过 {cleared} 关，江湖上开始流传「{hero.name}」的名字。")
    # 这里故意换一种写法：log() 用 *args 收参数，等效于上面那句 f-string
    log("  通关结算：", hero.name, "| 等级", hero.level,
        "| 银两", hero.gold, "| 招式", len(hero.skills), "个")
    print("★" * 50)


# 这句是 Python 的入门仪式：
# 只有"直接运行本文件"时才执行 main()，被别人 import 时不执行。
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  （你按了 Ctrl+C，江湖暂别。）")
    except EOFError:
        print("\n\n  （没有更多输入了，江湖暂别。）")
