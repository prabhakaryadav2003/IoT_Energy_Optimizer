from .base import BaseDevice
from utils import CompressorProtection

class ACDevice(BaseDevice):

    def __init__(self, mqtt, name):
        super().__init__(mqtt, f"control/{name}/state")
        self.protection = CompressorProtection()

    def turn_on(self, temp):
        if self.state == "ON":
            return

        if not self.protection.can_turn_on():
            return

        self.publish({
            "power": "ON",
            "target_temp": temp
        })

        self.state = "ON"
        self.protection.mark_on()

    def turn_off(self):
        if self.state == "OFF":
            return

        if not self.protection.can_turn_off():
            return

        self.publish({"power": "OFF"})

        self.state = "OFF"
        self.protection.mark_off()