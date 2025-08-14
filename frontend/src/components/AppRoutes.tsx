import React, { Suspense, lazy } from 'react';
import { Routes, Route } from 'react-router-dom';
import LoadingSpinner from './LoadingSpinner';

// Lazy loading de componentes para code splitting
const Dashboard = lazy(() => import('../pages/Dashboard'));
const EnviosList = lazy(() => import('../pages/EnviosList'));
const EnvioDetail = lazy(() => import('../pages/EnvioDetail'));
const NuevoEnvio = lazy(() => import('../pages/NuevoEnvio'));
const Login = lazy(() => import('../pages/Login'));
const Register = lazy(() => import('../pages/Register'));

// Wrapper con Suspense para mejor UX
const LazyRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <Suspense fallback={<LoadingSpinner message="Cargando página..." />}>
    {children}
  </Suspense>
);

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <LazyRoute>
            <Dashboard />
          </LazyRoute>
        }
      />
      <Route
        path="/dashboard"
        element={
          <LazyRoute>
            <Dashboard />
          </LazyRoute>
        }
      />
      <Route
        path="/envios"
        element={
          <LazyRoute>
            <EnviosList />
          </LazyRoute>
        }
      />
      <Route
        path="/envios/:id"
        element={
          <LazyRoute>
            <EnvioDetail />
          </LazyRoute>
        }
      />
      <Route
        path="/envios/nuevo"
        element={
          <LazyRoute>
            <NuevoEnvio />
          </LazyRoute>
        }
      />
      <Route
        path="/login"
        element={
          <LazyRoute>
            <Login />
          </LazyRoute>
        }
      />
      <Route
        path="/register"
        element={
          <LazyRoute>
            <Register />
          </LazyRoute>
        }
      />
    </Routes>
  );
};

export default AppRoutes;
