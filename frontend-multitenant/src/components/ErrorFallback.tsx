// Componente de seguridad para manejar errores en tiempo de ejecución
import React from 'react';

interface ErrorFallbackProps {
  error?: Error;
  resetErrorBoundary?: () => void;
}

const ErrorFallback: React.FC<ErrorFallbackProps> = ({ error, resetErrorBoundary }) => {  // Función para recargar la página completamente
  const handleRefreshPage = () => {
    const win = window as Window;
    win.location.reload();
  };// Función para limpiar el caché y recargar
  const handleClearCacheAndRefresh = () => {
    if ('caches' in window) {
      caches.keys().then((keyList) => {
        return Promise.all(
          keyList.map((key) => {
            return caches.delete(key);
          })
        );
      }).then(() => {
        console.log('Caché limpiado');
        const win = window as Window;
        win.location.reload();
      });
    } else {
      // Fallback si la API de Cache no está disponible
      const win = window as Window;
      win.location.reload();
    }
  };

  return (
    <div className="error-fallback">
      <div className="error-icon">⚠️</div>
      <h2>Algo salió mal</h2>
      
      {error && (
        <div className="error-details">
          <p>Error: {error.message}</p>
          {error.stack && (
            <details>
              <summary>Detalles técnicos</summary>
              <pre>{error.stack}</pre>
            </details>
          )}
        </div>
      )}
      
      <div className="error-actions">
        <button 
          onClick={resetErrorBoundary || handleRefreshPage} 
          className="btn"
        >
          Intentar de nuevo
        </button>
        <button 
          onClick={handleClearCacheAndRefresh} 
          className="btn btn-secondary"
        >
          Limpiar caché y recargar
        </button>
          {/* Botón específico para el problema de página en blanco después de crear envío */}
        <button 
          onClick={() => {
            // Limpiar cualquier estado problemático
            sessionStorage.removeItem('_lastEnvioSuccess');
            // Navegar manualmente al dashboard
            const win = window as Window;
            win.location.href = '/dashboard?reload=true';
          }} 
          className="btn btn-outline"
          title="Usar si ves una página en blanco después de crear un envío"
        >
          Volver al Dashboard
        </button>
      </div>
      
      <div className="error-help">
        <p>Si el problema persiste:</p>
        <ol>
          <li>Intenta abrir la aplicación en una ventana de incógnito</li>
          <li>Presiona Ctrl+F5 para recargar sin usar caché</li>
          <li>Contacta al soporte técnico</li>
        </ol>
      </div>
    </div>
  );
};

export default ErrorFallback;
