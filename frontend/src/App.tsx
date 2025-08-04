import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Layout from './components/Layout';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import NewShipment from './pages/NewShipment';
import ShipmentDetail from './pages/ShipmentDetail';
import TrackingPage from './pages/TrackingPage';
import PublicTrackingPage from './pages/PublicTrackingPage';
import DiagnosticPage from './pages/DiagnosticPage';
import './App.css';

// Componente protegido que redirecciona a login si no hay autenticación
const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const { isAuthenticated, isLoading, token } = useAuth();
  
  if (isLoading) {
    console.log('ProtectedRoute: Cargando autenticación...');
    return <div className="loading-app">Cargando...</div>;
  }
  
  // Información adicional para depuración
  console.log('ProtectedRoute: Estado de autenticación:', isAuthenticated);
  console.log('ProtectedRoute: Token presente:', !!token);
  if (token) {
    console.log('ProtectedRoute: Longitud del token:', token.length);
    console.log('ProtectedRoute: Primeros 10 caracteres del token:', token.substring(0, 10) + '...');
  }
  
  if (!isAuthenticated) {
    console.log('ProtectedRoute: Usuario no autenticado, redirigiendo a login');
    return <Navigate to="/login" />;
  }
  
  console.log('ProtectedRoute: Usuario autenticado, renderizando contenido protegido');
  return children;
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>          <Route path="/login" element={<LoginPage />} />
          <Route path="/diagnostico" element={<DiagnosticPage />} />
          <Route path="/rastrear" element={<PublicTrackingPage />} />
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
            <Route path="seguimiento" element={<TrackingPage />} />
          </Route>
          
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;