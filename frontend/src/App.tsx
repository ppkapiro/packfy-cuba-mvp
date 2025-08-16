import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout';  // Layout clásico que funciona
import PublicHeader from './components/PublicHeader';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import ShipmentDetail from './pages/ShipmentDetail';
import PublicTrackingPage from './pages/PublicTrackingPage';
import DiagnosticPage from './pages/DiagnosticPage';
import SimpleAdvancedPage from './pages/SimpleAdvancedPage';
import PremiumFormPage from './pages/PremiumFormPage';
import GestionUnificada from './pages/GestionUnificada';
import EditarEnvio from './pages/EditarEnvio';
import PWAInstallPrompt from './components/PWAInstallPrompt';
import NetworkStatusBanner from './components/NetworkStatusBanner';
import ModeSelector from './components/ModeSelector';
import ProtectedRoute from './components/ProtectedRoute';
import GlobalErrorBoundary from './components/GlobalErrorBoundary';
// 🇨🇺 CSS ya se importa en main.tsx - sin duplicados

// 🇨🇺 PACKFY CUBA - SISTEMA UNIFICADO v4.1 con Error Handling Avanzado

// ProtectedRoute se importa desde components/ProtectedRoute y usa AuthContext

// Wrapper para páginas públicas con header
function PublicPageWrapper({ children }: { children: React.ReactNode }) {
  return (
    <>
      <PublicHeader />
      {children}
    </>
  );
}

function App() {
  console.log('🇨🇺 Packfy Cuba v4.1 - Sistema Unificado con Error Handling iniciando...');

  return (
    <GlobalErrorBoundary>
      <AuthProvider>
        <div className="app-container">
          {/* Banner de estado de conexión */}
          <NetworkStatusBanner />

          <BrowserRouter>
            <div className="app-content">
              <Routes>
                {/* Rutas públicas */}
                <Route path="/login" element={<PublicPageWrapper><LoginPage /></PublicPageWrapper>} />
                <Route path="/diagnostico" element={<PublicPageWrapper><DiagnosticPage /></PublicPageWrapper>} />
                <Route path="/rastrear" element={<PublicPageWrapper><PublicTrackingPage /></PublicPageWrapper>} />

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
                <Route path="envios" element={<GestionUnificada />} />
                <Route path="envios/nuevo" element={<ModeSelector />} />
                <Route path="envios/simple" element={<SimpleAdvancedPage />} />
                <Route path="envios/premium" element={<PremiumFormPage />} />
                <Route path="envios/:id" element={<ShipmentDetail />} />
                <Route path="envios/:id/editar" element={<EditarEnvio />} />
              </Route>
            </Routes>
          </div>
        </BrowserRouter>

        {/* PWA Install Prompt */}
        <PWAInstallPrompt />
      </div>
    </AuthProvider>
    </GlobalErrorBoundary>
  );
}

export default App;
