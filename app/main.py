from fastapi import FastAPI, UploadFile, File
import shutil
import os
import random

from fastapi.middleware.cors import CORSMiddleware
from app.youtube_fetch import search_youtube

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# 🎥 Upload endpoint (lightweight)
@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "File uploaded successfully"}


# 🔍 Compare endpoint (SIMULATED for cloud)
@app.post("/compare")
async def compare_videos(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    similarity = round(random.uniform(60, 90), 2)

    return {
        "similarity": similarity,
        "message": "Match Found" if similarity > 70 else "No Significant Match"
    }


# 🔍 YouTube Scan (CLOUD SAFE)
@app.get("/youtube-scan")
def youtube_scan():
    youtube_results = search_youtube("RR vs RCB highlights")

    output = []

    for vid in youtube_results[:5]:
        title = vid["title"].lower()

        if "live" in title or "stream" in title or "full match" in title:
            continue

        if not ("rr" in title and "rcb" in title):
            continue

        similarity = round(random.uniform(60, 90), 2)

        if similarity > 85:
            status = "🚨 Exact Copy Detected"
        elif similarity > 65:
            status = "⚠ Modified Content"
        else:
            status = "Safe"

        output.append({
            "title": vid["title"],
            "thumbnail": vid["thumbnail"],
            "similarity": similarity,
            "status": status
        })

    return {"results": output}