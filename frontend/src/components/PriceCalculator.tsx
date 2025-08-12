import React, { useState, useEffect } from 'react';
import { Calculator, RotateCcw, Info } from 'lucide-react';
import CurrencyService, { PriceCalculation, CurrencyRates } from '../services/currency';

interface PriceCalculatorProps {
  onPriceCalculated?: (calculation: PriceCalculation) => void;
}

const PriceCalculator: React.FC<PriceCalculatorProps> = ({ onPriceCalculated }) => {
  const [weight, setWeight] = useState<string>('');
  const [weightUnit, setWeightUnit] = useState<'kg' | 'lb'>('kg');
  const [dimensions, setDimensions] = useState({
    length: '',
    width: '',
    height: ''
  });
  const [dimensionUnit, setDimensionUnit] = useState<'cm' | 'in'>('cm');
  const [hasInsurance, setHasInsurance] = useState(false);
  const [calculation, setCalculation] = useState<PriceCalculation | null>(null);
  const [rates, setRates] = useState<CurrencyRates>(CurrencyService.getCurrentRates());
  const [isUpdatingRates, setIsUpdatingRates] = useState(false);

  const convertWeight = (value: number, unit: 'kg' | 'lb'): number => {
    return unit === 'lb' ? value * 0.453592 : value; // Convertir libras a kg
  };

  const convertDimension = (value: number, unit: 'cm' | 'in'): number => {
    return unit === 'in' ? value * 2.54 : value; // Convertir pulgadas a cm
  };

  const calculatePrice = () => {
    if (!weight || !dimensions.length || !dimensions.width || !dimensions.height) {
      return;
    }

    const weightInKg = convertWeight(parseFloat(weight), weightUnit);
    const dimensionsInCm = {
      length: convertDimension(parseFloat(dimensions.length), dimensionUnit),
      width: convertDimension(parseFloat(dimensions.width), dimensionUnit),
      height: convertDimension(parseFloat(dimensions.height), dimensionUnit)
    };

    const result = CurrencyService.calculateShippingPrice(
      weightInKg,
      dimensionsInCm,
      hasInsurance
    );

    setCalculation(result);
    onPriceCalculated?.(result);
  };

  const updateRates = async () => {
    setIsUpdatingRates(true);
    try {
      const newRates = await CurrencyService.updateRates();
      setRates(newRates);
      // Recalcular precio si ya hay un cálculo
      if (calculation) {
        calculatePrice();
      }
    } catch (error) {
      console.error('Error actualizando tasas:', error);
    } finally {
      setIsUpdatingRates(false);
    }
  };

  useEffect(() => {
    if (weight && dimensions.length && dimensions.width && dimensions.height) {
      calculatePrice();
    }
  }, [weight, weightUnit, dimensions, dimensionUnit, hasInsurance]);

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-md mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
          <Calculator className="w-5 h-5" />
          Calculadora de Precios
        </h3>
        <button
          onClick={updateRates}
          disabled={isUpdatingRates}
          className="flex items-center gap-1 px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 disabled:opacity-50"
        >
          <RotateCcw className={`w-4 h-4 ${isUpdatingRates ? 'animate-spin' : ''}`} />
          Actualizar
        </button>
      </div>

      {/* Información de tasas de cambio */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4">
        <div className="flex items-center gap-2 text-yellow-800 text-sm font-medium mb-1">
          <Info className="w-4 h-4" />
          Tasas de Cambio Actuales
        </div>
        <div className="text-xs text-yellow-700">
          <div>1 USD = {rates.USD_CUP.toLocaleString()} CUP</div>
          <div className="text-xs text-yellow-600">
            Actualizado: {new Date(rates.lastUpdated).toLocaleString('es-CU')}
          </div>
        </div>
      </div>

      {/* Peso */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Peso del Paquete
        </label>
        <div className="flex gap-2">
          <input
            type="number"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="0.0"
            step="0.1"
            min="0"
          />
          <select
            value={weightUnit}
            onChange={(e) => setWeightUnit(e.target.value as 'kg' | 'lb')}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            title="Unidad de peso"
            aria-label="Seleccionar unidad de peso"
          >
            <option value="kg">kg</option>
            <option value="lb">lb</option>
          </select>
        </div>
      </div>

      {/* Dimensiones */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Dimensiones del Paquete
        </label>
        <div className="grid grid-cols-3 gap-2 mb-2">
          <input
            type="number"
            value={dimensions.length}
            onChange={(e) => setDimensions(prev => ({ ...prev, length: e.target.value }))}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Largo"
            step="0.1"
            min="0"
          />
          <input
            type="number"
            value={dimensions.width}
            onChange={(e) => setDimensions(prev => ({ ...prev, width: e.target.value }))}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Ancho"
            step="0.1"
            min="0"
          />
          <input
            type="number"
            value={dimensions.height}
            onChange={(e) => setDimensions(prev => ({ ...prev, height: e.target.value }))}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Alto"
            step="0.1"
            min="0"
          />
        </div>
        <select
          value={dimensionUnit}
          onChange={(e) => setDimensionUnit(e.target.value as 'cm' | 'in')}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          title="Unidad de dimensiones"
          aria-label="Seleccionar unidad de dimensiones"
        >
          <option value="cm">Centímetros (cm)</option>
          <option value="in">Pulgadas (in)</option>
        </select>
      </div>

      {/* Seguro */}
      <div className="mb-6">
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={hasInsurance}
            onChange={(e) => setHasInsurance(e.target.checked)}
            className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
          />
          <span className="text-sm text-gray-700">Incluir seguro (+5%)</span>
        </label>
      </div>

      {/* Resultado del cálculo */}
      {calculation && (
        <div className="border-t pt-4">
          <h4 className="font-semibold text-gray-800 mb-3">Desglose de Precio:</h4>
          
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">Precio base:</span>
              <span>{CurrencyService.formatCurrency(calculation.basePrice, 'USD')}</span>
            </div>
            
            <div className="flex justify-between">
              <span className="text-gray-600">Manejo (15%):</span>
              <span>{CurrencyService.formatCurrency(calculation.fees.handling / rates.USD_CUP, 'USD')}</span>
            </div>
            
            {hasInsurance && (
              <div className="flex justify-between">
                <span className="text-gray-600">Seguro (5%):</span>
                <span>{CurrencyService.formatCurrency(calculation.fees.insurance / rates.USD_CUP, 'USD')}</span>
              </div>
            )}
            
            <div className="border-t pt-2 border-gray-200">
              <div className="flex justify-between font-medium">
                <span>Subtotal USD:</span>
                <span>{CurrencyService.formatCurrency(
                  calculation.basePrice + (calculation.fees.total / rates.USD_CUP), 
                  'USD'
                )}</span>
              </div>
            </div>
            
            <div className="bg-blue-50 p-3 rounded-lg mt-3">
              <div className="flex justify-between items-center">
                <span className="font-semibold text-blue-900">Total en CUP:</span>
                <span className="text-xl font-bold text-blue-900">
                  {CurrencyService.formatCurrency(calculation.finalPrice, 'CUP')}
                </span>
              </div>
              <div className="text-xs text-blue-700 mt-1">
                Tasa: 1 USD = {calculation.exchangeRate} CUP
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PriceCalculator;
