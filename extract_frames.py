import cv2
import os

video_path = r"d:\ClaudeProjects\ROCKYP\P1\2026-07-02 18-46-49.mp4"
out_dir = r"d:\ClaudeProjects\ROCKYP\P1\frames"
os.makedirs(out_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = total_frames / fps if fps > 0 else 0

print(f"Video: {total_frames} frames, {fps:.1f} fps, {duration:.1f}s")

# Sample: take frames evenly across the video, ~15 key frames
target_frames = 15
interval = max(1, total_frames // target_frames)

extracted = []
frame_num = 0
while frame_num < total_frames:
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()
    if not ret:
        break
    # Resize to a reasonable width for web
    h, w = frame.shape[:2]
    ratio = 720 / w
    frame = cv2.resize(frame, (720, int(h * ratio)))
    out_path = os.path.join(out_dir, f"frame_{len(extracted):03d}.png")
    cv2.imwrite(out_path, frame)
    extracted.append(out_path)
    print(f"  Frame {frame_num} -> {out_path} ({w}x{h} -> 720x{int(h*ratio)})")
    frame_num += interval

cap.release()
print(f"\nExtracted {len(extracted)} key frames to {out_dir}")
