class Track:
    def __init__(self, bbox, tid):
        self.bbox = bbox
        self.id = tid
        self.missed = 0


class Tracker:
    def __init__(self, max_missed=5):
        self.tracks = []
        self.next_id = 1
        self.max_missed = max_missed

    def iou(self, a, b):
        xA = max(a[0], b[0])
        yA = max(a[1], b[1])
        xB = min(a[0]+a[2], b[0]+b[2])
        yB = min(a[1]+a[3], b[1]+b[3])

        inter = max(0, xB-xA) * max(0, yB-yA)
        union = a[2]*a[3] + b[2]*b[3] - inter
        return inter / union if union else 0

    def update(self, detections):
        assigned = set()

        for t in self.tracks:
            best_iou, best_i = 0, -1

            for i, d in enumerate(detections):
                if i in assigned:
                    continue

                iou = self.iou(t.bbox, d)
                if iou > best_iou:
                    best_iou, best_i = iou, i

            if best_iou > 0.3:
                t.bbox = detections[best_i]
                t.missed = 0
                assigned.add(best_i)
            else:
                t.missed += 1

        self.tracks = [t for t in self.tracks if t.missed < self.max_missed]

        for i, d in enumerate(detections):
            if i not in assigned:
                self.tracks.append(Track(d, self.next_id))
                self.next_id += 1

        return self.tracks