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

crop_left, crop_top = 4, 70
crop_right, crop_bottom = 1454, 946

sample_step = 8
start_pct, end_pct = 0.08, 0.92
start_frame = int(total_frames * start_pct)
end_frame = int(total_frames * end_pct)

threshold = 2.5
target_w = 960

prev_gray = None
extracted = []
frame_num = start_frame
target_count = 120

while len(extracted) < target_count and frame_num < end_frame:
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()
    if not ret:
        break

    frame = frame[crop_top:crop_bottom, crop_left:crop_right]

    # --- Remove mouse cursor ---
    # Cursor is typically white (high brightness) with black outline
    gray_full = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Find very bright pixels (cursor body) and very dark pixels right next to them (cursor outline)
    _, bright = cv2.threshold(gray_full, 240, 255, cv2.THRESH_BINARY)
    _, dark = cv2.threshold(gray_full, 30, 255, cv2.THRESH_BINARY_INV)

    # The cursor has bright and dark pixels close together
    kernel = np.ones((3,3), np.uint8)
    bright_dilated = cv2.dilate(bright, kernel, iterations=2)
    cursor_mask = cv2.bitwise_and(bright_dilated, dark)
    cursor_mask = cv2.dilate(cursor_mask, kernel, iterations=3)

    # Only inpaint if cursor area is small (cursor is ~400-2000 px)
    cursor_area = cv2.countNonZero(cursor_mask)
    if 200 < cursor_area < 3000:
        frame = cv2.inpaint(frame, cursor_mask, 3, cv2.INPAINT_TELEA)

    # Scene detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (160, 100))

    if prev_gray is not None:
        diff = cv2.absdiff(small, prev_gray)
        mean_diff = np.mean(diff)
        if mean_diff < threshold:
            frame_num += sample_step
            continue

    h, w = frame.shape[:2]
    ratio = target_w / w
    frame = cv2.resize(frame, (target_w, int(h * ratio)), interpolation=cv2.INTER_LANCZOS4)

    out_path = os.path.join(out_dir, f"frame_{len(extracted):03d}.png")
    cv2.imwrite(out_path, frame)
    tag = " [cursor removed]" if (200 < cursor_area < 3000) else ""
    print(f"  [{len(extracted)+1}] frame {frame_num} diff={mean_diff:.1f}{tag}" if prev_gray is not None else f"  [1] frame {frame_num} (start){tag}")
    extracted.append(out_path)

    prev_gray = small
    frame_num += sample_step

cap.release()
print(f"\nDone: {len(extracted)} frames")
