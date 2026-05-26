import os
import glob
import cv2
from ultralytics import YOLO
from tracker import CentroidTracker

MODEL_PATH = "runs/detect/train/weights/best.pt"
CUT_HEIGHT_THRESHOLD = 180


def detect_trees(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    model = YOLO(MODEL_PATH)
    tracker = CentroidTracker(max_distance=100)

    image_files = sorted(
        glob.glob(os.path.join(input_folder, "*.jpg"))
    )

    stats = {
        "total": 0,
        "cut": 0,
        "keep": 0
    }

    for image_path in image_files:
        image = cv2.imread(image_path)

        if image is None:
            continue

        results = model(image_path, verbose=False)

        frame_detections = []
        detection_data = []

        for result in results:
            if result.boxes is None:
                continue

            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])

                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                frame_detections.append((cx, cy))
                detection_data.append((x1, y1, x2, y2, conf))

        tracked_objects = tracker.update(frame_detections)

        used_boxes = set()

        for object_id, (cx, cy) in tracked_objects.items():
            closest_index = None
            closest_distance = float("inf")

            for index, data in enumerate(detection_data):
                if index in used_boxes:
                    continue

                x1, y1, x2, y2, conf = data

                box_cx = int((x1 + x2) / 2)
                box_cy = int((y1 + y2) / 2)

                distance = ((cx - box_cx) ** 2 + (cy - box_cy) ** 2) ** 0.5

                if distance < closest_distance:
                    closest_distance = distance
                    closest_index = index

            if closest_index is None:
                continue

            used_boxes.add(closest_index)

            x1, y1, x2, y2, conf = detection_data[closest_index]

            box_height = y2 - y1

            decision = "CUT" if box_height < CUT_HEIGHT_THRESHOLD else "KEEP"

            color = (0, 255, 0) if decision == "CUT" else (0, 0, 255)

            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

            nearest_id = None
            nearest_distance = None

            for other_id, (other_cx, other_cy) in tracked_objects.items():
                if other_id == object_id:
                    continue

                distance = ((cx - other_cx) ** 2 + (cy - other_cy) ** 2) ** 0.5

                if nearest_distance is None or distance < nearest_distance:
                    nearest_distance = distance
                    nearest_id = other_id

            if nearest_id is not None:
                label = f"Tree {object_id}: {decision} | Near T{nearest_id}: {nearest_distance:.0f}px"
            else:
                label = f"Tree {object_id}: {decision}"

            cv2.putText(
                image,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

            stats["total"] += 1

            if decision == "CUT":
                stats["cut"] += 1
            else:
                stats["keep"] += 1

        output_path = os.path.join(
            output_folder,
            os.path.basename(image_path)
        )

        cv2.imwrite(output_path, image)

    return stats