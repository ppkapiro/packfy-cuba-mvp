import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm, SubmitHandler } from 'react-hook-form';
import { enviosAPI } from '../services/api';

interface EnvioFormData {
  numero_guia: string;
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
  const navigate = useNavigate();
  
  const { register, handleSubmit, formState: { errors } } = useForm<EnvioFormData>({
    defaultValues: {
      peso: 0,
      alto: 0,
      ancho: 0, 
      largo: 0,
      valor_declarado: 0
    }
  });  const onSubmit: SubmitHandler<EnvioFormData> = async (data) => {
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
      
      console.log('Datos a enviar:', formattedData);
      
      // Intentar crear el envío
      const response = await enviosAPI.create(formattedData);
      console.log('Envío creado con éxito:', response.data);
      
      // Guardar el estado de éxito en sessionStorage y localStorage para mayor persistencia
      const mensaje = 'Envío creado exitosamente';
      sessionStorage.setItem('_lastEnvioSuccess', mensaje);
      localStorage.setItem('_temp_success_message', mensaje);
      localStorage.setItem('_temp_success_timestamp', new Date().toISOString());
      
      // Sistema mejorado de redirección con múltiples capas de seguridad
      try {
        // Primero, intentar navegación con react-router (más limpia)
        console.log('Intentando navegación primaria con React Router');
        navigate('/dashboard', { 
          replace: true, 
          state: { success: mensaje } 
        });
        
        // Segunda capa: Establecer un timer para verificar si la navegación funcionó
        const navTimer = setTimeout(() => {
          console.log('Verificando si la navegación fue exitosa...');
          
          // Si todavía estamos en la página de nuevo envío, usar Window.location
          if (window.location.pathname.includes('/envios/nuevo')) {
            console.log('Parece que la navegación con React Router falló, aplicando fallback');
            // Usar window.location.assign en lugar de window.location.href para evitar problemas de caché
            window.location.assign('/dashboard?success=true&t=' + new Date().getTime());
          }
        }, 800); // Tiempo reducido para responder más rápido
        
        // Tercera capa: Botón manual que aparece después de 2 segundos (ver en el return)
        return () => {
          clearTimeout(navTimer); // Limpiar el timer si el componente se desmonta
        };
      } catch (navError) {
        console.error('Error durante la navegación:', navError);
        // Fallback inmediato si hay alguna excepción durante la navegación
        window.location.assign('/dashboard?success=true&fallback=true&t=' + new Date().getTime());
      }
    } catch (err: any) {
      console.error('Error completo:', err);
      
      // Manejo mejorado de errores
      if (err.response?.data) {
        // Si es un objeto de errores de validación de Django Rest Framework
        if (typeof err.response.data === 'object') {
          const errorMessages = Object.entries(err.response.data)
            .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
            .join('; ');
          setError(`Errores de validación: ${errorMessages}`);
        } else {
          setError(err.response.data.detail || err.response.data || 'Error al crear el envío');
        }
      } else {
        setError('Error al crear el envío: No se pudo conectar con el servidor');
      }
    } finally {
      setLoading(false);
    }
  };
    // Estado para mostrar el botón de fallback después de cierto tiempo
  const [showManualRedirect, setShowManualRedirect] = useState(false);
  
  // Mostrar el botón de redirección manual después de un tiempo
  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (loading) {
      timer = setTimeout(() => {
        setShowManualRedirect(true);
      }, 2000);
    }
    return () => clearTimeout(timer);
  }, [loading]);
  
  return (
    <div className="new-shipment-page">
      <h1>Nuevo Envío</h1>
      {error && <div className="alert alert-error">{error}</div>}
      
      {loading && (
        <div className="alert alert-info">
          <p>Procesando su solicitud...</p>
          <p>Si no es redirigido automáticamente después de crear el envío, use los botones a continuación.</p>
          
          {showManualRedirect && (
            <div className="manual-redirect-buttons">
              <p><strong>Parece que hay un problema con la redirección automática.</strong></p>
              <button 
                type="button"
                onClick={() => {
                  window.location.assign('/dashboard');
                }}
                className="btn btn-primary"
              >
                Ir al Dashboard (Opción 1)
              </button>
              
              <button 
                type="button"
                onClick={() => {
                  // Usar una ruta diferente primero y luego redirigir
                  window.location.assign('/?redirect_to=dashboard&t=' + new Date().getTime());
                }}
                className="btn btn-secondary"
              >
                Ir al Dashboard (Opción 2)
              </button>
            </div>
          )}
        </div>
      )}
      
      <form onSubmit={handleSubmit(onSubmit)} className="envio-form">
        <div className="form-section">
          <h2>Información del Paquete</h2>
          
          <div className="form-row">
            <div className="form-group">
              <label>Número de Guía</label>
              <input 
                type="text" 
                {...register('numero_guia', { required: true })}
                className={`form-control ${errors.numero_guia ? 'is-invalid' : ''}`}
              />
              {errors.numero_guia && <span className="error-message">Este campo es requerido</span>}
            </div>
            
            <div className="form-group">
              <label>Valor Declarado</label>
              <input 
                type="number" 
                step="0.01"
                {...register('valor_declarado', { required: true, min: 0 })}
                className={`form-control ${errors.valor_declarado ? 'is-invalid' : ''}`}
              />
              {errors.valor_declarado && <span className="error-message">Valor inválido</span>}
            </div>
          </div>
          
          <div className="form-group">
            <label>Descripción</label>
            <textarea 
              {...register('descripcion', { required: true })}
              className={`form-control ${errors.descripcion ? 'is-invalid' : ''}`}
              rows={3}
            ></textarea>
            {errors.descripcion && <span className="error-message">Este campo es requerido</span>}
          </div>
          
          <div className="form-row">
            <div className="form-group">
              <label>Peso (kg)</label>
              <input 
                type="number" 
                step="0.01"
                {...register('peso', { required: true, min: 0 })}
                className={`form-control ${errors.peso ? 'is-invalid' : ''}`}
              />
              {errors.peso && <span className="error-message">Valor inválido</span>}
            </div>
            
            <div className="form-group">
              <label>Alto (cm)</label>
              <input 
                type="number" 
                step="0.1"
                {...register('alto', { required: true, min: 0 })}
                className={`form-control ${errors.alto ? 'is-invalid' : ''}`}
              />
              {errors.alto && <span className="error-message">Valor inválido</span>}
            </div>
            
            <div className="form-group">
              <label>Ancho (cm)</label>
              <input 
                type="number" 
                step="0.1"
                {...register('ancho', { required: true, min: 0 })}
                className={`form-control ${errors.ancho ? 'is-invalid' : ''}`}
              />
              {errors.ancho && <span className="error-message">Valor inválido</span>}
            </div>
            
            <div className="form-group">
              <label>Largo (cm)</label>
              <input 
                type="number" 
                step="0.1"
                {...register('largo', { required: true, min: 0 })}
                className={`form-control ${errors.largo ? 'is-invalid' : ''}`}
              />
              {errors.largo && <span className="error-message">Valor inválido</span>}
            </div>
          </div>
        </div>
        
        <div className="form-section">
          <h2>Información del Remitente</h2>
          
          <div className="form-group">
            <label>Nombre</label>
            <input 
              type="text" 
              {...register('remitente_nombre', { required: true })}
              className={`form-control ${errors.remitente_nombre ? 'is-invalid' : ''}`}
            />
            {errors.remitente_nombre && <span className="error-message">Este campo es requerido</span>}
          </div>
          
          <div className="form-group">
            <label>Dirección</label>
            <textarea 
              {...register('remitente_direccion', { required: true })}
              className={`form-control ${errors.remitente_direccion ? 'is-invalid' : ''}`}
              rows={2}
            ></textarea>
            {errors.remitente_direccion && <span className="error-message">Este campo es requerido</span>}
          </div>
          
          <div className="form-row">
            <div className="form-group">
              <label>Teléfono</label>
              <input 
                type="text" 
                {...register('remitente_telefono', { required: true })}
                className={`form-control ${errors.remitente_telefono ? 'is-invalid' : ''}`}
              />
              {errors.remitente_telefono && <span className="error-message">Este campo es requerido</span>}
            </div>
            
            <div className="form-group">
              <label>Email</label>
              <input 
                type="email" 
                {...register('remitente_email')}
                className="form-control"
              />
            </div>
          </div>
        </div>
        
        <div className="form-section">
          <h2>Información del Destinatario</h2>
          
          <div className="form-group">
            <label>Nombre</label>
            <input 
              type="text" 
              {...register('destinatario_nombre', { required: true })}
              className={`form-control ${errors.destinatario_nombre ? 'is-invalid' : ''}`}
            />
            {errors.destinatario_nombre && <span className="error-message">Este campo es requerido</span>}
          </div>
          
          <div className="form-group">
            <label>Dirección</label>
            <textarea 
              {...register('destinatario_direccion', { required: true })}
              className={`form-control ${errors.destinatario_direccion ? 'is-invalid' : ''}`}
              rows={2}
            ></textarea>
            {errors.destinatario_direccion && <span className="error-message">Este campo es requerido</span>}
          </div>
          
          <div className="form-row">
            <div className="form-group">
              <label>Teléfono</label>
              <input 
                type="text" 
                {...register('destinatario_telefono', { required: true })}
                className={`form-control ${errors.destinatario_telefono ? 'is-invalid' : ''}`}
              />
              {errors.destinatario_telefono && <span className="error-message">Este campo es requerido</span>}
            </div>
            
            <div className="form-group">
              <label>Email</label>
              <input 
                type="email" 
                {...register('destinatario_email')}
                className="form-control"
              />
            </div>
          </div>
        </div>
        
        <div className="form-section">
          <h2>Información Adicional</h2>
          
          <div className="form-group">
            <label>Fecha Estimada de Entrega</label>
            <input 
              type="date" 
              {...register('fecha_entrega_estimada')}
              className="form-control"
            />
          </div>
          
          <div className="form-group">
            <label>Notas Adicionales</label>
            <textarea 
              {...register('notas')}
              className="form-control"
              rows={3}
            ></textarea>
          </div>
        </div>
        
        <div className="form-actions">
          <button 
            type="button" 
            onClick={() => navigate(-1)} 
            className="btn btn-secondary"
          >
            Cancelar
          </button>
          
          <button 
            type="submit" 
            className="btn" 
            disabled={loading}
          >
            {loading ? 'Guardando...' : 'Crear Envío'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default NewShipment;