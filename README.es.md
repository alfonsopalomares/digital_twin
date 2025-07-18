# Sistema de Monitoreo Industrial 4.0 - Expendedor de Agua

## Descripción General

Sistema de monitoreo en tiempo real para un expendedor de agua industrial, implementando conceptos de Industria 4.0 con análisis de datos avanzado, detección de anomalías adaptativa y métricas de rendimiento integrales.

## Arquitectura del Sistema

### Backend (FastAPI)
- **API REST**: Endpoints para métricas, anomalías y configuración
- **Base de Datos**: SQLite para almacenamiento de lecturas de sensores
- **Detección de Anomalías**: Algoritmo adaptativo basado en z-score
- **Simulación**: Generador de datos de sensores en tiempo real

### Frontend (React)
- **Dashboard Interactivo**: Visualización de métricas en tiempo real
- **Gauges Dinámicos**: Indicadores visuales con colores según estado
- **Alertas Visuales**: Notificaciones de problemas y anomalías
- **Responsive Design**: Interfaz adaptable a diferentes dispositivos

## Endpoints de Métricas

### 1. Endpoint `mtba` (Mean Time Between Adaptive Anomalies)
Mide el tiempo promedio entre anomalías adaptativas detectadas usando análisis z-score.

**Parámetros:**
- `window`: Tamaño de ventana para detección (default: 60)
- `sensor`: Filtro por sensor específico (opcional)

**Respuesta incluye:**
- Tiempo promedio entre anomalías (minutos)
- Estadísticas de intervalos (mínimo, máximo, desviación estándar)
- Tasa de anomalías por hora
- Estado cualitativo (excellent/good/acceptable/poor)
- Distribución por sensor
- Umbrales de clasificación

### 2. Endpoint `level_uptime`
Mide el porcentaje de tiempo que el nivel de agua está dentro del rango aceptable.

**Parámetros:**
- `start`: Timestamp de inicio (ISO format, opcional)
- `end`: Timestamp de fin (ISO format, opcional)

**Respuesta incluye:**
- Porcentaje de uptime
- Estadísticas de nivel (promedio, mínimo, máximo, variabilidad)
- Distribución de lecturas (bajo/normal/overflow)
- Estado cualitativo
- Umbrales de clasificación

### 3. Endpoint `availability`
Mide el porcentaje de tiempo que el sistema está activamente dispensando agua.

**Parámetros:**
- `start`: Timestamp de inicio (ISO format, opcional)
- `end`: Timestamp de fin (ISO format, opcional)

**Respuesta incluye:**
- Porcentaje de disponibilidad
- Estadísticas de flujo (promedio, rango, variabilidad)
- Volumen total dispensado
- Distribución de flujo (cero/bajo/normal)
- Estado cualitativo
- Umbrales de clasificación

### 4. Endpoint `performance`
Compara litros reales dispensados vs esperados basado en configuración.

**Parámetros:**
- `users`: Número de usuarios (opcional)
- `hours`: Horas de operación (opcional)

**Respuesta incluye:**
- Ratio de rendimiento (actual vs esperado)
- Eficiencia como porcentaje
- Déficit o excedente de litros
- Estadísticas de flujo logrado vs configurado
- Estado cualitativo
- Umbrales de clasificación

### 5. Endpoint `quality`
Mide el porcentaje de lecturas de temperatura dentro del rango aceptable.

**Parámetros:**
- `start`: Timestamp de inicio (ISO format, opcional)
- `end`: Timestamp de fin (ISO format, opcional)

**Respuesta incluye:**
- Porcentaje de calidad
- Estadísticas de temperatura (promedio, rango, variabilidad)
- Desviaciones del setpoint
- Distribución de lecturas (bajo/dentro del rango/alto)
- Estado cualitativo
- Umbrales de clasificación

### 6. Endpoint `response_index`
Mide el tiempo promedio de respuesta del sistema ante anomalías adaptativas.

**Parámetros:**
- `window`: Tamaño de ventana para detección (default: 60)
- `sensor`: Filtro por sensor específico (opcional)

**Respuesta incluye:**
- Tiempo promedio de respuesta (minutos)
- Estadísticas de respuesta (mínimo, máximo, variabilidad)
- Distribución por velocidad (rápida/buena/lenta/muy lenta)
- Tasa de respuestas por hora
- Tiempos promedio por sensor
- Estado cualitativo
- Umbrales de clasificación

### 7. Endpoint `energy_efficiency`
Calcula la eficiencia energética en kWh por litro dispensado.

**Parámetros:**
- `start`: Timestamp de inicio (ISO format, opcional)
- `end`: Timestamp de fin (ISO format, opcional)

**Respuesta incluye:**
- Eficiencia energética (kWh/L)
- Ratio vs valor esperado
- Consumo total y volumen
- Estado cualitativo
- Indicador de tolerancia

### 8. Endpoint `thermal_variation`
Mide la variación térmica usando desviación estándar de temperaturas.

**Parámetros:**
- `start`: Timestamp de inicio (ISO format, opcional)
- `end`: Timestamp de fin (ISO format, opcional)

**Respuesta incluye:**
- Variación térmica (°C)
- Estadísticas de temperatura
- Desviación del setpoint
- Estado cualitativo
- Porcentaje dentro de tolerancia

### 9. Endpoint `peak_flow_ratio`
Calcula la relación entre flujo máximo y flujo nominal.

**Parámetros:**
- `users`: Número de usuarios (default: 1)

**Respuesta incluye:**
- Ratio de flujo pico
- Estadísticas de flujo
- Indicadores de capacidad
- Estado cualitativo
- Alertas de límites

