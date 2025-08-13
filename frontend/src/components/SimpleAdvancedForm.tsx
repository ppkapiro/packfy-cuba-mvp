import React, { useState, useCallback } from 'react';
import { Package, Camera, QrCode, DollarSign, Star, CheckCircle, MapPin, User, Weight, Calculator } from 'lucide-react';
import { api } from '../services/api';
import '../styles/simple-mode.css';

// Interfaces mejoradas
interface PackageData {
  senderName: string;
  senderPhone: string;
  senderAddress: string;
  recipientName: string;
  recipientPhone: string;
  recipientAddress: string;
  weight: string;
  description: string;
  category: string;
  packageSize: string;
  isInternational: boolean;
  isUrgent: boolean;
  isFragile: boolean;
  declaredValue: string;
}

interface PriceBreakdown {
  basePrice: number;
  insurance: number;
  handling: number;
  urgent: number;
  total: number;
  totalCUP: number;
  weightRange: string;
}

// Servicio de conversión mejorado (Sistema en Libras)
const SimpleCurrencyService = {
  rate: 320, // USD a CUP

  calculatePrice(weightLbs: number, hasInsurance = false, hasUrgent = false): PriceBreakdown {
    // Cálculo de precio base mejorado en libras
    let basePrice = 8.50; // Precio base para hasta 2.2 lbs (1kg)

    if (weightLbs <= 2.2) basePrice = 8.50;        // Hasta 2.2 lbs (1kg)
    else if (weightLbs <= 4.4) basePrice = 15.00;  // 2.2-4.4 lbs (1-2kg)
    else if (weightLbs <= 11) basePrice = 28.00;   // 4.4-11 lbs (2-5kg)
    else if (weightLbs <= 22) basePrice = 45.00;   // 11-22 lbs (5-10kg)
    else if (weightLbs <= 44) basePrice = 85.00;   // 22-44 lbs (10-20kg)
    else basePrice = 85.00 + ((weightLbs - 44) * 2.05); // Más de 44 lbs (>20kg)

    // Servicios adicionales
    const insurance = hasInsurance ? basePrice * 0.05 : 0;
    const handling = basePrice * 0.15;
    const urgent = hasUrgent ? basePrice * 0.25 : 0;

    const total = basePrice + insurance + handling + urgent;
    const totalCUP = total * this.rate;

    return {
      basePrice,
      insurance,
      handling,
      urgent,
      total,
      totalCUP,
      weightRange: this.getWeightRange(weightLbs)
    };
  },

  getWeightRange(weightLbs: number): string {
    if (weightLbs <= 2.2) return "Hasta 2.2 lbs";
    if (weightLbs <= 4.4) return "2.2-4.4 lbs";
    if (weightLbs <= 11) return "4.4-11 lbs";
    if (weightLbs <= 22) return "11-22 lbs";
    if (weightLbs <= 44) return "22-44 lbs";
    return `Más de 44 lbs`;
  }
};

// Servicio de cámara mejorado
const SimpleCameraService = {
  async capturePhoto(): Promise<File | null> {
    return new Promise((resolve) => {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*';
      input.capture = 'environment';

      input.onchange = (e) => {
        const file = (e.target as HTMLInputElement).files?.[0];
        if (file) {
          console.log('📷 Foto capturada:', file.name, `${(file.size/1024/1024).toFixed(2)}MB`);
        }
        resolve(file || null);
      };

      input.oncancel = () => {
        console.log('📷 Captura cancelada por el usuario');
        resolve(null);
      };

      input.click();
    });
  }
};

// Servicio de QR simplificado
const SimpleQRService = {
  generateTrackingNumber(): string {
    const timestamp = Date.now().toString().slice(-8);
    return `PCK${timestamp}`;
  },

  createQRData(packageInfo: any): string {
    return JSON.stringify({
      tracking: this.generateTrackingNumber(),
      weight: packageInfo.weight,
      destination: packageInfo.destination,
      created: new Date().toLocaleDateString()
    });
  }
};

