// 📱 Service Worker para PWA Packfy - VERSIÓN SIMPLIFICADA v1.3
// Evita problemas de input en móvil

const CACHE_NAME = 'packfy-v1.3';
const STATIC_ASSETS = [
  '/',
  '/manifest.json',
  '/icon-192.svg',
  '/icon-512.svg'
];

// Instalación más simple
self.addEventListener('install', (event) => {
  console.log('🚀 SW v1.3: Instalando...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(STATIC_ASSETS))
      .then(() => {
        console.log('✅ SW: Assets cacheados');
        self.skipWaiting();
      })
      .catch((error) => console.error('❌ SW: Error en instalación:', error))
  );
});

// Activación simple
self.addEventListener('activate', (event) => {
  console.log('🔄 SW v1.3: Activando...');
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((cacheName) => cacheName !== CACHE_NAME)
            .map((cacheName) => {
              console.log('🗑️ SW: Eliminando cache obsoleto:', cacheName);
              return caches.delete(cacheName);
            })
        );
      })
      .then(() => {
        console.log('✅ SW v1.3: Activado y limpio');
        return self.clients.claim();
      })
  );
});

// Fetch simplificado - SOLO para navegación y assets estáticos
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // IGNORAR requests que pueden causar problemas con input
  if (
    request.method !== 'GET' ||
    url.pathname.includes('/api/') ||
    request.headers.get('content-type')?.includes('application/json') ||
    request.destination === 'document' && request.mode === 'navigate'
  ) {
    console.log('🚫 SW: Ignorando request problemático:', url.pathname);
    return; // Dejar que el navegador maneje esto normalmente
  }
  
  // Solo cachear assets estáticos básicos
  if (STATIC_ASSETS.includes(url.pathname) || url.pathname.endsWith('.svg')) {
    event.respondWith(
      caches.match(request)
        .then((response) => {
          if (response) {
            console.log('📦 SW: Sirviendo desde cache:', url.pathname);
            return response;
          }
          
          return fetch(request)
            .then((response) => {
              if (response.status === 200) {
                const responseClone = response.clone();
                caches.open(CACHE_NAME)
                  .then((cache) => cache.put(request, responseClone));
              }
              return response;
            });
        })
        .catch(() => {
          console.log('❌ SW: Falló request para:', url.pathname);
          return new Response('Offline', { status: 503 });
        })
    );
  }
});

// Mensaje de estado
console.log('📱 SW v1.3: Service Worker simplificado cargado');
