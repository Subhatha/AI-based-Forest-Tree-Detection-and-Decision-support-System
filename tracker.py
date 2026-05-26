import math


class CentroidTracker:
    def __init__(self, max_distance=80):
        self.next_id = 1
        self.objects = {}
        self.max_distance = max_distance

    def update(self, detections):
        updated_objects = {}
        assigned_ids = set()

        for detection in detections:
            cx, cy = detection

            best_id = None
            best_distance = float("inf")

            for object_id, old_centroid in self.objects.items():
                if object_id in assigned_ids:
                    continue

                ox, oy = old_centroid
                distance = math.sqrt((cx - ox) ** 2 + (cy - oy) ** 2)

                if distance < best_distance:
                    best_distance = distance
                    best_id = object_id

            if best_id is not None and best_distance < self.max_distance:
                updated_objects[best_id] = (cx, cy)
                assigned_ids.add(best_id)
            else:
                updated_objects[self.next_id] = (cx, cy)
                assigned_ids.add(self.next_id)
                self.next_id += 1

        self.objects = updated_objects
        return self.objects