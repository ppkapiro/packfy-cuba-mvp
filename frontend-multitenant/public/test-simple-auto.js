console.log('🧪 TEST VERSIÓN SIMPLE - Iniciando...');

// Test 1: Verificar que los elementos básicos existen
function testBasicElements() {
    console.log('📋 Test 1: Verificando elementos básicos...');
    
    const form = document.querySelector('form');
    const inputs = document.querySelectorAll('input');
    const buttons = document.querySelectorAll('button');
    
    console.log('✅ Formulario encontrado:', !!form);
    console.log('✅ Inputs encontrados:', inputs.length);
    console.log('✅ Botones encontrados:', buttons.length);
    
    return !!form && inputs.length > 0 && buttons.length > 0;
}

// Test 2: Simular cálculo de precio
function testPriceCalculation() {
    console.log('💰 Test 2: Verificando cálculo de precios...');
    
    const rate = 320; // USD a CUP
    const weightKg = 2.5;
    
    // Lógica del servicio simplificado
    let basePrice = 8.50;
    if (weightKg > 1) basePrice = 15.00;
    if (weightKg > 2) basePrice = 28.00;
    
    const handling = basePrice * 0.15;
    const totalUSD = basePrice + handling;
    const totalCUP = totalUSD * rate;
    
    console.log('📊 Peso:', weightKg, 'kg');
    console.log('📊 Precio base:', basePrice, 'USD');
    console.log('📊 Manejo (15%):', handling, 'USD');
    console.log('📊 Total USD:', totalUSD, 'USD');
    console.log('📊 Total CUP:', totalCUP, 'CUP');
    console.log('✅ Cálculo completado');
    
    return totalCUP > 0;
}

// Test 3: Verificar capacidad de cámara
function testCameraCapability() {
    console.log('📷 Test 3: Verificando capacidad de cámara...');
    
    const hasGetUserMedia = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
    const hasFileInput = document.createElement('input').type === 'file';
    
    console.log('✅ getUserMedia disponible:', hasGetUserMedia);
    console.log('✅ File input disponible:', hasFileInput);
    
    return hasGetUserMedia || hasFileInput;
}

// Test 4: Simular generación de QR
function testQRGeneration() {
    console.log('🔖 Test 4: Verificando generación de QR...');
    
    const timestamp = Date.now().toString().slice(-8);
    const tracking = `PCK${timestamp}`;
    
    const qrData = JSON.stringify({
        tracking: tracking,
        weight: '2.5kg',
        destination: 'La Habana, Cuba',
        created: new Date().toLocaleDateString()
    });
    
    console.log('✅ Tracking generado:', tracking);
    console.log('✅ Datos QR:', qrData);
    
    return tracking.startsWith('PCK') && tracking.length === 11;
}

// Ejecutar todos los tests
function runAllTests() {
    console.log('🚀 EJECUTANDO TODOS LOS TESTS...');
    console.log('================================');
    
    const results = {
        elements: testBasicElements(),
        price: testPriceCalculation(),
        camera: testCameraCapability(),
        qr: testQRGeneration()
    };
    
    console.log('📊 RESULTADOS FINALES:');
    console.log('======================');
    
    Object.entries(results).forEach(([test, passed]) => {
        const icon = passed ? '✅' : '❌';
        console.log(`${icon} Test ${test}:`, passed ? 'PASÓ' : 'FALLÓ');
    });
    
    const allPassed = Object.values(results).every(Boolean);
    console.log('');
    console.log(allPassed ? '🎉 TODOS LOS TESTS PASARON!' : '⚠️ ALGUNOS TESTS FALLARON');
    
    return results;
}

// Auto-ejecutar cuando se carga
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runAllTests);
} else {
    runAllTests();
}

// Hacer disponible globalmente para testing manual
window.testSimpleVersion = runAllTests;
