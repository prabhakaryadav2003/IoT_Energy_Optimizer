# Occupancy Module

## Overview

The Occupancy Module converts raw people count into intelligent signals used by the environment controller.

It provides:

- Occupancy state (occupied / empty)
- Probability of presence
- Confidence level
- Precooling signal

---

## Usage

```python
from occupancy_module import OccupancyModule

occ = OccupancyModule()

result = occ.update(count)
```

---

## Output

```python
{
    "state": "OCCUPIED" | "EMPTY",
    "occupied": bool,
    "probability": float,
    "confidence": float,
    "precool": bool,
    "count": int
}
```

---

## Components

### OccupancyState

Handles short-term presence logic.

- Uses timeout (`EMPTY_DELAY`)
- Prevents flickering

---

### OccupancyPatternModel

Learns time-based behavior.

- 96 slots/day (15-min)
- Tracks presence & samples
- Uses decay

#### Persistence

- Stored in `occupancy_pattern.json`
- Auto-load + periodic save

---

### OccupancyPredictor

Determines precooling:

```
precool = probability > threshold AND confidence sufficient
```

---

## Notes

- Lightweight (Raspberry Pi friendly)
- Improves over time
