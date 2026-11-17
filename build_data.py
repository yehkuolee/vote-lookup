#!/usr/bin/env python3
"""從中選會公開 JSON 抓 115 年地方選舉投開票所資料，輸出 data/stations.json。
用法：python3 build_data.py
"""
import json, time, urllib.request
from datetime import datetime, timezone, timedelta

BASE = "https://info.cec.gov.tw/vote2026/static/json"
UA = {"User-Agent": "Mozilla/5.0 (ETtoday vote lookup builder)"}


def get(path):
    for i in range(3):
        try:
            req = urllib.request.Request(f"{BASE}/{path}", headers=UA)
            return json.load(urllib.request.urlopen(req, timeout=30))
        except Exception:
            if i == 2:
                return None
            time.sleep(1.5)


def main():
    dist = get("dist/prvCityDept.json")["prvs"]
    voters = [(v["voterCode"], v["voterName"]) for v in get("tbox/voter.json")["voters"]]
    out = {"voters": voters, "cities": []}
    total = 0
    for prv in dist:
        code = prv["prvCityCode"]
        dept_names = {d["deptCode"]: d["deptName"] for a in prv["areas"] for d in a["depts"]}
        city = {"code": code, "name": prv["prvName"], "v": {}}
        for vcode, _ in voters:
            data = get(f"tbox/{code}/{vcode}{code}.json")
            if not data:
                continue
            depts = []
            for d in data["depts"]:
                lis = []
                for li in d["lis"]:
                    # 每個里 → 投開票所 [所號, 名稱, 地址, 鄰別]
                    boxes = [[t["tboxNo"], t["tboxName"], t["addr"], t["neighbor"]] for t in li["tboxs"]]
                    total += len(boxes)
                    lis.append([li["liName"], boxes])
                depts.append([dept_names.get(d["deptCode"], d["deptCode"]), lis])
            city["v"][vcode] = depts
        out["cities"].append(city)
        print("OK", prv["prvName"])
    tz = timezone(timedelta(hours=8))
    out["updated"] = datetime.now(tz).strftime("%Y-%m-%d")
    with open("data/stations.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print("投開票所筆數（含各類別重複）:", total)


if __name__ == "__main__":
    main()
