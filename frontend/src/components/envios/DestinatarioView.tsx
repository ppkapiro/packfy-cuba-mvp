import React, { useState, useEffect } from 'react';
import {
  Package, Search, Clock, MapPin,
  CheckCircle, XCircle, AlertCircle,
  Truck, User, Mail, Phone
} from 'lucide-react';
import { api } from '../../services/api';

interface DestinatarioViewProps {
  user: any;
  tenant: any;
  perfil: any;
}

interface Envio {
  id: number;
  numero_seguimiento: string;
  descripcion_contenido: string;
  peso_kg: number;
  estado_actual: string;
  fecha_creacion: string;
  fecha_estimada_entrega: string;
  nombre_remitente: string;
  telefono_remitente: string;
  email_remitente: string;
  direccion_origen: string;
  direccion_destino: string;
  notas?: string;
  precio_estimado?: number;
}

const DestinatarioView: React.FC<DestinatarioViewProps> = ({ user }) => {
  const [envios, setEnvios] = useState<Envio[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedEnvio, setSelectedEnvio] = useState<Envio | null>(null);

  useEffect(() => {
    loadEnvios();
  }, []);

  const loadEnvios = async () => {
    try {
      setIsLoading(true);
      // Buscar envíos donde el usuario es el destinatario
      const response = await api.get(`/envios/?destinatario=${user.id}`);

      const enviosData = (response.data as any).results || (response.data as any) || [];
      setEnvios(enviosData);
    } catch (error) {
      console.error('Error al cargar envíos:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getEstadoIcon = (estado: string) => {
    switch (estado.toLowerCase()) {
      case 'recibido':
        return <Clock className="w-4 h-4 text-blue-500" />;
      case 'en_transito':
        return <Truck className="w-4 h-4 text-yellow-500" />;
      case 'en_reparto':
        return <MapPin className="w-4 h-4 text-purple-500" />;
      case 'entregado':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'devuelto':
      case 'cancelado':
        return <XCircle className="w-4 h-4 text-red-500" />;
      default:
        return <AlertCircle className="w-4 h-4 text-gray-500" />;
    }
  };

  const getEstadoColor = (estado: string) => {
    switch (estado.toLowerCase()) {
      case 'recibido':
        return 'bg-blue-100 text-blue-800';
      case 'en_transito':
        return 'bg-yellow-100 text-yellow-800';
      case 'en_reparto':
        return 'bg-purple-100 text-purple-800';
      case 'entregado':
        return 'bg-green-100 text-green-800';
      case 'devuelto':
      case 'cancelado':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const filteredEnvios = envios.filter(envio =>
    envio.numero_seguimiento.toLowerCase().includes(searchTerm.toLowerCase()) ||
    envio.descripcion_contenido.toLowerCase().includes(searchTerm.toLowerCase()) ||
    envio.nombre_remitente.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (selectedEnvio) {
    return (
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white shadow-sm border-b">
          <div className="max-w-4xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <button
                  onClick={() => setSelectedEnvio(null)}
                  className="mr-4 text-gray-600 hover:text-gray-900"
                >
                  ← Volver
                </button>
                <Package className="w-6 h-6 text-blue-600 mr-3" />
                <div>
                  <h1 className="text-xl font-bold text-gray-900">
                    Envío #{selectedEnvio.numero_seguimiento}
                  </h1>
                  <p className="text-sm text-gray-600">Detalles del envío</p>
                </div>
              </div>
              <div className="flex items-center">
                {getEstadoIcon(selectedEnvio.estado_actual)}
                <span className={`ml-2 px-2 py-1 rounded-full text-xs font-medium ${getEstadoColor(selectedEnvio.estado_actual)}`}>
                  {selectedEnvio.estado_actual.replace('_', ' ').toUpperCase()}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Contenido del detalle */}
        <div className="max-w-4xl mx-auto px-4 py-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Información del paquete */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Información del Paquete
              </h3>
              <div className="space-y-3">
                <div>
                  <label className="text-sm font-medium text-gray-600">
                    Contenido
                  </label>
                  <p className="text-sm text-gray-900">
                    {selectedEnvio.descripcion_contenido}
                  </p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">
                    Peso
                  </label>
                  <p className="text-sm text-gray-900">
                    {selectedEnvio.peso_kg} kg
                  </p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">
                    Fecha de Creación
                  </label>
                  <p className="text-sm text-gray-900">
                    {new Date(selectedEnvio.fecha_creacion).toLocaleDateString()}
                  </p>
                </div>
                {selectedEnvio.fecha_estimada_entrega && (
                  <div>
                    <label className="text-sm font-medium text-gray-600">
                      Fecha Estimada de Entrega
                    </label>
                    <p className="text-sm text-gray-900">
                      {new Date(selectedEnvio.fecha_estimada_entrega).toLocaleDateString()}
                    </p>
                  </div>
                )}
                {selectedEnvio.precio_estimado && (
                  <div>
                    <label className="text-sm font-medium text-gray-600">
                      Precio Estimado
                    </label>
                    <p className="text-sm text-gray-900">
                      ${selectedEnvio.precio_estimado}
                    </p>
                  </div>
                )}
                {selectedEnvio.notas && (
                  <div>
                    <label className="text-sm font-medium text-gray-600">
                      Notas
                    </label>
                    <p className="text-sm text-gray-900">
                      {selectedEnvio.notas}
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Información del remitente */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Información del Remitente
              </h3>
              <div className="space-y-3">
                <div className="flex items-center">
                  <User className="w-4 h-4 text-gray-400 mr-2" />
                  <div>
                    <label className="text-sm font-medium text-gray-600">
                      Nombre
                    </label>
                    <p className="text-sm text-gray-900">
                      {selectedEnvio.nombre_remitente}
                    </p>
                  </div>
                </div>
                {selectedEnvio.telefono_remitente && (
                  <div className="flex items-center">
                    <Phone className="w-4 h-4 text-gray-400 mr-2" />
                    <div>
                      <label className="text-sm font-medium text-gray-600">
                        Teléfono
                      </label>
                      <p className="text-sm text-gray-900">
                        {selectedEnvio.telefono_remitente}
                      </p>
                    </div>
                  </div>
                )}
                {selectedEnvio.email_remitente && (
                  <div className="flex items-center">
                    <Mail className="w-4 h-4 text-gray-400 mr-2" />
                    <div>
                      <label className="text-sm font-medium text-gray-600">
                        Email
                      </label>
                      <p className="text-sm text-gray-900">
                        {selectedEnvio.email_remitente}
                      </p>
                    </div>
                  </div>
                )}
                <div className="flex items-start">
                  <MapPin className="w-4 h-4 text-gray-400 mr-2 mt-1" />
                  <div>
                    <label className="text-sm font-medium text-gray-600">
                      Dirección de Origen
                    </label>
                    <p className="text-sm text-gray-900">
                      {selectedEnvio.direccion_origen}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Información de entrega */}
            <div className="bg-white rounded-lg shadow-md p-6 lg:col-span-2">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Información de Entrega
              </h3>
              <div className="flex items-start">
                <MapPin className="w-4 h-4 text-gray-400 mr-2 mt-1" />
                <div>
                  <label className="text-sm font-medium text-gray-600">
                    Dirección de Destino
                  </label>
                  <p className="text-sm text-gray-900">
                    {selectedEnvio.direccion_destino}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
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
                <h1 className="text-2xl font-bold text-gray-900">Mis Envíos</h1>
                <p className="text-sm text-gray-600">
                  {user.first_name} {user.last_name} • {envios.length} envíos
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="relative">
                <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                  type="text"
                  placeholder="Buscar por número, contenido o remitente..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <button
                onClick={loadEnvios}
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
              >
                Actualizar
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Contenido principal */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        {isLoading ? (
          <div className="text-center py-12">
            <Package className="w-12 h-12 text-gray-400 mx-auto mb-4 animate-pulse" />
            <p className="text-gray-600">Cargando tus envíos...</p>
          </div>
        ) : filteredEnvios.length === 0 ? (
          <div className="text-center py-12">
            <Package className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {searchTerm ? 'No se encontraron envíos' : 'No tienes envíos registrados'}
            </h3>
            <p className="text-sm text-gray-600">
              {searchTerm
                ? 'Intenta con otros términos de búsqueda'
                : 'Los envíos dirigidos a ti aparecerán aquí'
              }
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredEnvios.map((envio) => (
              <div
                key={envio.id}
                className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer"
                onClick={() => setSelectedEnvio(envio)}
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center">
                    {getEstadoIcon(envio.estado_actual)}
                    <span className="ml-2 text-sm font-medium text-gray-900">
                      #{envio.numero_seguimiento}
                    </span>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getEstadoColor(envio.estado_actual)}`}>
                    {envio.estado_actual.replace('_', ' ').toUpperCase()}
                  </span>
                </div>

                <div className="space-y-2">
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {envio.descripcion_contenido}
                    </p>
                    <p className="text-xs text-gray-600">
                      {envio.peso_kg} kg
                    </p>
                  </div>

                  <div>
                    <p className="text-sm text-gray-600">
                      De: {envio.nombre_remitente}
                    </p>
                    <p className="text-xs text-gray-500 truncate">
                      {envio.direccion_origen}
                    </p>
                  </div>

                  <div className="pt-2 border-t border-gray-100">
                    <p className="text-xs text-gray-600">
                      Creado: {new Date(envio.fecha_creacion).toLocaleDateString()}
                    </p>
                    {envio.fecha_estimada_entrega && (
                      <p className="text-xs text-gray-600">
                        Entrega estimada: {new Date(envio.fecha_estimada_entrega).toLocaleDateString()}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default DestinatarioView;
