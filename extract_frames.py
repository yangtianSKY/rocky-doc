import cv2
import numpy as np
import os

video_path = r"d:\ClaudeProjects\ROCKYP\P1\2026-07-02 18-46-49.mp4"
out_dir = r"d:\ClaudeProjects\ROCKYP\P1\frames"
os.makedirs(out_dir, exist_ok=True)

for f in os.listdir(out_dir):
    os.remove(os.path.join(out_dir, f))

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Sample a few frames from the middle to detect content bounds
sample_frames = [int(total_frames * p) for p in [0.2, 0.3, 0.4, 0.5, 0.6]]
bounds = []

for sf in sample_frames:
    cap.set(cv2.CAP_PROP_POS_FRAMES, sf)
    ret, frame = cap.read()
    if not ret:
        continue
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Find non-black (value > 15) pixels
    _, thresh = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)
    coords = cv2.findNonZero(thresh)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        bounds.append((x, y, x+w, y+h))
        print(f"  Sample @ {sf}: content box x={x} y={y} w={w} h={h} (frame {frame.shape[1]}x{frame.shape[0]})")

# Use the widest content bounds across samples
if bounds:
    left = min(b[0] for b in bounds)
    top = min(b[1] for b in bounds)
    right = max(b[2] for b in bounds)
    bottom = max(b[3] for b in bounds)
else:
    left, top, right, bottom = 0, 0, 1920, 1080

# Add small padding inside
pad = 4
left = max(0, left + pad)
top = max(0, top + pad)
right = min(1920, right - pad)
bottom = min(1080, bottom - pad)

print(f"\nAuto crop: left={left} top={top} right={right} bottom={bottom}")
print(f"Crop region: {right-left}x{bottom-top}")

# 15fps, 8 seconds
target_fps = 15
target_frames = 120
start_pct, end_pct = 0.10, 0.90
start_frame = int(total_frames * start_pct)
end_frame = int(total_frames * end_pct)
step = max(1, (end_frame - start_frame) // target_frames)

extracted = []
frame_num = start_frame
count = 0
while count < target_frames and frame_num < end_frame:
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()
    if not ret:
        break

    frame = frame[top:bottom, left:right]
    h, w = frame.shape[:2]
    ratio = 720 / w
    frame = cv2.resize(frame, (720, int(h * ratio)))

    out_path = os.path.join(out_dir, f"frame_{count:03d}.png")
    cv2.imwrite(out_path, frame)
    extracted.append(out_path)
    frame_num += step
    count += 1

cap.release()
print(f"Done: {len(extracted)} frames")
