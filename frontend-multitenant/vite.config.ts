import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 🇨🇺 PACKFY CUBA - CONFIGURACIÓN VITE UNIFICADA v3.0
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
    host: "localhost",

    // HTTPS opcional con certificados locales
    // Descomentado para permitir acceso HTTP directo
    // https: {
    //   key: './certs/cert.key',
    //   cert: './certs/cert.crt',
    // },

    // Configuración optimizada para desarrollo móvil
    watch: {
      usePolling: false,
      interval: 3000,
      ignored: ["**/node_modules/**", "**/dist/**"],
    },

    hmr: {
      clientPort: 5173,
      host: "0.0.0.0",
      timeout: 30000,
      overlay: false,
    },

    // Proxy para desarrollo local
    proxy: {
      "/api": {
        target: "http://packfy-backend:8000",
        changeOrigin: true,
        secure: false,
        timeout: 30000,
        configure: (proxy, _options) => {
          proxy.on("error", (err, _req, _res) => {
            console.log("🚨 Proxy error:", err);
          });
          proxy.on("proxyReq", (proxyReq, req, _res) => {
            console.log("📡 Proxy request:", req.method, req.url);
          });
        },
      },
    },
  },

  build: {
    outDir: "dist",
    sourcemap: true,

    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
          router: ["react-router-dom"],
          api: ["axios"],
        },
      },
    },

    // Optimizaciones de build
    minify: "terser",
    target: "es2020",
  },

  define: {
    "process.env.NODE_ENV": JSON.stringify(
      process.env.NODE_ENV || "development"
    ),
    __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
    __VERSION__: JSON.stringify("3.0.0"),
  },

  // Optimizaciones específicas
  optimizeDeps: {
    include: ["react", "react-dom", "react-router-dom"],
    exclude: ["@vite/client"],
  },

  // CSS
  css: {
    devSourcemap: true,
    preprocessorOptions: {
      css: {
        charset: false,
      },
    },
  },
});
