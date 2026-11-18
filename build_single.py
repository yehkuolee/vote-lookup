#!/usr/bin/env python3
"""把 source.html + data/stations.json + LOGO 打包成單一 HTML。
用法：python3 build_single.py [輸出路徑]
"""
import base64, json, sys, os

root = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, "dist", "查投開票所_單檔版.html")

s = open(os.path.join(root, "source.html"), encoding="utf-8").read()
data = open(os.path.join(root, "data", "stations.json"), encoding="utf-8").read()
json.loads(data)  # 驗證格式
logo = base64.b64encode(open(os.path.join(root, "assets", "logo_ettoday.png"), "rb").read()).decode()

# 1) LOGO 內嵌
assert 'src="assets/logo_ettoday.png"' in s
s = s.replace('src="assets/logo_ettoday.png"', 'src="data:image/png;base64,%s"' % logo)

# 2) 資料內嵌，取代 fetch
old = "fetch('data/stations.json').then(r=>{ if(!r.ok) throw 0; return r.json(); })"
assert old in s
s = s.replace(old, "Promise.resolve(JSON.parse(document.getElementById('db').textContent))")
safe = data.replace("</", "<\\/")
block = '<script type="application/json" id="db">' + safe + "</script>\n"
i = s.rindex("<script>\n(function(){")
s = s[:i] + block + s[i:]

os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, "w", encoding="utf-8").write(s)
print("OK", out, round(os.path.getsize(out) / 1024 / 1024, 2), "MB")
