#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成概念组「Python 第 1 课 · 下半场四概念」的配套可运行 Notebook。

对象：本组第 4 / 4 个概念 —— 列表套字典 = 一张表（List of Dicts）。
内容严格取自 `Python基础语法课程/learning-materials/列表套字典.html`，
术语服从该组骨架 `concept-group/python-lesson1-second-half/00-骨架.md` 的共享术语表。

不依赖 nbformat（环境未安装），直接构造 nbformat 4.5 的 JSON。
"""
import json
import os

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "Python基础语法课程",
    "notebooks",
)

_counter = {"n": 0}


def _cid():
    _counter["n"] += 1
    return "cell-%02d" % _counter["n"]


def md(text):
    return {
        "cell_type": "markdown",
        "id": _cid(),
        "metadata": {},
        "source": text.strip("\n").splitlines(keepends=True),
    }


def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": _cid(),
        "metadata": {},
        "outputs": [],
        "source": text.strip("\n").splitlines(keepends=True),
    }


def notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "mimetype": "text/x-python",
                "file_extension": ".py",
                "nbconvert_exporter": "python",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


# ----------------------------------------------------------------------------
# 03 · 概念组配套 Notebook：列表套字典 = 一张表
# ----------------------------------------------------------------------------
nb = []
_counter["n"] = 0

nb += [
    md(r"""
# Python 基础语法 · 第 1 课概念组

## 列表套字典 = 一张表（List of Dicts）

> 配套材料：`Python基础语法课程/learning-materials/列表套字典.html`
> 所属概念组：**Python 第 1 课 · 下半场四概念**（本组第 4 / 4）
> 先修：**运算符**、**列表**、**字典**（同组前三篇）
> 概念组索引：`concept-group/python-lesson1-second-half/index.html`

### 使用说明

1. **运行单元格**：选中单元格后按 `Shift + Enter` 运行并跳到下一个；按 `Ctrl + Enter` 运行但停在原地。
2. **按顺序运行**：请从第一个单元格开始，从上到下依次运行。后面的单元格依赖前面定义的变量。
3. **动手改**：看到代码先猜结果，再运行；然后把字段名和值改掉再跑一次，观察变化。

> ⚠️ 第 5 节里有一行**故意报错**的代码（讲"键必须一致"）。看到红色报错不要慌，那是设计好的。
"""),
    md(r"""
---

## 0. 先修自检

这一篇建立在两个你已经学过的容器之上：**列表**（按索引取）与**字典**（按键取）。先用两行代码确认手感。
"""),
    code(r"""
fruits = ["苹果", "香蕉", "梨"]
print(fruits[0])          # 列表：按索引取第一个

person = {"name": "小明", "score": 90}
print(person["name"])     # 字典：按键取
"""),
    md(r"""
**预期输出**

```
苹果
小明
```

- `fruits[0]` —— 列表按**索引**取，索引从 0 开始（完整规则见《列表》篇）。
- `person["name"]` —— 字典按**键**取（完整规则见《字典》篇）。

这一篇要做的事情只有一件：把这两件事**叠起来**。
"""),
    md(r"""
---

## 1. 一行数据 = 一个字典

一张表里的一行，其实是一组"**字段名 → 值**"的对应。姓名是"小明"、班级是"一班"、分数是 90 —— 有名字、有内容，这不正好就是字典吗？

于是一行数据这样写：
"""),
    code(r"""
row1 = {"name": "小明", "class": "一班", "score": 90}
row2 = {"name": "小红", "class": "二班", "score": 85}

print(row1)
print(row1["name"])       # 字段名随身带着，不用记"第几列"
print(row2["score"])
"""),
    md(r"""
**预期输出**

```
{'name': '小明', 'class': '一班', 'score': 90}
小明
85
```

关键在第二行 `row1["name"]`：**字段名和值是绑在一起存进去的**。这就是"字典适合装一行"的全部理由 —— 换成一串没有名字的值，你就只能靠脑记第几个位置是什么。
"""),
    md(r"""
---

## 2. 整张表 = 一个列表装多行

一行有了，多行怎么办？按顺序放进一个**列表**里 —— 列表有序、可增删，天然对应"表里有很多行，行的先后有意义"。

记得**在同一个单元格里一次性运行**下面这段，否则后面的单元格找不到变量。
"""),
    code(r"""
