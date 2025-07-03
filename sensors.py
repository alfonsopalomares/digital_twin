
# -*- coding: utf-8 -*-

import random
from datetime import datetime
import pandas as pd
from typing import List

class VirtualSensor:
    """
    Base class for virtual sensors. Each sensor must implement the read() method.
    """
    def __init__(self, name: str):
        self.name = name

    def read(self) -> dict:
        raise NotImplementedError("Subclasses must implement this method")

class TemperatureSensor(VirtualSensor):
    def __init__(self, name: str = 'temperature', min_temp: float = 4.0, max_temp: float = 90.0):
        super().__init__(name)
        self.min_temp = min_temp
        self.max_temp = max_temp

    def read(self) -> dict:
        value = random.uniform(self.min_temp, self.max_temp)
        return {'sensor': self.name,
                'timestamp': datetime.utcnow(),
                'value': round(value, 2)}

class FlowSensor(VirtualSensor):
    def __init__(self, name: str = 'flow', min_flow: float = 0.1, max_flow: float = 1.5):
        super().__init__(name)
        self.min_flow = min_flow
        self.max_flow = max_flow

    def read(self) -> dict:
        value = random.uniform(self.min_flow, self.max_flow)
        return {'sensor': self.name,
                'timestamp': datetime.utcnow(),
                'value': round(value, 3)}

class LevelSensor(VirtualSensor):
    def __init__(self, name: str = 'level'):
        super().__init__(name)

    def read(self) -> dict:
        value = random.uniform(0.0, 100.0)
        return {'sensor': self.name,
                'timestamp': datetime.utcnow(),
                'value': round(value, 1)}

class PowerSensor(VirtualSensor):
    def __init__(self, name: str = 'power', min_watt: float = 0.0, max_watt: float = 2000.0):
        super().__init__(name)
        self.min_watt = min_watt
        self.max_watt = max_watt

    def read(self) -> dict:
        value = random.uniform(self.min_watt, self.max_watt)
        return {'sensor': self.name,
                'timestamp': datetime.utcnow(),
                'value': round(value, 1)}

class SensorSimulator:
    """
    Aggregates readings from multiple virtual sensors.
    """
    def __init__(self, sensors: List[VirtualSensor]):
        self.sensors = sensors

    def run_once(self) -> pd.DataFrame:
        records = [s.read() for s in self.sensors]
        return pd.DataFrame(records)