# -*- coding: utf-8 -*-
"""radar report char whitelist scan (reuse each run)"""
import re, sys, unicodedata

p = sys.argv[1]
t = open(p, encoding="utf-8").read()

allowed = (
    "\u4e00-\u9fff"   # CJK
    "\u3000-\u303f"   # CJK punct
    "a-zA-Z0-9"
    "\s"
    r"\.,:;!?(){}\[\]<>=\"'`~@#\$%\^&\*\-\+_/\\|"
    "·—–…"
    "「」『』"
    "⭐✅❌🔴⚠️⏸🟡⏳🎯"
    "①②③④⑤⑥⑦⑧⑨⑩"
    "×÷≈≠≤≥→←↔⇒↓↑"
    "²³⁻⁺⁰¹²³⁴⁵⁶⁷⁸⁹"
    "μ"
)
ok = re.compile("[" + allowed + "]")
bad = {}
for ch in t:
    if not ok.match(ch):
        bad[ch] = bad.get(ch, 0) + 1
print("total chars:", len(t))
if bad:
    for ch, n in sorted(bad.items(), key=lambda x: -x[1]):
        try:
            name = unicodedata.name(ch)
        except ValueError:
            name = "?"
        print("ILLEGAL: %r x%d (%s)" % (ch, n, name))
else:
    print("illegal: NONE")
print("tail3:", repr(t[-30:]))
