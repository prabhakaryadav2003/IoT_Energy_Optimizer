# Smart HVAC System – Updated Documentation

---

# 1. System Overview

This project implements an **intelligent indoor environment control system** that combines:

- Environmental sensing (SEN55)
- Camera-based occupancy detection
- MQTT messaging
- Predictive ventilation
- Occupancy-aware cooling
- Adaptive comfort modeling

The system automatically controls:

- Air conditioners (multiple units)
- Exhaust ventilation

to maintain:

- indoor air quality
- thermal comfort
- energy efficiency

---

# 2. High-Level Architecture

The system follows a modular layered architecture:

```
Sensors / Camera
      │
      ▼
MQTT Input Layer
      │
      ▼
Sensor Module
Occupancy Module
      │
      ▼
Air Quality Module
      │
      ▼
Environment Controller
      │
      ▼
Device Manager
      │
      ▼
AC / Exhaust
```

Each module is isolated and reusable.

---

# 3. Data Flow

```
SEN55 → MQTT → main.py
             │
             ▼
        SensorModule
             │
             ▼
     AirQualityModule
             │
             ▼
     OccupancyModule
             │
             ▼
   EnvironmentController
             │
             ▼
       DeviceManager
             │
             ▼
       AC / Exhaust
```

---

# 4. Updated Folder Structure

```
smart_hvac/
│
├── main.py
├── config/
│
├── mqtt/
│
├── sensors/
├── occupancy/
├── air_quality/
│
├── environment_system/
│   ├── controller.py
│   └── device_manager.py
│
├── utils/
│   ├── moving_average.py
│   ├── time_utils.py
│   ├── protection.py
│   └── comfort.py
```

---

# 5. Core Modules

---

## Sensor Module

### Purpose

Processes raw sensor data and removes noise.

### Features

- Moving average smoothing
- Stabilizes control signals

### Output

```python
{
  "data": EnvironmentData
}
```

---

## Air Quality Module

### Purpose

Evaluates air quality and predicts ventilation needs.

### Components

- AQI Scorer
- Trend Detector
- Ventilation Predictor

### Output

```python
{
  "score": float,
  "trend_rising": bool,
  "ventilate": bool
}
```

---

## Occupancy Module

### Purpose

Converts people count into intelligent signals.

### Features

- Occupancy state tracking
- Time-based learning (pattern model)
- Persistence across restarts
- Precooling prediction

### Output

```python
{
  "occupied": bool,
  "probability": float,
  "confidence": float,
  "precool": bool
}
```

---

## Utils Module

Shared utilities across the system:

### MovingAverage

- Smooths sensor data

### Time Utilities

- Standardized time handling

### CompressorProtection

- Prevents AC short cycling

### ComfortCalculator (Indoor Model)

- Computes perceived temperature
- Uses indoor humidity-adjusted model
- Stable for HVAC control

---

## Device Manager

### Purpose

Unified control for multiple devices.

### Features

- Controls multiple AC units
- Controls exhaust systems
- Supports future device types

### API

```python
turn_on_ac(temp)
turn_off_ac()
turn_on_exhaust()
turn_off_exhaust()
is_exhaust_on()
```

---

## Environment Controller

### Purpose

Central decision engine.

### Inputs

- Sensor data
- Occupancy state
- Air quality analysis

---

# 6. Controller Decision Logic

### 1. Emergency Mode

```
AQI > threshold
```

Action:

```
AC OFF
Exhaust ON
```

---

### 2. Ventilation

```
ventilate == True
```

Action:

```
Exhaust ON
```

---

### 3. Exhaust Override

```
If exhaust ON → AC OFF
```

---

### 4. Occupied Comfort

Maintain:

```
COMFORT_TEMP ± TEMP_BAND
```

Using **feels_like temperature**

---

### 5. Predictive Precooling

```
If precool → AC ON (eco temp)
```

---

### 6. Empty Room

```
AC OFF
```

---

# 7. MQTT Integration

### Topics

| Type      | Topic              |
| --------- | ------------------ |
| Sensor    | sensors/data/sen55 |
| Occupancy | cam/occupancy      |

---

### Sensor Message

```json
{
  "temperature": 29.3,
  "humidity": 72,
  "nox": 110,
  "voc": 80,
  "pm2_5": 15
}
```

---

### Occupancy Message

```json
{
  "count": 2
}
```

---

### Architecture

- Topic-based routing
- Separate handlers per topic
- Thread-safe publishing
- Auto reconnect

---

# 8. Configuration

Centralized in `config/`

```python
COMFORT_TEMP = 24
ECO_TEMP = 27
TEMP_BAND = 1.5

AQI_EMERGENCY_THRESHOLD = 75
AQI_PREVENTIVE_THRESHOLD = 55
```

---

# 9. Deployment

### Hardware

- Raspberry Pi / Jetson Nano
- SEN55 sensor
- Camera
- MQTT broker (Mosquitto)

---

### Steps

1. Install dependencies

```
pip install paho-mqtt numpy
```

2. Start MQTT

```
mosquitto
```

3. Run system

```
python main.py
```

---

# 10. Tuning Guide

| Parameter       | Range   |
| --------------- | ------- |
| Comfort temp    | 23–25°C |
| Eco temp        | 26–28°C |
| AQI threshold   | ~75     |
| Trend threshold | ~15     |

---

# 11. Future Improvements

- Zone-based AC control (using heatmap)
- PID temperature control
- CO₂ estimation
- Adaptive comfort learning
- Multi-room support
- Cloud analytics

---

# Summary

This system is a **modular intelligent HVAC controller** combining:

- sensor fusion
- occupancy learning
- predictive air quality control
- indoor comfort modeling
- safe device control

It is designed for **edge deployment**, scalability, and real-world reliability.
