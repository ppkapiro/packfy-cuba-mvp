import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout';  // Layout clásico que funciona
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import NewShipment from './pages/NewShipment';
import ShipmentDetail from './pages/ShipmentDetail';
import PublicTrackingPage from './pages/PublicTrackingPage';
import DiagnosticPage from './pages/DiagnosticPage';
import ModernModeSelector from './components/ModernModeSelector';
import SimpleAdvancedPage from './pages/SimpleAdvancedPage';
import PremiumFormPage from './pages/PremiumFormPage';
import GestionUnificada from './pages/GestionUnificada';
import EditarEnvio from './pages/EditarEnvio';
import PWAInstallPrompt from './components/PWAInstallPrompt';
import NetworkStatusBanner from './components/NetworkStatusBanner';
import AIPage from './pages/AIPage';

// 🇨🇺 PACKFY CUBA - SISTEMA UNIFICADO v3.3 (estilos cargados desde main.tsx)

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

              {/* Rutas protegidas con navegación clásica funcional */}
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
                <Route path="ai" element={<AIPage />} />
                <Route path="envios" element={<GestionUnificada />} />
                <Route path="envios/modo" element={<ModernModeSelector />} />
                <Route path="envios/nuevo" element={<NewShipment />} />
                <Route path="envios/:id" element={<ShipmentDetail />} />
                <Route path="envios/:id/editar" element={<EditarEnvio />} />
                <Route path="envios/simple" element={<SimpleAdvancedPage />} />
                <Route path="envios/premium" element={<PremiumFormPage />} />
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
