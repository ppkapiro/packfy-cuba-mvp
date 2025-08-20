// Servicio de cámara optimizada para conexiones lentas en Cuba

export interface PackagePhoto {
  id: string;
  originalFile: File;
  compressedDataUrl: string;
  thumbnail: string;
  metadata: {
    originalSize: number;
    compressedSize: number;
    compressionRatio: number;
    timestamp: string;
    dimensions: { width: number; height: number };
  };
}

export interface CompressionOptions {
  maxWidth: number;
  maxHeight: number;
  quality: number;
  thumbnailSize: number;
}

class CameraService {
  private static readonly DEFAULT_OPTIONS: CompressionOptions = {
    maxWidth: 1024,     // Máximo ancho para mantener calidad pero reducir tamaño
    maxHeight: 768,     // Máximo alto 
    quality: 0.75,      // 75% de calidad - buen balance calidad/tamaño
    thumbnailSize: 150  // Thumbnail pequeño para lista rápida
  };

  // Configuraciones específicas para diferentes contextos
  private static readonly PRESETS = {
    lowBandwidth: {
      maxWidth: 640,
      maxHeight: 480,
      quality: 0.6,
      thumbnailSize: 100
    },
    highQuality: {
      maxWidth: 1600,
      maxHeight: 1200,
      quality: 0.85,
      thumbnailSize: 200
    },
    default: this.DEFAULT_OPTIONS
  };

