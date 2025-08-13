import React, { useState, useCallback } from 'react';
import { Package, Camera, QrCode, Star, CheckCircle, MapPin, User, Calculator, Printer, Save } from 'lucide-react';
import { api } from '../services/api';
import CameraService, { PackagePhoto as CameraPhoto } from '../services/camera';
import PackageCamera from './PackageCamera';
// 🇨🇺 Estilos cargados globalmente desde main.tsx

// 🎯 FORMULARIO PREMIUM COMPLETO - Todas las funcionalidades
// Formulario avanzado con características premium completas

// Interfaces premium completas
interface PremiumPackageData {
  // Datos del remitente
  senderName: string;
  senderPhone: string;
  senderAddress: string;
  senderEmail: string;

  // Datos del destinatario
  recipientName: string;
  recipientPhone: string;
  recipientAddress: string;
  recipientEmail: string;

  // Información del paquete
  weight: string;
  dimensions: {
    length: string;
    width: string;
    height: string;
  };
  description: string;
  category: string;
  packageSize: string;

  // Opciones premium
  isInternational: boolean;
  isUrgent: boolean;
  isFragile: boolean;
  hasInsurance: boolean;
  declaredValue: string;
  currency: 'USD' | 'CUP';

  // Servicios adicionales
  requiresSignature: boolean;
  needsCustoms: boolean;
  specialInstructions: string;
}

interface PremiumPriceBreakdown {
  basePrice: number;
  insurance: number;
  handling: number;
  urgent: number;
  international: number;
  signature: number;
  customs: number;
  total: number;
  totalCUP: number;
  weightRange: string;
}

interface PackagePhoto {
  id: string;
  file: File;
  preview: string;
  type: 'package' | 'contents' | 'dimensions' | 'receipt';
  description: string;
}

interface PackageLabel {
  trackingNumber: string;
  qrCode: string;
  recipient: any;
  sender: any;
  packageInfo: any;
  generatedAt: Date;
}

// 🏆 Servicio de precios premium avanzado
const PremiumPriceService = {
  rate: 320, // USD a CUP

  calculate(weightLbs: number, options: {
    hasInsurance?: boolean;
    isUrgent?: boolean;
    isInternational?: boolean;
    requiresSignature?: boolean;
    needsCustoms?: boolean;
    declaredValue?: number;
  } = {}): PremiumPriceBreakdown {

    // Cálculo base mejorado en libras
    let basePrice = 8.50;
    if (weightLbs <= 2.2) basePrice = 8.50;        // Hasta 2.2 lbs (1kg)
    else if (weightLbs <= 4.4) basePrice = 15.00;  // 2.2-4.4 lbs (1-2kg)
    else if (weightLbs <= 11) basePrice = 28.00;   // 4.4-11 lbs (2-5kg)
    else if (weightLbs <= 22) basePrice = 45.00;   // 11-22 lbs (5-10kg)
    else if (weightLbs <= 44) basePrice = 85.00;   // 22-44 lbs (10-20kg)
    else basePrice = 85.00 + ((weightLbs - 44) * 2.05); // Más de 44 lbs

    // Servicios premium
    const insurance = options.hasInsurance ? Math.max(basePrice * 0.05, options.declaredValue! * 0.02) : 0;
    const handling = basePrice * 0.15;
    const urgent = options.isUrgent ? basePrice * 0.25 : 0;
    const international = options.isInternational ? basePrice * 0.30 : 0;
    const signature = options.requiresSignature ? 5.00 : 0;
    const customs = options.needsCustoms ? 8.00 : 0;

    const total = basePrice + insurance + handling + urgent + international + signature + customs;
    const totalCUP = total * this.rate;

    return {
      basePrice,
      insurance,
      handling,
      urgent,
      international,
      signature,
      customs,
      total,
      totalCUP,
      weightRange: this.getWeightRange(weightLbs)
    };
  },

  getWeightRange(weightLbs: number): string {
    if (weightLbs <= 2.2) return "Hasta 2.2 lbs (Pequeño)";
    if (weightLbs <= 4.4) return "2.2-4.4 lbs (Mediano)";
    if (weightLbs <= 11) return "4.4-11 lbs (Grande)";
    if (weightLbs <= 22) return "11-22 lbs (Extra Grande)";
    if (weightLbs <= 44) return "22-44 lbs (Jumbo)";
    return `Más de 44 lbs (Comercial)`;
  }
};

