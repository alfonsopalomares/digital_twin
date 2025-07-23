import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import json

class DigitalTwinApiClient:
    """
    Cliente para consumir la API del gemelo digital del calentador de agua.
    Convierte las respuestas en pandas DataFrames para facilitar el análisis.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """Método auxiliar para hacer requests HTTP"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en request a {url}: {e}")
            return None
    
    def _post_request(self, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Any:
        """Método auxiliar para hacer POST requests"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.post(url, json=data, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en POST a {url}: {e}")
            return None

    # =============================================================================
    # MÉTODOS PARA LECTURAS (READINGS)
    # =============================================================================
    
    def get_readings_df(self) -> pd.DataFrame:
        """
        Obtiene todas las lecturas de sensores como DataFrame.
        
        Returns:
            DataFrame con columnas: sensor, timestamp, value
        """
        data = self._make_request('/readings/readings')
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
        
        return df
    
    def get_latest_reading_df(self) -> pd.DataFrame:
        """
        Obtiene la última lectura como DataFrame.
        
        Returns:
            DataFrame con la última lectura
        """
        data = self._make_request('/readings/readings/latest')
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame([data])
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
    
    def get_readings_by_sensor(self, sensor_name: str) -> pd.DataFrame:
        """
        Filtra las lecturas por sensor específico.
        
        Args:
            sensor_name: Nombre del sensor (ej: 'temperature', 'flow', 'level', 'power')
            
        Returns:
            DataFrame filtrado por sensor
        """
        df = self.get_readings_df()
        if df.empty:
            return df
        
        return df[df['sensor'] == sensor_name].reset_index(drop=True)

    # =============================================================================
    # MÉTODOS PARA MÉTRICAS
    # =============================================================================
    
    def get_all_metrics_df(self, start: Optional[str] = None, end: Optional[str] = None, 
                          users: int = 1, hours: int = 1) -> pd.DataFrame:
        """
        Obtiene todas las métricas disponibles en un solo DataFrame.
        
        Args:
            start: Timestamp ISO de inicio (opcional)
            end: Timestamp ISO de fin (opcional)
            users: Número de usuarios para métricas de performance
            hours: Número de horas para métricas de performance
            
        Returns:
            DataFrame con todas las métricas
        """
        metrics_data = []
        
        # Métricas que requieren start/end
        time_based_metrics = [
            'availability', 'quality', 'energy_efficiency', 
            'thermal_variation', 'level_uptime', 'nonproductive_consumption',
            'mtbf', 'quality_full', 'response_time', 'usage_rate'
        ]
        
        params = {}
        if start:
            params['start'] = start
        if end:
            params['end'] = end
        
        for metric in time_based_metrics:
            data = self._make_request(f'/metrics/{metric}', params)
            if data:
                for key, value in data.items():
                    metrics_data.append({
                        'metric': metric,
                        'sensor_or_key': key,
                        'value': value,
                        'timestamp': datetime.now().isoformat()
                    })
        
        # Métricas que requieren users
        user_based_metrics = ['performance', 'peak_flow_ratio']
        for metric in user_based_metrics:
            params_user = {'users': users}
            if metric == 'performance':
                params_user['hours'] = hours
            
            data = self._make_request(f'/metrics/{metric}', params_user)
            if data:
                for key, value in data.items():
                    metrics_data.append({
                        'metric': metric,
                        'sensor_or_key': key,
                        'value': value,
                        'timestamp': datetime.now().isoformat()
                    })
        
        # Métricas especiales
        special_metrics = [
            ('mtba', {'window': 60}),
            ('response_index', {'window': 60}),
            ('failures_count', {'weeks': 1})
        ]
        
        for metric, params_special in special_metrics:
            data = self._make_request(f'/metrics/{metric}', params_special)
            if data:
                for key, value in data.items():
                    metrics_data.append({
                        'metric': metric,
                        'sensor_or_key': key,
                        'value': value,
                        'timestamp': datetime.now().isoformat()
                    })
        
        df = pd.DataFrame(metrics_data)
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
    
    def get_specific_metric_df(self, metric_name: str, **kwargs) -> pd.DataFrame:
        """
        Obtiene una métrica específica como DataFrame.
        
        Args:
            metric_name: Nombre de la métrica
            **kwargs: Parámetros adicionales según la métrica
            
        Returns:
            DataFrame con la métrica solicitada
        """
        data = self._make_request(f'/metrics/{metric_name}', kwargs)
        if not data:
            return pd.DataFrame()
        
        metrics_data = []
        for key, value in data.items():
            metrics_data.append({
                'metric': metric_name,
                'sensor_or_key': key,
                'value': value,
                'timestamp': datetime.now().isoformat()
            })
        
        df = pd.DataFrame(metrics_data)
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df

    # =============================================================================
    # MÉTODOS PARA ANOMALÍAS
    # =============================================================================
    
    def get_static_anomalies_df(self) -> pd.DataFrame:
        """
        Obtiene anomalías estáticas como DataFrame.
        
        Returns:
            DataFrame con anomalías detectadas
        """
        data = self._make_request('/anomalies/static')
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
        
        return df
    
    def get_adaptive_anomalies_df(self, sensor: Optional[str] = None, 
                                 window: int = 60) -> pd.DataFrame:
        """
        Obtiene anomalías adaptativas como DataFrame.
        
        Args:
            sensor: Filtrar por sensor específico
            window: Tamaño de ventana para detección adaptativa
            
        Returns:
            DataFrame con anomalías adaptativas
        """
        params = {'window': window}
        if sensor:
            params['sensor'] = sensor
        
        data = self._make_request('/anomalies/adaptive', params)
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        if not df.empty and 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
        
        return df
    
    def get_classified_anomalies_df(self, sensor: Optional[str] = None, 
                                   window: int = 60) -> pd.DataFrame:
        """
        Obtiene anomalías clasificadas como DataFrame.
        
        Args:
            sensor: Filtrar por sensor específico
            window: Tamaño de ventana para detección adaptativa
            
        Returns:
            DataFrame con anomalías clasificadas
        """
        params = {'window': window}
        if sensor:
            params['sensor'] = sensor
        
        data = self._make_request('/anomalies/classify', params)
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        if not df.empty and 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
        
        return df

    # =============================================================================
    # MÉTODOS PARA SIMULACIÓN
    # =============================================================================
    
    def simulate_usage(self, hours: int = 8, users: int = 10, 
                      sensor: Optional[str] = None, value: Optional[float] = None,
                      timestamp: Optional[str] = None) -> Dict:
        """
        Ejecuta simulación de uso del calentador.
        
        Args:
            hours: Duración de simulación en horas
            users: Número de usuarios activos
            sensor: Sensor específico a simular (opcional)
            value: Valor override para el sensor (opcional)
            timestamp: Timestamp ISO para la simulación (opcional)
            
        Returns:
            Respuesta de la simulación
        """
        params = {'hours': hours, 'users': users}
        if sensor:
            params['sensor'] = sensor
        if value is not None:
            params['value'] = value
        if timestamp:
            params['timestamp'] = timestamp
        
        return self._post_request('/simulate/simulate', params=params)
    
    def simulate_scenarios_df(self, scenarios: List[Dict], 
                             duration_hours: int = 1) -> pd.DataFrame:
        """
        Ejecuta simulaciones de múltiples escenarios.
        
        Args:
            scenarios: Lista de configuraciones de escenario
            duration_hours: Duración de cada escenario en horas
            
        Returns:
            DataFrame con resultados de los escenarios
        """
        data = self._post_request('/simulate/simulate_scenarios', 
                                 data=scenarios, 
                                 params={'duration_hours': duration_hours})
        
        if not data:
            return pd.DataFrame()
        
        # Aplanar los datos de configuración para el DataFrame
        flattened_data = []
        for result in data:
            row = {
                'total_energy_kWh': result['total_energy_kWh'],
                'avg_temperature': result['avg_temperature'],
                'duration_hours': duration_hours
            }
            # Agregar campos de configuración
            config = result.get('config', {})
            for key, value in config.items():
                row[f'config_{key}'] = value
            
            flattened_data.append(row)
        
        return pd.DataFrame(flattened_data)

    # =============================================================================
    # MÉTODOS AUXILIARES Y DE ANÁLISIS
    # =============================================================================
    
    def get_sensor_summary_df(self) -> pd.DataFrame:
        """
        Obtiene un resumen estadístico de todos los sensores.
        
        Returns:
            DataFrame con estadísticas por sensor
        """
        df = self.get_readings_df()
        if df.empty:
            return pd.DataFrame()
        
        summary = df.groupby('sensor')['value'].agg([
            'count', 'mean', 'std', 'min', 'max', 'median'
        ]).reset_index()
        
        # Agregar información temporal
        time_stats = df.groupby('sensor')['timestamp'].agg([
            ('first_reading', 'min'),
            ('last_reading', 'max')
        ]).reset_index()
        
        summary = summary.merge(time_stats, on='sensor')
        return summary
    
    def get_time_series_df(self, sensor: str, 
                          start: Optional[str] = None, 
                          end: Optional[str] = None) -> pd.DataFrame:
        """
        Obtiene serie temporal de un sensor específico.
        
        Args:
            sensor: Nombre del sensor
            start: Fecha de inicio (formato ISO)
            end: Fecha de fin (formato ISO)
            
        Returns:
            DataFrame de serie temporal
        """
        df = self.get_readings_by_sensor(sensor)
        if df.empty:
            return df
        
        if start:
            df = df[df['timestamp'] >= pd.to_datetime(start)]
        if end:
            df = df[df['timestamp'] <= pd.to_datetime(end)]
        
        return df.set_index('timestamp')
    
    def delete_all_readings(self) -> bool:
        """
        Elimina todas las lecturas almacenadas.
        
        Returns:
            True si fue exitoso
        """
        try:
            response = self.session.delete(f"{self.base_url}/readings/readings")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error eliminando lecturas: {e}")
            return False


# =============================================================================
# CONEXION
# =============================================================================

    def is_online(self) -> bool:
        """
        Verifica si hay conección
        
        Returns:
            si está o no disponible
        """
        # url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(self.base_url)
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            return False

# =============================================================================
# EJEMPLO DE USO
# =============================================================================

def example_usage():
    """Ejemplo de cómo usar el cliente"""
    
    # Inicializar cliente
    client = DigitalTwinApiClient("http://localhost:8000")
    
    # Obtener todas las lecturas
    readings_df = client.get_readings_df()
    print("Lecturas obtenidas:", len(readings_df))
    
    # Obtener métricas
    metrics_df = client.get_all_metrics_df(users=5, hours=2)
    print("Métricas obtenidas:", len(metrics_df))
    
    # Obtener anomalías
    anomalies_df = client.get_static_anomalies_df()
    print("Anomalías detectadas:", len(anomalies_df))
    
    # Simular uso
    simulation_result = client.simulate_usage(hours=2, users=5)
    print("Simulación completada")
    
    # Obtener resumen de sensores
    summary_df = client.get_sensor_summary_df()
    print("Resumen de sensores:")
    print(summary_df)

if __name__ == "__main__":
    example_usage()
