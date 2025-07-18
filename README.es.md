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

### Métricas de Desempeño (`metrics_endpoints.py`)

#### **1. Endpoint `mtba` (Mean Time Between Adaptive Anomalies)**
- `GET /metrics/mtba?window={n}&sensor={s}`
  - MTBA: tiempo medio entre anomalías adaptativas.
  - Incluye estadísticas de intervalos, tasa de anomalías, distribución por sensor y estado cualitativo.

#### **2. Endpoint `level_uptime`**
- `GET /metrics/level_uptime?start={t0}&end={t1}`
  - Level Uptime: % tiempo con nivel de agua aceptable.
  - Incluye estadísticas de nivel, detección de overflow y estado cualitativo.

#### **3. Endpoint `availability`**
- `GET /metrics/availability?start={t0}&end={t1}`
  - Disponibilidad: % de tiempo con flujo > 0.
  - Incluye estadísticas de flujo, volumen total, distribución de lecturas y estado cualitativo.

#### **4. Endpoint `performance`**
- `GET /metrics/performance?users={u}&hours={h}`
  - Rendimiento: ratio de litros reales vs esperados.
  - Incluye eficiencia, déficit/excedente, estadísticas de flujo y estado cualitativo.

#### **5. Endpoint `quality`**
- `GET /metrics/quality?start={t0}&end={t1}`
  - Calidad: % temperatura dentro de ±5°C del setpoint (60°C).
  - Incluye estadísticas térmicas, desviaciones del setpoint y estado cualitativo.

#### **6. Endpoint `response_index`**
- `GET /metrics/response_index?window={n}&sensor={s}`
  - Índice de Respuesta: tiempo promedio de respuesta a anomalías.
  - Incluye estadísticas de respuesta, distribución por velocidad y estado cualitativo.

#### **7. Endpoint `energy_efficiency`**
- `GET /metrics/energy_efficiency?start={t0}&end={t1}`
  - Eficiencia Energética: kWh/L con valor esperado 0.051 kWh/L.
  - Incluye ratio vs esperado, consumos totales y estado cualitativo.

#### **8. Endpoint `thermal_variation`**
- `GET /metrics/thermal_variation?start={t0}&end={t1}`
  - Variación Térmica: desviación estándar de temperaturas.
  - Incluye estadísticas de temperatura, desviación del setpoint y estado cualitativo.

#### **9. Endpoint `peak_flow_ratio`**
- `GET /metrics/peak_flow_ratio?users={u}`
  - Flujo Pico: max flujo / nominal.
  - Incluye estadísticas de flujo, indicadores de capacidad y estado cualitativo.

#### **10. Endpoint `nonproductive_consumption`**
- `GET /metrics/nonproductive_consumption?start={t0}&end={t1}`
  - Consumo No Productivo: kWh en inactividad.

#### **11. Endpoint `mtbf` (Mean Time Between Failures)**
- `GET /metrics/mtbf?start={t0}&end={t1}`
  - MTBF: tiempo medio entre fallas (horas).

#### **12. Endpoint `quality_full`**
- `GET /metrics/quality_full?start={t0}&end={t1}`
  - Calidad Completa: % servicios con temperatura y volumen correctos.

#### **13. Endpoint `response_time`**
- `GET /metrics/response_time?start={t0}&end={t1}`
  - Tiempo de Respuesta: tiempo medio selección→dispensado (segundos).

#### **14. Endpoint `failures_count`**
- `GET /metrics/failures_count?weeks={n}`
  - Conteo de Fallas: número de fallas en las últimas `n` semanas.

#### **15. Endpoint `usage_rate`**
- `GET /metrics/usage_rate?start={t0}&end={t1}`
  - Tasa de Uso: promedio de servicios por hora.

### Detalle de Endpoints de Métricas

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

### Detalle de Métricas en el Dashboard

#### **1. MTBA (Mean Time Between Adaptive Anomalies)**
- **Gauge**: Muestra tiempo promedio entre anomalías (minutos)
- **Metadatos visualizados**:
  - Rango de intervalos (mínimo - máximo)
  - Tasa de anomalías por hora
  - Estado de estabilidad del sistema
  - Distribución por sensor (power, flow, level, temperature)
  - Tiempo analizado y tamaño de ventana
- **Alertas**: Alta tasa de anomalías, estabilidad deficiente

#### **2. Level Uptime**
- **Gauge**: Muestra porcentaje de tiempo con nivel aceptable
- **Metadatos visualizados**:
  - Nivel promedio, mínimo y máximo
  - Variabilidad del nivel (%)
  - Distribución de lecturas (bajo/normal/overflow)
  - Umbral bajo configurado
  - Tiempo analizado
