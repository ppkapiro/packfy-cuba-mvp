import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 🇨🇺 Configuración Vite para Docker - Interfaz Moderna v3.0
export default defineConfig({
  plugins: [react()],
  base: "/",
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@components": path.resolve(__dirname, "./src/components"),
      "@pages": path.resolve(__dirname, "./src/pages"),
      "@services": path.resolve(__dirname, "./src/services"),
      "@styles": path.resolve(__dirname, "./src/styles"),
      "@types": path.resolve(__dirname, "./src/types"),
      "@utils": path.resolve(__dirname, "./src/utils"),
    },
  },
  server: {
    port: 5173,
    host: "0.0.0.0",
    strictPort: true,
    https: {
      key: "./certs/cert.key",
      cert: "./certs/cert.crt",
    },
    // Configuración optimizada para la nueva interfaz
    watch: {
      usePolling: true,
      interval: 1000,
      ignored: ["**/node_modules/**", "**/dist/**"],
    },
    hmr: {
      clientPort: 5173,
      host: "0.0.0.0",
      timeout: 30000,
      overlay: true,
      port: 5173,
    },
    proxy: {
      "/api": {
        target: "http://backend:8000",
        changeOrigin: true,
        secure: false,
        timeout: 30000,
        configure: (proxy, options) => {
          proxy.on("error", (err, req, res) => {
            console.log("proxy error", err);
          });
          proxy.on("proxyReq", (proxyReq, req, res) => {
            console.log("Sending Request to the Target:", req.method, req.url);
          });
          proxy.on("proxyRes", (proxyRes, req, res) => {
            console.log(
              "Received Response from the Target:",
              proxyRes.statusCode,
              req.url
            );
          });
        },
      },
    },
  },
  build: {
    outDir: "dist",
    sourcemap: true,
    minify: "esbuild",
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
          router: ["react-router-dom"],
          ui: ["lucide-react"],
          utils: ["date-fns", "axios"],
        },
      },
    },
  },
  define: {
    "process.env.NODE_ENV": JSON.stringify(
      process.env.NODE_ENV || "development"
    ),
  },
});
