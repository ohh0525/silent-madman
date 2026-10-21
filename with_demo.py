"""with 语句演示：运行本文件，观察每一步的输出顺序。

运行方式（在 VS Code 终端里执行）:
    python with_demo.py
"""
import time
from contextlib import contextmanager

print("=" * 40)
print("1. 文件自动关闭")
print("=" * 40)
with open("demo.txt", "w", encoding="utf-8") as f:
    f.write("hello with")
    print("  写入完成，f.closed =", f.closed)
print("  离开 with 块，f.closed =", f.closed)   # True，自动关闭了

print()
print("=" * 40)
print("2. 异常时也会自动清理")
print("=" * 40)
try:
    with open("demo2.txt", "w", encoding="utf-8") as f:
        raise ValueError("模拟出错")
except ValueError as e:
    print("  捕获异常:", e)
print("  但文件依然被关闭，f.closed =", f.closed)

print()
print("=" * 40)
print("3. 自定义上下文管理器（类协议）")
print("=" * 40)


class Timer:
    def __enter__(self):
        print("  [__enter__] 开始计时")
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"  [__exit__]  耗时 {self.elapsed:.4f}s")
        return False   # False = 不吞掉异常；True = 抑制异常


with Timer() as t:
    total = sum(range(1_000_000))
    print("  求和结果:", total)

print()
print("=" * 40)
print("4. 用 @contextmanager 写（更简洁）")
print("=" * 40)


@contextmanager
def timer():
    start = time.perf_counter()
    print("  [进入] 开始计时")
    try:
        yield            # yield 之前的代码 = __enter__，之后的 = __exit__
    finally:
        print(f"  [退出] 耗时 {time.perf_counter() - start:.4f}s")


with timer():
    total = sum(range(500_000))

print()
print("=" * 40)
print("5. 一次管理多个资源")
print("=" * 40)
with open("demo.txt", encoding="utf-8") as fin, \
     open("demo_copy.txt", "w", encoding="utf-8") as fout:
    fout.write(fin.read())
    print("  已把 demo.txt 复制到 demo_copy.txt")

# 清理演示文件
import os
for name in ("demo.txt", "demo2.txt", "demo_copy.txt"):
    os.remove(name)
print()
print("全部演示完成，演示文件已清理。")
