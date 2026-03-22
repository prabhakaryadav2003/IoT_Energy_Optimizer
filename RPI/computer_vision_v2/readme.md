# Computer Vision System

## Overview

Processes camera frames to detect and track humans.

Outputs:

- People count
- Positions
- Heatmap

---

## Usage

```python
from occupancy_system import OccupancySystem

system = OccupancySystem("model.tflite")
result = system.process(frame)
```

---

## Output

```python
{
    "count": int,
    "points": [(x, y)],
    "heatmap": np.array,
    "tracks": [...]
}
```

---

## Components

### HumanDetector

- YOLOv8 TFLite
- INT8 optimized
- Vectorized inference

---

### Tracker

- SORT-like tracker
- IOU matching
- Stable IDs

---

### OccupancyMap

- Heatmap with decay
- Shows spatial usage

---

## Pipeline

Frame → Detection → Tracking → Mapping → Heatmap

---

## Notes

- Optimized for low-power devices
- Can skip frames for performance
