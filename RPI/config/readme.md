# Configuration Module

## Overview

Centralized configuration for system behavior, thresholds, and communication settings.

---

## Usage

```python
import config

if score > config.AQI_EMERGENCY_THRESHOLD:
    ...
```

---

## Sections

---

### Comfort Settings

```python
COMFORT_TEMP = 24
ECO_TEMP = 27
TEMP_BAND = 1.5
```

- Defines HVAC target temperatures
- TEMP_BAND provides hysteresis to prevent rapid switching

---

### MQTT Settings

```python
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
```

- Broker connection settings

---

### Topics

```python
SEN55_TOPIC = "sensors/data/sen55"
SCD30_TOPIC = "sensors/data/scd30"
OCC_TOPIC = "cam/occupancy"
```

- Sensor data topics
- Occupancy data topic

---

### Air Quality Thresholds

```python
AQI_EMERGENCY_THRESHOLD = 75
AQI_PREVENTIVE_THRESHOLD = 55
```

- Emergency: immediate ventilation
- Preventive: early action on rising pollution

---

### System Settings

```python
LOOP_DELAY = 0.01
```

- Controls main loop timing

---

## Notes

- Centralized tuning of system behavior
- Avoid hardcoding values in modules
- Makes system easier to calibrate and deploy

---

## Best Practices

- Adjust thresholds based on environment
- Use different configs for testing vs production
- Keep all constants here for maintainability
