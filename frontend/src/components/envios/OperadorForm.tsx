import React, { useState, useEffect } from 'react';
import { Package, Search, Filter, Plus, Edit, Eye } from 'lucide-react';
import { api } from '../../services/api';
import RemitenteForm from './RemitenteForm';

interface OperadorFormProps {
  user: any;
  tenant: any;
  perfil: any;
}

interface Envio {
  id: number;
  numero_guia: string;
  estado_actual: string;
  estado_display: string;
  fecha_creacion: string;
  descripcion: string;
  peso: number;
  remitente_nombre: string;
  destinatario_nombre: string;
  destinatario_direccion: string;
}

const OperadorForm: React.FC<OperadorFormProps> = ({ user, tenant, perfil }) => {
  const [activeTab, setActiveTab] = useState<'lista' | 'crear'>('lista');
  const [envios, setEnvios] = useState<Envio[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filtroEstado, setFiltroEstado] = useState('');

  useEffect(() => {
    loadEnvios();
  }, []);

  const loadEnvios = async () => {
    try {
      setIsLoading(true);
      const response = await api.get('/envios/');
      setEnvios(response.data.results || response.data || []);
    } catch (error) {
      console.error('Error al cargar envíos:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const filteredEnvios = envios.filter(envio => {
    const matchesSearch = envio.numero_guia.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         envio.remitente_nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         envio.destinatario_nombre.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesEstado = !filtroEstado || envio.estado_actual === filtroEstado;

    return matchesSearch && matchesEstado;
  });

  const getEstadoColor = (estado: string) => {
    switch (estado) {
      case 'RECIBIDO': return 'bg-blue-100 text-blue-800';
      case 'EN_TRANSITO': return 'bg-yellow-100 text-yellow-800';
      case 'EN_REPARTO': return 'bg-purple-100 text-purple-800';
      case 'ENTREGADO': return 'bg-green-100 text-green-800';
      case 'DEVUELTO': return 'bg-red-100 text-red-800';
      case 'CANCELADO': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  if (activeTab === 'crear') {
    return (
      <div>
        {/* Header con navegación */}
        <div className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold text-gray-900">Gestión de Envíos</h1>
              <button
                onClick={() => setActiveTab('lista')}
                className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition-colors"
              >
                Volver a Lista
              </button>
            </div>
          </div>
        </div>

        <RemitenteForm user={user} tenant={tenant} perfil={perfil} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Package className="w-8 h-8 text-blue-600 mr-3" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Gestión de Envíos</h1>
                <p className="text-sm text-gray-600">
                  {user.first_name} {user.last_name} • {perfil.rol === 'operador_miami' ? 'Operador Miami' : 'Operador Cuba'}
                </p>
              </div>
            </div>
            <button
              onClick={() => setActiveTab('crear')}
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors flex items-center"
            >
              <Plus className="w-4 h-4 mr-2" />
              Nuevo Envío
            </button>
          </div>
        </div>
      </div>

      {/* Filtros */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="bg-white rounded-lg shadow-md p-4 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Buscar
              </label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Número de guía, remitente, destinatario..."
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Estado
              </label>
              <div className="relative">
                <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <select
                  value={filtroEstado}
                  onChange={(e) => setFiltroEstado(e.target.value)}
                  className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Todos los estados</option>
                  <option value="RECIBIDO">Recibido</option>
                  <option value="EN_TRANSITO">En tránsito</option>
                  <option value="EN_REPARTO">En reparto</option>
                  <option value="ENTREGADO">Entregado</option>
                  <option value="DEVUELTO">Devuelto</option>
                  <option value="CANCELADO">Cancelado</option>
                </select>
              </div>
            </div>

            <div className="flex items-end">
              <button
                onClick={loadEnvios}
                className="w-full bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition-colors"
              >
                Actualizar
              </button>
            </div>
          </div>
        </div>

        {/* Lista de envíos */}
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">
              Envíos ({filteredEnvios.length})
            </h2>
          </div>

          {isLoading ? (
            <div className="p-6 text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
              <p className="text-gray-500 mt-2">Cargando envíos...</p>
            </div>
          ) : filteredEnvios.length === 0 ? (
            <div className="p-6 text-center">
              <Package className="w-12 h-12 text-gray-400 mx-auto mb-2" />
              <p className="text-gray-500">No se encontraron envíos</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Guía
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Estado
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Remitente
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Destinatario
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Fecha
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Peso
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Acciones
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredEnvios.map((envio) => (
                    <tr key={envio.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {envio.numero_guia}
                        </div>
                        <div className="text-sm text-gray-500 truncate max-w-xs">
                          {envio.descripcion}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getEstadoColor(envio.estado_actual)}`}>
                          {envio.estado_display}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {envio.remitente_nombre}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">{envio.destinatario_nombre}</div>
                        <div className="text-sm text-gray-500 truncate max-w-xs">
                          {envio.destinatario_direccion}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {formatDate(envio.fecha_creacion)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {envio.peso} kg
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <button className="text-blue-600 hover:text-blue-900">
                            <Eye className="w-4 h-4" />
                          </button>
                          <button className="text-green-600 hover:text-green-900">
                            <Edit className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default OperadorForm;
