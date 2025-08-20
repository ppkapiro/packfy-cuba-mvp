import { useTenant, usePermissions } from '../../contexts/TenantContext';
import './TenantInfo.css';

const TenantInfo = () => {
  const { empresaActual, perfilActual, isLoading } = useTenant();
  const { rol, esAdmin, puede } = usePermissions();

  if (isLoading) {
    return (
      <div className="tenant-info loading">
        <div className="loading-spinner"></div>
        <span>Cargando información de empresa...</span>
      </div>
    );
  }

  if (!empresaActual || !perfilActual) {
    return (
      <div className="tenant-info error">
        <span className="error-icon">⚠️</span>
        <span>No se pudo cargar la información de la empresa</span>
      </div>
    );
  }

  // Traducir roles al español
  const rolesEspanol = {
    'dueno': 'Dueño',
    'operador_miami': 'Operador Miami',
    'operador_cuba': 'Operador Cuba',
    'remitente': 'Remitente',
    'destinatario': 'Destinatario'
  };

  // Iconos por rol
  const iconosRol = {
    'dueno': '👑',
    'operador_miami': '🏢',
    'operador_cuba': '🏝️',
    'remitente': '📦',
    'destinatario': '📬'
  };

  // Permisos del rol actual
  const permisosDisponibles = [
    { accion: 'crear_envio', nombre: 'Crear Envíos', disponible: puede('crear_envio') },
    { accion: 'editar_envio', nombre: 'Editar Envíos', disponible: puede('editar_envio') },
    { accion: 'cambiar_estado', nombre: 'Cambiar Estados', disponible: puede('cambiar_estado') },
    { accion: 'ver_reportes', nombre: 'Ver Reportes', disponible: puede('ver_reportes') },
  ];

  return (
    <div className="tenant-info">
      <div className="tenant-info-header">
        <h3>
          <span className="header-icon">🏢</span>
          Información de Empresa
        </h3>
      </div>

      <div className="tenant-info-content">
        {/* Información de la empresa */}
        <div className="empresa-card">
          <div className="empresa-header">
            <h4>{empresaActual.nombre}</h4>
            <span className="empresa-slug">{empresaActual.slug}</span>
          </div>
          {empresaActual.descripcion && (
            <p className="empresa-descripcion">{empresaActual.descripcion}</p>
          )}
          <div className="empresa-meta">
            <span className="meta-item">
              <strong>Activa desde:</strong> {new Date(empresaActual.fecha_creacion).toLocaleDateString()}
            </span>
          </div>
        </div>

        {/* Información del perfil */}
        <div className="perfil-card">
          <div className="perfil-header">
            <span className="rol-icon">{iconosRol[rol as keyof typeof iconosRol]}</span>
            <div className="perfil-details">
              <h4>Tu Rol</h4>
              <span className="rol-nombre">{rolesEspanol[rol as keyof typeof rolesEspanol]}</span>
              {esAdmin() && <span className="admin-badge">Administrador</span>}
            </div>
          </div>
          <div className="perfil-meta">
            <span className="meta-item">
              <strong>Miembro desde:</strong> {new Date(perfilActual.fecha_ingreso).toLocaleDateString()}
            </span>
          </div>
        </div>

        {/* Permisos disponibles */}
        <div className="permisos-card">
          <h4>
            <span className="permisos-icon">🔑</span>
            Permisos Disponibles
          </h4>
          <div className="permisos-grid">
            {permisosDisponibles.map((permiso) => (
              <div
                key={permiso.accion}
                className={`permiso-item ${permiso.disponible ? 'disponible' : 'no-disponible'}`}
              >
                <span className="permiso-status">
                  {permiso.disponible ? '✅' : '❌'}
                </span>
                <span className="permiso-nombre">{permiso.nombre}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TenantInfo;
