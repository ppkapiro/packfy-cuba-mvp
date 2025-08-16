import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';
import { enviosAPI } from '../services/api';
import Skeleton, { SkeletonText, SkeletonRow } from '../components/Skeleton';

// 🇨🇺 VER ENVÍO UNIFICADO - Sin CSS personalizado, con CSS Master

// Funciones auxiliares mejoradas
const formatearMoneda = (valor: string | number | null | undefined): string => {
  if (!valor) return '$0.00';

  try {
    const numero = typeof valor === 'string' ? parseFloat(valor) : valor;
    if (isNaN(numero)) return '$0.00';
    return `$${numero.toFixed(2)}`;
  } catch (error) {
    console.error('Error al formatear moneda:', valor, error);
    return '$0.00';
  }
};

const formatearPeso = (peso: string | number | null | undefined): string => {
  if (!peso) return '0 lbs';

  try {
    const numero = typeof peso === 'string' ? parseFloat(peso) : peso;
    if (isNaN(numero)) return '0 lbs';
    return `${numero} lbs`;
  } catch (error) {
    console.error('Error al formatear peso:', peso, error);
    return '0 lbs';
  }
};

const formatearFechaSafe = (fecha: string | null | undefined, formato: string = 'dd/MM/yyyy HH:mm'): string => {
  if (!fecha) return 'No disponible';

  try {
    const fechaObj = new Date(fecha);
    if (isNaN(fechaObj.getTime())) {
      console.warn('Fecha inválida recibida:', fecha);
      return 'Fecha inválida';
    }
    return format(fechaObj, formato, { locale: es });
  } catch (error) {
    console.error('Error al formatear fecha:', fecha, error);
    return 'Error en fecha';
  }
};

// Función para obtener el icono del estado
const getEstadoIcon = (estado: string): string => {
  switch (estado?.toLowerCase()) {
    case 'pendiente':
      return '⏳';
    case 'en_transito':
    case 'en_camino':
      return '🚚';
    case 'entregado':
      return '✅';
    case 'cancelado':
      return '❌';
    default:
      return '📦';
  }
};

// Función para obtener el color del estado
const getEstadoColor = (estado: string): string => {
  switch (estado?.toLowerCase()) {
    case 'pendiente':
      return 'text-warning';
    case 'en_transito':
    case 'en_camino':
      return 'text-info';
    case 'entregado':
      return 'text-success';
    case 'cancelado':
      return 'text-error';
    default:
      return 'text-muted';
  }
};

interface HistorialEstado {
  id: number;
  estado: string;
  estado_display: string;
  fecha_cambio: string;
  notas?: string;
}

