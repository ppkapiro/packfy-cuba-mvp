import { useState } from 'react';
import { useTenant } from '../../contexts/TenantContext';
import './TenantSelector.css';

const TenantSelector = () => {
  const {
    empresaActual,
    empresasDisponibles,
    cambiarEmpresa,
    isLoading
  } = useTenant();

  const [isOpen, setIsOpen] = useState(false);
  const [isChanging, setIsChanging] = useState(false);

  const handleCambiarEmpresa = async (empresaSlug: string) => {
    if (empresaSlug === empresaActual?.slug) {
      setIsOpen(false);
      return;
    }

    try {
      setIsChanging(true);
      await cambiarEmpresa(empresaSlug);
      setIsOpen(false);
    } catch (error) {
      console.error('Error cambiando empresa:', error);
      // Aquí podrías mostrar un toast de error
    } finally {
      setIsChanging(false);
    }
  };

  if (isLoading || !empresaActual) {
    return (
      <div className="tenant-selector loading">
        <div className="loading-spinner"></div>
        <span>Cargando...</span>
      </div>
    );
  }

  return (
    <div className="tenant-selector">
      <button
        className={`tenant-button ${isOpen ? 'open' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        disabled={isChanging}
      >
        <div className="tenant-info">
          <span className="tenant-icon">🏢</span>
          <div className="tenant-details">
            <span className="tenant-name">{empresaActual.nombre}</span>
            <span className="tenant-role">Empresa Activa</span>
          </div>
        </div>
        <span className={`dropdown-arrow ${isOpen ? 'up' : 'down'}`}>
          {isChanging ? '⏳' : '▼'}
        </span>
      </button>

      {isOpen && (
        <div className="tenant-dropdown">
          <div className="dropdown-header">
            <span>Seleccionar Empresa</span>
          </div>
          <div className="dropdown-options">
            {empresasDisponibles.map((empresa) => (
              <button
                key={empresa.slug}
                className={`dropdown-option ${
                  empresa.slug === empresaActual.slug ? 'active' : ''
                }`}
                onClick={() => handleCambiarEmpresa(empresa.slug)}
                disabled={isChanging}
              >
                <div className="option-content">
                  <span className="option-icon">🏢</span>
                  <div className="option-details">
                    <span className="option-name">{empresa.nombre}</span>
                    <span className="option-slug">{empresa.slug}</span>
                  </div>
                  {empresa.slug === empresaActual.slug && (
                    <span className="active-indicator">✓</span>
                  )}
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Overlay para cerrar dropdown */}
      {isOpen && (
        <div
          className="dropdown-overlay"
          onClick={() => setIsOpen(false)}
        />
      )}
    </div>
  );
};

export default TenantSelector;
