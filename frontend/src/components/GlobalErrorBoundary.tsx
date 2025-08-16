import { Component, ErrorInfo, ReactNode } from 'react';

// Extender Window para gtag
declare global {
  interface Window {
    gtag?: (...args: any[]) => void;
  }
}

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error?: Error;
  errorInfo?: ErrorInfo;
}

class GlobalErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log estructurado del error
    console.error('🚨 Error Boundary capturó un error:', {
      error: error.message,
      stack: error.stack,
      component: errorInfo.componentStack,
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      url: window.location.href
    });

    // Enviar a servicio de monitoreo (Sentry, etc.)
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }

    // Opcional: Enviar a analytics
    if (window.gtag) {
      window.gtag('event', 'exception', {
        description: error.message,
        fatal: false
      });
    }

    this.setState({ error, errorInfo });
  }

  handleReload = () => {
    window.location.reload();
  };

  handleGoHome = () => {
    window.location.href = '/dashboard';
  };

  render() {
    if (this.state.hasError) {
      // Fallback UI personalizado
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="error-boundary-container">
          <div className="error-boundary-content">
            <div className="error-icon">⚠️</div>

            <h1 className="error-title">
              ¡Oops! Algo salió mal
            </h1>

            <p className="error-message">
              Se produjo un error inesperado. Nuestro equipo ha sido notificado y trabajamos para solucionarlo.
            </p>

            <div className="error-actions">
              <button
                onClick={this.handleReload}
                className="btn btn-primary"
              >
                🔄 Recargar Página
              </button>

              <button
                onClick={this.handleGoHome}
                className="btn btn-secondary"
              >
                🏠 Ir al Dashboard
              </button>
            </div>

            {/* Información técnica solo en desarrollo */}
            {import.meta.env.DEV && this.state.error && (
              <details className="error-details">
                <summary>Información técnica (solo desarrollo)</summary>
                <pre className="error-stack">
                  {this.state.error.message}
                  {'\n\n'}
                  {this.state.error.stack}
                  {'\n\n'}
                  {this.state.errorInfo?.componentStack}
                </pre>
              </details>
            )}
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default GlobalErrorBoundary;
