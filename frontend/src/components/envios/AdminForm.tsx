import React, { useState, useEffect } from 'react';
import {
  Package, BarChart3, Users, TrendingUp,
  Calendar
} from 'lucide-react';
import { api } from '../../services/api';
import OperadorForm from './OperadorForm';

interface AdminFormProps {
  user: any;
  tenant: any;
  perfil: any;
}

interface EstadisticasEnvios {
  total: number;
  recibidos: number;
  en_transito: number;
  en_reparto: number;
  entregados: number;
  devueltos: number;
  cancelados: number;
}

const AdminForm: React.FC<AdminFormProps> = ({ user, tenant, perfil }) => {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'envios' | 'usuarios'>('dashboard');
  const [estadisticas, setEstadisticas] = useState<EstadisticasEnvios>({
    total: 0,
    recibidos: 0,
    en_transito: 0,
    en_reparto: 0,
    entregados: 0,
    devueltos: 0,
    cancelados: 0
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadEstadisticas();
  }, []);

  const loadEstadisticas = async () => {
    try {
      setIsLoading(true);
      const response = await api.get('/envios/');
      const envios = (response.data as any).results || (response.data as any) || [];

      // Calcular estadísticas
      const stats = envios.reduce((acc: any, envio: any) => {
        acc.total++;
        acc[envio.estado_actual.toLowerCase()] = (acc[envio.estado_actual.toLowerCase()] || 0) + 1;
        return acc;
      }, {
        total: 0,
        recibidos: 0,
        en_transito: 0,
        en_reparto: 0,
        entregados: 0,
        devueltos: 0,
        cancelados: 0
      });

      setEstadisticas(stats);
    } catch (error) {
      console.error('Error al cargar estadísticas:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (activeTab === 'envios') {
    return (
      <div>
        {/* Header con navegación */}
        <div className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold text-gray-900">Gestión de Envíos</h1>
              <div className="flex space-x-2">
                <button
                  onClick={() => setActiveTab('dashboard')}
                  className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition-colors"
                >
                  Dashboard
                </button>
                <button
                  onClick={() => setActiveTab('usuarios')}
                  className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
                >
                  Usuarios
                </button>
              </div>
            </div>
          </div>
        </div>

        <OperadorForm user={user} tenant={tenant} perfil={perfil} />
      </div>
    );
  }

  if (activeTab === 'usuarios') {
    return (
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <Users className="w-8 h-8 text-blue-600 mr-3" />
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">Gestión de Usuarios</h1>
                  <p className="text-sm text-gray-600">
                    Administrar usuarios de {tenant.nombre}
                  </p>
                </div>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => setActiveTab('dashboard')}
                  className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition-colors"
                >
                  Dashboard
                </button>
                <button
                  onClick={() => setActiveTab('envios')}
                  className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors"
                >
                  Envíos
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="text-center">
              <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Gestión de Usuarios
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                Para gestionar usuarios, accede al panel de administración de Django
              </p>
              <a
                href="/admin/"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors inline-flex items-center"
              >
                <Users className="w-4 h-4 mr-2" />
                Ir al Admin Django
              </a>
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
              <BarChart3 className="w-8 h-8 text-blue-600 mr-3" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Dashboard Administrativo</h1>
                <p className="text-sm text-gray-600">
                  {user.first_name} {user.last_name} • Dueño de {tenant.nombre}
                </p>
              </div>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => setActiveTab('envios')}
                className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors flex items-center"
              >
                <Package className="w-4 h-4 mr-2" />
                Gestionar Envíos
              </button>
              <button
                onClick={() => setActiveTab('usuarios')}
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors flex items-center"
              >
                <Users className="w-4 h-4 mr-2" />
                Gestionar Usuarios
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Dashboard Content */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        {/* Estadísticas generales */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Package className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Envíos</p>
                <p className="text-2xl font-bold text-gray-900">
                  {isLoading ? '...' : estadisticas.total}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <TrendingUp className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Entregados</p>
                <p className="text-2xl font-bold text-gray-900">
                  {isLoading ? '...' : estadisticas.entregados}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <Calendar className="w-6 h-6 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">En Tránsito</p>
                <p className="text-2xl font-bold text-gray-900">
                  {isLoading ? '...' : estadisticas.en_transito}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <BarChart3 className="w-6 h-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">En Reparto</p>
                <p className="text-2xl font-bold text-gray-900">
                  {isLoading ? '...' : estadisticas.en_reparto}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Desglose por estados */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Estados de Envíos</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Recibidos</span>
                <span className="text-sm font-medium text-blue-600">
                  {estadisticas.recibidos}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">En Tránsito</span>
                <span className="text-sm font-medium text-yellow-600">
                  {estadisticas.en_transito}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">En Reparto</span>
                <span className="text-sm font-medium text-purple-600">
                  {estadisticas.en_reparto}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Entregados</span>
                <span className="text-sm font-medium text-green-600">
                  {estadisticas.entregados}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Devueltos</span>
                <span className="text-sm font-medium text-red-600">
                  {estadisticas.devueltos}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Cancelados</span>
                <span className="text-sm font-medium text-gray-600">
                  {estadisticas.cancelados}
                </span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Acciones Rápidas</h3>
            <div className="space-y-3">
              <button
                onClick={() => setActiveTab('envios')}
                className="w-full text-left p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center">
                  <Package className="w-5 h-5 text-blue-600 mr-3" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Gestionar Envíos</p>
                    <p className="text-xs text-gray-500">Ver, crear y editar envíos</p>
                  </div>
                </div>
              </button>

              <button
                onClick={() => setActiveTab('usuarios')}
                className="w-full text-left p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center">
                  <Users className="w-5 h-5 text-green-600 mr-3" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Gestionar Usuarios</p>
                    <p className="text-xs text-gray-500">Administrar roles y permisos</p>
                  </div>
                </div>
              </button>

              <a
                href="/admin/"
                target="_blank"
                rel="noopener noreferrer"
                className="w-full text-left p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors block"
              >
                <div className="flex items-center">
                  <BarChart3 className="w-5 h-5 text-purple-600 mr-3" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Admin Django</p>
                    <p className="text-xs text-gray-500">Panel de administración completo</p>
                  </div>
                </div>
              </a>

              <button
                onClick={loadEstadisticas}
                className="w-full text-left p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center">
                  <TrendingUp className="w-5 h-5 text-indigo-600 mr-3" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Actualizar Datos</p>
                    <p className="text-xs text-gray-500">Refrescar estadísticas</p>
                  </div>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminForm;
