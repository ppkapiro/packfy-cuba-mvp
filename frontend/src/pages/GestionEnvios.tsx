import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Search, Package, Edit3, Trash2, Eye, Filter, Plus, RefreshCw, Star } from 'lucide-react';
import api from '../services/api';

// 🚀 PACKFY CUBA - GESTIÓN GRATUITA DE ENVÍOS
// Página completa para administrar todos los envíos del sistema

interface Envio {
  id: string;
  numero_guia: string;
  descripcion: string;
  peso: number;
  valor_declarado: number;

  remitente_nombre: string;
  remitente_telefono: string;

  destinatario_nombre: string;
  destinatario_telefono: string;

  estado_actual: string;
  fecha_creacion: string;
  fecha_estimada_entrega: string | null;

  notas?: string;
}

const GestionEnvios: React.FC = () => {
  // Estados del componente
  const [envios, setEnvios] = useState<Envio[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filtroEstado, setFiltroEstado] = useState('');
  const [envioSeleccionado] = useState<string | null>(null);

  const navigate = useNavigate();

  // Determinar si es modo premium basado en la URL
  const isPremium = window.location.pathname.includes('/gestion/premium');  // Estados disponibles para filtros
  const estadosDisponibles = [
    { value: '', label: 'Todos los estados' },
    { value: 'RECIBIDO', label: '📦 Recibido' },
    { value: 'EN_TRANSITO', label: '🚚 En Tránsito' },
    { value: 'EN_REPARTO', label: '🏃 En Reparto' },
    { value: 'ENTREGADO', label: '✅ Entregado' },
    { value: 'DEVUELTO', label: '↩️ Devuelto' },
    { value: 'CANCELADO', label: '❌ Cancelado' }
  ];

  // Cargar envíos al montar el componente
  useEffect(() => {
    cargarEnvios();
  }, []);

  const cargarEnvios = async () => {
    try {
      setLoading(true);
      setError(null);

      console.log('🔄 Cargando lista de envíos...');
      const response = await api.getEnvios();

      console.log('✅ Envíos cargados:', response.data);
      const data: any = response.data;
      setEnvios(data?.results || data || []);

    } catch (err: any) {
      console.error('❌ Error al cargar envíos:', err);
      setError('Error al cargar la lista de envíos');
    } finally {
      setLoading(false);
    }
  };

  // Filtrar envíos según criterios de búsqueda
  const enviosFiltrados = envios.filter(envio => {
    const coincideBusqueda = searchTerm === '' ||
      envio.numero_guia.toLowerCase().includes(searchTerm.toLowerCase()) ||
      envio.remitente_nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
      envio.destinatario_nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
      envio.descripcion.toLowerCase().includes(searchTerm.toLowerCase());

    const coincideEstado = filtroEstado === '' || envio.estado_actual === filtroEstado;

    return coincideBusqueda && coincideEstado;
  });

  // Manejar eliminación de envío
  const eliminarEnvio = async (id: string, numeroGuia: string) => {
    if (!window.confirm(`¿Está seguro de eliminar el envío ${numeroGuia}? Esta acción no se puede deshacer.`)) {
      return;
    }

    try {
      await api.deleteEnvio(parseInt(id));
      console.log(`✅ Envío ${numeroGuia} eliminado correctamente`);

      // Actualizar la lista
      setEnvios(envios.filter(e => e.id !== id));

      // Notificación de éxito
      alert(`Envío ${numeroGuia} eliminado correctamente`);

    } catch (err: any) {
      console.error('❌ Error al eliminar envío:', err);
      alert('Error al eliminar el envío. Inténtalo de nuevo.');
    }
  };

  // Formatear fecha para mostrar
  const formatearFecha = (fecha: string) => {
    return new Date(fecha).toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Obtener color según estado
  const getEstadoColor = (estado: string) => {
    const colores: { [key: string]: string } = {
      'RECIBIDO': 'bg-blue-100 text-blue-800',
      'EN_TRANSITO': 'bg-yellow-100 text-yellow-800',
      'EN_REPARTO': 'bg-purple-100 text-purple-800',
      'ENTREGADO': 'bg-green-100 text-green-800',
      'DEVUELTO': 'bg-orange-100 text-orange-800',
      'CANCELADO': 'bg-red-100 text-red-800'
    };
    return colores[estado] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-96">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-gray-600">Cargando gestión de envíos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="gestion-envios-page p-6 max-w-7xl mx-auto">
      {/* Header con acciones principales */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-800 flex items-center gap-3">
              {isPremium ? (
                <>
                  <Star className="w-8 h-8 text-yellow-600" />
                  Gestión Premium
                </>
              ) : (
                <>
                  <Package className="w-8 h-8 text-blue-600" />
                  Gestión Gratuita
                </>
              )}
            </h1>
            <p className="text-gray-600 mt-2">
              {isPremium
                ? `Gestión avanzada de envíos con herramientas profesionales • ${enviosFiltrados.length} de ${envios.length} envíos`
                : `Administra todos los envíos de forma gratuita • ${enviosFiltrados.length} de ${envios.length} envíos`
              }
            </p>
          </div>

          <div className="flex gap-3">
            <button
              onClick={cargarEnvios}
              className="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
              title="Recargar lista"
            >
              <RefreshCw className="w-4 h-4" />
              Recargar
            </button>

            {isPremium && (
              <>
                <button
                  onClick={() => alert('🚀 Función Premium: Exportar a Excel')}
                  className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
                  title="Exportar datos"
                >
                  📊 Exportar
                </button>

                <button
                  onClick={() => alert('🚀 Función Premium: Análisis de Rendimiento')}
                  className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
                  title="Análisis avanzado"
                >
                  📈 Análisis
                </button>
              </>
            )}

            <Link
              to="/envios/nuevo"
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              <Plus className="w-4 h-4" />
              Nuevo Envío
            </Link>
          </div>
        </div>
      </div>

      {/* Filtros y búsqueda */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Búsqueda */}
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Search className="w-4 h-4 inline mr-2" />
              Buscar envíos
            </label>
            <input
              type="text"
              placeholder="Buscar por guía, remitente, destinatario o descripción..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          {/* Filtro por estado */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Filter className="w-4 h-4 inline mr-2" />
              Filtrar por estado
            </label>
            <select
              value={filtroEstado}
              onChange={(e) => setFiltroEstado(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              title="Filtrar envíos por estado"
            >
              {estadosDisponibles.map(estado => (
                <option key={estado.value} value={estado.value}>
                  {estado.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Mostrar errores */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
          <p className="font-medium">❌ Error</p>
          <p>{error}</p>
        </div>
      )}

      {/* Lista de envíos */}
      {enviosFiltrados.length === 0 ? (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <Package className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-600 mb-2">
            {envios.length === 0 ? 'No hay envíos registrados' : 'No se encontraron envíos'}
          </h3>
          <p className="text-gray-500 mb-6">
            {envios.length === 0
              ? 'Crea tu primer envío para comenzar'
              : 'Intenta modificar los filtros de búsqueda'
            }
          </p>
          {envios.length === 0 && (
            <Link
              to="/envios/nuevo"
              className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              <Plus className="w-5 h-5" />
              Crear Primer Envío
            </Link>
          )}
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          {/* Tabla responsive */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Guía / Descripción
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Remitente
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Destinatario
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Estado
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Fecha
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {enviosFiltrados.map((envio) => (
                  <tr
                    key={envio.id}
                    className={`hover:bg-gray-50 transition-colors ${
                      envioSeleccionado === envio.id ? 'bg-blue-50' : ''
                    }`}
                  >
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          #{envio.numero_guia}
                        </div>
                        <div className="text-sm text-gray-500 truncate max-w-xs">
                          {envio.descripcion}
                        </div>
                        <div className="text-xs text-gray-400">
                          {envio.peso} kg • ${envio.valor_declarado}
                        </div>
                      </div>
                    </td>

                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{envio.remitente_nombre}</div>
                      <div className="text-sm text-gray-500">{envio.remitente_telefono}</div>
                    </td>

                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{envio.destinatario_nombre}</div>
                      <div className="text-sm text-gray-500">{envio.destinatario_telefono}</div>
                    </td>

                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getEstadoColor(envio.estado_actual)}`}>
                        {envio.estado_actual.replace('_', ' ')}
                      </span>
                    </td>

                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div>{formatearFecha(envio.fecha_creacion)}</div>
                      {envio.fecha_estimada_entrega && (
                        <div className="text-xs text-gray-400">
                          Est: {new Date(envio.fecha_estimada_entrega).toLocaleDateString()}
                        </div>
                      )}
                    </td>

                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex gap-2">
                        <Link
                          to={`/envios/${envio.id}`}
                          className="text-blue-600 hover:text-blue-800 p-1 rounded"
                          title="Ver detalles"
                        >
                          <Eye className="w-4 h-4" />
                        </Link>

                        <button
                          onClick={() => navigate(`/envios/${envio.id}/editar`)}
                          className="text-green-600 hover:text-green-800 p-1 rounded"
                          title="Editar envío"
                        >
                          <Edit3 className="w-4 h-4" />
                        </button>

                        <button
                          onClick={() => eliminarEnvio(envio.id, envio.numero_guia)}
                          className="text-red-600 hover:text-red-800 p-1 rounded"
                          title="Eliminar envío"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Footer informativo */}
      <div className="mt-8 text-center text-gray-500">
        {isPremium ? (
          <>
            <p className="text-sm">
              ⭐ <strong>Gestión Premium</strong> • Herramientas avanzadas desbloqueadas
            </p>
            <p className="text-xs mt-1">
              Disfruta de todas las funciones profesionales • <Link to="/envios" className="text-blue-600 hover:underline">Volver al selector</Link>
            </p>
          </>
        ) : (
          <>
            <p className="text-sm">
              🎉 <strong>Gestión Gratuita</strong> • Todas las funciones básicas sin costo
            </p>
            <p className="text-xs mt-1">
              ¿Necesitas funciones avanzadas? <Link to="/envios" className="text-blue-600 hover:underline">Conoce el modo Premium</Link>
            </p>
          </>
        )}
      </div>
    </div>
  );
};

export default GestionEnvios;