  static async requestCameraPermission(): Promise<boolean> {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          facingMode: 'environment', // Cámara trasera preferida
          width: { ideal: 1280 },
          height: { ideal: 720 }
        } 
      });
      
      // Detener stream inmediatamente después de verificar permisos
      stream.getTracks().forEach(track => track.stop());
      return true;
    } catch (error) {
      console.error('Error accediendo a la cámara:', error);
      return false;
    }
  }

  static async capturePhoto(
    preset: 'lowBandwidth' | 'highQuality' | 'default' = 'default'
  ): Promise<PackagePhoto | null> {
    try {
      const options = this.PRESETS[preset];
      
      // Crear input file para móvil (funciona mejor que MediaDevices en algunos casos)
      const fileInput = document.createElement('input');
      fileInput.type = 'file';
      fileInput.accept = 'image/*';
      fileInput.capture = 'environment'; // Preferir cámara trasera
      
      return new Promise((resolve) => {
        fileInput.onchange = async (event) => {
          const file = (event.target as HTMLInputElement).files?.[0];
          if (!file) {
            resolve(null);
            return;
          }

          try {
            const photo = await this.processImage(file, options);
            resolve(photo);
          } catch (error) {
            console.error('Error procesando imagen:', error);
            resolve(null);
          }
        };

        fileInput.oncancel = () => resolve(null);
        fileInput.click();
      });
    } catch (error) {
      console.error('Error capturando foto:', error);
      return null;
    }
  }

  private static async processImage(
    file: File, 
    options: CompressionOptions
  ): Promise<PackagePhoto> {
    const id = this.generatePhotoId();
    const originalSize = file.size;
    
    // Crear imagen para procesamiento
    const img = await this.createImageElement(file);
    
    // Calcular nuevas dimensiones manteniendo proporción
    const { width, height } = this.calculateDimensions(
      img.naturalWidth, 
      img.naturalHeight, 
      options.maxWidth, 
      options.maxHeight
    );

    // Comprimir imagen principal
    const compressedDataUrl = await this.compressImage(img, width, height, options.quality);
    
    // Crear thumbnail
    const thumbnailSize = options.thumbnailSize;
    const { width: thumbWidth, height: thumbHeight } = this.calculateDimensions(
      img.naturalWidth, 
      img.naturalHeight, 
      thumbnailSize, 
      thumbnailSize
    );
    const thumbnail = await this.compressImage(img, thumbWidth, thumbHeight, 0.6);

    // Calcular tamaño comprimido (aproximado basado en dataURL)
    const compressedSize = Math.round((compressedDataUrl.length * 3) / 4);
    const compressionRatio = ((originalSize - compressedSize) / originalSize) * 100;

    return {
      id,
      originalFile: file,
      compressedDataUrl,
      thumbnail,
      metadata: {
        originalSize,
        compressedSize,
        compressionRatio,
        timestamp: new Date().toISOString(),
        dimensions: { width, height }
      }
    };
  }

  private static createImageElement(file: File): Promise<HTMLImageElement> {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = URL.createObjectURL(file);
    });
  }

  private static calculateDimensions(
    originalWidth: number, 
    originalHeight: number, 
    maxWidth: number, 
    maxHeight: number
  ): { width: number; height: number } {
    let { width, height } = { width: originalWidth, height: originalHeight };
    
    // Reducir proporcionalmente si excede los límites
    if (width > maxWidth) {
      height = (height * maxWidth) / width;
      width = maxWidth;
    }
    
    if (height > maxHeight) {
      width = (width * maxHeight) / height;
      height = maxHeight;
    }
    
    return { width: Math.round(width), height: Math.round(height) };
  }

  private static compressImage(
    img: HTMLImageElement, 
    width: number, 
    height: number, 
    quality: number
  ): Promise<string> {
    return new Promise((resolve) => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d')!;
      
      canvas.width = width;
      canvas.height = height;
      
      // Configurar compresión óptima
      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = 'high';
      
      // Dibujar imagen redimensionada
      ctx.drawImage(img, 0, 0, width, height);
      
      // Convertir a dataURL con compresión
      const dataUrl = canvas.toDataURL('image/jpeg', quality);
      resolve(dataUrl);
    });
  }

  private static generatePhotoId(): string {
    return `pkg_photo_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  // Función para estimar tiempo de carga según conexión
  static estimateUploadTime(imageSizeBytes: number, connectionType?: string): string {
    // Velocidades típicas en Cuba (kbps)
    const speeds = {
      'slow-2g': 50,
      '2g': 70,
      '3g': 200,
      '4g': 1000,
      'wifi': 500 // WiFi promedio en Cuba
    };

    const speed = speeds[connectionType as keyof typeof speeds] || speeds.wifi;
    const timeSeconds = (imageSizeBytes * 8) / (speed * 1000); // Convertir a segundos
    
    if (timeSeconds < 5) return '< 5 seg';
    if (timeSeconds < 30) return `~${Math.round(timeSeconds)} seg`;
    if (timeSeconds < 60) return `~${Math.round(timeSeconds / 60)} min`;
    return `~${Math.round(timeSeconds / 60)} min`;
  }

  // Detectar calidad de conexión (básico)
  static detectConnectionQuality(): 'lowBandwidth' | 'default' | 'highQuality' {
    // @ts-ignore - API experimental
    const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    
    if (!connection) return 'default';
    
    const effectiveType = connection.effectiveType;
    const downlink = connection.downlink;
    
    if (effectiveType === 'slow-2g' || effectiveType === '2g' || downlink < 0.5) {
      return 'lowBandwidth';
    }
    
    if (effectiveType === '4g' && downlink > 2) {
      return 'highQuality';
    }
    
    return 'default';
  }

  // Función para batch upload optimizado
  static async uploadPhotos(
    photos: PackagePhoto[],
    onProgress?: (progress: number, photoIndex: number) => void
  ): Promise<string[]> {
    const uploadedUrls: string[] = [];
    
    for (let i = 0; i < photos.length; i++) {
      const photo = photos[i];
      
      try {
        // Simular upload - en producción sería una llamada real a la API
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // En una implementación real, aquí se haría el upload al servidor
        const uploadedUrl = `https://api.packfy.cu/photos/${photo.id}`;
        uploadedUrls.push(uploadedUrl);
        
        onProgress?.(((i + 1) / photos.length) * 100, i);
      } catch (error) {
        console.error(`Error subiendo foto ${i + 1}:`, error);
        // Continuar con las demás fotos
      }
    }
    
    return uploadedUrls;
  }
}

export default CameraService;
