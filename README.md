# 查投開票所（ETtoday 風格）

正式網址：https://features.ettoday.net/polling-station-2026/

- 原始碼：source.html（index.html 只是轉址到正式網址）
- 資料：`python3 build_data.py` 重抓中選會資料
- 打包單檔：`python3 build_single.py`，輸出 dist/查投開票所_單檔版.html
- 本機預覽：`python3 -m http.server`，開 /source.html
