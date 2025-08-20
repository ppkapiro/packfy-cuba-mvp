#!/usr/bin/env python3
"""
🧹 GENERADOR DE CÓDIGO PARA ELIMINAR SERVICE WORKER
==================================================
Script que genera el código JavaScript para limpiar completamente el Service Worker.
"""


def print_banner():
    print("🧹 GENERADOR DE CÓDIGO PARA ELIMINAR SERVICE WORKER")
    print("=" * 55)
    print()


def generar_codigo_limpieza():
    """Generar código JavaScript para limpiar Service Worker"""
    print("📋 CÓDIGO JAVASCRIPT PARA PEGAR EN DEVTOOLS:")
    print("-" * 45)
    print()

    codigo_js = """
// 🧹 LIMPIEZA COMPLETA DEL SERVICE WORKER
console.log('🧹 Iniciando limpieza completa del Service Worker...');

// 1. Desregistrar todos los Service Workers
navigator.serviceWorker.getRegistrations().then(function(registrations) {
    console.log('📋 Service Workers encontrados:', registrations.length);

    for(let registration of registrations) {
        console.log('🗑️ Desregistrando SW:', registration.scope);
        registration.unregister().then(function(boolean) {
            console.log('✅ SW desregistrado:', boolean);
        });
    }

    if (registrations.length === 0) {
        console.log('✅ No hay Service Workers registrados');
    }
});

// 2. Limpiar cache del navegador
if ('caches' in window) {
    caches.keys().then(function(cacheNames) {
        console.log('📋 Caches encontrados:', cacheNames.length);

        return Promise.all(
            cacheNames.map(function(cacheName) {
                console.log('🗑️ Eliminando cache:', cacheName);
                return caches.delete(cacheName);
            })
        );
    }).then(function() {
        console.log('✅ Todos los caches eliminados');
    });
}

// 3. Limpiar localStorage y sessionStorage
try {
    localStorage.clear();
    sessionStorage.clear();
    console.log('✅ Storage local limpiado');
} catch (e) {
    console.log('⚠️ Error limpiando storage:', e);
}

// 4. Recargar la página para aplicar cambios
setTimeout(function() {
    console.log('🔄 Recargando página para aplicar cambios...');
    window.location.reload(true);
}, 2000);

console.log('🎉 Limpieza completa iniciada!');
"""

    print(codigo_js)
    print()
    print("=" * 60)
    print()


def mostrar_instrucciones():
    """Mostrar instrucciones paso a paso"""
    print("📋 INSTRUCCIONES PASO A PASO:")
    print("-" * 30)
    print()
    print("1. 🌐 **Abrir:** http://localhost:5173")
    print("2. 🔧 **Presionar F12** (Abrir DevTools)")
    print("3. 📝 **Ir a pestaña 'Console'** (Consola)")
    print("4. 📋 **Copiar y pegar** el código JavaScript de arriba")
    print("5. ⏎ **Presionar Enter** para ejecutar")
    print("6. 👀 **Esperar** que aparezcan los mensajes de limpieza")
    print("7. 🔄 **La página se recargará automáticamente**")
    print("8. ✅ **Verificar** que ya no aparezcan logs de 'sw.js'")
    print()


def generar_codigo_verificacion():
    """Generar código para verificar que se limpió correctamente"""
    print("🔍 CÓDIGO PARA VERIFICAR LIMPIEZA:")
    print("-" * 35)
    print()

    codigo_verificacion = """
// 🔍 VERIFICACIÓN DE LIMPIEZA
console.log('🔍 Verificando limpieza del Service Worker...');

navigator.serviceWorker.getRegistrations().then(function(registrations) {
    if (registrations.length === 0) {
        console.log('✅ SUCCESS: No hay Service Workers registrados');
        console.log('🎉 Limpieza completada exitosamente!');
    } else {
        console.log('⚠️ Aún hay', registrations.length, 'Service Workers registrados');
        registrations.forEach(reg => console.log('📍 SW activo:', reg.scope));
    }
});

// Verificar caches
if ('caches' in window) {
    caches.keys().then(function(cacheNames) {
        if (cacheNames.length === 0) {
            console.log('✅ SUCCESS: No hay caches almacenados');
        } else {
            console.log('⚠️ Aún hay', cacheNames.length, 'caches:', cacheNames);
        }
    });
}

console.log('🔍 Verificación completada');
"""

    print(codigo_verificacion)
    print()


def main():
    print_banner()
    generar_codigo_limpieza()
    mostrar_instrucciones()
    generar_codigo_verificacion()

    print("🎯 RESULTADO ESPERADO:")
    print("-" * 20)
    print("✅ Ya no verás logs de 'sw.js' en la consola")
    print("✅ Sistema completamente limpio y estable")
    print("✅ Multi-tenancy funcionando sin molestias")
    print("🎉 ¡Packfy Cuba 100% operativo!")

    return 0


if __name__ == "__main__":
    exit(main())
