// 📱 Componente de instalación PWA
// Botón para instalar la app en el dispositivo

import React from 'react';
import { usePWA } from '../hooks/usePWA';

export const InstallPWAButton: React.FC = () => {
  const { isInstallable, isInstalled, install } = usePWA();

  if (isInstalled) {
    return (
      <div className="flex items-center gap-2 text-green-600 text-sm">
        <span>📱</span>
        <span>App instalada</span>
      </div>
    );
  }

  if (!isInstallable) {
    return null;
  }

  return (
    <button
      onClick={install}
      className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
    >
      <span>📱</span>
      <span>Instalar App</span>
    </button>
  );
};
