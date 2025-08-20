import React, { useState } from 'react';
import { Package, Send, AlertCircle, CheckCircle, Loader2 } from 'lucide-react';
import { api } from '../../services/api';

interface RemitenteFormProps {
  user: any;
  tenant: any;
  perfil: any;
}

interface EnvioData {
  descripcion: string;
  peso: string;
  valor_declarado: string;
  destinatario_nombre: string;
  destinatario_direccion: string;
  destinatario_telefono: string;
  destinatario_email: string;
  notas: string;
}

const RemitenteForm: React.FC<RemitenteFormProps> = ({ user, tenant, perfil }) => {
  const [formData, setFormData] = useState<EnvioData>({
    descripcion: '',
    peso: '',
    valor_declarado: '',
    destinatario_nombre: '',
    destinatario_direccion: '',
    destinatario_telefono: '',
    destinatario_email: '',
    notas: ''
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [numeroGuia, setNumeroGuia] = useState<string>('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus('idle');

    try {
      // Preparar datos para el backend
      const envioData = {
        ...formData,
        peso: parseFloat(formData.peso),
        valor_declarado: formData.valor_declarado ? parseFloat(formData.valor_declarado) : null,
        // Los datos del remitente se toman del usuario autenticado
        remitente_nombre: `${user.first_name} ${user.last_name}`,
        remitente_direccion: perfil.direccion || 'No especificada',
        remitente_telefono: perfil.telefono || user.telefono || '',
        remitente_email: user.email
      };

      const response = await api.post('/envios/', envioData);

      if (response.data) {
        setNumeroGuia(response.data.numero_guia);
        setSubmitStatus('success');
        // Limpiar formulario
        setFormData({
          descripcion: '',
          peso: '',
          valor_declarado: '',
          destinatario_nombre: '',
          destinatario_direccion: '',
          destinatario_telefono: '',
          destinatario_email: '',
          notas: ''
        });
      }
    } catch (error) {
      console.error('Error al crear envío:', error);
      setSubmitStatus('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (submitStatus === 'success') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-center w-12 h-12 mx-auto bg-green-100 rounded-full mb-4">
            <CheckCircle className="w-6 h-6 text-green-600" />
          </div>
          <div className="text-center">
            <h2 className="text-lg font-medium text-gray-900 mb-2">
              ¡Envío Creado Exitosamente!
            </h2>
            <p className="text-sm text-gray-600 mb-4">
              Tu envío ha sido registrado con el número de guía:
            </p>
            <div className="bg-gray-100 rounded-lg p-3 mb-4">
              <p className="text-lg font-bold text-gray-900">{numeroGuia}</p>
            </div>
            <p className="text-xs text-gray-500 mb-6">
              Guarda este número para hacer seguimiento de tu envío
            </p>
            <button
              onClick={() => setSubmitStatus('idle')}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
            >
              Crear Otro Envío
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex items-center mb-4">
            <Package className="w-8 h-8 text-blue-600 mr-3" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Crear Nuevo Envío</h1>
              <p className="text-sm text-gray-600">
                {user.first_name} {user.last_name} • {tenant.nombre}
              </p>
            </div>
          </div>
        </div>

        {/* Formulario */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Información del paquete */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Información del Paquete</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Descripción del contenido *
                </label>
                <textarea
                  name="descripcion"
                  value={formData.descripcion}
                  onChange={handleInputChange}
                  required
                  rows={3}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Describe el contenido del paquete..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Peso (kg) *
                </label>
                <input
                  type="number"
                  name="peso"
                  value={formData.peso}
                  onChange={handleInputChange}
                  required
                  min="0.1"
                  step="0.1"
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="0.0"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Valor declarado (USD)
                </label>
                <input
                  type="number"
                  name="valor_declarado"
                  value={formData.valor_declarado}
                  onChange={handleInputChange}
                  min="0"
                  step="0.01"
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="0.00"
                />
              </div>
            </div>
          </div>

          {/* Información del destinatario */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Datos del Destinatario</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nombre completo *
                </label>
                <input
                  type="text"
                  name="destinatario_nombre"
                  value={formData.destinatario_nombre}
                  onChange={handleInputChange}
                  required
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Nombre del destinatario"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Teléfono *
                </label>
                <input
                  type="tel"
                  name="destinatario_telefono"
                  value={formData.destinatario_telefono}
                  onChange={handleInputChange}
                  required
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="+53 5 1234 5678"
                />
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Dirección completa *
                </label>
                <textarea
                  name="destinatario_direccion"
                  value={formData.destinatario_direccion}
                  onChange={handleInputChange}
                  required
                  rows={2}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Dirección completa en Cuba..."
                />
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email (opcional)
                </label>
                <input
                  type="email"
                  name="destinatario_email"
                  value={formData.destinatario_email}
                  onChange={handleInputChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="email@ejemplo.com"
                />
              </div>
            </div>
          </div>

          {/* Notas adicionales */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Notas Adicionales</h2>
            <textarea
              name="notas"
              value={formData.notas}
              onChange={handleInputChange}
              rows={3}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Instrucciones especiales o comentarios..."
            />
          </div>

          {/* Botón de envío */}
          <div className="bg-white rounded-lg shadow-md p-6">
            {submitStatus === 'error' && (
              <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
                <div className="flex items-center">
                  <AlertCircle className="w-4 h-4 text-red-600 mr-2" />
                  <p className="text-sm text-red-700">
                    Error al crear el envío. Por favor verifica los datos e intenta nuevamente.
                  </p>
                </div>
              </div>
            )}

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Creando envío...
                </>
              ) : (
                <>
                  <Send className="w-4 h-4 mr-2" />
                  Crear Envío
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RemitenteForm;
