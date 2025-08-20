// ⏳ Componente Loading Spinner - Moderno y elegante
import { Loader } from 'lucide-react'
import './LoadingSpinner.css'

interface LoadingSpinnerProps {
  fullScreen?: boolean
  size?: 'sm' | 'md' | 'lg'
  message?: string
}

export default function LoadingSpinner({ 
  fullScreen = false, 
  size = 'md', 
  message = 'Cargando...' 
}: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8', 
    lg: 'w-12 h-12'
  }

  const content = (
    <div className="loading-content">
      <Loader 
        className={`animate-spin text-blue-600 ${sizeClasses[size]}`}
      />
      {message && (
        <p className="loading-message">{message}</p>
      )}
    </div>
  )

  if (fullScreen) {
    return (
      <div className="loading-fullscreen">
        {content}
      </div>
    )
  }

  return (
    <div className="loading-inline">
      {content}
    </div>
  )
}
