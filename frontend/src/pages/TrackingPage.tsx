import React, { useState } from 'react';
import { enviosAPI } from '../services/api';
import './TrackingPage.css';
import '../styles/mobile-optimized.css';

interface SearchResult {
  resultados: number;
  nombre_buscado: string;
  tipo_busqueda: string;
  envios: Array<{
    id: number;
    numero_guia: string;
    estado: string;
    estado_display: string;
    remitente_nombre: string;
    destinatario_nombre: string;
    fecha_creacion: string;
    fecha_actualizacion: string;
    peso: number;
    descripcion: string;
  }>;
}

const TrackingPage: React.FC = () => {
  const [nombre, setNombre] = useState<string>('');
  const [tipoBusqueda, setTipoBusqueda] = useState<string>('ambos');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [resultados, setResultados] = useState<SearchResult | null>(null);

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
      const response = await enviosAPI.getByNombre(nombre.trim(), tipoBusqueda);
      const data = response.data as SearchResult;
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
    <div className="tracking-page">
      <h1>Seguimiento de Envíos</h1>
      <p className="subtitle">Busca tus envíos por nombre del remitente o destinatario</p>

      {error && <div className="alert alert-danger">{error}</div>}

      <div className="search-form">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="nombre">Nombre:</label>
            <input
              id="nombre"
              type="text"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              placeholder="Nombre del remitente o destinatario"
              className="form-control"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="tipo">Buscar en:</label>
            <select
              id="tipo"
              value={tipoBusqueda}
              onChange={(e) => setTipoBusqueda(e.target.value)}
              className="form-control"
              disabled={loading}
            >
              <option value="ambos">Remitente y Destinatario</option>
              <option value="remitente">Solo Remitente</option>
              <option value="destinatario">Solo Destinatario</option>
            </select>
          </div>

          <div className="form-group">
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading || !nombre.trim()}
            >
              {loading ? 'Buscando...' : 'Buscar'}
            </button>
          </div>
        </form>
      </div>

      {resultados && (
        <div className="search-results">
          <h2>Resultados para "{resultados.nombre_buscado}"</h2>
          <p className="results-count">{resultados.resultados} envíos encontrados</p>

          <div className="results-list">
            {resultados.envios.map((envio) => (
              <div key={envio.id} className="result-item">
                <div className="result-header">
                  <h3>Envío #{envio.numero_guia}</h3>
                  <span className={`estado estado-${envio.estado.toLowerCase()}`}>
                    {envio.estado_display}
                  </span>
                </div>

                <div className="result-body">
                  <div className="result-row">
                    <span className="label">Remitente:</span>
                    <span className="value">{envio.remitente_nombre}</span>
                  </div>
                  <div className="result-row">
                    <span className="label">Destinatario:</span>
                    <span className="value">{envio.destinatario_nombre}</span>
                  </div>
                  <div className="result-row">
                    <span className="label">Peso:</span>
                    <span className="value">{envio.peso} lbs</span>
                  </div>
                  <div className="result-row">
                    <span className="label">Descripción:</span>
                    <span className="value">{envio.descripcion}</span>
                  </div>
                  <div className="result-row">
                    <span className="label">Fecha de creación:</span>
                    <span className="value">
                      {new Date(envio.fecha_creacion).toLocaleDateString('es-ES', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })}
                    </span>
                  </div>
                  <div className="result-row">
                    <span className="label">Última actualización:</span>
                    <span className="value">
                      {new Date(envio.fecha_actualizacion).toLocaleDateString('es-ES', {
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
  );
};

export default TrackingPage;
