import os
import glob
import cv2
import plotly.graph_objects as go
from ultralytics import YOLO

MODEL_PATH = "runs/detect/train/weights/best.pt"
CUT_HEIGHT_THRESHOLD = 180


def create_interactive_3d_map(input_folder, output_html):
    model = YOLO(MODEL_PATH)

    image_files = sorted(glob.glob(os.path.join(input_folder, "*.jpg")))

    xs = []
    ys = []
    zs = []
    colors = []
    labels = []

    tree_id = 1

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
                conf = float(box.conf[0])

                box_height = y2 - y1
                x_center = ((x1 + x2) / 2) / w

                decision = "CUT" if box_height < CUT_HEIGHT_THRESHOLD else "KEEP"

                map_x = (x_center - 0.5) * 20
                map_y = frame_index * 1.5
                map_z = (box_height / h) * 30

                xs.append(map_x)
                ys.append(map_y)
                zs.append(map_z)

                colors.append("green" if decision == "CUT" else "red")

                labels.append(
                    f"Tree ID: {tree_id}<br>"
                    f"Decision: {decision}<br>"
                    f"Confidence: {conf:.2f}<br>"
                    f"X: {map_x:.2f}<br>"
                    f"Y: {map_y:.2f}<br>"
                    f"Estimated Size: {map_z:.2f}"
                )

                tree_id += 1

    if not xs:
        raise Exception("No detections found for interactive map.")

    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=xs,
                y=ys,
                z=zs,
                mode="markers",
                marker=dict(
                    size=6,
                    color=colors,
                    opacity=0.85
                ),
                text=labels,
                hoverinfo="text"
            )
        ]
    )

    fig.update_layout(
        title="Interactive 3D Forest Tree Decision Map",
        scene=dict(
            xaxis_title="Left / Right Position",
            yaxis_title="Walking Path Direction",
            zaxis_title="Estimated Tree Size"
        )
    )

    fig.write_html(output_html)

    return output_html