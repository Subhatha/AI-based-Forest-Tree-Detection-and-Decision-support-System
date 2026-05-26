import os
import glob
import cv2


def create_video(input_folder, output_video_path, fps=5):
    image_files = sorted(
        glob.glob(os.path.join(input_folder, "*.jpg"))
    )

    if not image_files:
        raise Exception("No detected frames found to create video.")

    first_frame = cv2.imread(image_files[0])

    if first_frame is None:
        raise Exception("Could not read first frame.")

    height, width, _ = first_frame.shape

    writer = cv2.VideoWriter(
        output_video_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    for image_path in image_files:
        frame = cv2.imread(image_path)

        if frame is not None:
            writer.write(frame)

    writer.release()

    return output_video_path