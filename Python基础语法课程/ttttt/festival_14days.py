# -*- coding: utf-8 -*-
"""
=====================================================================
  十四天后的校园祭  ——  在终端里玩的少女养成游戏
=====================================================================
 运行：  python festival_14days.py              # 正常玩
        python festival_14days.py --no-color     # 关掉颜色

 玩法一句话：十四天后要在校园祭上台演出。每天两个时段，你要在
 「练琴 / 和阿栗合奏 / 打工 / 复习 / 休息 / 请她吃甜品」里做选择。

 真正的难点不是练得多狠，而是——
   · 体力：用完会当众晕倒，白白浪费一整天
   · 心情：太低练习效率砍半，太高又会飘
   · 学业：低于 40 分，妈妈会把你禁足
   · 阿栗：她也有体力和心情。你一直自己练，她会难过；你一直拉她合奏，
           她会累垮；她心情掉到底，这段搭档关系就结束了
 演出评分 = 琴技 + 默契，但你得先保证那天台上是两个人。

 代码里用的都是 Python 基础语法，正好可以和课程对上：
   变量与类型 / 字符串与格式化 / 运算符与表达式  → 第 1~2 课
   列表、字典、列表套字典                        → 第 3~5 课概念组
   while / for / if-elif-else 控制流
=====================================================================
"""

import os
import random
import sys

# ---------------------------------------------------------------------
# 第 0 节：让 Windows 终端也能正常显示方块字符和颜色
# ---------------------------------------------------------------------
try:
    sys.stdout.reconfigure(encoding="utf-8")      # type: ignore # 防止 GBK 终端认不出 █ ░ ♥
except Exception:
    pass

USE_COLOR = sys.stdout.isatty() and "--no-color" not in sys.argv
if os.name == "nt" and USE_COLOR:
    try:
        os.system("")                             # 打开 Windows 控制台的 ANSI 支持
    except Exception:
        pass


def c(text, code):
    """给文字上色。USE_COLOR 为 False 时原样返回，方便重定向到文件"""
    return "\033[" + code + "m" + str(text) + "\033[0m" if USE_COLOR else str(text)


PINK, CYAN, YELLOW, GREEN, GRAY, BOLD = "95", "96", "93", "92", "90", "1"
LINE = "─" * 62
HEAVY = "═" * 62


# ---------------------------------------------------------------------
# 第 1 节：数据 —— 全是「列表套字典」，想改游戏内容只需要动这一块
# ---------------------------------------------------------------------

# 六个行动。每个行动是一本字典：
#   "你"   -> 你自己的数值变化（固定值）
#   "阿栗" -> 搭档的数值变化（固定值）
#   "涨"   -> 会随心情打折/加成的成长值，写成 (最小, 最大) 元组
ACTS = [
    {"键": "1", "名称": "自己一个人练琴",
     "提示": "琴技涨得快，但一个人练，阿栗会觉得被冷落",
     "你":   {"体力": -14, "心情": -4},
     "阿栗": {"体力": 0,   "心情": -1},
     "涨":   {"琴技": (7, 11), "默契": 0}},

    {"键": "2", "名称": "和阿栗一起合奏",
     "提示": "默契涨得最快，她也会开心，但两个人都累",
     "你":   {"体力": -12, "心情": -2},
     "阿栗": {"体力": -12, "心情": 3},
     "涨":   {"琴技": (2, 4), "默契": (7, 10)}},

    {"键": "3", "名称": "去便利店打工",
     "提示": "赚 50 元，很累，心情也会变差",
     "你":   {"体力": -16, "心情": -6, "零花": 50},
     "阿栗": {"体力": 0,   "心情": 0},
     "涨":   {"琴技": 0, "默契": 0}},

    {"键": "4", "名称": "老老实实复习功课",
     "提示": "学业低于 40 会被禁足，这是妈妈的底线",
     "你":   {"体力": -8, "心情": -3, "学业": 10},
     "阿栗": {"体力": 0,  "心情": 0},
     "涨":   {"琴技": 0, "默契": 0}},

    {"键": "5", "名称": "躺平休息",
     "提示": "回体力和心情，什么都没干的一天",
     "你":   {"体力": 26, "心情": 12},
     "阿栗": {"体力": 0,  "心情": 0},
     "涨":   {"琴技": 0, "默契": 0}},

    {"键": "6", "名称": "请阿栗吃甜品",
     "提示": "花 30 元，她的体力和心情一起回来",
     "你":   {"心情": 4, "零花": -30},
     "阿栗": {"体力": 10, "心情": 14},
     "涨":   {"琴技": 0, "默契": 0}},
]

