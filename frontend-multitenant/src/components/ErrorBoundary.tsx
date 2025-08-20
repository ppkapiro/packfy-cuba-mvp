import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null
    };
  }

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    console.error('ErrorBoundary capturó un error:', error);
    console.error('Información del error:', errorInfo);
    
    // Aquí podrías enviar el error a un servicio de monitoreo
  }

  render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }
      
      return (
        <div className="error-boundary">
          <h2>Ha ocurrido un error inesperado</h2>
          <p>Lo sentimos, ha ocurrido un problema al cargar esta página.</p>          <details>
            <summary>Detalles del error</summary>
            <p>{this.state.error?.message}</p>
          </details>
          <button 
            onClick={() => {
              const win = window as Window;
              win.location.reload();
            }}
            className="btn-retry"
          >
            Intentar de nuevo
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
