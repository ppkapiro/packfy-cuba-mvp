import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { enviosAPI } from '../services/api';

// 🇨🇺 PACKFY CUBA - GESTIÓN COMPLETA DE ENVÍOS UNIFICADA
// Página principal para administrar todos los envíos con estilos consistentes

interface Envio {
  id: string;
  numero_guia: string;
  descripcion: string;
  peso: number;
  valor_declarado: number;
  remitente_nombre: string;
  remitente_telefono: string;
  destinatario_nombre: string;
  destinatario_telefono: string;
  estado_actual: string;
  fecha_creacion: string;
  fecha_estimada_entrega: string | null;
  notas?: string;
}

const GestionUnificada: React.FC = () => {
  // Estados principales
  const [envios, setEnvios] = useState<Envio[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Estados de filtros y búsqueda
  const [searchTerm, setSearchTerm] = useState('');
  const [filtroEstado, setFiltroEstado] = useState('');
  const [tipoBusqueda, setTipoBusqueda] = useState<'todos' | 'remitente' | 'destinatario' | 'guia'>('todos');

  // Estados disponibles
  const estadosDisponibles = [
    { value: '', label: 'Todos los estados', icon: '📦' },
    { value: 'RECIBIDO', label: 'Recibido', icon: '📥' },
    { value: 'EN_TRANSITO', label: 'En Tránsito', icon: '🚚' },
    { value: 'EN_REPARTO', label: 'En Reparto', icon: '🏃‍♂️' },
    { value: 'ENTREGADO', label: 'Entregado', icon: '✅' },
    { value: 'DEVUELTO', label: 'Devuelto', icon: '↩️' },
    { value: 'CANCELADO', label: 'Cancelado', icon: '❌' }
  ];

  // Cargar envíos al montar el componente
  useEffect(() => {
    cargarEnvios();
  }, []);

  const cargarEnvios = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await enviosAPI.getAll();
      console.log('📦 Envíos cargados:', response.data);

      // Manejar tanto respuesta paginada como array directo
      const enviosData = (response.data as any)?.results || response.data || [];
      setEnvios(enviosData);

    } catch (err: any) {
      console.error('❌ Error al cargar envíos:', err);
      setError(err?.response?.data?.detail || err?.message || 'Error al cargar los envíos');
    } finally {
      setLoading(false);
    }
  };

  // Filtrar envíos basado en los criterios de búsqueda
  const enviosFiltrados = envios.filter(envio => {
    // Filtro por estado
    if (filtroEstado && envio.estado_actual !== filtroEstado) {
      return false;
    }

    // Filtro por término de búsqueda
    if (searchTerm) {
      const term = searchTerm.toLowerCase();

      switch (tipoBusqueda) {
        case 'remitente':
          return envio.remitente_nombre?.toLowerCase().includes(term);
        case 'destinatario':
          return envio.destinatario_nombre?.toLowerCase().includes(term);
        case 'guia':
          return envio.numero_guia?.toLowerCase().includes(term);
        case 'todos':
        default:
          return (
            envio.numero_guia?.toLowerCase().includes(term) ||
            envio.remitente_nombre?.toLowerCase().includes(term) ||
            envio.destinatario_nombre?.toLowerCase().includes(term) ||
            envio.descripcion?.toLowerCase().includes(term)
          );
      }
    }

    return true;
  });

  // Función para obtener el color del estado
  const getEstadoColor = (estado: string) => {
    switch (estado) {
      case 'RECIBIDO': return 'text-primary';
      case 'EN_TRANSITO': return 'text-warning';
      case 'EN_REPARTO': return 'text-warning';
      case 'ENTREGADO': return 'text-success';
      case 'DEVUELTO': return 'text-error';
      case 'CANCELADO': return 'text-error';
      default: return 'text-secondary';
    }
  };

  // Función para obtener el ícono del estado
  const getEstadoIcon = (estado: string) => {
    const estadoObj = estadosDisponibles.find(e => e.value === estado);
    return estadoObj?.icon || '📦';
  };

  // Función para formatear fecha
  const formatearFecha = (fecha: string) => {
    try {
      return new Date(fecha).toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      });
    } catch {
      return 'N/A';
    }
  };

  // Calcular estadísticas
  const estadisticas = {
    total: envios.length,
    recibidos: envios.filter(e => e.estado_actual === 'RECIBIDO').length,
    enTransito: envios.filter(e => e.estado_actual === 'EN_TRANSITO').length,
    entregados: envios.filter(e => e.estado_actual === 'ENTREGADO').length
  };

  // Función para eliminar envío
  const eliminarEnvio = async (id: string) => {
    if (!window.confirm('¿Estás seguro de que quieres eliminar este envío?')) {
      return;
    }

    try {
      await enviosAPI.delete(parseInt(id));
      await cargarEnvios(); // Recargar la lista
      console.log('✅ Envío eliminado exitosamente');
    } catch (err: any) {
      console.error('❌ Error al eliminar envío:', err);
      setError(err?.response?.data?.detail || 'Error al eliminar el envío');
    }
  };

  // Vista de carga
  if (loading) {
    return (
      <div className="page-container gestion-page">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <h2>Cargando envíos...</h2>
          <p>Por favor espere un momento</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container gestion-page">
      {/* Header de la página */}
      <div className="page-header">
        <div>
          <h1 className="page-title">📦 Gestión de Envíos</h1>
          <p className="page-subtitle">
            Administra todos los envíos del sistema desde un solo lugar
          </p>
        </div>
        <div className="page-actions">
          <button
            onClick={cargarEnvios}
            className="btn btn-secondary"
            disabled={loading}
          >
            🔄 Refrescar
          </button>
          <Link to="/envios/nuevo" className="btn btn-primary">
            ➕ Nuevo Envío
          </Link>
        </div>
      </div>

      {/* Estadísticas generales */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-title">Total Envíos</span>
            <span className="stat-icon">📦</span>
          </div>
          <div className="stat-value">{estadisticas.total}</div>
        </div>

        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-title">Recibidos</span>
            <span className="stat-icon">📥</span>
          </div>
          <div className="stat-value text-primary">{estadisticas.recibidos}</div>
        </div>

        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-title">En Tránsito</span>
            <span className="stat-icon">🚚</span>
          </div>
          <div className="stat-value text-warning">{estadisticas.enTransito}</div>
        </div>

        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-title">Entregados</span>
            <span className="stat-icon">✅</span>
          </div>
          <div className="stat-value text-success">{estadisticas.entregados}</div>
        </div>
      </div>

      {/* Alertas */}
      {error && (
        <div className="alert alert-error">
          <span>{error}</span>
          <button
            className="close-button"
            onClick={() => setError(null)}
          >
            ✕
          </button>
        </div>
      )}

      {/* Filtros y búsqueda */}
      <div className="filters-container">
        <div className="filters-row">
          <div className="form-group">
            <label className="form-label">🔍 Buscar en:</label>
            <select
              value={tipoBusqueda}
              onChange={(e) => setTipoBusqueda(e.target.value as any)}
              className="form-control"
              title="Seleccionar tipo de búsqueda"
            >
              <option value="todos">Todos los campos</option>
              <option value="guia">Número de guía</option>
              <option value="remitente">Remitente</option>
              <option value="destinatario">Destinatario</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Término de búsqueda:</label>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Escribe para buscar..."
              className="search-input"
            />
          </div>

          <div className="form-group">
            <label className="form-label">📊 Estado:</label>
            <select
              value={filtroEstado}
              onChange={(e) => setFiltroEstado(e.target.value)}
              className="form-control"
              title="Seleccionar estado"
            >
              {estadosDisponibles.map(estado => (
                <option key={estado.value} value={estado.value}>
                  {estado.icon} {estado.label}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">&nbsp;</label>
            <button
              onClick={() => {
                setSearchTerm('');
                setFiltroEstado('');
                setTipoBusqueda('todos');
              }}
              className="btn btn-secondary w-full"
            >
              🗑️ Limpiar Filtros
            </button>
          </div>
        </div>
      </div>

      {/* Tabla de envíos */}
      <div className="table-container">
        {enviosFiltrados.length === 0 ? (
          <div className="no-data">
            {envios.length === 0 ? (
              <>
                <h3>😔 No hay envíos registrados</h3>
                <p>Comienza creando tu primer envío haciendo clic en "Nuevo Envío"</p>
                <Link to="/envios/nuevo" className="btn btn-primary mt-3">
                  ➕ Crear Primer Envío
                </Link>
              </>
            ) : (
              <>
                <h3>🔍 No se encontraron envíos</h3>
                <p>Intenta cambiar los filtros de búsqueda</p>
              </>
            )}
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Número Guía</th>
                <th>Remitente</th>
                <th>Destinatario</th>
                <th>Estado</th>
                <th>Fecha Creación</th>
                <th>Peso</th>
                <th>Valor</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {enviosFiltrados.map((envio) => (
                <tr key={envio.id}>
                  <td>
                    <strong>{envio.numero_guia}</strong>
                  </td>
                  <td>
                    <div>
                      <strong>{envio.remitente_nombre}</strong>
                      <br />
                      <small>{envio.remitente_telefono}</small>
                    </div>
                  </td>
                  <td>
                    <div>
                      <strong>{envio.destinatario_nombre}</strong>
                      <br />
                      <small>{envio.destinatario_telefono}</small>
                    </div>
                  </td>
                  <td>
                    <span className={getEstadoColor(envio.estado_actual)}>
                      {getEstadoIcon(envio.estado_actual)} {envio.estado_actual}
                    </span>
                  </td>
                  <td>{formatearFecha(envio.fecha_creacion)}</td>
                  <td>{envio.peso} kg</td>
                  <td>${envio.valor_declarado}</td>
                  <td>
                    <div className="action-buttons">
                      <Link
                        to={`/envios/${envio.id}`}
                        className="btn btn-sm btn-primary"
                        title="Ver detalles"
                      >
                        👁️
                      </Link>
                      <Link
                        to={`/envios/${envio.id}/editar`}
                        className="btn btn-sm btn-warning"
                        title="Editar"
                      >
                        ✏️
                      </Link>
                      <button
                        onClick={() => eliminarEnvio(envio.id)}
                        className="btn btn-sm btn-danger"
                        title="Eliminar"
                      >
                        🗑️
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Resumen de resultados */}
      {enviosFiltrados.length > 0 && (
        <div className="card">
          <div className="card-body text-center">
            <p>
              <strong>📊 Mostrando {enviosFiltrados.length} de {envios.length} envíos</strong>
              {searchTerm && (
                <span> · Búsqueda: "{searchTerm}"</span>
              )}
              {filtroEstado && (
                <span> · Estado: {estadosDisponibles.find(e => e.value === filtroEstado)?.label}</span>
              )}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default GestionUnificada;
