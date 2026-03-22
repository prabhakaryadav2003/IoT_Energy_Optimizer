# Utils Module

## Overview

Provides shared utility functions and lightweight components used across the system.

Includes:

- Time utilities
- Moving average filter
- Compressor protection
- Indoor comfort calculation

---

## Usage

```python
from utils import (
    MovingAverage,
    now,
    CompressorProtection,
    ComfortCalculator
)
```

---

## Components

---

### MovingAverage

```python
ma = MovingAverage(size=5)
value = ma.update(new_value)
```

- Smooths noisy data
- Used in sensor processing
- Helps stabilize control decisions

---

### Time Utilities

```python
from utils import now, seconds_since, current_slot
```

Functions:

- `now()` → current timestamp
- `seconds_since(ts)`
- `minutes_since(ts)`
- `current_hour()`
- `current_slot()` (15-min default)

---

### CompressorProtection

```python
cp = CompressorProtection()

if cp.can_turn_on():
    cp.mark_on()
```

Prevents:

- rapid ON/OFF cycling
- compressor damage

#### Rules

- Minimum OFF time before turning ON
- Minimum ON time before turning OFF

---

### ComfortCalculator (Indoor Model)

```python
from utils import ComfortCalculator

cc = ComfortCalculator()
feels = cc.feels_like(temp, humidity)
```

---

## Indoor Comfort Model

The system uses a **lightweight indoor comfort approximation** instead of the outdoor Heat Index.

### Why not Heat Index?

- Designed for outdoor conditions
- Inaccurate below ~27°C
- Produces unstable values indoors

---

### Model Behavior

The model adjusts perceived temperature based on humidity:

```text
Feels Like = Temperature + Humidity Adjustment
```

#### Key Properties

- Stable in indoor range (18–30°C)
- Humidity influence is controlled and realistic
- No extreme spikes

---

### Example Behavior

| Temp | Humidity | Feels Like |
| ---- | -------- | ---------- |
| 24°C | 50%      | 24.0       |
| 24°C | 70%      | ~24.8      |
| 26°C | 70%      | ~27.2      |
| 22°C | 70%      | ~22.4      |

---

### Interpretation

- Higher humidity → feels warmer
- Lower humidity → feels cooler
- Effect increases at higher temperatures

---

## Integration

Used in EnvironmentController:

```python
feels_like = comfort.feels_like(
    data.temperature,
    data.humidity
)
```

---

## Notes

- Designed for HVAC control systems
- Lightweight and fast (Raspberry Pi compatible)
- Improves stability of AC decisions
- Works well with occupancy-based control

---

## Future Improvements

- Adaptive comfort (learn user preference)
- Zone-based comfort adjustments
- Personalized comfort profiles
- Seasonal tuning

---
