import { useState, useEffect } from 'react';

interface NetworkStatus {
  isOnline: boolean;
  isSlowConnection: boolean;
  effectiveType: string | null;
  downlink: number | null;
}

export const useNetworkStatus = (): NetworkStatus => {
  const [networkStatus, setNetworkStatus] = useState<NetworkStatus>({
    isOnline: navigator.onLine,
    isSlowConnection: false,
    effectiveType: null,
    downlink: null
  });

  useEffect(() => {
    const updateNetworkStatus = () => {
      const connection = (navigator as any).connection || 
                        (navigator as any).mozConnection || 
                        (navigator as any).webkitConnection;

      const isSlowConnection = connection ? 
        (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g') : 
        false;

      setNetworkStatus({
        isOnline: navigator.onLine,
        isSlowConnection,
        effectiveType: connection?.effectiveType || null,
        downlink: connection?.downlink || null
      });
    };

    const handleOnline = () => {
      console.log('🌐 Conexión restaurada');
      updateNetworkStatus();
    };

    const handleOffline = () => {
      console.log('📴 Sin conexión');
      updateNetworkStatus();
    };

    const handleConnectionChange = () => {
      updateNetworkStatus();
    };

    // Inicializar estado
    updateNetworkStatus();

    // Escuchar cambios de conectividad
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Escuchar cambios en la calidad de conexión
    const connection = (navigator as any).connection;
    if (connection) {
      connection.addEventListener('change', handleConnectionChange);
    }

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
      if (connection) {
        connection.removeEventListener('change', handleConnectionChange);
      }
    };
  }, []);

  return networkStatus;
};

export default useNetworkStatus;
