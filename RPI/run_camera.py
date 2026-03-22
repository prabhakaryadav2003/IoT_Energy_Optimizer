import time
import cv2
from picamera2 import Picamera2 #type: ignore

from computer_vision_v2 import OccupancySystem
from mqtt.mqtt_client import MQTTClient
import config


# ------------------ CONFIG ------------------

FRAME_SKIP = 4          # run detection every N frames
SLEEP_TIME = 0.02       # loop delay
USE_LORES = True        # use low-res stream


# ------------------ INIT ------------------

mqtt = MQTTClient(config.MQTT_BROKER)
mqtt.connect()

vision = OccupancySystem("models/yolov8n_saved_model/yolov8n_int8.tflite")

picam2 = Picamera2()

if USE_LORES:
    cam_config = picam2.create_preview_configuration(
        main={"size": (320, 240)},
        lores={"size": (160, 120), "format": "RGB888"}
    )
    stream_name = "lores"
else:
    cam_config = picam2.create_preview_configuration(
        main={"size": (320, 240), "format": "RGB888"}
    )
    stream_name = "main"

picam2.configure(cam_config)
picam2.start()

frame_id = 0
people = 0


# ------------------ LOOP ------------------

try:
    while True:

        # -------- Capture --------
        frame = picam2.capture_array(stream_name)

        # Convert RGB → BGR (OpenCV requirement)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # -------- Detection (skipped frames) --------
        if frame_id % FRAME_SKIP == 0:
            result = vision.process(frame)
            people = result["count"]

            mqtt.publish(
                config.OCC_TOPIC,
                {"count": people}
            )

        frame_id += 1

        # -------- Sleep (CPU control) --------
        time.sleep(SLEEP_TIME)

except KeyboardInterrupt:
    print("Stopping vision service...")
    picam2.stop()
    mqtt.disconnect()