// 🇨🇺 PACKFY CUBA - PWA & Push Notifications Service
import { toast } from "react-hot-toast";

interface PushSubscriptionData {
  endpoint: string;
  keys: {
    p256dh: string;
    auth: string;
  };
}

interface NotificationPayload {
  title: string;
  body: string;
  icon?: string;
  badge?: string;
  tag?: string;
  requireInteraction?: boolean;
  actions?: NotificationAction[];
  data?: any;
}

interface BrowserInfo {
  userAgent: string;
  platform: string;
  language: string;
  timezone: string;
}

class PWAService {
  private vapidPublicKey: string | null = null;
  private registration: ServiceWorkerRegistration | null = null;
  private isSubscribed: boolean = false;

  constructor() {
    this.init();
  }

  // ===============================
  // INICIALIZACIÓN PWA
  // ===============================

  async init(): Promise<void> {
    if (!("serviceWorker" in navigator)) {
      console.warn("Service Worker no soportado en este navegador");
      return;
    }

    try {
      // Registrar service worker
      this.registration = await navigator.serviceWorker.register(
        "/sw-advanced.js",
        {
          scope: "/",
          updateViaCache: "none",
        }
      );

      console.log("Service Worker registrado exitosamente");

      // Configurar listeners
      this.setupServiceWorkerListeners();

      // Verificar actualizaciones
      this.checkForUpdates();

      // Inicializar notificaciones push
      await this.initPushNotifications();
    } catch (error) {
      console.error("Error registrando Service Worker:", error);
      toast.error("Error inicializando funciones offline");
    }
  }

  private setupServiceWorkerListeners(): void {
    if (!this.registration) return;

    // Listener para actualizaciones del SW
    this.registration.addEventListener("updatefound", () => {
      const newWorker = this.registration!.installing;
      if (newWorker) {
        newWorker.addEventListener("statechange", () => {
          if (
            newWorker.state === "installed" &&
            navigator.serviceWorker.controller
          ) {
            this.showUpdateAvailableNotification();
          }
        });
      }
    });

    // Listener para mensajes del SW
    navigator.serviceWorker.addEventListener("message", (event) => {
      this.handleServiceWorkerMessage(event.data);
    });

    // Listener para cambios de conexión
    window.addEventListener("online", () => {
      toast.success("Conexión restaurada");
      this.syncPendingData();
    });

    window.addEventListener("offline", () => {
      toast("Modo offline activado", {
        icon: "📡",
        duration: 3000,
      });
    });
  }

  private handleServiceWorkerMessage(data: any): void {
    const { type, payload } = data;

    switch (type) {
      case "CACHE_UPDATED":
        console.log("Cache actualizado:", payload);
        break;
      case "SYNC_COMPLETE":
        toast.success("Datos sincronizados");
        break;
      case "ERROR":
        console.error("Error del Service Worker:", payload);
        break;
    }
  }

  // ===============================
  // ACTUALIZACIONES PWA
  // ===============================

  private checkForUpdates(): void {
    if (!this.registration) return;

    // Verificar actualizaciones cada 5 minutos
    setInterval(() => {
      this.registration!.update();
    }, 5 * 60 * 1000);
  }

  private showUpdateAvailableNotification(): void {
    toast.custom(
      (t) => {
        const handleUpdate = () => {
          this.skipWaiting();
          toast.dismiss(t.id);
        };

        const handleDismiss = () => {
          toast.dismiss(t.id);
        };

        return `
        <div style="display: flex; align-items: center; gap: 12px; padding: 16px; background: white; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
          <div style="flex: 1;">
            <div style="font-weight: 600; margin-bottom: 4px;">Nueva versión disponible</div>
            <div style="font-size: 14px; opacity: 0.75;">Actualiza para obtener las últimas mejoras</div>
          </div>
          <div style="display: flex; gap: 8px;">
            <button onclick="${handleUpdate.toString()}()" style="padding: 6px 12px; background: #3b82f6; color: white; border: none; border-radius: 6px; font-size: 14px; cursor: pointer;">
              Actualizar
            </button>
            <button onclick="${handleDismiss.toString()}()" style="padding: 6px 12px; background: #d1d5db; color: #374151; border: none; border-radius: 6px; font-size: 14px; cursor: pointer;">
              Después
            </button>
          </div>
        </div>
      `;
      },
      {
        duration: 10000,
        position: "bottom-center",
      }
    );
  }

