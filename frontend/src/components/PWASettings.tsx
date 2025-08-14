// 🇨🇺 PACKFY CUBA - Componente PWA Settings
import React, { useState, useEffect } from 'react';
import { usePWA } from '../services/pwa';
import {
  Bell,
  Download,
  Wifi,
  WifiOff,
  Check,
  X,
  Settings,
  Smartphone,
  Globe,
  RefreshCw,
  AlertCircle
} from 'lucide-react';

interface PWASettingsProps {
  className?: string;
}

export const PWASettings: React.FC<PWASettingsProps> = ({ className = '' }) => {
  const {
    isOffline,
    isInstallable,
    isPushSubscribed,
    notificationPermission,
    isServiceWorkerSupported,
    isPushSupported,
    subscribeToPush,
    unsubscribeFromPush,
    installApp,
    sendTestNotification,
    syncPendingData
  } = usePWA();

  const [isLoading, setIsLoading] = useState({
    push: false,
    install: false,
    test: false,
    sync: false
  });

  const [stats, setStats] = useState({
    cacheSize: '0 MB',
    lastSync: 'Nunca',
    notificationsSent: 0
  });

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      // Estimar tamaño de cache
      if ('storage' in navigator && 'estimate' in navigator.storage) {
        const estimate = await navigator.storage.estimate();
        const used = estimate.usage || 0;
        setStats(prev => ({
          ...prev,
          cacheSize: `${(used / 1024 / 1024).toFixed(1)} MB`
        }));
      }

      // Cargar estadísticas de notificaciones
      const response = await fetch('/api/push/stats/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setStats(prev => ({
          ...prev,
          notificationsSent: data.summary?.sent || 0,
          lastSync: data.last_sync || 'Nunca'
        }));
      }
    } catch (error) {
      console.error('Error loading PWA stats:', error);
    }
  };

  const handlePushToggle = async () => {
    setIsLoading(prev => ({ ...prev, push: true }));

    try {
      if (isPushSubscribed) {
        await unsubscribeFromPush();
      } else {
        await subscribeToPush();
      }
    } finally {
      setIsLoading(prev => ({ ...prev, push: false }));
    }
  };

  const handleInstall = async () => {
    setIsLoading(prev => ({ ...prev, install: true }));

    try {
      await installApp();
    } finally {
      setIsLoading(prev => ({ ...prev, install: false }));
    }
  };

  const handleTestNotification = async () => {
    setIsLoading(prev => ({ ...prev, test: true }));

    try {
      await sendTestNotification();
    } finally {
      setIsLoading(prev => ({ ...prev, test: false }));
    }
  };

  const handleSync = async () => {
    setIsLoading(prev => ({ ...prev, sync: true }));

    try {
      await syncPendingData();
      await loadStats();
    } finally {
      setIsLoading(prev => ({ ...prev, sync: false }));
    }
  };

  const getConnectionStatus = () => {
    if (isOffline) {
      return {
        icon: <WifiOff className="w-5 h-5 text-red-500" />,
        text: 'Sin conexión',
        color: 'text-red-500',
        bg: 'bg-red-50'
      };
    }
    return {
      icon: <Wifi className="w-5 h-5 text-green-500" />,
      text: 'Conectado',
      color: 'text-green-500',
      bg: 'bg-green-50'
    };
  };

  const getNotificationStatus = () => {
    if (!isPushSupported) {
      return {
        icon: <X className="w-5 h-5 text-gray-400" />,
        text: 'No soportado',
        color: 'text-gray-400'
      };
    }

    if (notificationPermission === 'denied') {
      return {
        icon: <X className="w-5 h-5 text-red-500" />,
        text: 'Bloqueadas',
        color: 'text-red-500'
      };
    }

    if (isPushSubscribed) {
      return {
        icon: <Check className="w-5 h-5 text-green-500" />,
        text: 'Activas',
        color: 'text-green-500'
      };
    }

    return {
      icon: <Bell className="w-5 h-5 text-yellow-500" />,
      text: 'Disponibles',
      color: 'text-yellow-500'
    };
  };

  const connectionStatus = getConnectionStatus();
  const notificationStatus = getNotificationStatus();

  return (
    <div className={`bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-6 ${className}`}>
      <div className="flex items-center gap-3 mb-6">
        <Settings className="w-6 h-6 text-white" />
        <h3 className="text-xl font-bold text-white">Configuración PWA</h3>
      </div>

      {/* Estado de Conexión */}
      <div className="mb-6">
        <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/10">
          <div className="flex items-center gap-3">
            {connectionStatus.icon}
            <div>
              <div className="font-semibold text-white">Estado de Conexión</div>
              <div className={`text-sm ${connectionStatus.color}`}>
                {connectionStatus.text}
              </div>
            </div>
          </div>
          {isOffline && (
            <button
              onClick={handleSync}
              disabled={isLoading.sync}
              className="flex items-center gap-2 px-3 py-1 bg-blue-500/20 text-blue-200 rounded-lg border border-blue-400/30 hover:bg-blue-500/30 transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${isLoading.sync ? 'animate-spin' : ''}`} />
              Sincronizar
            </button>
          )}
        </div>
      </div>

      {/* Notificaciones Push */}
      <div className="mb-6">
        <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/10">
          <div className="flex items-center gap-3">
            {notificationStatus.icon}
            <div>
              <div className="font-semibold text-white">Notificaciones Push</div>
              <div className={`text-sm ${notificationStatus.color}`}>
                {notificationStatus.text}
              </div>
            </div>
          </div>
          <div className="flex gap-2">
            {isPushSupported && notificationPermission !== 'denied' && (
              <>
                <button
                  onClick={handlePushToggle}
                  disabled={isLoading.push}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors disabled:opacity-50 ${
                    isPushSubscribed
                      ? 'bg-red-500/20 text-red-200 border border-red-400/30 hover:bg-red-500/30'
                      : 'bg-green-500/20 text-green-200 border border-green-400/30 hover:bg-green-500/30'
                  }`}
                >
                  {isLoading.push ? (
                    <RefreshCw className="w-4 h-4 animate-spin" />
                  ) : isPushSubscribed ? (
                    'Desactivar'
                  ) : (
                    'Activar'
                  )}
                </button>
                {isPushSubscribed && (
                  <button
                    onClick={handleTestNotification}
                    disabled={isLoading.test}
                    className="px-3 py-2 bg-blue-500/20 text-blue-200 rounded-lg border border-blue-400/30 hover:bg-blue-500/30 transition-colors disabled:opacity-50"
                  >
                    {isLoading.test ? (
                      <RefreshCw className="w-4 h-4 animate-spin" />
                    ) : (
                      'Probar'
                    )}
                  </button>
                )}
              </>
            )}
          </div>
        </div>
      </div>

      {/* Instalación de App */}
      {isInstallable && (
        <div className="mb-6">
          <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/10">
            <div className="flex items-center gap-3">
              <Smartphone className="w-5 h-5 text-purple-400" />
              <div>
                <div className="font-semibold text-white">Instalar Aplicación</div>
                <div className="text-sm text-purple-200">
                  Instala PACKFY CUBA en tu dispositivo
                </div>
              </div>
            </div>
            <button
              onClick={handleInstall}
              disabled={isLoading.install}
              className="flex items-center gap-2 px-4 py-2 bg-purple-500/20 text-purple-200 rounded-lg border border-purple-400/30 hover:bg-purple-500/30 transition-colors disabled:opacity-50"
            >
              {isLoading.install ? (
                <RefreshCw className="w-4 h-4 animate-spin" />
              ) : (
                <Download className="w-4 h-4" />
              )}
              Instalar
            </button>
          </div>
        </div>
      )}

      {/* Estadísticas */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="p-4 bg-white/5 rounded-xl border border-white/10">
          <div className="flex items-center gap-2 mb-2">
            <Globe className="w-4 h-4 text-blue-400" />
            <span className="text-sm text-blue-200">Cache</span>
          </div>
          <div className="text-lg font-bold text-white">{stats.cacheSize}</div>
        </div>

        <div className="p-4 bg-white/5 rounded-xl border border-white/10">
          <div className="flex items-center gap-2 mb-2">
            <Bell className="w-4 h-4 text-green-400" />
            <span className="text-sm text-green-200">Notificaciones</span>
          </div>
          <div className="text-lg font-bold text-white">{stats.notificationsSent}</div>
        </div>

        <div className="p-4 bg-white/5 rounded-xl border border-white/10">
          <div className="flex items-center gap-2 mb-2">
            <RefreshCw className="w-4 h-4 text-yellow-400" />
            <span className="text-sm text-yellow-200">Última Sync</span>
          </div>
          <div className="text-lg font-bold text-white truncate">{stats.lastSync}</div>
        </div>
      </div>

      {/* Información del Sistema */}
      <div className="p-4 bg-white/5 rounded-xl border border-white/10">
        <h4 className="font-semibold text-white mb-3">Estado del Sistema</h4>
        <div className="space-y-2 text-sm">
          <div className="flex items-center justify-between">
            <span className="text-gray-300">Service Worker</span>
            <span className={isServiceWorkerSupported ? 'text-green-400' : 'text-red-400'}>
              {isServiceWorkerSupported ? 'Soportado' : 'No soportado'}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-300">Push Notifications</span>
            <span className={isPushSupported ? 'text-green-400' : 'text-red-400'}>
              {isPushSupported ? 'Soportado' : 'No soportado'}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-300">Modo Offline</span>
            <span className="text-green-400">Disponible</span>
          </div>
        </div>
      </div>

      {/* Alertas */}
      {notificationPermission === 'denied' && isPushSupported && (
        <div className="mt-4 p-4 bg-yellow-500/20 border border-yellow-400/30 rounded-xl">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-yellow-400 mt-0.5" />
            <div>
              <div className="font-semibold text-yellow-200 mb-1">
                Notificaciones Bloqueadas
              </div>
              <div className="text-sm text-yellow-300">
                Para recibir notificaciones, habilita los permisos en la configuración de tu navegador.
              </div>
            </div>
          </div>
        </div>
      )}

      {!isServiceWorkerSupported && (
        <div className="mt-4 p-4 bg-red-500/20 border border-red-400/30 rounded-xl">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-400 mt-0.5" />
            <div>
              <div className="font-semibold text-red-200 mb-1">
                Funciones PWA No Disponibles
              </div>
              <div className="text-sm text-red-300">
                Tu navegador no soporta Service Workers. Algunas funciones offline no estarán disponibles.
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PWASettings;