- **Alertas**: Niveles bajos prolongados, desbordamiento detectado

#### **3. Availability**
- **Gauge**: Muestra porcentaje de tiempo con flujo activo
- **Metadatos visualizados**:
  - Flujo promedio, mínimo y máximo
  - Volumen total dispensado
  - Distribución de flujo (cero/bajo/normal)
  - Variabilidad del flujo (%)
  - Tiempo analizado
- **Alertas**: Tiempo alto de inactividad, utilización baja del sistema

#### **4. Performance**
- **Gauge**: Muestra ratio de rendimiento (real vs esperado)
- **Metadatos visualizados**:
  - Litros reales vs esperados
  - Eficiencia como porcentaje
  - Déficit o excedente de litros
  - Tasa de flujo lograda vs configurada
  - Estadísticas de flujo observado
- **Alertas**: Déficit detectado, rendimiento crítico/pobre

#### **5. Quality**
- **Gauge**: Muestra porcentaje de temperatura dentro de tolerancia
- **Metadatos visualizados**:
  - Temperatura promedio, mínimo y máximo
  - Desviación promedio y máxima del setpoint
  - Distribución de lecturas (bajo/dentro del rango/alto)
  - Variabilidad de temperatura (%)
  - Setpoint y banda de tolerancia
- **Alertas**: Control deficiente de temperatura, desviación máxima excede tolerancia

#### **6. Response Index**
- **Gauge**: Muestra tiempo promedio de respuesta a anomalías
- **Metadatos visualizados**:
  - Rango de tiempos de respuesta (mínimo - máximo)
  - Distribución por velocidad (rápida/buena/lenta/muy lenta)
  - Tasa de respuestas por hora
  - Tiempos promedio por sensor
  - Variabilidad de respuesta (%)
- **Alertas**: Tiempo de respuesta deficiente, alto porcentaje de respuestas muy lentas

#### **7. Energy Efficiency**
- **Gauge**: Muestra eficiencia energética (kWh/L)
- **Metadatos visualizados**:
  - Valor esperado y tolerancia
  - Ratio actual vs esperado
  - Consumo total de energía (kWh)
  - Volumen total dispensado (L)
  - Indicador de estar dentro de tolerancia
- **Alertas**: Eficiencia fuera de tolerancia

#### **8. Thermal Variation**
- **Gauge**: Muestra variación térmica (desviación estándar)
- **Metadatos visualizados**:
  - Temperatura promedio, mínimo y máximo
  - Desviación del setpoint
  - Porcentaje dentro de tolerancia
  - Umbrales de clasificación
- **Alertas**: Variación excesiva

#### **9. Peak Flow Ratio**
- **Gauge**: Muestra ratio de flujo pico vs nominal
- **Metadatos visualizados**:
  - Flujo máximo, promedio y nominal
  - Porcentaje por encima del nominal
  - Indicadores de capacidad de tubería
  - Variabilidad del flujo (%)
- **Alertas**: Excede capacidad del tubo, por debajo del mínimo

### Características del Dashboard

#### **Visualización Dinámica**
- **Gauges con colores**: Cambian automáticamente según el estado de la métrica
- **Metadatos expandibles**: Información detallada visible al hacer hover o click
- **Actualización en tiempo real**: Datos se refrescan automáticamente
- **Responsive**: Se adapta a diferentes tamaños de pantalla

#### **Sistema de Estados y Colores**
- **🟢 Verde (Excellent)**: Rendimiento excepcional
- **🔵 Azul (Good)**: Rendimiento bueno
- **🟡 Amarillo (Acceptable)**: Rendimiento aceptable
- **🟠 Naranja (Poor)**: Rendimiento deficiente
- **🔴 Rojo (Critical)**: Rendimiento crítico

#### **Alertas Inteligentes**
El sistema muestra advertencias automáticas cuando:
- **Valores fuera de tolerancia** configurada
- **Tasas de anomalías altas** que indican problemas
- **Estabilidad deficiente** del sistema
- **Niveles bajos prolongados** de agua
- **Desbordamientos detectados** en el sistema
- **Tiempos de inactividad altos**
- **Utilización baja** del sistema
- **Déficits de rendimiento** significativos
- **Control deficiente** de temperatura
- **Desviaciones excesivas** del setpoint
- **Tiempos de respuesta deficientes**
- **Porcentajes altos** de respuestas muy lentas

