import React, { useState, useEffect } from 'react';
import { Camera, Upload, Trash2, Eye, Wifi, WifiOff } from 'lucide-react';
import CameraService, { PackagePhoto } from '../services/camera';

interface PackageCameraProps {
  onPhotosChange?: (photos: PackagePhoto[]) => void;
  maxPhotos?: number;
}

const PackageCamera: React.FC<PackageCameraProps> = ({ 
  onPhotosChange, 
  maxPhotos = 5 
}) => {
  const [photos, setPhotos] = useState<PackagePhoto[]>([]);
  const [isCapturing, setIsCapturing] = useState(false);
  const [connectionQuality, setConnectionQuality] = useState<'lowBandwidth' | 'default' | 'highQuality'>('default');
  const [uploadProgress, setUploadProgress] = useState<{ progress: number; photoIndex: number } | null>(null);
  const [viewingPhoto, setViewingPhoto] = useState<PackagePhoto | null>(null);

  useEffect(() => {
    // Detectar calidad de conexión al montar
    const quality = CameraService.detectConnectionQuality();
    setConnectionQuality(quality);
  }, []);

  useEffect(() => {
    onPhotosChange?.(photos);
  }, [photos, onPhotosChange]);

  const handleCapturePhoto = async () => {
    if (photos.length >= maxPhotos) {
      alert(`Máximo ${maxPhotos} fotos permitidas`);
      return;
    }

    setIsCapturing(true);
    
    try {
      const photo = await CameraService.capturePhoto(connectionQuality);
      
      if (photo) {
        setPhotos(prev => [...prev, photo]);
      }
    } catch (error) {
      console.error('Error capturando foto:', error);
      alert('Error al capturar la foto. Inténtalo de nuevo.');
    } finally {
      setIsCapturing(false);
    }
  };

  const handleDeletePhoto = (photoId: string) => {
    setPhotos(prev => prev.filter(photo => photo.id !== photoId));
  };

  const handleUploadPhotos = async () => {
    if (photos.length === 0) return;

    try {
      setUploadProgress({ progress: 0, photoIndex: 0 });
      
      const uploadedUrls = await CameraService.uploadPhotos(
        photos,
        (progress, photoIndex) => {
          setUploadProgress({ progress, photoIndex });
        }
      );
      
      console.log('Fotos subidas:', uploadedUrls);
      alert('¡Fotos subidas exitosamente!');
      
    } catch (error) {
      console.error('Error subiendo fotos:', error);
      alert('Error subiendo las fotos. Revisa tu conexión.');
    } finally {
      setUploadProgress(null);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const getConnectionIcon = () => {
    switch (connectionQuality) {
      case 'lowBandwidth':
        return <WifiOff className="w-4 h-4 text-red-500" />;
      case 'highQuality':
        return <Wifi className="w-4 h-4 text-green-500" />;
      default:
        return <Wifi className="w-4 h-4 text-yellow-500" />;
    }
  };

  const getQualityText = () => {
    switch (connectionQuality) {
      case 'lowBandwidth':
        return 'Conexión lenta - Compresión alta';
      case 'highQuality':
        return 'Conexión buena - Calidad alta';
      default:
        return 'Conexión normal - Calidad estándar';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
          <Camera className="w-5 h-5" />
          Fotos del Paquete
        </h3>
        <div className="flex items-center gap-2 text-sm">
          {getConnectionIcon()}
          <span className="text-gray-600">{getQualityText()}</span>
        </div>
      </div>

      {/* Información de optimización */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
        <div className="text-sm text-blue-800">
          <div className="font-medium mb-1">💡 Optimizado para Cuba:</div>
          <ul className="text-xs space-y-1 text-blue-700">
            <li>• Compresión automática según tu conexión</li>
            <li>• Imágenes optimizadas para envío rápido</li>
            <li>• Thumbnails para vista previa instantánea</li>
          </ul>
        </div>
      </div>

      {/* Botón de captura */}
      <div className="mb-6">
        <button
          onClick={handleCapturePhoto}
          disabled={isCapturing || photos.length >= maxPhotos}
          className="w-full flex items-center justify-center gap-2 bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          <Camera className="w-5 h-5" />
          {isCapturing ? 'Capturando...' : `Tomar Foto (${photos.length}/${maxPhotos})`}
        </button>
      </div>

      {/* Lista de fotos */}
      {photos.length > 0 && (
        <div className="space-y-3 mb-6">
          <h4 className="font-medium text-gray-700">Fotos Capturadas:</h4>
          
          {photos.map((photo, index) => (
            <div key={photo.id} className="border border-gray-200 rounded-lg p-3">
              <div className="flex items-start gap-3">
                {/* Thumbnail */}
                <img
                  src={photo.thumbnail}
                  alt={`Foto ${index + 1}`}
                  className="w-16 h-16 object-cover rounded-lg cursor-pointer hover:opacity-80"
                  onClick={() => setViewingPhoto(photo)}
                />
                
                {/* Info */}
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-gray-800">
                    Foto #{index + 1}
                  </div>
                  <div className="text-xs text-gray-500 space-y-1">
                    <div>
                      {photo.metadata.dimensions.width}x{photo.metadata.dimensions.height}
                    </div>
                    <div>
                      Original: {formatFileSize(photo.metadata.originalSize)}
                    </div>
                    <div className="text-green-600">
                      Comprimida: {formatFileSize(photo.metadata.compressedSize)} 
                      (-{photo.metadata.compressionRatio.toFixed(1)}%)
                    </div>
                    <div>
                      Tiempo estimado: {CameraService.estimateUploadTime(
                        photo.metadata.compressedSize, 
                        connectionQuality === 'lowBandwidth' ? '2g' : 'wifi'
                      )}
                    </div>
                  </div>
                </div>
                
                {/* Acciones */}
                <div className="flex gap-2">
                  <button
                    onClick={() => setViewingPhoto(photo)}
                    className="p-2 text-blue-600 hover:bg-blue-100 rounded-lg"
                    title="Ver foto completa"
                  >
                    <Eye className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleDeletePhoto(photo.id)}
                    className="p-2 text-red-600 hover:bg-red-100 rounded-lg"
                    title="Eliminar foto"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Botón de upload */}
      {photos.length > 0 && (
        <button
          onClick={handleUploadPhotos}
          disabled={uploadProgress !== null}
          className="w-full flex items-center justify-center gap-2 bg-green-600 text-white py-3 px-4 rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          <Upload className="w-5 h-5" />
          {uploadProgress 
            ? `Subiendo... ${uploadProgress.progress.toFixed(0)}%` 
            : `Subir ${photos.length} Foto${photos.length > 1 ? 's' : ''}`
          }
        </button>
      )}

      {/* Progress bar */}
      {uploadProgress && (
        <div className="mt-3">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-green-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${uploadProgress.progress}%` }}
            />
          </div>
          <div className="text-xs text-gray-600 mt-1 text-center">
            Subiendo foto {uploadProgress.photoIndex + 1} de {photos.length}
          </div>
        </div>
      )}

      {/* Modal de vista de foto */}
      {viewingPhoto && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-lg w-full max-h-[90vh] overflow-hidden">
            <div className="p-4 border-b">
              <div className="flex items-center justify-between">
                <h4 className="font-medium">Vista Previa</h4>
                <button
                  onClick={() => setViewingPhoto(null)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ✕
                </button>
              </div>
            </div>
            
            <div className="p-4">
              <img
                src={viewingPhoto.compressedDataUrl}
                alt="Vista completa"
                className="w-full h-auto rounded-lg"
              />
              
              <div className="mt-3 text-sm text-gray-600">
                <div>Dimensiones: {viewingPhoto.metadata.dimensions.width}x{viewingPhoto.metadata.dimensions.height}</div>
                <div>Tamaño optimizado: {formatFileSize(viewingPhoto.metadata.compressedSize)}</div>
                <div>Compresión: {viewingPhoto.metadata.compressionRatio.toFixed(1)}%</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PackageCamera;
