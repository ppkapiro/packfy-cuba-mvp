import React, { useState } from 'react';
import { Package, Calculator, Camera, QrCode } from 'lucide-react';
import { api } from '../services/api';

// Interfaz simplificada para el modo simple/gratuito
interface SimpleFormData {
  recipientName: string;
  recipientAddress: string;
  recipientPhone: string;
  weight: string;
  description: string;
  isUrgent: boolean;
}

interface SimplePrice {
  base: number;
  handling: number;
  urgent: number;
  total: number;
  totalCUP: number;
}

// Servicio de precios simplificado
const PriceService = {
  rate: 320, // USD a CUP

  calculate(weightLbs: number, isUrgent: boolean): SimplePrice {
    // Tabla simple de precios en libras
    let base = 8.50; // Hasta 2.2 lbs (1kg)

    if (weightLbs <= 2.2) base = 8.50;
    else if (weightLbs <= 4.4) base = 15.00;
    else if (weightLbs <= 11) base = 28.00;
    else if (weightLbs <= 22) base = 45.00;
    else base = 85.00;

    const handling = base * 0.15; // 15% manejo
    const urgent = isUrgent ? base * 0.25 : 0; // 25% si es urgente
    const total = base + handling + urgent;

    return {
      base,
      handling,
      urgent,
      total,
      totalCUP: total * this.rate
    };
  }
};

