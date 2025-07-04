# Proyecto Industria 4.0: Expendedor de Agua Inteligente

Este repositorio contiene dos partes principales:

- **Backend**: API REST con FastAPI y SQLite para simular, almacenar lecturas de sensores y calcular métricas.
- **Frontend**: Aplicación React con React Router, Recharts y React‑Bootstrap para interactuar con la API, simular datos y visualizar dashboards.

---

## Prerrequisitos

### General

- Git
- Conexión a internet para descargar dependencias

### Backend

- Python 3.10 o superior
- `pip` (gestor de paquetes de Python)

### Frontend

- Node.js (v16 o superior) y npm (incluido con Node)

---

## Instalación y Ejecución del Backend

1. Clonar el repositorio y entrar en la carpeta `backend`:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <CARPETA>/backend
   ```
2. Crear y activar un entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\\Scripts\\activate   # Windows
   ```
3. Instalar dependencias:
   ```bash
   pip install --upgrade pip
   pip install fastapi uvicorn pydantic sqlite3
   ```
4. Iniciar la API:
   ```bash
   uvicorn api:app --reload
   ```
   - **Documentación interactiva**: http://localhost:8000/docs

---

## Endpoints del Backend

### Lecturas de sensores

| Método | Ruta                    | Descripción                                        |
| ------ | ----------------------- | -------------------------------------------------- |
| GET    | `/readings`             | Devuelve todas las lecturas almacenadas.           |
| GET    | `/readings/latest`      | Retorna la lectura más reciente.                   |
| DELETE | `/readings`             | Elimina todas las lecturas.                        |
| POST   | `/simulate?hours=&users=` | Simula `hours` horas con `users` usuarios.          |

### Anomalías

| Método | Ruta           | Descripción                                                    |
| ------ | -------------- | -------------------------------------------------------------- |
| GET    | `/anomalies`   | Detecta anomalías: sobretemperatura, inactividad, nivel bajo, consumo alto. |

### Métricas OEE y extendidas `/metrics`

Se exponen 10 endpoints para métricas:

| Ruta                          | Parámetros                          | Descripción                                                        |
| ----------------------------- | ---------------------------------- | ------------------------------------------------------------------ |
| `/metrics/availability`       | `start`, `end`                     | % tiempo con `flow`>0.                                             |
| `/metrics/performance`        | `users`, `hours`                   | Litros reales vs esperados.                                        |
| `/metrics/quality`            | `start`, `end`                     | % temperaturas dentro de ±1°C.                                      |
| `/metrics/energy_efficiency`  | `start`, `end`                     | kWh consumidos por litro dispensado.                               |
| `/metrics/peak_flow_ratio`    | `users`                            | Máximo flujo / flujo nominal por usuario.                          |
| `/metrics/mtba`               | —                                  | Tiempo medio entre anomalías (minutos).                            |
| `/metrics/level_uptime`       | `start`, `end`                     | % tiempo nivel entre 20% y 100%.                                   |
| `/metrics/response_index`     | —                                  | Promedio minutos hasta recuperación tras anomalía.                 |
| `/metrics/thermal_variation`  | `start`, `end`                     | Desviación estándar de temperatura (°C).                           |
| `/metrics/nonproductive_consumption` | `start`, `end`             | kWh consumidos con `flow`≤umbral.                                  |

Para incluir estas rutas, en `api.py`:
```python
from api_metrics_endpoints import router as metrics_router
app.include_router(metrics_router)
```

---

## Instalación y Ejecución del Frontend

1. Moverse al directorio `frontend`:
   ```bash
   cd ../frontend
   ```
2. Instalar Node.js y npm (desde [nodejs.org](https://nodejs.org/)) y verificar:
   ```bash
   node -v
   npm -v
   ```
3. Instalar dependencias:
   ```bash
   npm install
   npm install react-router-dom recharts react-bootstrap bootstrap
   ```
4. Importar CSS de Bootstrap en `src/index.js`:
   ```js
   import 'bootstrap/dist/css/bootstrap.min.css';
   ```
5. Iniciar la app:
   ```bash
   npm start
   ```
   - Visitar http://localhost:3000

---

## Estructura del Frontend

- **`index.js`**: Renderiza `<App />` envuelto en `<BrowserRouter>`.
- **`App.jsx`**: Barra de menú (Home, Simulación, Analytics, Anomalías) y `Routes`:
  - `/` → `MainPage.jsx`
  - `/simulate` → `SimulatePage.jsx`
  - `/analytics` → `AnalyticsPage.jsx`
  - `/anomalies` → `AnomaliesPage.jsx`
- **`MainPage.jsx`**: Landing con enlaces.
- **`SimulatePage.jsx`**: Inputs de horas y usuarios, botones de Simular y Limpiar, display de lecturas en grilla.
- **`AnalyticsPage.jsx`**: Muestra `AnalyticsDashboard.jsx`, gráficos con zoom/pan y umbrales.
- **`AnomaliesPage.jsx`**: Muestra `AnomaliesDashboard.jsx`, tablas por sensor y resúmenes.

---

## Cambios Front-end Relevantes

- **Menú de navegación dinámico** con estilos custom.
- **React Router** para múltiples páginas.
- **Recharts** para gráficas interactivas (`/analytics`).
- **React-Bootstrap** para tablas responsivas en anomalías.
- **Dashboard de anomalías**: agrupación por sensor, scroll interno y resumen.

---

## Ajustes y Personalizaciones

- Umbrales y setpoints en código (adj. en `simulator.py` y dashboards).
- Ajusta estilos CSS directamente o integra Tailwind si lo deseas.

---