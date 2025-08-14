import React from 'react';
import { useNavigate } from 'react-router-dom';

// 🇨🇺 SELECTOR DE MODO UNIFICADO - Sin Tailwind, con CSS Master

const ModeSelector: React.FC = () => {
  const navigate = useNavigate();

  const modes = [
    {
      id: 'simple',
      title: 'Modo Simple',
      subtitle: 'Gratis • Rápido • Fácil',
      description: 'Formulario básico para envíos estándar. Perfecto para uso diario y personal.',
      icon: '📦',
      features: [
        'Formulario simplificado',
        'Campos esenciales únicamente',
        'Proceso rápido de 3 pasos',
        'Interfaz limpia y amigable'
      ],
      route: '/envios/simple',
      className: 'border-primary'
    },
    {
      id: 'premium',
      title: 'Modo Premium',
      subtitle: 'Completo • Avanzado • Profesional',
      description: 'Formulario completo con todas las funciones avanzadas para uso comercial.',
      icon: '⭐',
      features: [
        'Captura de fotos HD',
        'Códigos QR y etiquetas',
        'Servicios adicionales',
        'Análisis detallado de precios'
      ],
      route: '/envios/premium',
      className: 'border-warning'
    }
  ];

  const handleModeSelect = (route: string) => {
    navigate(route);
  };

  return (
    <div className="page-container">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">🚀 Crear Nuevo Envío</h1>
          <p className="page-subtitle">
            Selecciona el modo que mejor se adapte a tus necesidades
          </p>
        </div>
        <div className="page-actions">
          <button
            onClick={() => navigate('/dashboard')}
            className="btn btn-secondary"
          >
            🔙 Volver al Dashboard
          </button>
        </div>
      </div>

      {/* Información destacada */}
      <div className="alert alert-info mb-4">
        <span>
          <strong>💡 Consejo</strong><br />
          Para envíos personales usa el <strong>Modo Simple</strong>. Para empresas o envíos complejos, elige <strong>Modo Premium</strong>.
        </span>
      </div>

      {/* Selector de modos */}
      <div className="form-container">
        <div className="mode-selector-grid">
          {modes.map((mode) => (
            <div
              key={mode.id}
              className={`mode-card ${mode.className}`}
              onClick={() => handleModeSelect(mode.route)}
            >
              {/* Header del modo */}
              <div className="mode-card-header">
                <div className="mode-icon">{mode.icon}</div>
                <div className="mode-info">
                  <h3 className="mode-title">{mode.title}</h3>
                  <p className="mode-subtitle">{mode.subtitle}</p>
                </div>
              </div>

              {/* Descripción */}
              <p className="mode-description">{mode.description}</p>

              {/* Características */}
              <div className="mode-features">
                <h4 className="mode-features-title">✨ Características:</h4>
                <ul className="mode-features-list">
                  {mode.features.map((feature, index) => (
                    <li key={index} className="mode-feature">
                      <span className="feature-icon">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Botón de acción */}
              <div className="mode-card-footer">
                <button className={`btn ${mode.id === 'simple' ? 'btn-primary' : 'btn-warning'} btn-lg mode-button`}>
                  {mode.id === 'simple' ? '📦 Usar Modo Simple' : '⭐ Usar Modo Premium'}
                  <span className="ml-2">→</span>
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Comparación rápida */}
        <div className="card mt-6">
          <div className="card-header">
            <h3 className="card-title">📊 Comparación Rápida</h3>
          </div>
          <div className="card-body">
            <div className="comparison-table">
              <div className="comparison-row">
                <div className="comparison-feature">Características</div>
                <div className="comparison-simple">📦 Simple</div>
                <div className="comparison-premium">⭐ Premium</div>
              </div>
              <div className="comparison-row">
                <div className="comparison-feature">Tiempo de proceso</div>
                <div className="comparison-simple text-success">✓ 3 minutos</div>
                <div className="comparison-premium text-warning">~ 10 minutos</div>
              </div>
              <div className="comparison-row">
                <div className="comparison-feature">Fotos del paquete</div>
                <div className="comparison-simple text-muted">✗ No disponible</div>
                <div className="comparison-premium text-success">✓ Incluido</div>
              </div>
              <div className="comparison-row">
                <div className="comparison-feature">Servicios adicionales</div>
                <div className="comparison-simple text-muted">✗ Básicos</div>
                <div className="comparison-premium text-success">✓ Completos</div>
              </div>
              <div className="comparison-row">
                <div className="comparison-feature">Gestión aduanal</div>
                <div className="comparison-simple text-muted">✗ No incluida</div>
                <div className="comparison-premium text-success">✓ Disponible</div>
              </div>
              <div className="comparison-row">
                <div className="comparison-feature">Ideal para</div>
                <div className="comparison-simple">Uso personal</div>
                <div className="comparison-premium">Uso comercial</div>
              </div>
            </div>
          </div>
        </div>

        {/* Acciones adicionales */}
        <div className="d-flex gap-3 justify-center mt-4">
          <button
            onClick={() => navigate('/gestion')}
            className="btn btn-info"
          >
            📋 Ver Envíos Existentes
          </button>
          <button
            onClick={() => navigate('/rastrear')}
            className="btn btn-secondary"
          >
            🔍 Rastrear Envío
          </button>
        </div>
      </div>
    </div>
  );
};

export default ModeSelector;
