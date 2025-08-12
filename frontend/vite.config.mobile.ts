import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// https://vitejs.dev/config/
export default defineConfig({
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
    // Configuración optimizada para móvil - menos actualizaciones
    watch: {
      usePolling: false, // Desactivar polling para móvil
      interval: 5000, // Intervalo más largo
      ignored: ['**/node_modules/**', '**/dist/**'],
    },
    hmr: {
      clientPort: 5173,
      host: '0.0.0.0',
      // Configuración HMR más estable para móvil
      timeout: 30000,
      overlay: false, // Desactivar overlay de errores que puede interferir
    },
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        timeout: 30000, // Timeout más largo para móvil
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
        },
      },
    },
  },
  define: {
    'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development'),
  },
  // Optimizaciones específicas para móvil
  optimizeDeps: {
    include: ['react', 'react-dom', 'react-router-dom'],
    exclude: ['@vite/client'],
  },
})
