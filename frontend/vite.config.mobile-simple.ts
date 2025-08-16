import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Configuración especial para móvil con SSL relajado
export default defineConfig({
  plugins: [react()],
  base: "/",
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5173,
    host: "0.0.0.0",
    https: {
      cert: "/app/certs/localhost.crt",
      key: "/app/certs/localhost.key",
    },
    // Headers especiales para móvil
    headers: {
      "Cache-Control": "no-cache, no-store, must-revalidate",
      "Pragma": "no-cache",
      "Expires": "0",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "*",
    },
    // Configuración relajada para móvil
    strictPort: false,
    cors: true,
    watch: {
      usePolling: false,
      interval: 5000,
      ignored: ["**/node_modules/**", "**/dist/**"],
    },
    hmr: {
      clientPort: 5173,
      host: "0.0.0.0",
      timeout: 30000,
      overlay: false,
    },
    proxy: {
      "/api": {
        target: "https://192.168.12.178:8443",
        changeOrigin: true,
        secure: false,
        timeout: 30000,
        // Headers adicionales para móvil
        headers: {
          "User-Agent": "Packfy-Mobile-App/1.0",
        }
      },
    },
  },
  build: {
    outDir: "dist",
    sourcemap: false, // Desactivar sourcemaps para móvil
    rollupOptions: {
      output: {
        manualChunks: undefined, // Simplificar chunks para móvil
      },
    },
  },
});
