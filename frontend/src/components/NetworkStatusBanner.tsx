import React from 'react';
import { useNetworkStatus } from '../hooks/useNetworkStatus';

interface NetworkStatusBannerProps {
  className?: string;
}

export const NetworkStatusBanner: React.FC<NetworkStatusBannerProps> = ({ className = '' }) => {
  const { isOnline, isSlowConnection, effectiveType } = useNetworkStatus();

  // No mostrar nada si hay conexión normal
  if (isOnline && !isSlowConnection) {
    return null;
  }

  return (
    <div className={`network-status-banner ${className}`}>
      {!isOnline ? (
        // Sin conexión
        <div className="bg-red-500 text-white px-4 py-2 text-center text-sm font-medium">
          <span className="inline-flex items-center gap-2">
            <span className="text-lg">📴</span>
            <span>Sin conexión - Modo offline activo</span>
          </span>
        </div>
      ) : isSlowConnection ? (
        // Conexión lenta
        <div className="bg-yellow-500 text-white px-4 py-2 text-center text-sm font-medium">
          <span className="inline-flex items-center gap-2">
            <span className="text-lg">🐌</span>
            <span>
              Conexión lenta ({effectiveType}) - Algunas funciones pueden tardar más
            </span>
          </span>
        </div>
      ) : null}
    </div>
  );
};

export default NetworkStatusBanner;
