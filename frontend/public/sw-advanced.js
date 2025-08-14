// 🇨🇺 PACKFY CUBA - Service Worker Avanzado v4.0

const CACHE_NAME = "packfy-cuba-v4.0";
const CACHE_VERSION = "4.0.0";
const STATIC_CACHE = `${CACHE_NAME}-static`;
const DYNAMIC_CACHE = `${CACHE_NAME}-dynamic`;
const API_CACHE = `${CACHE_NAME}-api`;

// Recursos para cache estático
const STATIC_ASSETS = [
  "/",
  "/manifest.json",
  "/offline.html",
  "/icons/icon-192.svg",
  "/icons/icon-512.svg",
  // CSS y JS principales se cachearán automáticamente por Vite
];

// Patrones de URL para diferentes estrategias de cache
const CACHE_STRATEGIES = {
  // Cache First - Para assets estáticos
  CACHE_FIRST: [
    /\.(css|js|woff2?|ttf|eot|svg|png|jpg|jpeg|gif|webp|ico)$/,
    /\/assets\//,
  ],

  // Network First - Para contenido dinámico
  NETWORK_FIRST: [/\/api\/.*envios/, /\/api\/.*rastreo/, /\/api\/.*auth/],

  // Stale While Revalidate - Para datos que pueden ser ligeramente obsoletos
  STALE_WHILE_REVALIDATE: [/\/api\/.*estadisticas/, /\/api\/.*empresas/],
};

// ===============================
// INSTALACIÓN DEL SERVICE WORKER
// ===============================
self.addEventListener("install", (event) => {
  console.log("[SW] Installing Service Worker v" + CACHE_VERSION);

  event.waitUntil(
    Promise.all([
      // Cache de recursos estáticos
      caches.open(STATIC_CACHE).then((cache) => {
        console.log("[SW] Caching static assets");
        return cache.addAll(STATIC_ASSETS);
      }),

      // Skip waiting para activar inmediatamente
      self.skipWaiting(),
    ])
  );
});

// ===============================
// ACTIVACIÓN DEL SERVICE WORKER
// ===============================
self.addEventListener("activate", (event) => {
  console.log("[SW] Activating Service Worker v" + CACHE_VERSION);

  event.waitUntil(
    Promise.all([
      // Limpiar caches antiguos
      cleanupOldCaches(),

      // Tomar control de todos los clientes
      self.clients.claim(),

      // Configurar notificaciones push
      setupPushNotifications(),
    ])
  );
});

async function cleanupOldCaches() {
  const cacheNames = await caches.keys();
  const oldCaches = cacheNames.filter(
    (name) => name.startsWith("packfy-cuba-") && !name.includes(CACHE_VERSION)
  );

  console.log("[SW] Cleaning up old caches:", oldCaches);

  return Promise.all(oldCaches.map((cacheName) => caches.delete(cacheName)));
}

// ===============================
// ESTRATEGIAS DE FETCH
// ===============================
self.addEventListener("fetch", (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Solo manejar requests HTTP/HTTPS
  if (!request.url.startsWith("http")) return;

  // Determinar estrategia basada en la URL
  const strategy = determineStrategy(request.url);

  event.respondWith(handleRequest(request, strategy));
});

function determineStrategy(url) {
  for (const [strategy, patterns] of Object.entries(CACHE_STRATEGIES)) {
    if (patterns.some((pattern) => pattern.test(url))) {
      return strategy;
    }
  }
  return "NETWORK_FIRST"; // Estrategia por defecto
}

async function handleRequest(request, strategy) {
  switch (strategy) {
    case "CACHE_FIRST":
      return cacheFirst(request);
    case "NETWORK_FIRST":
      return networkFirst(request);
    case "STALE_WHILE_REVALIDATE":
      return staleWhileRevalidate(request);
    default:
      return networkFirst(request);
  }
}

// ===============================
// IMPLEMENTACIÓN DE ESTRATEGIAS
// ===============================

async function cacheFirst(request) {
  try {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    const networkResponse = await fetch(request);
    await cacheResponse(request, networkResponse.clone(), STATIC_CACHE);
    return networkResponse;
  } catch (error) {
    console.error("[SW] Cache First error:", error);
    return getOfflineResponse(request);
  }
}

async function networkFirst(request) {
  try {
    const networkResponse = await fetch(request);

    // Cache solo responses exitosas
    if (networkResponse.ok) {
      await cacheResponse(request, networkResponse.clone(), DYNAMIC_CACHE);
    }

    return networkResponse;
  } catch (error) {
    console.log("[SW] Network failed, trying cache:", error);

    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    return getOfflineResponse(request);
  }
}

