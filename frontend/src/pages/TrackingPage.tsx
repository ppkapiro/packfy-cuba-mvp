import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { enviosAPI } from '../services/api';

const TrackingPage = () => {
  const [numeroGuia, setNumeroGuia] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!numeroGuia.trim()) return;
    
    setLoading(true);
    setError('');
    
    try {
      const response = await enviosAPI.buscarPorGuia(numeroGuia);
      // Si encuentra el envío, redirigir a la página de detalles
      navigate(`/envios/${response.data.id}`);
    } catch (err: any) {
      setError(err.response?.data?.error || 'No se encontró ningún envío con ese número de guía');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="tracking-page">
      <h1>Seguimiento de Envíos</h1>
      <p className="subtitle">Ingresa el número de guía para ver el estado de tu envío</p>
      
      {error && <div className="alert alert-error">{error}</div>}
      
      <div className="tracking-form-container">
        <form onSubmit={handleSubmit} className="tracking-form">
          <div className="form-row">
            <input
              type="text"
              value={numeroGuia}
              onChange={(e) => setNumeroGuia(e.target.value)}
              placeholder="Número de Guía (ej: PKF00000001)"
              className="form-control"
              disabled={loading}
            />
            <button 
              type="submit" 
              className="btn" 
              disabled={loading}
            >
              {loading ? 'Buscando...' : 'Buscar'}
            </button>
          </div>
        </form>
      </div>
      
      <div className="tracking-info">
        <h3>¿Qué es el número de guía?</h3>
        <p>
          El número de guía es un código único asignado a tu envío que te permite
          rastrear su estado en tiempo real. Lo puedes encontrar en tu comprobante
          de envío o en el correo electrónico de confirmación.
        </p>
      </div>
    </div>
  );
};

export default TrackingPage;
