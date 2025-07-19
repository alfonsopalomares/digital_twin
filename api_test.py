# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from response_time_fixed import router as response_time_router

app = FastAPI()

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar dominios en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(response_time_router)

@app.get("/")
def api_root():
    return {
        "test": "Response Time Fixed API",
        "endpoints": {
            "response_time": "/metrics/response_time"
        }
    } 