import React, { useState, useEffect } from 'react';

export const PWAStatusIndicator: React.FC = () => {
  const [isStandalone, setIsStandalone] = useState(false);

  useEffect(() => {
    const checkStandaloneMode = () => {
      const standalone = window.matchMedia('(display-mode: standalone)').matches ||
                        (window.navigator as any).standalone === true ||
                        window.matchMedia('(display-mode: minimal-ui)').matches;
      
      setIsStandalone(standalone);
      
      if (standalone) {
        console.log('🎉 PWA: Ejecutándose en modo standalone');
      }
    };

    checkStandaloneMode();
    
    // Escuchar cambios
    const mediaQuery = window.matchMedia('(display-mode: standalone)');
    mediaQuery.addListener(checkStandaloneMode);

    return () => {
      mediaQuery.removeListener(checkStandaloneMode);
    };
  }, []);

  if (!isStandalone) {
    return null;
  }

  return (
    <div className="pwa-status-indicator">
      <div className="flex items-center gap-1 bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs font-medium">
        <span className="text-sm">📱</span>
        <span>App</span>
      </div>
    </div>
  );
};

export default PWAStatusIndicator;
