import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const isDev = mode === 'development'
  // Deshabilitar HMR por defecto para evitar problemas móviles
  const enableHMR = false // Cambiar a true solo para desarrollo local
  
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
      watch: {
        usePolling: true,
        interval: 2000, // Reducir frecuencia para evitar actualizaciones constantes
      },
      hmr: enableHMR ? {
        clientPort: 5173,
        host: 'localhost', // Solo para localhost
        overlay: false, // Sin overlay que pueda causar problemas
      } : false, // HMR deshabilitado para evitar actualizaciones constantes
      proxy: {
        '/api': {
          target: process.env.BACKEND_URL || 'http://backend:8000',
          changeOrigin: true,
          secure: false,
          // No reescribir la ruta - mantener /api/ porque el backend lo necesita
          // rewrite: (path) => path.replace(/^\/api/, ''),
          configure: (proxy, options) => {
            // Log para debugging de proxy
            proxy.on('proxyReq', (proxyReq, req, res) => {
              console.log('📡 Proxy request:', req.method, req.url, '→', proxyReq.path);
            });
            proxy.on('error', (err, req, res) => {
              console.error('❌ Proxy error:', err.message);
            });
          },
        },
      },
    },
  }
})