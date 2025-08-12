// Servicio de conversión de divisas y precios para Cuba

export interface CurrencyRates {
  USD_CUP: number; // Dólar a Peso Cubano
  EUR_CUP: number; // Euro a Peso Cubano  
  CAD_CUP: number; // Dólar Canadiense a Peso Cubano
  lastUpdated: string;
}

export interface PriceCalculation {
  basePrice: number;
  currency: 'USD' | 'EUR' | 'CAD' | 'CUP';
  convertedPrice: number;
  convertedCurrency: 'CUP';
  exchangeRate: number;
  fees: {
    handling: number;
    insurance: number;
    total: number;
  };
  finalPrice: number;
}

class CurrencyService {
  private static readonly OFFICIAL_RATES: CurrencyRates = {
    USD_CUP: 320.0, // Tasa aproximada actual
    EUR_CUP: 350.0,
    CAD_CUP: 240.0,
    lastUpdated: new Date().toISOString()
  };

  // Tarifas base por peso (en USD)
  private static readonly BASE_RATES = {
    '0-1kg': 8.50,
    '1-2kg': 15.00,
    '2-5kg': 28.00,
    '5-10kg': 45.00,
    '10-20kg': 85.00,
    '20kg+': 4.50 // por kg adicional
  };

  static getCurrentRates(): CurrencyRates {
    // En una implementación real, esto vendría de una API
    return this.OFFICIAL_RATES;
  }

  static getWeightCategory(weightKg: number): string {
    if (weightKg <= 1) return '0-1kg';
    if (weightKg <= 2) return '1-2kg';
    if (weightKg <= 5) return '2-5kg';
    if (weightKg <= 10) return '5-10kg';
    if (weightKg <= 20) return '10-20kg';
    return '20kg+';
  }

  static calculateBasePrice(weightKg: number): number {
    const category = this.getWeightCategory(weightKg);
    
    if (category === '20kg+') {
      const baseFor20kg = this.BASE_RATES['10-20kg'];
      const extraKg = weightKg - 20;
      return baseFor20kg + (extraKg * this.BASE_RATES['20kg+']);
    }
    
    return this.BASE_RATES[category as keyof typeof this.BASE_RATES] as number;
  }

  static calculateShippingPrice(
    weightKg: number,
    dimensions: { length: number; width: number; height: number },
    hasInsurance: boolean = false
  ): PriceCalculation {
    const basePrice = this.calculateBasePrice(weightKg);
    const rates = this.getCurrentRates();
    
    // Calcular peso volumétrico (importante para paquetes grandes y ligeros)
    const volumetricWeight = (dimensions.length * dimensions.width * dimensions.height) / 5000;
    const chargeableWeight = Math.max(weightKg, volumetricWeight);
    
    // Recalcular precio si el peso volumétrico es mayor
    const adjustedBasePrice = chargeableWeight > weightKg 
      ? this.calculateBasePrice(chargeableWeight)
      : basePrice;

    // Calcular tarifas adicionales
    const handlingFee = adjustedBasePrice * 0.15; // 15% manejo
    const insuranceFee = hasInsurance ? adjustedBasePrice * 0.05 : 0; // 5% seguro
    const totalFees = handlingFee + insuranceFee;
    
    const subtotal = adjustedBasePrice + totalFees;
    
    // Conversión a pesos cubanos
    const exchangeRate = rates.USD_CUP;
    const convertedPrice = subtotal * exchangeRate;
    
    return {
      basePrice: adjustedBasePrice,
      currency: 'USD',
      convertedPrice,
      convertedCurrency: 'CUP',
      exchangeRate,
      fees: {
        handling: handlingFee * exchangeRate,
        insurance: insuranceFee * exchangeRate,
        total: totalFees * exchangeRate
      },
      finalPrice: convertedPrice
    };
  }

  static formatCurrency(amount: number, currency: 'USD' | 'CUP' | 'EUR' | 'CAD'): string {
    const formatters = {
      USD: new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }),
      CUP: new Intl.NumberFormat('es-CU', { 
        style: 'currency', 
        currency: 'CUP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }),
      EUR: new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }),
      CAD: new Intl.NumberFormat('en-CA', { style: 'currency', currency: 'CAD' })
    };
    
    return formatters[currency].format(amount);
  }

  // Función para obtener tasas actualizadas (simular API)
  static async updateRates(): Promise<CurrencyRates> {
    // En producción, esto haría una llamada a una API de tasas de cambio
    // Por ahora simulamos con un pequeño delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Simular pequeñas variaciones en las tasas
    const variance = 0.02; // 2% de variación
    const usdRate = this.OFFICIAL_RATES.USD_CUP * (1 + (Math.random() - 0.5) * variance);
    
    return {
      USD_CUP: Math.round(usdRate * 100) / 100,
      EUR_CUP: Math.round(usdRate * 1.1 * 100) / 100,
      CAD_CUP: Math.round(usdRate * 0.75 * 100) / 100,
      lastUpdated: new Date().toISOString()
    };
  }
}

export default CurrencyService;
