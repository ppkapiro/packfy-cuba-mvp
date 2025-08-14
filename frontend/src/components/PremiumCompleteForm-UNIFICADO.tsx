import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import PackageCamera from './PackageCamera';

// 🇨🇺 FORMULARIO PREMIUM UNIFICADO - Sin Tailwind, con CSS Master

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

// Servicio de precios premium avanzado
const PremiumCurrencyService = {
  rates: {
    USD_TO_CUP: 320,
    EUR_TO_USD: 1.1
  },

  calculatePremiumPrice(
    weightLbs: number,
    isInternational = false,
    hasInsurance = false,
    hasUrgent = false,
    hasSignature = false,
    hasCustoms = false,
    declaredValue = 0
  ): PremiumPriceBreakdown {
    // Cálculo de precio base premium en libras
    let basePrice = 12.00; // Premium base para hasta 2.2 lbs

    if (weightLbs <= 2.2) basePrice = 12.00;        // Premium hasta 2.2 lbs
    else if (weightLbs <= 4.4) basePrice = 22.00;   // Premium 2.2-4.4 lbs
    else if (weightLbs <= 11) basePrice = 38.00;    // Premium 4.4-11 lbs
    else if (weightLbs <= 22) basePrice = 65.00;    // Premium 11-22 lbs
    else if (weightLbs <= 44) basePrice = 120.00;   // Premium 22-44 lbs
    else basePrice = 120.00 + ((weightLbs - 44) * 3.50); // Premium más de 44 lbs

    // Servicios premium
    const handling = basePrice * 0.12; // Manejo premium reducido
    const insurance = hasInsurance ? Math.max(declaredValue * 0.03, 5.00) : 0;
    const urgent = hasUrgent ? basePrice * 0.30 : 0; // Premium urgente +30%
    const international = isInternational ? basePrice * 0.40 : 0; // Internacional +40%
    const signature = hasSignature ? 8.00 : 0; // Firma requerida
    const customs = hasCustoms ? 15.00 : 0; // Gestión aduanal

    const total = basePrice + handling + insurance + urgent + international + signature + customs;
    const totalCUP = total * this.rates.USD_TO_CUP;

    return {
      basePrice,
      handling,
      insurance,
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
    if (weightLbs <= 2.2) return "Premium hasta 2.2 lbs";
    if (weightLbs <= 4.4) return "Premium 2.2-4.4 lbs";
    if (weightLbs <= 11) return "Premium 4.4-11 lbs";
    if (weightLbs <= 22) return "Premium 11-22 lbs";
    if (weightLbs <= 44) return "Premium 22-44 lbs";
    return `Premium más de 44 lbs`;
  }
};

// Componente de input premium unificado
const PremiumFormInput: React.FC<{
  label: string;
  field: string;
  value: string;
  onChange: (field: string, value: string) => void;
  required?: boolean;
  type?: string;
  isTextarea?: boolean;
  errors: Record<string, string>;
  icon?: string;
}> = ({ label, field, value, onChange, required = false, type = "text", isTextarea = false, errors, icon }) => {
  return (
    <div className="form-group">
      <label className="form-label">
        {icon && <span className="mr-2">{icon}</span>}
        {label} {required && <span className="text-error">*</span>}
      </label>

      {isTextarea ? (
        <textarea
          value={value}
          onChange={(e) => onChange(field, e.target.value)}
          className={`form-control ${errors[field] ? 'is-invalid' : ''}`}
          rows={4}
          required={required}
          aria-label={label}
          placeholder={`Ingrese ${label.toLowerCase()}`}
        />
      ) : (
        <input
          type={type}
          value={value}
          onChange={(e) => onChange(field, e.target.value)}
          className={`form-control ${errors[field] ? 'is-invalid' : ''}`}
          required={required}
          aria-label={label}
          placeholder={`Ingrese ${label.toLowerCase()}`}
        />
      )}

      {errors[field] && (
        <span className="error-message">{errors[field]}</span>
      )}
    </div>
  );
};

// Componente principal
const PremiumCompleteForm: React.FC = () => {
  const navigate = useNavigate();

  const [currentStep, setCurrentStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [photos, setPhotos] = useState<PackagePhoto[]>([]);
  const [showCamera, setShowCamera] = useState(false);

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
    dimensions: {
      length: '',
      width: '',
      height: ''
    },
    description: '',
    category: 'tecnologia',
    packageSize: 'mediano',
    isInternational: false,
    isUrgent: false,
    isFragile: false,
    hasInsurance: true,
    declaredValue: '200',
    currency: 'USD',
    requiresSignature: false,
    needsCustoms: false,
    specialInstructions: ''
  });

  const [priceData, setPriceData] = useState<PremiumPriceBreakdown | null>(null);

  // Steps del proceso premium
  const steps = [
    { key: 1, title: 'Datos', icon: '👤', completed: false, active: true },
    { key: 2, title: 'Paquete', icon: '📦', completed: false, active: false },
    { key: 3, title: 'Servicios', icon: '⭐', completed: false, active: false },
    { key: 4, title: 'Fotos', icon: '📸', completed: false, active: false },
    { key: 5, title: 'Precio', icon: '💰', completed: false, active: false },
    { key: 6, title: 'Confirmar', icon: '✅', completed: false, active: false }
  ];

  // Manejar cambios en el formulario
  const handleChange = useCallback((field: string, value: string | boolean) => {
    if (field.includes('.')) {
      const [parent, child] = field.split('.');
      setFormData(prev => ({
        ...prev,
        [parent]: {
          ...(prev as any)[parent],
          [child]: value
        }
      }));
    } else {
      setFormData(prev => ({ ...prev, [field]: value }));
    }

    // Limpiar error del campo
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }

    // Recalcular precio si cambián factores relevantes
    if (['weight', 'isInternational', 'hasInsurance', 'isUrgent', 'requiresSignature', 'needsCustoms', 'declaredValue'].includes(field)) {
      setTimeout(() => {
        calculatePrice();
      }, 100);
    }
  }, [errors]);

  // Calcular precio premium
  const calculatePrice = useCallback(() => {
    const weightLbs = parseFloat(formData.weight);
    if (!isNaN(weightLbs) && weightLbs > 0) {
      const price = PremiumCurrencyService.calculatePremiumPrice(
        weightLbs,
        formData.isInternational,
        formData.hasInsurance,
        formData.isUrgent,
        formData.requiresSignature,
        formData.needsCustoms,
        parseFloat(formData.declaredValue) || 0
      );
      setPriceData(price);
    }
  }, [formData]);

  // Validar formulario por paso
  const validateStep = (step: number): boolean => {
    const newErrors: Record<string, string> = {};

    switch (step) {
      case 1:
        if (!formData.senderName.trim()) newErrors.senderName = 'Nombre del remitente requerido';
        if (!formData.senderPhone.trim()) newErrors.senderPhone = 'Teléfono del remitente requerido';
        if (!formData.senderAddress.trim()) newErrors.senderAddress = 'Dirección del remitente requerida';
        if (!formData.senderEmail.trim()) newErrors.senderEmail = 'Email del remitente requerido';
        if (!formData.recipientName.trim()) newErrors.recipientName = 'Nombre del destinatario requerido';
        if (!formData.recipientPhone.trim()) newErrors.recipientPhone = 'Teléfono del destinatario requerido';
        if (!formData.recipientAddress.trim()) newErrors.recipientAddress = 'Dirección del destinatario requerida';
        if (!formData.recipientEmail.trim()) newErrors.recipientEmail = 'Email del destinatario requerido';
        break;

      case 2:
        if (!formData.weight.trim()) newErrors.weight = 'Peso requerido';
        if (!formData.description.trim()) newErrors.description = 'Descripción requerida';
        if (!formData.dimensions.length.trim()) newErrors['dimensions.length'] = 'Largo requerido';
        if (!formData.dimensions.width.trim()) newErrors['dimensions.width'] = 'Ancho requerido';
        if (!formData.dimensions.height.trim()) newErrors['dimensions.height'] = 'Alto requerido';
        break;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Avanzar al siguiente paso
  const nextStep = () => {
    if (validateStep(currentStep)) {
      if (currentStep < 6) {
        setCurrentStep(currentStep + 1);

        // Calcular precio al llegar al paso 5
        if (currentStep === 4) {
          calculatePrice();
        }
      }
    }
  };

  // Retroceder paso
  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  // Eliminar foto
  const removePhoto = (photoId: string) => {
    setPhotos(prev => prev.filter(p => p.id !== photoId));
  };

  // Confirmar envío premium
  const handlePremiumConfirm = async () => {
    setIsLoading(true);

    try {
      const payload = {
        remitente_nombre: formData.senderName,
        remitente_telefono: formData.senderPhone,
        remitente_direccion: formData.senderAddress,
        remitente_email: formData.senderEmail,
        destinatario_nombre: formData.recipientName,
        destinatario_telefono: formData.recipientPhone,
        destinatario_direccion: formData.recipientAddress,
        destinatario_email: formData.recipientEmail,
        peso: parseFloat(formData.weight),
        descripcion: formData.description,
        valor_declarado: parseFloat(formData.declaredValue),
        alto: parseFloat(formData.dimensions.height),
        ancho: parseFloat(formData.dimensions.width),
        largo: parseFloat(formData.dimensions.length),
        notas: `PREMIUM - ${formData.category} - ${formData.specialInstructions}`
      };

      const response = await api.post('/envios/', payload);

      navigate('/dashboard', {
        state: {
          mensaje: `¡Envío Premium creado exitosamente! Número de guía: ${(response.data as any).numero_guia}`,
          tipo: 'success'
        }
      });

    } catch (error: any) {
      console.error('Error al crear envío premium:', error);
      setErrors({ submit: error.response?.data?.detail || 'Error al crear el envío premium' });
    } finally {
      setIsLoading(false);
    }
  };

  // Categorías premium
  const premiumCategories = [
    { value: 'tecnologia', label: '📱 Tecnología Avanzada' },
    { value: 'documentos', label: '📄 Documentos Importantes' },
    { value: 'medicinas', label: '💊 Medicinas Especializadas' },
    { value: 'joyeria', label: '💎 Joyería y Valores' },
    { value: 'arte', label: '🎨 Arte y Antigüedades' },
    { value: 'otros', label: '📦 Otros Valiosos' }
  ];

  // Monedas disponibles
  const currencies = [
    { value: 'USD', label: '💵 USD - Dólar Americano' },
    { value: 'CUP', label: '🇨🇺 CUP - Peso Cubano' }
  ];

  return (
    <div className="page-container">
      {/* Header premium */}
      <div className="page-header">
        <div>
          <h1 className="page-title">⭐ Envío Premium</h1>
          <p className="page-subtitle">Formulario completo con todos los servicios avanzados</p>
        </div>
        <div className="page-actions">
          <button
            onClick={() => navigate('/envios/modo')}
            className="btn btn-secondary"
          >
            🔙 Cambiar Modo
          </button>
          <button
            onClick={() => navigate('/envios/simple')}
            className="btn btn-primary"
          >
            📦 Modo Simple
          </button>
        </div>
      </div>

      {/* Indicador de pasos premium */}
      <div className="card mb-4">
        <div className="card-body">
          <div className="d-flex justify-center align-center gap-2">
            {steps.map((step, index) => (
              <div key={step.key} className="d-flex align-center">
                <div className={`stat-card step-card text-center ${
                  currentStep === step.key ? 'border-warning' :
                  currentStep > step.key ? 'border-success' : 'border-secondary'
                }`}>
                  <div className="stat-icon">{step.icon}</div>
                  <div className="stat-title">{step.title}</div>
                </div>
                {index < steps.length - 1 && (
                  <div className={`step-navigation-arrow ${
                    currentStep > step.key ? 'text-success' : 'text-muted'
                  }`}>
                    →
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Alerta premium */}
      <div className="alert alert-warning mb-4">
        <span>
          <strong>⭐ Modo Premium Activo</strong><br />
          Tienes acceso a funciones avanzadas: seguros extendidos, gestión aduanal, fotos del paquete, firma requerida y más.
        </span>
      </div>

      {/* Error global */}
      {errors.submit && (
        <div className="alert alert-error">
          <span>{errors.submit}</span>
          <button
            className="close-button"
            onClick={() => setErrors({ ...errors, submit: '' })}
          >
            ✕
          </button>
        </div>
      )}

      {/* Contenido de cada paso */}
      <div className="form-container">

        {/* PASO 1: Datos de contacto */}
        {currentStep === 1 && (
          <>
            <div className="form-section">
              <h3 className="form-section-title">👤 Información del Remitente</h3>
              <div className="form-row">
                <PremiumFormInput
                  label="Nombre completo"
                  field="senderName"
                  value={formData.senderName}
                  onChange={handleChange}
                  required
                  errors={errors}
                  icon="👤"
                />
                <PremiumFormInput
                  label="Teléfono"
                  field="senderPhone"
                  value={formData.senderPhone}
                  onChange={handleChange}
                  required
                  errors={errors}
                  icon="📞"
                />
              </div>
              <div className="form-row">
                <PremiumFormInput
                  label="Email"
                  field="senderEmail"
                  value={formData.senderEmail}
                  onChange={handleChange}
                  required
                  type="email"
                  errors={errors}
                  icon="📧"
                />
              </div>
              <PremiumFormInput
                label="Dirección completa"
                field="senderAddress"
                value={formData.senderAddress}
                onChange={handleChange}
                required
                isTextarea
                errors={errors}
                icon="📍"
              />
            </div>

            <div className="form-section">
              <h3 className="form-section-title">🎯 Información del Destinatario</h3>
              <div className="form-row">
                <PremiumFormInput
                  label="Nombre completo"
                  field="recipientName"
                  value={formData.recipientName}
                  onChange={handleChange}
                  required
                  errors={errors}
                  icon="👤"
                />
                <PremiumFormInput
                  label="Teléfono"
                  field="recipientPhone"
                  value={formData.recipientPhone}
                  onChange={handleChange}
                  required
                  errors={errors}
                  icon="📞"
                />
              </div>
              <div className="form-row">
                <PremiumFormInput
                  label="Email"
                  field="recipientEmail"
                  value={formData.recipientEmail}
                  onChange={handleChange}
                  required
                  type="email"
                  errors={errors}
                  icon="📧"
                />
              </div>
              <PremiumFormInput
                label="Dirección completa"
                field="recipientAddress"
                value={formData.recipientAddress}
                onChange={handleChange}
                required
                isTextarea
                errors={errors}
                icon="📍"
              />
            </div>
          </>
        )}

        {/* PASO 2: Información del paquete */}
        {currentStep === 2 && (
          <>
            <div className="form-section">
              <h3 className="form-section-title">📦 Detalles del Paquete</h3>
              <div className="form-row">
                <PremiumFormInput
                  label="Peso (libras)"
                  field="weight"
                  value={formData.weight}
                  onChange={handleChange}
                  required
                  type="number"
                  errors={errors}
                  icon="⚖️"
                />
                <div className="form-group">
                  <label className="form-label">
                    <span className="mr-2">📦</span>
                    Categoría <span className="text-error">*</span>
                  </label>
                  <select
                    value={formData.category}
                    onChange={(e) => handleChange('category', e.target.value)}
                    className="form-control"
                    aria-label="Categoría del paquete"
                  >
                    {premiumCategories.map(cat => (
                      <option key={cat.value} value={cat.value}>
                        {cat.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <PremiumFormInput
                label="Descripción detallada del contenido"
                field="description"
                value={formData.description}
                onChange={handleChange}
                required
                isTextarea
                errors={errors}
                icon="📝"
              />

              <h4 className="form-section-subtitle">📏 Dimensiones (cm)</h4>
              <div className="form-row">
                <PremiumFormInput
                  label="Largo"
                  field="dimensions.length"
                  value={formData.dimensions.length}
                  onChange={handleChange}
                  required
                  type="number"
                  errors={errors}
                  icon="📏"
                />
                <PremiumFormInput
                  label="Ancho"
                  field="dimensions.width"
                  value={formData.dimensions.width}
                  onChange={handleChange}
                  required
                  type="number"
                  errors={errors}
                  icon="📐"
                />
                <PremiumFormInput
                  label="Alto"
                  field="dimensions.height"
                  value={formData.dimensions.height}
                  onChange={handleChange}
                  required
                  type="number"
                  errors={errors}
                  icon="📋"
                />
              </div>

              <div className="form-row">
                <PremiumFormInput
                  label="Valor declarado"
                  field="declaredValue"
                  value={formData.declaredValue}
                  onChange={handleChange}
                  type="number"
                  errors={errors}
                  icon="💰"
                />
                <div className="form-group">
                  <label className="form-label">
                    <span className="mr-2">💱</span>
                    Moneda
                  </label>
                  <select
                    value={formData.currency}
                    onChange={(e) => handleChange('currency', e.target.value)}
                    className="form-control"
                    aria-label="Moneda del valor declarado"
                  >
                    {currencies.map(curr => (
                      <option key={curr.value} value={curr.value}>
                        {curr.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          </>
        )}

        {/* PASO 3: Servicios premium */}
        {currentStep === 3 && (
          <div className="form-section">
            <h3 className="form-section-title">⭐ Servicios Premium</h3>

            <div className="form-row">
              <div className="form-group">
                <label className="d-flex align-center gap-2">
                  <input
                    type="checkbox"
                    checked={formData.isInternational}
                    onChange={(e) => handleChange('isInternational', e.target.checked)}
                  />
                  <span>🌍 Envío internacional (+40%)</span>
                </label>
              </div>
              <div className="form-group">
                <label className="d-flex align-center gap-2">
                  <input
                    type="checkbox"
                    checked={formData.isUrgent}
                    onChange={(e) => handleChange('isUrgent', e.target.checked)}
                  />
                  <span>🚀 Envío urgente (+30%)</span>
                </label>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="d-flex align-center gap-2">
                  <input
                    type="checkbox"
                    checked={formData.hasInsurance}
                    onChange={(e) => handleChange('hasInsurance', e.target.checked)}
                  />
                  <span>🛡️ Seguro extendido (3% del valor)</span>
                </label>
              </div>
              <div className="form-group">
                <label className="d-flex align-center gap-2">
                  <input
                    type="checkbox"
                    checked={formData.isFragile}
                    onChange={(e) => handleChange('isFragile', e.target.checked)}
                  />
                  <span>⚠️ Contenido frágil</span>
                </label>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="d-flex align-center gap-2">
                  <input
                    type="checkbox"
                    checked={formData.requiresSignature}
                    onChange={(e) => handleChange('requiresSignature', e.target.checked)}
                  />
                  <span>✍️ Firma requerida (+$8.00)</span>
                </label>
              </div>
              <div className="form-group">
                <label className="d-flex align-center gap-2">
                  <input
                    type="checkbox"
                    checked={formData.needsCustoms}
                    onChange={(e) => handleChange('needsCustoms', e.target.checked)}
                  />
                  <span>🏛️ Gestión aduanal (+$15.00)</span>
                </label>
              </div>
            </div>

            <PremiumFormInput
              label="Instrucciones especiales"
              field="specialInstructions"
              value={formData.specialInstructions}
              onChange={handleChange}
              isTextarea
              errors={errors}
              icon="📋"
            />
          </div>
        )}

        {/* PASO 4: Fotos del paquete */}
        {currentStep === 4 && (
          <div className="form-section">
            <h3 className="form-section-title">📸 Fotos del Paquete</h3>

            <div className="alert alert-info mb-4">
              <span>
                <strong>📷 Documentación Visual</strong><br />
                Las fotos ayudan en caso de reclamos y proporcionan evidencia del estado del paquete.
              </span>
            </div>

            <div className="d-flex gap-3 mb-4">
              <button
                onClick={() => setShowCamera(true)}
                className="btn btn-primary"
              >
                📸 Tomar Foto
              </button>
            </div>

            {/* Galería de fotos */}
            {photos.length > 0 && (
              <div className="stats-grid">
                {photos.map(photo => (
                  <div key={photo.id} className="stat-card">
                    <img
                      src={photo.preview}
                      alt={photo.description}
                      className="photo-preview"
                    />
                    <div className="stat-title">{photo.description}</div>
                    <button
                      onClick={() => removePhoto(photo.id)}
                      className="btn btn-danger btn-sm mt-2"
                    >
                      ❌ Eliminar
                    </button>
                  </div>
                ))}
              </div>
            )}

            {/* Cámara */}
            {showCamera && (
              <div className="card">
                <div className="card-header">
                  <h4 className="card-title">📸 Tomar Foto</h4>
                  <button
                    onClick={() => setShowCamera(false)}
                    className="btn btn-secondary btn-sm"
                  >
                    ❌ Cerrar
                  </button>
                </div>
                <div className="card-body">
                  <PackageCamera
                    onPhotosChange={(newPhotos) => {
                      const mappedPhotos = newPhotos.map((photo, index) => ({
                        id: `${Date.now()}-${index}`,
                        file: photo.originalFile || new File([], 'photo.jpg'),
                        preview: photo.compressedDataUrl || '',
                        type: 'package' as const,
                        description: `Foto del paquete ${photos.length + index + 1}`
                      }));
                      setPhotos(prev => [...prev, ...mappedPhotos]);
                      setShowCamera(false);
                    }}
                    maxPhotos={5}
                  />
                </div>
              </div>
            )}
          </div>
        )}

        {/* PASO 5: Cálculo de precio premium */}
        {currentStep === 5 && priceData && (
          <div className="form-section">
            <h3 className="form-section-title">💰 Cálculo Premium</h3>

            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-header">
                  <span className="stat-title">Peso</span>
                  <span className="stat-icon">⚖️</span>
                </div>
                <div className="stat-value">{formData.weight} lbs</div>
              </div>

              <div className="stat-card">
                <div className="stat-header">
                  <span className="stat-title">Categoría</span>
                  <span className="stat-icon">⭐</span>
                </div>
                <div className="stat-value text-warning">{priceData.weightRange}</div>
              </div>

              <div className="stat-card">
                <div className="stat-header">
                  <span className="stat-title">Precio Base</span>
                  <span className="stat-icon">💵</span>
                </div>
                <div className="stat-value">${priceData.basePrice.toFixed(2)}</div>
              </div>

              <div className="stat-card">
                <div className="stat-header">
                  <span className="stat-title">Total USD</span>
                  <span className="stat-icon">💰</span>
                </div>
                <div className="stat-value text-success">${priceData.total.toFixed(2)}</div>
              </div>
            </div>

            <div className="card">
              <div className="card-header">
                <h4 className="card-title">💹 Desglose Premium</h4>
              </div>
              <div className="card-body">
                <div className="d-flex justify-between mb-2">
                  <span>Precio base premium:</span>
                  <span>${priceData.basePrice.toFixed(2)}</span>
                </div>
                <div className="d-flex justify-between mb-2">
                  <span>Manejo premium (12%):</span>
                  <span>${priceData.handling.toFixed(2)}</span>
                </div>
                {priceData.insurance > 0 && (
                  <div className="d-flex justify-between mb-2">
                    <span>Seguro extendido (3%):</span>
                    <span>${priceData.insurance.toFixed(2)}</span>
                  </div>
                )}
                {priceData.urgent > 0 && (
                  <div className="d-flex justify-between mb-2 text-warning">
                    <span>Urgente premium (30%):</span>
                    <span>${priceData.urgent.toFixed(2)}</span>
                  </div>
                )}
                {priceData.international > 0 && (
                  <div className="d-flex justify-between mb-2 text-info">
                    <span>Internacional (40%):</span>
                    <span>${priceData.international.toFixed(2)}</span>
                  </div>
                )}
                {priceData.signature > 0 && (
                  <div className="d-flex justify-between mb-2">
                    <span>Firma requerida:</span>
                    <span>${priceData.signature.toFixed(2)}</span>
                  </div>
                )}
                {priceData.customs > 0 && (
                  <div className="d-flex justify-between mb-2">
                    <span>Gestión aduanal:</span>
                    <span>${priceData.customs.toFixed(2)}</span>
                  </div>
                )}
                <hr />
                <div className="d-flex justify-between font-bold">
                  <span>Total Premium USD:</span>
                  <span className="text-success">${priceData.total.toFixed(2)}</span>
                </div>
                <div className="d-flex justify-between text-muted">
                  <span>Total CUP:</span>
                  <span>${priceData.totalCUP.toLocaleString()}</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* PASO 6: Confirmación premium */}
        {currentStep === 6 && (
          <div className="form-section">
            <h3 className="form-section-title">✅ Confirmar Envío Premium</h3>

            <div className="alert alert-warning">
              <span>
                <strong>⭐ Resumen Premium</strong><br />
                Revisa todos los datos y servicios antes de confirmar. El envío premium incluye seguimiento avanzado y atención prioritaria.
              </span>
            </div>

            <div className="card">
              <div className="card-header">
                <h4 className="card-title">📦 Resumen del Envío Premium</h4>
              </div>
              <div className="card-body">
                <div className="form-row">
                  <div>
                    <strong>👤 Remitente:</strong><br />
                    {formData.senderName}<br />
                    {formData.senderPhone}<br />
                    {formData.senderEmail}<br />
                    {formData.senderAddress}
                  </div>
                  <div>
                    <strong>🎯 Destinatario:</strong><br />
                    {formData.recipientName}<br />
                    {formData.recipientPhone}<br />
                    {formData.recipientEmail}<br />
                    {formData.recipientAddress}
                  </div>
                </div>
                <hr />
                <div className="form-row">
                  <div>
                    <strong>📦 Paquete:</strong><br />
                    {formData.weight} lbs - {formData.category}<br />
                    {formData.dimensions.length} x {formData.dimensions.width} x {formData.dimensions.height} cm<br />
                    {formData.description}
                  </div>
                  <div>
                    <strong>⭐ Servicios:</strong><br />
                    ${priceData?.total.toFixed(2)} USD<br />
                    {formData.isInternational && <span className="text-info">🌍 Internacional</span>}<br />
                    {formData.isUrgent && <span className="text-warning">🚀 Urgente</span>}<br />
                    {formData.hasInsurance && <span className="text-success">🛡️ Asegurado</span>}<br />
                    {formData.requiresSignature && <span>✍️ Firma requerida</span>}
                  </div>
                </div>
                {photos.length > 0 && (
                  <>
                    <hr />
                    <div>
                      <strong>📸 Fotos adjuntas:</strong> {photos.length} imagen(es)
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Botones de navegación */}
        <div className="d-flex gap-3 justify-center">
          {currentStep > 1 && (
            <button
              onClick={prevStep}
              className="btn btn-secondary"
              disabled={isLoading}
            >
              ← Anterior
            </button>
          )}

          {currentStep < 6 ? (
            <button
              onClick={nextStep}
              className="btn btn-warning"
            >
              Siguiente →
            </button>
          ) : (
            <button
              onClick={handlePremiumConfirm}
              className="btn btn-success btn-lg"
              disabled={isLoading}
            >
              {isLoading ? '⏳ Creando Premium...' : '⭐ Confirmar Envío Premium'}
            </button>
          )}

          <button
            onClick={() => navigate('/dashboard')}
            className="btn btn-secondary"
            disabled={isLoading}
          >
            ❌ Cancelar
          </button>
        </div>
      </div>
    </div>
  );
};

export default PremiumCompleteForm;
