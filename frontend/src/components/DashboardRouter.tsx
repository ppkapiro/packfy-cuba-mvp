import React from 'react';
import { useTenant } from '../contexts/TenantContext';
import AdminDashboard from '../pages/AdminDashboard';
import Dashboard from '../pages/Dashboard';

const DashboardRouter: React.FC = () => {
  const { perfilActual } = useTenant();

  console.log('DashboardRouter: perfilActual:', perfilActual);
  console.log('DashboardRouter: rol:', perfilActual?.rol);

  // Si el usuario es dueño, mostrar AdminDashboard
  if (perfilActual?.rol === 'dueno') {
    console.log('DashboardRouter: Renderizando AdminDashboard para dueño');
    return <AdminDashboard />;
  }

  // Para todos los demás roles, mostrar Dashboard normal
  console.log('DashboardRouter: Renderizando Dashboard estándar para rol:', perfilActual?.rol);
  return <Dashboard />;
};

export default DashboardRouter;
