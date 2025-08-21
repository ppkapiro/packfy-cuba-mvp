import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import '../../styles/reportes-admin.css';

interface ReporteData {
  envios: {
    total: number;
    entregados: number;
    en_proceso: number;
    cancelados: number;
  };
  usuarios: {
    total: number;
    activos: number;
  };
  ingresos: {
    estimado: number;
    mes_actual: number;
  };
}

const ReportesAdmin: React.FC = () => {
  const [reporteData, setReporteData] = useState<ReporteData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadReporteData();
  }, []);

  const loadReporteData = async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Cargar datos de múltiples endpoints
      const [enviosResponse, usuariosResponse] = await Promise.all([
        api.get('/envios/'),
        api.get('/usuarios/')
      ]);

      const envios = (enviosResponse.data as any)?.results || [];
      const usuarios = (usuariosResponse.data as any)?.results || [];

      // Calcular estadísticas
      const data: ReporteData = {
        envios: {
          total: envios.length,
          entregados: envios.filter((e: any) => e.estado_actual === 'entregado').length,
          en_proceso: envios.filter((e: any) => ['recibido', 'en_transito', 'en_reparto'].includes(e.estado_actual)).length,
          cancelados: envios.filter((e: any) => e.estado_actual === 'cancelado').length,
        },
        usuarios: {
          total: usuarios.length,
          activos: usuarios.filter((u: any) => u.is_active).length,
        },
        ingresos: {
          estimado: envios.reduce((sum: number, e: any) => sum + (e.precio_estimado || 0), 0),
          mes_actual: envios.filter((e: any) => {
            const fecha = new Date(e.fecha_creacion);
            const ahora = new Date();
            return fecha.getMonth() === ahora.getMonth() && fecha.getFullYear() === ahora.getFullYear();
          }).reduce((sum: number, e: any) => sum + (e.precio_estimado || 0), 0)
        }
      };

      setReporteData(data);
    } catch (error) {
      console.error('Error cargando datos de reportes:', error);
      setError('Error al cargar los datos de reportes');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="reportes-admin loading">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Cargando reportes...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="reportes-admin error">
        <div className="error-container">
          <h2>Error al cargar reportes</h2>
          <p>{error}</p>
          <button onClick={loadReporteData} className="retry-button">
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  if (!reporteData) {
    return <div>No hay datos disponibles</div>;
  }

  return (
    <div className="reportes-admin">
      {/* Header de la página */}
      <div className="page-header">
        <div className="header-content">
          <h1>Reportes y Análisis</h1>
          <p>Análisis detallado del rendimiento de la empresa</p>
        </div>
        <div className="header-actions">
          <button className="btn btn-primary">
            Exportar Reporte
          </button>
          <button className="btn btn-secondary">
            Configurar Filtros
          </button>
        </div>
      </div>

      {/* Métricas principales */}
      <div className="reportes-grid">
        {/* Reporte de Envíos */}
        <div className="reporte-card envios">
          <div className="card-header">
            <h3>📦 Análisis de Envíos</h3>
          </div>
          <div className="card-content">
            <div className="metric-main">
              <span className="metric-value">{reporteData.envios.total}</span>
              <span className="metric-label">Total Envíos</span>
            </div>
            <div className="metrics-breakdown">
              <div className="breakdown-item">
                <span className="breakdown-value">{reporteData.envios.entregados}</span>
                <span className="breakdown-label">Entregados</span>
                <span className="breakdown-percentage">
                  {reporteData.envios.total > 0 ?
                    Math.round((reporteData.envios.entregados / reporteData.envios.total) * 100) : 0}%
                </span>
              </div>
              <div className="breakdown-item">
                <span className="breakdown-value">{reporteData.envios.en_proceso}</span>
                <span className="breakdown-label">En Proceso</span>
                <span className="breakdown-percentage">
                  {reporteData.envios.total > 0 ?
                    Math.round((reporteData.envios.en_proceso / reporteData.envios.total) * 100) : 0}%
                </span>
              </div>
              <div className="breakdown-item">
                <span className="breakdown-value">{reporteData.envios.cancelados}</span>
                <span className="breakdown-label">Cancelados</span>
                <span className="breakdown-percentage">
                  {reporteData.envios.total > 0 ?
                    Math.round((reporteData.envios.cancelados / reporteData.envios.total) * 100) : 0}%
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Reporte de Usuarios */}
        <div className="reporte-card usuarios">
          <div className="card-header">
            <h3>👥 Análisis de Usuarios</h3>
          </div>
          <div className="card-content">
            <div className="metric-main">
              <span className="metric-value">{reporteData.usuarios.total}</span>
              <span className="metric-label">Total Usuarios</span>
            </div>
            <div className="metrics-breakdown">
              <div className="breakdown-item">
                <span className="breakdown-value">{reporteData.usuarios.activos}</span>
                <span className="breakdown-label">Activos</span>
                <span className="breakdown-percentage">
                  {reporteData.usuarios.total > 0 ?
                    Math.round((reporteData.usuarios.activos / reporteData.usuarios.total) * 100) : 0}%
                </span>
              </div>
              <div className="breakdown-item">
                <span className="breakdown-value">
                  {reporteData.usuarios.total - reporteData.usuarios.activos}
                </span>
                <span className="breakdown-label">Inactivos</span>
                <span className="breakdown-percentage">
                  {reporteData.usuarios.total > 0 ?
                    Math.round(((reporteData.usuarios.total - reporteData.usuarios.activos) / reporteData.usuarios.total) * 100) : 0}%
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Reporte de Ingresos */}
        <div className="reporte-card ingresos">
          <div className="card-header">
            <h3>💰 Análisis Financiero</h3>
          </div>
          <div className="card-content">
            <div className="metric-main">
              <span className="metric-value">${reporteData.ingresos.estimado.toFixed(2)}</span>
              <span className="metric-label">Ingresos Estimados</span>
            </div>
            <div className="metrics-breakdown">
              <div className="breakdown-item">
                <span className="breakdown-value">${reporteData.ingresos.mes_actual.toFixed(2)}</span>
                <span className="breakdown-label">Este Mes</span>
              </div>
              <div className="breakdown-item">
                <span className="breakdown-value">
                  ${(reporteData.ingresos.estimado / Math.max(reporteData.envios.total, 1)).toFixed(2)}
                </span>
                <span className="breakdown-label">Promedio por Envío</span>
              </div>
            </div>
          </div>
        </div>

        {/* Reporte de Rendimiento */}
        <div className="reporte-card rendimiento">
          <div className="card-header">
            <h3>📈 Indicadores de Rendimiento</h3>
          </div>
          <div className="card-content">
            <div className="kpi-list">
              <div className="kpi-item">
                <span className="kpi-label">Tasa de Entrega</span>
                <span className="kpi-value">
                  {reporteData.envios.total > 0 ?
                    Math.round((reporteData.envios.entregados / reporteData.envios.total) * 100) : 0}%
                </span>
              </div>
              <div className="kpi-item">
                <span className="kpi-label">Eficiencia Operativa</span>
                <span className="kpi-value">
                  {reporteData.envios.total > 0 ?
                    Math.round(((reporteData.envios.entregados + reporteData.envios.en_proceso) / reporteData.envios.total) * 100) : 0}%
                </span>
              </div>
              <div className="kpi-item">
                <span className="kpi-label">Usuarios Activos</span>
                <span className="kpi-value">
                  {reporteData.usuarios.total > 0 ?
                    Math.round((reporteData.usuarios.activos / reporteData.usuarios.total) * 100) : 0}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Acciones adicionales */}
      <div className="reportes-actions">
        <h2>Acciones Disponibles</h2>
        <div className="actions-grid">
          <button className="action-card">
            <h3>📊 Reporte Detallado</h3>
            <p>Generar reporte completo con gráficos</p>
          </button>
          <button className="action-card">
            <h3>📈 Análisis de Tendencias</h3>
            <p>Ver evolución en el tiempo</p>
          </button>
          <button className="action-card">
            <h3>💾 Exportar Datos</h3>
            <p>Descargar datos en Excel/CSV</p>
          </button>
          <button className="action-card">
            <h3>⚙️ Configurar Alertas</h3>
            <p>Notificaciones automáticas</p>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ReportesAdmin;
