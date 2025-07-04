import React from 'react';
import { MetricsDashboard } from './MetricsDashboard';

/**
 * MetricsPage: page component to host the MetricsDashboard
 */
export default function MetricsPage() {
  return (
    <div style={{ padding: '16px' }}>
      <h1>Metrics Dashboard</h1>
      <MetricsDashboard />
    </div>
  );
}