  private skipWaiting(): void {
    if (!this.registration?.waiting) return;

    this.registration.waiting.postMessage({ type: "SKIP_WAITING" });
    window.location.reload();
  }

  // ===============================
  // NOTIFICACIONES PUSH
  // ===============================

  async initPushNotifications(): Promise<void> {
    if (!("Notification" in window) || !("PushManager" in window)) {
      console.warn("Notificaciones push no soportadas");
      return;
    }

    try {
      // Obtener clave pública VAPID
      await this.getVapidPublicKey();

      // Verificar suscripción existente
      await this.checkSubscriptionStatus();
    } catch (error) {
      console.error("Error inicializando notificaciones push:", error);
    }
  }

  private async getVapidPublicKey(): Promise<void> {
    try {
      const response = await fetch("/api/push/vapid-key/", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        this.vapidPublicKey = data.publicKey;
      }
    } catch (error) {
      console.error("Error obteniendo clave VAPID:", error);
    }
  }

  private async checkSubscriptionStatus(): Promise<void> {
    if (!this.registration) return;

    try {
      const subscription =
        await this.registration.pushManager.getSubscription();
      this.isSubscribed = !!subscription;

      if (subscription) {
        console.log("Suscripción push activa");
        // Verificar si la suscripción está sincronizada con el servidor
        await this.syncSubscriptionWithServer(subscription);
      }
    } catch (error) {
      console.error("Error verificando suscripción push:", error);
    }
  }

  async requestNotificationPermission(): Promise<boolean> {
    if (!("Notification" in window)) {
      toast.error("Notificaciones no soportadas en este navegador");
      return false;
    }

    if (Notification.permission === "granted") {
      return true;
    }

    if (Notification.permission === "denied") {
      toast.error(
        "Notificaciones bloqueadas. Habilita en configuración del navegador."
      );
      return false;
    }

    const permission = await Notification.requestPermission();

    if (permission === "granted") {
      toast.success("Notificaciones habilitadas");
      return true;
    } else {
      toast.error("Permisos de notificación denegados");
      return false;
    }
  }

  async subscribeToPush(): Promise<boolean> {
    if (!this.registration || !this.vapidPublicKey) {
      console.error("Service Worker o VAPID key no disponibles");
      return false;
    }

    try {
      // Solicitar permisos
      const hasPermission = await this.requestNotificationPermission();
      if (!hasPermission) return false;

      // Crear suscripción
      const subscription = await this.registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: this.urlBase64ToUint8Array(this.vapidPublicKey)
          .buffer as ArrayBuffer,
      });

      // Enviar suscripción al servidor
      const success = await this.sendSubscriptionToServer(subscription);

