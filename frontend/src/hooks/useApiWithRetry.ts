import { useState, useCallback } from "react";

interface RetryOptions {
  maxRetries?: number;
  baseDelay?: number;
  maxDelay?: number;
  backoffMultiplier?: number;
  retryCondition?: (error: any) => boolean;
}

interface UseApiWithRetryResult<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  execute: (...args: any[]) => Promise<void>;
  retry: () => Promise<void>;
  retryCount: number;
}

const defaultOptions: Required<RetryOptions> = {
  maxRetries: 3,
  baseDelay: 1000,
  maxDelay: 10000,
  backoffMultiplier: 2,
  retryCondition: (error: any) => {
    // Reintentar para errores de red, timeouts, 5xx
    if (!error.status) return true; // Network errors
    return error.status >= 500 || error.status === 408; // Server errors or timeout
  },
};

export function useApiWithRetry<T = any>(
  apiFunction: (
    ...args: any[]
  ) => Promise<{ data?: T; error?: string; status: number }>,
  options: RetryOptions = {}
): UseApiWithRetryResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);
  const [lastArgs, setLastArgs] = useState<any[]>([]);

  const opts = { ...defaultOptions, ...options };

  const sleep = (ms: number) =>
    new Promise((resolve) => setTimeout(resolve, ms));

  const calculateDelay = (attempt: number): number => {
    const delay = opts.baseDelay * Math.pow(opts.backoffMultiplier, attempt);
    return Math.min(delay, opts.maxDelay);
  };

  const execute = useCallback(
    async (...args: any[]) => {
      setLastArgs(args);
      setLoading(true);
      setError(null);

      let lastError: any = null;
      let attempt = 0;

      while (attempt <= opts.maxRetries) {
        try {
          console.log(
            `🔄 API call attempt ${attempt + 1}/${opts.maxRetries + 1}`,
            { args }
          );

          const result = await apiFunction(...args);

          if (result.error && opts.retryCondition(result)) {
            throw new Error(result.error);
          }

          if (result.error) {
            // Error que no debe reintentarse
            setError(result.error);
            setRetryCount(attempt);
            setLoading(false);
            return;
          }

          // Éxito
          setData(result.data || null);
          setError(null);
          setRetryCount(attempt);
          setLoading(false);

          if (attempt > 0) {
            console.log(`✅ API call succeeded after ${attempt} retries`);
          }

          return;
        } catch (err: any) {
          lastError = err;
          console.warn(
            `⚠️ API call attempt ${attempt + 1} failed:`,
            err.message
          );

          if (attempt === opts.maxRetries || !opts.retryCondition(err)) {
            break;
          }

          const delay = calculateDelay(attempt);
          console.log(`⏱️ Retrying in ${delay}ms...`);
          await sleep(delay);
          attempt++;
        }
      }

      // Todos los intentos fallaron
      setError(lastError?.message || "Error desconocido");
      setRetryCount(attempt);
      setLoading(false);

      console.error(`❌ API call failed after ${attempt} retries:`, lastError);
    },
    [apiFunction, opts]
  );

  const retry = useCallback(async () => {
    if (lastArgs.length > 0) {
      await execute(...lastArgs);
    }
  }, [execute, lastArgs]);

  return {
    data,
    loading,
    error,
    execute,
    retry,
    retryCount,
  };
}

// Hook específico para operaciones CRUD comunes
export function useApiOperation<T = any>(
  apiFunction: (
    ...args: any[]
  ) => Promise<{ data?: T; error?: string; status: number }>
) {
  return useApiWithRetry(apiFunction, {
    maxRetries: 2,
    baseDelay: 1000,
    retryCondition: (error: any) => {
      // Para operaciones CRUD, solo reintentar errores de red y 5xx
      return !error.status || error.status >= 500;
    },
  });
}

// Wrapper para llamadas que requieren autenticación con token refresh
export function useAuthenticatedApi<T = any>(
  apiFunction: (
    ...args: any[]
  ) => Promise<{ data?: T; error?: string; status: number }>
) {
  return useApiWithRetry(apiFunction, {
    maxRetries: 1, // Solo 1 retry para auth errors
    baseDelay: 500,
    retryCondition: (error: any) => {
      // Reintentar 401 una vez (para token refresh)
      return error.status === 401;
    },
  });
}
