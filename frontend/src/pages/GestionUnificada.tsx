import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Search, Package, Edit3, Trash2, Eye, Plus, RefreshCw,
  Filter, Calendar, Phone, User, MapPin, AlertTriangle, CheckCircle2
} from 'lucide-react';
import api from '../services/api';

// 🇨🇺 PACKFY CUBA - GESTIÓN COMPLETA DE ENVÍOS
// Página principal para administrar todos los envíos con búsqueda funcional

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

const GestionUnificada: React.FC = () => {
  // Estados principales
  const [envios, setEnvios] = useState<Envio[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Estados de filtros y búsqueda
  const [searchTerm, setSearchTerm] = useState('');
  const [filtroEstado, setFiltroEstado] = useState('');
  const [tipoBusqueda, setTipoBusqueda] = useState<'todos' | 'remitente' | 'destinatario' | 'guia'>('todos');

  // Estados disponibles
  const estadosDisponibles = [
    { value: '', label: 'Todos los estados', icon: '📦' },
    { value: 'RECIBIDO', label: 'Recibido', icon: '📥' },
    { value: 'EN_TRANSITO', label: 'En Tránsito', icon: '🚚' },
    { value: 'EN_REPARTO', label: 'En Reparto', icon: '🏃‍♂️' },
    { value: 'ENTREGADO', label: 'Entregado', icon: '✅' },
    { value: 'DEVUELTO', label: 'Devuelto', icon: '↩️' },
    { value: 'CANCELADO', label: 'Cancelado', icon: '❌' }
  ];

  // Cargar envíos
  useEffect(() => {
    cargarEnvios();
  }, []);

  const cargarEnvios = async () => {
    try {
      setLoading(true);
      setError(null);

      console.log('🔄 Cargando envíos...');

      // Intentar diferentes formas de obtener los datos
      const response = await api.getEnvios(1, 100);

      console.log('📡 Respuesta del API:', response);

      let enviosData: Envio[] = [];

      // Verificar diferentes estructuras de respuesta
      if (response?.data) {
        if (Array.isArray(response.data)) {
          enviosData = response.data;
        } else if ((response.data as any).results && Array.isArray((response.data as any).results)) {
          enviosData = (response.data as any).results;
        } else if ((response.data as any).data && Array.isArray((response.data as any).data)) {
          enviosData = (response.data as any).data;
        }
      } else if (Array.isArray(response)) {
        enviosData = response;
      }

      console.log('📋 Envíos procesados:', enviosData);

      setEnvios(enviosData);

      if (enviosData.length > 0) {
        console.log(`✅ ${enviosData.length} envíos cargados exitosamente`);
      } else {
        console.log('⚠️ No se encontraron envíos');
      }

    } catch (err: any) {
      console.error('❌ Error al cargar envíos:', err);
      setError('Error al cargar los envíos. Verifique la conexión.');
    } finally {
      setLoading(false);
    }
  };

  // Función de filtrado mejorada
  const enviosFiltrados = envios.filter(envio => {
    if (!envio) return false;

    // Filtro por estado
    if (filtroEstado && envio.estado_actual !== filtroEstado) {
      return false;
    }

    // Si no hay término de búsqueda, mostrar todos
    if (!searchTerm.trim()) {
      return true;
    }

    const termino = searchTerm.toLowerCase().trim();

    // Búsqueda según el tipo
    switch (tipoBusqueda) {
      case 'remitente':
        return (envio.remitente_nombre?.toLowerCase() || '').includes(termino) ||
               (envio.remitente_telefono || '').includes(termino);

      case 'destinatario':
        return (envio.destinatario_nombre?.toLowerCase() || '').includes(termino) ||
               (envio.destinatario_telefono || '').includes(termino);

      case 'guia':
        return (envio.numero_guia?.toLowerCase() || '').includes(termino);

      case 'todos':
      default:
        return (envio.numero_guia?.toLowerCase() || '').includes(termino) ||
               (envio.remitente_nombre?.toLowerCase() || '').includes(termino) ||
               (envio.destinatario_nombre?.toLowerCase() || '').includes(termino) ||
               (envio.descripcion?.toLowerCase() || '').includes(termino) ||
               (envio.remitente_telefono || '').includes(termino) ||
               (envio.destinatario_telefono || '').includes(termino);
    }
  });

  const eliminarEnvio = async (id: string, numeroGuia: string) => {
    if (!window.confirm(`¿Eliminar el envío ${numeroGuia}?`)) {
      return;
    }

    try {
      await api.deleteEnvio(parseInt(id));
      console.log(`✅ Envío ${numeroGuia} eliminado`);
      await cargarEnvios();
    } catch (err: any) {
      console.error('❌ Error al eliminar:', err);
      alert('Error al eliminar el envío');
    }
  };

  const getEstadoColor = (estado: string) => {
    const colores = {
      'RECIBIDO': 'bg-blue-100 text-blue-800',
      'EN_TRANSITO': 'bg-yellow-100 text-yellow-800',
      'EN_REPARTO': 'bg-orange-100 text-orange-800',
      'ENTREGADO': 'bg-green-100 text-green-800',
      'DEVUELTO': 'bg-purple-100 text-purple-800',
      'CANCELADO': 'bg-red-100 text-red-800'
    };
    return colores[estado as keyof typeof colores] || 'bg-gray-100 text-gray-800';
  };

  const getEstadoIcon = (estado: string) => {
    const iconos = {
      'RECIBIDO': '📥',
      'EN_TRANSITO': '🚚',
      'EN_REPARTO': '🏃‍♂️',
      'ENTREGADO': '✅',
      'DEVUELTO': '↩️',
      'CANCELADO': '❌'
    };
    return iconos[estado as keyof typeof iconos] || '📦';
  };

  const formatearFecha = (fecha: string) => {
    if (!fecha) return 'Sin fecha';
    try {
      return new Date(fecha).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return 'Fecha inválida';
    }
  };

  const limpiarFiltros = () => {
    setSearchTerm('');
    setFiltroEstado('');
    setTipoBusqueda('todos');
  };

  // Mostrar loading
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-blue-50 flex items-center justify-center">
        <div className="text-center p-8">
          <RefreshCw className="w-16 h-16 text-red-600 animate-spin mx-auto mb-4" />
          <h2 className="text-2xl font-semibold text-gray-800 mb-2">Cargando envíos...</h2>
          <p className="text-gray-600">Por favor espere un momento</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-blue-50">
      <div className="container mx-auto px-4 py-6">

        {/* Header */}
        <div className="mb-8">
          <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 mb-6">
            <div>
              <h1 className="text-4xl font-bold text-gray-800 mb-2 flex items-center gap-3">
                <Package className="text-red-600" />
                🇨🇺 Gestión de Envíos
              </h1>
              <p className="text-gray-600 text-lg">
                Administración completa de paquetes y envíos
              </p>
            </div>

            <Link
              to="/envios/nuevo"
              className="bg-gradient-to-r from-red-600 to-red-700 text-white px-6 py-3 rounded-xl font-semibold hover:from-red-700 hover:to-red-800 transition-all duration-200 flex items-center gap-2 shadow-lg"
            >
              <Plus className="w-5 h-5" />
              Nuevo Envío
            </Link>
          </div>

          {/* Estadísticas rápidas */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white p-4 rounded-lg shadow border-l-4 border-blue-500">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total Envíos</p>
                  <p className="text-2xl font-bold text-gray-800">{envios.length}</p>
                </div>
                <Package className="w-8 h-8 text-blue-500" />
              </div>
            </div>

            <div className="bg-white p-4 rounded-lg shadow border-l-4 border-yellow-500">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">En Tránsito</p>
                  <p className="text-2xl font-bold text-gray-800">
                    {envios.filter(e => e.estado_actual === 'EN_TRANSITO').length}
                  </p>
                </div>
                <div className="text-2xl">🚚</div>
              </div>
            </div>

            <div className="bg-white p-4 rounded-lg shadow border-l-4 border-green-500">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Entregados</p>
                  <p className="text-2xl font-bold text-gray-800">
                    {envios.filter(e => e.estado_actual === 'ENTREGADO').length}
                  </p>
                </div>
                <CheckCircle2 className="w-8 h-8 text-green-500" />
              </div>
            </div>

            <div className="bg-white p-4 rounded-lg shadow border-l-4 border-purple-500">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Resultados</p>
                  <p className="text-2xl font-bold text-gray-800">{enviosFiltrados.length}</p>
                </div>
                <Search className="w-8 h-8 text-purple-500" />
              </div>
            </div>
          </div>
        </div>

        {/* Panel principal */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-200">

          {/* Filtros */}
          <div className="p-6 bg-gradient-to-r from-red-600 to-blue-600 text-white rounded-t-xl">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Filter className="w-5 h-5" />
              Búsqueda y Filtros
            </h2>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
              {/* Tipo de búsqueda */}
              <div>
                <label className="block text-sm font-medium text-red-100 mb-2">
                  Buscar en:
                </label>
                <select
                  value={tipoBusqueda}
                  onChange={(e) => setTipoBusqueda(e.target.value as any)}
                  className="w-full px-3 py-2 bg-white text-gray-800 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-300"
                  title="Seleccionar tipo de búsqueda"
                >
                  <option value="todos">🔍 Buscar en todo</option>
                  <option value="guia">📦 Número de guía</option>
                  <option value="remitente">👤 Remitente</option>
                  <option value="destinatario">🎯 Destinatario</option>
                </select>
              </div>

              {/* Campo de búsqueda */}
              <div>
                <label className="block text-sm font-medium text-red-100 mb-2">
                  Término:
                </label>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                  <input
                    type="text"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    placeholder={
                      tipoBusqueda === 'guia' ? 'PKF00001234' :
                      tipoBusqueda === 'remitente' ? 'Nombre remitente' :
                      tipoBusqueda === 'destinatario' ? 'Nombre destinatario' :
                      'Buscar...'
                    }
                    className="w-full pl-10 pr-3 py-2 bg-white text-gray-800 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-300"
                  />
                </div>
              </div>

              {/* Filtro estado */}
              <div>
                <label className="block text-sm font-medium text-red-100 mb-2">
                  Estado:
                </label>
                <select
                  value={filtroEstado}
                  onChange={(e) => setFiltroEstado(e.target.value)}
                  className="w-full px-3 py-2 bg-white text-gray-800 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-300"
                  title="Filtrar por estado"
                >
                  {estadosDisponibles.map(estado => (
                    <option key={estado.value} value={estado.value}>
                      {estado.icon} {estado.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Acciones */}
              <div className="flex gap-2">
                <button
                  onClick={limpiarFiltros}
                  className="flex-1 px-4 py-2 bg-white bg-opacity-20 text-white border border-white border-opacity-30 rounded-lg hover:bg-opacity-30 transition-all"
                >
                  Limpiar
                </button>

                <button
                  onClick={cargarEnvios}
                  className="flex-1 px-4 py-2 bg-white bg-opacity-20 text-white border border-white border-opacity-30 rounded-lg hover:bg-opacity-30 transition-all"
                  title="Actualizar lista de envíos"
                >
                  <RefreshCw className="w-4 h-4 mx-auto" />
                </button>
              </div>
            </div>

            {/* Indicador de filtros activos */}
            {(searchTerm || filtroEstado) && (
              <div className="mt-4 p-3 bg-white bg-opacity-10 rounded-lg">
                <div className="flex flex-wrap gap-2 text-sm">
                  <span className="text-red-100">Filtros activos:</span>
                  {searchTerm && (
                    <span className="bg-white bg-opacity-20 text-white px-2 py-1 rounded">
                      {tipoBusqueda}: "{searchTerm}"
                    </span>
                  )}
                  {filtroEstado && (
                    <span className="bg-white bg-opacity-20 text-white px-2 py-1 rounded">
                      Estado: {estadosDisponibles.find(e => e.value === filtroEstado)?.label}
                    </span>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Contenido */}
          <div className="p-6">
            {/* Error */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-red-500" />
                <p className="text-red-700">{error}</p>
                <button
                  onClick={cargarEnvios}
                  className="ml-auto px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700"
                >
                  Reintentar
                </button>
              </div>
            )}

            {/* Debug info removido para producción */}

            {/* Tabla */}
            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr className="bg-gray-50">
                    <th className="text-left py-3 px-4 font-semibold text-gray-700 border-b">Guía</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700 border-b">Remitente</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700 border-b">Destinatario</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700 border-b">Estado</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700 border-b">Fecha</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700 border-b">Peso</th>
                    <th className="text-right py-3 px-4 font-semibold text-gray-700 border-b">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {enviosFiltrados.length === 0 ? (
                    <tr>
                      <td colSpan={7} className="text-center py-12">
                        <Package className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                        <p className="text-gray-500 text-lg">
                          {envios.length === 0 ?
                            'No hay envíos registrados' :
                            'No se encontraron envíos con los filtros aplicados'
                          }
                        </p>
                        {envios.length === 0 && (
                          <Link
                            to="/envios/nuevo"
                            className="inline-flex items-center gap-2 mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
                          >
                            <Plus className="w-4 h-4" />
                            Crear primer envío
                          </Link>
                        )}
                      </td>
                    </tr>
                  ) : (
                    enviosFiltrados.map((envio) => (
                      <tr key={envio.id} className="border-b hover:bg-gray-50 transition-colors">
                        <td className="py-3 px-4">
                          <div className="font-semibold text-gray-900">
                            {envio.numero_guia || 'Sin guía'}
                          </div>
                          <div className="text-sm text-gray-500 truncate max-w-32" title={envio.descripcion}>
                            {envio.descripcion || 'Sin descripción'}
                          </div>
                        </td>

                        <td className="py-3 px-4">
                          <div className="font-medium text-gray-900 flex items-center gap-1">
                            <User className="w-3 h-3 text-gray-400" />
                            {envio.remitente_nombre || 'Sin nombre'}
                          </div>
                          <div className="text-sm text-gray-500 flex items-center gap-1">
                            <Phone className="w-3 h-3" />
                            {envio.remitente_telefono || 'Sin teléfono'}
                          </div>
                        </td>

                        <td className="py-3 px-4">
                          <div className="font-medium text-gray-900 flex items-center gap-1">
                            <MapPin className="w-3 h-3 text-gray-400" />
                            {envio.destinatario_nombre || 'Sin nombre'}
                          </div>
                          <div className="text-sm text-gray-500 flex items-center gap-1">
                            <Phone className="w-3 h-3" />
                            {envio.destinatario_telefono || 'Sin teléfono'}
                          </div>
                        </td>

                        <td className="py-3 px-4">
                          <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getEstadoColor(envio.estado_actual)}`}>
                            {getEstadoIcon(envio.estado_actual)} {envio.estado_actual || 'Sin estado'}
                          </span>
                        </td>

                        <td className="py-3 px-4">
                          <div className="text-sm text-gray-900 flex items-center gap-1">
                            <Calendar className="w-3 h-3 text-gray-400" />
                            {formatearFecha(envio.fecha_creacion)}
                          </div>
                        </td>

                        <td className="py-3 px-4">
                          <div className="text-sm text-gray-900 font-medium">
                            {envio.peso || 0} kg
                          </div>
                        </td>

                        <td className="py-3 px-4">
                          <div className="flex justify-end gap-1">
                            <Link
                              to={`/envios/${envio.id}`}
                              className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                              title="Ver detalles"
                            >
                              <Eye className="w-4 h-4" />
                            </Link>
                            <Link
                              to={`/envios/${envio.id}/editar`}
                              className="p-2 text-yellow-600 hover:bg-yellow-50 rounded-lg transition-colors"
                              title="Editar"
                            >
                              <Edit3 className="w-4 h-4" />
                            </Link>
                            <button
                              onClick={() => eliminarEnvio(envio.id, envio.numero_guia)}
                              className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                              title="Eliminar"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>

            {/* Resumen */}
            {envios.length > 0 && (
              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <div className="flex flex-wrap justify-between items-center gap-4 text-sm text-gray-600">
                  <div>
                    Mostrando <strong>{enviosFiltrados.length}</strong> de <strong>{envios.length}</strong> envíos
                  </div>
                  <div className="flex gap-4">
                    <span className="flex items-center gap-1">
                      <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                      Entregados: {envios.filter(e => e.estado_actual === 'ENTREGADO').length}
                    </span>
                    <span className="flex items-center gap-1">
                      <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                      En tránsito: {envios.filter(e => e.estado_actual === 'EN_TRANSITO').length}
                    </span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default GestionUnificada;
