import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { publicAPI } from '../services/api';

interface EnvioInfo {
  id: number;
  numero_guia: string;
  estado: string;
  estado_display: string;
  remitente_nombre: string;
  remitente_telefono?: string;
  destinatario_nombre: string;
  destinatario_telefono?: string;
  fecha_creacion: string;
  fecha_actualizacion: string;
  descripcion?: string;
  peso?: number;
  valor_declarado?: number;
}

interface TrackingResponse {
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

const TrackingPageFixed = () => {
  const [busqueda, setBusqueda] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [envios, setEnvios] = useState<EnvioInfo[]>([]);
  const [tipoBusqueda, setTipoBusqueda] = useState<'guia' | 'remitente' | 'destinatario'>('guia');
  const location = useLocation();

  useEffect(() => {
    console.log('🔍 TrackingPageFixed: Componente montado');
    console.log('📍 Ubicación actual:', location.pathname);
    console.log('🌐 URL completa:', window.location.href);
  }, [location]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('� TrackingPageFixed: handleSubmit iniciado');
    console.log('�🔍 TrackingPageFixed: Buscando:', { busqueda, tipoBusqueda });

    if (!busqueda.trim()) {
      console.log('❌ Búsqueda vacía');
      setError('Por favor ingresa un criterio de búsqueda');
      return;
    }

    console.log('⏳ Iniciando loading...');
    setLoading(true);
    setError('');
    setEnvios([]);

    console.log('🔄 Estado actualizado - loading: true, error: "", envios: []');

    try {
      let response;
      let resultados: EnvioInfo[] = [];

      console.log('🔍 Iniciando búsqueda:', tipoBusqueda, busqueda);

      switch (tipoBusqueda) {
        case 'guia':
          // Buscar por número de guía (función existente)
          console.log('📡 Llamando a publicAPI.trackPackage...');
          const startTime = performance.now();

          response = await publicAPI.trackPackage(busqueda);

          const endTime = performance.now();
          console.log(`⏱️ Tiempo de respuesta: ${(endTime - startTime).toFixed(2)}ms`);
          console.log('📦 Respuesta trackPackage completa:', {
            status: response.status,
            data: response.data,
            error: response.error
          });

          if (response.status === 200 && response.data) {
            // Mapear la respuesta al formato esperado
            const envioData = response.data as TrackingResponse;
            const envioMapeado: EnvioInfo = {
              id: Date.now(), // ID temporal para React
              numero_guia: envioData.numero_guia,
              estado: envioData.estado,
              estado_display: envioData.estado_display,
              remitente_nombre: envioData.remitente_nombre,
              destinatario_nombre: envioData.destinatario_nombre,
              fecha_creacion: envioData.fecha_actualizacion, // Usar fecha_actualizacion como creación
              fecha_actualizacion: envioData.fecha_actualizacion,
              descripcion: 'Información disponible via rastreo público',
              peso: 0,
              valor_declarado: 0
            };
            resultados = [envioMapeado];
            console.log('✅ Envío mapeado correctamente:', envioMapeado);
          } else if (response.status === 404) {
            console.log('⚠️ Envío no encontrado (404)');
            setError(`No se encontró ningún envío con la guía: "${busqueda}"`);
          } else if (response.error) {
            console.log('⚠️ Error en respuesta:', response.error);
            setError(response.error);
          } else {
            console.log('⚠️ Respuesta inesperada:', response);
            setError('Respuesta inesperada del servidor');
          }
          break;

        case 'remitente':
          // Buscar por nombre del remitente
          console.log('👤 Llamando a publicAPI.searchByRemitente...');
          const startTimeRemitente = performance.now();

          response = await publicAPI.searchByRemitente(busqueda);

          const endTimeRemitente = performance.now();
          console.log(`⏱️ Tiempo de respuesta remitente: ${(endTimeRemitente - startTimeRemitente).toFixed(2)}ms`);
          console.log('👤 Respuesta searchByRemitente completa:', {
            status: response.status,
            data: response.data,
            error: response.error
          });

          if (response.status === 200 && response.data) {
            const searchData = response.data as { count: number; results: TrackingResponse[] };
            // Mapear múltiples resultados
            resultados = searchData.results.map((envioData, index) => ({
              id: Date.now() + index, // ID temporal único para React
              numero_guia: envioData.numero_guia,
              estado: envioData.estado,
              estado_display: envioData.estado_display,
              remitente_nombre: envioData.remitente_nombre,
              destinatario_nombre: envioData.destinatario_nombre,
              fecha_creacion: envioData.fecha_actualizacion,
              fecha_actualizacion: envioData.fecha_actualizacion,
              descripcion: 'Información disponible via búsqueda por remitente',
              peso: 0,
              valor_declarado: 0
            }));
            console.log(`✅ ${resultados.length} envío(s) mapeados correctamente por remitente`);
          } else if (response.status === 404) {
            console.log('⚠️ No se encontraron envíos para el remitente (404)');
            setError(`No se encontraron envíos para el remitente: "${busqueda}"`);
          } else if (response.error) {
            console.log('⚠️ Error en respuesta de remitente:', response.error);
            setError(response.error);
          } else {
            console.log('⚠️ Respuesta inesperada de remitente:', response);
            setError('Respuesta inesperada del servidor');
          }
          break;

        case 'destinatario':
          // Buscar por nombre del destinatario
          console.log('📍 Llamando a publicAPI.searchByDestinatario...');
          const startTimeDestinatario = performance.now();

          response = await publicAPI.searchByDestinatario(busqueda);

          const endTimeDestinatario = performance.now();
          console.log(`⏱️ Tiempo de respuesta destinatario: ${(endTimeDestinatario - startTimeDestinatario).toFixed(2)}ms`);
          console.log('📍 Respuesta searchByDestinatario completa:', {
            status: response.status,
            data: response.data,
            error: response.error
          });

          if (response.status === 200 && response.data) {
            const searchData = response.data as { count: number; results: TrackingResponse[] };
            // Mapear múltiples resultados
            resultados = searchData.results.map((envioData, index) => ({
              id: Date.now() + index, // ID temporal único para React
              numero_guia: envioData.numero_guia,
              estado: envioData.estado,
              estado_display: envioData.estado_display,
              remitente_nombre: envioData.remitente_nombre,
              destinatario_nombre: envioData.destinatario_nombre,
              fecha_creacion: envioData.fecha_actualizacion,
              fecha_actualizacion: envioData.fecha_actualizacion,
              descripcion: 'Información disponible via búsqueda por destinatario',
              peso: 0,
              valor_declarado: 0
            }));
            console.log(`✅ ${resultados.length} envío(s) mapeados correctamente por destinatario`);
          } else if (response.status === 404) {
            console.log('⚠️ No se encontraron envíos para el destinatario (404)');
            setError(`No se encontraron envíos para el destinatario: "${busqueda}"`);
          } else if (response.error) {
            console.log('⚠️ Error en respuesta de destinatario:', response.error);
            setError(response.error);
          } else {
            console.log('⚠️ Respuesta inesperada de destinatario:', response);
            setError('Respuesta inesperada del servidor');
          }
          break;
      }

      console.log('📊 Resultados obtenidos:', resultados);
      setEnvios(resultados);

      if (resultados.length === 0 && !error) {
        setError(`No se encontraron envíos para el ${tipoBusqueda}: "${busqueda}"`);
      } else {
        console.log(`✅ Se encontraron ${resultados.length} envío(s)`);
      }

    } catch (err: any) {
      console.error('🔍 TrackingPageFixed: Error en búsqueda:', err);
      console.error('🔍 Error completo:', {
        message: err.message,
        name: err.name,
        stack: err.stack,
        response: err.response,
        status: err.response?.status,
        data: err.response?.data
      });

      let errorMessage = 'No se puede conectar con el servidor';

      // Manejo mejorado de errores
      if (err.name === 'TypeError' && err.message.includes('fetch')) {
        errorMessage = 'Error de red. Verifica tu conexión a internet y que el servidor esté funcionando.';
      } else if (err.response?.status === 404) {
        errorMessage = `No se encontró ningún envío con el ${tipoBusqueda}: "${busqueda}"`;
      } else if (err.response?.status === 401) {
        errorMessage = 'Error de autenticación. Por favor inicia sesión nuevamente.';
      } else if (err.response?.status === 500) {
        errorMessage = 'Error del servidor. Por favor intenta nuevamente más tarde.';
      } else if (err.response?.status === 0) {
        errorMessage = 'No se puede conectar con el servidor. Verifica que el servicio esté funcionando.';
      } else if (err.response?.data?.error) {
        errorMessage = err.response.data.error;
      } else if (err.message) {
        errorMessage = `Error de conexión: ${err.message}`;
      }

      console.error('📢 Error final mostrado al usuario:', errorMessage);
      setError(errorMessage);
    } finally {
      console.log('🏁 Finally ejecutándose - loading: false');
      setLoading(false);
      console.log('✅ handleSubmit terminado');
    }
  };

  const formatFecha = (fecha: string) => {
    return new Date(fecha).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  console.log('🖼️ TrackingPageFixed renderizando:', {
    loading,
    error,
    enviosCount: envios.length,
    busqueda,
    tipoBusqueda
  });

  return (
    <div className="tracking-page">
      <div className="container">
        <h1>🔍 Rastrear Envíos - ¡ACTUALIZADO! 🚀</h1>
        <p>Busca envíos por número de guía, nombre del remitente o destinatario</p>

        <form onSubmit={handleSubmit} className="tracking-form">
          <div className="form-group">
            <label htmlFor="tipoBusqueda">Tipo de búsqueda:</label>
            <select
              id="tipoBusqueda"
              value={tipoBusqueda}
              onChange={(e) => setTipoBusqueda(e.target.value as 'guia' | 'remitente' | 'destinatario')}
              className="form-control"
            >
              <option value="guia">Número de Guía</option>
              <option value="remitente">Nombre del Remitente</option>
              <option value="destinatario">Nombre del Destinatario</option>
            </select>
          </div>

          <div className="form-group">
            <input
              type="text"
              value={busqueda}
              onChange={(e) => setBusqueda(e.target.value)}
              placeholder={
                tipoBusqueda === 'guia' ? 'Ej: PKF00000001' :
                tipoBusqueda === 'remitente' ? 'Ej: Juan Pérez' :
                'Ej: María García'
              }
              disabled={loading}
              className="form-control"
            />
            <button
              type="submit"
              disabled={loading || !busqueda.trim()}
              className="btn btn-primary"
            >
              {loading ? 'Buscando...' : 'Buscar Envíos'}
            </button>
          </div>
        </form>

        {error && (
          <div className="alert alert-warning">
            {error}
          </div>
        )}

        {envios.length > 0 && (
          <div className="resultados-busqueda">
            <h2>� Envíos Encontrados ({envios.length})</h2>

            {envios.map((envio) => (
              <div key={envio.id} className="envio-card">
                <div className="envio-header">
                  <h3>Guía: {envio.numero_guia}</h3>
                  <span
                    className={`estado-badge estado-${envio.estado.toLowerCase()}`}
                  >
                    {envio.estado_display}
                  </span>
                </div>

                <div className="envio-details">
                  <div className="detail-row">
                    <strong>� Remitente:</strong> {envio.remitente_nombre}
                    {envio.remitente_telefono && <span> - 📞 {envio.remitente_telefono}</span>}
                  </div>

                  <div className="detail-row">
                    <strong>📍 Destinatario:</strong> {envio.destinatario_nombre}
                    {envio.destinatario_telefono && <span> - 📞 {envio.destinatario_telefono}</span>}
                  </div>

                  {envio.descripcion && (
                    <div className="detail-row">
                      <strong>📋 Descripción:</strong> {envio.descripcion}
                    </div>
                  )}

                  {envio.peso && (
                    <div className="detail-row">
                      <strong>⚖️ Peso:</strong> {envio.peso} kg
                    </div>
                  )}

                  <div className="detail-row">
                    <strong>📅 Creado:</strong> {formatFecha(envio.fecha_creacion)}
                  </div>

                  <div className="detail-row">
                    <strong>🔄 Última actualización:</strong> {formatFecha(envio.fecha_actualizacion)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        <div className="debug-panel">
          <h3>🔧 Panel de Debug</h3>
          <div className="debug-info">
            <p><strong>🔍 Componente:</strong> ✅ TrackingPageFixed funcionando</p>
            <p><strong>� Ruta:</strong> {location.pathname}</p>
            <p><strong>� Tipo búsqueda:</strong> {tipoBusqueda}</p>
            <p><strong>📝 Búsqueda:</strong> {busqueda || '❌ Vacío'}</p>
            <p><strong>� Envíos encontrados:</strong> {envios.length}</p>
            <p><strong>🔄 Estado:</strong> {loading ? '🔄 Cargando' : '✅ Listo'}</p>
            <p><strong>❗ Error:</strong> {error || '✅ Sin errores'}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrackingPageFixed;
