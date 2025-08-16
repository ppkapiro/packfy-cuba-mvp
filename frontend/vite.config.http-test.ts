import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 🚨 CONFIGURACIÓN TEMPORAL HTTP (SIN SSL) PARA TEST MÓVIL
export default defineConfig({
  plugins: [react()],
  base: "/",
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5174, // Puerto diferente para evitar conflictos
    host: "0.0.0.0",
    // ❌ SIN HTTPS - Solo HTTP
    https: false,
    // Headers para móvil
    headers: {
      "Cache-Control": "no-cache, no-store, must-revalidate",
      "Pragma": "no-cache",
      "Expires": "0",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "*",
    },
    cors: true,
    strictPort: false,
    watch: {
      usePolling: false,
      interval: 5000,
      ignored: ["**/node_modules/**", "**/dist/**"],
    },
    hmr: {
      clientPort: 5174,
      host: "0.0.0.0",
      timeout: 30000,
      overlay: false,
    },
    proxy: {
      "/api": {
        target: "http://192.168.12.178:8000", // ❌ SIN HTTPS
        changeOrigin: true,
        secure: false, // Importante para HTTP
        timeout: 30000,
        headers: {
          "User-Agent": "Packfy-Test-HTTP/1.0",
        }
      },
    },
  },
  build: {
    outDir: "dist",
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: undefined,
      },
    },
  },
});