# 随机事件。每天开始时 45% 的概率发生一件，十四天内不重复。
# "特殊" 那一项交给 handle_event() 里的 if/elif 处理。
EVENTS = [
    {"名称": "断掉的琴弦",
     "文": "一弦在最响的地方断了。",
     "特殊": "string"},

    {"名称": "阿栗的数学",
     "文": "阿栗数学考砸了，她妈妈今天把她锁在家里补课。",
     "特殊": "hari_lock", "阿栗": {"心情": -5}},

    {"名称": "大方的客人",
     "文": "便利店里有个大叔买了两条烟，把找零都留给了你。",
     "你": {"零花": 30}},

    {"名称": "楼下的阿姨",
     "文": "楼下阿姨上楼敲门：姑娘，能不能别在晚上弹琴。",
     "你": {"心情": -6}},

    {"名称": "深夜刷到的视频",
     "文": "你刷到一个和你同年的女孩在街头演出，看了三遍。",
     "你": {"琴技": 3, "心情": 5}},

    {"名称": "感冒了",
     "文": "早上起来鼻子堵得厉害，嗓子也哑了。",
     "你": {"体力": -15, "心情": -4}},

    {"名称": "阿栗发来的 demo",
     "文": "半夜十二点，阿栗发来一段她自己录的旋律，只有二十秒。",
     "你": {"心情": 6}, "阿栗": {"心情": 6}},

    {"名称": "临时加课",
     "文": "班主任宣布下午加两节自习，今天只剩一个时段了。",
     "特殊": "short_day"},
]

ENDING_TEXT = [
    (105, "校园祭的传说",
     ["第一段前奏下去，前排就安静了。",
      "副歌的时候，台下有人跟着哼。你听见阿栗在你右边笑了。",
      "结束的那一下，掌声比你想象中长得多。",
      "后来有人在学校的贴吧里发帖：今天下午三点的那个乐队，是谁？"]),

    (88, "台下有人哭了",
     ["上台前你们的手都是凉的，第一个和弦还弹呲了一下。",
      "但到了第二段，两个人忽然就对了。",
      "散场以后，有个一年级的女生跑过来问你们叫什么名字。",
      "阿栗说：我们还没有名字。那就先这样吧。"]),

    (70, "副歌很响",
     ["整体还算稳，只有中间一段两个人差点没跟上。",
      "台下有人在玩手机，也有几个人在听。",
      "阿栗下台以后说：比我想的好。她说这话的时候在笑。",
      "你决定相信她。"]),

    (50, "音响接触不良",
     ["音箱的线接触不良，你的琴声时断时续。",
      "阿栗一直在看你，你不敢看她。",
      "三首曲子，二十一分钟，很快就过去了。",
      "没有人说什么。回教室的路上你们走得很慢。"]),

    (0, "那个没人记得的节目",
     ["你们确实上台了。台下大概站了三十个人。",
      "第一首弹到一半，你听见自己手里的声音是散的，两个人不在一个拍子上。",
      "阿栗试着跟上你，但是没跟上。",
      "结束的时候有稀稀拉拉的几下掌声。你们鞠躬，下台。"]),
]


# ---------------------------------------------------------------------
# 第 2 节：小工具函数
# ---------------------------------------------------------------------

def rnd(value):
    """如果一个值是 (最小, 最大) 元组，就随机取一个；否则直接用。
    这是本游戏里最常用的一行代码，用来演示 isinstance 和元组解包。"""
    if isinstance(value, tuple):
        return random.randint(value[0], value[1])
    return value


def clamp(person, key, low=0, high=100):
    """把数值限制在合理范围内（体力不会变成负数，也不会超过 100）"""
    person[key] = max(low, min(high, person[key]))


def bar(cur, maximum=100, width=10):
    """把数值画成进度条：整除算出实心格数，字符串乘法拼出来"""
    cur = max(0, min(maximum, cur))
    filled = round(cur / maximum * width)
    return "█" * filled + "░" * (width - filled)


def add(person, changes):
    """把一本字典里的变化量加到某个人身上，并顺手做范围限制"""
    for key, delta in changes.items():
        person[key] = person.get(key, 0) + delta
        if key in ("体力", "心情"):
            clamp(person, key)


# ---------------------------------------------------------------------
# 第 3 节：显示
# ---------------------------------------------------------------------

