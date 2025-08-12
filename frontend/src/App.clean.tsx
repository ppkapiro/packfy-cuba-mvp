import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import NewShipment from './pages/NewShipment';
import ShipmentDetail from './pages/ShipmentDetail';
import TrackingPage from './pages/TrackingPage';
import PublicTrackingPage from './pages/PublicTrackingPage';
import DiagnosticPage from './pages/DiagnosticPage';
import EnvioModePage from './pages/EnvioModePage';
import SimpleAdvancedPage from './pages/SimpleAdvancedPage';
import ModernAdvancedPage from './pages/ModernAdvancedPage';
import PWAInstallPrompt from './components/PWAInstallPrompt';
import NetworkStatusBanner from './components/NetworkStatusBanner';

// 🇨🇺 PACKFY CUBA - SISTEMA UNIFICADO v3.0
import './styles/unified-system.css';

// Componente de rutas protegidas
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const token = localStorage.getItem('token');
  
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
}

function App() {
  console.log('🇨🇺 Packfy Cuba v3.0 - Sistema Unificado iniciando...');
  
  return (
    <AuthProvider>
      <div className="app-container">
        {/* Banner de estado de conexión */}
        <NetworkStatusBanner />
        
        <BrowserRouter>
          <div className="app-content">
            <Routes>
              {/* Rutas públicas */}
              <Route path="/login" element={<LoginPage />} />
              <Route path="/diagnostico" element={<DiagnosticPage />} />
              <Route path="/rastrear" element={<PublicTrackingPage />} />
              
              {/* Rutas protegidas */}
              <Route 
                path="/" 
                element={
                  <ProtectedRoute>
                    <Layout />
                  </ProtectedRoute>
                }
              >
                <Route index element={<Navigate to="/dashboard" />} />
                <Route path="dashboard" element={<Dashboard />} />
                <Route path="envios/nuevo" element={<NewShipment />} />
                <Route path="envios/:id" element={<ShipmentDetail />} />
                <Route path="envios" element={<EnvioModePage />} />
                <Route path="envios/simple" element={<SimpleAdvancedPage />} />
                <Route path="envios/premium" element={<ModernAdvancedPage />} />
                <Route path="envios/moderno" element={<ModernAdvancedPage />} />
                <Route path="rastreo" element={<TrackingPage />} />
              </Route>
            </Routes>
          </div>
        </BrowserRouter>

        {/* PWA Install Prompt */}
        <PWAInstallPrompt />
      </div>
    </AuthProvider>
  );
}

export default App;
