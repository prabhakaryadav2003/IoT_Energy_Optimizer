# Sensor Module

## Overview

The Sensor Module processes raw environmental sensor data to reduce noise and improve stability.

It provides:

- Smoothed sensor readings
- Consistent input for air quality and control logic

---

## Usage

```python
from sensor_module import SensorModule

sensor = SensorModule()

result = sensor.update(data)
data = result["data"]
```

---

## Output

```python
{
    "data": EnvironmentData
}
```

---

## Components

### SensorSmoother

Applies moving average filtering to:

- Temperature
- Humidity
- NOx index
- VOC index
- PM2.5

---

## Behavior

| Input             | Output          |
| ----------------- | --------------- |
| Noisy sensor data | Smoothed values |
| Sudden spikes     | Dampened        |
| Stable readings   | Maintained      |

---

## Notes

- Uses MovingAverage filter
- Lightweight (suitable for Raspberry Pi)
- Improves AQI stability and control decisions

---

## Integration

Used before Air Quality Module:

```python
data = sensor.update(data)["data"]
aq = air.update(data)
```

---

## Future Improvements

- Outlier rejection
- Sensor calibration
- Drift compensation
- Adaptive smoothing window
