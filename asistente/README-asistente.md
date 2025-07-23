# Asistente Conversacional con LLM

Aplicación Dash que integra un agente LLM con visualizaciones en Plotly y consulta sobre DataFrames precargados. Ideal para análisis técnico, monitoreo de sensores y asistencia con gemelos digitales.

---
## Preparación del entorno Python

Para ejecutar el asistente correctamente, necesitás configurar un entorno con los siguientes paquetes principales:
🔧 Requisitos mínimos
 - Python >=3.9
 - LangChain >=0.3.0
 - Dash >=2.15.0
 - Dash Table
 - Dash Bootstrap Components >=1.5.0
 - pandas
 - plotly
 - dotenv
 - requests

se pueden instalar lso paques con:
```bash
pip install langchain dash dash-table dash-bootstrap-components pandas plotly dotenv requests
```

Dependiendo del modelo que uses en chat_llm.py, puede que necesites paquetes adicionales. En la prueba se usaron:
 - *OpenAI / OpenRouter* corresponde `langchain-openai`
 - *Google Vertex / Gemini* corresponde `langchain-google-genai`

## Cómo iniciar la aplicación

Asegurate de tener instaladas las dependencias necesarias (`dash`, `dash-bootstrap-components`, `langchain`, etc.) y luego ejecutá:

```bash
python dash_asistente.py
```

La aplicación se abrirá en tu navegador en http://127.0.0.1:8050/.

## Configuración de API Keys

Antes de iniciar, editá el archivo `.env` para incluir las credenciales del proveedor LLM que desees usar. 

## Estructura del proyecto

```
try_agent/
├── dash_asistente.py     # App principal Dash
├── chat_llm.py           # Selección y conexión al modelo LLM
├── chat_asistente.py     # Definición del agente y herramientas
├── api_digital_twin.py   # Consume la API de Gemelo Digital
├── data.py               # Comprueba conexión y recolecta datos
├── assets/
│   ├── logo.png          # Logo de la aplicación
│   └── estilos.css       # Estilos personalizados (opcional)
└── .env                  # API keys necesarias
```