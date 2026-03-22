import time
from .state import OccupancyState
from .pattern import OccupancyPatternModel
from .predictor import OccupancyPredictor


class OccupancyModule:

    SAVE_INTERVAL = 60

    def __init__(self):
        self.state = OccupancyState()
        self.pattern = OccupancyPatternModel()
        self.predictor = OccupancyPredictor()

        self._last_save = time.time()

    def update(self, count: int):
        state = self.state.update(count)
        occupied = state == "OCCUPIED"

        self.pattern.update(occupied)

        probability = self.pattern.probability()
        confidence = self.pattern.confidence()

        precool = self.predictor.should_precool(
            probability,
            confidence
        )

        # periodic save
        now = time.time()
        if now - self._last_save > self.SAVE_INTERVAL:
            self.pattern.save()
            self._last_save = now

        return {
            "state": state,
            "occupied": occupied,
            "probability": probability,
            "confidence": confidence,
            "precool": precool,
            "count": count
        }

    def save(self):
        self.pattern.save()