#### **Funcionalidades Avanzadas**
- **Filtros temporales**: Selección de rangos de tiempo para análisis
- **Filtros por sensor**: Análisis específico por tipo de sensor
- **Exportación de datos**: Posibilidad de exportar métricas
- **Histórico de alertas**: Registro de eventos y anomalías
- **Configuración de umbrales**: Personalización de límites de alerta

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

## 📊 Detalle de KPIs

| Categoría            | KPI Sugerido                                       | Unidad / Método de Medición                   | Endpoint                          |
| -------------------- | -------------------------------------------------- | --------------------------------------------- | --------------------------------- |
| **Disponibilidad**   | % de tiempo operativo                              | (Tiempo operativo / Total disponible) × 100   | `/metrics/availability`           |
| **Energía**          | Consumo por litro dispensado                       | kWh / L                                       | `/metrics/energy_efficiency`      |
| **Mantenimiento**    | Tiempo medio entre fallas (MTBF)                   | Promedio de horas entre interrupciones        | `/metrics/mtbf`                   |
| **Calidad**          | % de servicios con temperatura y volumen correctos | (Servicios correctos / Total servicios) × 100 | `/metrics/quality_full`           |
| **Tiempo de Respuesta** | Promedio de espera entre selección y dispensado    | Segundos                                      | `/metrics/response_time`          |
| **Fallos**           | Número de fallos por semana                        | Conteo automático de errores                  | `/metrics/failures_count`         |
| **Uso**              | Promedio de servicios por franja horaria           | Servicios/hora (segmentado por turno)         | `/metrics/usage_rate`             |
| **Estabilidad**      | Tiempo medio entre anomalías adaptativas           | Minutos entre eventos anómalos                | `/metrics/mtba`                   |
| **Reactividad**      | Tiempo de respuesta a anomalías                    | Minutos de recuperación                       | `/metrics/response_index`         |
| **Nivel de Agua**    | % tiempo con nivel aceptable                       | (Tiempo aceptable / Total) × 100              | `/metrics/level_uptime`           |

---

## ⚙️ Componentes del OEE Adaptados

| Componente     | Descripción                                                                | Fórmula                                            | Endpoint                |
| -------------- | -------------------------------------------------------------------------- | -------------------------------------------------- | ----------------------- |
| **Disponibilidad** | Tiempo que el equipo estuvo operativo respecto al tiempo total disponible  | (Tiempo operativo / Tiempo total disponible) × 100 | `/metrics/availability` |
| **Rendimiento**    | Relación entre el volumen real dispensado y el volumen esperado            | (Volumen real dispensado / Volumen esperado) × 100 | `/metrics/performance`  |
| **Calidad**        | Porcentaje de servicios correctamente ejecutados (temp. y flujo adecuados) | (Servicios correctos / Total servicios) × 100      | `/metrics/quality_full` |

---

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
npm install react-router-dom recharts react-bootstrap bootstrap
```
En `src/index.js`, agrega:
```js
import 'bootstrap/dist/css/bootstrap.min.css';
```

```bash
npm start
```
Abre http://localhost:3000.

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

## 📈 Estado Actual del Proyecto

### **✅ Funcionalidades Completadas**
- ✅ Simulación de sensores IoT (temperatura, flujo, nivel, potencia)
- ✅ Detección de anomalías estáticas y adaptativas
- ✅ Cálculo de métricas OEE adaptadas con metadatos enriquecidos
- ✅ Dashboard interactivo con visualizaciones dinámicas
- ✅ API REST completa con documentación Swagger
- ✅ Sistema de alertas inteligentes y notificaciones
- ✅ Clasificación de estados cualitativos (excellent/good/acceptable/poor)
- ✅ Filtros temporales y por sensor
- ✅ Visualización de metadatos detallados para cada métrica

### **🔧 Características Técnicas**
- **Backend**: FastAPI con SQLite y detección de anomalías adaptativa
- **Frontend**: React con gauges dinámicos y sistema de colores
- **Métricas**: 15 endpoints con análisis estadístico completo
- **Alertas**: Sistema automático de notificaciones
- **Documentación**: README completo y CHANGELOG detallado

### **📊 Métricas Disponibles**
- **Disponibilidad**: Análisis de tiempo operativo y utilización
- **Rendimiento**: Comparación real vs esperado con eficiencia
- **Calidad**: Control de temperatura y estabilidad térmica
- **Energía**: Eficiencia energética y consumo no productivo
- **Mantenimiento**: MTBF, MTBA y análisis de fallas
- **Reactividad**: Tiempos de respuesta y recuperación
- **Nivel**: Monitoreo de disponibilidad de agua

Feliz monitoreo! 🚰📊

---

## Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo LICENSE para más detalles.
