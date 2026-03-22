import config

class VentilationPredictor:

    PREVENTIVE_THRESHOLD = 55

    def should_ventilate(self, score, trend_rising):

        # Critical air quality
        if score > config.AQI_EMERGENCY_THRESHOLD:
            return True

        # Preventive ventilation
        if trend_rising and score > config.AQI_PREVENTIVE_THRESHOLD:
            return True

        return False