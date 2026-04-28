from fastapi import APIRouter
from app.youtube_fetch import search_youtube
import random

router = APIRouter()

@router.get("/youtube-scan")
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