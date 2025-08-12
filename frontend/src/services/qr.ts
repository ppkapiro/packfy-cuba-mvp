// Servicio de generación de códigos QR y etiquetas para paquetes

export interface PackageLabel {
  packageId: string;
  qrCode: string;
  trackingNumber: string;
  recipient: {
    name: string;
    address: string;
    phone: string;
  };
  sender: {
    name: string;
    address: string;
  };
  packageInfo: {
    weight: number;
    dimensions: string;
    description: string;
    value: number;
    currency: 'USD' | 'CUP';
  };
  createdAt: string;
  estimatedDelivery: string;
}

class QRService {
  private static readonly QR_API_BASE = 'https://api.qrserver.com/v1/create-qr-code/';
  
  // Generar número de tracking único
  static generateTrackingNumber(): string {
    const prefix = 'PKF'; // Packfy
    const timestamp = Date.now().toString(36).toUpperCase();
    const random = Math.random().toString(36).substr(2, 4).toUpperCase();
    return `${prefix}${timestamp}${random}`;
  }

  // Generar código QR con información del paquete
  static generateQRCode(packageData: {
    trackingNumber: string;
    recipientName: string;
    senderName: string;
    weight: number;
  }): string {
    // Datos que irán en el QR (formato compacto para Cuba)
    const qrData = {
      t: packageData.trackingNumber,     // tracking
      r: packageData.recipientName,      // recipient
      s: packageData.senderName,         // sender
      w: packageData.weight,             // weight
      d: new Date().toISOString().split('T')[0] // date
    };

    const qrContent = JSON.stringify(qrData);
    
    // URL del QR code (usando servicio público)
    const qrUrl = `${this.QR_API_BASE}?size=200x200&data=${encodeURIComponent(qrContent)}&format=png&ecc=M`;
    
    return qrUrl;
  }

  // Crear etiqueta completa del paquete
  static createPackageLabel(packageInfo: {
    recipient: { name: string; address: string; phone: string };
    sender: { name: string; address: string };
    weight: number;
    dimensions: { length: number; width: number; height: number };
    description: string;
    value: number;
    currency: 'USD' | 'CUP';
  }): PackageLabel {
    const trackingNumber = this.generateTrackingNumber();
    const packageId = `pkg_${Date.now()}_${Math.random().toString(36).substr(2, 8)}`;
    
    const qrCode = this.generateQRCode({
      trackingNumber,
      recipientName: packageInfo.recipient.name,
      senderName: packageInfo.sender.name,
      weight: packageInfo.weight
    });

    // Estimar fecha de entrega (7-14 días típico para Cuba)
    const estimatedDelivery = new Date();
    estimatedDelivery.setDate(estimatedDelivery.getDate() + 10); // 10 días promedio

    return {
      packageId,
      qrCode,
      trackingNumber,
      recipient: packageInfo.recipient,
      sender: packageInfo.sender,
      packageInfo: {
        weight: packageInfo.weight,
        dimensions: `${packageInfo.dimensions.length}x${packageInfo.dimensions.width}x${packageInfo.dimensions.height} cm`,
        description: packageInfo.description,
        value: packageInfo.value,
        currency: packageInfo.currency
      },
      createdAt: new Date().toISOString(),
      estimatedDelivery: estimatedDelivery.toISOString()
    };
  }

