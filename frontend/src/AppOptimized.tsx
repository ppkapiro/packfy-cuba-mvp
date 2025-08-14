// 🇨🇺 PACKFY CUBA - App Optimizada con Code Splitting v4.0
// Sistema de carga lazy y optimizaciones de performance

import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from 'react-router-dom'
import { Suspense, lazy, useEffect } from 'react'
import { AuthProvider } from './contexts/AuthContext'
import ErrorBoundary from './components/ErrorBoundary'
import LoadingSpinner from './components/LoadingSpinner'
import NetworkStatusBanner from './components/NetworkStatusBanner'
import PWAInstallPrompt from './components/PWAInstallPrompt'

// 🚀 LAZY LOADING - Componentes cargados bajo demanda
const Layout = lazy(() => import('./components/Layout'))
const LoginPage = lazy(() => import('./pages/LoginPage'))
const Dashboard = lazy(() => import('./pages/Dashboard'))
const NewShipment = lazy(() => import('./pages/NewShipment'))
const ShipmentDetail = lazy(() => import('./pages/ShipmentDetail'))
const PublicTrackingPage = lazy(() => import('./pages/PublicTrackingPage'))
const DiagnosticPage = lazy(() => import('./pages/DiagnosticPage'))
const ModernModeSelector = lazy(() => import('./components/ModernModeSelector'))
const SimpleAdvancedPage = lazy(() => import('./pages/SimpleAdvancedPage'))
const PremiumFormPage = lazy(() => import('./pages/PremiumFormPage'))
const GestionUnificada = lazy(() => import('./pages/GestionUnificada'))
const EditarEnvio = lazy(() => import('./pages/EditarEnvio'))

// 📊 PRELOADING - Componentes críticos precargados
const preloadCriticalComponents = () => {
  // Precargar componentes que se usan frecuentemente
  import('./pages/Dashboard')
  import('./pages/NewShipment')
  import('./components/Layout')
}

// 🔐 Componente de rutas protegidas optimizado
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const token = localStorage.getItem('token') || localStorage.getItem('packfy_tokens')

  if (!token) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

// 🎨 Componente de carga personalizado
function AppLoadingFallback() {
  return (
    <div className="app-loading">
      <div className="loading-container">
        <LoadingSpinner />
        <p className="loading-text">Cargando Packfy Cuba...</p>
      </div>
    </div>
  )
}

// 🚨 Componente de error personalizado
function AppErrorFallback({ error, resetError }: { error: Error; resetError: () => void }) {
  return (
    <div className="error-container">
      <h2>¡Oops! Algo salió mal</h2>
      <p>Error: {error.message}</p>
      <button onClick={resetError} className="btn btn-primary">
        Intentar de nuevo
      </button>
    </div>
  )
}

function OptimizedApp() {
  useEffect(() => {
    // Precargar componentes críticos después del primer render
    const timer = setTimeout(preloadCriticalComponents, 1000)

    // Optimizar performance
    if ('requestIdleCallback' in window) {
      requestIdleCallback(() => {
        // Operaciones de baja prioridad
        console.log('🚀 App inicializada con optimizaciones')
      })
    }

    return () => clearTimeout(timer)
  }, [])

  return (
    <ErrorBoundary fallback={AppErrorFallback}>
      <AuthProvider>
        <BrowserRouter>
          {/* 📱 Componentes de PWA y estado */}
          <NetworkStatusBanner />
          <PWAInstallPrompt />

          <Suspense fallback={<AppLoadingFallback />}>
            <Routes>
              {/* 🌐 Rutas públicas */}
              <Route path="/login" element={<LoginPage />} />
              <Route path="/tracking" element={<PublicTrackingPage />} />
              <Route path="/diagnostico" element={<DiagnosticPage />} />

              {/* 🔐 Rutas protegidas */}
              <Route path="/" element={
                <ProtectedRoute>
                  <Layout />
                </ProtectedRoute>
              }>
                <Route index element={<Navigate to="/dashboard" replace />} />
                <Route path="dashboard" element={<Dashboard />} />
                <Route path="selector-modo" element={<ModernModeSelector />} />
                <Route path="nuevo-envio" element={<NewShipment />} />
                <Route path="envio/:id" element={<ShipmentDetail />} />
                <Route path="editar-envio/:id" element={<EditarEnvio />} />

                {/* 📋 Páginas de formularios */}
                <Route path="simple-avanzado" element={<SimpleAdvancedPage />} />
                <Route path="premium" element={<PremiumFormPage />} />
                <Route path="gestion-unificada" element={<GestionUnificada />} />
              </Route>

              {/* 🚫 Ruta 404 */}
              <Route path="*" element={
                <div className="not-found">
                  <h2>Página no encontrada</h2>
                  <Navigate to="/dashboard" replace />
                </div>
              } />
            </Routes>
          </Suspense>
        </BrowserRouter>
      </AuthProvider>
    </ErrorBoundary>
  )
}

export default OptimizedApp
