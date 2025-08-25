import React from 'react';
import { useLocation } from 'react-router-dom';
import AdminDashboard from '../../pages/AdminDashboard';
import GestionEnvios from '../../pages/GestionEnvios';
import SimpleAdvancedPage from '../../pages/SimpleAdvancedPage';
import ModernAdvancedPage from '../../pages/ModernAdvancedPage';
import GestionUsuarios from './GestionUsuarios';
import ReportesAdmin from './ReportesAdmin';
import ConfiguracionAdmin from './ConfiguracionAdmin';

const AdminRouter: React.FC = () => {
  const location = useLocation();
  const pathname = location.pathname;

  console.log('AdminRouter: Ruta actual:', pathname);

  // Determinar qué componente mostrar según la ruta
  if (pathname.startsWith('/admin/envios/simple')) {
    console.log('AdminRouter: Mostrando SimpleAdvancedPage para admin');
    return <SimpleAdvancedPage />;
  }

  if (pathname.startsWith('/admin/envios/premium')) {
    console.log('AdminRouter: Mostrando ModernAdvancedPage para admin');
    return <ModernAdvancedPage />;
  }

  if (pathname.startsWith('/admin/envios')) {
    console.log('AdminRouter: Mostrando GestionEnvios para admin');
    return <GestionEnvios />;
  }

  if (pathname.startsWith('/admin/usuarios')) {
    console.log('AdminRouter: Mostrando GestionUsuarios para admin');
    return <GestionUsuarios />;
  }

  if (pathname.startsWith('/admin/reportes')) {
    console.log('AdminRouter: Mostrando ReportesAdmin para admin');
    return <ReportesAdmin />;
  }

  if (pathname.startsWith('/admin/configuracion')) {
    console.log('AdminRouter: Mostrando ConfiguracionAdmin para admin');
    return <ConfiguracionAdmin />;
  }

  // Por defecto, mostrar el dashboard ejecutivo
  console.log('AdminRouter: Mostrando dashboard ejecutivo por defecto');
  return <AdminDashboard />;
};

export default AdminRouter;
