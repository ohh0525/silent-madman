# Python `with` 语句概念讲解

## 一句话概括

`with` 用于**自动管理资源的获取与释放**（上下文管理器），确保无论代码块正常结束还是抛出异常，清理操作（如关闭文件、释放锁、回滚事务）都一定会被执行。

## 为什么需要 with

不用 `with` 时，手动管理资源容易出错：

```python
# 不推荐：一旦 open 和 close 之间抛异常，文件就永远不会被关闭
f = open("data.txt", "w")
f.write("hello")   # 如果这里出错，close() 不会执行
f.close()
```

用 `try/finally` 虽然安全，但代码冗长重复：

```python
f = open("data.txt", "w")
try:
    f.write("hello")
finally:
    f.close()
```

`with` 一行搞定，既安全又简洁：

```python
with open("data.txt", "w") as f:
    f.write("hello")
# 离开 with 块时，f 自动关闭（即使中途抛异常）
```

## 执行流程

`with 表达式 as 变量:` 背后发生了什么：

1. 执行表达式，得到一个**上下文管理器**对象（定义了 `__enter__` 和 `__exit__` 方法的对象）。
2. 调用其 `__enter__()`，返回值赋给 `as` 后面的变量（如文件对象 `f`）。
3. 执行 `with` 缩进块内的代码。
4. 无论块内代码是正常结束还是抛出异常，都会调用 `__exit__()` 做清理：
   - `__exit__` 收到异常信息时可以选择处理（返回 True 吞掉异常）或放行（返回 False）。
   - 常见对象的 `__exit__` 就是做清理：文件关闭、锁释放、连接断开、临时目录删除等。

等价伪代码：

```python
mgr = open("data.txt", "w")
f = mgr.__enter__()
try:
    f.write("hello")
finally:
    mgr.__exit__(None, None, None)   # 出错时传入异常信息
```

## 常见使用场景

| 场景 | 写法 |
|------|------|
| 文件读写 | `with open("a.txt") as f:` |
| 临时目录/文件 | `with tempfile.TemporaryDirectory() as d:` |
| 多线程锁 | `with lock:` |
| 数据库事务 | `with conn:` |
| 精度/行为开关 | `with decimal.localcontext():` |
| 计时 | `with timer:` |
| 单元测试 | `with self.assertRaises(ValueError):` |
| 重定向输出 | `with contextlib.redirect_stdout(buf):` |

## 同时管理多个资源

```python
with open("in.txt") as fin, open("out.txt", "w") as fout:
    fout.write(fin.read())
```

Python 3.10+ 还支持括号分组写法：

```python
with (open("in.txt") as fin,
      open("out.txt", "w") as fout):
    fout.write(fin.read())
```

## 自定义上下文管理器

### 方式一：实现类协议（__enter__ / __exit__）

```python
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self                      # 赋给 as 后面的变量

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"耗时 {self.elapsed:.3f}s")
        return False                     # 不吞异常，继续向外抛
```

### 方式二：用生成器写装饰器（更简洁）

```python
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.perf_counter()
    try:
        yield                            # yield 前是 __enter__，之后是 __exit__
    finally:
        print(f"耗时 {time.perf_counter() - start:.3f}s")
```

## 三个关键点

1. **异常安全**：清理逻辑写在 `__exit__` / `finally` 里，异常时也保证执行。
2. **不是 try/finally 的糖那么简单**：`__exit__` 还能根据异常信息决定是否抑制异常。
3. **标准库大量支持**：凡是"获取—使用—释放"模式的资源，优先想到 `with`。
