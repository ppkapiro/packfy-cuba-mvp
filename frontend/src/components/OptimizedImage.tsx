// 🇨🇺 PACKFY CUBA - Sistema de Optimización de Imágenes v4.0
// Compresión automática y lazy loading de imágenes

import { useState, useEffect, useRef, useCallback } from 'react'

interface OptimizedImageProps {
  src: string
  alt: string
  className?: string
  width?: number
  height?: number
  lazy?: boolean
  quality?: number
  placeholder?: string
  onLoad?: () => void
  onError?: () => void
}

interface ImageCache {
  [key: string]: {
    blob: Blob
    objectUrl: string
    timestamp: number
  }
}

// 🗄️ Caché global de imágenes
const imageCache: ImageCache = {}
const CACHE_DURATION = 30 * 60 * 1000 // 30 minutos

// 🖼️ Componente de imagen optimizada
export function OptimizedImage({
  src,
  alt,
  className = '',
  width,
  height,
  lazy = true,
  quality = 80,
  placeholder = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik04NyA3NEgxMTNWMTAwSDg3Vjc0WiIgZmlsbD0iI0Q1RDVENSIvPgo8cGF0aCBkPSJNMTA0IDEyNkgxNTZWMTQwSDEwNFYxMjZaIiBmaWxsPSIjRDVENUQ1Ii8+CjxwYXRoIGQ9Ik00NCAxMjZIOTZWMTQwSDQ0VjEyNloiIGZpbGw9IiNENUQ1RDUiLz4KPC9zdmc+',
  onLoad,
  onError
}: OptimizedImageProps) {
  const [isLoaded, setIsLoaded] = useState(false)
  const [isInView, setIsInView] = useState(!lazy)
  const [imageSrc, setImageSrc] = useState(placeholder)
  const [error, setError] = useState(false)
  const imgRef = useRef<HTMLImageElement>(null)
  const observerRef = useRef<IntersectionObserver | null>(null)

  // 🔍 Intersection Observer para lazy loading
  useEffect(() => {
    if (!lazy || isInView) return

    const observerCallback = (entries: IntersectionObserverEntry[]) => {
      const [entry] = entries
      if (entry.isIntersecting) {
        setIsInView(true)
        observerRef.current?.disconnect()
      }
    }

    observerRef.current = new IntersectionObserver(observerCallback, {
      threshold: 0.1,
      rootMargin: '50px'
    })

    if (imgRef.current) {
      observerRef.current.observe(imgRef.current)
    }

    return () => {
      observerRef.current?.disconnect()
    }
  }, [lazy, isInView])

  // 🖼️ Cargar imagen optimizada
  const loadOptimizedImage = useCallback(async (imageUrl: string) => {
    try {
      // Verificar caché
      const cacheKey = `${imageUrl}_${quality}_${width}_${height}`
      const cachedImage = imageCache[cacheKey]

      if (cachedImage && Date.now() - cachedImage.timestamp < CACHE_DURATION) {
        setImageSrc(cachedImage.objectUrl)
        setIsLoaded(true)
        onLoad?.()
        return
      }

      // Cargar imagen
      const response = await fetch(imageUrl)
      if (!response.ok) throw new Error('Failed to load image')

      const blob = await response.blob()

      // Comprimir si es necesario
      const optimizedBlob = await compressImage(blob, quality, width, height)

      // Crear object URL
      const objectUrl = URL.createObjectURL(optimizedBlob)

      // Guardar en caché
      imageCache[cacheKey] = {
        blob: optimizedBlob,
        objectUrl,
        timestamp: Date.now()
      }

      setImageSrc(objectUrl)
      setIsLoaded(true)
      onLoad?.()

    } catch (err) {
      console.error('Error loading image:', err)
      setError(true)
      onError?.()
    }
  }, [src, quality, width, height, onLoad, onError])

  // 🚀 Cargar imagen cuando esté en vista
  useEffect(() => {
    if (isInView && src && src !== placeholder) {
      loadOptimizedImage(src)
    }
  }, [isInView, src, loadOptimizedImage, placeholder])

  // 🧹 Limpiar object URLs
  useEffect(() => {
    return () => {
      if (imageSrc.startsWith('blob:')) {
        URL.revokeObjectURL(imageSrc)
      }
    }
  }, [imageSrc])

  return (
    <div className={`optimized-image-container ${className}`}>
      <img
        ref={imgRef}
        src={imageSrc}
        alt={alt}
        width={width}
        height={height}
        className={`
          optimized-image
          ${isLoaded ? 'loaded' : 'loading'}
          ${error ? 'error' : ''}
        `}
        loading={lazy ? 'lazy' : 'eager'}
        onLoad={() => {
          if (imageSrc !== placeholder) {
            setIsLoaded(true)
            onLoad?.()
          }
        }}
        onError={() => {
          setError(true)
          onError?.()
        }}
        style={{
          transition: 'opacity 0.3s ease-in-out',
          opacity: isLoaded ? 1 : 0.7,
          filter: isLoaded ? 'none' : 'blur(1px)',
        }}
      />

      {/* 🔄 Indicador de carga */}
      {!isLoaded && !error && (
        <div className="image-loading-indicator">
          <div className="loading-spinner"></div>
        </div>
      )}

      {/* ❌ Indicador de error */}
      {error && (
        <div className="image-error-indicator">
          <span>❌ Error cargando imagen</span>
        </div>
      )}
    </div>
  )
}

