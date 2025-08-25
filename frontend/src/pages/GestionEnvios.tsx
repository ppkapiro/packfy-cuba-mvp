import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { api } from '../services/api';
import '../styles/gestion-envios.css';

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

const GestionEnvios: React.FC = () => {
  const [envios, setEnvios] = useState<Envio[]>([]);
  const [filteredEnvios, setFilteredEnvios] = useState<Envio[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');

  const navigate = useNavigate();
  const location = useLocation();

  // Detectar si estamos en contexto admin
  const isAdminContext = location.pathname.startsWith('/admin');

  const estadosDisponibles = [
    { value: 'all', label: 'Todos los estados' },
    { value: 'recibido', label: '📦 Recibido' },
    { value: 'en_transito', label: '🚚 En Tránsito' },
    { value: 'en_reparto', label: '🏃 En Reparto' },
    { value: 'entregado', label: '✅ Entregado' },
    { value: 'devuelto', label: '↩️ Devuelto' },
    { value: 'cancelado', label: '❌ Cancelado' }
  ];

  useEffect(() => {
    loadEnvios();
  }, []);

  useEffect(() => {
    filterEnvios();
  }, [envios, searchTerm, statusFilter]);

  const filterEnvios = () => {
    let filtered = envios;

    // Filtrar por búsqueda
    if (searchTerm) {
      filtered = filtered.filter(envio =>
        envio.numero_guia.toLowerCase().includes(searchTerm.toLowerCase()) ||
        envio.remitente_nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
        envio.destinatario_nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
        envio.descripcion.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filtrar por estado
    if (statusFilter !== 'all') {
      filtered = filtered.filter(envio =>
        envio.estado_actual.toLowerCase() === statusFilter.toLowerCase()
      );
    }

    setFilteredEnvios(filtered);
  };

  const loadEnvios = async () => {
    try {
      setIsLoading(true);
      setError(null);
      console.log('🔍 Cargando envíos...');

      const response = await api.get('/envios/');
      console.log('📡 Respuesta API envíos:', response);

      const data = response.data as any;
      const enviosList = data?.results || data || [];
      console.log('📦 Envíos obtenidos:', enviosList.length, 'envíos');

      setEnvios(enviosList);
    } catch (error) {
      console.error('❌ Error cargando envíos:', error);
      setError('Error al cargar la lista de envíos');
    } finally {
      setIsLoading(false);
    }
  };

  const eliminarEnvio = async (id: string, numeroGuia: string) => {
    if (!window.confirm(`¿Está seguro de eliminar el envío ${numeroGuia}?`)) {
      return;
    }

    try {
      await api.delete(`/envios/${id}/`);
      setEnvios(envios.filter(e => e.id !== id));
      alert(`Envío ${numeroGuia} eliminado correctamente`);
    } catch (error) {
      console.error('Error eliminando envío:', error);
      alert('Error al eliminar el envío');
    }
  };

  const formatearFecha = (fecha: string) => {
    return new Date(fecha).toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getEstadoClass = (estado: string) => {
    return estado.toLowerCase().replace('_', '');
  };

  console.log('🎯 GestionEnvios render - isLoading:', isLoading, 'error:', error, 'envíos:', envios.length);

  if (isLoading) {
    return (
      <div className="gestion-envios loading">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Cargando envíos...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="gestion-envios error">
        <div className="error-container">
          <h2>❌ Error al cargar envíos</h2>
          <p>{error}</p>
          <button onClick={loadEnvios} className="retry-button">
            🔄 Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="gestion-envios">
      {/* Header de la página */}
      <div className="page-header">
        <div className="header-content">
          <h1>📦 Gestión de Envíos</h1>
          <p>Administra todos los envíos de la empresa</p>
        </div>
        <div className="header-actions">
          <Link to={isAdminContext ? '/admin/envios/simple' : '/envios/nuevo'} className="btn btn-primary">
            ➕ Envío Simple
            <span className="badge badge-success">GRATIS</span>
          </Link>
          <Link to={isAdminContext ? '/admin/envios/premium' : '/envios/premium'} className="btn btn-premium">
            ⭐ Envío Premium
            <span className="badge badge-premium">$5 USD</span>
          </Link>
          <button onClick={loadEnvios} className="btn btn-secondary">
            🔄 Actualizar
          </button>
        </div>
      </div>

      {/* Stats rápidas */}
      <div className="envios-stats">
        <div className="stat-card">
          <h3>Total Envíos</h3>
          <span className="stat-number">{envios.length}</span>
        </div>
        <div className="stat-card">
          <h3>Entregados</h3>
          <span className="stat-number">
            {envios.filter(e => e.estado_actual.toLowerCase() === 'entregado').length}
          </span>
        </div>
        <div className="stat-card">
          <h3>En Proceso</h3>
          <span className="stat-number">
            {envios.filter(e => ['recibido', 'en_transito', 'en_reparto'].includes(e.estado_actual.toLowerCase())).length}
          </span>
        </div>
        <div className="stat-card">
          <h3>Cancelados</h3>
          <span className="stat-number">
            {envios.filter(e => e.estado_actual.toLowerCase() === 'cancelado').length}
          </span>
        </div>
      </div>

      {/* Lista de envíos */}
      <div className="envios-list">
        <div className="list-header">
          <h2>📋 Lista de Envíos</h2>
          <div className="list-filters">
            <input
              type="text"
              placeholder="🔍 Buscar por guía, remitente, destinatario..."
              className="search-input"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <select
              className="filter-select"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              title="Filtrar por estado"
            >
              {estadosDisponibles.map(estado => (
                <option key={estado.value} value={estado.value}>
                  {estado.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {filteredEnvios.length > 0 ? (
          <div className="envios-table">
            <table>
              <thead>
                <tr>
                  <th>Envío</th>
                  <th>Remitente</th>
                  <th>Destinatario</th>
                  <th>Estado</th>
                  <th>Peso</th>
                  <th>Fecha</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filteredEnvios.map((envio) => (
                  <tr key={envio.id}>
                    <td>
                      <div className="envio-info">
                        <div className="envio-icon">
                          {envio.numero_guia.slice(-3)}
                        </div>
                        <div className="envio-details">
                          <div className="envio-guia">#{envio.numero_guia}</div>
                          <div className="envio-descripcion">{envio.descripcion}</div>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div>
                        <div className="contact-name">{envio.remitente_nombre}</div>
                        <div className="contact-phone">{envio.remitente_telefono}</div>
                      </div>
                    </td>
                    <td>
                      <div>
                        <div className="contact-name">{envio.destinatario_nombre}</div>
                        <div className="contact-phone">{envio.destinatario_telefono}</div>
                      </div>
                    </td>
                    <td>
                      <span className={`status-badge ${getEstadoClass(envio.estado_actual)}`}>
                        {envio.estado_actual.replace('_', ' ')}
                      </span>
                    </td>
                    <td>{envio.peso} kg</td>
                    <td>{formatearFecha(envio.fecha_creacion)}</td>
                    <td>
                      <div className="actions">
                        <button
                          className="btn-action view"
                          title="Ver detalles"
                          onClick={() => navigate(`/envios/${envio.id}`)}
                        >
                          👁️
                        </button>
                        <button
                          className="btn-action edit"
                          title="Editar"
                          onClick={() => navigate(`/envios/${envio.id}/editar`)}
                        >
                          ✏️
                        </button>
                        <button
                          className="btn-action delete"
                          title="Eliminar"
                          onClick={() => eliminarEnvio(envio.id, envio.numero_guia)}
                        >
                          🗑️
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="no-data">
            {envios.length === 0 ? (
              <>
                <h3>📭 No hay envíos registrados</h3>
                <p>Todavía no se han creado envíos en el sistema.</p>
                <div className="create-buttons">
                  <Link to={isAdminContext ? '/admin/envios/simple' : '/envios/nuevo'} className="btn btn-primary">
                    ➕ Crear Envío Simple
                    <span className="badge badge-success">GRATIS</span>
                  </Link>
                  <Link to={isAdminContext ? '/admin/envios/premium' : '/envios/premium'} className="btn btn-premium">
                    ⭐ Crear Envío Premium
                    <span className="badge badge-premium">$5 USD</span>
                  </Link>
                </div>
              </>
            ) : (
              <>
                <h3>🔍 No se encontraron envíos</h3>
                <p>No hay envíos que coincidan con los filtros aplicados.</p>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default GestionEnvios;
