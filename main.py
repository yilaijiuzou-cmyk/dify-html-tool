from fastapi import FastAPI
from pydantic import BaseModel
import uuid, tempfile, os, datetime

app = FastAPI(title="HTML-Downloader-for-Dify")

class In(BaseModel):
    content: str

@app.post("/gen_html")
def gen_html(inp: In):
    html = inp.content
    if not html.strip().startswith("<!doctype"):
        html = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>Dify report</title></head>
<body>{html}</body></html>"""
    fname = f"{uuid.uuid4().hex}.html"
    path = f"/tmp/{fname}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    # 华为云监听 9000，返回可下载地址
    return {"download_url": f"/download/{fname}"}

from fastapi.staticfiles import StaticFiles
app.mount("/download", StaticFiles(directory="/tmp"), name="static")
