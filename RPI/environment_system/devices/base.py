class BaseDevice:
    def __init__(self, mqtt, topic):
        self.mqtt = mqtt
        self.topic = topic
        self.state = "OFF"

    def publish(self, payload):
        self.mqtt.publish(self.topic, payload)