// 🗜️ Función de compresión de imágenes
async function compressImage(
  blob: Blob,
  quality: number = 80,
  maxWidth?: number,
  maxHeight?: number
): Promise<Blob> {
  return new Promise((resolve) => {
    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')!
    const img = new Image()

    img.onload = () => {
      // Calcular dimensiones optimales
      let { width, height } = img

      if (maxWidth && width > maxWidth) {
        height = (height * maxWidth) / width
        width = maxWidth
      }

      if (maxHeight && height > maxHeight) {
        width = (width * maxHeight) / height
        height = maxHeight
      }

      // Configurar canvas
      canvas.width = width
      canvas.height = height

      // Dibujar imagen redimensionada
      ctx.drawImage(img, 0, 0, width, height)

      // Convertir a blob comprimido
      canvas.toBlob(
        (compressedBlob) => {
          resolve(compressedBlob || blob)
        },
        'image/jpeg',
        quality / 100
      )
    }

    img.src = URL.createObjectURL(blob)
  })
}

// 🧹 Función para limpiar caché
export function clearImageCache(): void {
  Object.values(imageCache).forEach(cached => {
    URL.revokeObjectURL(cached.objectUrl)
  })

  Object.keys(imageCache).forEach(key => {
    delete imageCache[key]
  })

  console.log('🧹 Caché de imágenes limpiado')
}

// 📊 Función para obtener estadísticas de caché
export function getImageCacheStats() {
  const entries = Object.values(imageCache)
  const totalSize = entries.reduce((sum, entry) => sum + entry.blob.size, 0)

  return {
    totalImages: entries.length,
    totalSize,
    totalSizeMB: (totalSize / (1024 * 1024)).toFixed(2),
    oldestEntry: Math.min(...entries.map(e => e.timestamp)),
    newestEntry: Math.max(...entries.map(e => e.timestamp))
  }
}

// 🎨 Hook para precargar imágenes
export function useImagePreloader(urls: string[]) {
  const [loadedImages, setLoadedImages] = useState<Set<string>>(new Set())
  const [isLoading, setIsLoading] = useState(false)

  const preloadImages = useCallback(async () => {
    setIsLoading(true)
    const promises = urls.map(async (url) => {
      try {
        const response = await fetch(url)
        const blob = await response.blob()
        const optimizedBlob = await compressImage(blob, 60) // Menor calidad para preload

        const objectUrl = URL.createObjectURL(optimizedBlob)
        const cacheKey = `${url}_preload`

        imageCache[cacheKey] = {
          blob: optimizedBlob,
          objectUrl,
          timestamp: Date.now()
        }

        setLoadedImages(prev => new Set([...prev, url]))
        return url
      } catch (error) {
        console.error(`Error preloading image ${url}:`, error)
        return null
      }
    })

    await Promise.allSettled(promises)
    setIsLoading(false)
  }, [urls])

  useEffect(() => {
    if (urls.length > 0) {
      preloadImages()
    }
  }, [urls, preloadImages])

  return { loadedImages, isLoading }
}

export default OptimizedImage