async function staleWhileRevalidate(request) {
  const cachedResponse = caches.match(request);

  const networkResponse = fetch(request)
    .then((response) => {
      if (response.ok) {
        cacheResponse(request, response.clone(), API_CACHE);
      }
      return response;
    })
    .catch((error) => {
      console.warn("[SW] Stale While Revalidate network error:", error);
      return null;
    });

  return cachedResponse || networkResponse || getOfflineResponse(request);
}

async function cacheResponse(request, response, cacheName) {
  // No cachear requests no-GET o responses no-ok
  if (request.method !== "GET" || !response.ok) return;

  try {
    const cache = await caches.open(cacheName);
    await cache.put(request, response);
  } catch (error) {
    console.error("[SW] Error caching response:", error);
  }
}

function getOfflineResponse(request) {
  const url = new URL(request.url);

  // Para navegación, mostrar página offline
  if (request.mode === "navigate") {
    return caches.match("/offline.html");
  }

  // Para API, devolver response JSON offline
  if (url.pathname.startsWith("/api/")) {
    return new Response(
      JSON.stringify({
        error: "Sin conexión",
        message: "Esta función requiere conexión a internet",
        offline: true,
      }),
      {
        status: 503,
        statusText: "Service Unavailable",
        headers: { "Content-Type": "application/json" },
      }
    );
  }

  // Para assets, devolver respuesta básica
  return new Response("", { status: 404 });
}

// ===============================
// NOTIFICACIONES PUSH
// ===============================

self.addEventListener("push", (event) => {
  console.log("[SW] Push message received");

  let notificationData = {
    title: "PACKFY CUBA",
    body: "Nueva notificación",
    icon: "/icons/icon-192.svg",
    badge: "/icons/badge-72x72.png",
    tag: "packfy-notification",
    requireInteraction: true,
    actions: [],
  };

  if (event.data) {
    try {
      const data = event.data.json();
      notificationData = { ...notificationData, ...data };

      // Personalizar según tipo de notificación
      notificationData = customizeNotification(data);
    } catch (error) {
      console.error("[SW] Error parsing push data:", error);
    }
  }

  event.waitUntil(
    self.registration.showNotification(notificationData.title, notificationData)
  );
});

function customizeNotification(data) {
  const { type, shipment, status } = data;

  switch (type) {
    case "shipment_status_update":
      return {
        title: "📦 Estado de Envío Actualizado",
        body: `Tu envío ${shipment?.numero_guia} está ahora: ${status}`,
        icon: "/icons/shipment-notification.png",
        tag: `shipment-${shipment?.id}`,
        actions: [
          {
            action: "track",
            title: "Rastrear",
            icon: "/icons/track-action.png",
          },
          {
            action: "view",
            title: "Ver Detalles",
            icon: "/icons/view-action.png",
          },
        ],
        data: { shipmentId: shipment?.id, type: "shipment_update" },
      };

    case "new_shipment":
      return {
        title: "📦 Nuevo Envío Creado",
        body: `Envío ${shipment?.numero_guia} creado exitosamente`,
        icon: "/icons/new-shipment.png",
        tag: `new-shipment-${shipment?.id}`,
        actions: [
          {
            action: "view",
            title: "Ver Envío",
            icon: "/icons/view-action.png",
          },
        ],
        data: { shipmentId: shipment?.id, type: "new_shipment" },
      };

    case "delivery_reminder":
      return {
        title: "🚚 Recordatorio de Entrega",
        body: `Tu envío ${shipment?.numero_guia} será entregado hoy`,
        icon: "/icons/delivery-reminder.png",
        tag: `delivery-${shipment?.id}`,
        requireInteraction: true,
        actions: [
          {
            action: "confirm",
            title: "Confirmar Recepción",
            icon: "/icons/confirm-action.png",
          },
          {
            action: "reschedule",
            title: "Reprogramar",
            icon: "/icons/reschedule-action.png",
          },
        ],
        data: { shipmentId: shipment?.id, type: "delivery_reminder" },
      };

    default:
      return data;
  }
}

// ===============================
// MANEJO DE CLICKS EN NOTIFICACIONES
// ===============================

self.addEventListener("notificationclick", (event) => {
  console.log("[SW] Notification clicked:", event);

  event.notification.close();

  const { action, notification } = event;
  const data = notification.data || {};

  event.waitUntil(handleNotificationClick(action, data));
});

