// 🛡️ Componente de Ruta Protegida - Modernizado (AuthContext)
import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import LoadingSpinner from './LoadingSpinner'

interface ProtectedRouteProps {
  children: React.ReactNode
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, isLoading, token } = useAuth()

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