students = [
    {"name": "小明", "class": "一班", "score": 90},
    {"name": "小红", "class": "二班", "score": 85},
]

print("共", len(students), "行")
print(students[0]["name"], students[0]["score"])
print(students[1]["name"], students[1]["score"])
"""),
    md(r"""
**预期输出**

```
共 2 行
小明 90
小红 85
```

到这一步，一张表就立起来了。分工很干净：

| 谁 | 管什么 |
| --- | --- |
| 列表 `students` | 管"有哪几行、什么顺序" |
| 字典 | 管"每一行里每个字段叫什么、值是多少" |

两层各管一半，互不越界 —— 这就是整个结构的设计。
"""),
    md(r"""
---

## 3. 两层取值：先按位置找行，再按名字找字段

这是本结构最常用的动作。注意括号要写**两层**。
"""),
    code(r"""
print(students[0])              # 第 1 行（得到整个字典）
print(students[0]["name"])      # 第 1 行的 name 格
print(students[1]["score"])     # 第 2 行的 score 格
"""),
    md(r"""
**预期输出**

```
{'name': '小明', 'class': '一班', 'score': 90}
小明
85
```

读法就是人话的顺序：`students[0]["name"]` 念作"**第 1 行的姓名**"。

- 先 `students[0]` —— 用列表的**索引**找到第几行；
- 再 `["name"]` —— 用字典的**键**找到那一行里的哪个字段。

两层恰好把列表和字典的强项都用上了。常见的写法错误是只写一层，比如 `students["name"]` —— 那是拿"名字"去当行号，行不通。
"""),
    md(r"""
### 对照：为什么不用「列表套列表」

看看不用字典会怎样。
"""),
    code(r"""
rows_plain = [["小明", "一班", 90], ["小红", "二班", 85]]

print(rows_plain[0])
print(rows_plain[0][1])
"""),
    md(r"""
**预期输出**

```
['小明', '一班', 90]
一班
```

代码能跑，但 `rows_plain[0][1]` 这句你得**回头数**："索引 1 到底是班级还是分数？"

字段多起来之后，这种写法就没法看了 —— 这就是"列表套字典"存在的意义：**列表套列表会丢列名**。
"""),
    md(r"""
---

## 4. 增一行 / 改一格 / 删一行

认清一个规律，括号就不会写错：

- **整行层面**的操作 → 用**列表**的写法；
- **某一格**的修改 → 用**字典**的写法。

### 4.1 增一行（列表的写法）
"""),
    code(r"""
students.append({"name": "小刚", "class": "一班", "score": 78})

print("现在共", len(students), "行")
print(students[-1])       # -1 是最后一行
"""),
    md(r"""
**预期输出**

```
现在共 3 行
{'name': '小刚', 'class': '一班', 'score': 78}
```

