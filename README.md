# Proyecto Industria 4.0: Expendedor de Agua Inteligente

Este repositorio contiene dos partes principales:

- **Backend**: API REST construida con FastAPI y SQLite para simular y almacenar lecturas de sensores.
- **Frontend**: Aplicación React para interactuar con la API, simular datos y mostrar dashboards analíticos.

---

## Prerrequisitos

### General

- Git
- Conexión a internet para descargar dependencias

### Backend

- Python 3.10 o superior
- `pip` (gestor de paquetes de Python)

### Frontend

- Node.js (v16 o superior) y npm (incluido con Node)

---

## Instalación y Ejecución del Backend

1. **Clonar el repositorio**

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <CARPETA_DEL_PROYECTO>/backend
   ```

2. **Crear y activar un entorno virtual**

   ```bash
   python3 -m venv venv        # Crear entorno virtual
   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Instalar dependencias**

   ```bash
   pip install --upgrade pip
   pip install fastapi uvicorn pydantic sqlite3
   ```

4. **Ejecutar la API**

   ```bash
   uvicorn api:app --reload
   ```

   - La API quedará disponible en `http://localhost:8000`
   - Documentación interactiva OpenAPI: `http://localhost:8000/docs`

---

## Instalación y Ejecución del Frontend

1. **Ingresar al directorio del frontend**

   ```bash
   cd ../frontend
   ```

2. **Instalar Node.js y npm**

   - Descargar e instalar desde [nodejs.org](https://nodejs.org/)
   - Verificar versiones:
     ```bash
     node -v
     npm -v
     ```

3. **Instalar dependencias del proyecto**

   ```bash
   npm install
   ```

4. **Iniciar la aplicación React**

   ```bash
   npm start
   ```

   - Abre `http://localhost:3000` en tu navegador.

---

## Estructura de Carpetas

```plaintext
backend/
├── api.py             # Punto de entrada FastAPI
├── simulator.py       # Generador de lecturas de sensores
├── storage.py         # Persistencia en SQLite
├── sensor_data.db     # Base de datos SQLite (creada en ejecución)
└── venv/              # Entorno virtual Python

frontend/
├── public/
│   └── index.html     # HTML base
├── src/
│   ├── App.jsx        # Router y navegación
│   ├── MainPage.jsx   # Página principal
│   ├── SimulatePage.jsx  # Página de simulación
│   ├── AnalyticsPage.jsx  # Página de dashboards
│   └── AnalyticsDashboard.jsx # Componente de gráficas
├── package.json       # Dependencias y scripts
└── node_modules/      # Paquetes npm
```

---

## Uso

1. Arrancar el backend:
   ```bash
   cd backend
   source venv/bin/activate  # o venv\Scripts\activate
   uvicorn api:app --reload
   ```
2. Arrancar el frontend:
   ```bash
   cd frontend
   npm install
   npm start
   ```
3. Navegar a `http://localhost:3000` y usar los enlaces "Home", "Simulación" y "Analytics".

---

## Ajustes de Umbrales

En `AnalyticsDashboard.jsx` puedes modificar las constantes:

```js
const TEMP_THRESHOLD       = 85.0;   // Temperatura (°C)
const FLOW_IDLE_THRESHOLD  = 0.002;  // Flujo mínimo (L/min)
const FLOW_LEAK_THRESHOLD  = 0.05;   // Flujo de fuga (L/min)
const LEVEL_LOW_THRESHOLD  = 0.20;   // Nivel mínimo (proporción)
const POWER_HIGH_THRESHOLD = 8.0;    // Potencia alta (kW)
```

Ajusta estos valores según tus necesidades.

---

¡Listo! Ahora tienes un **README.md** completo para instalar y ejecutar tu proyecto tanto en backend como en frontend. Puedes descargarlo o copiarlo directamente del lienzo.
