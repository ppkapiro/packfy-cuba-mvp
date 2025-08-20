import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import './styles/master-premium.css'
import './styles/layout-fixes.css'
import './styles/mobile-optimized.css'
import './styles/mobile-pwa.css'

// �️ FORZAR LIMPIEZA DEL SERVICE WORKER PROBLEMÁTICO
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    // Forzar registro del Service Worker auto-destructor
    navigator.serviceWorker.register('/sw.js', { updateViaCache: 'none' })
      .then((registration) => {
        console.log('�️ SW Auto-destructor registrado:', registration.scope);

        // Forzar actualización inmediata
        registration.update().then(() => {
          console.log('🔄 Forzando actualización del SW...');
        });
      })
      .catch((error) => {
        console.log('❌ Error al registrar SW destructor:', error);
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
    <App />
  </React.StrictMode>,
)