      if (success) {
        this.isSubscribed = true;
        toast.success("Notificaciones activadas");
        return true;
      } else {
        await subscription.unsubscribe();
        return false;
      }
    } catch (error) {
      console.error("Error suscribiendo a notificaciones push:", error);
      toast.error("Error activando notificaciones");
      return false;
    }
  }

  async unsubscribeFromPush(): Promise<boolean> {
    if (!this.registration) return false;

    try {
      const subscription =
        await this.registration.pushManager.getSubscription();

      if (subscription) {
        // Desuscribir del navegador
        await subscription.unsubscribe();

        // Notificar al servidor
        await this.removeSubscriptionFromServer(subscription);

        this.isSubscribed = false;
        toast.success("Notificaciones desactivadas");
        return true;
      }

      return false;
    } catch (error) {
      console.error("Error desuscribiendo de notificaciones:", error);
      toast.error("Error desactivando notificaciones");
      return false;
    }
  }

  private async sendSubscriptionToServer(
    subscription: PushSubscription
  ): Promise<boolean> {
    try {
      const subscriptionData: PushSubscriptionData = {
        endpoint: subscription.endpoint,
        keys: {
          p256dh: this.arrayBufferToBase64(subscription.getKey("p256dh")!),
          auth: this.arrayBufferToBase64(subscription.getKey("auth")!),
        },
      };

      const browserInfo: BrowserInfo = {
        userAgent: navigator.userAgent,
        platform: navigator.platform,
        language: navigator.language,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      };

      const response = await fetch("/api/push/subscribe/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          subscription: subscriptionData,
          browserInfo,
        }),
      });

      return response.ok;
    } catch (error) {
      console.error("Error enviando suscripción al servidor:", error);
      return false;
    }
  }

  private async removeSubscriptionFromServer(
    subscription: PushSubscription
  ): Promise<boolean> {
    try {
      const response = await fetch("/api/push/subscribe/", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          endpoint: subscription.endpoint,
        }),
      });

      return response.ok;
    } catch (error) {
      console.error("Error removiendo suscripción del servidor:", error);
      return false;
    }
  }

  private async syncSubscriptionWithServer(
    subscription: PushSubscription
  ): Promise<void> {
    // Reenviar suscripción para asegurar sincronización
    await this.sendSubscriptionToServer(subscription);
  }

  async sendTestNotification(): Promise<void> {
    try {
      const response = await fetch("/api/push/test/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (response.ok) {
        toast.success("Notificación de prueba enviada");
      } else {
        toast.error("Error enviando notificación de prueba");
      }
    } catch (error) {
      console.error("Error enviando notificación de prueba:", error);
      toast.error("Error enviando notificación de prueba");
    }
  }

  // ===============================
  // SINCRONIZACIÓN OFFLINE
  // ===============================

  async syncPendingData(): Promise<void> {
    if (!this.registration) return;

    try {
      // Verificar si el browser soporta background sync
      if ("sync" in this.registration) {
        // Registrar tareas de sincronización
        await (this.registration as any).sync.register("shipment-sync");
        await (this.registration as any).sync.register("metrics-sync");

        console.log("Sincronización en background registrada");
      } else {
        // Fallback: sincronización manual
        console.log("Background sync no soportado, sincronizando manualmente");
        this.manualSync();
      }
    } catch (error) {
      console.error("Error registrando sincronización:", error);
    }
  }

  private async manualSync(): Promise<void> {
    // Implementación de sincronización manual como fallback
    try {
      // Aquí iría la lógica de sincronización manual
      console.log("Ejecutando sincronización manual");
    } catch (error) {
      console.error("Error en sincronización manual:", error);
    }
  }

  async cacheShipmentData(shipmentData: any): Promise<void> {
    if (!this.registration?.active) return;

    this.registration.active.postMessage({
      type: "CACHE_SHIPMENT",
      payload: shipmentData,
    });
  }

  // ===============================
  // INSTALACIÓN PWA
  // ===============================

  async showInstallPrompt(): Promise<boolean> {
    const deferredPrompt = (window as any).deferredPrompt;

    if (!deferredPrompt) {
      toast("La aplicación ya está instalada o no se puede instalar", {
        icon: "📱",
      });
      return false;
    }

    try {
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;

      if (outcome === "accepted") {
        toast.success("¡Aplicación instalada exitosamente!");
        (window as any).deferredPrompt = null;
        return true;
      } else {
        toast("Instalación cancelada", { icon: "❌" });
        return false;
      }
    } catch (error) {
      console.error("Error durante la instalación:", error);
      toast.error("Error durante la instalación");
      return false;
    }
  }

  // ===============================
  // UTILIDADES
  // ===============================

  private urlBase64ToUint8Array(base64String: string): Uint8Array {
    const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
    const base64 = (base64String + padding)
      .replace(/-/g, "+")
      .replace(/_/g, "/");

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }

  private arrayBufferToBase64(buffer: ArrayBuffer): string {
    const bytes = new Uint8Array(buffer);
    let binary = "";
    for (let i = 0; i < bytes.byteLength; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
  }

  // ===============================
  // GETTERS
  // ===============================

  get isServiceWorkerSupported(): boolean {
    return "serviceWorker" in navigator;
  }

  get isPushSupported(): boolean {
    return "PushManager" in window && "Notification" in window;
  }

  get isInstallable(): boolean {
    return !!(window as any).deferredPrompt;
  }

  get notificationPermission(): NotificationPermission {
    return Notification.permission;
  }

  get isOffline(): boolean {
    return !navigator.onLine;
  }

  get isPushSubscribed(): boolean {
    return this.isSubscribed;
  }
}

