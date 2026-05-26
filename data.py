import os
import cv2


VIDEO_PATH = "1.mp4"
OUTPUT_FOLDER = "dataset_frames"
MAX_FRAMES = 50


def extract_dataset_frames(video_path, output_folder, max_frames=50):
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames == 0:
        print("Error: Video has no frames.")
        return

    interval = max(total_frames // max_frames, 1)

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % interval == 0:
            frame_name = f"dataset_frame_{saved_count:04d}.jpg"
            frame_path = os.path.join(output_folder, frame_name)

            cv2.imwrite(frame_path, frame)

            saved_count += 1

            if saved_count >= max_frames:
                break

        frame_count += 1

    cap.release()

    print(f"Done! Extracted {saved_count} frames.")
    print(f"Saved in folder: {output_folder}")


if __name__ == "__main__":
    extract_dataset_frames(VIDEO_PATH, OUTPUT_FOLDER, MAX_FRAMES)