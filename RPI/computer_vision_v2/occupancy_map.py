import numpy as np
import cv2

class OccupancyMap:
    def __init__(self, width=200, height=200, decay=0.96):
        self.map = np.zeros((height, width), dtype=np.float32)
        self.decay = decay

    def update(self, points):
        self.map *= self.decay

        for x, y in points:
            if 0 <= x < self.map.shape[1] and 0 <= y < self.map.shape[0]:
                self.map[y, x] += 2

    def render(self):
        norm = cv2.normalize(self.map, self.map.copy(), 0, 255, cv2.NORM_MINMAX)
        norm = norm.astype(np.uint8)

        heat = cv2.applyColorMap(norm, cv2.COLORMAP_JET)
        heat[norm == 0] = 0

        return heat