// 📷 Servicio de cámara premium con múltiples fotos usando CameraService real
const PremiumCameraService = {
  async capturePhoto(type: PackagePhoto['type'] = 'package'): Promise<File | null> {
    try {
      console.log(`📷 Iniciando captura de foto tipo: ${type}`);

      // Usar el servicio real de cámara con preset optimizado
      const cameraPhoto: CameraPhoto | null = await CameraService.capturePhoto('default');

      if (!cameraPhoto) {
        console.log('📷 Captura cancelada por el usuario');
        return null;
      }

      console.log(`📷 Foto ${type} capturada exitosamente:`, {
        originalSize: `${(cameraPhoto.metadata.originalSize/1024/1024).toFixed(2)}MB`,
        compressedSize: `${(cameraPhoto.metadata.compressedSize/1024/1024).toFixed(2)}MB`,
        compressionRatio: `${cameraPhoto.metadata.compressionRatio.toFixed(1)}%`,
        dimensions: cameraPhoto.metadata.dimensions
      });

      return cameraPhoto.originalFile;
    } catch (error) {
      console.error(`❌ Error capturando foto ${type}:`, error);
      return null;
    }
  },

  async createPhotoPreview(file: File): Promise<string> {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result as string);
      reader.readAsDataURL(file);
    });
  },

  // Método adicional para obtener información completa de la foto
  async capturePhotoWithMetadata(type: PackagePhoto['type'] = 'package'): Promise<CameraPhoto | null> {
    try {
      console.log(`📷 Capturando foto completa tipo: ${type}`);
      return await CameraService.capturePhoto('highQuality');
    } catch (error) {
      console.error(`❌ Error capturando foto completa ${type}:`, error);
      return null;
    }
  }
};

