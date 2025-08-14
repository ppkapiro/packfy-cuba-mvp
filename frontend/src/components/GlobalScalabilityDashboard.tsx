// 🇨🇺 PACKFY CUBA - Dashboard Global de Escalabilidad v4.0
import React, { useState, useEffect } from 'react';
import {
  Globe,
  BarChart3,
  TrendingUp,
  Users,
  Package,
  DollarSign,
  MapPin,
  Activity,
  Zap,
  Shield,
  Database,
  Cloud,
  RefreshCw,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Clock,
  Server,
  Cpu,
  HardDrive
} from 'lucide-react';

interface GlobalMetrics {
  revenue: {
    total: number;
    change: number;
    by_region: Record<string, number>;
  };
  shipments: {
    total: number;
    active: number;
    by_status: Record<string, number>;
  };
  users: {
    active: number;
    new_today: number;
    by_region: Record<string, number>;
  };
  performance: {
    uptime: number;
    response_time: number;
    error_rate: number;
  };
}

interface RegionStatus {
  name: string;
  code: string;
  status: 'online' | 'warning' | 'offline';
  load: number;
  users: number;
  shipments: number;
  latency: number;
}

interface SystemAlert {
  id: string;
  type: 'info' | 'warning' | 'error';
  message: string;
  timestamp: string;
  region?: string;
}

