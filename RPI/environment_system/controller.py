from sensors import SensorModule
from utils import ComfortCalculator
from air_quality import AirQualityModule
import config


class EnvironmentController:

    def __init__(self, devices, occupancy_module):
        self.devices = devices
        self.occupancy = occupancy_module
        self.sensor = SensorModule()
        self.air = AirQualityModule()
        self.comfort = ComfortCalculator()

    def process(self, data, people):
        # -------- Occupancy --------
        occ = self.occupancy.update(people)

        # -------- Sensor smoothing --------
        sensor = self.sensor.update(data)
        data = sensor["data"]

        # -------- Air Quality --------
        aq = self.air.update(data)

        score = aq["score"]
        ventilate = aq["ventilate"]

        # -------- Emergency --------
        if score > config.AQI_EMERGENCY_THRESHOLD:
            print("Dangerous air quality")

            self.devices.turn_off_ac()
            self.devices.turn_on_exhaust()
            return

        # -------- Ventilation --------
        if ventilate:
            self.devices.turn_on_exhaust()
        else:
            self.devices.turn_off_exhaust()

        # Exhaust overrides AC
        if self.devices.is_exhaust_on():
            self.devices.turn_off_ac()
            return

        # -------- Comfort --------
        feels_like = self.comfort.feels_like(
            data.temperature,
            data.humidity
        )

        # -------- Occupancy logic --------
        if occ["occupied"]:
            if feels_like > config.COMFORT_TEMP + config.TEMP_BAND:
                self.devices.turn_on_ac(config.COMFORT_TEMP)

            elif feels_like < config.COMFORT_TEMP - config.TEMP_BAND:
                self.devices.turn_off_ac()

        elif occ["precool"]:
            print("Precooling")
            self.devices.turn_on_ac(config.ECO_TEMP)

        else:
            self.devices.turn_off_ac()

        print(
            f"AQI:{score:.1f} "
            f"Temp:{data.temperature:.1f} "
            f"Humidity:{data.humidity:.1f} "
            f"Feels:{feels_like:.1f} "
            f"People:{people}"
        )