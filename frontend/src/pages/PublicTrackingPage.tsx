import { useState } from 'react';
import { Link } from 'react-router-dom';
import { enviosAPI } from '../services/api';

interface EnvioPublico {
  numero_guia: string;
  estado: string;
  estado_display: string;
  remitente_nombre: string;
  destinatario_nombre: string;
  fecha_actualizacion: string;
  historial: Array<{
    estado: string;
    fecha: string;
    comentario?: string;
    ubicacion?: string;
  }>;
}

const PublicTrackingPage = () => {
  const [numeroGuia, setNumeroGuia] = useState('');
  const [envio, setEnvio] = useState<EnvioPublico | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!numeroGuia.trim()) return;

    setLoading(true);
    setError('');
    setEnvio(null);

    try {
      const response = await enviosAPI.rastrearPublico(numeroGuia);
      setEnvio(response.data);
    } catch (err: any) {
      setError(err.response?.data?.error || 'No se encontró ningún envío con ese número de guía');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="public-tracking-page">
      <header className="tracking-header">
        <div className="container">
          <div className="logo">
            <h1>Paquetería Cuba</h1>
          </div>
          <div className="auth-links">
            <Link to="/login">Iniciar Sesión</Link>
          </div>
        </div>
      </header>

      <main className="tracking-content">
        <div className="container">
          <div className="tracking-hero">
            <h2>Rastreo de Envíos</h2>
            <p>Consulta el estado de tus envíos en tiempo real</p>

            <div className="tracking-search">
              <form onSubmit={handleSubmit}>
                <div className="form-row">
                  <input
                    type="text"
                    value={numeroGuia}
                    onChange={(e) => setNumeroGuia(e.target.value)}
                    placeholder="Ingresa tu número de guía"
                    className="form-control"
                    disabled={loading}
                  />
                  <button
                    type="submit"
                    className="btn"
                    disabled={loading}
                  >
                    {loading ? 'Buscando...' : 'Rastrear'}
                  </button>
                </div>
              </form>
            </div>
          </div>

          {error && (
            <div className="tracking-result error">
              <div className="alert alert-error">{error}</div>
            </div>
          )}

          {envio && (
            <div className="tracking-result">
              <div className="tracking-summary">
                <h3>Envío #{envio.numero_guia}</h3>
                <div className="tracking-status">
                  <span className={`estado estado-${envio.estado}`}>
                    {envio.estado_display}
                  </span>
                </div>

                <div className="shipment-info">
                  <div className="info-item">
                    <span className="label">Remitente:</span>
                    <span className="value">{envio.remitente_nombre}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Destinatario:</span>
                    <span className="value">{envio.destinatario_nombre}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Última actualización:</span>
                    <span className="value">{new Date(envio.fecha_actualizacion).toLocaleDateString('es-ES', {
                      day: '2-digit',
                      month: '2-digit',
                      year: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}</span>
                  </div>
                </div>
              </div>

              <div className="tracking-history">
                <h4>Historial de rastreo</h4>
                <div className="timeline">
                  {envio.historial?.map((item, index) => (
                    <div key={index} className="timeline-item">
                      <div className="timeline-date">
                        {new Date(item.fecha).toLocaleDateString('es-ES', {
                          day: '2-digit',
                          month: '2-digit',
                          year: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </div>
                      <div className="timeline-content">
                        <div className="timeline-status">{item.estado}</div>
                        {item.ubicacion && <div className="timeline-location">{item.ubicacion}</div>}
                        {item.comentario && <div className="timeline-comment">{item.comentario}</div>}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      <footer className="tracking-footer">
        <div className="container">
          <p>&copy; {new Date().getFullYear()} Paquetería Cuba - Todos los derechos reservados</p>
        </div>
      </footer>
    </div>
  );
};

export default PublicTrackingPage;
