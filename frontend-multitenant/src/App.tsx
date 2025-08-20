import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { TenantProvider } from './contexts/TenantContext';
import Layout from './components/Layout';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import NewShipment from './pages/NewShipment';
import ShipmentDetail from './pages/ShipmentDetail';
import TrackingPageFixed from './pages/TrackingPageFixed';
import PublicTrackingPage from './pages/PublicTrackingPage';
import DiagnosticPage from './pages/DiagnosticPage';
import EnvioModePage from './pages/EnvioModePage';
import SimpleAdvancedPage from './pages/SimpleAdvancedPage';
import ModernAdvancedPage from './pages/ModernAdvancedPage';
import GestionEnvios from './pages/GestionEnvios';
import EditarEnvio from './pages/EditarEnvio';
// PWA Install Prompt deshabilitado para evitar pop-ups molestos
// import PWAInstallPrompt from './components/PWAInstallPrompt';
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
      <TenantProvider>
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
                <Route path="envios" element={<GestionEnvios />} />
                <Route path="envios/modo" element={<EnvioModePage />} />
                <Route path="gestion/gratuita" element={<GestionEnvios />} />
                <Route path="gestion/premium" element={<GestionEnvios />} />
                <Route path="envios/nuevo" element={<NewShipment />} />
                <Route path="envios/:id" element={<ShipmentDetail />} />
                <Route path="envios/:id/editar" element={<EditarEnvio />} />
                <Route path="envios/simple" element={<SimpleAdvancedPage />} />
                <Route path="envios/premium" element={<ModernAdvancedPage />} />
                <Route path="envios/moderno" element={<ModernAdvancedPage />} />
                <Route path="rastreo" element={<TrackingPageFixed />} />
              </Route>
            </Routes>
          </div>
        </BrowserRouter>

        {/* PWA Install Prompt - DESHABILITADO para evitar pop-ups molestos */}
        {/* <PWAInstallPrompt /> */}
      </div>
      </TenantProvider>
    </AuthProvider>
  );
}

export default App;
