import React, { useState } from 'react';
import { Package, DollarSign, Camera, QrCode, Save } from 'lucide-react';
import PriceCalculator from './PriceCalculator';
import PackageCamera from './PackageCamera';
import QRService, { PackageLabel } from '../services/qr';
import { PriceCalculation } from '../services/currency';
import { PackagePhoto } from '../services/camera';

const AdvancedPackageForm: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<'info' | 'price' | 'photos' | 'label'>('info');
  const [packageInfo, setPackageInfo] = useState({
    recipient: { name: '', address: '', phone: '' },
    sender: { name: '', address: '' },
    description: '',
    value: 0,
    currency: 'USD' as 'USD' | 'CUP'
  });
  const [priceCalculation, setPriceCalculation] = useState<PriceCalculation | null>(null);
  const [photos, setPhotos] = useState<PackagePhoto[]>([]);
  const [packageLabel, setPackageLabel] = useState<PackageLabel | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  const handleBasicInfoSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (packageInfo.recipient.name && packageInfo.recipient.address && packageInfo.sender.name) {
      setCurrentStep('price');
    }
  };

  const handlePriceCalculated = (calculation: PriceCalculation) => {
    setPriceCalculation(calculation);
  };

  const handleCreateLabel = () => {
    if (!priceCalculation) return;

    const label = QRService.createPackageLabel({
      recipient: packageInfo.recipient,
      sender: packageInfo.sender,
      weight: priceCalculation.basePrice / 8.50, // Estimado basado en precio base
      dimensions: { length: 30, width: 20, height: 15 }, // Valores por defecto
      description: packageInfo.description,
      value: packageInfo.value,
      currency: packageInfo.currency
    });

    setPackageLabel(label);
    setCurrentStep('label');
  };

  const handlePrintLabel = () => {
    if (!packageLabel) return;

    const printWindow = window.open('', '_blank');
    if (printWindow) {
      printWindow.document.write(QRService.generatePrintableLabel(packageLabel));
      printWindow.document.close();
    }
  };

  const handleSavePackage = async () => {
    setIsSaving(true);
    
    try {
      // Simular guardado en backend
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      alert('¡Paquete registrado exitosamente!');
      
      // Reset form
      setCurrentStep('info');
      setPackageInfo({
        recipient: { name: '', address: '', phone: '' },
        sender: { name: '', address: '' },
        description: '',
        value: 0,
        currency: 'USD'
      });
      setPriceCalculation(null);
      setPhotos([]);
      setPackageLabel(null);
      
    } catch (error) {
      alert('Error guardando el paquete. Inténtalo de nuevo.');
    } finally {
      setIsSaving(false);
    }
  };

  const renderStepIndicator = () => {
    const steps = [
      { key: 'info', label: 'Información', icon: Package },
      { key: 'price', label: 'Precio', icon: DollarSign },
      { key: 'photos', label: 'Fotos', icon: Camera },
      { key: 'label', label: 'Etiqueta', icon: QrCode }
    ];

    return (
      <div className="flex justify-center mb-8">
        <div className="flex items-center space-x-4">
          {steps.map((step, index) => {
            const Icon = step.icon;
            const isActive = currentStep === step.key;
            const isCompleted = steps.findIndex(s => s.key === currentStep) > index;
            
            return (
              <div key={step.key} className="flex items-center">
                <div className={`
                  flex items-center justify-center w-10 h-10 rounded-full
                  ${isActive ? 'bg-blue-600 text-white' : 
                    isCompleted ? 'bg-green-600 text-white' : 
                    'bg-gray-300 text-gray-600'}
                `}>
                  <Icon className="w-5 h-5" />
                </div>
                <span className={`ml-2 text-sm font-medium ${
                  isActive || isCompleted ? 'text-gray-900' : 'text-gray-500'
                }`}>
                  {step.label}
                </span>
                {index < steps.length - 1 && (
                  <div className={`w-8 h-px mx-4 ${
                    isCompleted ? 'bg-green-600' : 'bg-gray-300'
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
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6">
          <h1 className="text-2xl font-bold">Registro Avanzado de Paquete</h1>
          <p className="text-blue-100 mt-1">Sistema optimizado para Cuba con precios en CUP</p>
        </div>
        
        <div className="p-6">
          {renderStepIndicator()}
          
          {currentStep === 'info' && (
            <form onSubmit={handleBasicInfoSubmit} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                {/* Destinatario */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-800">Destinatario</h3>
                  <input
                    type="text"
                    placeholder="Nombre completo"
                    value={packageInfo.recipient.name}
                    onChange={(e) => setPackageInfo(prev => ({
                      ...prev,
                      recipient: { ...prev.recipient, name: e.target.value }
                    }))}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    required
                  />
                  <textarea
                    placeholder="Dirección completa en Cuba"
                    value={packageInfo.recipient.address}
                    onChange={(e) => setPackageInfo(prev => ({
                      ...prev,
                      recipient: { ...prev.recipient, address: e.target.value }
                    }))}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 h-24 resize-none"
                    required
                  />
                  <input
                    type="tel"
                    placeholder="Teléfono (+53 5 1234 5678)"
                    value={packageInfo.recipient.phone}
                    onChange={(e) => setPackageInfo(prev => ({
                      ...prev,
                      recipient: { ...prev.recipient, phone: e.target.value }
                    }))}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                {/* Remitente */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-800">Remitente</h3>
                  <input
                    type="text"
                    placeholder="Nombre completo"
                    value={packageInfo.sender.name}
                    onChange={(e) => setPackageInfo(prev => ({
                      ...prev,
                      sender: { ...prev.sender, name: e.target.value }
                    }))}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    required
                  />
                  <textarea
                    placeholder="Dirección del origen"
                    value={packageInfo.sender.address}
                    onChange={(e) => setPackageInfo(prev => ({
                      ...prev,
                      sender: { ...prev.sender, address: e.target.value }
                    }))}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 h-24 resize-none"
                    required
                  />
                </div>
              </div>

              {/* Información del paquete */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-800">Información del Paquete</h3>
                <textarea
                  placeholder="Descripción del contenido (medicamentos, ropa, etc.)"
                  value={packageInfo.description}
                  onChange={(e) => setPackageInfo(prev => ({
                    ...prev,
                    description: e.target.value
                  }))}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 h-24 resize-none"
                  required
                />
                
                <div className="grid grid-cols-2 gap-4">
                  <input
                    type="number"
                    placeholder="Valor declarado"
                    value={packageInfo.value || ''}
                    onChange={(e) => setPackageInfo(prev => ({
                      ...prev,
                      value: parseFloat(e.target.value) || 0
                    }))}
                    className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    min="0"
                    step="0.01"
                  />
                  <select
                    value={packageInfo.currency}
                    onChange={(e) => setPackageInfo(prev => ({
                      ...prev,
                      currency: e.target.value as 'USD' | 'CUP'
                    }))}
                    className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    title="Seleccionar moneda"
                    aria-label="Seleccionar moneda"
                  >
                    <option value="USD">USD (Dólares)</option>
                    <option value="CUP">CUP (Pesos Cubanos)</option>
                  </select>
                </div>
              </div>

              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                Continuar al Cálculo de Precio
              </button>
            </form>
          )}

          {currentStep === 'price' && (
            <div className="space-y-6">
              <PriceCalculator onPriceCalculated={handlePriceCalculated} />
              
              {priceCalculation && (
                <div className="flex gap-4">
                  <button
                    onClick={() => setCurrentStep('info')}
                    className="flex-1 bg-gray-500 text-white py-3 px-6 rounded-lg hover:bg-gray-600 transition-colors"
                  >
                    Volver
                  </button>
                  <button
                    onClick={() => setCurrentStep('photos')}
                    className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Continuar a Fotos
                  </button>
                </div>
              )}
            </div>
          )}

          {currentStep === 'photos' && (
            <div className="space-y-6">
              <PackageCamera onPhotosChange={setPhotos} />
              
              <div className="flex gap-4">
                <button
                  onClick={() => setCurrentStep('price')}
                  className="flex-1 bg-gray-500 text-white py-3 px-6 rounded-lg hover:bg-gray-600 transition-colors"
                >
                  Volver
                </button>
                <button
                  onClick={handleCreateLabel}
                  className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Generar Etiqueta
                </button>
              </div>
            </div>
          )}

          {currentStep === 'label' && packageLabel && (
            <div className="space-y-6">
              <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4">Etiqueta Generada</h3>
                
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <div className="bg-white p-4 rounded-lg border">
                      <div className="text-center mb-4">
                        <div className="text-2xl font-bold text-blue-600">PACKFY CUBA</div>
                        <div className="text-lg font-bold">{packageLabel.trackingNumber}</div>
                      </div>
                      
                      <div className="space-y-3 text-sm">
                        <div>
                          <div className="font-semibold">Destinatario:</div>
                          <div>{packageLabel.recipient.name}</div>
                          <div className="text-gray-600">{packageLabel.recipient.address}</div>
                        </div>
                        
                        <div>
                          <div className="font-semibold">Remitente:</div>
                          <div>{packageLabel.sender.name}</div>
                        </div>
                        
                        <div className="text-center py-4">
                          <img 
                            src={packageLabel.qrCode} 
                            alt="QR Code" 
                            className="w-24 h-24 mx-auto border"
                          />
                          <div className="text-xs text-gray-500 mt-1">Escanear para rastrear</div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="bg-white p-4 rounded-lg border">
                      <h4 className="font-semibold mb-2">Resumen del Paquete</h4>
                      <div className="space-y-2 text-sm">
                        <div>Peso: {packageLabel.packageInfo.weight} kg</div>
                        <div>Dimensiones: {packageLabel.packageInfo.dimensions}</div>
                        <div>Valor: {packageLabel.packageInfo.value} {packageLabel.packageInfo.currency}</div>
                        <div>Fotos: {photos.length} archivo(s)</div>
                        {priceCalculation && (
                          <div className="text-lg font-bold text-green-600">
                            Total: {priceCalculation.finalPrice.toLocaleString()} CUP
                          </div>
                        )}
                      </div>
                    </div>
                    
                    <div className="space-y-3">
                      <button
                        onClick={handlePrintLabel}
                        className="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition-colors"
                      >
                        🖨️ Imprimir Etiqueta
                      </button>
                      
                      <button
                        onClick={handleSavePackage}
                        disabled={isSaving}
                        className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors flex items-center justify-center gap-2"
                      >
                        <Save className="w-5 h-5" />
                        {isSaving ? 'Guardando...' : 'Guardar Paquete'}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              <button
                onClick={() => setCurrentStep('photos')}
                className="w-full bg-gray-500 text-white py-3 px-6 rounded-lg hover:bg-gray-600 transition-colors"
              >
                Volver a Fotos
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdvancedPackageForm;
