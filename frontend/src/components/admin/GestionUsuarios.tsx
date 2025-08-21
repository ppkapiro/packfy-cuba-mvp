import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import '../../styles/gestion-usuarios.css';

interface Usuario {
  id: number;
  email: string;
  nombre: string;
  apellidos: string;
  telefono: string;
  is_active: boolean;
  date_joined: string;
}

const GestionUsuarios: React.FC = () => {
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadUsuarios();
  }, []);

  const loadUsuarios = async () => {
    try {
      setIsLoading(true);
      setError(null);
      console.log('🔍 Cargando usuarios...');

      const response = await api.get('/usuarios/');
      console.log('📡 Respuesta API usuarios:', response);

      const data = response.data as any;
      const usuariosList = data?.results || data || [];
      console.log('👥 Usuarios obtenidos:', usuariosList.length, 'usuarios');

      setUsuarios(usuariosList);
    } catch (error) {
      console.error('❌ Error cargando usuarios:', error);
      setError('Error al cargar la lista de usuarios. Verifica la conexión con el servidor.');
    } finally {
      setIsLoading(false);
    }
  };

  console.log('🎯 GestionUsuarios render - isLoading:', isLoading, 'error:', error, 'usuarios:', usuarios.length);

  if (isLoading) {
    return (
      <div className="gestion-usuarios loading">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Cargando usuarios...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="gestion-usuarios error">
        <div className="error-container">
          <h2>❌ Error al cargar usuarios</h2>
          <p>{error}</p>
          <button onClick={loadUsuarios} className="retry-button">
            🔄 Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="gestion-usuarios">
      {/* Header de la página */}
      <div className="page-header">
        <div className="header-content">
          <h1>👥 Gestión de Usuarios</h1>
          <p>Administra todos los usuarios de la empresa</p>
        </div>
        <div className="header-actions">
          <button className="btn btn-primary">
            ➕ Agregar Usuario
          </button>
        </div>
      </div>

      {/* Stats rápidas */}
      <div className="usuarios-stats">
        <div className="stat-card">
          <h3>Total Usuarios</h3>
          <span className="stat-number">{usuarios.length}</span>
        </div>
        <div className="stat-card">
          <h3>Usuarios Activos</h3>
          <span className="stat-number">
            {usuarios.filter(u => u.is_active).length}
          </span>
        </div>
        <div className="stat-card">
          <h3>Usuarios Inactivos</h3>
          <span className="stat-number">
            {usuarios.filter(u => !u.is_active).length}
          </span>
        </div>
      </div>

      {/* Lista de usuarios */}
      <div className="usuarios-list">
        <div className="list-header">
          <h2>📋 Lista de Usuarios</h2>
          <div className="list-filters">
            <input
              type="text"
              placeholder="🔍 Buscar usuarios..."
              className="search-input"
            />
            <select className="filter-select" title="Filtrar por estado">
              <option value="all">Todos los estados</option>
              <option value="active">Activos</option>
              <option value="inactive">Inactivos</option>
            </select>
          </div>
        </div>

        {usuarios.length > 0 ? (
          <div className="usuarios-table">
            <table>
              <thead>
                <tr>
                  <th>Usuario</th>
                  <th>Email</th>
                  <th>Teléfono</th>
                  <th>Estado</th>
                  <th>Registrado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {usuarios.map((usuario) => (
                  <tr key={usuario.id}>
                    <td>
                      <div className="usuario-info">
                        <div className="usuario-avatar">
                          {usuario.nombre?.charAt(0) || '?'}{usuario.apellidos?.charAt(0) || '?'}
                        </div>
                        <div className="usuario-details">
                          <span className="usuario-name">
                            {usuario.nombre || 'Sin nombre'} {usuario.apellidos || 'Sin apellidos'}
                          </span>
                        </div>
                      </div>
                    </td>
                    <td>{usuario.email}</td>
                    <td>{usuario.telefono || 'No especificado'}</td>
                    <td>
                      <span className={`status-badge ${usuario.is_active ? 'active' : 'inactive'}`}>
                        {usuario.is_active ? '✅ Activo' : '❌ Inactivo'}
                      </span>
                    </td>
                    <td>
                      {usuario.date_joined ? new Date(usuario.date_joined).toLocaleDateString() : 'No disponible'}
                    </td>
                    <td>
                      <div className="actions">
                        <button
                          className="btn-action view"
                          title="Ver detalles"
                          onClick={() => alert(`Ver detalles de ${usuario.nombre}`)}
                        >
                          👁️
                        </button>
                        <button
                          className="btn-action edit"
                          title="Editar"
                          onClick={() => alert(`Editar ${usuario.nombre}`)}
                        >
                          ✏️
                        </button>
                        <button
                          className={`btn-action ${usuario.is_active ? 'disable' : 'enable'}`}
                          title={usuario.is_active ? 'Desactivar' : 'Activar'}
                          onClick={() => alert(`${usuario.is_active ? 'Desactivar' : 'Activar'} ${usuario.nombre}`)}
                        >
                          {usuario.is_active ? '🚫' : '✅'}
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
            <h3>📭 No hay usuarios registrados</h3>
            <p>Todavía no se han registrado usuarios en el sistema.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default GestionUsuarios;
