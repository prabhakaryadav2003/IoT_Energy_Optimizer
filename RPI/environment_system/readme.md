# Environment System

## Overview

Controls AC and exhaust based on:

- Air quality
- Occupancy
- Comfort

---

## Usage

```python
controller.process(sensor_data, occupancy_result)
```

---

## Pipeline

1. Sensor smoothing
2. AQI scoring
3. Trend detection
4. Ventilation decision
5. Comfort calculation

---

## Logic

### Emergency

```
if AQI > 75:
    AC OFF
    Exhaust ON
```

---

### Ventilation

```
if pollution rising:
    Exhaust ON
else:
    Exhaust OFF
```

---

### Cooling

If exhaust ON:

```
AC OFF
```

If occupied:

```
Hot → AC ON
Cold → AC OFF
```

If precool:

```
AC ON (eco)
```

If empty:

```
AC OFF
```

---

## Notes

- Exhaust overrides AC
- Real-time control loop

---

# Device Manager

## Overview

Manages multiple AC and exhaust devices.

---

## Usage

```python
devices = DeviceManager(mqtt)

devices.add_ac("ac1")
devices.add_ac("ac2")
devices.add_exhaust("exhaust")
```

---

## API

### AC

```python
devices.turn_on_ac(temp)
devices.turn_off_ac()
```

---

### Exhaust

```python
devices.turn_on_exhaust()
devices.turn_off_exhaust()
```

---

### State

```python
devices.is_exhaust_on()
```

---

## Features

- Multi-device support
- Group control
- Extensible

---

## Notes

- AC includes compressor protection