async function handleNotificationClick(action, data) {
  const { shipmentId, type } = data;

  let url = "/";

  switch (action) {
    case "track":
      url = `/rastreo?guia=${shipmentId}`;
      break;
    case "view":
      url = `/envios/${shipmentId}`;
      break;
    case "confirm":
      url = `/envios/${shipmentId}/confirmar`;
      break;
    case "reschedule":
      url = `/envios/${shipmentId}/reprogramar`;
      break;
    default:
      // Click en la notificación sin acción específica
      if (type === "shipment_update") {
        url = `/envios/${shipmentId}`;
      } else if (type === "new_shipment") {
        url = `/envios`;
      }
  }

  // Abrir o enfocar ventana existente
  const clients = await self.clients.matchAll({ type: "window" });

  for (const client of clients) {
    if (client.url.includes(url) && "focus" in client) {
      return client.focus();
    }
  }

  // Abrir nueva ventana si no existe
  if (self.clients.openWindow) {
    return self.clients.openWindow(url);
  }
}

// ===============================
// SINCRONIZACIÓN EN BACKGROUND
// ===============================

self.addEventListener("sync", (event) => {
  console.log("[SW] Background sync:", event.tag);

  switch (event.tag) {
    case "shipment-sync":
      event.waitUntil(syncPendingShipments());
      break;
    case "metrics-sync":
      event.waitUntil(syncMetrics());
      break;
    default:
      console.log("[SW] Unknown sync tag:", event.tag);
  }
});

async function syncPendingShipments() {
  try {
    // Obtener datos pendientes del IndexedDB
    const pendingData = await getPendingData("shipments");

    for (const shipment of pendingData) {
      try {
        const response = await fetch("/api/envios/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(shipment.data),
        });

        if (response.ok) {
          await removePendingData("shipments", shipment.id);
          console.log("[SW] Synced shipment:", shipment.id);
        }
      } catch (error) {
        console.error("[SW] Error syncing shipment:", error);
      }
    }
  } catch (error) {
    console.error("[SW] Error in shipment sync:", error);
  }
}

async function syncMetrics() {
  try {
    // Enviar métricas de uso offline
    const metrics = await getPendingData("metrics");

    if (metrics.length > 0) {
      await fetch("/api/analytics/offline-metrics/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(metrics),
      });

      await clearPendingData("metrics");
      console.log("[SW] Synced offline metrics");
    }
  } catch (error) {
    console.error("[SW] Error syncing metrics:", error);
  }
}

// ===============================
// UTILIDADES PARA INDEXEDDB
// ===============================

async function getPendingData(store) {
  // Implementación simplificada - en producción usar IDB library
  return [];
}

async function removePendingData(store, id) {
  // Implementación para remover datos específicos
}

async function clearPendingData(store) {
  // Implementación para limpiar store completo
}

// ===============================
// CONFIGURACIÓN INICIAL
// ===============================

async function setupPushNotifications() {
  try {
    // Solicitar suscripción a notificaciones si no existe
    const subscription = await self.registration.pushManager.getSubscription();

    if (!subscription) {
      console.log("[SW] No push subscription found");
      return;
    }

    // Enviar suscripción al servidor
    await fetch("/api/push/subscribe/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        subscription: subscription.toJSON(),
      }),
    });

    console.log("[SW] Push subscription updated");
  } catch (error) {
    console.error("[SW] Error setting up push notifications:", error);
  }
}

// ===============================
// MENSAJES DESDE LA APLICACIÓN
// ===============================

self.addEventListener("message", (event) => {
  const { type, payload } = event.data;

  switch (type) {
    case "SKIP_WAITING":
      self.skipWaiting();
      break;

    case "GET_VERSION":
      event.ports[0].postMessage({ version: CACHE_VERSION });
      break;

    case "CLEAR_CACHE":
      clearAllCaches().then(() => {
        event.ports[0].postMessage({ success: true });
      });
      break;

    case "CACHE_SHIPMENT":
      cacheShipmentData(payload);
      break;

    default:
      console.log("[SW] Unknown message type:", type);
  }
});

async function clearAllCaches() {
  const cacheNames = await caches.keys();
  return Promise.all(cacheNames.map((cacheName) => caches.delete(cacheName)));
}

async function cacheShipmentData(shipmentData) {
  try {
    const cache = await caches.open(API_CACHE);
    const response = new Response(JSON.stringify(shipmentData), {
      headers: { "Content-Type": "application/json" },
    });
    await cache.put(`/api/envios/${shipmentData.id}/`, response);
  } catch (error) {
    console.error("[SW] Error caching shipment data:", error);
  }
}
