import cv2
import os

video_path = r"d:\ClaudeProjects\ROCKYP\P1\2026-07-02 18-46-49.mp4"
out_dir = r"d:\ClaudeProjects\ROCKYP\P1\frames"
os.makedirs(out_dir, exist_ok=True)

# Clear old frames
for f in os.listdir(out_dir):
    os.remove(os.path.join(out_dir, f))

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = total_frames / fps if fps > 0 else 0

print(f"Video: {total_frames} frames, {fps:.1f} fps, {duration:.1f}s")

# Skip first 10% (loading/startup) and last 5% (shutdown)
start_pct = 0.10
end_pct = 0.95
target_frames = 16

start_frame = int(total_frames * start_pct)
end_frame = int(total_frames * end_pct)
usable = end_frame - start_frame
interval = max(1, usable // target_frames)

extracted = []
for i in range(target_frames):
    frame_num = start_frame + i * interval
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    # Crop: remove top bar & black borders
    # Original 1920x1080 — crop top 80px, bottom 30px, sides proportionally
    crop_top = int(h * 0.07)   # ~76px from top
    crop_bot = int(h * 0.03)   # ~32px from bottom
    crop_left = int(w * 0.02)  # ~38px from left
    crop_right = int(w * 0.02) # ~38px from right

    frame = frame[crop_top:h-crop_bot, crop_left:w-crop_right]

    # Resize to web width
    h2, w2 = frame.shape[:2]
    ratio = 720 / w2
    frame = cv2.resize(frame, (720, int(h2 * ratio)))

    out_path = os.path.join(out_dir, f"frame_{len(extracted):03d}.png")
    cv2.imwrite(out_path, frame)
    extracted.append(out_path)
    print(f"  Frame {frame_num} cropped -> {out_path}")

cap.release()
print(f"\nDone: {len(extracted)} frames")
