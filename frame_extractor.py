import os
import cv2

def extract_frames(video_path, output_folder, fps_extract=5):
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception("Could not open video file.")

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    interval = max(int(video_fps / fps_extract), 1)

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % interval == 0:
            frame_name = f"frame_{saved_count:05d}.jpg"
            frame_path = os.path.join(output_folder, frame_name)
            cv2.imwrite(frame_path, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    return saved_count