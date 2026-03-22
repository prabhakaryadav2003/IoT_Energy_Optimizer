class OccupancyPredictor:
    PRECOOL_THRESHOLD = 0.6
    MIN_CONFIDENCE = 5

    def should_precool(self, probability, confidence):
        if confidence < self.MIN_CONFIDENCE:
            return False

        return probability > self.PRECOOL_THRESHOLD