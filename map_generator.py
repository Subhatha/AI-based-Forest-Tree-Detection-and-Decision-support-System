import os
import glob
import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO

MODEL_PATH = "runs/detect/train/weights/best.pt"
CUT_HEIGHT_THRESHOLD = 180


def create_3d_map(input_folder, output_path):
    model = YOLO(MODEL_PATH)

    image_files = sorted(
        glob.glob(os.path.join(input_folder, "*.jpg"))
    )

    tree_points = []

    for frame_index, image_path in enumerate(image_files):
        image = cv2.imread(image_path)

        if image is None:
            continue

        h, w, _ = image.shape

        results = model(image_path, verbose=False)

        for result in results:
            if result.boxes is None:
                continue

            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()

                box_height = y2 - y1
                x_center = ((x1 + x2) / 2) / w

                decision = "CUT" if box_height < CUT_HEIGHT_THRESHOLD else "KEEP"

                map_x = (x_center - 0.5) * 20
                map_y = frame_index * 1.5
                map_z = (box_height / h) * 30

                tree_points.append((map_x, map_y, map_z, decision))

    if not tree_points:
        raise Exception("No tree detections found for 3D map.")

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    for i, (x, y, z, decision) in enumerate(tree_points, start=1):
        color = "green" if decision == "CUT" else "red"
        ax.scatter(x, y, z, c=color, s=60)
        ax.text(x, y, z, str(i), fontsize=8)

    ax.set_title("3D Forest Tree Decision Map")
    ax.set_xlabel("Left / Right Position")
    ax.set_ylabel("Walking Path Direction")
    ax.set_zlabel("Estimated Tree Size")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    return output_path