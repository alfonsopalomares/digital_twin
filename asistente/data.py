
from datetime import datetime, timedelta
import threading
import json
from typing import Dict
import pandas as pd
from digital_twin_api_client import DigitalTwinApiClient


PATH_JSON = "datos.json"

class DataGetter():
    cliente: DigitalTwinApiClient
    intervalo: int
    ult_act: datetime
    datos: Dict[str, pd.DataFrame]
    
    def cliente_online(self):
        return self.cliente.is_online()
    
    def actualizar(self) -> bool:
        ahora = datetime.now()
        print(f"actualizar {ahora}")
        
        if self.ult_act is None or (ahora - self.ult_act) > timedelta(minutes=self.intervalo):
            if self.cliente_online():
                self.datos = self.obtener_datos_gemelo()
                
                # with open(PATH_JSON, "w", encoding="utf-8") as f:
                #     # json.dump(self.datos, f, indent=2, ensure_ascii=False)
                #     json.dump({ k: v.to_dict(orient="records") 
                #                for k,v in self.datos.items()
                #                }, f, indent=2, ensure_ascii=False)
                    
                self.ult_act = ahora
                return True
            
        return False
    
    
    def __init__(self, intervalo: int):
        self.cliente = DigitalTwinApiClient()
        self.intervalo = intervalo
        self.ult_act = None
        
        self.actualizar()
        # Reprogramar el próximo llamado
        # threading.Timer(intervalo, self.actualizar).start()
        
    
    def obtener_datos_gemelo(self) -> Dict[str, pd.DataFrame]:
        df_gemelo = {
            "df_lecturas": self.cliente.get_readings_df(),
            "df_metricas": self.cliente.get_all_metrics_df(),
            "df_anomalias": self.cliente.get_static_anomalies_df(),
            "df_sensores": self.cliente.get_sensor_summary_df()
            }
        return df_gemelo
    
    def obtener_datos(self) -> Dict[str, pd.DataFrame]:
        
        if not self.actualizar():
            # with open(PATH_JSON, "r", encoding="utf-8") as f:
            #     data = json.load(f)
            #     self.datos = { k: pd.DataFrame(data[k]) 
            #                   for k in ["df_lecturas","df_metricas","df_anomalias","df_anomalies"]}
            pass    
            
        return self.datos


