import { useState } from 'react';

const TestApiPage = () => {
  const [results, setResults] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const log = (message: string) => {
    console.log(message);
    setResults(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  const testAPI = async () => {
    setLoading(true);
    setResults([]);

    try {
      // Test 1: Health check
      log("🏥 Testing health check...");
      const healthResponse = await fetch('/api/health/');
      const healthData = await healthResponse.json();
      log(`✅ Health check: ${JSON.stringify(healthData)}`);

      // Test 2: Login sin tenant
      log("🔐 Testing login without tenant...");
      const loginResponse1 = await fetch('/api/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: 'superadmin@packfy.com',
          password: 'super123!'
        })
      });
      log(`❌ Login without tenant status: ${loginResponse1.status}`);
      const loginData1 = await loginResponse1.json();
      log(`❌ Login without tenant response: ${JSON.stringify(loginData1).substring(0, 200)}...`);

      // Test 3: Login con tenant
      log("🏢 Testing login with tenant...");
      const loginResponse2 = await fetch('/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Tenant-Slug': 'packfy-express'
        },
        body: JSON.stringify({
          email: 'superadmin@packfy.com',
          password: 'super123!'
        })
      });
      log(`✅ Login with tenant status: ${loginResponse2.status}`);
      const loginData2 = await loginResponse2.json();

      if (loginResponse2.ok && loginData2.access) {
        log(`🎉 Login successful! Token: ${loginData2.access.substring(0, 20)}...`);

        // Test 4: Usuario actual
        log("👤 Testing current user...");
        const userResponse = await fetch('/api/usuarios/me/', {
          headers: {
            'Authorization': `Bearer ${loginData2.access}`,
            'X-Tenant-Slug': 'packfy-express'
          }
        });
        log(`👤 Current user status: ${userResponse.status}`);
        const userData = await userResponse.json();
        log(`👤 Current user: ${JSON.stringify(userData).substring(0, 200)}...`);
      } else {
        log(`❌ Login failed: ${JSON.stringify(loginData2)}`);
      }

    } catch (error) {
      log(`💥 Error: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h1>🧪 Packfy API Test</h1>

      <button
        onClick={testAPI}
        disabled={loading}
        style={{
          padding: '10px 20px',
          fontSize: '16px',
          backgroundColor: loading ? '#ccc' : '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: loading ? 'not-allowed' : 'pointer'
        }}
      >
        {loading ? '⏳ Testing...' : '🚀 Run API Tests'}
      </button>

      <div style={{ marginTop: '20px' }}>
        <h3>📊 Results:</h3>
        <div style={{
          backgroundColor: '#f8f9fa',
          border: '1px solid #dee2e6',
          borderRadius: '5px',
          padding: '15px',
          maxHeight: '400px',
          overflowY: 'auto'
        }}>
          {results.length === 0 ? (
            <p style={{ color: '#6c757d' }}>Click "Run API Tests" to start testing...</p>
          ) : (
            results.map((result, index) => (
              <div key={index} style={{
                padding: '2px 0',
                borderBottom: index < results.length - 1 ? '1px solid #eee' : 'none',
                fontSize: '12px'
              }}>
                {result}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default TestApiPage;
