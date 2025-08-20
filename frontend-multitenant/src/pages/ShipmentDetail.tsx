import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';
import { enviosAPI } from '../services/api';

// Funciones auxiliares para manejo seguro de datos
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
  if (!peso) return '0 kg';
  
  try {
    const numero = typeof peso === 'string' ? parseFloat(peso) : peso;
    if (isNaN(numero)) return '0 kg';
    return `${numero} kg`;
  } catch (error) {
    console.error('Error al formatear peso:', peso, error);
    return '0 kg';
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

interface HistorialEstado {
  id: string;
  estado_anterior: string;
  estado_nuevo: string;
  estado_anterior_display: string;
  estado_nuevo_display: string;
  fecha_cambio: string;
  usuario: string;
  notas: string;
}

interface Envio {
  id: string;
  numero_guia: string;
  descripcion: string;
  peso: number;
  alto: number;
  ancho: number;
  largo: number;
  valor_declarado: number;
  
  remitente_nombre: string;
  remitente_direccion: string;
  remitente_telefono: string;
  remitente_email: string | null;
  
  destinatario_nombre: string;
  destinatario_direccion: string;
  destinatario_telefono: string;
  destinatario_email: string | null;
  
  estado: string;
  estado_display: string;
  fecha_creacion: string;
  fecha_actualizacion: string;
  fecha_estimada_entrega: string | null;
  fecha_entrega_real: string | null;
  
  notas: string | null;
  historial: HistorialEstado[];
}

const ShipmentDetail = () => {
  const params = useParams();
  const id = params.id;
  const navigate = useNavigate();
  
  const [envio, setEnvio] = useState<Envio | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const [nuevoEstado, setNuevoEstado] = useState('');
  const [notasCambioEstado, setNotasCambioEstado] = useState('');
  const [cambiandoEstado, setCambiandoEstado] = useState(false);
  
  useEffect(() => {
    if (id) {
      cargarEnvio();
    }
  }, [id]);
  
  const cargarEnvio = async () => {
    setLoading(true);
    try {
      const response = await enviosAPI.getById(id!);
      setEnvio(response.data);
    } catch (err) {
      setError('Error al cargar los datos del envío');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  const handleCambioEstado = async () => {
    if (!nuevoEstado) return;
    
    setCambiandoEstado(true);
    try {
      await enviosAPI.changeStatus(id!, nuevoEstado, notasCambioEstado);
      await cargarEnvio();
      setNuevoEstado('');
      setNotasCambioEstado('');
    } catch (err) {
      setError('Error al cambiar el estado del envío');
      console.error(err);
    } finally {
      setCambiandoEstado(false);
    }
  };
  
  if (loading) {
    return <div className="loading">Cargando datos del envío...</div>;
  }
  
  if (error) {
    return <div className="alert alert-error">{error}</div>;
  }
  
  if (!envio) {
    return <div className="not-found">Envío no encontrado</div>;
  }
  
  return (
    <div className="shipment-detail-page">
      <div className="detail-header">
        <h1>Envío #{envio.numero_guia}</h1>
        <div className="detail-actions">
          <button 
            onClick={() => navigate(-1)} 
            className="btn btn-secondary"
          >
            Volver
          </button>
        </div>
      </div>
      
      <div className="shipment-status">
        <span className={`estado estado-${envio.estado}`}>
          {envio.estado_display}
        </span>
        {envio.fecha_entrega_real && (
          <span className="entrega-real">
            Entregado el {formatearFechaSafe(envio.fecha_entrega_real)}
          </span>
        )}
      </div>
      
      <div className="cambio-estado">
        <h3>Cambiar Estado</h3>
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="estado-select">Nuevo Estado:</label>
            <select 
              id="estado-select"
              value={nuevoEstado} 
              onChange={(e) => setNuevoEstado(e.target.value)}
              className="form-control"
              disabled={cambiandoEstado}
              aria-label="Seleccionar nuevo estado del envío"
              title="Seleccionar nuevo estado del envío"
            >
              <option value="">-- Seleccionar nuevo estado --</option>
              {envio.estado !== 'registrado' && <option value="registrado">Registrado</option>}
              {envio.estado !== 'en_transito' && <option value="en_transito">En tránsito</option>}
              {envio.estado !== 'en_almacen' && <option value="en_almacen">En almacén</option>}
              {envio.estado !== 'en_ruta' && <option value="en_ruta">En ruta de entrega</option>}
              {envio.estado !== 'entregado' && <option value="entregado">Entregado</option>}
              {envio.estado !== 'devuelto' && <option value="devuelto">Devuelto</option>}
              {envio.estado !== 'cancelado' && <option value="cancelado">Cancelado</option>}
            </select>
          </div>
          <div className="form-group">
            <input 
              type="text" 
              value={notasCambioEstado}
              onChange={(e) => setNotasCambioEstado(e.target.value)}
              placeholder="Notas sobre el cambio de estado (opcional)"
              className="form-control"
              disabled={cambiandoEstado}
            />
          </div>
          <button 
            className="btn" 
            onClick={handleCambioEstado}
            disabled={!nuevoEstado || cambiandoEstado}
          >
            {cambiandoEstado ? 'Aplicando...' : 'Aplicar Cambio'}
          </button>
        </div>
      </div>
      
      <div className="detail-sections">
        <div className="detail-section">
          <h2>Información del Paquete</h2>
          <div className="detail-grid">
            <div className="detail-item">
              <span className="label">Guía:</span>
              <span className="value">{envio.numero_guia}</span>
            </div>
            <div className="detail-item">
              <span className="label">Descripción:</span>
              <span className="value">{envio.descripcion}</span>
            </div>
            <div className="detail-item">
              <span className="label">Dimensiones:</span>
              <span className="value">{envio.alto} × {envio.ancho} × {envio.largo} cm</span>
            </div>
            <div className="detail-item">
              <span className="label">Peso:</span>
              <span className="value">{formatearPeso(envio.peso)}</span>
            </div>
            <div className="detail-item">
              <span className="label">Valor Declarado:</span>
              <span className="value">{formatearMoneda(envio.valor_declarado)}</span>
            </div>
            <div className="detail-item">
              <span className="label">Fecha de Registro:</span>
              <span className="value">
                {formatearFechaSafe(envio.fecha_creacion)}
              </span>
            </div>
            <div className="detail-item">
              <span className="label">Entrega Estimada:</span>
              <span className="value">
                {envio.fecha_estimada_entrega 
                  ? formatearFechaSafe(envio.fecha_estimada_entrega, 'dd/MM/yyyy')
                  : 'No definida'}
              </span>
            </div>
          </div>
        </div>
        
        <div className="detail-section">
          <h2>Remitente</h2>
          <div className="detail-grid">
            <div className="detail-item">
              <span className="label">Nombre:</span>
              <span className="value">{envio.remitente_nombre}</span>
            </div>
            <div className="detail-item">
              <span className="label">Dirección:</span>
              <span className="value">{envio.remitente_direccion}</span>
            </div>
            <div className="detail-item">
              <span className="label">Teléfono:</span>
              <span className="value">{envio.remitente_telefono}</span>
            </div>
            <div className="detail-item">
              <span className="label">Email:</span>
              <span className="value">{envio.remitente_email || 'No proporcionado'}</span>
            </div>
          </div>
        </div>
        
        <div className="detail-section">
          <h2>Destinatario</h2>
          <div className="detail-grid">
            <div className="detail-item">
              <span className="label">Nombre:</span>
              <span className="value">{envio.destinatario_nombre}</span>
            </div>
            <div className="detail-item">
              <span className="label">Dirección:</span>
              <span className="value">{envio.destinatario_direccion}</span>
            </div>
            <div className="detail-item">
              <span className="label">Teléfono:</span>
              <span className="value">{envio.destinatario_telefono}</span>
            </div>
            <div className="detail-item">
              <span className="label">Email:</span>
              <span className="value">{envio.destinatario_email || 'No proporcionado'}</span>
            </div>
          </div>
        </div>
        
        {envio.notas && (
          <div className="detail-section">
            <h2>Notas</h2>
            <p className="notas">{envio.notas}</p>
          </div>
        )}
      </div>
      
      <div className="historial-section">
        <h2>Historial de Estados</h2>
        
        {envio.historial.length === 0 ? (
          <p className="no-data">No hay registros en el historial</p>
        ) : (
          <div className="historial-timeline">
            {envio.historial.map((item) => (
              <div className="timeline-item" key={item.id}>
                <div className="timeline-dot"></div>
                <div className="timeline-content">
                  <div className="timeline-header">
                    <span className="timeline-date">
                      {formatearFechaSafe(item.fecha_cambio)}
                    </span>
                    {item.usuario && <span className="timeline-user">por {item.usuario}</span>}
                  </div>
                  <div className="timeline-body">
                    <div className="estado-cambio">
                      {item.estado_anterior ? (
                        <>
                          De <span className={`estado estado-${item.estado_anterior}`}>{item.estado_anterior_display}</span> a{' '}
                          <span className={`estado estado-${item.estado_nuevo}`}>{item.estado_nuevo_display}</span>
                        </>
                      ) : (
                        <>
                          Estado inicial: <span className={`estado estado-${item.estado_nuevo}`}>{item.estado_nuevo_display}</span>
                        </>
                      )}
                    </div>
                    {item.notas && <div className="timeline-notes">{item.notas}</div>}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ShipmentDetail;