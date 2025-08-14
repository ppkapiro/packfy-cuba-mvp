import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { splitVendorChunkPlugin } from "vite";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 🇨🇺 PACKFY CUBA - CONFIGURACIÓN VITE OPTIMIZADA v4.0
export default defineConfig({
  plugins: [
    react({
      // Optimizaciones de React
      babel: {
        plugins: [
          // Plugin para lazy loading de componentes
          [
            "babel-plugin-import",
            {
              libraryName: "lucide-react",
              libraryDirectory: "",
              camel2DashComponentName: false,
            },
          ],
        ],
      },
    }),
    // Separar vendor chunks automáticamente
    splitVendorChunkPlugin(),
  ],

  base: "/",

  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@components": path.resolve(__dirname, "./src/components"),
      "@pages": path.resolve(__dirname, "./src/pages"),
      "@services": path.resolve(__dirname, "./src/services"),
      "@utils": path.resolve(__dirname, "./src/utils"),
      "@styles": path.resolve(__dirname, "./src/styles"),
    },
  },

  // 🚀 OPTIMIZACIONES DE BUILD
  build: {
    // Configuración optimizada para producción
    target: "es2015",
    cssCodeSplit: true,
    sourcemap: false, // Deshabilitar sourcemaps en producción
    minify: "terser",

    terserOptions: {
      compress: {
        drop_console: true, // Eliminar console.logs en producción
        drop_debugger: true,
        pure_funcs: ["console.log", "console.info"],
      },
      format: {
        comments: false, // Eliminar comentarios
      },
    },

    rollupOptions: {
      output: {
        // 📦 Configuración de chunks optimizada
        manualChunks: {
          // Chunk principal de React
          "react-vendor": ["react", "react-dom", "react-router-dom"],

          // Chunk de utilidades
          "utils-vendor": ["axios", "date-fns", "zustand"],

          // Chunk de UI
          "ui-vendor": ["lucide-react", "react-hot-toast", "clsx"],

          // Chunk de formularios
          "forms-vendor": ["react-hook-form"],
        },

        // Nomenclatura optimizada de archivos
        chunkFileNames: (chunkInfo) => {
          const facadeModuleId = chunkInfo.facadeModuleId;
          if (facadeModuleId) {
            const fileName = path.basename(
              facadeModuleId,
              path.extname(facadeModuleId)
            );
            return `chunks/${fileName}-[hash].js`;
          }
          return "chunks/[name]-[hash].js";
        },

        entryFileNames: "entry/[name]-[hash].js",
        assetFileNames: (assetInfo) => {
          // Organizar assets por tipo
          const extType = assetInfo.name?.split(".").pop();

          if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(extType ?? "")) {
            return "images/[name]-[hash][extname]";
          }

          if (/css/i.test(extType ?? "")) {
            return "styles/[name]-[hash][extname]";
          }

          return "assets/[name]-[hash][extname]";
        },
      },

      // 🔧 Optimizaciones de dependencies
      external: [],
    },

    // 📊 Configuración de chunks
    chunkSizeWarningLimit: 1000, // 1MB warning limit

    // 🗜️ Compresión adicional
    reportCompressedSize: true,
  },

  // ⚡ OPTIMIZACIONES DE DESARROLLO
  server: {
    port: 5173,
    host: "0.0.0.0",

    // Configuración optimizada para desarrollo
    watch: {
      usePolling: false,
      interval: 1000,
      ignored: ["**/node_modules/**", "**/dist/**"],
    },

    hmr: {
      overlay: true,
      port: 5174,
    },

    // 🔧 Proxy para APIs
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        secure: false,
        timeout: 30000,
        configure: (proxy, _options) => {
          proxy.on("error", (err, _req, _res) => {
            console.log("🔴 Proxy error:", err);
          });
          proxy.on("proxyReq", (proxyReq, req, _res) => {
            console.log("🔹 Proxy request:", req.method, req.url);
          });
        },
      },
    },
  },

  // 🎯 OPTIMIZACIONES ESPECÍFICAS
  optimizeDeps: {
    // Pre-bundling de dependencias frecuentes
    include: [
      "react",
      "react-dom",
      "react-router-dom",
      "axios",
      "lucide-react",
      "react-hot-toast",
      "zustand",
      "clsx",
      "date-fns",
    ],

    // Excluir dependencias problemáticas
    exclude: ["@vitejs/plugin-react"],

    // Forzar pre-bundling
    force: false,
  },

  // 🔒 Configuración de preview
  preview: {
    port: 5173,
    host: "0.0.0.0",
    strictPort: true,
    https: false,
  },

  // 📱 Configuración de PWA
  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version || "4.0.0"),
    __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
  },

  // 🎨 Configuración de CSS
  css: {
    devSourcemap: true,

    preprocessorOptions: {
      // Configuraciones para pre-procesadores si se usan
    },

    postcss: {
      plugins: [
        // Autoprefixer automático
      ],
    },

    // Módulos CSS
    modules: {
      localsConvention: "camelCase",
    },
  },

  // 🚫 Configuración de ESBuild
  esbuild: {
    // Eliminar console.logs en producción
    drop: process.env.NODE_ENV === "production" ? ["console", "debugger"] : [],

    // Optimizaciones de JSX
    jsxFactory: "React.createElement",
    jsxFragment: "React.Fragment",
  },
});
