from .smoother import SensorSmoother


class SensorModule:

    def __init__(self):
        self.smoother = SensorSmoother()

    def update(self, data):
        """
        Process raw sensor data.

        Returns smoothed data.
        """
        data = self.smoother.smooth(data)

        return {
            "data": data
        }