from .time_utils import now


class CompressorProtection:
    """
    Prevents rapid ON/OFF cycles for compressors
    """

    MIN_OFF = 180
    MIN_ON = 180

    def __init__(self):
        self.last_on = 0
        self.last_off = 0
        self.state = "OFF"

    def can_turn_on(self):
        if self.state == "ON":
            return False

        return now() - self.last_off > self.MIN_OFF

    def can_turn_off(self):
        if self.state == "OFF":
            return False

        return now() - self.last_on > self.MIN_ON

    def mark_on(self):
        self.state = "ON"
        self.last_on = now()

    def mark_off(self):
        self.state = "OFF"
        self.last_off = now()