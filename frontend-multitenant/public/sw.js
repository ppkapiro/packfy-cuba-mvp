// 🗑️ Service Worker AUTO-DESTRUCTOR - Elimina cache y se desregistra
console.log(
  "🗑️ SW: Iniciando auto-destrucción para eliminar interferencias..."
);

// Auto-desregistro inmediato
self.addEventListener("install", (event) => {
  console.log("🗑️ SW: Instalando para auto-destruirse...");
  event.waitUntil(
    caches
      .keys()
      .then((cacheNames) => {
        console.log("🧹 SW: Eliminando todos los caches:", cacheNames);
        return Promise.all(
          cacheNames.map((cacheName) => {
            console.log("🗑️ SW: Eliminando cache:", cacheName);
            return caches.delete(cacheName);
          })
        );
      })
      .then(() => {
        console.log("✅ SW: Todos los caches eliminados");
        self.skipWaiting();
      })
  );
});

// Activación y auto-desregistro
self.addEventListener("activate", (event) => {
  console.log("🗑️ SW: Activando para auto-destruirse...");
  event.waitUntil(
    self.registration
      .unregister()
      .then(() => {
        console.log("✅ SW: Desregistrado exitosamente");
        return self.clients.matchAll();
      })
      .then((clients) => {
        console.log("🔄 SW: Recargando clientes para aplicar cambios");
        clients.forEach((client) => client.navigate(client.url));
      })
  );
});

console.log("🗑️ SW: Auto-destructor cargado");