  // Generar HTML para imprimir etiqueta
  static generatePrintableLabel(label: PackageLabel): string {
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Etiqueta - ${label.trackingNumber}</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: white;
          }
          .label {
            width: 10cm;
            border: 2px solid #000;
            padding: 10px;
            margin: 0 auto;
            background: white;
          }
          .header {
            text-align: center;
            border-bottom: 1px solid #000;
            padding-bottom: 10px;
            margin-bottom: 10px;
          }
          .logo {
            font-size: 24px;
            font-weight: bold;
            color: #2563eb;
          }
          .tracking {
            font-size: 18px;
            font-weight: bold;
            margin: 5px 0;
          }
          .section {
            margin: 10px 0;
            padding: 5px 0;
          }
          .section-title {
            font-weight: bold;
            text-decoration: underline;
            margin-bottom: 5px;
          }
          .qr-section {
            text-align: center;
            margin: 15px 0;
          }
          .qr-code {
            width: 120px;
            height: 120px;
            border: 1px solid #ccc;
          }
          .footer {
            border-top: 1px solid #000;
            padding-top: 10px;
            text-align: center;
            font-size: 12px;
          }
          .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            font-size: 11px;
          }
          @media print {
            body { margin: 0; padding: 10px; }
            .label { margin: 0; }
          }
        </style>
      </head>
      <body>
        <div class="label">
          <div class="header">
            <div class="logo">PACKFY CUBA</div>
            <div class="tracking">${label.trackingNumber}</div>
          </div>
          
          <div class="section">
            <div class="section-title">DESTINATARIO:</div>
            <div><strong>${label.recipient.name}</strong></div>
            <div>${label.recipient.address}</div>
            <div>Tel: ${label.recipient.phone}</div>
          </div>
          
          <div class="section">
            <div class="section-title">REMITENTE:</div>
            <div><strong>${label.sender.name}</strong></div>
            <div>${label.sender.address}</div>
          </div>
          
          <div class="qr-section">
            <img src="${label.qrCode}" alt="QR Code" class="qr-code" />
            <div style="font-size: 10px; margin-top: 5px;">
              Escanear para rastrear
            </div>
          </div>
          
          <div class="info-grid">
            <div>
              <strong>Peso:</strong><br>
              ${label.packageInfo.weight} kg
            </div>
            <div>
              <strong>Dimensiones:</strong><br>
              ${label.packageInfo.dimensions}
            </div>
            <div>
              <strong>Valor:</strong><br>
              ${label.packageInfo.value} ${label.packageInfo.currency}
            </div>
            <div>
              <strong>Entrega Est.:</strong><br>
              ${new Date(label.estimatedDelivery).toLocaleDateString('es-CU')}
            </div>
          </div>
          
          <div class="section">
            <div class="section-title">CONTENIDO:</div>
            <div style="font-size: 11px;">${label.packageInfo.description}</div>
          </div>
          
          <div class="footer">
            <div>www.packfy.cu</div>
            <div>Creado: ${new Date(label.createdAt).toLocaleDateString('es-CU')}</div>
          </div>
        </div>
        
        <script>
          // Auto-print cuando se abre
          window.onload = function() {
            setTimeout(() => window.print(), 500);
          };
        </script>
      </body>
      </html>
    `;
  }

  // Validar código QR escaneado
  static validateQRCode(qrContent: string): {
    isValid: boolean;
    data?: {
      trackingNumber: string;
      recipientName: string;
      senderName: string;
      weight: number;
      date: string;
    };
    error?: string;
  } {
    try {
      const data = JSON.parse(qrContent);
      
      if (!data.t || !data.r || !data.s) {
        return {
          isValid: false,
          error: 'Código QR incompleto o inválido'
        };
      }

      return {
        isValid: true,
        data: {
          trackingNumber: data.t,
          recipientName: data.r,
          senderName: data.s,
          weight: data.w,
          date: data.d
        }
      };
    } catch (error) {
      return {
        isValid: false,
        error: 'Formato de código QR inválido'
      };
    }
  }

  // Buscar paquete por tracking number
  static async trackPackage(trackingNumber: string): Promise<{
    found: boolean;
    package?: PackageLabel;
    status?: string;
    location?: string;
    lastUpdate?: string;
  }> {
    // Simular búsqueda en base de datos
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // En una implementación real, esto consultaría la base de datos
    return {
      found: true,
      package: {
        packageId: 'pkg_example',
        qrCode: '',
        trackingNumber,
        recipient: {
          name: 'Juan Pérez',
          address: 'Calle 23 #456, Vedado, La Habana',
          phone: '+53 5 234 5678'
        },
        sender: {
          name: 'María García',
          address: 'Miami, FL, USA'
        },
        packageInfo: {
          weight: 2.5,
          dimensions: '30x20x15 cm',
          description: 'Medicamentos y ropa',
          value: 150,
          currency: 'USD'
        },
        createdAt: new Date().toISOString(),
        estimatedDelivery: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString()
      },
      status: 'En tránsito',
      location: 'Centro de distribución - La Habana',
      lastUpdate: new Date().toISOString()
    };
  }
}

export default QRService;
