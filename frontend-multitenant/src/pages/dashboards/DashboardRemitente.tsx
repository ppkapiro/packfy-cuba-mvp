import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Package, Send, Clock, CheckCircle, Plus, Search } from 'lucide-react';
import { enviosAPI } from '../../services/api';
import { Empresa, PerfilUsuario } from '../../types';

interface DashboardRemitenteProps {
  empresa: Empresa;
  perfil: PerfilUsuario;
}tate, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Package, Plus, Eye, Search, TrendingUp, Clock } from 'lucide-react';
import { enviosAPI } from '../../services/api';

interface Empresa {
  id: number;
  nombre: string;
  slug: string;
}

interface PerfilUsuario {
  rol: 'remitente';
  fecha_ingreso?: string;
}

interface DashboardRemitenteProps {
  empresa: Empresa;
  perfil: PerfilUsuario;
}

interface MisEnvios {
  total: number;
  entregados: number;
  en_transito: number;
  pendientes: number;
  recientes: any[];
}

/**
 * 📤 DASHBOARD PARA REMITENTES
 *
 * Funcionalidades:
 * - Ver mis envíos
 * - Crear nuevos envíos
 * - Seguimiento de paquetes
 * - Historial de envíos
 */

const DashboardRemitente: React.FC<DashboardRemitenteProps> = ({ empresa, perfil }) => {
  const [misEnvios, setMisEnvios] = useState<MisEnvios>({
    total: 0,
    entregados: 0,
    en_transito: 0,
    pendientes: 0,
    recientes: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    cargarMisEnvios();
  }, []);

  const cargarMisEnvios = async () => {
    try {
      setLoading(true);

      // Cargar envíos del remitente actual
      const response = await enviosAPI.getAll();
      const envios = Array.isArray((response.data as any)?.results)
        ? (response.data as any).results
        : [];

      // Procesar estadísticas
      const total = envios.length;
      const entregados = envios.filter((e: any) => e.estado_actual === 'ENTREGADO').length;
      const en_transito = envios.filter((e: any) =>
        ['EN_TRANSITO', 'EN_REPARTO'].includes(e.estado_actual)
      ).length;
      const pendientes = envios.filter((e: any) => e.estado_actual === 'RECIBIDO').length;

      setMisEnvios({
        total,
        entregados,
        en_transito,
        pendientes,
        recientes: envios.slice(0, 3) // Últimos 3 envíos
      });

    } catch (err: any) {
      console.error('Error cargando mis envíos:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-remitente-loading">
        <div className="loading-spinner"></div>
        <p>Cargando tus envíos...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-remitente">
      {/* Bienvenida personalizada */}
      <div className="dashboard-welcome">
        <h2>📤 Panel de Remitente</h2>
        <p>Gestiona tus envíos con {empresa.nombre}</p>
      </div>

      {/* Resumen de mis envíos */}
      <div className="dashboard-summary">
        <h3>📊 Resumen de Mis Envíos</h3>
        <div className="summary-grid">
          <div className="summary-card total">
            <div className="summary-icon">
              <Package size={24} />
            </div>
            <div className="summary-content">
              <h4>Total Envíos</h4>
              <p className="summary-number">{misEnvios.total}</p>
            </div>
          </div>

          <div className="summary-card success">
            <div className="summary-icon">
              <TrendingUp size={24} />
            </div>
            <div className="summary-content">
              <h4>Entregados</h4>
              <p className="summary-number">{misEnvios.entregados}</p>
            </div>
          </div>

          <div className="summary-card warning">
            <div className="summary-icon">
              <Clock size={24} />
            </div>
            <div className="summary-content">
              <h4>En Tránsito</h4>
              <p className="summary-number">{misEnvios.en_transito}</p>
            </div>
          </div>

          <div className="summary-card info">
            <div className="summary-icon">
              <Package size={24} />
            </div>
            <div className="summary-content">
              <h4>Pendientes</h4>
              <p className="summary-number">{misEnvios.pendientes}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Envíos recientes */}
      <div className="dashboard-recent">
        <h3>📦 Mis Envíos Recientes</h3>
        {misEnvios.recientes.length > 0 ? (
          <div className="recent-list">
            {misEnvios.recientes.map((envio: any, index: number) => (
              <div key={envio.id || index} className="recent-item">
                <div className="recent-header">
                  <span className="recent-guide">{envio.numero_guia || `PK${Date.now()}${index}`}</span>
                  <span className={`status-badge ${envio.estado_actual?.toLowerCase() || 'pendiente'}`}>
                    {envio.estado_actual || 'PENDIENTE'}
                  </span>
                </div>
                <div className="recent-content">
                  <p><strong>Para:</strong> {envio.destinatario_nombre || 'Destinatario'}</p>
                  <p><strong>Descripción:</strong> {envio.descripcion || 'Sin descripción'}</p>
                  <p><strong>Fecha:</strong> {envio.fecha_creacion ? new Date(envio.fecha_creacion).toLocaleDateString() : 'Fecha no disponible'}</p>
                </div>
                <div className="recent-actions">
                  <Link to={`/envios/${envio.id}`} className="btn-action view">
                    <Eye size={16} />
                    Ver Detalles
                  </Link>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-recent">
            <p>📭 No tienes envíos recientes</p>
            <p>¡Crea tu primer envío!</p>
          </div>
        )}
      </div>

      {/* Acciones principales */}
      <div className="dashboard-actions">
        <h3>🚀 ¿Qué quieres hacer?</h3>
        <div className="actions-grid">
          <Link to="/envios/nuevo" className="action-card primary">
            <Plus size={24} />
            <div className="action-content">
              <h4>Crear Nuevo Envío</h4>
              <p>Envía un paquete a Cuba</p>
            </div>
          </Link>

          <Link to="/envios" className="action-card">
            <Package size={24} />
            <div className="action-content">
              <h4>Ver Mis Envíos</h4>
              <p>Historial completo</p>
            </div>
          </Link>

          <Link to="/rastreo" className="action-card">
            <Search size={24} />
            <div className="action-content">
              <h4>Rastrear Envío</h4>
              <p>Seguimiento por guía</p>
            </div>
          </Link>

          <Link to="/ayuda" className="action-card">
            <Eye size={24} />
            <div className="action-content">
              <h4>¿Necesitas Ayuda?</h4>
              <p>Guías y soporte</p>
            </div>
          </Link>
        </div>
      </div>

      {/* Información útil para remitente */}
      <div className="dashboard-info">
        <h3>💡 Información Útil</h3>
        <div className="info-grid">
          <div className="info-item">
            <h4>📋 Documentos Requeridos</h4>
            <p>Asegúrate de incluir toda la documentación necesaria para el envío.</p>
          </div>
          <div className="info-item">
            <h4>⏰ Tiempos de Entrega</h4>
            <p>Los envíos a Cuba toman entre 7-15 días hábiles.</p>
          </div>
          <div className="info-item">
            <h4>📞 Soporte</h4>
            <p>¿Preguntas? Contacta al equipo de {empresa.nombre}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardRemitente;
