import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { publicAPI } from '../services/api';
import './TrackingPage.css';
import '../styles/mobile-optimized.css';

interface TrackingPublicResult {
  resultados: number;
  nombre_buscado: string;
  tipo_busqueda: string;
  envios: Array<{
    numero_guia: string;
    estado: string;
    estado_display: string;
    remitente_nombre: string;
    destinatario_nombre: string;
    fecha_creacion: string;
    fecha_actualizacion: string;
  }>;
}

const PublicTrackingPage: React.FC = () => {
  const [nombre, setNombre] = useState<string>('');
  const [tipoBusqueda, setTipoBusqueda] = useState<string>('ambos');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [resultados, setResultados] = useState<TrackingPublicResult | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!nombre.trim()) {
      setError('Por favor ingresa un nombre para buscar');
      return;
    }

    setLoading(true);
    setError('');
    setResultados(null);

    try {
      const response = await publicAPI.trackByName(nombre.trim(), tipoBusqueda);
      const data = response.data as TrackingPublicResult;
      setResultados(data);

      if (data.resultados === 0) {
        setError('No se encontraron envíos para ese nombre');
      }
    } catch (err: any) {
      console.error('Error en búsqueda:', err);
      if (err.response?.status === 404) {
        setError('No se encontraron envíos para ese nombre');
      } else {
        setError('Error al buscar envíos. Por favor intenta nuevamente.');
      }
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
          <div className="nav">
            <Link to="/dashboard" className="nav-link">
              Acceso al Sistema
            </Link>
          </div>
        </div>
      </header>

      <main className="tracking-main">
        <div className="container">
          <div className="tracking-hero">
            <h2>Rastrea tus Envíos</h2>
            <p>Busca por nombre del remitente o destinatario</p>
          </div>

          <div className="tracking-form-section">
            <form onSubmit={handleSubmit} className="public-tracking-form">
              <div className="form-group">
                <input
                  type="text"
                  value={nombre}
                  onChange={(e) => setNombre(e.target.value)}
                  placeholder="Nombre del remitente o destinatario"
                  className="form-control"
                  disabled={loading}
                />
                <select
                  value={tipoBusqueda}
                  onChange={(e) => setTipoBusqueda(e.target.value)}
                  className="form-control"
                  disabled={loading}
                  aria-label="Tipo de búsqueda"
                  title="Seleccionar tipo de búsqueda"
                >
                  <option value="ambos">Remitente o Destinatario</option>
                  <option value="remitente">Solo Remitente</option>
                  <option value="destinatario">Solo Destinatario</option>
                </select>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={loading || !nombre.trim()}
                >
                  {loading ? 'Buscando...' : 'Buscar Envíos'}
                </button>
              </div>
            </form>

            {error && (
              <div className="alert alert-error">
                <p>{error}</p>
              </div>
            )}
          </div>

          {resultados && (
            <div className="tracking-results">
              <div className="results-header">
                <h3>Resultados para "{resultados.nombre_buscado}"</h3>
                <span className="results-count">{resultados.resultados} envíos encontrados</span>
              </div>

              <div className="results-list">
                {resultados.envios.map((envio, index) => (
                  <div key={index} className="result-item">
                    <div className="result-header">
                      <h4>Envío #{envio.numero_guia}</h4>
                      <span className={`estado estado-${envio.estado.toLowerCase()}`}>
                        {envio.estado_display}
                      </span>
                    </div>

                    <div className="result-body">
                      <div className="result-row">
                        <span className="label">De:</span>
                        <span className="value">{envio.remitente_nombre}</span>
                      </div>
                      <div className="result-row">
                        <span className="label">Para:</span>
                        <span className="value">{envio.destinatario_nombre}</span>
                      </div>
                      <div className="result-row">
                        <span className="label">Fecha:</span>
                        <span className="value">
                          {new Date(envio.fecha_creacion).toLocaleDateString('es-ES', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric'
                          })}
                        </span>
                      </div>
                      <div className="result-row">
                        <span className="label">Estado:</span>
                        <span className="value">
                          Actualizado el {new Date(envio.fecha_actualizacion).toLocaleDateString('es-ES', {
                            year: 'numeric',
                            month: 'short',
                            day: 'numeric'
                          })}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
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
