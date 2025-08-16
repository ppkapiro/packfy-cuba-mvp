import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";
import path from "path";
import { fileURLToPath } from "url";
import fs from "fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 🇨🇺 PACKFY CUBA - CONFIGURACIÓN VITE v4.0 con PWA
export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: "autoUpdate",
      workbox: {
        globPatterns: ["**/*.{js,css,html,ico,png,svg,woff2}"],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/api\./i,
            handler: "NetworkFirst",
            options: {
              cacheName: "api-cache",
              networkTimeoutSeconds: 10,
              cacheableResponse: {
                statuses: [0, 200],
              },
            },
          },
          {
            urlPattern: /\.(?:png|jpg|jpeg|svg|gif|webp)$/,
            handler: "CacheFirst",
            options: {
              cacheName: "images-cache",
              expiration: {
                maxEntries: 100,
                maxAgeSeconds: 60 * 60 * 24 * 30, // 30 días
              },
            },
          },
        ],
      },
      manifest: {
        name: "PACKFY CUBA",
        short_name: "PACKFY",
        description: "Sistema de Paquetería Moderna para Cuba",
        theme_color: "#667eea",
        background_color: "#1a1a2e",
        display: "standalone",
        orientation: "portrait",
        scope: "/",
        start_url: "/",
        icons: [
          {
            src: "/icons/icon-192.svg",
            sizes: "192x192",
            type: "image/svg+xml",
          },
          {
            src: "/icons/icon-512.svg",
            sizes: "512x512",
            type: "image/svg+xml",
          },
          {
            src: "/icons/icon-192.png",
            sizes: "192x192",
            type: "image/png",
          },
          {
            src: "/icons/icon-512.png",
            sizes: "512x512",
            type: "image/png",
          },
        ],
      },
      devOptions: {
        enabled: true,
      },
    }),
  ],
  base: "/",

  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },

  server: {
    port: 5173,
    host: "0.0.0.0",

    // 🔒 CONFIGURACIÓN HTTPS PARA DESARROLLO SEGURO
    https: {
      key: fs.readFileSync(path.resolve(__dirname, "./certs/cert.key")),
      cert: fs.readFileSync(path.resolve(__dirname, "./certs/cert.crt")),
    },

    // Configuración optimizada para desarrollo
    watch: {
      usePolling: false,
      interval: 1000,
      ignored: ["**/node_modules/**", "**/dist/**"],
    },

    hmr: {
      clientPort: 5173,
      host: "0.0.0.0",
      timeout: 10000,
      overlay: true,
      port: 5173,
    },

    // Proxy al backend dentro de Docker (HTTP)
    proxy: {
      "/api": {
        // El backend de desarrollo corre en HTTP dentro del contenedor
        target: "http://backend:8000",
        changeOrigin: true,
        secure: false, // No verificar TLS (no aplica en HTTP)
        timeout: 15000,
        rewrite: (path) => path,
      },
    },
  },

  // Optimizaciones de build
  build: {
    outDir: "dist",
    target: "esnext",
    minify: "esbuild",
    sourcemap: true,
    cssCodeSplit: true,

    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
          router: ["react-router-dom"],
          ui: ["lucide-react"],
        },
      },
    },

    // Configuración para chunks optimizados
    chunkSizeWarningLimit: 1000,
  },

  // Optimizaciones CSS
  css: {
    devSourcemap: true,
    modules: {
      localsConvention: "camelCase",
    },
  },

  // Configuración optimizada
  optimizeDeps: {
    include: ["react", "react-dom", "react-router-dom", "axios"],
    exclude: ["@vitejs/plugin-react"],
  },

  define: {
    "process.env.NODE_ENV": JSON.stringify(
      process.env.NODE_ENV || "development"
    ),
    __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
    __VERSION__: JSON.stringify("4.0.0"),
  },
});