// 🏷️ Servicio QR y etiquetas premium
const PremiumQRService = {
  generateTrackingNumber(): string {
    const prefix = 'PKF';
    const timestamp = Date.now().toString().slice(-6);
    const random = Math.random().toString(36).substr(2, 3).toUpperCase();
    return `${prefix}${timestamp}${random}`;
  },

  createPackageLabel(packageData: PremiumPackageData, priceInfo: PremiumPriceBreakdown): PackageLabel {
    const trackingNumber = this.generateTrackingNumber();

    return {
      trackingNumber,
      qrCode: `https://packfy.cu/track/${trackingNumber}`,
      recipient: {
        name: packageData.recipientName,
        address: packageData.recipientAddress,
        phone: packageData.recipientPhone
      },
      sender: {
        name: packageData.senderName,
        address: packageData.senderAddress,
        phone: packageData.senderPhone
      },
      packageInfo: {
        weight: packageData.weight,
        dimensions: packageData.dimensions,
        description: packageData.description,
        value: packageData.declaredValue,
        price: priceInfo.total
      },
      generatedAt: new Date()
    };
  },

  generatePrintableLabel(label: PackageLabel): string {
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <title>Etiqueta Packfy Cuba - ${label.trackingNumber}</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 20px; }
          .label { border: 2px solid #000; padding: 20px; width: 400px; }
          .header { text-align: center; font-weight: bold; font-size: 18px; }
          .tracking { font-size: 24px; font-weight: bold; text-align: center; margin: 10px 0; }
          .section { margin: 10px 0; }
          .qr-placeholder { width: 100px; height: 100px; border: 1px solid #000; margin: 10px auto; }
        </style>
      </head>
      <body>
        <div class="label">
          <div class="header">📦 PACKFY CUBA 🇨🇺</div>
          <div class="tracking">${label.trackingNumber}</div>
          <div class="section">
            <strong>DE:</strong><br>
            ${label.sender.name}<br>
            ${label.sender.address}
          </div>
          <div class="section">
            <strong>PARA:</strong><br>
            ${label.recipient.name}<br>
            ${label.recipient.address}
          </div>
          <div class="section">
            <strong>PESO:</strong> ${label.packageInfo.weight} lbs<br>
            <strong>VALOR:</strong> $${label.packageInfo.price} USD
          </div>
          <div class="qr-placeholder">QR CODE</div>
        </div>
      </body>
      </html>
    `;
  }
};

const PremiumCompleteForm: React.FC = () => {
  const [step, setStep] = useState<'info' | 'price' | 'photos' | 'label'>('info');

  const [formData, setFormData] = useState<PremiumPackageData>({
    senderName: '',
    senderPhone: '',
    senderAddress: '',
    senderEmail: '',
    recipientName: '',
    recipientPhone: '',
    recipientAddress: '',
    recipientEmail: '',
    weight: '',
    dimensions: { length: '', width: '', height: '' },
    description: '',
    category: '',
    packageSize: '',
    isInternational: false,
    isUrgent: false,
    isFragile: false,
    hasInsurance: false,
    declaredValue: '',
    currency: 'USD',
    requiresSignature: false,
    needsCustoms: false,
    specialInstructions: ''
  });

  const [price, setPrice] = useState<PremiumPriceBreakdown | null>(null);
  const [photos, setPhotos] = useState<PackagePhoto[]>([]);
  const [cameraPhotos, setCameraPhotos] = useState<CameraPhoto[]>([]);
  const [packageLabel, setPackageLabel] = useState<PackageLabel | null>(null);
  const [errors, setErrors] = useState<{[key: string]: string}>({});
  const [isSaving, setIsSaving] = useState(false);

  // Validación premium completa
  const validateForm = useCallback((): boolean => {
    const newErrors: {[key: string]: string} = {};

    // Validar remitente
    if (!formData.senderName.trim()) newErrors.senderName = 'Nombre del remitente es requerido';
    if (!formData.senderAddress.trim()) newErrors.senderAddress = 'Dirección del remitente es requerida';

    // Validar destinatario
    if (!formData.recipientName.trim()) newErrors.recipientName = 'Nombre del destinatario es requerido';
    if (!formData.recipientAddress.trim()) newErrors.recipientAddress = 'Dirección del destinatario es requerida';

    // Validar paquete
    if (!formData.weight.trim()) {
      newErrors.weight = 'Peso es requerido';
    } else {
      const weight = parseFloat(formData.weight);
      if (isNaN(weight) || weight <= 0) {
        newErrors.weight = 'Peso debe ser un número válido';
      } else if (weight > 100) {
        newErrors.weight = 'Peso máximo permitido: 100 lbs';
      }
    }

    if (!formData.description.trim()) newErrors.description = 'Descripción es requerida';

    // Validar valor declarado si tiene seguro
    if (formData.hasInsurance && !formData.declaredValue.trim()) {
      newErrors.declaredValue = 'Valor declarado es requerido para el seguro';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, [formData]);

  // Manejar envío del formulario de información
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    const weight = parseFloat(formData.weight);
    const declaredValue = parseFloat(formData.declaredValue) || 0;

    const calculatedPrice = PremiumPriceService.calculate(weight, {
      hasInsurance: formData.hasInsurance,
      isUrgent: formData.isUrgent,
      isInternational: formData.isInternational,
      requiresSignature: formData.requiresSignature,
      needsCustoms: formData.needsCustoms,
      declaredValue
    });

    setPrice(calculatedPrice);
    setStep('price');
  };

  // Manejar cambio de fotos desde PackageCamera (Nueva funcionalidad real de cámara)
  const handleCameraPhotosChange = useCallback((newCameraPhotos: CameraPhoto[]) => {
    setCameraPhotos(newCameraPhotos);

    // Convertir CameraPhoto a PackagePhoto para compatibilidad con el resto del formulario
    const convertedPhotos: PackagePhoto[] = newCameraPhotos.map((cameraPhoto, index) => ({
      id: cameraPhoto.id,
      file: cameraPhoto.originalFile,
      preview: cameraPhoto.compressedDataUrl,
      type: 'package', // Por ahora todas como 'package', luego se puede hacer más específico
      description: `Foto ${index + 1} - ${new Date(cameraPhoto.metadata.timestamp).toLocaleString()}`
    }));

    setPhotos(convertedPhotos);
    console.log(`📷 ${newCameraPhotos.length} fotos actualizadas desde cámara real`);
  }, []);

  // Capturar foto premium (método original como fallback)
  const handleCapturePhoto = async (type: PackagePhoto['type']) => {
    try {
      const file = await PremiumCameraService.capturePhoto(type);
      if (file) {
        const preview = await PremiumCameraService.createPhotoPreview(file);
        const newPhoto: PackagePhoto = {
          id: Date.now().toString(),
          file,
          preview,
          type,
          description: `Foto ${type} - ${new Date().toLocaleString()}`
        };
        setPhotos(prev => [...prev, newPhoto]);
      }
    } catch (error) {
      console.error('Error capturando foto:', error);
    }
  };

  // Eliminar foto
  const handleRemovePhoto = (photoId: string) => {
    setPhotos(prev => prev.filter(p => p.id !== photoId));
  };

  // Generar etiqueta premium
  const handleGenerateLabel = () => {
    if (!price) return;

    const label = PremiumQRService.createPackageLabel(formData, price);
    setPackageLabel(label);
    setStep('label');
  };

  // Imprimir etiqueta
  const handlePrintLabel = () => {
    if (!packageLabel) return;

    const printWindow = window.open('', '_blank');
    if (printWindow) {
      printWindow.document.write(PremiumQRService.generatePrintableLabel(packageLabel));
      printWindow.document.close();
      printWindow.print();
    }
  };

  // Guardar paquete
  const handleSavePackage = async () => {
    if (!packageLabel || !price) return;

    setIsSaving(true);
    try {
      const packageData = {
        numero_guia: packageLabel.trackingNumber,
        remitente_nombre: formData.senderName,
        remitente_direccion: formData.senderAddress,
        remitente_telefono: formData.senderPhone || 'No especificado',
        destinatario_nombre: formData.recipientName,
        destinatario_direccion: formData.recipientAddress,
        destinatario_telefono: formData.recipientPhone || 'No especificado',
        peso: parseFloat(formData.weight),
        descripcion: formData.description,
        precio_usd: price.total,
        precio_cup: price.totalCUP,
        es_urgente: formData.isUrgent,
        es_fragil: formData.isFragile,
        tiene_seguro: formData.hasInsurance,
        valor_declarado: parseFloat(formData.declaredValue) || 0,
        es_internacional: formData.isInternational
      };

      await api.post('/envios/', packageData);
      console.log('✅ Paquete premium guardado exitosamente');

      // Reset form
      setStep('info');
      setFormData({
        senderName: '', senderPhone: '', senderAddress: '', senderEmail: '',
        recipientName: '', recipientPhone: '', recipientAddress: '', recipientEmail: '',
        weight: '', dimensions: { length: '', width: '', height: '' },
        description: '', category: '', packageSize: '',
        isInternational: false, isUrgent: false, isFragile: false, hasInsurance: false,
        declaredValue: '', currency: 'USD', requiresSignature: false, needsCustoms: false,
        specialInstructions: ''
      });
      setPrice(null);
      setPhotos([]);
      setPackageLabel(null);
      setErrors({});

    } catch (error) {
      console.error('❌ Error guardando paquete:', error);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-cyan-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">

          {/* Header Premium */}
          <div className="bg-gradient-to-r from-purple-600 via-blue-600 to-cyan-600 p-6 text-center text-white">
            <div className="inline-flex items-center bg-white/20 backdrop-blur-sm px-6 py-3 rounded-full text-sm font-bold mb-4">
              <Star className="w-5 h-5 mr-2" />
              MODO PREMIUM - COMPLETO
            </div>
            <h1 className="text-3xl font-bold mb-2">
              🏆 Packfy Cuba Premium
            </h1>
            <p className="text-purple-100">
              Formulario completo con todas las funcionalidades premium
            </p>
          </div>

          {/* Indicador de pasos premium */}
          <div className="flex items-center justify-center py-6 bg-gray-50">
            {[
              { key: 'info', label: 'Información', icon: Package },
              { key: 'price', label: 'Precio', icon: Calculator },
              { key: 'photos', label: 'Fotos', icon: Camera },
              { key: 'label', label: 'Etiqueta', icon: QrCode }
            ].map((s, i) => (
              <div key={s.key} className="flex items-center">
                <div className={`w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all ${
                  step === s.key
                    ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg scale-110'
                    : 'bg-gray-300 text-gray-600'
                }`}>
                  <s.icon className="w-6 h-6" />
                </div>
                <span className={`ml-3 text-sm font-medium ${
                  step === s.key ? 'text-purple-600 font-bold' : 'text-gray-500'
                }`}>
                  {s.label}
                </span>
                {i < 3 && <div className="w-12 h-1 mx-6 bg-gray-200 rounded" />}
              </div>
            ))}
          </div>

          <div className="p-8">
            {/* PASO 1: INFORMACIÓN COMPLETA */}
            {step === 'info' && (
              <div className="space-y-8">
                <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
                  📋 Información Completa del Paquete
                </h2>

                <form onSubmit={handleSubmit} className="space-y-8">

                  {/* Datos del Remitente */}
                  <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
                    <h3 className="text-lg font-semibold text-blue-800 mb-4 flex items-center">
                      <User className="w-5 h-5 mr-2" />
                      Datos del Remitente
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium mb-2">Nombre Completo *</label>
                        <input
                          type="text"
                          value={formData.senderName}
                          onChange={(e) => setFormData(prev => ({ ...prev, senderName: e.target.value }))}
                          className={`w-full px-4 py-3 border rounded-lg ${
                            errors.senderName ? 'border-red-500' : 'border-gray-300'
                          }`}
                          placeholder="Nombre del remitente"
                        />
                        {errors.senderName && <p className="text-red-500 text-xs mt-1">{errors.senderName}</p>}
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2">Teléfono</label>
                        <input
                          type="tel"
                          value={formData.senderPhone}
                          onChange={(e) => setFormData(prev => ({ ...prev, senderPhone: e.target.value }))}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg"
                          placeholder="+1 305-123-4567"
                        />
                      </div>
                      <div className="md:col-span-2">
                        <label className="block text-sm font-medium mb-2">Dirección *</label>
                        <textarea
                          value={formData.senderAddress}
                          onChange={(e) => setFormData(prev => ({ ...prev, senderAddress: e.target.value }))}
                          className={`w-full px-4 py-3 border rounded-lg resize-none ${
                            errors.senderAddress ? 'border-red-500' : 'border-gray-300'
                          }`}
                          placeholder="Dirección completa del remitente"
                          rows={3}
                        />
                        {errors.senderAddress && <p className="text-red-500 text-xs mt-1">{errors.senderAddress}</p>}
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2">Email</label>
                        <input
                          type="email"
                          value={formData.senderEmail}
                          onChange={(e) => setFormData(prev => ({ ...prev, senderEmail: e.target.value }))}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg"
                          placeholder="email@ejemplo.com"
                        />
                      </div>
                    </div>
                  </div>

                  {/* Datos del Destinatario */}
                  <div className="bg-green-50 border border-green-200 rounded-xl p-6">
                    <h3 className="text-lg font-semibold text-green-800 mb-4 flex items-center">
                      <MapPin className="w-5 h-5 mr-2" />
                      Datos del Destinatario (Cuba)
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium mb-2">Nombre Completo *</label>
                        <input
                          type="text"
                          value={formData.recipientName}
                          onChange={(e) => setFormData(prev => ({ ...prev, recipientName: e.target.value }))}
                          className={`w-full px-4 py-3 border rounded-lg ${
                            errors.recipientName ? 'border-red-500' : 'border-gray-300'
                          }`}
                          placeholder="Nombre del destinatario"
                        />
                        {errors.recipientName && <p className="text-red-500 text-xs mt-1">{errors.recipientName}</p>}
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2">Teléfono</label>
                        <input
                          type="tel"
                          value={formData.recipientPhone}
                          onChange={(e) => setFormData(prev => ({ ...prev, recipientPhone: e.target.value }))}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg"
                          placeholder="+53 5123-4567"
                        />
                      </div>
                      <div className="md:col-span-2">
                        <label className="block text-sm font-medium mb-2">Dirección en Cuba *</label>
                        <textarea
                          value={formData.recipientAddress}
                          onChange={(e) => setFormData(prev => ({ ...prev, recipientAddress: e.target.value }))}
                          className={`w-full px-4 py-3 border rounded-lg resize-none ${
                            errors.recipientAddress ? 'border-red-500' : 'border-gray-300'
                          }`}
                          placeholder="Calle, número, entre calles, municipio, provincia..."
                          rows={3}
                        />
                        {errors.recipientAddress && <p className="text-red-500 text-xs mt-1">{errors.recipientAddress}</p>}
                      </div>
                    </div>
                  </div>

                  {/* Información del Paquete */}
                  <div className="bg-purple-50 border border-purple-200 rounded-xl p-6">
                    <h3 className="text-lg font-semibold text-purple-800 mb-4 flex items-center">
                      <Package className="w-5 h-5 mr-2" />
                      Información del Paquete
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div>
                        <label className="block text-sm font-medium mb-2">Peso (lbs) *</label>
                        <input
                          type="number"
                          step="0.1"
                          min="0.1"
                          max="100"
                          value={formData.weight}
                          onChange={(e) => setFormData(prev => ({ ...prev, weight: e.target.value }))}
                          className={`w-full px-4 py-3 border rounded-lg ${
                            errors.weight ? 'border-red-500' : 'border-gray-300'
                          }`}
                          placeholder="5.5"
                        />
                        {errors.weight && <p className="text-red-500 text-xs mt-1">{errors.weight}</p>}
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2">Largo (cm)</label>
                        <input
                          type="number"
                          step="0.1"
                          value={formData.dimensions.length}
                          onChange={(e) => setFormData(prev => ({
                            ...prev,
                            dimensions: { ...prev.dimensions, length: e.target.value }
                          }))}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg"
                          placeholder="30"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2">Ancho (cm)</label>
                        <input
                          type="number"
                          step="0.1"
                          value={formData.dimensions.width}
                          onChange={(e) => setFormData(prev => ({
                            ...prev,
                            dimensions: { ...prev.dimensions, width: e.target.value }
                          }))}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg"
                          placeholder="20"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2">Alto (cm)</label>
                        <input
                          type="number"
                          step="0.1"
                          value={formData.dimensions.height}
                          onChange={(e) => setFormData(prev => ({
                            ...prev,
                            dimensions: { ...prev.dimensions, height: e.target.value }
                          }))}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg"
                          placeholder="15"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2">Categoría</label>
                        <select
                          value={formData.category}
                          onChange={(e) => setFormData(prev => ({ ...prev, category: e.target.value }))}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg"
                          aria-label="Categoría del paquete"
                        >
                          <option value="">Seleccionar...</option>
                          <option value="electronics">Electrónicos</option>
                          <option value="clothes">Ropa</option>
                          <option value="medicine">Medicinas</option>
                          <option value="food">Alimentos</option>
                          <option value="documents">Documentos</option>
                          <option value="other">Otros</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2">Tamaño</label>
                        <select
                          value={formData.packageSize}
                          onChange={(e) => setFormData(prev => ({ ...prev, packageSize: e.target.value }))}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg"
                          aria-label="Tamaño del paquete"
                        >
                          <option value="">Seleccionar...</option>
                          <option value="small">Pequeño</option>
                          <option value="medium">Mediano</option>
                          <option value="large">Grande</option>
                          <option value="xlarge">Extra Grande</option>
                        </select>
                      </div>
                      <div className="md:col-span-3">
                        <label className="block text-sm font-medium mb-2">Descripción *</label>
                        <textarea
                          value={formData.description}
                          onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                          className={`w-full px-4 py-3 border rounded-lg resize-none ${
                            errors.description ? 'border-red-500' : 'border-gray-300'
                          }`}
                          placeholder="Describe detalladamente el contenido del paquete..."
                          rows={3}
                        />
                        {errors.description && <p className="text-red-500 text-xs mt-1">{errors.description}</p>}
                      </div>
                    </div>
                  </div>

                  {/* Opciones Premium */}
                  <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6">
                    <h3 className="text-lg font-semibold text-yellow-800 mb-4 flex items-center">
                      <Star className="w-5 h-5 mr-2" />
                      Opciones Premium
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      <label className="flex items-center space-x-3 p-3 border border-yellow-300 rounded-lg hover:bg-yellow-100 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={formData.isUrgent}
                          onChange={(e) => setFormData(prev => ({ ...prev, isUrgent: e.target.checked }))}
                          className="w-4 h-4 text-yellow-600 rounded"
                        />
                        <span className="text-sm font-medium">🚀 Envío Urgente (+25%)</span>
                      </label>
                      <label className="flex items-center space-x-3 p-3 border border-yellow-300 rounded-lg hover:bg-yellow-100 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={formData.isFragile}
                          onChange={(e) => setFormData(prev => ({ ...prev, isFragile: e.target.checked }))}
                          className="w-4 h-4 text-yellow-600 rounded"
                        />
                        <span className="text-sm font-medium">💎 Frágil</span>
                      </label>
                      <label className="flex items-center space-x-3 p-3 border border-yellow-300 rounded-lg hover:bg-yellow-100 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={formData.hasInsurance}
                          onChange={(e) => setFormData(prev => ({ ...prev, hasInsurance: e.target.checked }))}
                          className="w-4 h-4 text-yellow-600 rounded"
                        />
                        <span className="text-sm font-medium">🛡️ Seguro</span>
                      </label>
                      <label className="flex items-center space-x-3 p-3 border border-yellow-300 rounded-lg hover:bg-yellow-100 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={formData.isInternational}
                          onChange={(e) => setFormData(prev => ({ ...prev, isInternational: e.target.checked }))}
                          className="w-4 h-4 text-yellow-600 rounded"
                        />
                        <span className="text-sm font-medium">🌍 Internacional (+30%)</span>
                      </label>
                      <label className="flex items-center space-x-3 p-3 border border-yellow-300 rounded-lg hover:bg-yellow-100 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={formData.requiresSignature}
                          onChange={(e) => setFormData(prev => ({ ...prev, requiresSignature: e.target.checked }))}
                          className="w-4 h-4 text-yellow-600 rounded"
                        />
                        <span className="text-sm font-medium">✍️ Firma Requerida (+$5)</span>
                      </label>
                      <label className="flex items-center space-x-3 p-3 border border-yellow-300 rounded-lg hover:bg-yellow-100 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={formData.needsCustoms}
                          onChange={(e) => setFormData(prev => ({ ...prev, needsCustoms: e.target.checked }))}
                          className="w-4 h-4 text-yellow-600 rounded"
                        />
                        <span className="text-sm font-medium">📋 Declaración Aduanal (+$8)</span>
                      </label>
                    </div>

                    {formData.hasInsurance && (
                      <div className="mt-4">
                        <label className="block text-sm font-medium mb-2">Valor Declarado (${formData.currency}) *</label>
                        <div className="flex gap-2">
                          <input
                            type="number"
                            step="0.01"
                            min="0"
                            value={formData.declaredValue}
                            onChange={(e) => setFormData(prev => ({ ...prev, declaredValue: e.target.value }))}
                            className={`flex-1 px-4 py-3 border rounded-lg ${
                              errors.declaredValue ? 'border-red-500' : 'border-gray-300'
                            }`}
                            placeholder="100.00"
                          />
                          <select
                            value={formData.currency}
                            onChange={(e) => setFormData(prev => ({ ...prev, currency: e.target.value as 'USD' | 'CUP' }))}
                            className="px-4 py-3 border border-gray-300 rounded-lg"
                            aria-label="Moneda"
                          >
                            <option value="USD">USD</option>
                            <option value="CUP">CUP</option>
                          </select>
                        </div>
                        {errors.declaredValue && <p className="text-red-500 text-xs mt-1">{errors.declaredValue}</p>}
                      </div>
                    )}

                    <div className="mt-4">
                      <label className="block text-sm font-medium mb-2">Instrucciones Especiales</label>
                      <textarea
                        value={formData.specialInstructions}
                        onChange={(e) => setFormData(prev => ({ ...prev, specialInstructions: e.target.value }))}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg resize-none"
                        placeholder="Instrucciones especiales de manejo o entrega..."
                        rows={2}
                      />
                    </div>
                  </div>

                  <button
                    type="submit"
                    className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-4 rounded-lg font-bold hover:from-purple-700 hover:to-blue-700 transition-all shadow-lg"
                  >
                    <div className="flex items-center justify-center">
                      <Calculator className="w-6 h-6 mr-3" />
                      Calcular Precio Premium
                    </div>
                  </button>
                </form>
              </div>
            )}

            {/* PASO 2: PRECIO PREMIUM */}
            {step === 'price' && price && (
              <div className="text-center space-y-6">
                <h2 className="text-2xl font-bold text-gray-800 mb-6">
                  💰 Cálculo Premium Completo
                </h2>

                <div className="bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-xl p-8">
                  <div className="text-4xl font-bold text-green-600 mb-4">
                    ${price.totalCUP.toLocaleString()} CUP
                  </div>
                  <div className="text-xl text-gray-600 mb-6">
                    (${price.total.toFixed(2)} USD)
                  </div>

                  <div className="bg-white rounded-lg p-6 text-left space-y-3">
                    <h3 className="font-bold text-lg mb-4 text-center">Desglose de Precios</h3>

                    <div className="flex justify-between py-2 border-b">
                      <span>Precio base ({price.weightRange}):</span>
                      <span className="font-medium">${price.basePrice.toFixed(2)} USD</span>
                    </div>

                    <div className="flex justify-between py-2 border-b">
                      <span>Manejo (15%):</span>
                      <span className="font-medium">${price.handling.toFixed(2)} USD</span>
                    </div>

                    {price.insurance > 0 && (
                      <div className="flex justify-between py-2 border-b text-blue-600">
                        <span>🛡️ Seguro:</span>
                        <span className="font-medium">${price.insurance.toFixed(2)} USD</span>
                      </div>
                    )}

                    {price.urgent > 0 && (
                      <div className="flex justify-between py-2 border-b text-orange-600">
                        <span>🚀 Urgente (25%):</span>
                        <span className="font-medium">${price.urgent.toFixed(2)} USD</span>
                      </div>
                    )}

                    {price.international > 0 && (
                      <div className="flex justify-between py-2 border-b text-purple-600">
                        <span>🌍 Internacional (30%):</span>
                        <span className="font-medium">${price.international.toFixed(2)} USD</span>
                      </div>
                    )}

                    {price.signature > 0 && (
                      <div className="flex justify-between py-2 border-b text-indigo-600">
                        <span>✍️ Firma requerida:</span>
                        <span className="font-medium">${price.signature.toFixed(2)} USD</span>
                      </div>
                    )}

                    {price.customs > 0 && (
                      <div className="flex justify-between py-2 border-b text-red-600">
                        <span>📋 Declaración aduanal:</span>
                        <span className="font-medium">${price.customs.toFixed(2)} USD</span>
                      </div>
                    )}

                    <div className="flex justify-between py-3 border-t-2 border-gray-300 font-bold text-lg">
                      <span>TOTAL:</span>
                      <span className="text-green-600">${price.total.toFixed(2)} USD</span>
                    </div>
                  </div>
                </div>

                <div className="flex gap-4">
                  <button
                    onClick={() => setStep('info')}
                    className="flex-1 bg-gray-500 text-white py-3 rounded-lg hover:bg-gray-600 font-bold"
                  >
                    ← Modificar Información
                  </button>
                  <button
                    onClick={() => setStep('photos')}
                    className="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 rounded-lg hover:from-purple-700 hover:to-blue-700 font-bold"
                  >
                    Continuar a Fotos →
                  </button>
                </div>
              </div>
            )}

            {/* PASO 3: FOTOS PREMIUM CON CÁMARA REAL */}
            {step === 'photos' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
                  📷 Galería de Fotos Premium
                </h2>

                {/* Componente de cámara real con interfaz visual */}
                <PackageCamera
                  onPhotosChange={handleCameraPhotosChange}
                  maxPhotos={8}
                />

                {/* Información adicional sobre las fotos capturadas */}
                {photos.length > 0 && (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <h4 className="font-semibold text-green-800 mb-2">
                      ✅ {photos.length} foto{photos.length !== 1 ? 's' : ''} capturada{photos.length !== 1 ? 's' : ''}
                    </h4>
                    <p className="text-sm text-green-700">
                      Las fotos han sido comprimidas automáticamente para envío rápido manteniendo la calidad.
                    </p>
                  </div>
                )}

                {/* Botones alternativos para captura específica (fallback) */}
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                  <h4 className="font-medium text-gray-700 mb-3">Captura específica por tipo:</h4>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                    {[
                      { type: 'package' as const, label: '📦 Paquete', color: 'blue' },
                      { type: 'contents' as const, label: '📄 Contenido', color: 'green' },
                      { type: 'dimensions' as const, label: '📏 Dimensiones', color: 'purple' },
                      { type: 'receipt' as const, label: '🧾 Recibo', color: 'orange' }
                    ].map(({ type, label, color }) => (
                      <button
                        key={type}
                        onClick={() => handleCapturePhoto(type)}
                        className={`flex flex-col items-center p-2 border border-${color}-300 rounded-lg hover:border-${color}-500 hover:bg-${color}-50 transition-all text-xs`}
                      >
                        <Camera className={`w-4 h-4 text-${color}-500 mb-1`} />
                        <span className="font-medium">{label}</span>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <h4 className="font-semibold text-yellow-800 mb-2">💡 Consejos para mejores fotos:</h4>
                  <ul className="text-sm text-yellow-700 space-y-1">
                    <li>• Usa buena iluminación natural</li>
                    <li>• Incluye toda la información visible del paquete</li>
                    <li>• Toma fotos desde diferentes ángulos</li>
                    <li>• Asegúrate de que las etiquetas sean legibles</li>
                  </ul>
                </div>

                <div className="flex gap-4">
                  <button
                    onClick={() => setStep('price')}
                    className="flex-1 bg-gray-500 text-white py-3 rounded-lg hover:bg-gray-600 font-bold"
                  >
                    ← Volver al Precio
                  </button>
                  <button
                    onClick={handleGenerateLabel}
                    className="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 rounded-lg hover:from-purple-700 hover:to-blue-700 font-bold"
                  >
                    Generar Etiqueta →
                  </button>
                </div>
              </div>
            )}

            {/* PASO 4: ETIQUETA PREMIUM */}
            {step === 'label' && packageLabel && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
                  🏷️ Etiqueta Premium Generada
                </h2>

                <div className="bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-xl p-8 text-center">
                  <div className="inline-flex items-center bg-green-100 px-6 py-3 rounded-full mb-6">
                    <CheckCircle className="w-6 h-6 text-green-600 mr-2" />
                    <span className="font-bold text-green-800">¡Paquete Registrado Exitosamente!</span>
                  </div>

                  <div className="bg-white rounded-lg p-6 mb-6">
                    <h3 className="text-xl font-bold mb-4">Código de Seguimiento</h3>
                    <div className="text-3xl font-mono bg-gray-100 p-4 rounded-lg border-2 border-dashed border-gray-300 mb-4">
                      {packageLabel.trackingNumber}
                    </div>
                    <div className="text-sm text-gray-600">
                      Generado: {packageLabel.generatedAt.toLocaleString()}
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-6 text-left">
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <h4 className="font-bold text-blue-800 mb-2">👤 Remitente</h4>
                      <p className="text-sm">
                        <strong>{packageLabel.sender.name}</strong><br />
                        {packageLabel.sender.address}<br />
                        {packageLabel.sender.phone}
                      </p>
                    </div>
                    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                      <h4 className="font-bold text-green-800 mb-2">📍 Destinatario</h4>
                      <p className="text-sm">
                        <strong>{packageLabel.recipient.name}</strong><br />
                        {packageLabel.recipient.address}<br />
                        {packageLabel.recipient.phone}
                      </p>
                    </div>
                  </div>

                  <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mt-4">
                    <h4 className="font-bold text-purple-800 mb-2">📦 Información del Paquete</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <strong>Peso:</strong><br />
                        {packageLabel.packageInfo.weight} lbs
                      </div>
                      <div>
                        <strong>Valor:</strong><br />
                        ${packageLabel.packageInfo.value} USD
                      </div>
                      <div>
                        <strong>Precio:</strong><br />
                        ${packageLabel.packageInfo.price.toFixed(2)} USD
                      </div>
                      <div>
                        <strong>Fotos:</strong><br />
                        {photos.length} adjuntas
                      </div>
                    </div>
                  </div>
                </div>

                <div className="flex gap-4">
                  <button
                    onClick={handlePrintLabel}
                    className="flex-1 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 font-bold flex items-center justify-center"
                  >
                    <Printer className="w-5 h-5 mr-2" />
                    Imprimir Etiqueta
                  </button>
                  <button
                    onClick={handleSavePackage}
                    disabled={isSaving}
                    className="flex-1 bg-gradient-to-r from-green-600 to-blue-600 text-white py-3 rounded-lg hover:from-green-700 hover:to-blue-700 font-bold flex items-center justify-center disabled:opacity-50"
                  >
                    <Save className="w-5 h-5 mr-2" />
                    {isSaving ? 'Guardando...' : 'Guardar y Finalizar'}
                  </button>
                </div>

                <div className="text-center">
                  <button
                    onClick={() => {
                      setStep('info');
                      setFormData({
                        senderName: '', senderPhone: '', senderAddress: '', senderEmail: '',
                        recipientName: '', recipientPhone: '', recipientAddress: '', recipientEmail: '',
                        weight: '', dimensions: { length: '', width: '', height: '' },
                        description: '', category: '', packageSize: '',
                        isInternational: false, isUrgent: false, isFragile: false, hasInsurance: false,
                        declaredValue: '', currency: 'USD', requiresSignature: false, needsCustoms: false,
                        specialInstructions: ''
                      });
                      setPrice(null);
                      setPhotos([]);
                      setPackageLabel(null);
                      setErrors({});
                    }}
                    className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 font-bold"
                  >
                    📦 Registrar Nuevo Paquete Premium
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PremiumCompleteForm;
