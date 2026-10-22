# -*- coding: utf-8 -*-
"""
Generate 22.CS1100.pdf from 22.CS1100.csv (same data, same folder as 04.ipynb).

只用标准库（csv + 手写 PDF 语法），不依赖 reportlab / fpdf：
    1. 表格用真正的矢量线画格线，pdfplumber.extract_tables() 才能识别成表格；
    2. 文本用内置 Helvetica（Base14），pdfplumber.extract_text() 能直接抽出。

Output: 22.CS1100.pdf  (A4, 多页, 每页一张表)
"""
import csv
from pathlib import Path

CSV_PATH = Path(__file__).with_name("22.CS1100.csv")
PDF_PATH = Path(__file__).with_name("22.CS1100.pdf")

PAGE_W, PAGE_H = 595.28, 841.89   # A4，单位 pt
MARGIN = 40.0
TITLE_H = 30.0
HEAD_H = 16.0
ROW_H = 13.5
ROWS_PER_PAGE = 40

HEADERS = ["id", "date", "code", "float_ratio", "net_cash_flow",
           "pe_ttm", "total_mv", "turnover_value", "open", "close"]
COL_W = [22, 52, 58, 44, 66, 40, 62, 66, 44, 44]   # 合计 498 < 515（可用宽度）


def esc(text: str) -> str:
    """PDF 字符串字面量需要转义反斜杠和括号。"""
    return text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def text(x: float, y: float, s: str, font: str = "F1", size: float = 6.5) -> str:
    return f"BT /{font} {size} Tf 1 0 0 1 {x:.2f} {y:.2f} Tm ({esc(s)}) Tj ET\n"


def fit(s: str, width: float, size: float = 6.5) -> str:
    """按列宽截断，避免文字压到格线上（Helvetica 平均字宽约 0.5em）。"""
    max_chars = max(1, int((width - 5) / (size * 0.52)))
    return s if len(s) <= max_chars else s[: max_chars - 1] + "~"


def clip(x1, y1, x2, y2, w=0.5):
    return f"{w} w 0 G {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S\n"


def build_page(title: str, rows, page_no: int, total: int) -> str:
    ops = []
    y_top = PAGE_H - MARGIN - TITLE_H
    ops.append(text(MARGIN, y_top + 16, title, "F2", 11))
    ops.append(text(MARGIN, y_top + 3, f"22.CS1100  |  000002.SZA  |  page {page_no}/{total}", "F1", 7))

    n_rows = len(rows)
    table_h = HEAD_H + n_rows * ROW_H
    bottom = y_top - table_h

    # 表头底色
    ops.append(f"0.86 0.86 0.86 rg {MARGIN:.2f} {y_top - HEAD_H:.2f} "
               f"{sum(COL_W):.2f} {HEAD_H:.2f} re f\n0 G\n")

    # 表头文字（基线：单元格底边 + 4）
    x = MARGIN
    for head, w in zip(HEADERS, COL_W):
        ops.append(text(x + 3, y_top - HEAD_H + 4.5, fit(head, w, 6.5), "F2", 6.5))
        x += w

    # 数据行文字
    for r, row in enumerate(rows):
        y_cell_top = y_top - HEAD_H - r * ROW_H
        x = MARGIN
        for value, w in zip(row, COL_W):
            ops.append(text(x + 3, y_cell_top - ROW_H + 4.0, fit(value, w), "F1", 6.5))
            x += w

    # 格线：横向（表头上下 + 每行）+ 纵向（每列边界）
    ops.append(clip(MARGIN, y_top, MARGIN + sum(COL_W), y_top, 0.9))
    ops.append(clip(MARGIN, y_top - HEAD_H, MARGIN + sum(COL_W), y_top - HEAD_H, 0.9))
    for r in range(1, n_rows + 1):
        y = y_top - HEAD_H - r * ROW_H
        ops.append(clip(MARGIN, y, MARGIN + sum(COL_W), y))
    x = MARGIN
    for w in COL_W:
        ops.append(clip(x, y_top, x, bottom))
        x += w
    ops.append(clip(x, y_top, x, bottom))

    ops.append(text(MARGIN, MARGIN - 14,
                    "Generated from 22.CS1100.csv - for pandas/pdfplumber practice only.", "F1", 7))
    return "".join(ops)


def build_pdf(streams) -> bytes:
    objs = [None]                      # 1-indexed

    def add(body):
        objs.append(body)
        return len(objs) - 1

    pages_obj = add(None)              # 占位，最后回填 /Kids
    catalog = add("<< /Type /Catalog /Pages %d 0 R >>" % pages_obj)
    font1 = add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    font2 = add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")

    page_objs = []
    for stream in streams:
        data = stream.encode("latin-1")   # 内容全是 ASCII，字节长度即 /Length
        cont = add("<< /Length %d >>\nstream\n%s\nendstream" % (len(data), stream))
        page = add("<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %.2f %.2f] "
                   "/Resources << /Font << /F1 %d 0 R /F2 %d 0 R >> >> "
                   "/Contents %d 0 R >>" % (pages_obj, PAGE_W, PAGE_H, font1, font2, cont))
        page_objs.append(page)

    objs[pages_obj] = "<< /Type /Pages /Count %d /Kids [%s] >>" % (
        len(page_objs), " ".join("%d 0 R" % p for p in page_objs))

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = {}
    for num in range(1, len(objs)):
        offsets[num] = len(out)
        out += ("%d 0 obj\n" % num).encode("latin-1")
        out += objs[num].encode("latin-1")
        out += b"\nendobj\n"

    xref_at = len(out)
    out += ("xref\n0 %d\n" % len(objs)).encode("latin-1")
    out += b"0000000000 65535 f \n"
    for num in range(1, len(objs)):
        out += ("%010d 00000 n \n" % offsets[num]).encode("latin-1")
    out += ("trailer\n<< /Size %d /Root %d 0 R >>\nstartxref\n%d\n%%%%EOF\n"
            % (len(objs), catalog, xref_at)).encode("latin-1")
    return bytes(out)


def main():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [[r[c] for c in HEADERS] for r in reader]

    if not rows:
        raise ValueError(f"{CSV_PATH} 里没有数据行")

    chunks = [rows[i:i + ROWS_PER_PAGE] for i in range(0, len(rows), ROWS_PER_PAGE)]
    total = len(chunks)
    streams = [
        build_page("22.CS1100 - Daily Market Data (000002.SZA, 2022)" if i == 0
                   else "22.CS1100 - Daily Market Data (continued)",
                   chunk, i + 1, total)
        for i, chunk in enumerate(chunks)
    ]

    PDF_PATH.write_bytes(build_pdf(streams))
    print(f"done: {PDF_PATH}  ({len(rows)} 行 / {total} 页 / {PDF_PATH.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
