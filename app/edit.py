import cv2

# Input video
cap = cv2.VideoCapture("data/video2.mp4")

# Output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("data/video2_edited.mp4", fourcc, 30, (640, 480))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # --- 1. Crop (remove borders) ---
    h, w, _ = frame.shape
    cropped = frame[int(h*0.1):int(h*0.9), int(w*0.1):int(w*0.9)]

    # --- 2. Resize ---
    resized = cv2.resize(cropped, (640, 480))

    # --- 3. Add slight blur ---
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)

    # --- 4. Add watermark text ---
    cv2.putText(
        blurred,
        "FanPage",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )

    # Write frame
    out.write(blurred)

cap.release()
out.release()

print("Edited video saved as data/video2_edited.mp4")