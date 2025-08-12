import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const isDev = mode === 'development'
  // Deshabilitado HMR para evitar reinicios constantes
  const enableHMR = false // Cambiado a false para estabilidad
  
  console.log('🔧 Vite config:', { mode, isDev, enableHMR })
  
  return {
    plugins: [react()],
    base: '/',
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    server: {
      port: 5173,
      host: '0.0.0.0',
      headers: {
        'Cache-Control': 'public, max-age=31536000',
        'Service-Worker-Allowed': '/',
      },
      watch: {
        usePolling: false, // Deshabilitado polling
        // interval: 2000, // Sin intervalo
      },
      hmr: enableHMR ? {
        clientPort: 5173,
        host: 'localhost', // Solo para localhost
        overlay: false, // Sin overlay que pueda causar problemas
      } : false, // HMR deshabilitado para evitar actualizaciones constantes
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
          configure: (proxy, options) => {
            // Log para debugging de proxy
            proxy.on('proxyReq', (proxyReq, req, res) => {
              console.log('📡 Proxy request:', req.method, req.url, '→', proxyReq.path);
            });
            proxy.on('proxyRes', (proxyRes, req, res) => {
              console.log('📡 Proxy response:', proxyRes.statusCode, req.url);
            });
            proxy.on('error', (err, req, res) => {
              console.error('❌ Proxy error:', err.message, req.url);
            });
          }
        }
      }
    },
    build: {
      outDir: 'dist',
      sourcemap: isDev,
      minify: !isDev,
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: ['react', 'react-dom'],
            router: ['react-router-dom'],
          },
        },
      },
    },
    // 🔧 PWA Runtime defines
    define: {
      __APP_VERSION__: JSON.stringify(process.env.npm_package_version || '2.0.0'),
      __PWA_ENABLED__: JSON.stringify(true)
    },
    // 🚀 Performance optimizations
    optimizeDeps: {
      include: ['react', 'react-dom', 'axios']
    }
  }
})
