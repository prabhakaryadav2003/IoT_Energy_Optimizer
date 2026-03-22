from utils import MovingAverage


class SensorSmoother:

    def __init__(self, window_size=5):
        self.temp = MovingAverage(window_size)
        self.humidity = MovingAverage(window_size)
        self.nox = MovingAverage(window_size)
        self.voc = MovingAverage(window_size)
        self.pm25 = MovingAverage(window_size)

    def smooth(self, data):
        data.temperature = self.temp.update(data.temperature)
        data.humidity = self.humidity.update(data.humidity)
        data.nox_index = self.nox.update(data.nox_index)
        data.voc_index = self.voc.update(data.voc_index)
        data.pm2_5 = self.pm25.update(data.pm2_5)

        return data