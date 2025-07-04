# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Import modules
from simulator import SensorSimulator
from storage import LocalStorage

# Import API endpoints
from metrics_endpoints import router as metrics_router
from simulate_endpoints import router as simulate_router
from anomalies_endpoints import router as anomalies_router
from readings_endpoints import router as readings_router

from settings import *

app = FastAPI()
# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar dominios en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Instancias únicas de simulador y almacenamiento
simulator = SensorSimulator(avg_flow_rate=0.5)
storage = LocalStorage()


@app.get("/")
def api_root():
    return {
        "readings": {
            "all": "/readings",
            "latest": "/readings/latest",
            "delete": "/readings (DELETE)"
        },
        "anomalies": {
            "static": "/anomalies/static",
            "adaptive": "/anomalies/adaptive?sensor={sensor}&window={window}",
            "classify": "/anomalies/classify?sensor={sensor}&window={window}"
        },
        "simulations": {
            "simulate": "/simulate?hours={hours}&users={users}",
            "simulate_scenarios": "/simulate_scenarios?duration_hours={duration_hours}"
        },
        "metrics": {
            "availability": "/metrics/availability?start={ISO}&end={ISO}",
            "performance": "/metrics/performance?users={n}&hours={h}",
            "quality": "/metrics/quality?start={ISO}&end={ISO}",
            "energy_efficiency": "/metrics/energy_efficiency?start={ISO}&end={ISO}",
            "peak_flow_ratio": "/metrics/peak_flow_ratio?users={n}",
            "mtba": "/metrics/mtba",
            "level_uptime": "/metrics/level_uptime?start={ISO}&end={ISO}",
            "response_index": "/metrics/response_index",
            "thermal_variation": "/metrics/thermal_variation?start={ISO}&end={ISO}",
            "nonproductive_consumption": "/metrics/nonproductive_consumption?start={ISO}&end={ISO}"
        }
    }




app.include_router(metrics_router)
app.include_router(simulate_router)
app.include_router(anomalies_router)
app.include_router(readings_router)