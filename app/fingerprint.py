import cv2
from PIL import Image
import imagehash

def extract_frames(video_path, frame_interval=1):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    frames = []
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if count % (fps * frame_interval) == 0:
            frames.append(frame)

        count += 1

    cap.release()
    return frames


def generate_hashes(frames):
    hashes = []
    for frame in frames:
        img = Image.fromarray(frame)
        phash = imagehash.phash(img)
        hashes.append(phash)
    return hashes


def get_video_fingerprint(video_path):
    frames = extract_frames(video_path,frame_interval=1)
    return generate_hashes(frames)