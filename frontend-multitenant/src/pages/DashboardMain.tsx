import React from 'react';
import { useTenant } from '../contexts/TenantContext';
import DashboardTemporal from './dashboards/DashboardTemporal';
import LoadingSpinner from '../components/LoadingSpinner';
import '../styles/dashboards.css';

/**
 * 🏠 DASHBOARD PRINCIPAL - PACKFY CUBA
 *
 * Dashboard dinámico que renderiza el componente correcto según el rol del usuario:
 * - Dueño: Métricas de empresa, gestión global
 * - Operador Miami/Cuba: Gestión de operaciones específicas
 * - Remitente: Mis envíos, crear nuevos
 * - Destinatario: Paquetes recibidos, tracking
 */

const DashboardMain: React.FC = () => {
  const { perfilActual, empresaActual, isLoading } = useTenant();

  // Mostrar loading mientras se cargan los datos del tenant
  if (isLoading) {
    return (
      <div className="dashboard-loading">
        <LoadingSpinner />
        <p>Cargando información de la empresa...</p>
      </div>
    );
  }

  // Si no hay perfil, mostrar mensaje de error
  if (!perfilActual) {
    return (
      <div className="dashboard-error">
        <h2>⚠️ Error de configuración</h2>
        <p>No se pudo determinar tu rol en la empresa.</p>
        <p>Por favor, contacta al administrador.</p>
      </div>
    );
  }

  // Si no hay empresa, mostrar mensaje de error
  if (!empresaActual) {
    return (
      <div className="dashboard-error">
        <h2>⚠️ Sin empresa asignada</h2>
        <p>No tienes una empresa asignada.</p>
        <p>Por favor, contacta al administrador.</p>
      </div>
    );
  }

  // Renderizar dashboard según el rol del usuario
  const renderDashboardPorRol = () => {
    if (!empresaActual || !perfilActual) {
      return (
        <div className="dashboard-error">
          <h2>⚠️ Información Faltante</h2>
          <p>No se pudo cargar la información de empresa o perfil.</p>
        </div>
      );
    }

    // Por ahora usamos el dashboard temporal para todos los roles
    return <DashboardTemporal empresa={empresaActual} perfil={perfilActual} />;
  };  return (
    <div className="dashboard-main">
      {/* Header común */}
      <div className="dashboard-header">
        <div className="dashboard-empresa-info">
          <h1>📊 Dashboard - {empresaActual.name}</h1>
          <p className="dashboard-rol-badge">
            {perfilActual.rol === 'dueno' ? '👑 Dueño' :
             perfilActual.rol === 'operador_miami' ? '🌴 Operador Miami' :
             perfilActual.rol === 'operador_cuba' ? '🏝️ Operador Cuba' :
             perfilActual.rol === 'remitente' ? '📤 Remitente' :
             perfilActual.rol === 'destinatario' ? '📥 Destinatario' :
             perfilActual.rol}
          </p>
        </div>
      </div>

      {/* Dashboard específico por rol */}
      {renderDashboardPorRol()}
    </div>
  );
};

export default DashboardMain;
