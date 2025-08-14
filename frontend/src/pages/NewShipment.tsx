import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm, SubmitHandler } from 'react-hook-form';
import { enviosAPI } from '../services/api';

interface EnvioFormData {
  // numero_guia se genera automáticamente en el backend
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

  fecha_entrega_estimada: string;
  notas: string;
}

const NewShipment = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showManualRedirect, setShowManualRedirect] = useState(false);
  const navigate = useNavigate();

  const { register, handleSubmit, formState: { errors } } = useForm<EnvioFormData>({
    defaultValues: {
      peso: 0,
      alto: 0,
      ancho: 0,
      largo: 0,
      valor_declarado: 0
    }
  });

  const onSubmit: SubmitHandler<EnvioFormData> = async (data) => {
    setLoading(true);
    setError('');

    try {
      // Asegurarnos de que todos los campos numéricos sean números
      const formattedData = {
        ...data,
        peso: parseFloat(data.peso.toString()),
        alto: parseFloat(data.alto.toString()),
        ancho: parseFloat(data.ancho.toString()),
        largo: parseFloat(data.largo.toString()),
        valor_declarado: parseFloat(data.valor_declarado.toString())
      };

      console.log('🚀 Enviando datos del nuevo envío:', formattedData);

      const response = await enviosAPI.create(formattedData);
      console.log('✅ Envío creado exitosamente:', response.data);

      // Intentar redirigir
      const numeroGuia = (response.data as any)?.numero_guia || (response.data as any)?.id;

      if (numeroGuia) {
        console.log('🔄 Redirigiendo al dashboard...');

        // Intentar múltiples métodos de redirección
        try {
          navigate('/dashboard', {
            state: {
              mensaje: `Envío ${numeroGuia} creado exitosamente`,
              tipo: 'success'
            },
            replace: true
          });

          // Backup: redirección directa después de un delay
          setTimeout(() => {
            if (window.location.pathname === '/envios/nuevo') {
              console.log('🔄 Redirección de respaldo...');
              window.location.href = '/dashboard';
            }
          }, 1000);

        } catch (navError) {
          console.error('❌ Error en navigate:', navError);
          window.location.href = '/dashboard';
        }
      }

    } catch (err: any) {
      console.error('❌ Error al crear envío:', err);
      setError(
        err.response?.data?.detail ||
        err.response?.data?.message ||
        err.message ||
        'Error al crear el envío'
      );
    } finally {
      setLoading(false);
    }
  };

  // Mostrar botones manuales si la redirección no funciona
  useEffect(() => {
    if (!loading) return;

    const timer = setTimeout(() => {
      if (loading) {
        setShowManualRedirect(true);
      }
    }, 3000);

    return () => clearTimeout(timer);
  }, [loading]);

  return (
    <div className="page-container new-shipment-page">
      {/* Header de la página */}
      <div className="page-header">
        <div>
          <h1 className="page-title">📦 Nuevo Envío</h1>
          <p className="page-subtitle">Registra un nuevo paquete en el sistema</p>
        </div>
        <div className="page-actions">
          <button
            type="button"
            onClick={() => navigate('/dashboard')}
            className="btn btn-secondary"
          >
            🔙 Volver al Dashboard
          </button>
        </div>
      </div>

      {/* Alertas */}
      {error && (
        <div className="alert alert-error">
          <span>{error}</span>
          <button
            className="close-button"
            onClick={() => setError('')}
          >
            ✕
          </button>
        </div>
      )}

      {loading && (
        <div className="alert alert-info">
          <div>
            <p><strong>⏳ Procesando su solicitud...</strong></p>
            <p>Si no es redirigido automáticamente después de crear el envío, use los botones a continuación.</p>

            {showManualRedirect && (
              <div className="d-flex gap-2 mt-3">
                <button
                  type="button"
                  onClick={() => window.location.assign('/dashboard')}
                  className="btn btn-primary btn-sm"
                >
                  Ir al Dashboard
                </button>
                <button
                  type="button"
                  onClick={() => window.location.assign('/envios')}
                  className="btn btn-secondary btn-sm"
                >
                  Ver Envíos
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Formulario principal */}
      <form onSubmit={handleSubmit(onSubmit)} className="form-container">

        {/* Sección: Información del Paquete */}
        <div className="form-section">
          <h3 className="form-section-title">📦 Información del Paquete</h3>

          <div className="alert alert-info">
            <span><strong>💡 Importante:</strong> El número de guía se generará automáticamente una vez creado el envío.</span>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="valor_declarado">Valor Declarado (USD):</label>
              <input
                type="number"
                step="0.01"
                id="valor_declarado"
                {...register('valor_declarado', { required: true, min: 0 })}
                className={`form-control ${errors.valor_declarado ? 'is-invalid' : ''}`}
              />
              {errors.valor_declarado && <span className="error-message">Valor inválido</span>}
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="peso">Peso (kg):</label>
              <input
                type="number"
                step="0.01"
                id="peso"
                {...register('peso', { required: true, min: 0.01 })}
                className={`form-control ${errors.peso ? 'is-invalid' : ''}`}
              />
              {errors.peso && <span className="error-message">Valor inválido</span>}
            </div>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="descripcion">Descripción del contenido:</label>
            <textarea
              id="descripcion"
              {...register('descripcion', { required: true })}
              className={`form-control ${errors.descripcion ? 'is-invalid' : ''}`}
              rows={3}
            />
            {errors.descripcion && <span className="error-message">Este campo es requerido</span>}
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="alto">Alto (cm):</label>
              <input
                type="number"
                step="0.01"
                id="alto"
                {...register('alto', { required: true, min: 0.01 })}
                className={`form-control ${errors.alto ? 'is-invalid' : ''}`}
              />
              {errors.alto && <span className="error-message">Valor inválido</span>}
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="ancho">Ancho (cm):</label>
              <input
                type="number"
                step="0.01"
                id="ancho"
                {...register('ancho', { required: true, min: 0.01 })}
                className={`form-control ${errors.ancho ? 'is-invalid' : ''}`}
              />
              {errors.ancho && <span className="error-message">Valor inválido</span>}
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="largo">Largo (cm):</label>
              <input
                type="number"
                step="0.01"
                id="largo"
                {...register('largo', { required: true, min: 0.01 })}
                className={`form-control ${errors.largo ? 'is-invalid' : ''}`}
              />
              {errors.largo && <span className="error-message">Valor inválido</span>}
            </div>
          </div>
        </div>

        {/* Sección: Información del Remitente */}
        <div className="form-section">
          <h3 className="form-section-title">👤 Información del Remitente</h3>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="remitente_nombre">Nombre completo:</label>
              <input
                type="text"
                id="remitente_nombre"
                {...register('remitente_nombre', { required: true })}
                className={`form-control ${errors.remitente_nombre ? 'is-invalid' : ''}`}
              />
              {errors.remitente_nombre && <span className="error-message">Este campo es requerido</span>}
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="remitente_telefono">Teléfono:</label>
              <input
                type="tel"
                id="remitente_telefono"
                {...register('remitente_telefono', { required: true })}
                className={`form-control ${errors.remitente_telefono ? 'is-invalid' : ''}`}
              />
              {errors.remitente_telefono && <span className="error-message">Este campo es requerido</span>}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="remitente_direccion">Dirección completa:</label>
              <textarea
                id="remitente_direccion"
                {...register('remitente_direccion', { required: true })}
                className={`form-control ${errors.remitente_direccion ? 'is-invalid' : ''}`}
                rows={2}
              />
              {errors.remitente_direccion && <span className="error-message">Este campo es requerido</span>}
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="remitente_email">Email:</label>
              <input
                type="email"
                id="remitente_email"
                {...register('remitente_email', { required: true })}
                className={`form-control ${errors.remitente_email ? 'is-invalid' : ''}`}
              />
              {errors.remitente_email && <span className="error-message">Este campo es requerido</span>}
            </div>
          </div>
        </div>

        {/* Sección: Información del Destinatario */}
        <div className="form-section">
          <h3 className="form-section-title">🎯 Información del Destinatario</h3>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="destinatario_nombre">Nombre completo:</label>
              <input
                type="text"
                id="destinatario_nombre"
                {...register('destinatario_nombre', { required: true })}
                className={`form-control ${errors.destinatario_nombre ? 'is-invalid' : ''}`}
              />
              {errors.destinatario_nombre && <span className="error-message">Este campo es requerido</span>}
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="destinatario_telefono">Teléfono:</label>
              <input
                type="tel"
                id="destinatario_telefono"
                {...register('destinatario_telefono', { required: true })}
                className={`form-control ${errors.destinatario_telefono ? 'is-invalid' : ''}`}
              />
              {errors.destinatario_telefono && <span className="error-message">Este campo es requerido</span>}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="destinatario_direccion">Dirección completa:</label>
              <textarea
                id="destinatario_direccion"
                {...register('destinatario_direccion', { required: true })}
                className={`form-control ${errors.destinatario_direccion ? 'is-invalid' : ''}`}
                rows={2}
              />
              {errors.destinatario_direccion && <span className="error-message">Este campo es requerido</span>}
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="destinatario_email">Email:</label>
              <input
                type="email"
                id="destinatario_email"
                {...register('destinatario_email', { required: true })}
                className={`form-control ${errors.destinatario_email ? 'is-invalid' : ''}`}
              />
              {errors.destinatario_email && <span className="error-message">Este campo es requerido</span>}
            </div>
          </div>
        </div>

        {/* Sección: Información de Entrega */}
        <div className="form-section">
          <h3 className="form-section-title">📅 Información de Entrega</h3>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="fecha_entrega_estimada">Fecha estimada de entrega:</label>
              <input
                type="date"
                id="fecha_entrega_estimada"
                {...register('fecha_entrega_estimada')}
                className="form-control"
                min={new Date().toISOString().split('T')[0]}
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="notas">Notas adicionales:</label>
              <textarea
                id="notas"
                {...register('notas')}
                className="form-control"
                rows={2}
                placeholder="Instrucciones especiales, comentarios, etc."
              />
            </div>
          </div>
        </div>

        {/* Botones de acción */}
        <div className="d-flex gap-3 justify-center">
          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary btn-lg"
          >
            {loading ? '⏳ Creando...' : '📦 Crear Envío'}
          </button>

          <button
            type="button"
            onClick={() => navigate('/dashboard')}
            className="btn btn-secondary btn-lg"
          >
            ❌ Cancelar
          </button>
        </div>
      </form>
    </div>
  );
};

export default NewShipment;