def show_intro():
    print(c(HEAVY, PINK))
    print(c("           十 四 天 后 的 校 园 祭", BOLD))
    print(c(HEAVY, PINK))
    print()
    print("  你今年高二。书包侧袋里插着一把二手的吉他，三千二百块。")
    print("  校园祭还有十四天，你和阿栗报了名。全校一共两个节目。")
    print()
    print(c("  阿栗：「就我们两个人？也行。」", CYAN))
    print()
    print("  每天有两个时段。十四天之后，你们要上台。")
    print("  记住两件事：你自己会累，阿栗也会累。")
    print()
    print(c(LINE, GRAY))


def show_status(day, slot, you, hari, hari_lock, grounded):
    left = 14 - day + 1
    print()
    print(c(HEAVY, PINK))
    print("  第 " + str(day) + " 天 · " + slot + "           " +
          c("距离演出还有 " + str(left) + " 天", YELLOW))
    print(c(HEAVY, PINK))

    print("  " + c(you["名"], BOLD) + "　体力 " + bar(you["体力"]) + " " +
          c(you["体力"], GREEN) + "　心情 " + bar(you["心情"]) + " " +
          c(you["心情"], PINK))
    print("  　　　琴技 " + str(you["琴技"]) + "　默契 " + str(you["默契"]) +
          "　学业 " + c(you["学业"], YELLOW if you["学业"] < 45 else GRAY) +
          "　零花 " + str(you["零花"]) + " 元")

    mood_word = ("状态不错" if hari["心情"] >= 70 else
                 "有点敷衍" if hari["心情"] >= 40 else
                 "很没精神" if hari["心情"] >= 20 else "一句话都不想说")
    print("  " + c(hari["名"], BOLD) + "　体力 " + bar(hari["体力"]) + " " +
          c(hari["体力"], GREEN) + "　心情 " + bar(hari["心情"]) + " " +
          c(hari["心情"], PINK) + "　" + c(mood_word, GRAY))

    if grounded:
        print("  " + c("※ 你今天被禁足了，只能复习功课。", YELLOW))
    elif hari_lock:
        print("  " + c("※ 阿栗今天不在，合奏用不了。", YELLOW))
    print(c(LINE, GRAY))


def show_menu(you, hari, hari_lock, grounded):
    print("  今天能做什么：")
    for act in ACTS:
        usable = True
        note = ""
        if grounded and act["键"] != "4":
            usable = False
            note = "（禁足中）"
        if act["键"] == "2":
            if hari_lock:
                usable, note = False, "（阿栗今天不在）"
            elif hari["体力"] < 10:
                usable, note = False, "（阿栗太累了，先让她歇会儿）"
        if act["键"] == "6" and you["零花"] < 30:
            usable, note = False, "（钱不够 30 元）"

        head = "   " + act["键"] + ". " + act["名称"]
        padding = " " * max(2, 22 - len(act["名称"]) * 2)
        if usable:
            print(head + padding + c(act["提示"], GRAY))
        else:
            print(c(head + padding + "—— " + note, GRAY))
    print()


def ask(valid, blocked=None):
    """读一个选项。这里演示 try / except：输入不是数字会抛 ValueError，抓住它重来。
    选了暂时不能做的行动，会告诉你原因，而不是让你莫名其妙丢掉一个时段。"""
    tries = 0
    while tries < 6:
        text = input("  选择 > ").strip()
        try:
            number = int(text)
        except ValueError:
            print(c("  「" + text + "」不是数字，重新输入吧。", YELLOW))
            tries += 1
            continue

        if number in valid:
            return number
        if blocked and number in blocked:
            print(c("  " + blocked[number], YELLOW))
            tries += 1
            continue

        print(c("  只能输入 " + " / ".join(str(v) for v in valid) + "。", YELLOW))
        tries += 1

    print(c("  算了，你在琴房里发了会儿呆，这个时段就这么过去了。", GRAY))
    return None


# ---------------------------------------------------------------------
# 第 4 节：一个时段的行动
# ---------------------------------------------------------------------