// Componente Modo Simple (Gratuito) - Mejorado
const SimpleAdvancedForm: React.FC = () => {
  const [step, setStep] = useState<'info' | 'price' | 'photo' | 'qr'>('info');

  const [formData, setFormData] = useState<PackageData>({
    senderName: '',
    senderPhone: '',
    senderAddress: '',
    recipientName: '',
    recipientPhone: '',
    recipientAddress: '',
    weight: '',
    description: '',
    category: '',
    packageSize: '',
    isInternational: false,
    isUrgent: false,
    isFragile: false,
    declaredValue: ''
  });

  const [priceBreakdown, setPriceBreakdown] = useState<PriceBreakdown | null>(null);
  const [isCalculating, setIsCalculating] = useState(false);
  const [photo, setPhoto] = useState<File | null>(null);
  const [tracking, setTracking] = useState<string>('');
  const [errors, setErrors] = useState<{[key: string]: string}>({});

  // Debug logging
  console.log('🔍 Render Debug - step:', step, 'priceBreakdown exists:', !!priceBreakdown);

  // Función simple para manejar cambios
  const handleFieldChange = useCallback((field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Limpiar error del campo cuando el usuario empiece a escribir
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  }, [errors]);

  // Callbacks específicos para campos de peso
  const handleWeightChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    handleFieldChange('weight', e.target.value);
  }, [handleFieldChange]);

  // Validación de formulario mejorada
  const validateForm = (): boolean => {
    const newErrors: {[key: string]: string} = {};

    // Campos del remitente son opcionales en modo simple
    if (formData.senderName.trim() && formData.senderName.length < 2) {
      newErrors.senderName = 'Nombre debe tener al menos 2 caracteres';
    }

    if (formData.senderPhone.trim() && !/^\+?[\d\s-()]{8,15}$/.test(formData.senderPhone)) {
      newErrors.senderPhone = 'Formato de teléfono inválido';
    }

    if (formData.senderAddress.trim() && formData.senderAddress.length < 10) {
      newErrors.senderAddress = 'Dirección debe ser más específica (mínimo 10 caracteres)';
    }

    // Campos del destinatario son REQUERIDOS
    if (!formData.recipientName.trim()) {
      newErrors.recipientName = 'Nombre del destinatario es requerido';
    } else if (formData.recipientName.length < 2) {
      newErrors.recipientName = 'Nombre debe tener al menos 2 caracteres';
    }

    if (!formData.recipientAddress.trim()) {
      newErrors.recipientAddress = 'Dirección es requerida';
    } else if (formData.recipientAddress.length < 10) {
      newErrors.recipientAddress = 'Dirección debe ser más específica (mínimo 10 caracteres)';
    }

    if (formData.recipientPhone.trim() && !/^\+?[\d\s-()]{8,15}$/.test(formData.recipientPhone)) {
      newErrors.recipientPhone = 'Formato de teléfono inválido';
    }

    // Peso es requerido
    const weight = parseFloat(formData.weight);
    if (!formData.weight.trim()) {
      newErrors.weight = 'Peso es requerido';
    } else if (isNaN(weight) || weight <= 0) {
      newErrors.weight = 'Peso debe ser un número válido mayor a 0';
    } else if (weight < 0.1) {
      newErrors.weight = 'Peso mínimo: 0.1 lbs';
    } else if (weight > 110) {
      newErrors.weight = 'Peso máximo: 110 lbs';
    }

    // Descripción es requerida
    if (!formData.description.trim()) {
      newErrors.description = 'Descripción del contenido es requerida';
    } else if (formData.description.length < 5) {
      newErrors.description = 'Descripción debe ser más detallada (mínimo 5 caracteres)';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Manejar envío del paso de información
  const handleInfoSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('📝 Validando formulario...');

    if (!validateForm()) {
      console.log('❌ Formulario inválido, errores:', errors);
      return;
    }

    setIsCalculating(true);

    try {
      // Calcular precio
      const weight = parseFloat(formData.weight);
      const calculatedPrice = SimpleCurrencyService.calculatePrice(
        weight,
        formData.declaredValue.trim() !== '',
        formData.isUrgent
      );

      console.log('💰 Precio calculado:', calculatedPrice);
      setPriceBreakdown(calculatedPrice);

      // Intentar guardar en el backend
      if (!formData.recipientName || !formData.recipientAddress ||
          !formData.recipientPhone || !formData.weight ||
          !formData.description) {
        console.log('⚠️ Faltan campos requeridos para el backend');
        setStep('price');
        return;
      }

      const packageData = {
        remitente_nombre: formData.senderName || 'Cliente Anónimo',
        remitente_direccion: formData.senderAddress || 'Miami, FL',
        remitente_telefono: formData.senderPhone || 'No especificado',
        destinatario_nombre: formData.recipientName,
        destinatario_direccion: formData.recipientAddress,
        destinatario_telefono: formData.recipientPhone,
        peso: parseFloat(formData.weight),
        descripcion: formData.description,
        precio_usd: calculatedPrice.total,
        precio_cup: calculatedPrice.totalCUP,
        es_urgente: formData.isUrgent,
        es_fragil: formData.isFragile,
        valor_declarado: formData.declaredValue ? parseFloat(formData.declaredValue) : null,
        categoria: formData.category || 'General',
        tamano: formData.packageSize || 'Mediano'
      };

      console.log('🚀 Enviando al backend:', packageData);
      const response = await api.post('/envios/', packageData);
      console.log('✅ Respuesta del backend:', response.data);

      // Resetear el formulario
      setFormData({
        senderName: '',
        senderPhone: '',
        senderAddress: '',
        recipientName: '',
        recipientPhone: '',
        recipientAddress: '',
        weight: '',
        description: '',
        category: '',
        packageSize: '',
        isInternational: false,
        isUrgent: false,
        isFragile: false,
        declaredValue: ''
      });

      setStep('price');
    } catch (error) {
      console.error('❌ Error guardando en backend:', error);
      // Continuar al siguiente paso aunque falle el backend
      setStep('price');
    } finally {
      setIsCalculating(false);
    }
  };

  // Componente Simple Input para formularios
  const SimpleInput = ({ field, label, type = 'text', placeholder, value, required = false, rows = 1, isTextarea = false }: {
    field: string;
    label: string;
    type?: string;
    placeholder: string;
    value: string;
    required?: boolean;
    rows?: number;
    isTextarea?: boolean;
  }) => {
    const InputComponent = isTextarea ? 'textarea' : 'input';

    return (
      <div className="relative">
        <label className="block text-sm font-medium mb-1">
          {label} {required && <span className="text-red-500">*</span>}
        </label>
        <InputComponent
          type={isTextarea ? undefined : type}
          value={value}
          onChange={(e) => handleFieldChange(field, e.target.value)}
          className={`w-full px-3 py-2 border rounded-lg transition-colors ${isTextarea ? 'resize-none' : ''} ${
            errors[field] ? 'border-red-500 bg-red-50' : 'border-gray-300 focus:border-blue-500'
          }`}
          placeholder={placeholder}
          rows={isTextarea ? rows : undefined}
          autoComplete="off"
        />

        {errors[field] && (
          <p className="text-red-500 text-xs mt-1">{errors[field]}</p>
        )}
      </div>
    );
  };

  // Manejar captura de foto
  const handleCapturePhoto = async () => {
    console.log('📷 Iniciando captura de foto...');
    try {
      const capturedPhoto = await SimpleCameraService.capturePhoto();
      console.log('📷 Resultado de captura:', capturedPhoto);

      if (capturedPhoto) {
        console.log('📷 Foto capturada exitosamente:', capturedPhoto.name, capturedPhoto.size);
        setPhoto(capturedPhoto);
      } else {
        console.log('📷 No se capturó ninguna foto (usuario canceló)');
      }
    } catch (error) {
      console.error('📷 Error capturando foto:', error);
      alert('Error capturando foto: ' + error);
    }
  };

  // Generar QR y completar proceso
  const handleGenerateQR = () => {
    const trackingNumber = SimpleQRService.generateTrackingNumber();
    setTracking(trackingNumber);
    alert(`¡Paquete registrado exitosamente!
Tracking: ${trackingNumber}
Precio: $${priceBreakdown?.totalCUP.toLocaleString()} CUP`);
  };

  // Renderizar pasos del proceso
  const renderSteps = () => {
    const steps = [
      { key: 'info', label: 'Info', icon: Package, active: step === 'info', completed: step !== 'info' },
      { key: 'price', label: 'Precio', icon: DollarSign, active: step === 'price', completed: ['photo', 'qr'].includes(step) },
      { key: 'photo', label: 'Foto', icon: Camera, active: step === 'photo', completed: step === 'qr' },
      { key: 'qr', label: 'QR', icon: QrCode, active: step === 'qr', completed: false }
    ];

    return (
      <div className="flex justify-center mb-6">
        <div className="flex items-center space-x-4">
          {steps.map((s, i) => {
            const Icon = s.icon;
            return (
              <div key={s.key} className="flex items-center">
                <div className={`w-12 h-12 rounded-full flex items-center justify-center transition-all ${
                  s.completed
                    ? 'bg-green-500 text-white'
                    : s.active
                      ? 'bg-blue-600 text-white shadow-lg'
                      : 'bg-gray-200 text-gray-500'
                }`}>
                  {s.completed ? (
                    <CheckCircle className="w-6 h-6" />
                  ) : (
                    <Icon className="w-6 h-6" />
                  )}
                </div>
                <div className="ml-2">
                  <span className={`text-sm font-medium ${s.active ? 'text-blue-600' : s.completed ? 'text-green-600' : 'text-gray-500'}`}>
                    {s.label}
                  </span>
                </div>
                {i < steps.length - 1 && (
                  <div className={`w-8 h-1 mx-4 rounded ${
                    s.completed ? 'bg-green-500' : 'bg-gray-200'
                  }`} />
                )}
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-cyan-50 to-teal-50 py-8 px-4">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white rounded-3xl shadow-2xl overflow-hidden">
          {/* Header con indicador de modo gratuito */}
          <div className="bg-gradient-to-r from-blue-500 to-cyan-500 p-6 text-center relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-full bg-white/10 backdrop-blur-sm"></div>
            <div className="relative z-10">
              <div className="inline-flex items-center bg-white/20 backdrop-blur-sm text-white px-4 py-2 rounded-full text-sm font-bold mb-3 border border-white/30">
                <Package className="w-4 h-4 mr-2" />
                MODO SIMPLE - GRATIS
              </div>
              <h1 className="text-3xl font-bold text-white mb-2">
                🇨🇺 Packfy Cuba
              </h1>
              <p className="text-blue-100 text-lg">
                Registro de Paquete Simplificado
              </p>

              {/* Link a Premium mejorado */}
              <div className="mt-6 p-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl">
                <p className="text-white/90 text-sm mb-3">
                  ¿Necesitas funciones avanzadas?
                </p>
                <a
                  href="/envios"
                  className="inline-flex items-center bg-white text-blue-600 px-6 py-2 rounded-full font-bold text-sm hover:bg-blue-50 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105"
                >
                  <Star className="w-4 h-4 mr-2" />
                  Actualizar a Premium ✨
                </a>
              </div>
            </div>
          </div>

          <div className="p-8">

        {renderSteps()}

        {step === 'info' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              📦 Información del Paquete
            </h2>

            <form onSubmit={handleInfoSubmit} className="space-y-6">
              {/* Información del Remitente */}
              <div className="bg-blue-50 rounded-xl p-6">
                <h4 className="font-semibold text-blue-800 mb-4 flex items-center">
                  <User className="w-5 h-5 mr-2" />
                  Información del Remitente (Opcional)
                </h4>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <SimpleInput
                    field="senderName"
                    label="Nombre Completo"
                    placeholder="Tu nombre completo (opcional)"
                    value={formData.senderName}
                  />

                  <SimpleInput
                    field="senderPhone"
                    label="Teléfono"
                    type="tel"
                    placeholder="+1 305-123-4567"
                    value={formData.senderPhone}
                  />
                </div>

                <div className="mt-4">
                  <SimpleInput
                    field="senderAddress"
                    label="Dirección en Miami"
                    placeholder="Calle, número, ciudad, estado, código postal..."
                    value={formData.senderAddress}
                    isTextarea={true}
                    rows={3}
                  />
                </div>
              </div>

              {/* Información del Destinatario */}
              <div className="bg-green-50 rounded-xl p-6">
                <h4 className="font-semibold text-green-800 mb-4 flex items-center">
                  <MapPin className="w-5 h-5 mr-2" />
                  Información del Destinatario
                </h4>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <SimpleInput
                    field="recipientName"
                    label="Nombre Completo"
                    placeholder="Nombre del destinatario"
                    value={formData.recipientName}
                    required={true}
                  />

                  <SimpleInput
                    field="recipientPhone"
                    label="Teléfono"
                    type="tel"
                    placeholder="+53 5123-4567"
                    value={formData.recipientPhone}
                    required={true}
                  />
                </div>

                <div className="mt-4">
                  <SimpleInput
                    field="recipientAddress"
                    label="Dirección Completa en Cuba"
                    placeholder="Calle, número, entre calles, municipio, provincia..."
                    value={formData.recipientAddress}
                    isTextarea={true}
                    rows={3}
                    required={true}
                  />
                </div>
              </div>

              {/* Información del Paquete */}
              <div className="bg-orange-50 rounded-xl p-6">
                <h4 className="font-semibold text-orange-800 mb-4 flex items-center">
                  <Weight className="w-5 h-5 mr-2" />
                  Información del Paquete
                </h4>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Peso (lbs) <span className="text-red-500">*</span></label>
                    <input
                      type="number"
                      step="0.1"
                      min="0.1"
                      max="110"
                      value={formData.weight}
                      onChange={handleWeightChange}
                      className={`w-full px-3 py-2 border rounded-lg transition-colors ${
                        errors.weight ? 'border-red-500 bg-red-50' : 'border-gray-300 focus:border-blue-500'
                      }`}
                      placeholder="5.5"
                      required
                      autoComplete="off"
                    />
                    {errors.weight && (
                      <p className="text-red-500 text-xs mt-1">{errors.weight}</p>
                    )}
                    <p className="text-xs text-gray-500 mt-1">
                      💡 Peso mínimo: 0.1 lbs | Máximo: 110 lbs
                    </p>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <label className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          checked={formData.isUrgent}
                          onChange={(e) => handleFieldChange('isUrgent', e.target.checked.toString())}
                          className="w-4 h-4 text-blue-600 rounded"
                        />
                        <span className="text-sm">📦 Urgente (+25%)</span>
                      </label>
                    </div>

                    <div>
                      <label className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          checked={formData.isFragile}
                          onChange={(e) => handleFieldChange('isFragile', e.target.checked.toString())}
                          className="w-4 h-4 text-blue-600 rounded"
                        />
                        <span className="text-sm">🔍 Frágil</span>
                      </label>
                    </div>
                  </div>
                </div>

                <div className="mt-4">
                  <SimpleInput
                    field="description"
                    label="Descripción del Contenido"
                    placeholder="Describe qué contiene el paquete (requerido para aduana)..."
                    value={formData.description}
                    isTextarea={true}
                    rows={3}
                    required={true}
                  />
                </div>

                <div className="mt-4">
                  <SimpleInput
                    field="declaredValue"
                    label="Valor Declarado (USD)"
                    type="number"
                    placeholder="100.00 (opcional, para seguro)"
                    value={formData.declaredValue}
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    💡 Si declaras valor, se añadirá seguro (+5%)
                  </p>
                </div>
              </div>

              {/* Botón de continuar */}
              <div className="flex justify-center">
                <button
                  type="submit"
                  disabled={isCalculating}
                  className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white px-8 py-3 rounded-xl font-bold text-lg hover:from-blue-700 hover:to-cyan-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isCalculating ? (
                    <div className="flex items-center">
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Calculando...
                    </div>
                  ) : (
                    <div className="flex items-center">
                      <Calculator className="w-5 h-5 mr-2" />
                      Calcular Precio
                    </div>
                  )}
                </button>
              </div>
            </form>
          </div>
        )}

        {step === 'price' && priceBreakdown && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              💰 Cotización de Envío
            </h2>

            <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200">
              <div className="text-center mb-6">
                <div className="text-4xl font-bold text-green-600 mb-2">
                  ${priceBreakdown.totalCUP.toLocaleString()} CUP
                </div>
                <div className="text-lg text-gray-600">
                  (${priceBreakdown.total.toFixed(2)} USD)
                </div>
                <div className="text-sm text-gray-500 mt-2">
                  Peso: {priceBreakdown.weightRange}
                </div>
              </div>

              {/* Desglose de precios */}
              <div className="bg-white rounded-lg p-4 space-y-2">
                <h4 className="font-semibold text-gray-800 mb-3">Desglose de Costos:</h4>

                <div className="flex justify-between text-sm">
                  <span>Precio base ({priceBreakdown.weightRange}):</span>
                  <span>${priceBreakdown.basePrice.toFixed(2)} USD</span>
                </div>

                <div className="flex justify-between text-sm">
                  <span>Manejo y procesamiento (15%):</span>
                  <span>${priceBreakdown.handling.toFixed(2)} USD</span>
                </div>

                {priceBreakdown.insurance > 0 && (
                  <div className="flex justify-between text-sm">
                    <span>Seguro (5%):</span>
                    <span>${priceBreakdown.insurance.toFixed(2)} USD</span>
                  </div>
                )}

                {priceBreakdown.urgent > 0 && (
                  <div className="flex justify-between text-sm">
                    <span>Urgente (25%):</span>
                    <span>${priceBreakdown.urgent.toFixed(2)} USD</span>
                  </div>
                )}

                <hr className="my-2" />

                <div className="flex justify-between font-bold">
                  <span>Total:</span>
                  <span>${priceBreakdown.total.toFixed(2)} USD</span>
                </div>

                <div className="flex justify-between text-lg font-bold text-green-600">
                  <span>En CUP:</span>
                  <span>${priceBreakdown.totalCUP.toLocaleString()} CUP</span>
                </div>
              </div>

              <div className="mt-6 text-center">
                <p className="text-sm text-gray-600 mb-4">
                  💡 Este precio incluye todos los costos hasta la entrega en Cuba
                </p>

                <div className="flex gap-4 justify-center">
                  <button
                    onClick={() => setStep('info')}
                    className="bg-gray-500 text-white px-6 py-2 rounded-lg hover:bg-gray-600 transition-colors"
                  >
                    ← Modificar
                  </button>

                  <button
                    onClick={() => setStep('photo')}
                    className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white px-6 py-2 rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all shadow-lg"
                  >
                    Continuar a Foto →
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {step === 'photo' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              📷 Foto del Paquete
            </h2>

            <div className="bg-blue-50 rounded-xl p-6 text-center">
              {!photo ? (
                <div>
                  <Camera className="w-16 h-16 text-blue-500 mx-auto mb-4" />
                  <p className="text-gray-600 mb-4">
                    Toma una foto del paquete para el registro
                  </p>
                  <button
                    onClick={handleCapturePhoto}
                    className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-bold"
                  >
                    📷 Capturar Foto
                  </button>
                </div>
              ) : (
                <div>
                  <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                  <p className="text-green-600 font-bold mb-2">¡Foto capturada!</p>
                  <p className="text-sm text-gray-600 mb-4">
                    {photo.name} ({(photo.size / 1024 / 1024).toFixed(2)} MB)
                  </p>

                  <div className="flex gap-4 justify-center">
                    <button
                      onClick={handleCapturePhoto}
                      className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600 transition-colors"
                    >
                      📷 Tomar Nueva
                    </button>

                    <button
                      onClick={() => setStep('qr')}
                      className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors font-bold"
                    >
                      Continuar a QR →
                    </button>
                  </div>
                </div>
              )}
            </div>

            <div className="text-center">
              <button
                onClick={() => setStep('price')}
                className="text-gray-500 hover:text-gray-700 transition-colors"
              >
                ← Volver al precio
              </button>
            </div>
          </div>
        )}

        {step === 'qr' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              🎯 Finalizar Registro
            </h2>

            <div className="bg-green-50 rounded-xl p-6 text-center">
              {!tracking ? (
                <div>
                  <QrCode className="w-16 h-16 text-green-500 mx-auto mb-4" />
                  <p className="text-gray-600 mb-4">
                    Genera tu código de seguimiento
                  </p>
                  <button
                    onClick={handleGenerateQR}
                    className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors font-bold"
                  >
                    🎯 Generar QR y Completar
                  </button>
                </div>
              ) : (
                <div>
                  <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                  <h3 className="text-xl font-bold text-green-600 mb-2">
                    ¡Registro Completado!
                  </h3>
                  <div className="bg-white rounded-lg p-4 mt-4">
                    <p className="font-bold mb-2">Código de Seguimiento:</p>
                    <p className="text-2xl font-mono bg-gray-100 p-2 rounded">
                      {tracking}
                    </p>
                  </div>
                  <p className="text-sm text-gray-600 mt-4">
                    Guarda este código para rastrear tu paquete
                  </p>
                </div>
              )}
            </div>

            <div className="text-center">
              <button
                onClick={() => {
                  // Resetear todo para nuevo paquete
                  setStep('info');
                  setFormData({
                    senderName: '',
                    senderPhone: '',
                    senderAddress: '',
                    recipientName: '',
                    recipientPhone: '',
                    recipientAddress: '',
                    weight: '',
                    description: '',
                    category: '',
                    packageSize: '',
                    isInternational: false,
                    isUrgent: false,
                    isFragile: false,
                    declaredValue: ''
                  });
                  setPriceBreakdown(null);
                  setPhoto(null);
                  setTracking('');
                  setErrors({});
                }}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                📦 Registrar Nuevo Paquete
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

export default SimpleAdvancedForm;
