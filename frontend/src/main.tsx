import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import { ThemeProvider } from './contexts/ThemeContext'
// 🇨🇺 CSS OPTIMIZADO - ARCHIVO ÚNICO PARA MEJOR RENDIMIENTO
import './styles/packfy-master-v6.css' // ✅ ARCHIVO MASTER ÚNICO Y OPTIMIZADO

// 📱 Service Worker PWA optimizado para móvil
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('🚀 SW v2.0 registrado exitosamente:', registration.scope);

        // Verificar actualizaciones del SW
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          if (newWorker) {
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                console.log('🔄 Nueva versión disponible. Recarga para actualizar.');
                // Opcionalmente mostrar notificación de actualización
              }
            });
          }
        });
      })
      .catch((error) => {
        console.log('❌ Error al registrar SW:', error);
      });

    // 📱 Detección de instalación PWA - MEJORADO PARA CHROME
    let deferredPrompt: any = null;

    window.addEventListener('beforeinstallprompt', (e: Event) => {
      console.log('📱 PWA listo para instalación');
      e.preventDefault();
      deferredPrompt = e;

      // Mostrar prompt INMEDIATAMENTE cuando esté disponible
      console.log('💡 Mostrando prompt de instalación INMEDIATO');
      setTimeout(() => {
        if (deferredPrompt) {
          deferredPrompt.prompt();
          deferredPrompt.userChoice.then((choiceResult: any) => {
            if (choiceResult.outcome === 'accepted') {
              console.log('✅ Usuario aceptó instalación PWA');
            } else {
              console.log('❌ Usuario rechazó instalación PWA');
              // Intentar de nuevo en 10 segundos
              setTimeout(() => {
                if (deferredPrompt) {
                  console.log('🔄 Segundo intento de instalación...');
                  deferredPrompt.prompt();
                }
              }, 10000);
            }
            deferredPrompt = null;
          });
        }
      }, 1000); // Reducido a 1 segundo
    });

    // Confirmar instalación exitosa
    window.addEventListener('appinstalled', () => {
      console.log('🎉 Packfy Cuba PWA instalada exitosamente');
    });
  });
} else {
  console.log('❌ Service Workers no soportados en este navegador');
}

// 📱 Optimizaciones para dispositivos móviles
if (window.DeviceMotionEvent) {
  console.log('📱 Dispositivo móvil detectado - Optimizaciones activadas');
}

// 🎯 Prevenir zoom accidental en iOS
document.addEventListener('gesturestart', function (e) {
  e.preventDefault();
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </React.StrictMode>,
)
