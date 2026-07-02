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
duration = total_frames / fps if fps > 0 else 0
print(f"Video: {total_frames} frames, {fps:.1f} fps, {duration:.1f}s")

# Content bounds (from previous auto-detect)
crop_left, crop_top = 4, 70
crop_right, crop_bottom = 1454, 946

# Sample densely, but only keep frames that differ significantly
sample_step = 8  # sample every 8 frames at 60fps = ~7.5 samples/sec
start_pct, end_pct = 0.08, 0.92
start_frame = int(total_frames * start_pct)
end_frame = int(total_frames * end_pct)

# Scene change threshold (lower = more sensitive to changes)
threshold = 2.5

prev_gray = None
extracted = []
frame_num = start_frame
target_count = 120

while len(extracted) < target_count and frame_num < end_frame:
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()
    if not ret:
        break

    # Crop
    frame = frame[crop_top:crop_bottom, crop_left:crop_right]

    # Convert to grayscale and resize small for comparison
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (160, 100))

    if prev_gray is not None:
        diff = cv2.absdiff(small, prev_gray)
        mean_diff = np.mean(diff)

        if mean_diff < threshold:
            frame_num += sample_step
            continue  # Skip — too similar to previous

    # Keep this frame — output at higher resolution
    h, w = frame.shape[:2]
    target_w = 960  # up from 720 for sharper output
    ratio = target_w / w
    frame = cv2.resize(frame, (target_w, int(h * ratio)), interpolation=cv2.INTER_LANCZOS4)

    out_path = os.path.join(out_dir, f"frame_{len(extracted):03d}.png")
    cv2.imwrite(out_path, frame)
    extracted.append(out_path)
    print(f"  [{len(extracted)}] frame {frame_num} diff={mean_diff:.1f}" if prev_gray is not None else f"  [1] frame {frame_num} (start)")

    prev_gray = small
    frame_num += sample_step

cap.release()
print(f"\nDone: {len(extracted)} unique frames (scene-change filtered, threshold={threshold})")
