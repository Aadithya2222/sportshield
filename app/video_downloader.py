import yt_dlp
import os
import time
import subprocess

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def _find_downloaded_file(video_id: str):
    prefix = f"{video_id}_full."
    for fn in os.listdir(DOWNLOAD_DIR):
        if fn.startswith(prefix) and fn.endswith(".mp4"):
            return os.path.join(DOWNLOAD_DIR, fn)
    return None


def download_and_trim(video_id: str):
    url = f"https://www.youtube.com/watch?v={video_id}"
    out_template = os.path.join(DOWNLOAD_DIR, f"{video_id}_full.%(ext)s")

    ydl_opts = {
    'format': 'best[ext=mp4]/best',   # ✅ fallback included
    'outtmpl': out_template,
    'quiet': True,
    'noplaylist': True,
    }

    try:
        # 🎬 Download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        time.sleep(1)  # avoid file lock issue

        downloaded = _find_downloaded_file(video_id)

        if not downloaded:
            raise FileNotFoundError("Download failed")

        clips = []

        # 🔥 MULTI-SEGMENT TRIMMING
        for start in [0, 10]:
            clip_path = os.path.join(
                DOWNLOAD_DIR,
                f"{video_id}_clip_{start}.mp4"
            )

            command = [
                "ffmpeg",
                "-y",
                "-ss", str(start),
                "-i", downloaded,
                "-t", "10",
                "-c", "copy",
                clip_path
            ]

            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            if os.path.exists(clip_path):
                clips.append(clip_path)

        return clips  # ✅ return list of clips

    except Exception as e:
        print(f"download_and_trim failed for {video_id}: {e}")
        return []