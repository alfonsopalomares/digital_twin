# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd
from typing import List, Dict

class LocalStorage:
    """
    Stores sensor data locally in a SQLite database.
    """
    def __init__(self, db_path: str = 'sensor_data.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor TEXT,
                timestamp TEXT,
                value REAL
            )
        ''')
        self.conn.commit()

    def save_batch(self, batch: List[Dict]):
        """
        Guarda un lote de lecturas de sensores en la base de datos.
        :param batch: lista de dicts con keys 'sensor','timestamp','value'
        """
        c = self.conn.cursor()
        # Convertir y ejecutar inserciones
        records = [
            (r['sensor'], r['timestamp'], r['value'])
            for r in batch
        ]
        c.executemany(
            'INSERT INTO sensor_data (sensor, timestamp, value) VALUES (?, ?, ?)',
            records
        )
        self.conn.commit()

    def insert_dataframe(self, df: pd.DataFrame):
        """
        Inserta un DataFrame completo en la base de datos.
        """
        records = df.to_dict(orient='records')
        c = self.conn.cursor()
        c.executemany(
            'INSERT INTO sensor_data (sensor, timestamp, value) VALUES (?, ?, ?)',
            [(r['sensor'], r['timestamp'], r['value']) for r in records]
        )
        self.conn.commit()

    def fetch_all(self) -> List[Dict]:
        c = self.conn.cursor()
        c.execute('SELECT sensor, timestamp, value FROM sensor_data ORDER BY timestamp DESC')
        rows = c.fetchall()
        return [{'sensor': r[0], 'timestamp': r[1], 'value': r[2]} for r in rows]

    def fetch_latest(self) -> Dict:
        c = self.conn.cursor()
        c.execute('''
            SELECT sensor, timestamp, value
            FROM sensor_data
            ORDER BY datetime(timestamp) DESC
            LIMIT 1
        ''')
        row = c.fetchone()
        return {'sensor': row[0], 'timestamp': row[1], 'value': row[2]} if row else None
    
    def clear_all(self) -> Dict:
        """
        Elimina todas las lecturas almacenadas.
        :return: dict con estado de la operación
        """
        c = self.conn.cursor()
        c.execute('DELETE FROM sensor_data')
        self.conn.commit()
        return {'status': 'deleted'}