`append` 是[列表](https://docs.python.org/zh-cn/3/tutorial/datastructures.html)的动作 —— 因为"多一行"是行层面的事。新行照样是一个字典。
"""),
    md(r"""
### 4.2 改一格（字典的写法）
"""),
    code(r"""
students[0]["score"] = 95

print(students[0])
"""),
    md(r"""
**预期输出**

```
{'name': '小明', 'class': '一班', 'score': 95}
```

注意写法：**没有** `students[0].append` 或 `students["score"]`，而是先按索引定位到行（列表的事），再按键赋值（字典的事）。左边两对方括号，正好对应两层。
"""),
    md(r"""
### 4.3 删一行（列表的写法）
"""),
    code(r"""
del students[1]

print("删掉第 2 行后，共", len(students), "行")
print(students)
"""),
    md(r"""
**预期输出**

```
删掉第 2 行后，共 2 行
[{'name': '小明', 'class': '一班', 'score': 95}, {'name': '小刚', 'class': '一班', 'score': 78}]
```

`del students[1]` 删的是**整行**。想只删一格里某个字段，那是字典的操作（`del students[0]["class"]`），不是本篇的重点。

> 别忘了 `students.pop(1)` 也能删一行，并且会把删掉的那行**返回**给你 —— 详见《列表》篇。
"""),
    md(r"""
---

## 5. 同一张表的键必须一致

这是"它算不算一张表"的前提：**每一行字典要用同一组字段名**。

下面这张表第 2 行把 `"score"` 写成了 `"points"`。先看正常的那行。
"""),
    code(r"""
bad = [
    {"name": "小明", "score": 90},
    {"name": "小红", "points": 85},      # 字段名写错了
]

print(bad[0]["score"])                   # 第 1 行正常

# 把下面这一行行首的 # 去掉，再运行一次，看看会发生什么：
# print(bad[1]["score"])
"""),
    md(r"""
**预期输出**（注释保留时）

```
90
```

把最后那一行的 `#` 去掉再运行，你会看到：

```
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
Cell In[9], line 9
----> 9 print(bad[1]["score"])

KeyError: 'score'
```

`KeyError: 'score'` 的意思是：**第 2 行里根本没有 `score` 这个键**（它叫 `points`）。

这里要记住的是**结论**，不是读报错的技巧：字段名不一致，"一张表"就散了，按字段取值必然出事。

> 完整的 Traceback 逐行读法与排查动作，见补充章节《报错怎么读》；`get()` 一类的兜底写法见《字典》篇。本篇只负责让你确认问题出在"键不一致"。
"""),
    md(r"""
---

## 6. 可变性：一张表的第二个名字

[列表](https://docs.python.org/zh-cn/3/tutorial/datastructures.html)和[字典](https://docs.python.org/zh-cn/3/tutorial/datastructures.html#dictionaries)都是**可变**的 —— 创建之后还能原地改内容。这带来一个必须提前知道的坑。
"""),
    code(r"""
same = students          # 这不是复制，只是给同一个列表起了第二个名字
same.append({"name": "小美", "class": "二班", "score": 88})

print("用 same 看，共", len(same), "行")
print("用 students 看，共", len(students), "行")
"""),
    md(r"""
**预期输出**

```
用 same 看，共 3 行
用 students 看，共 3 行
```

**两行都是 3。** 用 `students` 去看，也变了 —— 因为 `same` 和 `students` 指的是**同一个列表**，不是两份数据。

想要真正独立的副本，得显式复制（`students.copy()` 或 `list(students)`）。这条原理的完整讲解在《列表》篇；字典同样可变，只是本组不重复展开。
"""),
    md(r"""
---

## 7. 它长什么样：CSV 与 JSON 的形状对照

这一节只做一件事：让你**认出形状**。真正的文件读写、遍历筛选，属于后面的课程。

下面这段用一段"内存里的迷你表格"文本演示 —— 注意，它**不碰任何文件**，所以不需要准备 csv 文件就能跑。
"""),
    code(r"""
import csv, io, json

# 一段迷你的 CSV 文本（表头一行 + 两行数据）
csv_text = '''name,class,score
小明,一班,90
小红,二班,85
'''

rows = list(csv.DictReader(io.StringIO(csv_text)))

print(rows)
print(rows[0]["name"], "的分数是", rows[0]["score"])
print("它的类型是：", type(rows[0]["score"]).__name__)
"""),
    md(r"""
**预期输出**

```
[{'name': '小明', 'class': '一班', 'score': '90'}, {'name': '小红', 'class': '二班', 'score': '85'}]
小明 的分数是 90
它的类型是： str
```

两个要点：

1. **形状与你手写的表一模一样**：`csv.DictReader` 把表头那一行自动变成每行的**键**，于是"第几列"这件事彻底不用记了。这就是"列表套字典是真实数据最常见形状"的由来。
2. **`'90'` 是字符串，不是数字** —— 输出里带着引号，类型是 `str`。这正是上半场强调过的：**从外部读进来的内容，默认都是文本**。要对它做算术，得先转换。

再看 JSON。
"""),
    code(r"""
json_text = '[{"name": "小明", "score": 90}, {"name": "小红", "score": 85}]'

data = json.loads(json_text)

print(data)
print(data[0]["name"], "的分数是", data[0]["score"])
print("它的类型是：", type(data[0]["score"]).__name__)
"""),
    md(r"""
**预期输出**

```
[{'name': '小明', 'score': 90}, {'name': '小红', 'score': 85}]
小明 的分数是 90
它的类型是： int
```

**同样是列表套字典**，但这次 `90` 的类型是 `int` —— 因为 JSON 里它本来就写成了数字，没有引号。

把这两段并排看，你应该能得出结论：

| 来源 | 解析后的形状 | 数字的类型 |
| --- | --- | --- |
| CSV 文本 | 列表套字典 | `str`（带引号 → 文本） |
| JSON 文本 | 列表套字典 | `int`（不带引号 → 数字） |

**形状一样、类型可能不同** —— 这个区别第一次见容易栽跟头，值得现在就记住。

> 文件读写（`open`）与遍历筛选（`for` / 列表推导式）属后续课程；本篇只在代码块里做了形状对照。
"""),
    md(r"""
---

## 跟随练习

**题目**：下面是一张商品表。请完成四件事。

1. 取出**第 2 个商品**的名称，赋给 `second_name`；
2. 在**末尾加一个**商品：`{"name": "尺子", "price": 3.0, "stock": 30}`；
3. 把**第 1 个商品的价格**改成 `3.0`；
4. 打印整张表。

先自己动手，再往下翻参考答案。卡住了就把报错抄下来。
"""),
    code(r"""
# 跟随练习：给商品表取值、加行、改格
products = [
    {"name": "铅笔", "price": 2.5, "stock": 100},
    {"name": "橡皮", "price": 1.5, "stock": 50},
]

# TODO 1: 取第 2 个商品的名称（提示：先按索引找行，再按键找字段）
second_name = ""

# TODO 2: 在末尾加一个商品 {"name": "尺子", "price": 3.0, "stock": 30}


# TODO 3: 把第 1 个商品的价格改成 3.0


# TODO 4: 打印整张表，以及一共几个商品
print("第二个商品：", second_name)
print("现在共", len(products), "个商品")
print(products)
"""),
    md(r"""
**参考答案**

```python
products = [
    {"name": "铅笔", "price": 2.5, "stock": 100},
    {"name": "橡皮", "price": 1.5, "stock": 50},
]

second_name = products[1]["name"]

products.append({"name": "尺子", "price": 3.0, "stock": 30})

products[0]["price"] = 3.0

print("第二个商品：", second_name)
print("现在共", len(products), "个商品")
print(products)
```

预期输出：

```
第二个商品： 橡皮
现在共 3 个商品
[{'name': '铅笔', 'price': 3.0, 'stock': 100}, {'name': '橡皮', 'price': 1.5, 'stock': 50}, {'name': '尺子', 'price': 3.0, 'stock': 30}]
```

三处对照本节的规律：

- `products[1]["name"]` —— 两层取值，一次到位；
- `products.append({...})` —— 加行用**列表**的写法；
- `products[0]["price"] = 3.0` —— 改格用**字典**的写法。

> `products` 里的 `stock` 字段全程没被用到 —— 这很正常，真实的表总是"字段比这次用到的多"。
"""),
    md(r"""
---

## 小结与自检

| 你现在应该能做到 | 自检方式 |
| --- | --- |
| 说清"一行为什么用字典装" | 你能解释列表套列表丢了什么 |
| 把多行组成一张表 | 写出 `[{...}, {...}]` 的形式 |
| 两层取值 | 说得出 `rows[0]["name"]` 的两层各是什么 |
| 增删行与改字段 | 说得出哪一层用列表的写法、哪一层用字典的写法 |
| 知道"表"成立的铁律 | 答得出"每行的键必须怎样" |
| 认出 CSV / JSON 的形状 | 对比两者的输出，说出数字类型为什么不同 |

**一句话回顾**：一张表 = 列表装行 + 字典装字段名，`rows[0]["name"]` 就是"第 1 行的姓名"。

**下一步**：

- 想把这一篇的四个概念合起来看一遍，打开概念组索引页 `concept-group/python-lesson1-second-half/index.html`；
- 想补读报错，看《报错怎么读》；想补容器规则，回《列表》与《字典》；
- 真正的"整列取值、按条件筛行、排序分组"属于后续课程 —— 到那时你写的仍然是在这个结构上做文章。
"""),
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    fname = "03-概念组-列表套字典-一张表.ipynb"
    path = os.path.join(OUT_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(notebook(nb), f, ensure_ascii=False, indent=1)
        f.write("\n")
    n_md = sum(1 for c in nb if c["cell_type"] == "markdown")
    n_code = sum(1 for c in nb if c["cell_type"] == "code")
    print("written: %s  (%d cells: %d md + %d code)" % (fname, len(nb), n_md, n_code))


if __name__ == "__main__":
    main()
