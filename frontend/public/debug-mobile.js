// Debug script para probar funcionalidades móviles avanzadas
console.log('🔍 Iniciando debug de funcionalidades móviles...');

// Test 1: Verificar importaciones
try {
  console.log('✅ Test 1: Verificando importaciones...');
  
  // Importar servicios dinámicamente para verificar
  import('./services/currency.js').then(currencyModule => {
    console.log('✅ CurrencyService importado:', currencyModule.default);
    
    // Test conversión
    const rates = currencyModule.default.getCurrentRates();
    console.log('📊 Tasas actuales:', rates);
    
    const calculation = currencyModule.default.calculateShippingPrice(2.5, {
      length: 30,
      width: 20, 
      height: 15
    }, false);
    console.log('💰 Cálculo de prueba:', calculation);
    
  }).catch(err => {
    console.error('❌ Error importando CurrencyService:', err);
  });
  
  import('./services/camera.js').then(cameraModule => {
    console.log('✅ CameraService importado:', cameraModule.default);
    
    // Test detección de conexión
    const quality = cameraModule.default.detectConnectionQuality();
    console.log('📶 Calidad de conexión:', quality);
    
  }).catch(err => {
    console.error('❌ Error importando CameraService:', err);
  });
  
  import('./services/qr.js').then(qrModule => {
    console.log('✅ QRService importado:', qrModule.default);
    
    // Test generación de tracking
    const tracking = qrModule.default.generateTrackingNumber();
    console.log('🔖 Tracking generado:', tracking);
    
  }).catch(err => {
    console.error('❌ Error importando QRService:', err);
  });
  
} catch (error) {
  console.error('❌ Error en test de importaciones:', error);
}

// Test 2: Verificar permisos de cámara
console.log('📷 Test 2: Verificando permisos de cámara...');
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
  console.log('✅ MediaDevices API disponible');
  
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      console.log('✅ Permisos de cámara obtenidos');
      stream.getTracks().forEach(track => track.stop());
    })
    .catch(err => {
      console.error('❌ Error accediendo a cámara:', err);
    });
} else {
  console.error('❌ MediaDevices API no disponible');
}

// Test 3: Verificar localStorage
console.log('💾 Test 3: Verificando localStorage...');
try {
  localStorage.setItem('test', 'value');
  localStorage.removeItem('test');
  console.log('✅ localStorage funcionando');
} catch (error) {
  console.error('❌ Error con localStorage:', error);
}

// Test 4: Verificar compatibilidad móvil
console.log('📱 Test 4: Verificando compatibilidad móvil...');
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
console.log('📱 Es dispositivo móvil:', isMobile);
console.log('🌐 User Agent:', navigator.userAgent);
console.log('📺 Pantalla:', window.screen.width + 'x' + window.screen.height);

// Test 5: Verificar red
console.log('🌐 Test 5: Verificando conexión de red...');
if ('connection' in navigator) {
  const conn = navigator.connection;
  console.log('📶 Tipo de conexión:', conn.effectiveType);
  console.log('📊 Velocidad estimada:', conn.downlink + ' Mbps');
} else {
  console.log('⚠️ Network Information API no disponible');
}

console.log('🎉 Debug completado. Revisa la consola para detalles.');
