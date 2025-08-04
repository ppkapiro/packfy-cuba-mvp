// 📱 Service Worker para PWA Packfy
// Versión optimizada para mejor funcionamiento

const CACHE_NAME = 'packfy-v1.1';
const STATIC_ASSETS = [
  '/',
  '/manifest.json',
  '/icon-192.svg',
  '/icon-512.svg'
];

// Instalación del Service Worker
self.addEventListener('install', (event) => {
  console.log('🚀 SW: Instalando...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('📦 SW: Cacheando assets estáticos');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('✅ SW: Instalado correctamente');
        self.skipWaiting();
      })
      .catch((error) => {
        console.error('❌ SW: Error en instalación:', error);
      })
  );
});

// Activación del Service Worker
self.addEventListener('activate', (event) => {
  console.log('🔄 SW: Activando...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((cacheName) => cacheName !== CACHE_NAME)
          .map((cacheName) => {
            console.log('🗑️ SW: Eliminando caché antiguo:', cacheName);
            return caches.delete(cacheName);
          })
      );
    }).then(() => {
      console.log('✅ SW: Activado correctamente');
      return self.clients.claim();
    })
  );
});

// Interceptar requests
self.addEventListener('fetch', (event) => {
  // Solo manejar requests GET
  if (event.request.method !== 'GET') return;
  
  // Estrategia Network First para la app
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Si la respuesta es exitosa, guardarla en caché
        if (response.status === 200 && event.request.url.startsWith('http')) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME)
            .then((cache) => cache.put(event.request, responseClone));
        }
        return response;
      })
      .catch(() => {
        // Si no hay conexión, intentar servir desde caché
        return caches.match(event.request)
          .then((cachedResponse) => {
            if (cachedResponse) {
              return cachedResponse;
            }
            // Fallback para navegación
            if (event.request.destination === 'document') {
              return caches.match('/');
            }
          });
      })
  );
});
