import React from 'react';
import AnomaliesDashboard from './AnomaliesDashboard';

/**
 * AnomaliesPage: página para visualizar anomalías detectadas.
 */
export default function AnomaliesPage() {
  return (
    <div style={{ padding: 16 }}>
      <h1>Anomalías</h1>
      <AnomaliesDashboard />
    </div>
  );
}