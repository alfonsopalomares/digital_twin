# -*- coding: utf-8 -*-
import random
import datetime
from typing import List, Dict

class SensorSimulator:
    """
    Genera datos sintéticos de un expendedor de agua basado en parámetros de consumo.
    avg_flow_rate: litros por hora por usuario.
    """
    def __init__(self, avg_flow_rate: float = 0.5):
        # Consumo promedio en litros por hora por usuario
        self.avg_flow_rate = avg_flow_rate

    def generate_frame(self, timestamp: str, users: int = 1) -> List[Dict]:
        """
        Genera una "fotografía" de los sensores en un instante dado.

        :param timestamp: cadena ISO de la fecha/hora (UTC)
        :param users: número de usuarios activos
        :return: lista de lecturas para cada sensor
        """
        # Calcula flujo total (litros/hora) y convierte a litros/minuto
        total_flow_lph = self.avg_flow_rate * users
        flow_lpm = total_flow_lph / 60.0

        # Simulación de valores de sensores
        readings = [
            {
                "sensor": "flow",
                "timestamp": timestamp,
                "value": round(flow_lpm, 3),  # litros/minuto
            },
            {
                "sensor": "temperature",
                "timestamp": timestamp,
                "value": round(25 + random.uniform(-1, 1), 2),  # °C
            },
            {
                "sensor": "level",
                "timestamp": timestamp,
                "value": round(random.uniform(0.0, 1.0), 3),  # proporción tanque lleno
            },
            {
                "sensor": "power",
                "timestamp": timestamp,
                "value": round(random.uniform(0.0, 10.0), 2),  # kW
            },
        ]
        return readings

    @property
    def sensors_count(self) -> int:
        """
        Número de tipos de sensores que devuelve cada frame.
        """
        # Evaluar con un timestamp ficticio para contar sensores
        ts = datetime.datetime.utcnow().isoformat()
        return len(self.generate_frame(timestamp=ts, users=1))