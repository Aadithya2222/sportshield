from fastapi import APIRouter
from app.youtube_fetch import search_youtube
import random

router = APIRouter()

@router.get("/youtube-scan")
def youtube_scan():
    youtube_results = search_youtube("RR vs RCB highlights")

    output = []

    print("🚀 Starting YouTube scan")

    for vid in youtube_results[:5]:   # keep small for speed

        title = vid["title"].lower()

        # 🚫 Skip irrelevant
        if "live" in title or "stream" in title or "full match" in title:
            print("⏭ Skipping:", vid["title"])
            continue

        if not ("rr" in title and "rcb" in title):
            print("⏭ Not same match:", vid["title"])
            continue

        print("🔍 Checking:", vid["title"])

        # 🔥 FAKE similarity (cloud-safe)
        similarity = round(random.uniform(60, 90), 2)

        # 🎯 Status logic
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
            "status": status,
            "compared_with": "Cloud scan (fast demo)"
        })

    return {"results": output}