# Tests del Backend - Industria 4.0

Esta carpeta contiene los tests unitarios para el backend del sistema Industria 4.0.

## Estructura

```
tests/
├── __init__.py              # Hace de tests un paquete Python
├── conftest.py              # Configuración pytest y fixtures comunes
├── test_readings_endpoints.py    # Tests para endpoints de lecturas
├── test_simulate_endpoints.py    # Tests para endpoints de simulación
├── test_metrics_endpoints.py     # Tests para endpoints de métricas
├── test_simulator.py             # Tests para el simulador
├── test_storage.py               # Tests para el storage
└── README.md                     # Este archivo
```

## Ejecutar los Tests

### Ejecutar todos los tests:
```bash
pytest
```

### Ejecutar tests específicos:
```bash
# Tests de un archivo específico
pytest tests/test_readings_endpoints.py

# Tests de una clase específica
pytest tests/test_readings_endpoints.py::TestReadingsEndpoints

# Tests de un método específico
pytest tests/test_readings_endpoints.py::TestReadingsEndpoints::test_get_readings_empty
```

### Ejecutar tests con más detalle:
```bash
# Con más verbosidad
pytest -v

# Con cobertura de código
pytest --cov=.

# Con reporte HTML de cobertura
pytest --cov=. --cov-report=html
```

## Fixtures Disponibles

- `temp_db`: Crea una base de datos temporal para testing
- `storage`: Instancia de LocalStorage con base de datos temporal
- `sample_config`: Configuración de ejemplo para testing
- `sample_readings`: Lecturas de sensores de ejemplo para testing

## Cobertura de Tests

Los tests cubren:

### Endpoints de Readings
- ✅ `get_readings()` - Obtener todas las lecturas
- ✅ `get_latest_reading()` - Obtener la lectura más reciente
- ✅ `delete_readings()` - Borrar todas las lecturas

### Endpoints de Simulate
- ✅ `simulate_scenarios()` - Simulación de múltiples escenarios
- ✅ Configuraciones con diferentes parámetros
- ✅ Validación de resultados

### Endpoints de Metrics
- ✅ `get_availability()` - Disponibilidad del sistema
- ✅ `get_performance()` - Rendimiento vs esperado
- ✅ `get_quality()` - Calidad de temperatura
- ✅ `get_energy_efficiency()` - Eficiencia energética
- ✅ `get_thermal_variation()` - Variación térmica
- ✅ `get_peak_flow_ratio()` - Ratio de flujo máximo

### Simulator
- ✅ Inicialización con diferentes configuraciones
- ✅ Generación de frames de sensores
- ✅ Escalado con número de usuarios
- ✅ Rangos de valores válidos
- ✅ Métodos de ajuste de parámetros
- ✅ Simulación de escenarios

### Storage
- ✅ Guardado y recuperación de configuración
- ✅ Guardado y recuperación de lecturas
- ✅ Persistencia de datos
- ✅ Operaciones de limpieza
- ✅ Actualizaciones parciales de configuración

## Notas Importantes

1. **Base de Datos Temporal**: Los tests usan una base de datos temporal que se crea y destruye automáticamente para cada test.

2. **Aislamiento**: Cada test es independiente y no afecta a otros tests.

3. **Fixtures**: Los fixtures proporcionan datos de prueba consistentes y reutilizables.

4. **Constantes**: Los tests usan las constantes centralizadas desde `settings.py`.

## Agregar Nuevos Tests

Para agregar nuevos tests:

1. Crea un archivo `test_*.py` en la carpeta `tests/`
2. Define clases que hereden de `object` (no es necesario heredar de `unittest.TestCase`)
3. Define métodos que empiecen con `test_`
4. Usa los fixtures disponibles o crea nuevos en `conftest.py`
5. Ejecuta los tests para verificar que funcionan correctamente 