from fastapi import FastAPI, UploadFile, File
import shutil
import os

import random
from app.youtube_fetch import search_youtube

from app.fingerprint import get_video_fingerprint
from app.compare import compare_hashes
from app.youtube_scan import router as youtube_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(youtube_router)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# 🎥 Upload endpoint
@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "File uploaded successfully", "filename": file.filename}


# 🔍 Compare endpoint
@app.post("/compare")
async def compare_videos(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    path1 = os.path.join(UPLOAD_DIR, file1.filename)
    path2 = os.path.join(UPLOAD_DIR, file2.filename)

    # Save files
    with open(path1, "wb") as f:
        shutil.copyfileobj(file1.file, f)

    with open(path2, "wb") as f:
        shutil.copyfileobj(file2.file, f)

    # Generate fingerprints
    hashes1 = get_video_fingerprint(path1)
    hashes2 = get_video_fingerprint(path2)

    # Compare
    similarity = compare_hashes(hashes1, hashes2)

    return {
        "similarity": round(similarity, 2),
        "message": "Match Found" if similarity > 70 else "No Significant Match"
    }


@app.get("/youtube-scan")
def youtube_scan():
    youtube_results = search_youtube("IPL highlights")

    original_video = "data/video1.mp4"  # your official content

    output = []

    # Precompute original hash (important optimization)
    original_hashes = get_video_fingerprint(original_video)

    for vid in youtube_results:

        # Map YouTube result to a local sample (simulation)
        sample_videos = [
            "data/video2.mp4",
            "data/video2_edited.mp4",
            "data/video3.mp4"
        ]

        test_video = random.choice(sample_videos)

        test_hashes = get_video_fingerprint(test_video)
        similarity = compare_hashes(original_hashes, test_hashes)

        similarity = round(similarity, 2)

        if similarity > 85:
            status = "🚨 Exact Copy Detected"
        elif similarity > 65:
            status = "⚠ Modified Content"
        else:
            status = "Safe"

        output.append({
    "title": vid["title"],
    "videoId": vid["videoId"],
    "thumbnail": vid["thumbnail"],
    "similarity": similarity,
    "status": status,
    "compared_with": os.path.basename(test_video)   # 👈 ADD THIS
})
    return {"results": output}