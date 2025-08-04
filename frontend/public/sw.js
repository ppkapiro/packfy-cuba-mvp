// 📱 Service Worker para PWA Packfy
// Versión optimizada para mejor funcionamiento

const CACHE_NAME = 'packfy-v1.2';
const STATIC_ASSETS = [
  '/',
  '/manifest.json',
  '/icon-192.svg',
  '/icon-512.svg',
  '/test-pwa.html'
];

const API_CACHE = 'packfy-api-v1.2';
const DYNAMIC_CACHE = 'packfy-dynamic-v1.2';

// Instalación del Service Worker
self.addEventListener('install', (event) => {
  console.log('🚀 SW: Instalando versión mejorada...');
  event.waitUntil(
    Promise.all([
      // Cache de assets estáticos
      caches.open(CACHE_NAME).then((cache) => {
        console.log('📦 SW: Cacheando assets estáticos');
        return cache.addAll(STATIC_ASSETS);
      }),
      // Pre-cache de la aplicación principal
      caches.open(DYNAMIC_CACHE).then((cache) => {
        console.log('🎯 SW: Pre-cacheando app principal');
        return cache.add('/');
      })
    ]).then(() => {
      console.log('✅ SW: Instalado correctamente');
      self.skipWaiting();
    }).catch((error) => {
      console.error('❌ SW: Error en instalación:', error);
    })
  );
});

// Activación del Service Worker
self.addEventListener('activate', (event) => {
  console.log('🔄 SW v1.2: Activando...');
  event.waitUntil(
    Promise.all([
      // Limpiar cachés antiguos (mantener solo los actuales)
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((cacheName) => ![CACHE_NAME, API_CACHE, DYNAMIC_CACHE].includes(cacheName))
            .map((cacheName) => {
              console.log('🗑️ SW: Eliminando caché antiguo:', cacheName);
              return caches.delete(cacheName);
            })
        );
      }),
      // Tomar control inmediato de todas las páginas
      self.clients.claim()
    ]).then(() => {
      console.log('✅ SW v1.2: Activado y funcionando con estrategia mejorada');
    })
  );
});

// Interceptar requests con estrategia mejorada
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Solo manejar requests GET
  if (request.method !== 'GET') return;
  
  // Estrategias diferentes según el tipo de recurso
  if (url.pathname.includes('/api/')) {
    // API: Network First con caché
    event.respondWith(handleApiRequest(request));
  } else if (STATIC_ASSETS.some(asset => url.pathname.endsWith(asset) || url.pathname === asset)) {
    // Assets estáticos: Cache First
    event.respondWith(handleStaticAssets(request));
  } else {
    // Páginas: Network First con fallback a Cache
    event.respondWith(handlePageRequest(request));
  }
});

// Manejar requests de API
async function handleApiRequest(request) {
  try {
    // Intentar network primero
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      // Cachear respuesta exitosa
      const cache = await caches.open(API_CACHE);
      cache.put(request, networkResponse.clone());
      return networkResponse;
    }
    
    // Si network falla, intentar cache
    return await getCachedResponse(request);
  } catch (error) {
    console.log('🌐 SW: Sin conexión, usando caché para API');
    return await getCachedResponse(request);
  }
}

// Manejar assets estáticos
async function handleStaticAssets(request) {
  const cachedResponse = await caches.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }
  
  // Si no está en caché, buscar en network
  try {
    const networkResponse = await fetch(request);
    const cache = await caches.open(CACHE_NAME);
    cache.put(request, networkResponse.clone());
    return networkResponse;
  } catch (error) {
    console.error('❌ SW: Error cargando asset:', error);
    return new Response('Asset no disponible offline', { status: 404 });
  }
}

// Manejar requests de páginas
async function handlePageRequest(request) {
  try {
    // Network First
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, networkResponse.clone());
      return networkResponse;
    }
    
    return await getCachedResponse(request);
  } catch (error) {
    console.log('🌐 SW: Sin conexión, usando versión cacheada');
    const cachedResponse = await getCachedResponse(request);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Fallback a página offline
    return await getOfflinePage();
  }
}

// Obtener respuesta cacheada de cualquier caché
async function getCachedResponse(request) {
  const caches_to_check = [CACHE_NAME, API_CACHE, DYNAMIC_CACHE];
  
  for (const cacheName of caches_to_check) {
    const cache = await caches.open(cacheName);
    const cachedResponse = await cache.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
  }
  
  return null;
}

// Página offline de emergencia
async function getOfflinePage() {
  return new Response(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Packfy - Sin conexión</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; text-align: center; padding: 50px; background: #f8fafc; margin: 0; }
        .offline-container { max-width: 400px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        .icon { font-size: 64px; margin-bottom: 20px; }
        h1 { color: #3b82f6; margin-bottom: 10px; font-size: 24px; }
        h2 { color: #1f2937; margin-bottom: 15px; font-size: 20px; }
        p { color: #6b7280; line-height: 1.6; margin-bottom: 15px; }
        button { background: #3b82f6; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; margin-top: 20px; font-size: 14px; font-weight: 500; transition: background 0.2s; }
        button:hover { background: #2563eb; }
        .status { background: #fef3c7; color: #d97706; padding: 8px 16px; border-radius: 6px; font-size: 14px; margin-top: 20px; }
      </style>
    </head>
    <body>
      <div class="offline-container">
        <div class="icon">📱</div>
        <h1>Packfy</h1>
        <h2>Sin conexión a internet</h2>
        <p>No hay conexión disponible en este momento. Algunas funciones pueden estar limitadas hasta que se restaure la conexión.</p>
        <div class="status">⚠️ Modo offline activo</div>
        <button onclick="window.location.reload()">🔄 Reintentar conexión</button>
      </div>
    </body>
    </html>
  `, {
    headers: { 'Content-Type': 'text/html' }
  });
}
