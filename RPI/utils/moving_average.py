from collections import deque
from statistics import mean


class MovingAverage:
    """
    Simple moving average filter
    """

    def __init__(self, size=5):
        self.values = deque(maxlen=size)

    def update(self, value):
        self.values.append(value)
        return mean(self.values)

    def reset(self):
        self.values.clear()