const SimpleForm: React.FC = () => {
  const [step, setStep] = useState<'info' | 'price' | 'photo' | 'qr'>('info');

  const [formData, setFormData] = useState<SimpleFormData>({
    recipientName: '',
    recipientAddress: '',
    recipientPhone: '',
    weight: '',
    description: '',
    isUrgent: false
  });

  const [price, setPrice] = useState<SimplePrice | null>(null);
  const [photo, setPhoto] = useState<File | null>(null);
  const [tracking, setTracking] = useState<string>('');
  const [errors, setErrors] = useState<{[key: string]: string}>({});

  // Validación simple
  const validateForm = (): boolean => {
    const newErrors: {[key: string]: string} = {};

    if (!formData.recipientName.trim()) {
      newErrors.recipientName = 'Nombre del destinatario es requerido';
    }

    if (!formData.recipientAddress.trim()) {
      newErrors.recipientAddress = 'Dirección es requerida';
    }

    if (!formData.weight.trim()) {
      newErrors.weight = 'Peso es requerido';
    } else {
      const weight = parseFloat(formData.weight);
      if (isNaN(weight) || weight <= 0) {
        newErrors.weight = 'Peso debe ser un número válido';
      } else if (weight > 44) {
        newErrors.weight = 'Peso máximo permitido: 44 lbs';
      }
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Descripción es requerida';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Manejar envío del formulario
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    const weight = parseFloat(formData.weight);
    const calculatedPrice = PriceService.calculate(weight, formData.isUrgent);
    setPrice(calculatedPrice);
    setStep('price');
  };

  // Capturar foto
  const handleCapturePhoto = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.capture = 'environment';

    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        setPhoto(file);
      }
    };

    input.click();
  };

  // Generar QR y completar
  const handleGenerateQR = async () => {
    try {
      const trackingCode = `PKF${Date.now().toString().slice(-6)}`;
      setTracking(trackingCode);

      // Intentar guardar en backend
      const packageData = {
        remitente_nombre: 'Cliente Anónimo',
        remitente_direccion: 'Miami, FL',
        remitente_telefono: 'No especificado',
        destinatario_nombre: formData.recipientName,
        destinatario_direccion: formData.recipientAddress,
        destinatario_telefono: formData.recipientPhone || 'No especificado',
        peso: parseFloat(formData.weight),
        descripcion: formData.description,
        precio_usd: price?.total || 0,
        precio_cup: price?.totalCUP || 0,
        es_urgente: formData.isUrgent,
        numero_guia: trackingCode
      };

      await api.post('/envios/', packageData);
      console.log('✅ Paquete guardado exitosamente');
    } catch (error) {
      console.error('❌ Error guardando paquete:', error);
      // Continúa aunque falle el backend
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-50 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">

          {/* Header */}
          <div className="bg-gradient-to-r from-blue-500 to-cyan-500 p-6 text-center text-white">
            <div className="inline-flex items-center bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-bold mb-3">
              <Package className="w-4 h-4 mr-2" />
              MODO SIMPLE - GRATIS
            </div>
            <h1 className="text-2xl font-bold mb-2">
              📦 Packfy Cuba
            </h1>
            <p className="text-blue-100">
              Registro Simplificado de Paquetes
            </p>
          </div>

          {/* Indicador de pasos */}
          <div className="flex items-center justify-center py-4 bg-gray-50">
            {[
              { key: 'info', label: 'Info', active: step === 'info' },
              { key: 'price', label: 'Precio', active: step === 'price' },
              { key: 'photo', label: 'Foto', active: step === 'photo' },
              { key: 'qr', label: 'QR', active: step === 'qr' }
            ].map((s, i) => (
              <div key={s.key} className="flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                  s.active ? 'bg-blue-500 text-white' : 'bg-gray-300 text-gray-600'
                }`}>
                  {i + 1}
                </div>
                <span className={`ml-2 text-sm font-medium ${s.active ? 'text-blue-600' : 'text-gray-500'}`}>
                  {s.label}
                </span>
                {i < 3 && <div className="w-8 h-1 mx-4 bg-gray-200 rounded" />}
              </div>
            ))}
          </div>

          <div className="p-6">
            {/* PASO 1: INFORMACIÓN */}
            {step === 'info' && (
              <div>
                <h2 className="text-xl font-bold text-gray-800 mb-6 text-center">
                  📋 Información del Paquete
                </h2>

                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Destinatario en Cuba <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      value={formData.recipientName}
                      onChange={(e) => setFormData(prev => ({ ...prev, recipientName: e.target.value }))}
                      className={`w-full px-3 py-2 border rounded-lg ${
                        errors.recipientName ? 'border-red-500' : 'border-gray-300'
                      }`}
                      placeholder="Nombre completo del destinatario"
                      autoComplete="off"
                    />
                    {errors.recipientName && (
                      <p className="text-red-500 text-xs mt-1">{errors.recipientName}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Dirección en Cuba <span className="text-red-500">*</span>
                    </label>
                    <textarea
                      value={formData.recipientAddress}
                      onChange={(e) => setFormData(prev => ({ ...prev, recipientAddress: e.target.value }))}
                      className={`w-full px-3 py-2 border rounded-lg resize-none ${
                        errors.recipientAddress ? 'border-red-500' : 'border-gray-300'
                      }`}
                      placeholder="Calle, número, entre calles, municipio, provincia..."
                      rows={3}
                      autoComplete="off"
                    />
                    {errors.recipientAddress && (
                      <p className="text-red-500 text-xs mt-1">{errors.recipientAddress}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Teléfono (opcional)
                    </label>
                    <input
                      type="tel"
                      value={formData.recipientPhone}
                      onChange={(e) => setFormData(prev => ({ ...prev, recipientPhone: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      placeholder="+53 5123-4567"
                      autoComplete="off"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Peso (lbs) <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      min="0.1"
                      max="44"
                      value={formData.weight}
                      onChange={(e) => setFormData(prev => ({ ...prev, weight: e.target.value }))}
                      className={`w-full px-3 py-2 border rounded-lg ${
                        errors.weight ? 'border-red-500' : 'border-gray-300'
                      }`}
                      placeholder="5.5"
                      autoComplete="off"
                    />
                    {errors.weight && (
                      <p className="text-red-500 text-xs mt-1">{errors.weight}</p>
                    )}
                    <p className="text-xs text-gray-500 mt-1">
                      💡 Máximo permitido: 44 lbs
                    </p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Descripción <span className="text-red-500">*</span>
                    </label>
                    <textarea
                      value={formData.description}
                      onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                      className={`w-full px-3 py-2 border rounded-lg resize-none ${
                        errors.description ? 'border-red-500' : 'border-gray-300'
                      }`}
                      placeholder="Describe qué contiene el paquete..."
                      rows={2}
                      autoComplete="off"
                    />
                    {errors.description && (
                      <p className="text-red-500 text-xs mt-1">{errors.description}</p>
                    )}
                  </div>

                  <div>
                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={formData.isUrgent}
                        onChange={(e) => setFormData(prev => ({ ...prev, isUrgent: e.target.checked }))}
                        className="w-4 h-4 text-blue-600 rounded"
                      />
                      <span className="text-sm">📦 Urgente (+25%)</span>
                    </label>
                  </div>

                  <button
                    type="submit"
                    className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 text-white py-3 rounded-lg font-bold hover:from-blue-700 hover:to-cyan-700 transition-all"
                  >
                    <div className="flex items-center justify-center">
                      <Calculator className="w-5 h-5 mr-2" />
                      Calcular Precio
                    </div>
                  </button>
                </form>
              </div>
            )}

            {/* PASO 2: PRECIO */}
            {step === 'price' && price && (
              <div className="text-center">
                <h2 className="text-xl font-bold text-gray-800 mb-6">
                  💰 Precio Calculado
                </h2>

                <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
                  <div className="text-3xl font-bold text-green-600 mb-2">
                    ${price.totalCUP.toLocaleString()} CUP
                  </div>
                  <div className="text-lg text-gray-600">
                    (${price.total.toFixed(2)} USD)
                  </div>

                  <div className="mt-4 text-left space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span>Precio base:</span>
                      <span>${price.base.toFixed(2)} USD</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Manejo (15%):</span>
                      <span>${price.handling.toFixed(2)} USD</span>
                    </div>
                    {price.urgent > 0 && (
                      <div className="flex justify-between">
                        <span>Urgente (25%):</span>
                        <span>${price.urgent.toFixed(2)} USD</span>
                      </div>
                    )}
                    <hr className="my-2" />
                    <div className="flex justify-between font-bold">
                      <span>Total:</span>
                      <span>${price.total.toFixed(2)} USD</span>
                    </div>
                  </div>
                </div>

                <div className="flex gap-4">
                  <button
                    onClick={() => setStep('info')}
                    className="flex-1 bg-gray-500 text-white py-2 rounded-lg hover:bg-gray-600"
                  >
                    ← Modificar
                  </button>
                  <button
                    onClick={() => setStep('photo')}
                    className="flex-1 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
                  >
                    Continuar →
                  </button>
                </div>
              </div>
            )}

            {/* PASO 3: FOTO */}
            {step === 'photo' && (
              <div className="text-center">
                <h2 className="text-xl font-bold text-gray-800 mb-6">
                  📷 Foto del Paquete
                </h2>

                {!photo ? (
                  <div>
                    <Camera className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600 mb-4">
                      Toma una foto del paquete
                    </p>
                    <button
                      onClick={handleCapturePhoto}
                      className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 font-bold"
                    >
                      📷 Capturar Foto
                    </button>
                  </div>
                ) : (
                  <div>
                    <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                      ✅ Foto capturada: {photo.name}
                    </div>
                    <div className="flex gap-4">
                      <button
                        onClick={handleCapturePhoto}
                        className="flex-1 bg-gray-500 text-white py-2 rounded-lg hover:bg-gray-600"
                      >
                        📷 Cambiar
                      </button>
                      <button
                        onClick={() => setStep('qr')}
                        className="flex-1 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
                      >
                        Continuar →
                      </button>
                    </div>
                  </div>
                )}

                <div className="mt-4">
                  <button
                    onClick={() => setStep('price')}
                    className="text-gray-500 hover:text-gray-700"
                  >
                    ← Volver al precio
                  </button>
                </div>
              </div>
            )}

            {/* PASO 4: QR */}
            {step === 'qr' && (
              <div className="text-center">
                <h2 className="text-xl font-bold text-gray-800 mb-6">
                  🎯 Finalizar Registro
                </h2>

                {!tracking ? (
                  <div>
                    <QrCode className="w-16 h-16 text-green-500 mx-auto mb-4" />
                    <p className="text-gray-600 mb-4">
                      Genera tu código de seguimiento
                    </p>
                    <button
                      onClick={handleGenerateQR}
                      className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 font-bold"
                    >
                      🎯 Generar QR y Completar
                    </button>
                  </div>
                ) : (
                  <div>
                    <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
                      <h3 className="text-lg font-bold text-green-600 mb-2">
                        ¡Registro Completado!
                      </h3>
                      <div className="bg-white rounded p-4">
                        <p className="font-bold mb-2">Código de Seguimiento:</p>
                        <p className="text-2xl font-mono bg-gray-100 p-2 rounded">
                          {tracking}
                        </p>
                      </div>
                    </div>

                    <button
                      onClick={() => {
                        setStep('info');
                        setFormData({
                          recipientName: '',
                          recipientAddress: '',
                          recipientPhone: '',
                          weight: '',
                          description: '',
                          isUrgent: false
                        });
                        setPrice(null);
                        setPhoto(null);
                        setTracking('');
                        setErrors({});
                      }}
                      className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
                    >
                      📦 Registrar Nuevo Paquete
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SimpleForm;
