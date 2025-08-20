// 🛡️ Componente de Ruta Protegida - Modernizado
import { Navigate } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'
import LoadingSpinner from './LoadingSpinner'

interface ProtectedRouteProps {
  children: React.ReactNode
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, isLoading, token } = useAuthStore()

  // Mostrar loading mientras se verifica la autenticación
  if (isLoading) {
    return <LoadingSpinner fullScreen />
  }

  // Redirigir a login si no está autenticado
  if (!isAuthenticated || !token) {
    return <Navigate to="/login" replace />
  }

  // Renderizar contenido protegido
  return <>{children}</>
}
