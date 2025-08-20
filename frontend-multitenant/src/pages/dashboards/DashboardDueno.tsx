import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { TrendingUp, Users, Package, DollarSign, Eye, BarChart3, Settings } from 'lucide-react';
import { enviosAPI } from '../../services/api';
import { Empresa, PerfilUsuario } from '../../types';

interface DashboardDuenoProps {
  empresa: Empresa;
  perfil: PerfilUsuario;
}

interface EstadisticasEmpresa {
  total_envios: number;
  envios_mes_actual: number;
  ingresos_mes: number;
  envios_pendientes: number;
  envios_entregados: number;
  clientes_activos: number;
}

/**
 * 👑 DASHBOARD PARA DUEÑO DE EMPRESA
 *
 * Funcionalidades:
 * - Métricas generales de la empresa
 * - Gráficos de rendimiento
 * - Gestión de empleados
 * - Configuración de empresa
 * - Reportes financieros
 */

const DashboardDueno: React.FC<DashboardDuenoProps> = ({ empresa, perfil }) => {
  const [estadisticas, setEstadisticas] = useState<EstadisticasEmpresa>({
    total_envios: 0,
    envios_mes_actual: 0,
    ingresos_mes: 0,
    envios_pendientes: 0,
    envios_entregados: 0,
    clientes_activos: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    cargarEstadisticas();
  }, [empresa.slug]);

  const cargarEstadisticas = async () => {
    try {
      setLoading(true);

      // Cargar estadísticas de envíos
      const response = await enviosAPI.getAll({ page_size: 1 });
      const totalEnvios = response.data.count || 0;

      // Simular otras estadísticas (en producción estas vendrían del backend)
      setEstadisticas({
        total_envios: totalEnvios,
        envios_mes_actual: Math.floor(totalEnvios * 0.3),
        ingresos_mes: totalEnvios * 25, // $25 promedio por envío
        envios_pendientes: Math.floor(totalEnvios * 0.15),
        envios_entregados: Math.floor(totalEnvios * 0.7),
        clientes_activos: Math.floor(totalEnvios * 0.6)
      });

    } catch (err: any) {
      console.error('Error cargando estadísticas:', err);
      setError('Error al cargar las estadísticas de la empresa');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-dueno-loading">
        <div className="loading-spinner"></div>
        <p>Cargando métricas de empresa...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <p>❌ {error}</p>
        <button onClick={cargarEstadisticas} className="btn-retry">
          Reintentar
        </button>
      </div>
    );
  }

  return (
    <div className="dashboard-dueno">
      {/* Bienvenida personalizada */}
      <div className="dashboard-welcome">
        <h2>👑 Bienvenido, Dueño de {empresa.name}</h2>
        <p>Aquí tienes un resumen completo del estado de tu empresa.</p>
      </div>

      {/* Grid de métricas principales */}
      <div className="dashboard-metrics-grid">
        <div className="metric-card primary">
          <div className="metric-icon">
            <Package size={24} />
          </div>
          <div className="metric-content">
            <h3>Total Envíos</h3>
            <p className="metric-number">{estadisticas.total_envios}</p>
            <span className="metric-label">Histórico</span>
          </div>
        </div>

        <div className="metric-card success">
          <div className="metric-icon">
            <TrendingUp size={24} />
          </div>
          <div className="metric-content">
            <h3>Este Mes</h3>
            <p className="metric-number">{estadisticas.envios_mes_actual}</p>
            <span className="metric-label">Envíos nuevos</span>
          </div>
        </div>

        <div className="metric-card warning">
          <div className="metric-icon">
            <DollarSign size={24} />
          </div>
          <div className="metric-content">
            <h3>Ingresos Mes</h3>
            <p className="metric-number">${estadisticas.ingresos_mes}</p>
            <span className="metric-label">Estimado</span>
          </div>
        </div>

        <div className="metric-card info">
          <div className="metric-icon">
            <Users size={24} />
          </div>
          <div className="metric-content">
            <h3>Clientes Activos</h3>
            <p className="metric-number">{estadisticas.clientes_activos}</p>
            <span className="metric-label">Únicos</span>
          </div>
        </div>
      </div>

      {/* Estado de operaciones */}
      <div className="dashboard-operations">
        <h3>📊 Estado de Operaciones</h3>
        <div className="operations-grid">
          <div className="operation-item">
            <span className="operation-label">✅ Entregados</span>
            <span className="operation-value">{estadisticas.envios_entregados}</span>
            <div className="operation-bar">
              <div
                className="operation-progress delivered"
                style={{ width: `${(estadisticas.envios_entregados / estadisticas.total_envios) * 100}%` }}
              ></div>
            </div>
          </div>

          <div className="operation-item">
            <span className="operation-label">🚚 Pendientes</span>
            <span className="operation-value">{estadisticas.envios_pendientes}</span>
            <div className="operation-bar">
              <div
                className="operation-progress pending"
                style={{ width: `${(estadisticas.envios_pendientes / estadisticas.total_envios) * 100}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* Acciones rápidas para dueño */}
      <div className="dashboard-actions">
        <h3>🚀 Acciones Rápidas</h3>
        <div className="actions-grid">
          <Link to="/envios" className="action-card">
            <Eye size={20} />
            <span>Ver Todos los Envíos</span>
          </Link>

          <Link to="/reportes" className="action-card">
            <BarChart3 size={20} />
            <span>Reportes Detallados</span>
          </Link>

          <Link to="/configuracion" className="action-card">
            <Settings size={20} />
            <span>Configurar Empresa</span>
          </Link>

          <Link to="/envios/nuevo" className="action-card primary">
            <Package size={20} />
            <span>Crear Nuevo Envío</span>
          </Link>
        </div>
      </div>

      {/* Información adicional */}
      <div className="dashboard-info">
        <p><strong>Empresa:</strong> {empresa.name}</p>
        <p><strong>Tu rol:</strong> Dueño - Acceso completo</p>
        <p><strong>Última actualización:</strong> {new Date().toLocaleString()}</p>
      </div>
    </div>
  );
};

export default DashboardDueno;
