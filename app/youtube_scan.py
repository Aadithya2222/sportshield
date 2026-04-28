from fastapi import APIRouter
from app.youtube_fetch import search_youtube
from app.video_downloader import download_and_trim
from app.fingerprint import get_video_fingerprint
from app.compare import compare_hashes
from app.gemini_parser import extract_match_info

router = APIRouter()

@router.get("/youtube-scan")
def youtube_scan():
    youtube_results = search_youtube("RR vs RCB 2026 hihglights")

    original_video = "data/video1.mp4"
    original_hashes = get_video_fingerprint(original_video)

    output = []

    print("🚀 Starting YouTube scan")

    for vid in youtube_results[:10]:   # 🔥 small limit for speed

        title = vid["title"].lower()

        # 🚫 Skip bad videos
        if "live" in title or "stream" in title or "full match" in title:
            print("⏭ Skipping:", vid["title"])
            continue

        if not ("rr" in title and "rcb" in title):
            print("⏭ Not same match:", vid["title"])
            continue
        print("🔽 Downloading:", vid["title"])

        # 🔽 Download + multi-clip
        clips = download_and_trim(vid["videoId"])

        print("✂ Clips created:", clips)

        best_similarity = 0

        if clips:
            for clip in clips:
                test_hashes = get_video_fingerprint(clip)
                sim = compare_hashes(original_hashes, test_hashes)
                best_similarity = max(best_similarity, sim)

        similarity = round(best_similarity, 2)

        # 🎯 Decide status
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
            "compared_with": "YouTube clips (multi-segment)"
        })

    return {"results": output}
match_query = extract_match_info("RR vs RCB IPL video")

youtube_results = search_youtube(match_query + " IPL highlights")