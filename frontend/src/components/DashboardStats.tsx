import React, { useState, useEffect } from 'react';
import { enviosAPI } from '../services/api';

interface DashboardStatsData {
  total: number;
  porEstado: {
    [key: string]: number;
  };
  recientes: number;
  pendientes: number;
  entregadosHoy: number;
}

const DashboardStats: React.FC = () => {
  const [stats, setStats] = useState<DashboardStatsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    setLoading(true);
    console.log("DashboardStats: Iniciando carga de estadísticas");

    try {
      console.log("DashboardStats: Solicitando /envios/estadisticas/");
      const response = await enviosAPI.getEstadisticas();
      if (!response.data) {
        setError('La respuesta de la API no contiene datos');
        return;
      }
      const d: any = response.data;
      const porEstado = d.porEstado || d.por_estado || {};
      const statsMapped: DashboardStatsData = {
        total: d.total ?? 0,
        porEstado,
        pendientes: d.pendientes ?? 0,
        entregadosHoy: d.entregadosHoy ?? d.entregados_hoy ?? 0,
        recientes: d.recientes ?? 0,
      };
      setStats(statsMapped);
    } catch (error: unknown) {
      console.error("DashboardStats: Error cargando estadísticas:", error);
      setError('No se pudieron cargar las estadísticas');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="dashboard-loading">Cargando estadísticas...</div>;
  if (error) return <div className="dashboard-error">{error}</div>;
  if (!stats) return <div className="dashboard-error">No se pudieron cargar las estadísticas</div>;

  return (
    <div className="dashboard-stats">
      <div className="stats-header">
        <h2>Resumen de Operaciones</h2>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📦</div>
          <div className="stat-value">{stats.total}</div>
          <div className="stat-label">Total de Envíos</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🆕</div>
          <div className="stat-value">{stats.recientes}</div>
          <div className="stat-label">Envíos Nuevos (7 días)</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⏳</div>
          <div className="stat-value">{stats.pendientes}</div>
          <div className="stat-label">Envíos Pendientes</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-value">{stats.entregadosHoy}</div>
          <div className="stat-label">Entregados Hoy</div>
        </div>
      </div>

      <div className="stats-by-status">
        <h3>Envíos por Estado</h3>
        <div className="status-bars">
          {Object.entries(stats.porEstado).map(([estado, cantidad]) => (
            <div key={estado} className="status-bar-container">
              <div className="status-bar-label">
                {estado} <span className="status-count">({cantidad})</span>
              </div>
              <div className="status-bar-wrapper">
                <div
                  className={`status-bar status-${estado.toLowerCase().replace(/\s+/g, '-')}`}
                  data-percentage={(cantidad / stats.total) * 100}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DashboardStats;
