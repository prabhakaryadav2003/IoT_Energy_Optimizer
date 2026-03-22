import json
import os
from collections import defaultdict
import datetime


class OccupancyPatternModel:
    DECAY = 0.995

    def __init__(self, path="occupancy_pattern.json"):
        self.presence = defaultdict(float)
        self.samples = defaultdict(float)
        self.path = path

        self.load()

    def _slot(self):
        now = datetime.datetime.now()
        return now.hour * 4 + now.minute // 15

    def update(self, occupied):
        slot = self._slot()

        # decay
        for k in list(self.samples.keys()):
            self.samples[k] *= self.DECAY
            self.presence[k] *= self.DECAY

        self.samples[slot] += 1

        if occupied:
            self.presence[slot] += 1

    def probability(self):
        slot = self._slot()
        s = self.samples[slot]

        if s < 5:
            return 0

        return self.presence[slot] / s

    def confidence(self):
        return self.samples[self._slot()]

    # ---------------- PERSISTENCE ----------------

    def save(self):
        data = {
            "presence": dict(self.presence),
            "samples": dict(self.samples)
        }

        tmp_path = self.path + ".tmp"

        with open(tmp_path, "w") as f:
            json.dump(data, f)

        os.replace(tmp_path, self.path)  # atomic write

    def load(self):
        if not os.path.exists(self.path):
            return

        try:
            with open(self.path, "r") as f:
                data = json.load(f)

            self.presence = defaultdict(float, data.get("presence", {}))
            self.samples = defaultdict(float, data.get("samples", {}))

            print("[Occupancy] Pattern loaded")

        except Exception as e:
            print(f"[Occupancy] Failed to load: {e}")