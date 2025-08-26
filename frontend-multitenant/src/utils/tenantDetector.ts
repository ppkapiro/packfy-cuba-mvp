/**
 * Detecta el tenant desde el hostname de la URL
 * Usado para configurar automáticamente el X-Tenant-Slug
 */

export function detectTenantFromHostname(): string | null {
  const hostname = window.location.hostname;

  console.log("🔍 Detectando tenant desde hostname:", hostname);

  // Mapeo de dominios a slugs de empresa
  const domainToSlugMap: Record<string, string> = {
    "cubaexpress.com": "cuba-express",
    "habanapremium.com": "habana-premium",
    "miamishipping.com": "miami-shipping",
    "packfy.com": "packfy-express",
  };

  // Desarrollo local: localhost o 127.0.0.1
  if (hostname === "localhost" || hostname === "127.0.0.1") {
    // En desarrollo, por defecto usar packfy-express
    console.log(
      "🏠 Desarrollo local detectado, usando tenant por defecto: packfy-express"
    );
    return "packfy-express";
  }

  // Desarrollo con subdominios: tenant.localhost
  if (hostname.endsWith(".localhost")) {
    const tenant = hostname.replace(".localhost", "");
    console.log("🏠 Subdominio local detectado:", tenant);
    return tenant;
  }

  // Red local con IP: 192.168.x.x
  if (hostname.match(/^192\.168\.|^10\.|^172\.(1[6-9]|2[0-9]|3[0-1])\./)) {
    // En red local, usar tenant por defecto
    console.log(
      "🌐 Red local detectada, usando tenant por defecto: packfy-express"
    );
    return "packfy-express";
  }

  // Producción: dominios específicos por empresa
  const slug = domainToSlugMap[hostname];
  if (slug) {
    console.log(`🌍 Dominio empresarial detectado: ${hostname} -> ${slug}`);
    return slug;
  }

  // Producción legacy: tenant.packfy.com
  if (hostname.endsWith(".packfy.com")) {
    const tenant = hostname.replace(".packfy.com", "");
    console.log("🌍 Subdominio Packfy detectado, tenant:", tenant);
    return tenant;
  }

  // Otros dominios: usar packfy-express por defecto
  console.log(
    "❓ Hostname no reconocido, usando tenant por defecto: packfy-express"
  );
  return "packfy-express";
}

export function initializeTenantFromHostname() {
  const tenantSlug = detectTenantFromHostname();

  if (tenantSlug) {
    console.log("🏢 Inicializando tenant desde hostname:", tenantSlug);

    // Guardar en localStorage para persistencia
    localStorage.setItem("tenant-slug", tenantSlug);

    return tenantSlug;
  }

  return null;
}
