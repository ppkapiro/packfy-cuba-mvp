import React from 'react';
import { Link } from 'react-router-dom';
import { Package, Users, Settings, BarChart3 } from 'lucide-react';
import { Empresa, PerfilUsuario } from '../../types';

interface DashboardTemporalProps {
  empresa: Empresa;
  perfil: PerfilUsuario;
}

const DashboardTemporal: React.FC<DashboardTemporalProps> = ({ empresa, perfil }) => {
  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>📊 Panel de Control</h1>
        <p>Dashboard para <strong>{perfil.rol}</strong> en <strong>{empresa.name}</strong></p>
      </div>

      <div className="dashboard-stats-grid">
        <div className="stat-card">
          <div className="stat-icon">
            <Package />
          </div>
          <div className="stat-content">
            <h3>Envíos</h3>
            <p className="stat-number">-</p>
            <small>Próximamente</small>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Users />
          </div>
          <div className="stat-content">
            <h3>Usuarios</h3>
            <p className="stat-number">-</p>
            <small>Próximamente</small>
          </div>
        </div>
      </div>

      <div className="dashboard-actions">
        <h3>Acciones Disponibles</h3>
        <div className="action-grid">
          <Link to="/envios" className="action-card">
            <Package />
            <span>Gestionar Envíos</span>
            <small>Ver lista de envíos</small>
          </Link>

          <Link to="/nuevo-envio" className="action-card primary">
            <Package />
            <span>Nuevo Envío</span>
            <small>Crear envío</small>
          </Link>

          {(perfil.rol === 'dueno' || perfil.rol === 'operador_miami' || perfil.rol === 'operador_cuba') && (
            <>
              <Link to="/users" className="action-card">
                <Users />
                <span>Usuarios</span>
                <small>Gestionar usuarios</small>
              </Link>

              <Link to="/reports" className="action-card">
                <BarChart3 />
                <span>Reportes</span>
                <small>Ver reportes</small>
              </Link>

              <Link to="/settings" className="action-card">
                <Settings />
                <span>Configuración</span>
                <small>Ajustes del sistema</small>
              </Link>
            </>
          )}
        </div>
      </div>

      <div className="dashboard-context">
        <h3>Información de Sesión</h3>
        <div className="context-info">
          <p><strong>Empresa:</strong> {empresa.name}</p>
          <p><strong>Rol:</strong> {perfil.rol}</p>
          <p><strong>ID Usuario:</strong> {perfil.id}</p>
        </div>
      </div>
    </div>
  );
};

export default DashboardTemporal;
