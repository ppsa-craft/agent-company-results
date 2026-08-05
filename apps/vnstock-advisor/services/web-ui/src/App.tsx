import { useState, useEffect } from 'react';
import { HealthCheckSchema, type HealthCheck } from '@vnstock/shared-typescript';

function App() {
  const [health, setHealth] = useState<HealthCheck | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/api/health')
      .then((res) => res.json())
      .then((data) => {
        const parsed = HealthCheckSchema.safeParse(data);
        if (parsed.success) {
          setHealth(parsed.data);
        } else {
          setError('Invalid health response');
        }
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!health) return <div>No health data</div>;

  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui' }}>
      <h1>vnstock Advisor</h1>
      <div style={{ marginTop: '1rem', padding: '1rem', border: '1px solid #ccc', borderRadius: '4px' }}>
        <h2>Service Health</h2>
        <pre>{JSON.stringify(health, null, 2)}</pre>
      </div>
    </div>
  );
}

export default App;