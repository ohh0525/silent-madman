# -*- coding: utf-8 -*-
"""
Generate a simulated A-share daily dataset CSV similar to the
Kaggle file "22.CS1100.csv" (000002.SZA, year 2022).

Output columns (same layout as the screenshot):
    id, date, code, float_ratio, net_cash_flow, pe_ttm,
    total_mv, turnover_value, open, close
"""
import csv
import random
from datetime import date, timedelta

random.seed(42)  # reproducible

# 2022 A-share market holidays (non-trading weekdays)
HOLIDAYS = {
    date(2022, 1, 3),                                   # New Year
    date(2022, 1, 31), date(2022, 2, 1), date(2022, 2, 2),
    date(2022, 2, 3), date(2022, 2, 4),                 # Spring Festival
    date(2022, 4, 4), date(2022, 4, 5),                 # Qingming
    date(2022, 5, 2), date(2022, 5, 3), date(2022, 5, 4),  # Labour Day
    date(2022, 6, 3),                                   # Dragon Boat
    date(2022, 9, 12),                                  # Mid-Autumn
    date(2022, 10, 3), date(2022, 10, 4), date(2022, 10, 5),
    date(2022, 10, 6), date(2022, 10, 7),               # National Day
}
# weekend makeup trading days (Sat/Sun but market open)
MAKEUP = {date(2022, 4, 2), date(2022, 5, 7), date(2022, 10, 8), date(2022, 10, 9)}


def trading_days(year):
    d = date(year, 1, 1)
    while d.year == year:
        if d.weekday() < 5 and d not in HOLIDAYS or d in MAKEUP:
            yield d
        d += timedelta(days=1)


def main():
    rows = []
    pe = 9.17            # random walk anchor
    close = 2909.745     # random walk anchor
    for i, d in enumerate(trading_days(2022)):
        # open near previous close, close random-walks in 2800-3020
        gap = random.uniform(-8, 8)
        open_p = close + gap
        close = min(3020, max(2800, close + random.uniform(-25, 25)))
        pe = min(10.3, max(8.9, pe + random.uniform(-0.12, 0.12)))
        total_mv = random.uniform(2.01e11, 2.11e11)
        turnover = random.uniform(1.3e9, 3.1e10)
        rows.append([
            i,
            f"{d.year}/{d.month}/{d.day}",
            "000002.SZA",
            0.6045,
            -24535195648,
            round(pe, 6),
            f"{total_mv / 1e11:.5f}E+11",
            round(turnover),
            round(open_p, 4),
            round(close, 4),
        ])

    out = r"D:/桌面/22.CS1100.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "date", "code", "float_ratio", "net_cash_flow",
                    "pe_ttm", "total_mv", "turnover_value", "open", "close"])
        w.writerows(rows)
    print(f"done: {out} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