export const GlobalScalabilityDashboard: React.FC<{ className?: string }> = ({ className = '' }) => {
  const [globalMetrics, setGlobalMetrics] = useState<GlobalMetrics | null>(null);
  const [regionStatus, setRegionStatus] = useState<RegionStatus[]>([]);
  const [systemAlerts, setSystemAlerts] = useState<SystemAlert[]>([]);
  const [selectedRegion, setSelectedRegion] = useState<string>('all');
  const [isLoading, setIsLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<string>('');

  const regions = [
    { code: 'all', name: 'Global', flag: '🌍' },
    { code: 'cu', name: 'Cuba', flag: '🇨🇺' },
    { code: 'mx', name: 'México', flag: '🇲🇽' },
    { code: 'co', name: 'Colombia', flag: '🇨🇴' },
    { code: 'us', name: 'Estados Unidos', flag: '🇺🇸' },
    { code: 'es', name: 'España', flag: '🇪🇸' }
  ];

  useEffect(() => {
    loadGlobalMetrics();
    loadRegionStatus();
    loadSystemAlerts();

    // Auto-refresh cada 30 segundos
    const interval = setInterval(() => {
      loadGlobalMetrics();
      loadRegionStatus();
    }, 30000);

    return () => clearInterval(interval);
  }, [selectedRegion]);

  const loadGlobalMetrics = async () => {
    try {
      const response = await fetch(`/api/analytics/global-metrics/?region=${selectedRegion}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setGlobalMetrics(data.metrics);
        setLastUpdate(new Date().toLocaleTimeString());
      }
    } catch (error) {
      console.error('Error loading global metrics:', error);
      // Datos simulados para demostración
      setGlobalMetrics({
        revenue: {
          total: 125430.50,
          change: 12.5,
          by_region: {
            'cu': 85000,
            'mx': 25000,
            'co': 10000,
            'us': 3500,
            'es': 1930.50
          }
        },
        shipments: {
          total: 1247,
          active: 324,
          by_status: {
            'pendiente': 45,
            'en_transito': 189,
            'en_aduana': 90,
            'entregado': 923
          }
        },
        users: {
          active: 5629,
          new_today: 47,
          by_region: {
            'cu': 4200,
            'mx': 850,
            'co': 350,
            'us': 150,
            'es': 79
          }
        },
        performance: {
          uptime: 99.97,
          response_time: 245,
          error_rate: 0.02
        }
      });
      setLastUpdate(new Date().toLocaleTimeString());
    }
  };

  const loadRegionStatus = async () => {
    try {
      // Simulación de estado de regiones
      setRegionStatus([
        {
          name: 'Cuba',
          code: 'cu',
          status: 'online',
          load: 68,
          users: 4200,
          shipments: 856,
          latency: 45
        },
        {
          name: 'México',
          code: 'mx',
          status: 'online',
          load: 42,
          users: 850,
          shipments: 245,
          latency: 120
        },
        {
          name: 'Colombia',
          code: 'co',
          status: 'warning',
          load: 85,
          users: 350,
          shipments: 98,
          latency: 180
        },
        {
          name: 'Estados Unidos',
          code: 'us',
          status: 'online',
          load: 35,
          users: 150,
          shipments: 35,
          latency: 95
        },
        {
          name: 'España',
          code: 'es',
          status: 'offline',
          load: 0,
          users: 79,
          shipments: 13,
          latency: 999
        }
      ]);
    } catch (error) {
      console.error('Error loading region status:', error);
    }
  };

  const loadSystemAlerts = async () => {
    try {
      // Simulación de alertas del sistema
      setSystemAlerts([
        {
          id: '1',
          type: 'warning',
          message: 'Alta carga en servidores de Colombia (85%)',
          timestamp: new Date(Date.now() - 15 * 60000).toISOString(),
          region: 'co'
        },
        {
          id: '2',
          type: 'error',
          message: 'Conexión perdida con región España',
          timestamp: new Date(Date.now() - 45 * 60000).toISOString(),
          region: 'es'
        },
        {
          id: '3',
          type: 'info',
          message: 'Pico de tráfico detectado en México',
          timestamp: new Date(Date.now() - 2 * 60000).toISOString(),
          region: 'mx'
        }
      ]);
    } catch (error) {
      console.error('Error loading system alerts:', error);
    }
  };

  const refreshDashboard = async () => {
    setIsLoading(true);
    await Promise.all([
      loadGlobalMetrics(),
      loadRegionStatus(),
      loadSystemAlerts()
    ]);
    setIsLoading(false);
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'online':
        return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'warning':
        return <AlertTriangle className="w-4 h-4 text-yellow-400" />;
      case 'offline':
        return <XCircle className="w-4 h-4 text-red-400" />;
      default:
        return <Clock className="w-4 h-4 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online':
        return 'border-green-400/50 bg-green-500/10';
      case 'warning':
        return 'border-yellow-400/50 bg-yellow-500/10';
      case 'offline':
        return 'border-red-400/50 bg-red-500/10';
      default:
        return 'border-gray-400/50 bg-gray-500/10';
    }
  };

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'info':
        return <Activity className="w-4 h-4 text-blue-400" />;
      case 'warning':
        return <AlertTriangle className="w-4 h-4 text-yellow-400" />;
      case 'error':
        return <XCircle className="w-4 h-4 text-red-400" />;
      default:
        return <Activity className="w-4 h-4 text-gray-400" />;
    }
  };

  return (
    <div className={`bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Globe className="w-8 h-8 text-blue-400" />
          <div>
            <h2 className="text-2xl font-bold text-white">Dashboard Global</h2>
            <p className="text-gray-300">Escalabilidad y Rendimiento Mundial</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          {/* Selector de Región */}
          <select
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-white text-sm"
          >
            {regions.map(region => (
              <option key={region.code} value={region.code} className="bg-gray-800">
                {region.flag} {region.name}
              </option>
            ))}
          </select>

          {/* Botón de Refresh */}
          <button
            onClick={refreshDashboard}
            disabled={isLoading}
            className="flex items-center gap-2 bg-blue-500/20 hover:bg-blue-500/30 border border-blue-400/50 text-blue-200 px-4 py-2 rounded-lg transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
            Actualizar
          </button>
        </div>
      </div>

      {/* Métricas Globales */}
      {globalMetrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          {/* Ingresos */}
          <div className="bg-white/5 rounded-xl p-4 border border-white/10">
            <div className="flex items-center justify-between mb-2">
              <DollarSign className="w-6 h-6 text-green-400" />
              <span className={`text-sm font-medium ${
                globalMetrics.revenue.change > 0 ? 'text-green-400' : 'text-red-400'
              }`}>
                {globalMetrics.revenue.change > 0 ? '+' : ''}{globalMetrics.revenue.change}%
              </span>
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              ${globalMetrics.revenue.total.toLocaleString()}
            </div>
            <div className="text-sm text-gray-300">Ingresos Totales</div>
          </div>

          {/* Envíos */}
          <div className="bg-white/5 rounded-xl p-4 border border-white/10">
            <div className="flex items-center justify-between mb-2">
              <Package className="w-6 h-6 text-blue-400" />
              <span className="text-sm font-medium text-blue-400">
                {globalMetrics.shipments.active} activos
              </span>
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {globalMetrics.shipments.total.toLocaleString()}
            </div>
            <div className="text-sm text-gray-300">Envíos Totales</div>
          </div>

          {/* Usuarios */}
          <div className="bg-white/5 rounded-xl p-4 border border-white/10">
            <div className="flex items-center justify-between mb-2">
              <Users className="w-6 h-6 text-purple-400" />
              <span className="text-sm font-medium text-purple-400">
                +{globalMetrics.users.new_today} hoy
              </span>
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {globalMetrics.users.active.toLocaleString()}
            </div>
            <div className="text-sm text-gray-300">Usuarios Activos</div>
          </div>

          {/* Rendimiento */}
          <div className="bg-white/5 rounded-xl p-4 border border-white/10">
            <div className="flex items-center justify-between mb-2">
              <Zap className="w-6 h-6 text-yellow-400" />
              <span className="text-sm font-medium text-yellow-400">
                {globalMetrics.performance.response_time}ms
              </span>
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {globalMetrics.performance.uptime}%
            </div>
            <div className="text-sm text-gray-300">Tiempo de Actividad</div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Estado de Regiones */}
        <div className="xl:col-span-2">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <MapPin className="w-5 h-5" />
            Estado de Regiones
          </h3>

          <div className="space-y-3">
            {regionStatus.map((region) => (
              <div
                key={region.code}
                className={`p-4 rounded-xl border ${getStatusColor(region.status)}`}
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    {getStatusIcon(region.status)}
                    <div>
                      <div className="font-semibold text-white">{region.name}</div>
                      <div className="text-sm text-gray-300 capitalize">{region.status}</div>
                    </div>
                  </div>

                  <div className="text-right">
                    <div className="text-sm text-gray-300">Latencia</div>
                    <div className="font-semibold text-white">{region.latency}ms</div>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center">
                    <div className="text-sm text-gray-300 mb-1">Carga</div>
                    <div className="flex items-center gap-2">
                      <div className="flex-1 bg-gray-700 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full transition-all duration-300 ${
                            region.load > 80 ? 'bg-red-500' :
                            region.load > 60 ? 'bg-yellow-500' : 'bg-green-500'
                          }`}
                          style={{ width: `${Math.min(region.load, 100)}%` }}
                        />
                      </div>
                      <span className="text-sm font-medium text-white w-8">
                        {region.load}%
                      </span>
                    </div>
                  </div>

                  <div className="text-center">
                    <div className="text-sm text-gray-300 mb-1">Usuarios</div>
                    <div className="font-semibold text-white">
                      {region.users.toLocaleString()}
                    </div>
                  </div>

                  <div className="text-center">
                    <div className="text-sm text-gray-300 mb-1">Envíos</div>
                    <div className="font-semibold text-white">
                      {region.shipments.toLocaleString()}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Alertas del Sistema */}
        <div>
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5" />
            Alertas del Sistema
          </h3>

          <div className="space-y-3 max-h-96 overflow-y-auto">
            {systemAlerts.length > 0 ? (
              systemAlerts.map((alert) => (
                <div
                  key={alert.id}
                  className="p-3 rounded-lg bg-white/5 border border-white/10"
                >
                  <div className="flex items-start gap-3">
                    {getAlertIcon(alert.type)}
                    <div className="flex-1">
                      <div className="text-sm text-white mb-1">
                        {alert.message}
                      </div>
                      <div className="flex items-center gap-2 text-xs text-gray-400">
                        <Clock className="w-3 h-3" />
                        {new Date(alert.timestamp).toLocaleTimeString()}
                        {alert.region && (
                          <>
                            <span>•</span>
                            <span>{alert.region.toUpperCase()}</span>
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-8 text-gray-400">
                <Shield className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>No hay alertas activas</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Información de Actualización */}
      {lastUpdate && (
        <div className="mt-6 text-center text-sm text-gray-400">
          Última actualización: {lastUpdate}
        </div>
      )}
    </div>
  );
};

export default GlobalScalabilityDashboard;
