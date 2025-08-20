import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Package, Search, Bell, MapPin, CheckCircle, Clock } from 'lucide-react';
import { enviosAPI } from '../../services/api';

interface Empresa {
  id: number;
  nombre: string;
  slug: string;
}

interface PerfilUsuario {
  rol: 'destinatario';
  fecha_ingreso?: string;
}

interface DashboardDestinatarioProps {
  empresa: Empresa;
  perfil: PerfilUsuario;
}

interface PaquetesRecibidos {
  total: number;
  recibidos: number;
  en_camino: number;
  pendientes: number;
  recientes: any[];
}

/**
 * 📥 DASHBOARD PARA DESTINATARIOS
 *
 * Funcionalidades:
 * - Ver paquetes dirigidos a mí
 * - Rastrear envíos
 * - Notificaciones de llegada
 * - Historial de recepciones
 */

const DashboardDestinatario: React.FC<DashboardDestinatarioProps> = ({ empresa, perfil }) => {
  const [misPaquetes, setMisPaquetes] = useState<PaquetesRecibidos>({
    total: 0,
    recibidos: 0,
    en_camino: 0,
    pendientes: 0,
    recientes: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    cargarMisPaquetes();
  }, []);

  const cargarMisPaquetes = async () => {
    try {
      setLoading(true);

      // En producción, filtrar por destinatario actual
      const response = await enviosAPI.getAll();
      const envios = Array.isArray((response.data as any)?.results)
        ? (response.data as any).results
        : [];

      // Simular paquetes para el destinatario
      const total = envios.length;
      const recibidos = envios.filter((e: any) => e.estado_actual === 'ENTREGADO').length;
      const en_camino = envios.filter((e: any) =>
        ['EN_TRANSITO', 'EN_REPARTO'].includes(e.estado_actual)
      ).length;
      const pendientes = envios.filter((e: any) => e.estado_actual === 'RECIBIDO').length;

      setMisPaquetes({
        total,
        recibidos,
        en_camino,
        pendientes,
        recientes: envios.slice(0, 3)
      });

    } catch (err: any) {
      console.error('Error cargando mis paquetes:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-destinatario-loading">
        <div className="loading-spinner"></div>
        <p>Cargando tus paquetes...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-destinatario">
      {/* Bienvenida personalizada */}
      <div className="dashboard-welcome">
        <h2>📥 Panel de Destinatario</h2>
        <p>Tus paquetes con {empresa.nombre}</p>
      </div>

      {/* Estado de mis paquetes */}
      <div className="dashboard-summary">
        <h3>📊 Estado de Mis Paquetes</h3>
        <div className="summary-grid">
          <div className="summary-card total">
            <div className="summary-icon">
              <Package size={24} />
            </div>
            <div className="summary-content">
              <h4>Total Paquetes</h4>
              <p className="summary-number">{misPaquetes.total}</p>
            </div>
          </div>

          <div className="summary-card success">
            <div className="summary-icon">
              <CheckCircle size={24} />
            </div>
            <div className="summary-content">
              <h4>Recibidos</h4>
              <p className="summary-number">{misPaquetes.recibidos}</p>
            </div>
          </div>

          <div className="summary-card warning">
            <div className="summary-icon">
              <MapPin size={24} />
            </div>
            <div className="summary-content">
              <h4>En Camino</h4>
              <p className="summary-number">{misPaquetes.en_camino}</p>
            </div>
          </div>

          <div className="summary-card info">
            <div className="summary-icon">
              <Clock size={24} />
            </div>
            <div className="summary-content">
              <h4>Pendientes</h4>
              <p className="summary-number">{misPaquetes.pendientes}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Notificaciones importantes */}
      {misPaquetes.en_camino > 0 && (
        <div className="dashboard-notifications">
          <div className="notification important">
            <Bell size={20} />
            <div className="notification-content">
              <h4>🚚 Paquetes en Camino</h4>
              <p>Tienes {misPaquetes.en_camino} paquete(s) que pronto llegará(n) a tu dirección.</p>
            </div>
          </div>
        </div>
      )}

      {/* Paquetes recientes */}
      <div className="dashboard-recent">
        <h3>📦 Mis Paquetes Recientes</h3>
        {misPaquetes.recientes.length > 0 ? (
          <div className="recent-list">
            {misPaquetes.recientes.map((paquete: any, index: number) => (
              <div key={paquete.id || index} className="recent-item">
                <div className="recent-header">
                  <span className="recent-guide">{paquete.numero_guia || `PK${Date.now()}${index}`}</span>
                  <span className={`status-badge ${paquete.estado_actual?.toLowerCase() || 'pendiente'}`}>
                    {paquete.estado_actual === 'ENTREGADO' ? '✅ Recibido' :
                     paquete.estado_actual === 'EN_REPARTO' ? '🚚 En Reparto' :
                     paquete.estado_actual === 'EN_TRANSITO' ? '✈️ En Tránsito' :
                     '📦 Procesando'}
                  </span>
                </div>
                <div className="recent-content">
                  <p><strong>De:</strong> {paquete.remitente_nombre || 'Remitente'}</p>
                  <p><strong>Descripción:</strong> {paquete.descripcion || 'Sin descripción'}</p>
                  <p><strong>Fecha:</strong> {paquete.fecha_creacion ? new Date(paquete.fecha_creacion).toLocaleDateString() : 'Fecha no disponible'}</p>
                </div>
                <div className="recent-actions">
                  <Link to={`/envios/${paquete.id}`} className="btn-action view">
                    Ver Detalles
                  </Link>
                  {paquete.estado_actual === 'EN_REPARTO' && (
                    <button className="btn-action confirm">
                      Confirmar Recepción
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-recent">
            <p>📭 No tienes paquetes recientes</p>
            <p>Cuando alguien te envíe algo, aparecerá aquí.</p>
          </div>
        )}
      </div>

      {/* Acciones principales */}
      <div className="dashboard-actions">
        <h3>🔍 ¿Qué quieres hacer?</h3>
        <div className="actions-grid">
          <Link to="/rastreo" className="action-card primary">
            <Search size={24} />
            <div className="action-content">
              <h4>Rastrear Paquete</h4>
              <p>Buscar por número de guía</p>
            </div>
          </Link>

          <Link to="/mis-paquetes" className="action-card">
            <Package size={24} />
            <div className="action-content">
              <h4>Todos Mis Paquetes</h4>
              <p>Historial completo</p>
            </div>
          </Link>

          <Link to="/notificaciones" className="action-card">
            <Bell size={24} />
            <div className="action-content">
              <h4>Notificaciones</h4>
              <p>Configurar alertas</p>
            </div>
          </Link>

          <Link to="/contacto" className="action-card">
            <MapPin size={24} />
            <div className="action-content">
              <h4>Contactar Empresa</h4>
              <p>Soporte y consultas</p>
            </div>
          </Link>
        </div>
      </div>

      {/* Información útil para destinatario */}
      <div className="dashboard-info">
        <h3>💡 Información Importante</h3>
        <div className="info-grid">
          <div className="info-item">
            <h4>📍 Dirección de Entrega</h4>
            <p>Verifica que tu dirección esté actualizada para las entregas.</p>
          </div>
          <div className="info-item">
            <h4>📞 Contacto</h4>
            <p>Mantén tu número de teléfono actualizado para coordinar entregas.</p>
          </div>
          <div className="info-item">
            <h4>⏰ Horarios</h4>
            <p>Las entregas se realizan de lunes a viernes de 9:00 AM a 5:00 PM.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardDestinatario;
