import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';

// 🇨🇺 FORMULARIO SIMPLE UNIFICADO - Sin Tailwind, con CSS Master

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

// Componente de input unificado
const FormInput: React.FC<{
  label: string;
  field: string;
  value: string;
  onChange: (field: string, value: string) => void;
  required?: boolean;
  type?: string;
  isTextarea?: boolean;
  errors: Record<string, string>;
}> = ({ label, field, value, onChange, required = false, type = "text", isTextarea = false, errors }) => {
  return (
    <div className="form-group">
      <label className="form-label">
        {label} {required && <span className="text-error">*</span>}
      </label>

      {isTextarea ? (
        <textarea
          value={value}
          onChange={(e) => onChange(field, e.target.value)}
          className={`form-control ${errors[field] ? 'is-invalid' : ''}`}
          rows={3}
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
const SimpleAdvancedForm: React.FC = () => {
  const navigate = useNavigate();

  const [currentStep, setCurrentStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const [formData, setFormData] = useState<PackageData>({
    senderName: '',
    senderPhone: '',
    senderAddress: '',
    recipientName: '',
    recipientPhone: '',
    recipientAddress: '',
    weight: '',
    description: '',
    category: 'ropa',
    packageSize: 'pequeno',
    isInternational: false,
    isUrgent: false,
    isFragile: false,
    declaredValue: '50'
  });

  const [priceData, setPriceData] = useState<PriceBreakdown | null>(null);

  // Steps del proceso
  const steps = [
    { key: 1, title: 'Datos', icon: '📝', completed: false, active: true },
    { key: 2, title: 'Calcular', icon: '💰', completed: false, active: false },
    { key: 3, title: 'Confirmar', icon: '✅', completed: false, active: false }
  ];

  // Manejar cambios en el formulario
  const handleChange = useCallback((field: string, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));

    // Limpiar error del campo al cambiar
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }

    // Recalcular precio si cambia el peso
    if (field === 'weight' && typeof value === 'string' && value) {
      const weightLbs = parseFloat(value);
      if (!isNaN(weightLbs) && weightLbs > 0) {
        const price = SimpleCurrencyService.calculatePrice(
          weightLbs,
          !!(formData.declaredValue && parseFloat(formData.declaredValue) > 100),
          formData.isUrgent
        );
        setPriceData(price);
      }
    }
  }, [errors, formData.declaredValue, formData.isUrgent]);

  // Validar formulario
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (currentStep === 1) {
      if (!formData.senderName.trim()) newErrors.senderName = 'Nombre del remitente requerido';
      if (!formData.senderPhone.trim()) newErrors.senderPhone = 'Teléfono del remitente requerido';
      if (!formData.senderAddress.trim()) newErrors.senderAddress = 'Dirección del remitente requerida';
      if (!formData.recipientName.trim()) newErrors.recipientName = 'Nombre del destinatario requerido';
      if (!formData.recipientPhone.trim()) newErrors.recipientPhone = 'Teléfono del destinatario requerido';
      if (!formData.recipientAddress.trim()) newErrors.recipientAddress = 'Dirección del destinatario requerida';
      if (!formData.weight.trim()) newErrors.weight = 'Peso requerido';
      if (!formData.description.trim()) newErrors.description = 'Descripción requerida';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Avanzar al siguiente paso
  const nextStep = () => {
    if (validateForm()) {
      if (currentStep < 3) {
        setCurrentStep(currentStep + 1);

        // Calcular precio en paso 2
        if (currentStep === 1) {
          const weightLbs = parseFloat(formData.weight);
          if (!isNaN(weightLbs) && weightLbs > 0) {
            const price = SimpleCurrencyService.calculatePrice(
              weightLbs,
              !!(formData.declaredValue && parseFloat(formData.declaredValue) > 100),
              formData.isUrgent
            );
            setPriceData(price);
          }
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

  // Confirmar envío
  const handleConfirm = async () => {
    setIsLoading(true);

    try {
      const payload = {
        remitente_nombre: formData.senderName,
        remitente_telefono: formData.senderPhone,
        remitente_direccion: formData.senderAddress,
        remitente_email: 'simple@packfy.cu',
        destinatario_nombre: formData.recipientName,
        destinatario_telefono: formData.recipientPhone,
        destinatario_direccion: formData.recipientAddress,
        destinatario_email: 'destinatario@packfy.cu',
        peso: parseFloat(formData.weight),
        descripcion: formData.description,
        valor_declarado: parseFloat(formData.declaredValue),
        alto: 20,
        ancho: 20,
        largo: 20,
        notas: `Modo Simple - ${formData.category} - ${formData.isUrgent ? 'URGENTE' : 'Normal'}`
      };

      const response = await api.post('/envios/', payload);

      navigate('/dashboard', {
        state: {
          mensaje: `¡Envío creado exitosamente! Número de guía: ${(response.data as any).numero_guia}`,
          tipo: 'success'
        }
      });

    } catch (error: any) {
      console.error('Error al crear envío:', error);
      setErrors({ submit: error.response?.data?.detail || 'Error al crear el envío' });
    } finally {
      setIsLoading(false);
    }
  };

  // Categorías disponibles
  const categories = [
    { value: 'ropa', label: '👕 Ropa' },
    { value: 'tecnologia', label: '📱 Tecnología' },
    { value: 'documentos', label: '📄 Documentos' },
    { value: 'medicinas', label: '💊 Medicinas' },
    { value: 'alimentos', label: '🍫 Alimentos' },
    { value: 'otros', label: '📦 Otros' }
  ];

  // Tamaños de paquete
  const packageSizes = [
    { value: 'pequeno', label: '📦 Pequeño' },
    { value: 'mediano', label: '📋 Mediano' },
    { value: 'grande', label: '📊 Grande' }
  ];

  return (
    <div className="page-container">
      {/* Header unificado */}
      <div className="page-header">
        <div>
          <h1 className="page-title">📦 Envío Simple</h1>
          <p className="page-subtitle">Formulario rápido y fácil para tus paquetes</p>
        </div>
        <div className="page-actions">
          <button
            onClick={() => navigate('/envios/modo')}
            className="btn btn-secondary"
          >
            🔙 Cambiar Modo
          </button>
          <button
            onClick={() => navigate('/envios/premium')}
            className="btn btn-warning"
          >
            ⭐ Actualizar a Premium
          </button>
        </div>
      </div>

      {/* Indicador de pasos */}
      <div className="card mb-4">
        <div className="card-body">
          <div className="d-flex justify-center align-center gap-4">
            {steps.map((step, index) => (
              <div key={step.key} className="d-flex align-center">
                <div className={`stat-card step-card text-center ${
                  currentStep === step.key ? 'border-primary' :
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

        {/* PASO 1: Datos del envío */}
        {currentStep === 1 && (
          <>
            <div className="form-section">
              <h3 className="form-section-title">👤 Información del Remitente</h3>
              <div className="form-row">
                <FormInput
                  label="Nombre completo"
                  field="senderName"
                  value={formData.senderName}
                  onChange={handleChange}
                  required
                  errors={errors}
                />
                <FormInput
                  label="Teléfono"
                  field="senderPhone"
                  value={formData.senderPhone}
                  onChange={handleChange}
                  required
                  errors={errors}
                />
              </div>
              <FormInput
                label="Dirección completa"
                field="senderAddress"
                value={formData.senderAddress}
                onChange={handleChange}
                required
                isTextarea
                errors={errors}
              />
            </div>

            <div className="form-section">
              <h3 className="form-section-title">🎯 Información del Destinatario</h3>
              <div className="form-row">
                <FormInput
                  label="Nombre completo"
                  field="recipientName"
                  value={formData.recipientName}
                  onChange={handleChange}
                  required
                  errors={errors}
                />
                <FormInput
                  label="Teléfono"
                  field="recipientPhone"
                  value={formData.recipientPhone}
                  onChange={handleChange}
                  required
                  errors={errors}
                />
              </div>
              <FormInput
                label="Dirección completa"
                field="recipientAddress"
                value={formData.recipientAddress}
                onChange={handleChange}
                required
                isTextarea
                errors={errors}
              />
            </div>

            <div className="form-section">
              <h3 className="form-section-title">📦 Información del Paquete</h3>
              <div className="form-row">
                <FormInput
                  label="Peso (libras)"
                  field="weight"
                  value={formData.weight}
                  onChange={handleChange}
                  required
                  type="number"
                  errors={errors}
                />
                <div className="form-group">
                  <label className="form-label">Categoría</label>
                  <select
                    value={formData.category}
                    onChange={(e) => handleChange('category', e.target.value)}
                    className="form-control"
                    aria-label="Categoría del paquete"
                  >
                    {categories.map(cat => (
                      <option key={cat.value} value={cat.value}>
                        {cat.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <FormInput
                label="Descripción del contenido"
                field="description"
                value={formData.description}
                onChange={handleChange}
                required
                isTextarea
                errors={errors}
              />

              <div className="form-row">
                <div className="form-group">
                  <label className="form-label">Tamaño del paquete</label>
                  <select
                    value={formData.packageSize}
                    onChange={(e) => handleChange('packageSize', e.target.value)}
                    className="form-control"
                    aria-label="Tamaño del paquete"
                  >
                    {packageSizes.map(size => (
                      <option key={size.value} value={size.value}>
                        {size.label}
                      </option>
                    ))}
                  </select>
                </div>
                <FormInput
                  label="Valor declarado (USD)"
                  field="declaredValue"
                  value={formData.declaredValue}
                  onChange={handleChange}
                  type="number"
                  errors={errors}
                />
              </div>

              {/* Opciones adicionales */}
              <div className="form-row">
                <div className="form-group">
                  <label className="d-flex align-center gap-2">
                    <input
                      type="checkbox"
                      checked={formData.isUrgent}
                      onChange={(e) => handleChange('isUrgent', e.target.checked)}
                    />
                    <span>🚀 Envío urgente (+25%)</span>
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
            </div>
          </>
        )}

        {/* PASO 2: Cálculo de precio */}
        {currentStep === 2 && priceData && (
          <div className="form-section">
            <h3 className="form-section-title">💰 Cálculo de Precio</h3>

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
                  <span className="stat-title">Rango</span>
                  <span className="stat-icon">📏</span>
                </div>
                <div className="stat-value text-primary">{priceData.weightRange}</div>
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
                <h4 className="card-title">💹 Desglose de Precio</h4>
              </div>
              <div className="card-body">
                <div className="d-flex justify-between mb-2">
                  <span>Precio base:</span>
                  <span>${priceData.basePrice.toFixed(2)}</span>
                </div>
                <div className="d-flex justify-between mb-2">
                  <span>Manejo (15%):</span>
                  <span>${priceData.handling.toFixed(2)}</span>
                </div>
                {priceData.insurance > 0 && (
                  <div className="d-flex justify-between mb-2">
                    <span>Seguro (5%):</span>
                    <span>${priceData.insurance.toFixed(2)}</span>
                  </div>
                )}
                {priceData.urgent > 0 && (
                  <div className="d-flex justify-between mb-2 text-warning">
                    <span>Urgente (25%):</span>
                    <span>${priceData.urgent.toFixed(2)}</span>
                  </div>
                )}
                <hr />
                <div className="d-flex justify-between font-bold">
                  <span>Total USD:</span>
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

        {/* PASO 3: Confirmación */}
        {currentStep === 3 && (
          <div className="form-section">
            <h3 className="form-section-title">✅ Confirmar Envío</h3>

            <div className="alert alert-info">
              <span>
                <strong>📋 Resumen del Envío</strong><br />
                Revisa todos los datos antes de confirmar. Una vez creado, se generará el número de guía automáticamente.
              </span>
            </div>

            <div className="card">
              <div className="card-header">
                <h4 className="card-title">📦 Datos del Envío</h4>
              </div>
              <div className="card-body">
                <div className="form-row">
                  <div>
                    <strong>👤 Remitente:</strong><br />
                    {formData.senderName}<br />
                    {formData.senderPhone}<br />
                    {formData.senderAddress}
                  </div>
                  <div>
                    <strong>🎯 Destinatario:</strong><br />
                    {formData.recipientName}<br />
                    {formData.recipientPhone}<br />
                    {formData.recipientAddress}
                  </div>
                </div>
                <hr />
                <div className="form-row">
                  <div>
                    <strong>📦 Paquete:</strong><br />
                    {formData.weight} lbs - {formData.category}<br />
                    {formData.description}
                  </div>
                  <div>
                    <strong>💰 Precio:</strong><br />
                    ${priceData?.total.toFixed(2)} USD<br />
                    {formData.isUrgent && <span className="text-warning">🚀 URGENTE</span>}
                  </div>
                </div>
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

          {currentStep < 3 ? (
            <button
              onClick={nextStep}
              className="btn btn-primary"
            >
              Siguiente →
            </button>
          ) : (
            <button
              onClick={handleConfirm}
              className="btn btn-success btn-lg"
              disabled={isLoading}
            >
              {isLoading ? '⏳ Creando...' : '✅ Confirmar Envío'}
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

export default SimpleAdvancedForm;
