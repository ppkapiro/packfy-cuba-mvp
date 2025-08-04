import React, { useState, useEffect, ChangeEvent } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';
import axios from 'axios';
import { enviosAPI } from '../services/api';
import Pagination from '../components/Pagination';
import DashboardStats from '../components/DashboardStats';
import ErrorBoundary from '../components/ErrorBoundary';
import ErrorFallback from '../components/ErrorFallback';
import { Envio } from '../types';
import '../styles/dashboard.css';

// Función auxiliar para formatear fechas de forma segura
const formatearFechaSafe = (fecha: string | null | undefined): string => {
  if (!fecha) return 'No disponible';
  
  try {
    const fechaObj = new Date(fecha);
    if (isNaN(fechaObj.getTime())) {
      console.warn('Fecha inválida recibida:', fecha);
      return 'Fecha inválida';
    }
    return format(fechaObj, 'dd/MM/yyyy', { locale: es });
  } catch (error) {
    console.error('Error al formatear fecha:', fecha, error);
    return 'Error en fecha';
  }
};

interface PaginatedResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Envio[];
}

const Dashboard: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [successMessage, setSuccessMessage] = useState('');
  const [envios, setEnvios] = useState<Envio[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filtroEstado, setFiltroEstado] = useState('');
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFin, setFechaFin] = useState('');
  
  // Estado para paginación
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const [pageSize, setPageSize] = useState(10);  useEffect(() => {
    // Sistema mejorado para recuperar mensajes de éxito de múltiples fuentes
    // 1. Verificar sessionStorage (volátil)
    const successFromSession = sessionStorage.getItem('_lastEnvioSuccess');
    
    // 2. Verificar localStorage (más persistente)
    const successFromLocalStorage = localStorage.getItem('_temp_success_message');
    const successTimestamp = localStorage.getItem('_temp_success_timestamp');
    
    // 3. Verificar parámetros de URL
    const successFromUrl = new URLSearchParams(location.search).get('success');
    
    // 4. Verificar state de react-router
    const successFromState = location.state?.success;
    
    // Lógica para determinar cuál mensaje usar y limpiar almacenamiento
    if (successFromSession) {
      console.log('Dashboard: Usando mensaje de éxito de sessionStorage');
      setSuccessMessage(successFromSession);
      sessionStorage.removeItem('_lastEnvioSuccess');
    } else if (successFromState) {
      console.log('Dashboard: Usando mensaje de éxito del estado de navegación');
      setSuccessMessage(successFromState as string);
      navigate(location.pathname, { replace: true, state: {} });
    } else if (successFromLocalStorage && successTimestamp) {
      // Solo usar el mensaje de localStorage si tiene menos de 5 minutos
      const timestamp = new Date(successTimestamp);
      const now = new Date();
      const ageInMinutes = (now.getTime() - timestamp.getTime()) / (1000 * 60);
      
      if (ageInMinutes < 5) {
        console.log('Dashboard: Usando mensaje de éxito de localStorage (edad: ' + ageInMinutes.toFixed(2) + ' minutos)');
        setSuccessMessage(successFromLocalStorage);
      }
      
      // Limpiar localStorage en cualquier caso
      localStorage.removeItem('_temp_success_message');
      localStorage.removeItem('_temp_success_timestamp');
    } else if (successFromUrl === 'true') {
      console.log('Dashboard: Usando mensaje de éxito de parámetros URL');
      setSuccessMessage('Operación completada exitosamente');
      navigate(location.pathname, { replace: true });
    }
    
    // Verificar si hay token antes de intentar cargar los envíos
    const token = localStorage.getItem('token');
    if (!token) {
      console.log('Dashboard: No hay token de autenticación, redirigiendo a login');
      const win = window as Window;
      win.location.href = '/login';
      return;
    }
    
    console.log('Dashboard: Iniciando carga de envíos');
    cargarEnvios();
  }, [filtroEstado, fechaInicio, fechaFin, currentPage, pageSize, location]);

  const cargarEnvios = async () => {
    setLoading(true);
    setError(''); // Limpiar errores anteriores
      try {
      console.log('Dashboard: Intentando cargar envíos...');
      const params: Record<string, any> = {};
      
      if (filtroEstado) {
        params.estado = filtroEstado;
      }
      
      if (fechaInicio) {
        params.fecha_registro_after = fechaInicio;
      }
      
      if (fechaFin) {
        params.fecha_registro_before = fechaFin;
      }
      
      console.log('Dashboard: Parámetros de consulta:', params);
      
      // Verificar si la autenticación fue exitosa recientemente
      const authSuccess = sessionStorage.getItem('_auth_success');
      const authTimestamp = sessionStorage.getItem('_auth_timestamp');
      const authAge = authTimestamp ? (new Date().getTime() - new Date(authTimestamp).getTime()) / 1000 : null;
      
      console.log('Dashboard: Estado de autenticación:', { 
        authSuccess, 
        authTimestamp, 
        authAge,
        hasToken: !!localStorage.getItem('token')
      });
      
      console.log('Dashboard: Realizando llamada a enviosAPI.getAll', currentPage, pageSize);
      
      // Manejar errores de conexión explícitamente
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 15000);
      
      try {
        const response = await enviosAPI.getAll(currentPage, pageSize, params);
        clearTimeout(timeout);
        
        console.log('Dashboard: Respuesta API recibida:', response);
        const data = response.data as PaginatedResponse;
        
        if (!data || !data.results) {
          console.error('Dashboard: Respuesta sin datos válidos:', data);
          setError('La respuesta del servidor no contiene datos válidos');
          setEnvios([]);
          return;
        }
        
        setEnvios(data.results);
        setTotalItems(data.count);
        setTotalPages(Math.ceil(data.count / pageSize));
      } catch (fetchError: any) {
        clearTimeout(timeout);
        throw fetchError;
      }
    } catch (err: any) {
      console.error('Dashboard: Error al cargar los envíos:', err);
      
      // Mostrar un mensaje de error más descriptivo y detallado
      if (axios.isAxiosError(err)) {
        if (err.response) {
          const statusCode = err.response.status;
          const statusText = err.response.statusText;
          const errorData = err.response.data;
          
          console.error(`Dashboard: Error de respuesta ${statusCode}:`, errorData);
          
          if (statusCode === 401) {
            setError('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.');
            // Podríamos redirigir a la página de login aquí
          } else if (statusCode === 403) {
            setError('No tienes permisos para acceder a estos datos.');
          } else if (statusCode >= 500) {
            setError(`Error del servidor (${statusCode}). Por favor, inténtalo más tarde.`);
          } else {
            setError(`Error al cargar los envíos: ${statusCode} - ${statusText}`);
          }
        } else if (err.request) {
          console.error('Dashboard: No se recibió respuesta del servidor:', err.request);
          setError('No se recibió respuesta del servidor. Comprueba tu conexión a internet o inténtalo más tarde.');
        } else {
          console.error('Dashboard: Error en la configuración de la solicitud:', err.message);
          setError(`Error al configurar la solicitud: ${err.message}`);
        }
      } else {
        console.error('Dashboard: Error desconocido');
        setError('Error desconocido al cargar los envíos');
      }
    } finally {
      setLoading(false);
    }
  };
    // Función para intentar limpiar la caché si hay problemas
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
        // Usar el objeto window.location sin parámetros
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
    <ErrorBoundary fallback={<ErrorFallback />}>      <div className="dashboard-page">
        {successMessage && (
          <div className="alert alert-success">
            {successMessage}
            <button 
              onClick={() => setSuccessMessage('')}
              className="close-button"
              title="Cerrar"
            >
              ×
            </button>
          </div>
        )}
        
        {error && (
          <div className="alert alert-error">
            {error}
            <div className="error-actions">
              <button 
                onClick={() => setError('')}
                className="close-button"
                title="Cerrar"
              >
                ×
              </button>
              <button 
                onClick={handleClearCacheAndRefresh}
                className="btn btn-secondary btn-sm"
                title="Limpiar caché y recargar página"
              >
                Recargar Página
              </button>
            </div>
          </div>
        )}
        
        {/* Sección de estadísticas - Con manejo de errores */}
        <div className="stats-container">
          <React.Suspense fallback={<div className="dashboard-loading">Cargando estadísticas...</div>}>            <ErrorBoundary fallback={
              <div className="dashboard-error">
                No se pudieron cargar las estadísticas.                <button 
                  onClick={() => {
                    const win = window as Window;
                    win.location.reload();
                  }} 
                  className="btn-retry"
                >
                  Reintentar
                </button>
              </div>
            }>
              <DashboardStats />
            </ErrorBoundary>
          </React.Suspense>
        </div>
          <div className="dashboard-header">
          <h1>Dashboard de Envíos</h1>
          <div className="dashboard-actions">
            <button 
              onClick={() => {
                console.log("Recargando dashboard manualmente");
                cargarEnvios();
              }} 
              className="btn-refresh"
              title="Recargar lista de envíos"
            >
              🔄
            </button>
            <Link to="/envios/nuevo" className="btn">Nuevo Envío</Link>
          </div>
        </div>
          <div className="filtros">
          <div className="form-group">
            <label htmlFor="filtroEstado">Estado:</label>
            <select 
              id="filtroEstado"
              name="filtroEstado"
              value={filtroEstado} 
              onChange={(e: ChangeEvent<HTMLSelectElement>) => setFiltroEstado(e.target.value)}
              className="form-control"
              aria-label="Filtrar por estado de envío"
              title="Seleccionar estado de envío"
            >
              <option value="">Todos</option>
              <option value="registrado">Registrado</option>
              <option value="en_transito">En tránsito</option>
              <option value="en_almacen">En almacén</option>
              <option value="en_ruta">En ruta de entrega</option>
              <option value="entregado">Entregado</option>
              <option value="devuelto">Devuelto</option>
              <option value="cancelado">Cancelado</option>
            </select>
          </div>
            <div className="form-group">
            <label htmlFor="fechaInicio">Desde:</label>
            <input 
              id="fechaInicio"
              name="fechaInicio"
              type="date" 
              value={fechaInicio} 
              onChange={(e: ChangeEvent<HTMLInputElement>) => setFechaInicio(e.target.value)}
              className="form-control"
              aria-label="Fecha inicial para filtrar envíos"
              title="Seleccionar fecha inicial"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="fechaFin">Hasta:</label>
            <input 
              id="fechaFin"
              name="fechaFin"
              type="date" 
              value={fechaFin} 
              onChange={(e: ChangeEvent<HTMLInputElement>) => setFechaFin(e.target.value)}
              className="form-control"
              aria-label="Fecha final para filtrar envíos"
              title="Seleccionar fecha final"
            />
          </div>
        </div>
        
        {error && (
          <div className="dashboard-error">
            <div className="error-icon">⚠️</div>
            <div>
              <strong>{error}</strong>
              <div className="dashboard-error-details">
                Por favor, inténtelo de nuevo más tarde o contacte con el administrador si el problema persiste.
              </div>
              <button onClick={handleClearCacheAndRefresh} className="btn btn-secondary mt-2">
                Limpiar caché y recargar
              </button>
            </div>
          </div>
        )}
        
        {loading ? (
          <div className="dashboard-loading">
            <div className="loading-spinner dashboard-spinner"></div>
            <span>Cargando envíos...</span>
          </div>
        ) : (
          <>
            <table className="envios-table">
              <thead>
                <tr>
                  <th>Guía</th>
                  <th>Remitente</th>
                  <th>Destinatario</th>
                  <th>Estado</th>
                  <th>Fecha de Registro</th>
                  <th>Entrega Estimada</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {envios.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="no-data">No hay envíos para mostrar</td>
                  </tr>
                ) : (
                  envios.map((envio) => (
                    <tr key={envio.id}>
                      <td>{envio.numero_guia}</td>
                      <td>{envio.remitente_nombre}</td>
                      <td>{envio.destinatario_nombre}</td>                      <td>
                        <span className={`estado estado-${envio.estado_actual ? envio.estado_actual.toLowerCase() : 'desconocido'}`}>
                          {envio.estado_display || envio.estado_actual || 'Desconocido'}
                        </span>
                      </td>
                      <td>
                        {formatearFechaSafe(envio.fecha_creacion)}
                      </td>
                      <td>
                        {formatearFechaSafe(envio.fecha_estimada_entrega)}
                      </td>
                      <td>
                        <Link to={`/envios/${envio.id}`} className="btn-link">
                          Ver Detalles
                        </Link>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
            
            {/* Componente de paginación */}
            {envios.length > 0 && (              <div className="pagination-container">
                <div className="items-per-page">
                  <label htmlFor="pageSize">Mostrar:</label>
                  <select 
                    id="pageSize"
                    name="pageSize"
                    value={pageSize}
                    onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                      setPageSize(Number(e.target.value));
                      setCurrentPage(1); // Volver a la primera página al cambiar el tamaño
                    }}
                    className="form-control"
                    aria-label="Número de elementos por página"
                    title="Seleccionar cantidad de envíos por página"
                  >
                    <option value="10">10</option>
                    <option value="25">25</option>
                    <option value="50">50</option>
                    <option value="100">100</option>
                  </select>
                  <span>por página</span>
                </div>
                
                <Pagination
                  currentPage={currentPage}
                  totalPages={totalPages}
                  onPageChange={setCurrentPage}
                  totalItems={totalItems}
                  itemsPerPage={pageSize}
                />
              </div>
            )}
          </>
        )}
      </div>
    </ErrorBoundary>
  );
};

export default Dashboard;
