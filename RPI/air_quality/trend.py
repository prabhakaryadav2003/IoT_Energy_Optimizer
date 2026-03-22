from collections import deque


class AirTrendDetector:

    def __init__(self, window=6, threshold=15):
        self.history = deque(maxlen=window)
        self.threshold = threshold

    def update(self, score):
        self.history.append(score)

        if len(self.history) < (self.history.maxlen or 0):
            return False

        trend = self.history[-1] - self.history[0]
        return trend > self.threshold