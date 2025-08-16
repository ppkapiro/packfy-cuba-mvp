/**
 * 📊 PACKFY CUBA - Configuración de Sentry v4.1
 * Monitoreo de errores y performance en tiempo real
 */

import * as Sentry from "@sentry/react";
import { BrowserTracing } from "@sentry/tracing";

// Configuración de Sentry
export const initSentry = () => {
  Sentry.init({
    dsn: import.meta.env.VITE_SENTRY_DSN || "", // Configurar en .env
    environment: import.meta.env.NODE_ENV || "development",
    debug: import.meta.env.NODE_ENV === "development",

    // Performance Monitoring
    tracesSampleRate: import.meta.env.NODE_ENV === "production" ? 0.1 : 1.0,

    // Integrations
    integrations: [
      new BrowserTracing({
        // Rutas que queremos monitorear
        routingInstrumentation: Sentry.reactRouterV6Instrumentation(
          React.useEffect,
          () => window.location,
          () => {}
        ),
      }),
    ],

    // Filtros de errores
    beforeSend(event, hint) {
      // No enviar errores de desarrollo
      if (import.meta.env.NODE_ENV === "development") {
        console.log("Sentry event (dev mode):", event);
        return null;
      }

      // Filtrar errores comunes del navegador
      const error = hint.originalException;
      if (error && typeof error === "object" && "message" in error) {
        const message = (error as Error).message;

        // Ignorar errores comunes del navegador
        const ignoredMessages = [
          "Network Error",
          "Script error",
          "ResizeObserver loop limit exceeded",
          "Non-Error promise rejection captured",
        ];

        if (ignoredMessages.some((ignored) => message.includes(ignored))) {
          return null;
        }
      }

      return event;
    },

    // Tags adicionales
    initialScope: {
      tags: {
        component: "packfy-frontend",
        version: "4.1.0",
      },
      user: {
        // Se actualizará dinámicamente al hacer login
      },
      extra: {
        buildDate: new Date().toISOString(),
        userAgent: navigator.userAgent,
      },
    },
  });
};

// Función para actualizar contexto de usuario
export const setSentryUser = (user: {
  id: string;
  email?: string;
  username?: string;
}) => {
  Sentry.setUser({
    id: user.id,
    email: user.email,
    username: user.username,
  });
};

// Función para limpiar contexto de usuario
export const clearSentryUser = () => {
  Sentry.setUser(null);
};

// Función para capturar errores personalizados
export const captureCustomError = (
  error: Error,
  context: Record<string, any> = {},
  level: "error" | "warning" | "info" = "error"
) => {
  Sentry.withScope((scope) => {
    scope.setLevel(level);
    scope.setContext("custom_context", context);
    Sentry.captureException(error);
  });
};

// Función para capturar eventos de negocio
export const captureBusinessEvent = (
  eventName: string,
  data: Record<string, any> = {}
) => {
  Sentry.addBreadcrumb({
    category: "business",
    message: eventName,
    data,
    level: "info",
  });
};

// Performance monitoring para operaciones críticas
export const trackPerformance = (operationName: string) => {
  const transaction = Sentry.startTransaction({
    name: operationName,
    op: "navigation",
  });

  return {
    finish: () => transaction.finish(),
    setStatus: (status: string) => transaction.setStatus(status),
    setData: (key: string, value: any) => transaction.setData(key, value),
  };
};

// React error boundary con Sentry
export const SentryErrorBoundary = Sentry.withErrorBoundary;

// Hook para reportar errores en React components
export const useSentryErrorHandler = () => {
  return (error: Error, errorInfo?: any) => {
    captureCustomError(error, { errorInfo }, "error");
  };
};

export default Sentry;
