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
    // Verificar si PWA está instalada
    const checkIfInstalled = () => {
      if (window.matchMedia('(display-mode: standalone)').matches || 
          (window.navigator as any).standalone === true) {
        setIsInstalled(true);
        return;
      }

      // Para Android Chrome
      if (window.matchMedia('(display-mode: minimal-ui)').matches) {
        setIsInstalled(true);
        return;
      }
    };

    // Verificar soporte PWA
    const checkPWASupport = () => {
      const isSupported = 'serviceWorker' in navigator && 'BeforeInstallPromptEvent' in window;
      setIsSupported(isSupported);
    };

    // Escuchar evento beforeinstallprompt
    const handleBeforeInstallPrompt = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e as BeforeInstallPromptEvent);
      setShowInstallButton(true);
    };

    // Escuchar cuando la app se instala
    const handleAppInstalled = () => {
      console.log('🎉 PWA: App instalada exitosamente');
      setIsInstalled(true);
      setShowInstallButton(false);
      setDeferredPrompt(null);
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

  // No mostrar nada si ya está instalada
  if (isInstalled) {
    return (
      <div className={`pwa-status installed ${className}`}>
        <div className="flex items-center gap-2 text-green-600">
          <span className="text-lg">✅</span>
          <span className="text-sm font-medium">App instalada</span>
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