def do_act(act, day, you, hari):
    """执行一个行动，返回要打印的几行字"""
    lines = []

    # 心情好，练习效率高；心情差，练了也白练
    mood = you["心情"]
    if mood >= 75:
        eff, mood_note = 1.2, "你今天手感很好"
    elif mood >= 50:
        eff, mood_note = 1.0, ""
    elif mood >= 30:
        eff, mood_note = 0.85, "你有点提不起劲"
    else:
        eff, mood_note = 0.65, "你几乎是在硬撑"

    # 阿栗心情很差的时候，合奏也带不动
    hari_flat = act["键"] == "2" and hari["心情"] < 20
    if hari_flat:
        eff *= 0.5

    add(you, act["你"])
    add(hari, act["阿栗"])

    gained = []
    for key, value in act["涨"].items():
        amount = round(rnd(value) * eff)
        if amount:
            you[key] += amount
            gained.append(key + " +" + str(amount))

    lines.append("  ▸ " + act["名称"] + ("……" if not gained else " —— " +
                 "、".join(gained)))
    if mood_note and gained:
        lines.append("    " + c("（" + mood_note + "，效率 " + str(round(eff, 2)) + " 倍）", GRAY))
    if hari_flat:
        lines.append("    " + c("（阿栗明显没在状态，你听见她漏了两个音）", GRAY))

    # 心情和体力一起见底，就会当众晕倒
    if you["体力"] <= 5 and you["心情"] < 25:
        lines.append("    " + c("你觉得眼前发黑，扶着琴架蹲了下去。", PINK))
    return lines


def end_of_day(you, hari, ignored_days, did_ensemble):
    """每天结束时的自然变化：学业会退步，阿栗自己会恢复一点体力，但也会慢慢失落。
    返回 (要打印的文字, 新的「被冷落天数」)"""
    you["学业"] -= 3
    hari["体力"] += 8
    hari["心情"] -= 2
    clamp(hari, "体力")
    clamp(hari, "心情")

    lines = []
    if you["学业"] < 40:
        lines.append(c("  妈妈翻了你的成绩单：这周别想出门了。", YELLOW))

    # 连续几天没和她一起练，她会开始怀疑自己是不是被嫌弃了
    ignored_days = 0 if did_ensemble else ignored_days + 1
    if ignored_days >= 2:
        hari["心情"] -= 12
        lines.append(c("  阿栗：你是不是……不太想和我一起练了。", PINK))
        lines.append("  " + c("（你已经 " + str(ignored_days) + " 天没和她合奏，她心情大跌）", GRAY))
        ignored_days = 0

    return lines, ignored_days


# ---------------------------------------------------------------------
# 第 5 节：随机事件
# ---------------------------------------------------------------------

def handle_event(event, you, hari):
    """把一件随机事件的效果落到数值上。返回 (要打印的文字, 是否锁住合奏, 是否只有一节课)"""
    lines = [c("  ★ 突发事件：" + event["名称"], YELLOW), "    " + event["文"]]

    add(you, event.get("你", {}))
    add(hari, event.get("阿栗", {}))

    for key, value in event.get("你", {}).items():
        if key in ("体力", "心情", "琴技", "零花"):
            lines.append("    " + c("你的" + key + " " + ("+" if value > 0 else "") + str(value), GRAY))

    hari_lock = False
    short_day = False

    special = event.get("特殊")
    if special == "string":                     # 断弦：花钱换，或者凑合
        if you["零花"] >= 20:
            you["零花"] -= 20
            lines.append("    你跑去琴行换了一根新弦，花了 20 元。")
        else:
            you["琴技"] = max(0, you["琴技"] - 4)
            lines.append(c("    身上没钱，你用胶带缠了缠，音有点飘。琴技 -4", GRAY))
    elif special == "hari_lock":
        hari_lock = True
        lines.append(c("    今天阿栗来不了，合奏用不了。", YELLOW))
    elif special == "short_day":
        short_day = True
        lines.append(c("    今天只剩一个时段。", YELLOW))

    return lines, hari_lock, short_day


# ---------------------------------------------------------------------
# 第 6 节：演出与结局
# ---------------------------------------------------------------------

def show_concert(you, hari):
    """算出最终分数，演一场戏，然后给结局"""
    print()
    print(c(HEAVY, PINK))
    print(c("  第 14 天 · 校园祭 · 下午三点", BOLD))
    print(c(HEAVY, PINK))
    print()

    score = round((you["琴技"] + you["默契"]) / 2 + random.randint(-4, 8))

    print("  后台的走廊很短，你走了很久才走到尽头。")
    print("  阿栗把琴背带往上提了提，看你一眼。")
    print()
    print("  琴技 " + str(you["琴技"]) + "　默契 " + str(you["默契"]) +
          "　→　" + c("演出评分 " + str(score), PINK + ";" + BOLD))
    print()

    # 先把坏结局挑出来：搭档没了，弹得再好也没用
    if hari["心情"] < 20:
        print(c(LINE, GRAY))
        print(c("  结局：两个人的乐队，只剩一个人", BOLD))
        print()
        print("  阿栗上台了，但整场没有看你一次。")
        print("  曲子是完整的，每一个音都在，就是不像两个人的东西。")
        print("  谢幕的时候她先走了。第二天她把社团的钥匙放在你桌上。")
        print()
        print(c("  （琴技 " + str(you["琴技"]) + "，默契 " + str(you["默契"]) +
                "。你练得很好，但你把搭档练没了。）", GRAY))
        return

    for threshold, title, text in ENDING_TEXT:
        if score >= threshold:
            print(c(LINE, GRAY))
            print(c("  结局：" + title, BOLD))
            print()
            for row in text:
                print("  " + row)
            print()
            print(c("  最终：琴技 " + str(you["琴技"]) + "　默契 " + str(you["默契"]) +
                    "　学业 " + str(you["学业"]) + "　零花 " + str(you["零花"]) + " 元", GRAY))
            if hari["心情"] >= 70:
                print(c("  阿栗的心情一直很好。这大概比评分更重要。", GRAY))
            return