const ShipmentDetail: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [envio, setEnvio] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [nuevoEstado, setNuevoEstado] = useState('');
  const [notasEstado, setNotasEstado] = useState('');
  const [actualizandoEstado, setActualizandoEstado] = useState(false);
  const [historialEstados, setHistorialEstados] = useState<HistorialEstado[]>([]);

  // Cargar datos del envío
  const cargarEnvio = async () => {
    try {
      setLoading(true);
      const response = await enviosAPI.getById(Number(id));
      setEnvio(response.data);

      // Para el historial, asumimos que vendrá en una futura actualización
      setHistorialEstados([]);

    } catch (error: any) {
      console.error('Error al cargar envío:', error);
      setError(error.message || 'Error al cargar los datos del envío');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (id) {
      cargarEnvio();
    }
  }, [id]);

  // Cambiar estado del envío
  const cambiarEstado = async () => {
    if (!nuevoEstado) return;

    try {
      setActualizandoEstado(true);
      await enviosAPI.update(Number(id), {
        estado: nuevoEstado,
        notas: notasEstado || ''
      });

      // Recargar datos
      await cargarEnvio();

      // Limpiar formulario
      setNuevoEstado('');
      setNotasEstado('');

    } catch (error: any) {
      console.error('Error al cambiar estado:', error);
      setError(error.message || 'Error al cambiar el estado');
    } finally {
      setActualizandoEstado(false);
    }
  };

  const estados = [
    { value: 'pendiente', label: '⏳ Pendiente' },
    { value: 'en_transito', label: '🚚 En Tránsito' },
    { value: 'entregado', label: '✅ Entregado' },
    { value: 'cancelado', label: '❌ Cancelado' }
  ];

  // Estados de carga y error
  if (loading) {
    return (
      <div className="page-container page-enter">
        <div className="form-container">
          <Skeleton width={280} height={28} className="mb-3" />
          <SkeletonText lines={3} />
          <div className="mt-4">
            <SkeletonRow columns={4} />
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-container">
        <div className="alert alert-error">
          <span>
            <strong>❌ Error</strong><br />
            {error}
          </span>
          <button
            onClick={() => navigate('/gestion')}
            className="btn btn-secondary btn-sm"
          >
            🔙 Volver a Gestión
          </button>
        </div>
      </div>
    );
  }

  if (!envio) {
    return (
      <div className="page-container">
        <div className="alert alert-warning">
          <span>
            <strong>📦 Envío no encontrado</strong><br />
            No se pudo encontrar el envío solicitado.
          </span>
          <button
            onClick={() => navigate('/gestion')}
            className="btn btn-secondary btn-sm"
          >
            🔙 Volver a Gestión
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      {/* Header */}
  <div className="page-header">
        <div>
          <h1 className="page-title">📦 Envío #{envio.numero_guia}</h1>
          <p className="page-subtitle">
            Detalles completos y gestión del envío
          </p>
        </div>
        <div className="page-actions">
          <button
            onClick={() => navigate('/gestion')}
    className="btn btn-secondary pressable hover-lift ripple"
          >
            🔙 Volver a Gestión
          </button>
          <button
            onClick={() => navigate(`/envios/editar/${envio.id}`)}
    className="btn btn-primary pressable hover-lift ripple"
          >
            ✏️ Editar Envío
          </button>
        </div>
      </div>

      {/* Estado actual destacado */}
      <div className="card mb-4">
        <div className="card-body">
          <div className="d-flex justify-between align-center">
            <div className="d-flex align-center gap-3">
              <span className="shipment-status-icon">
                {getEstadoIcon(envio.estado)}
              </span>
              <div>
                <h3 className={`shipment-status-text ${getEstadoColor(envio.estado)}`}>
                  {envio.estado_display || envio.estado}
                </h3>
                <p className="text-muted">Estado actual del envío</p>
              </div>
            </div>

            {envio.fecha_entrega_real && (
              <div className="text-right">
                <p className="text-success font-bold">✅ Entregado</p>
                <p className="text-muted">{formatearFechaSafe(envio.fecha_entrega_real)}</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Información principal */}
      <div className="stats-grid mb-4">
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-title">Peso</span>
            <span className="stat-icon">⚖️</span>
          </div>
          <div className="stat-value">{formatearPeso(envio.peso)}</div>
        </div>

        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-title">Valor Declarado</span>
            <span className="stat-icon">💰</span>
          </div>
          <div className="stat-value text-success">{formatearMoneda(envio.valor_declarado)}</div>
        </div>

        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-title">Precio Total</span>
            <span className="stat-icon">💵</span>
          </div>
          <div className="stat-value text-primary">{formatearMoneda(envio.precio_total)}</div>
        </div>

        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-title">Fecha Creación</span>
            <span className="stat-icon">📅</span>
          </div>
          <div className="stat-value">{formatearFechaSafe(envio.fecha_creacion, 'dd/MM/yyyy')}</div>
        </div>
      </div>

      {/* Detalles del envío */}
      <div className="form-container">

        {/* Información del paquete */}
        <div className="form-section">
          <h3 className="form-section-title">📦 Información del Paquete</h3>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Descripción</label>
              <p className="form-text">{envio.descripcion || 'No especificada'}</p>
            </div>
            <div className="form-group">
              <label className="form-label">Dimensiones (cm)</label>
              <p className="form-text">
                {envio.largo || 0} × {envio.ancho || 0} × {envio.alto || 0}
              </p>
            </div>
          </div>

          {envio.notas && (
            <div className="form-group">
              <label className="form-label">Notas especiales</label>
              <p className="form-text">{envio.notas}</p>
            </div>
          )}
        </div>

        {/* Información del remitente */}
        <div className="form-section">
          <h3 className="form-section-title">👤 Remitente</h3>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Nombre</label>
              <p className="form-text">{envio.remitente_nombre}</p>
            </div>
            <div className="form-group">
              <label className="form-label">Teléfono</label>
              <p className="form-text">{envio.remitente_telefono}</p>
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Email</label>
              <p className="form-text">{envio.remitente_email || 'No especificado'}</p>
            </div>
          </div>
          <div className="form-group">
            <label className="form-label">Dirección</label>
            <p className="form-text">{envio.remitente_direccion}</p>
          </div>
        </div>

        {/* Información del destinatario */}
        <div className="form-section">
          <h3 className="form-section-title">🎯 Destinatario</h3>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Nombre</label>
              <p className="form-text">{envio.destinatario_nombre}</p>
            </div>
            <div className="form-group">
              <label className="form-label">Teléfono</label>
              <p className="form-text">{envio.destinatario_telefono}</p>
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Email</label>
              <p className="form-text">{envio.destinatario_email || 'No especificado'}</p>
            </div>
          </div>
          <div className="form-group">
            <label className="form-label">Dirección</label>
            <p className="form-text">{envio.destinatario_direccion}</p>
          </div>
        </div>

        {/* Cambiar estado */}
        <div className="form-section">
          <h3 className="form-section-title">🔄 Gestión de Estado</h3>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Nuevo Estado</label>
              <select
                value={nuevoEstado}
                onChange={(e) => setNuevoEstado(e.target.value)}
                className="form-control input-focus"
                aria-label="Seleccionar nuevo estado"
              >
                <option value="">Seleccionar estado...</option>
                {estados.map(estado => (
                  <option key={estado.value} value={estado.value}>
                    {estado.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Notas del cambio (opcional)</label>
            <textarea
              value={notasEstado}
              onChange={(e) => setNotasEstado(e.target.value)}
              className="form-control input-focus"
              rows={3}
              placeholder="Agregar comentarios sobre el cambio de estado..."
              aria-label="Notas del cambio de estado"
            />
          </div>

          <button
            onClick={cambiarEstado}
            className="btn btn-warning pressable hover-lift ripple"
            disabled={!nuevoEstado || actualizandoEstado}
          >
            {actualizandoEstado ? '⏳ Actualizando...' : '🔄 Cambiar Estado'}
          </button>
        </div>

        {/* Historial de estados */}
        {historialEstados.length > 0 && (
          <div className="form-section">
            <h3 className="form-section-title">📋 Historial de Estados</h3>
            <div className="timeline">
              {historialEstados.map((item) => (
                <div key={item.id} className="timeline-item">
                  <div className="timeline-marker">
                    <span className={getEstadoColor(item.estado)}>
                      {getEstadoIcon(item.estado)}
                    </span>
                  </div>
                  <div className="timeline-content">
                    <div className="timeline-header">
                      <h4 className={`timeline-title ${getEstadoColor(item.estado)}`}>
                        {item.estado_display}
                      </h4>
                      <span className="timeline-date">
                        {formatearFechaSafe(item.fecha_cambio)}
                      </span>
                    </div>
                    {item.notas && (
                      <p className="timeline-notes">{item.notas}</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Acciones adicionales */}
        <div className="d-flex gap-3 justify-center">
          <button
            onClick={() => window.print()}
            className="btn btn-info pressable hover-lift ripple"
          >
            🖨️ Imprimir Detalles
          </button>
          <button
            onClick={() => navigate(`/rastrear/${envio.numero_guia}`)}
            className="btn btn-secondary pressable hover-lift ripple"
          >
            🔍 Ver Seguimiento Público
          </button>
        </div>
      </div>
    </div>
  );
};

export default ShipmentDetail;
