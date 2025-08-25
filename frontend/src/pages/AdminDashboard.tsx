import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Users, Package, TrendingUp, BarChart3,
  DollarSign, Clock, Settings,
  UserPlus, FileText, Eye, ExternalLink
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useTenant } from '../contexts/TenantContext';
import { api } from '../services/api';
import '../styles/admin-dashboard.css';

interface MetricasEjecutivas {
  usuarios: {
    total: number;
    activos: number;
    por_rol: Record<string, number>;
  };
  envios: {
    total: number;
    este_mes: number;
    entregados: number;
    en_proceso: number;
    ingresos_estimados: number;
  };
  rendimiento: {
    tiempo_promedio_entrega: number;
    satisfaccion_cliente: number;
    eficiencia_operativa: number;
  };
}

const AdminDashboard: React.FC = () => {
  const { user } = useAuth();
  const { empresaActual } = useTenant();
  const [metricas, setMetricas] = useState<MetricasEjecutivas | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadMetricasEjecutivas();
  }, []);

  const loadMetricasEjecutivas = async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Simular carga de métricas (en el futuro, estas vendrán de endpoints específicos)
      const [enviosResponse] = await Promise.all([
        api.get('/envios/')
      ]);

      const envios = (enviosResponse.data as any)?.results || [];

      // Calcular métricas básicas
      const metricasCalculadas: MetricasEjecutivas = {
        usuarios: {
          total: 0, // Se cargaría desde endpoint de usuarios
          activos: 0,
          por_rol: {}
        },
        envios: {
          total: envios.length,
          este_mes: envios.filter((e: any) => {
            const fecha = new Date(e.fecha_creacion);
            const ahora = new Date();
            return fecha.getMonth() === ahora.getMonth() && fecha.getFullYear() === ahora.getFullYear();
          }).length,
          entregados: envios.filter((e: any) => e.estado_actual === 'entregado').length,
          en_proceso: envios.filter((e: any) => ['recibido', 'en_transito', 'en_reparto'].includes(e.estado_actual)).length,
          ingresos_estimados: envios.reduce((sum: number, e: any) => sum + (e.precio_estimado || 0), 0)
        },
        rendimiento: {
          tiempo_promedio_entrega: 3.5, // días (calculado)
          satisfaccion_cliente: 4.2, // sobre 5
          eficiencia_operativa: 85 // porcentaje
        }
      };

      setMetricas(metricasCalculadas);
    } catch (error) {
      console.error('Error cargando métricas:', error);
      setError('Error al cargar las métricas del dashboard');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="admin-dashboard loading">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Cargando dashboard ejecutivo...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="admin-dashboard error">
        <div className="error-container">
          <h2>Error al cargar dashboard</h2>
          <p>{error}</p>
          <button onClick={loadMetricasEjecutivas} className="retry-button">
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      {/* Header del Dashboard */}
      <div className="dashboard-header">
        <div className="header-content">
          <div className="header-info">
            <h1>Dashboard Ejecutivo</h1>
            <p>
              Bienvenido, {user?.nombre} {user?.apellidos} •
              Dueño de {empresaActual?.nombre}
            </p>
          </div>
          <div className="header-actions">
            <Link to="/admin/reportes" className="action-button">
              <BarChart3 size={18} />
              Ver Reportes
            </Link>
            <a
              href="/admin/"
              target="_blank"
              rel="noopener noreferrer"
              className="action-button secondary"
            >
              <ExternalLink size={18} />
              Admin Django
            </a>
          </div>
        </div>
      </div>

      {/* Métricas Principales */}
      <div className="metrics-grid">
        {/* Métrica de Envíos */}
        <div className="metric-card envios">
          <div className="metric-header">
            <Package className="metric-icon" />
            <h3>Gestión de Envíos</h3>
          </div>
          <div className="metric-content">
            <div className="metric-main">
              <span className="metric-value">{metricas?.envios.total || 0}</span>
              <span className="metric-label">Total Envíos</span>
            </div>
            <div className="metric-details">
              <div className="detail-item">
                <span className="detail-value">{metricas?.envios.este_mes || 0}</span>
                <span className="detail-label">Este mes</span>
              </div>
              <div className="detail-item">
                <span className="detail-value">{metricas?.envios.entregados || 0}</span>
                <span className="detail-label">Entregados</span>
              </div>
              <div className="detail-item">
                <span className="detail-value">{metricas?.envios.en_proceso || 0}</span>
                <span className="detail-label">En proceso</span>
              </div>
            </div>
          </div>
          <div className="metric-actions">
            <Link to="/admin/envios" className="metric-link">
              <Eye size={16} />
              Ver todos
            </Link>
            <Link to="/admin/envios/simple" className="metric-link">
              <Package size={16} />
              Crear nuevo
            </Link>
          </div>
        </div>

        {/* Métrica de Usuarios */}
        <div className="metric-card usuarios">
          <div className="metric-header">
            <Users className="metric-icon" />
            <h3>Gestión de Usuarios</h3>
          </div>
          <div className="metric-content">
            <div className="metric-main">
              <span className="metric-value">{metricas?.usuarios.total || 0}</span>
              <span className="metric-label">Total Usuarios</span>
            </div>
            <div className="metric-details">
              <div className="detail-item">
                <span className="detail-value">{metricas?.usuarios.activos || 0}</span>
                <span className="detail-label">Activos</span>
              </div>
            </div>
          </div>
          <div className="metric-actions">
            <Link to="/admin/usuarios" className="metric-link">
              <Users size={16} />
              Ver usuarios
            </Link>
            <Link to="/admin/usuarios/nuevo" className="metric-link">
              <UserPlus size={16} />
              Agregar usuario
            </Link>
          </div>
        </div>

        {/* Métrica Financiera */}
        <div className="metric-card financiera">
          <div className="metric-header">
            <DollarSign className="metric-icon" />
            <h3>Rendimiento Financiero</h3>
          </div>
          <div className="metric-content">
            <div className="metric-main">
              <span className="metric-value">${metricas?.envios.ingresos_estimados || 0}</span>
              <span className="metric-label">Ingresos Estimados</span>
            </div>
            <div className="metric-details">
              <div className="detail-item">
                <span className="detail-value">{metricas?.rendimiento.eficiencia_operativa || 0}%</span>
                <span className="detail-label">Eficiencia</span>
              </div>
            </div>
          </div>
          <div className="metric-actions">
            <Link to="/admin/reportes" className="metric-link">
              <BarChart3 size={16} />
              Ver reportes
            </Link>
          </div>
        </div>

        {/* Métrica de Rendimiento */}
        <div className="metric-card rendimiento">
          <div className="metric-header">
            <TrendingUp className="metric-icon" />
            <h3>Indicadores de Rendimiento</h3>
          </div>
          <div className="metric-content">
            <div className="metric-main">
              <span className="metric-value">{metricas?.rendimiento.tiempo_promedio_entrega || 0}</span>
              <span className="metric-label">Días promedio entrega</span>
            </div>
            <div className="metric-details">
              <div className="detail-item">
                <span className="detail-value">{metricas?.rendimiento.satisfaccion_cliente || 0}/5</span>
                <span className="detail-label">Satisfacción</span>
              </div>
            </div>
          </div>
          <div className="metric-actions">
            <Link to="/admin/reportes" className="metric-link">
              <Clock size={16} />
              Ver detalles
            </Link>
          </div>
        </div>
      </div>

      {/* Acciones Rápidas */}
      <div className="quick-actions">
        <h2>Acciones Rápidas</h2>
        <div className="actions-grid">
          <Link to="/admin/usuarios/nuevo" className="quick-action">
            <UserPlus className="action-icon" />
            <span>Agregar Usuario</span>
          </Link>
          <Link to="/admin/envios/simple" className="quick-action">
            <Package className="action-icon" />
            <span>Crear Envío</span>
          </Link>
          <Link to="/admin/empresa" className="quick-action">
            <Settings className="action-icon" />
            <span>Configurar Empresa</span>
          </Link>
          <Link to="/admin/reportes" className="quick-action">
            <FileText className="action-icon" />
            <span>Generar Reporte</span>
          </Link>
          <a
            href="/admin/"
            target="_blank"
            rel="noopener noreferrer"
            className="quick-action"
          >
            <ExternalLink className="action-icon" />
            <span>Admin Django</span>
          </a>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
