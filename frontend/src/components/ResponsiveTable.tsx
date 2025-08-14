import React from 'react';
import { Link } from 'react-router-dom';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';
import { Envio } from '../types';

interface ResponsiveTableProps {
  envios: Envio[];
  loading: boolean;
  onRefresh?: () => void;
}

// Hook personalizado para detectar móvil
const useIsMobile = () => {
  const [isMobile, setIsMobile] = React.useState(false);

  React.useEffect(() => {
    const checkIsMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkIsMobile();
    window.addEventListener('resize', checkIsMobile);

    return () => window.removeEventListener('resize', checkIsMobile);
  }, []);

  return isMobile;
};

// Función auxiliar para formatear fechas
const formatearFechaSafe = (fecha: string | null | undefined): string => {
  if (!fecha) return 'No disponible';
  try {
    const fechaObj = new Date(fecha);
    if (isNaN(fechaObj.getTime())) return 'Fecha inválida';
    return format(fechaObj, 'dd/MM/yyyy', { locale: es });
  } catch {
    return 'Error en fecha';
  }
};

// Componente para vista móvil (cards)
const MobileCard: React.FC<{ envio: Envio }> = ({ envio }) => {
  // Función para obtener datos seguros
  const getSafeValue = (value: any, fallback: string = 'No disponible'): string => {
    if (value === null || value === undefined || value === '') {
      return fallback;
    }
    return String(value);
  };

  return (
    <div className="mobile-card">
      <div className="mobile-card-header">
        <div className="card-title">
          <strong>#{getSafeValue(envio.numero_guia, 'Sin número')}</strong>
          <div className="card-id">ID: {getSafeValue(envio.id)}</div>
        </div>
        <span className={`estado estado-${envio.estado_actual?.toLowerCase() || 'desconocido'}`}>
          {getSafeValue(envio.estado_display || envio.estado_actual, 'Desconocido')}
        </span>
      </div>

      <div className="mobile-card-content">
        <div className="card-row">
          <span className="label">📤 De:</span>
          <span className="value">{getSafeValue(envio.remitente_nombre, 'Remitente no especificado')}</span>
        </div>

        <div className="card-row">
          <span className="label">📥 Para:</span>
          <span className="value">{getSafeValue(envio.destinatario_nombre, 'Destinatario no especificado')}</span>
        </div>

        <div className="card-row">
          <span className="label">📅 Registro:</span>
          <span className="value">{formatearFechaSafe(envio.fecha_creacion)}</span>
        </div>

        {envio.fecha_estimada_entrega && (
          <div className="card-row">
            <span className="label">🚚 Entrega:</span>
            <span className="value">{formatearFechaSafe(envio.fecha_estimada_entrega)}</span>
          </div>
        )}

        {envio.descripcion && (
          <div className="card-row">
            <span className="label">📝 Descripción:</span>
            <span className="value">{getSafeValue(envio.descripcion)}</span>
          </div>
        )}
      </div>

      <div className="mobile-card-actions">
        <Link to={`/envios/${envio.id}`} className="btn btn-sm">
          👁️ Ver Detalles
        </Link>
      </div>
    </div>
  );
};

// Componente principal responsive
const ResponsiveTable: React.FC<ResponsiveTableProps> = ({ envios, loading, onRefresh }) => {
  const isMobile = useIsMobile();

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <span>Cargando envíos...</span>
      </div>
    );
  }

  if (envios.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">📦</div>
        <h3>No hay envíos para mostrar</h3>
        <p>Crea tu primer envío para comenzar</p>
        <Link to="/envios/nuevo" className="btn">
          Crear Envío
        </Link>
      </div>
    );
  }

  // Vista móvil - Cards
  if (isMobile) {
    return (
      <div className="mobile-table-container">
        <div className="mobile-table-header">
          <h3>Envíos ({envios.length})</h3>
          {onRefresh && (
            <button onClick={onRefresh} className="btn-refresh" title="Recargar">
              🔄
            </button>
          )}
        </div>

        <div className="mobile-cards-list">
          {envios.map((envio) => (
            <MobileCard key={envio.id} envio={envio} />
          ))}
        </div>
      </div>
    );
  }

  // Vista desktop - Tabla tradicional
  return (
    <div className="table-container">
      <table className="envios-table">
        <thead>
          <tr>
            <th>Guía</th>
            <th>Remitente</th>
            <th>Destinatario</th>
            <th>Estado</th>
            <th>Fecha de Registro</th>
            <th>Entrega Estimada</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {envios.map((envio) => (
            <tr key={envio.id}>
              <td>
                <strong>{envio.numero_guia}</strong>
              </td>
              <td>{envio.remitente_nombre}</td>
              <td>{envio.destinatario_nombre}</td>
              <td>
                <span className={`estado estado-${envio.estado_actual?.toLowerCase() || 'desconocido'}`}>
                  {envio.estado_display || envio.estado_actual || 'Desconocido'}
                </span>
              </td>
              <td>{formatearFechaSafe(envio.fecha_creacion)}</td>
              <td>{formatearFechaSafe(envio.fecha_estimada_entrega)}</td>
              <td>
                <Link to={`/envios/${envio.id}`} className="btn-link">
                  Ver Detalles
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ResponsiveTable;
