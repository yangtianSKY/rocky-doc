import cv2
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

# 15 fps output, ~8 seconds = 120 frames
target_fps = 15
target_duration = 8  # seconds
target_frames = target_fps * target_duration  # 120

# Skip first 10%, take from middle
start_pct = 0.10
end_pct = 0.90
start_frame = int(total_frames * start_pct)
end_frame = int(total_frames * end_pct)
usable = end_frame - start_frame
step = max(1, usable // target_frames)

# More aggressive crop for window borders
crop_top = int(1080 * 0.08)    # ~86px
crop_bot = int(1080 * 0.06)    # ~65px
crop_left = int(1920 * 0.05)   # ~96px
crop_right = int(1920 * 0.08)  # ~154px

extracted = []
frame_num = start_frame
count = 0
while count < 120 and frame_num < end_frame:
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    frame = frame[crop_top:h-crop_bot, crop_left:w-crop_right]
    h2, w2 = frame.shape[:2]
    ratio = 720 / w2
    frame = cv2.resize(frame, (720, int(h2 * ratio)))

    out_path = os.path.join(out_dir, f"frame_{count:03d}.png")
    cv2.imwrite(out_path, frame)
    extracted.append(out_path)

    frame_num += step
    count += 1

cap.release()
print(f"Done: {len(extracted)} frames ({target_fps}fps, {len(extracted)/target_fps:.1f}s)")