### 10. Endpoint `nonproductive_consumption`
Calcula energía consumida durante períodos de inactividad.

**Parámetros:**
- `start`: Timestamp de inicio (ISO format, opcional)
- `end`: Timestamp de fin (ISO format, opcional)

**Respuesta incluye:**
- Consumo no productivo (kWh)
- Número de muestras analizadas

### 11. Endpoint `mtbf` (Mean Time Between Failures)
Calcula el tiempo promedio entre fallas basado en anomalías estáticas.

**Parámetros:**
- `start`: Timestamp de inicio (ISO format, opcional)
- `end`: Timestamp de fin (ISO format, opcional)

**Respuesta incluye:**
- MTBF en horas
- Número de fallas detectadas

### 12. Endpoint `quality_full`
Evalúa la calidad completa de servicios considerando temperatura y volumen.

**Parámetros:**
- `start`: Timestamp de inicio (ISO format, opcional)
- `end`: Timestamp de fin (ISO format, opcional)

**Respuesta incluye:**
- Porcentaje de servicios correctos
- Número total de servicios analizados

### 13. Endpoint `response_time`
Mide el tiempo promedio entre selección y dispensado.

**Parámetros:**
- `start`: Timestamp de inicio (ISO format, opcional)
- `end`: Timestamp de fin (ISO format, opcional)

**Respuesta incluye:**
- Tiempo promedio de respuesta (segundos)
- Número de eventos analizados

### 14. Endpoint `failures_count`
Cuenta el número de fallas en un período específico.

**Parámetros:**
- `weeks`: Número de semanas a considerar (default: 1)

**Respuesta incluye:**
- Número de fallas
- Número total de lecturas

### 15. Endpoint `usage_rate`
Calcula la tasa promedio de servicios por hora.

**Parámetros:**
- `start`: Timestamp de inicio (ISO format, opcional)
- `end`: Timestamp de fin (ISO format, opcional)

**Respuesta incluye:**
- Tasa de uso (servicios/hora)
- Número de lecturas analizadas

## Funcionalidades del Frontend

### Dashboard de Métricas
- **Gauges Interactivos**: Visualización de métricas con colores dinámicos según estado
- **Metadatos Detallados**: Información adicional para cada métrica
- **Alertas Visuales**: Notificaciones de problemas y anomalías
- **Filtros Temporales**: Selección de rangos de tiempo para análisis
- **Responsive Design**: Interfaz adaptable a diferentes dispositivos

### Sistema de Estados
Todas las métricas utilizan un sistema de clasificación consistente:
- **Excellent**: Rendimiento excepcional
- **Good**: Rendimiento bueno
- **Acceptable**: Rendimiento aceptable
- **Poor**: Rendimiento deficiente
- **Critical**: Rendimiento crítico (cuando aplica)

### Sistema de Colores
Los gauges cambian de color según el estado:
- 🟢 Verde: Estado 'excellent'
- 🔵 Azul: Estado 'good' 
- 🟡 Amarillo: Estado 'acceptable'
- 🟠 Naranja: Estado 'poor'
- 🔴 Rojo: Estado 'critical'

### Alertas y Notificaciones
El sistema muestra advertencias automáticas para:
- Valores fuera de tolerancia
- Tasas de anomalías altas
- Estabilidad deficiente del sistema
- Niveles bajos prolongados
- Desbordamientos detectados
- Tiempos de inactividad altos
- Utilización baja del sistema
- Déficits de rendimiento
- Control deficiente de temperatura
- Desviaciones excesivas
- Tiempos de respuesta deficientes
- Porcentajes altos de respuestas lentas

## Configuración del Sistema

### Parámetros de Sensores
- **Temperatura**: Setpoint 60°C, tolerancia ±2.5°C
- **Flujo**: Umbral de inactividad 0.001 L/min
- **Nivel**: Umbral bajo 0.2 (20%)
- **Potencia**: Umbral alto 2.0 kW

### Parámetros de Anomalías
- **Ventana adaptativa**: 60 muestras por defecto
- **Z-score**: Umbral 2.0 para detección de anomalías
- **Agrupación**: Anomalías simultáneas tratadas como eventos únicos

### Parámetros de Rendimiento
- **Flujo configurado**: 0.008 L/min por usuario
- **Usuarios por defecto**: 3
- **Horas por defecto**: 120

## Instalación y Uso

### Requisitos
- Python 3.8+
- Node.js 14+
- SQLite3

### Instalación Backend
```bash
pip install -r requirements.txt
python -m uvicorn api:app --reload
```

### Instalación Frontend
```bash
cd frontend
npm install
npm start
```

### Uso
1. Iniciar el backend en `http://localhost:8000`
2. Iniciar el frontend en `http://localhost:3000`
3. Acceder al dashboard de métricas
4. Configurar parámetros según necesidades

## Estructura de Datos

### Lecturas de Sensores
```json
{
  "timestamp": "2024-12-19T10:30:00",
  "sensor": "temperature",
  "value": 59.8
}
```

### Respuesta de Métricas
```json
{
  "title": "MTBA",
  "unit": "minutes",
  "value": 15.5,
  "expected_value": 15.0,
  "samples": 100,
  "status": "good",
  "metadata": {
    "min_interval": 2.0,
    "max_interval": 45.0,
    "anomaly_rate": 3.87
  }
}
```

## Contribución

Para contribuir al proyecto:
1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios
4. Ejecutar pruebas
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo LICENSE para más detalles.
