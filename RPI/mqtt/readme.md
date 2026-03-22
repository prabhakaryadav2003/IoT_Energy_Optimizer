# MQTT Module

## Overview

Handles communication between system components.

---

## Features

- Topic-based routing
- Auto reconnect
- Thread-safe publish
- JSON messages

---

## Usage

### Connect

```python
mqtt.connect()
```

---

### Subscribe

```python
mqtt.subscribe("topic", callback)
```

---

### Publish

```python
mqtt.publish("topic", {"key": "value"})
```

---

## Callback

```python
def callback(topic, message):
    print(topic, message)
```

---

## Notes

- Handles unstable networks
- Designed for Raspberry Pi deployment
