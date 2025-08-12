import React, { useState, useEffect } from 'react';
import { enviosAPI } from '../services/api';
import { Envio } from '../types';
import axios from 'axios';

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
      // Simulamos obtener estadísticas desde los envíos
      // En un entorno real, esto se haría con un endpoint específico
      console.log("DashboardStats: Realizando llamada a enviosAPI.getAll");
      const response = await enviosAPI.getAll(1, 1000); // Traer todos para calcular estadísticas
      console.log("DashboardStats: Respuesta de la API recibida", response);
      
      if (!response.data) {
        console.error("DashboardStats: La respuesta no contiene datos:", response);
        setError('La respuesta de la API no contiene datos');
        setLoading(false);
        return;
      }
      
      const envios = response.data?.results || [];
      console.log("DashboardStats: Envíos obtenidos:", envios.length);
      
      // Si no hay envíos, mostrar estadísticas vacías en lugar de error
      if (envios.length === 0) {
        setStats({
          total: 0,
          porEstado: {},
          pendientes: 0,
          entregadosHoy: 0,
          recientes: 0
        });
        setLoading(false);
        return;
      }
      
      // Fecha actual
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      // Calcular estadísticas
      const porEstado: {[key: string]: number} = {};
      let pendientes = 0;
      let entregadosHoy = 0;
      let recientes = 0;
      
      envios.forEach((envio: Envio) => {
        try {
          // Conteo por estado
          const estadoKey = envio.estado_display || envio.estado_actual || 'Desconocido';
          porEstado[estadoKey] = (porEstado[estadoKey] || 0) + 1;
          
          // Envíos pendientes (no entregados/cancelados/devueltos)
          if (envio.estado_actual && !['ENTREGADO', 'CANCELADO', 'DEVUELTO'].includes(envio.estado_actual.toUpperCase())) {
            pendientes++;
          }
          
          // Envíos entregados hoy
          if (envio.estado_actual && envio.estado_actual.toUpperCase() === 'ENTREGADO' && envio.ultima_actualizacion) {
            const fechaActualizacion = new Date(envio.ultima_actualizacion);
            if (fechaActualizacion >= today) {
              entregadosHoy++;
            }
          }
          
          // Envíos recientes (últimos 7 días)
          if (envio.fecha_creacion) {
            const fechaRegistro = new Date(envio.fecha_creacion);
            const sevenDaysAgo = new Date();
            sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
            if (fechaRegistro >= sevenDaysAgo) {
              recientes++;
            }
          }
        } catch (e) {
          console.error("DashboardStats: Error procesando envío:", e, envio);
        }
      });
      
      setStats({
        total: envios.length,
        porEstado,
        pendientes,
        entregadosHoy,
        recientes
      });
      
      console.log("DashboardStats: Estadísticas calculadas:", {
        total: envios.length,
        porEstado,
        pendientes,
        entregadosHoy,
        recientes
      });
      
    } catch (error: unknown) {
      console.error("DashboardStats: Error en loadStats:", error);
      // Imprimir detalles completos del error para depuración
      try {
        console.error("DashboardStats: Error completo:", JSON.stringify(error, null, 2));
      } catch {
        console.error("DashboardStats: No se pudo convertir el error a JSON");
      }
      
      // Mostrar mensaje más específico según el tipo de error
      if (axios.isAxiosError(error)) {
        const axiosError = error as any; // Type casting para acceder a propiedades de axios
        if (axiosError.response) {
          // Error de respuesta del servidor
          console.error("DashboardStats: Error de respuesta:", axiosError.response.status, axiosError.response.statusText);
          setError(`Error al cargar estadísticas: ${axiosError.response.status} - ${axiosError.response.statusText}`);
        } else if (axiosError.request) {
          // No se recibió respuesta
          console.error("DashboardStats: No se recibió respuesta del servidor");
          setError('No se recibió respuesta del servidor. Compruebe su conexión.');
        } else {
          // Error en la configuración de la solicitud
          const errorMessage = axiosError.message || 'Error desconocido';
          console.error("DashboardStats: Error en configuración de solicitud:", errorMessage);
          setError(`Error al configurar la solicitud: ${errorMessage}`);
        }
      } else if (error instanceof Error) {
        console.error("DashboardStats: Error general:", error.message);
        setError(`Error: ${error.message}`);
      } else {
        console.error("DashboardStats: Error desconocido");
        setError('Error desconocido al cargar las estadísticas');
      }
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
          <div className="stat-icon">
            <span className="icon icon-package icon-xl"></span>
          </div>
          <div className="stat-value">{stats.total}</div>
          <div className="stat-label">Total de Envíos</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">
            <span className="icon icon-stats icon-xl"></span>
          </div>
          <div className="stat-value">{stats.recientes}</div>
          <div className="stat-label">Envíos Nuevos (7 días)</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">
            <span className="icon icon-search icon-xl"></span>
          </div>
          <div className="stat-value">{stats.pendientes}</div>
          <div className="stat-label">Envíos Pendientes</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">
            <span className="icon icon-user icon-xl"></span>
          </div>
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