# ---------------------------------------------------------------------
# 第 7 节：主流程
# ---------------------------------------------------------------------

def make_people():
    """开场输入名字，返回 (你, 阿栗) 两本字典"""
    raw = input("  你的名字（直接回车 = 林小满）：").strip()
    you = {"名": raw if raw else "林小满",
           "体力": 100, "心情": 70, "琴技": 10, "默契": 5, "学业": 60, "零花": 40}
    hari = {"名": "阿栗", "体力": 100, "心情": 65}
    return you, hari


def play():
    show_intro()
    you, hari = make_people()

    pool = EVENTS[:]              # 复制一份事件表，用过的就抽走，十四天不重复
    random.shuffle(pool)

    ignored_days = 0
    sick_days = 0
    grounded = False

    for day in range(1, 15):
        hari_lock = False
        short_day = False
        did_ensemble = False

        # 每天开场，有不到一半的概率撞上一件事（先算事件，再看当天状态）
        if pool and random.random() < 0.45:
            lines, hari_lock, short_day = handle_event(pool.pop(), you, hari)
            for row in lines:
                print(row)

        # 病倒的那一天什么都不用选，直接跳过去
        if sick_days > 0:
            sick_days -= 1
            show_status(day, "全天", you, hari, hari_lock, grounded)
            you["体力"] += 20
            you["心情"] -= 6
            clamp(you, "体力")
            clamp(you, "心情")
            print(c("  你裹着被子在家躺了一整天，什么也没干。", GRAY))
            continue

        slots = ["上午"] if short_day else ["上午", "下午"]
        for slot in slots:
            show_status(day, slot, you, hari, hari_lock, grounded)
            show_menu(you, hari, hari_lock, grounded)

            # 先算出这一时段能做什么、不能做的原因，再交给输入函数
            valid = []
            blocked = {}
            for act in ACTS:
                key = int(act["键"])
                if grounded and act["键"] != "4":
                    blocked[key] = "你今天被禁足了，只能复习功课。"
                elif act["键"] == "2" and hari_lock:
                    blocked[key] = "阿栗今天不在，合奏不了。"
                elif act["键"] == "2" and hari["体力"] < 10:
                    blocked[key] = "阿栗已经累到手指都在抖了，让她休息一天吧。"
                elif act["键"] == "6" and you["零花"] < 30:
                    blocked[key] = "你的钱包里只剩 " + str(you["零花"]) + " 元，甜品要 30 元。"
                else:
                    valid.append(key)

            choice = ask(valid, blocked)
            if choice is None:
                break

            act = [a for a in ACTS if a["键"] == str(choice)][0]
            for row in do_act(act, day, you, hari):
                print(row)

            if act["键"] == "2":
                did_ensemble = True

        if you["体力"] <= 0:
            you["体力"] = 0
            sick_days = 1
            print(c("  ！你倒下了，明天一整天都爬不起来。", PINK))

        lines, ignored_days = end_of_day(you, hari, ignored_days, did_ensemble)
        for row in lines:
            print(row)

        grounded = you["学业"] < 40
        if grounded:
            ignored_days = 0        # 被禁足这几天不算你冷落她

    show_concert(you, hari)


def main():
    print()
    while True:
        play()
        print()
        again = input("  再来一次？（输入 y = 再来一局，其他 = 结束）").strip().lower()
        print()
        if again not in ("y", "yes", "是", "再来"):
            print(c("  校园祭结束了。谢谢你陪她们走完这十四天。", PINK))
            print()
            return


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print()
        print(c("  （你先走了。十四天还没结束呢。）", GRAY))
        print()
