import os, json

frames_dir = r"d:\ClaudeProjects\ROCKYP\P1\frames"
frames = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
print(json.dumps(frames))
