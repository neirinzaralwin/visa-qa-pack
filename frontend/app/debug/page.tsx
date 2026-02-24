'use client';

import { useState, useEffect } from 'react';

export default function DebugPage() {
  const [apiUrl, setApiUrl] = useState('');
  const [response, setResponse] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setApiUrl(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000');
  }, []);

  const testAPI = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/prompt`);
      const data = await res.json();
      setResponse(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      setResponse(null);
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">API Debug Page</h1>
      
      <div className="mb-4">
        <p><strong>API URL:</strong> {apiUrl}</p>
        <p><strong>Environment:</strong> {process.env.NODE_ENV}</p>
      </div>

      <button 
        onClick={testAPI}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Test API Connection
      </button>

      {error && (
        <div className="mt-4 p-4 bg-red-100 border border-red-300 rounded">
          <p className="text-red-700"><strong>Error:</strong> {error}</p>
        </div>
      )}

      {response && (
        <div className="mt-4 p-4 bg-green-100 border border-green-300 rounded">
          <p className="text-green-700"><strong>Success!</strong></p>
          <pre className="mt-2 text-sm">{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
