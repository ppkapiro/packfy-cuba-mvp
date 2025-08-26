import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import '../../styles/configuracion-admin.css';

interface ConfiguracionEmpresa {
  id: number;
  nombre: string;
  slug: string;
  direccion: string;
  telefono: string;
  email: string;
  logo_url?: string;
  configuraciones: {
    precio_base: number;
    precio_por_kg: number;
    peso_maximo: number;
    zona_cobertura: string[];
    horario_operacion: string;
    notificaciones_email: boolean;
    notificaciones_sms: boolean;
  };
}

interface ConfiguracionSistema {
  version: string;
  modo_mantenimiento: boolean;
  max_usuarios: number;
  backup_automatico: boolean;
  logs_detallados: boolean;
}

const ConfiguracionAdmin: React.FC = () => {
  const [empresa, setEmpresa] = useState<ConfiguracionEmpresa | null>(null);
  const [sistema, setSistema] = useState<ConfiguracionSistema>({
    version: '3.0.0',
    modo_mantenimiento: false,
    max_usuarios: 100,
    backup_automatico: true,
    logs_detallados: false
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'empresa' | 'sistema' | 'usuarios' | 'seguridad'>('empresa');
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    loadConfiguracion();
  }, []);

  const loadConfiguracion = async () => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await api.get('/empresas/mi_empresa/');
      setEmpresa(response.data as ConfiguracionEmpresa);
    } catch (error) {
      console.error('Error cargando configuración:', error);
      setError('Error al cargar la configuración');
    } finally {
      setIsLoading(false);
    }
  };

  const guardarConfiguracion = async () => {
    if (!empresa) return;

    try {
      setIsSaving(true);
      await api.put(`/empresas/${empresa.id}/`, empresa);
      // Mostrar notificación de éxito
      alert('Configuración guardada exitosamente');
    } catch (error) {
      console.error('Error guardando configuración:', error);
      alert('Error al guardar la configuración');
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="configuracion-admin loading">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Cargando configuración...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="configuracion-admin error">
        <div className="error-container">
          <h2>Error al cargar configuración</h2>
          <p>{error}</p>
          <button onClick={loadConfiguracion} className="retry-button">
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="configuracion-admin">
      {/* Header de la página */}
      <div className="page-header">
        <div className="header-content">
          <h1>Configuración del Sistema</h1>
          <p>Administra la configuración de la empresa y el sistema</p>
        </div>
        <div className="header-actions">
          <button
            className="btn btn-primary"
            onClick={guardarConfiguracion}
            disabled={isSaving}
          >
            {isSaving ? 'Guardando...' : 'Guardar Cambios'}
          </button>
        </div>
      </div>

      {/* Tabs de navegación */}
      <div className="config-tabs">
        <button
          className={`tab ${activeTab === 'empresa' ? 'active' : ''}`}
          onClick={() => setActiveTab('empresa')}
        >
          Empresa
        </button>
        <button
          className={`tab ${activeTab === 'sistema' ? 'active' : ''}`}
          onClick={() => setActiveTab('sistema')}
        >
          Sistema
        </button>
        <button
          className={`tab ${activeTab === 'usuarios' ? 'active' : ''}`}
          onClick={() => setActiveTab('usuarios')}
        >
          Usuarios
        </button>
        <button
          className={`tab ${activeTab === 'seguridad' ? 'active' : ''}`}
          onClick={() => setActiveTab('seguridad')}
        >
          Seguridad
        </button>
      </div>

      {/* Contenido según tab activa */}
      <div className="config-content">
        {activeTab === 'empresa' && empresa && (
          <div className="config-section">
            <h2>Configuración de la Empresa</h2>

            <div className="config-form">
              <div className="form-group">
                <label htmlFor="empresa-nombre">Nombre de la Empresa</label>
                <input
                  id="empresa-nombre"
                  type="text"
                  value={empresa.nombre}
                  onChange={(e) => setEmpresa({...empresa, nombre: e.target.value})}
                  className="form-input"
                  placeholder="Ingrese el nombre de la empresa"
                  title="Nombre de la empresa"
                />
              </div>

              <div className="form-group">
                <label htmlFor="empresa-slug">Slug de la Empresa</label>
                <input
                  id="empresa-slug"
                  type="text"
                  value={empresa.slug}
                  onChange={(e) => setEmpresa({...empresa, slug: e.target.value})}
                  className="form-input"
                  placeholder="ej: mi-empresa"
                  title="Identificador único de la empresa"
                />
              </div>

              <div className="form-group">
                <label htmlFor="empresa-direccion">Dirección</label>
                <textarea
                  id="empresa-direccion"
                  value={empresa.direccion}
                  onChange={(e) => setEmpresa({...empresa, direccion: e.target.value})}
                  className="form-textarea"
                  rows={3}
                  placeholder="Dirección completa de la empresa"
                  title="Dirección de la empresa"
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="empresa-telefono">Teléfono</label>
                  <input
                    id="empresa-telefono"
                    type="text"
                    value={empresa.telefono}
                    onChange={(e) => setEmpresa({...empresa, telefono: e.target.value})}
                    className="form-input"
                    placeholder="Número de teléfono"
                    title="Teléfono de contacto de la empresa"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="empresa-email">Email</label>
                  <input
                    id="empresa-email"
                    type="email"
                    value={empresa.email}
                    onChange={(e) => setEmpresa({...empresa, email: e.target.value})}
                    className="form-input"
                    placeholder="email@empresa.com"
                    title="Email de contacto de la empresa"
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'sistema' && (
          <div className="config-section">
            <h2>Configuración del Sistema</h2>

            <div className="config-form">
              <div className="form-group">
                <label htmlFor="sistema-version">Versión del Sistema</label>
                <input
                  id="sistema-version"
                  type="text"
                  value={sistema.version}
                  disabled
                  className="form-input disabled"
                  title="Versión actual del sistema"
                  placeholder="Versión del sistema"
                />
              </div>

              <div className="form-group">
                <label htmlFor="sistema-max-usuarios">Máximo de Usuarios</label>
                <input
                  id="sistema-max-usuarios"
                  type="number"
                  value={sistema.max_usuarios}
                  onChange={(e) => setSistema({...sistema, max_usuarios: parseInt(e.target.value)})}
                  className="form-input"
                  title="Número máximo de usuarios permitidos"
                  placeholder="Ej: 100"
                />
              </div>

              <div className="form-switches">
                <div className="switch-group">
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={sistema.modo_mantenimiento}
                      onChange={(e) => setSistema({...sistema, modo_mantenimiento: e.target.checked})}
                      title="Activar modo de mantenimiento del sistema"
                      aria-label="Modo Mantenimiento"
                    />
                    <span className="slider"></span>
                  </label>
                  <span>Modo Mantenimiento</span>
                </div>

                <div className="switch-group">
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={sistema.backup_automatico}
                      onChange={(e) => setSistema({...sistema, backup_automatico: e.target.checked})}
                      title="Activar backups automáticos del sistema"
                      aria-label="Backup Automático"
                    />
                    <span className="slider"></span>
                  </label>
                  <span>Backup Automático</span>
                </div>

                <div className="switch-group">
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={sistema.logs_detallados}
                      onChange={(e) => setSistema({...sistema, logs_detallados: e.target.checked})}
                      title="Activar logs detallados del sistema"
                      aria-label="Logs Detallados"
                    />
                    <span className="slider"></span>
                  </label>
                  <span>Logs Detallados</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'usuarios' && (
          <div className="config-section">
            <h2>Configuración de Usuarios</h2>

            <div className="config-form">
              <div className="info-cards">
                <div className="info-card">
                  <h3>Registro de Usuarios</h3>
                  <p>Permitir que nuevos usuarios se registren automáticamente</p>
                  <label className="switch">
                    <input
                      type="checkbox"
                      defaultChecked
                      title="Permitir registro automático de usuarios"
                      aria-label="Permitir registro de usuarios"
                    />
                    <span className="slider"></span>
                  </label>
                </div>

                <div className="info-card">
                  <h3>Verificación de Email</h3>
                  <p>Requerir verificación de email para nuevos usuarios</p>
                  <label className="switch">
                    <input
                      type="checkbox"
                      defaultChecked
                      title="Requerir verificación de email"
                      aria-label="Verificación de email obligatoria"
                    />
                    <span className="slider"></span>
                  </label>
                </div>

                <div className="info-card">
                  <h3>Roles por Defecto</h3>
                  <p>Rol asignado automáticamente a nuevos usuarios</p>
                  <label htmlFor="rol-defecto" className="sr-only">Rol por defecto</label>
                  <select
                    id="rol-defecto"
                    className="form-select"
                    title="Seleccionar rol por defecto para nuevos usuarios"
                    aria-label="Rol por defecto para nuevos usuarios"
                  >
                    <option value="cliente">Cliente</option>
                    <option value="empleado">Empleado</option>
                    <option value="admin">Administrador</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'seguridad' && (
          <div className="config-section">
            <h2>Configuración de Seguridad</h2>

            <div className="config-form">
              <div className="security-options">
                <div className="security-card">
                  <h3>Autenticación de Dos Factores</h3>
                  <p>Habilitar 2FA para todos los usuarios administradores</p>
                  <label className="switch">
                    <input
                      type="checkbox"
                      title="Activar/desactivar autenticación de dos factores"
                      aria-label="Autenticación de dos factores"
                    />
                    <span className="slider"></span>
                  </label>
                </div>

                <div className="security-card">
                  <h3>Tiempo de Sesión</h3>
                  <p>Duración máxima de las sesiones de usuario</p>
                  <label htmlFor="tiempo-sesion" className="sr-only">Tiempo de sesión</label>
                  <select
                    id="tiempo-sesion"
                    className="form-select"
                    title="Seleccionar duración máxima de sesión"
                    aria-label="Duración máxima de sesión"
                  >
                    <option value="1h">1 Hora</option>
                    <option value="8h">8 Horas</option>
                    <option value="24h">24 Horas</option>
                    <option value="7d">7 Días</option>
                  </select>
                </div>

                <div className="security-card">
                  <h3>Bloqueo por Intentos</h3>
                  <p>Bloquear cuenta después de intentos fallidos</p>
                  <label htmlFor="intentos-bloqueo" className="sr-only">Número de intentos antes del bloqueo</label>
                  <input
                    id="intentos-bloqueo"
                    type="number"
                    defaultValue="5"
                    className="form-input small"
                    title="Número de intentos fallidos antes del bloqueo"
                    placeholder="5"
                    aria-label="Intentos antes del bloqueo"
                  />
                  <span> intentos</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ConfiguracionAdmin;
