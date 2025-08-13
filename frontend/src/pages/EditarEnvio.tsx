import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { ArrowLeft, Save, Package, X } from 'lucide-react';
import api from '../services/api';

// 🚀 PACKFY CUBA - EDITAR ENVÍO EXISTENTE
// Componente para editar envíos desde la gestión gratuita

interface EnvioFormData {
  descripcion: string;
  peso: number;
  alto: number;
  ancho: number;
  largo: number;
  valor_declarado: number;

  remitente_nombre: string;
  remitente_direccion: string;
  remitente_telefono: string;
  remitente_email: string;

  destinatario_nombre: string;
  destinatario_direccion: string;
  destinatario_telefono: string;
  destinatario_email: string;

  fecha_estimada_entrega: string;
  notas: string;
}

const EditarEnvio: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [loadingData, setLoadingData] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [envio, setEnvio] = useState<any>(null);

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors }
  } = useForm<EnvioFormData>();

  // Cargar datos del envío al montar
  useEffect(() => {
    cargarEnvio();
  }, [id]);

  const cargarEnvio = async () => {
    if (!id) return;

    try {
      setLoadingData(true);
      setError(null);

      console.log(`🔄 Cargando envío ${id}...`);
      const response = await api.getEnvio(parseInt(id));

      if (response.error) {
        throw new Error(response.error);
      }

      const data: any = response.data;
      setEnvio(data);

      // Rellenar el formulario con los datos existentes
      setValue('descripcion', data.descripcion || '');
      setValue('peso', data.peso || 0);
      setValue('alto', data.alto || 0);
      setValue('ancho', data.ancho || 0);
      setValue('largo', data.largo || 0);
      setValue('valor_declarado', data.valor_declarado || 0);

      setValue('remitente_nombre', data.remitente_nombre || '');
      setValue('remitente_direccion', data.remitente_direccion || '');
      setValue('remitente_telefono', data.remitente_telefono || '');
      setValue('remitente_email', data.remitente_email || '');

      setValue('destinatario_nombre', data.destinatario_nombre || '');
      setValue('destinatario_direccion', data.destinatario_direccion || '');
      setValue('destinatario_telefono', data.destinatario_telefono || '');
      setValue('destinatario_email', data.destinatario_email || '');

      setValue('fecha_estimada_entrega', data.fecha_estimada_entrega || '');
      setValue('notas', data.notas || '');

      console.log('✅ Envío cargado:', data);

    } catch (err: any) {
      console.error('❌ Error al cargar envío:', err);
      setError('Error al cargar los datos del envío');
    } finally {
      setLoadingData(false);
    }
  };

  const onSubmit = async (data: EnvioFormData) => {
    if (!id) return;

    try {
      setLoading(true);
      setError(null);

      console.log('📝 Actualizando envío:', data);

      // Formatear datos numéricos
      const formattedData = {
        ...data,
        peso: parseFloat(data.peso.toString()),
        alto: parseFloat(data.alto.toString()),
        ancho: parseFloat(data.ancho.toString()),
        largo: parseFloat(data.largo.toString()),
        valor_declarado: parseFloat(data.valor_declarado.toString())
      };

      const response = await api.updateEnvio(parseInt(id), formattedData);

      if (response.error) {
        throw new Error(response.error);
      }

      console.log('✅ Envío actualizado correctamente');

      // Volver a la gestión de envíos
      navigate('/envios', {
        state: {
          success: `Envío #${envio?.numero_guia} actualizado correctamente`
        }
      });

    } catch (err: any) {
      console.error('❌ Error al actualizar envío:', err);

      if (err.response?.data) {
        if (typeof err.response.data === 'object') {
          const errorMessages = Object.entries(err.response.data)
            .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
            .join('; ');
          setError(`Errores de validación: ${errorMessages}`);
        } else {
          setError(err.response.data.detail || err.response.data || 'Error al actualizar el envío');
        }
      } else {
        setError('Error al actualizar el envío: No se pudo conectar con el servidor');
      }
    } finally {
      setLoading(false);
    }
  };

  if (loadingData) {
    return (
      <div className="flex justify-center items-center min-h-96">
        <div className="text-center">
          <Package className="w-8 h-8 animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-gray-600">Cargando datos del envío...</p>
        </div>
      </div>
    );
  }

  if (!envio) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
          <p className="font-medium">❌ Error</p>
          <p>No se pudo cargar el envío solicitado.</p>
          <button
            onClick={() => navigate('/envios')}
            className="mt-3 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Volver a Gestión
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/envios')}
              className="flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              Volver
            </button>

            <div>
              <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-3">
                <Package className="w-6 h-6 text-blue-600" />
                Editar Envío #{envio.numero_guia}
              </h1>
              <p className="text-gray-600 mt-1">
                Estado: <span className="font-medium">{envio.estado_actual}</span>
              </p>
            </div>
          </div>

          <div className="text-right text-sm text-gray-500">
            <div>Creado: {new Date(envio.fecha_creacion).toLocaleDateString()}</div>
            <div>Actualizado: {new Date(envio.ultima_actualizacion).toLocaleDateString()}</div>
          </div>
        </div>
      </div>

      {/* Mostrar errores */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
          <p className="font-medium">❌ Error</p>
          <p>{error}</p>
        </div>
      )}

      {/* Formulario de edición */}
      <form onSubmit={handleSubmit(onSubmit)} className="bg-white rounded-lg shadow-md p-6">

        {/* Información del Paquete */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Package className="w-5 h-5 text-blue-600" />
            Información del Paquete
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Descripción *
              </label>
              <textarea
                {...register('descripcion', { required: 'La descripción es requerida' })}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${errors.descripcion ? 'border-red-500' : 'border-gray-300'}`}
                rows={3}
              />
              {errors.descripcion && <span className="text-red-500 text-sm">{errors.descripcion.message}</span>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Peso (kg) *
              </label>
              <input
                type="number"
                step="0.01"
                {...register('peso', {
                  required: 'El peso es requerido',
                  min: { value: 0.01, message: 'El peso debe ser mayor a 0' }
                })}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${errors.peso ? 'border-red-500' : 'border-gray-300'}`}
              />
              {errors.peso && <span className="text-red-500 text-sm">{errors.peso.message}</span>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Valor Declarado ($)
              </label>
              <input
                type="number"
                step="0.01"
                {...register('valor_declarado', { min: 0 })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Alto (cm)
              </label>
              <input
                type="number"
                step="0.01"
                {...register('alto', { min: 0 })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Ancho (cm)
              </label>
              <input
                type="number"
                step="0.01"
                {...register('ancho', { min: 0 })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Largo (cm)
              </label>
              <input
                type="number"
                step="0.01"
                {...register('largo', { min: 0 })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Datos del Remitente */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Datos del Remitente</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nombre Completo *
              </label>
              <input
                type="text"
                {...register('remitente_nombre', { required: 'El nombre del remitente es requerido' })}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${errors.remitente_nombre ? 'border-red-500' : 'border-gray-300'}`}
              />
              {errors.remitente_nombre && <span className="text-red-500 text-sm">{errors.remitente_nombre.message}</span>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Teléfono *
              </label>
              <input
                type="text"
                {...register('remitente_telefono', { required: 'El teléfono del remitente es requerido' })}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${errors.remitente_telefono ? 'border-red-500' : 'border-gray-300'}`}
              />
              {errors.remitente_telefono && <span className="text-red-500 text-sm">{errors.remitente_telefono.message}</span>}
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Dirección *
              </label>
              <textarea
                {...register('remitente_direccion', { required: 'La dirección del remitente es requerida' })}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${errors.remitente_direccion ? 'border-red-500' : 'border-gray-300'}`}
                rows={2}
              />
              {errors.remitente_direccion && <span className="text-red-500 text-sm">{errors.remitente_direccion.message}</span>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email
              </label>
              <input
                type="email"
                {...register('remitente_email')}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Datos del Destinatario */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Datos del Destinatario</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nombre Completo *
              </label>
              <input
                type="text"
                {...register('destinatario_nombre', { required: 'El nombre del destinatario es requerido' })}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${errors.destinatario_nombre ? 'border-red-500' : 'border-gray-300'}`}
              />
              {errors.destinatario_nombre && <span className="text-red-500 text-sm">{errors.destinatario_nombre.message}</span>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Teléfono *
              </label>
              <input
                type="text"
                {...register('destinatario_telefono', { required: 'El teléfono del destinatario es requerido' })}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${errors.destinatario_telefono ? 'border-red-500' : 'border-gray-300'}`}
              />
              {errors.destinatario_telefono && <span className="text-red-500 text-sm">{errors.destinatario_telefono.message}</span>}
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Dirección *
              </label>
              <textarea
                {...register('destinatario_direccion', { required: 'La dirección del destinatario es requerida' })}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${errors.destinatario_direccion ? 'border-red-500' : 'border-gray-300'}`}
                rows={2}
              />
              {errors.destinatario_direccion && <span className="text-red-500 text-sm">{errors.destinatario_direccion.message}</span>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email
              </label>
              <input
                type="email"
                {...register('destinatario_email')}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Información Adicional */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Información Adicional</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Fecha Estimada de Entrega
              </label>
              <input
                type="date"
                {...register('fecha_estimada_entrega')}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Notas Adicionales
              </label>
              <textarea
                {...register('notas')}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                rows={3}
                placeholder="Instrucciones especiales, observaciones, etc."
              />
            </div>
          </div>
        </div>

        {/* Botones de acción */}
        <div className="flex justify-end gap-4 pt-6 border-t border-gray-200">
          <button
            type="button"
            onClick={() => navigate('/envios')}
            className="flex items-center gap-2 px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            <X className="w-4 h-4" />
            Cancelar
          </button>

          <button
            type="submit"
            disabled={loading}
            className="flex items-center gap-2 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Save className="w-4 h-4" />
            {loading ? 'Guardando...' : 'Guardar Cambios'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default EditarEnvio;