// Instancia global del servicio PWA
export const pwaService = new PWAService();

// Hook React para usar el servicio PWA
import { useState, useEffect } from "react";

export function usePWA() {
  const [isOffline, setIsOffline] = useState(!navigator.onLine);
  const [isInstallable, setIsInstallable] = useState(false);
  const [isPushSubscribed, setIsPushSubscribed] = useState(false);
  const [notificationPermission, setNotificationPermission] =
    useState<NotificationPermission>(
      "Notification" in window ? Notification.permission : "denied"
    );

  useEffect(() => {
    // Listeners para estado de conexión
    const handleOnline = () => setIsOffline(false);
    const handleOffline = () => setIsOffline(true);

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    // Listener para prompt de instalación
    const handleBeforeInstallPrompt = (e: Event) => {
      e.preventDefault();
      (window as any).deferredPrompt = e;
      setIsInstallable(true);
    };

    window.addEventListener("beforeinstallprompt", handleBeforeInstallPrompt);

    // Listener para app instalada
    const handleAppInstalled = () => {
      setIsInstallable(false);
      (window as any).deferredPrompt = null;
      toast.success("¡Aplicación instalada exitosamente!");
    };

    window.addEventListener("appinstalled", handleAppInstalled);

    // Verificar estado inicial de notificaciones push
    const checkPushStatus = async () => {
      if (pwaService.isPushSupported) {
        // Actualizar estado periódicamente
        setIsPushSubscribed(pwaService.isPushSubscribed);
        setNotificationPermission(pwaService.notificationPermission);
      }
    };

    checkPushStatus();

    // Cleanup
    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
      window.removeEventListener(
        "beforeinstallprompt",
        handleBeforeInstallPrompt
      );
      window.removeEventListener("appinstalled", handleAppInstalled);
    };
  }, []);

  const subscribeToPush = async () => {
    const success = await pwaService.subscribeToPush();
    setIsPushSubscribed(success);
    if (success) {
      setNotificationPermission("granted");
    }
    return success;
  };

  const unsubscribeFromPush = async () => {
    const success = await pwaService.unsubscribeFromPush();
    setIsPushSubscribed(!success);
    return success;
  };

  const installApp = async () => {
    const success = await pwaService.showInstallPrompt();
    if (success) {
      setIsInstallable(false);
    }
    return success;
  };

  return {
    // Estado
    isOffline,
    isInstallable,
    isPushSubscribed,
    notificationPermission,
    isServiceWorkerSupported: pwaService.isServiceWorkerSupported,
    isPushSupported: pwaService.isPushSupported,

    // Acciones
    subscribeToPush,
    unsubscribeFromPush,
    installApp,
    sendTestNotification: pwaService.sendTestNotification.bind(pwaService),
    syncPendingData: pwaService.syncPendingData.bind(pwaService),
    cacheShipmentData: pwaService.cacheShipmentData.bind(pwaService),
  };
}
