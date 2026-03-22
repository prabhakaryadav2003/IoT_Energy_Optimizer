class ComfortCalculator:

    def feels_like(self, temp_c, humidity):
        humidity = max(0, min(humidity, 100))

        # humidity ratio centered at 50%
        h = (humidity - 50) / 50.0

        # nonlinear effect
        if temp_c >= 25:
            effect = h * 2.0
        elif temp_c >= 22:
            effect = h * 1.0
        else:
            effect = h * 0.5

        return temp_c + effect