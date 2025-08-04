import React, { useState, useEffect } from 'react';

interface BeforeInstallPromptEvent extends Event {
  prompt(): Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed'; platform: string }>;
}

interface PWAInstallPromptProps {
  className?: string;
}

export const PWAInstallPrompt: React.FC<PWAInstallPromptProps> = ({ className = '' }) => {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [showInstallButton, setShowInstallButton] = useState(false);
  const [isInstalled, setIsInstalled] = useState(false);
  const [isSupported, setIsSupported] = useState(false);

  useEffect(() => {
    // Verificar si PWA está instalada - MEJORADO para móvil
    const checkIfInstalled = () => {
      // Método 1: Display mode standalone (más confiable)
      const isStandalone = window.matchMedia('(display-mode: standalone)').matches;
      
      // Método 2: iOS standalone
      const isIOSStandalone = (window.navigator as any).standalone === true;
      
      // Método 3: Android minimal-ui
      const isMinimalUI = window.matchMedia('(display-mode: minimal-ui)').matches;
      
      // Método 4: Verificar si viene de homescreen (Android)
      const isFromHomescreen = window.location.search.includes('homescreen=1') ||
                              document.referrer === '' && 
                              !window.history.length;
      
      // Método 5: User Agent string para Android
      const isAndroidApp = navigator.userAgent.includes('Android') && 
                          (isStandalone || isMinimalUI);
      
      console.log('🔍 PWA Detection:', {
        isStandalone,
        isIOSStandalone, 
        isMinimalUI,
        isFromHomescreen,
        isAndroidApp,
        userAgent: navigator.userAgent
      });
      
      if (isStandalone || isIOSStandalone || isMinimalUI || isFromHomescreen || isAndroidApp) {
        console.log('✅ PWA: Detectada como instalada');
        setIsInstalled(true);
        return true;
      }
      
      return false;
    };

    // Verificar soporte PWA
    const checkPWASupport = () => {
      const isSupported = 'serviceWorker' in navigator && 'BeforeInstallPromptEvent' in window;
      setIsSupported(isSupported);
    };

    // Escuchar evento beforeinstallprompt - MEJORADO
    const handleBeforeInstallPrompt = (e: Event) => {
      // Si ya está instalada, no mostrar prompt
      if (checkIfInstalled()) {
        console.log('🚫 PWA: Ya instalada, omitiendo prompt');
        return;
      }
      
      e.preventDefault();
      console.log('📱 PWA: Prompt de instalación disponible');
      setDeferredPrompt(e as BeforeInstallPromptEvent);
      setShowInstallButton(true);
    };

    // Escuchar cuando la app se instala
    const handleAppInstalled = () => {
      console.log('🎉 PWA: App instalada exitosamente');
      setIsInstalled(true);
      setShowInstallButton(false);
      setDeferredPrompt(null);
      
      // Agregar parámetro para detectar en próximas cargas
      if ('URLSearchParams' in window) {
        const url = new URL(window.location.href);
        url.searchParams.set('homescreen', '1');
        window.history.replaceState({}, '', url.toString());
      }
    };

    checkIfInstalled();
    checkPWASupport();

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    window.addEventListener('appinstalled', handleAppInstalled);

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
      window.removeEventListener('appinstalled', handleAppInstalled);
    };
  }, []);

  const handleInstallClick = async () => {
    if (!deferredPrompt) return;

    try {
      // Mostrar prompt de instalación
      await deferredPrompt.prompt();
      
      // Esperar la decisión del usuario
      const choiceResult = await deferredPrompt.userChoice;
      
      if (choiceResult.outcome === 'accepted') {
        console.log('✅ PWA: Usuario aceptó la instalación');
      } else {
        console.log('❌ PWA: Usuario rechazó la instalación');
      }
      
      // Limpiar el prompt
      setDeferredPrompt(null);
      setShowInstallButton(false);
    } catch (error) {
      console.error('❌ PWA: Error durante la instalación:', error);
    }
  };

  // Manual install instructions for iOS/other browsers
  const getManualInstallInstructions = () => {
    const userAgent = navigator.userAgent.toLowerCase();
    
    if (userAgent.includes('iphone') || userAgent.includes('ipad')) {
      return {
        platform: 'iOS Safari',
        steps: [
          'Toca el botón Compartir (⬆️) en la parte inferior',
          'Selecciona "Agregar a pantalla de inicio"',
          'Toca "Agregar" en la esquina superior derecha'
        ]
      };
    }
    
    if (userAgent.includes('android')) {
      return {
        platform: 'Android Chrome',
        steps: [
          'Toca el menú (⋮) en la esquina superior derecha',
          'Selecciona "Agregar a pantalla de inicio"',
          'Toca "Agregar" para confirmar'
        ]
      };
    }
    
    return {
      platform: 'Escritorio',
      steps: [
        'Busca el icono de instalación (⬇️) en la barra de direcciones',
        'Haz clic en "Instalar Packfy"',
        'Confirma la instalación'
      ]
    };
  };

  // Mostrar indicador claro cuando está instalada
  if (isInstalled) {
    return (
      <div className={`pwa-status installed ${className}`}>
        <div className="bg-green-100 border border-green-500 rounded-lg p-3 shadow-sm">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-green-700">
              <span className="text-xl">📱</span>
              <div>
                <div className="font-semibold text-sm">Packfy App</div>
                <div className="text-xs opacity-75">Instalada y funcionando</div>
              </div>
            </div>
            <div className="text-green-600 text-xl">✅</div>
          </div>
        </div>
      </div>
    );
  }

  // Mostrar botón de instalación automática si está disponible
  if (showInstallButton && deferredPrompt) {
    return (
      <div className={`pwa-install-prompt ${className}`}>
        <button
          onClick={handleInstallClick}
          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg shadow-lg transition-colors duration-200"
          title="Instalar Packfy como aplicación"
        >
          <span className="text-lg">📱</span>
          <span className="font-medium">Instalar App</span>
        </button>
      </div>
    );
  }

  // Mostrar instrucciones manuales para navegadores que no soportan prompt automático
  if (isSupported) {
    const instructions = getManualInstallInstructions();
    
    return (
      <div className={`pwa-manual-install ${className}`}>
        <details className="bg-blue-50 border border-blue-200 rounded-lg p-3">
          <summary className="cursor-pointer flex items-center gap-2 font-medium text-blue-700">
            <span className="text-lg">📱</span>
            <span>Instalar como App ({instructions.platform})</span>
          </summary>
          <div className="mt-3 pl-6">
            <ol className="list-decimal list-inside space-y-1 text-sm text-blue-600">
              {instructions.steps.map((step, index) => (
                <li key={index}>{step}</li>
              ))}
            </ol>
          </div>
        </details>
      </div>
    );
  }

  // No mostrar nada si PWA no está soportada
  return null;
};

export default PWAInstallPrompt;
