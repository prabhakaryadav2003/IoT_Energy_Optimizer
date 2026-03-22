import cv2
import time

from computer_vision_v2 import OccupancySystem
from mqtt.mqtt_client import MQTTClient
import config


# ------------------ INIT ------------------

mqtt = MQTTClient(config.MQTT_BROKER)
mqtt.connect()

vision = OccupancySystem("RPI/models/yolov8n_saved_model/yolov8n_int8.tflite")

cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)

frame_id = 0
people = 0

# Store last detections for rendering between skipped frames
last_result = None


# ------------------ LOOP ------------------

try:    
    print(mqtt.is_connected())
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # -------- Detection (skip frames) --------
        if frame_id % 3 == 0:
            last_result = vision.process(frame)
            people = last_result["count"]

            mqtt.publish(
                config.OCC_TOPIC,
                {"count": people}
            )

            print(f"[VISION] People: {people}")

        frame_id += 1

        # -------- Rendering --------
        display = frame.copy()

        if last_result is not None:
            # Draw bounding boxes
            for t in last_result.get("tracks", []):
                x, y, w, h = map(int, t.bbox)

                cv2.rectangle(display, (x, y), (x+w, y+h), (0, 255, 0), 2)

                cv2.putText(
                    display,
                    f"ID {t.id}",
                    (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    1
                )

        # Draw people count
        cv2.rectangle(display, (0, 0), (200, 40), (30, 30, 30), -1)
        cv2.putText(
            display,
            f"People: {people}",
            (10, 28),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        # -------- Show --------
        cv2.imshow("Occupancy Vision", display)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.03)

except KeyboardInterrupt:
    print("Stopping vision service...")

finally:
    cap.release()
    cv2.destroyAllWindows()
    mqtt.disconnect()