import React, { useState, useEffect } from 'react';
import Skeleton, { SkeletonText, SkeletonRow } from '../components/Skeleton';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '../services/api';

// 🇨🇺 EDITAR ENVÍO UNIFICADO - Sin Tailwind, con CSS Master

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

// Componente de input unificado para editar
const EditFormInput: React.FC<{
  label: string;
  field: string;
  value: string | number;
  onChange: (field: string, value: string | number) => void;
  required?: boolean;
  type?: string;
  isTextarea?: boolean;
  errors: Record<string, string>;
  icon?: string;
}> = ({ label, field, value, onChange, required = false, type = "text", isTextarea = false, errors, icon }) => {
  return (
    <div className="form-group">
      <label className="form-label">
        {icon && <span className="mr-2">{icon}</span>}
        {label} {required && <span className="text-error">*</span>}
      </label>

      {isTextarea ? (
        <textarea
          value={value}
          onChange={(e) => onChange(field, e.target.value)}
          className={`form-control ${errors[field] ? 'is-invalid' : ''}`}
          rows={3}
          required={required}
          aria-label={label}
          placeholder={`Ingrese ${label.toLowerCase()}`}
        />
      ) : (
        <input
          type={type}
          value={value}
          onChange={(e) => onChange(field, type === 'number' ? parseFloat(e.target.value) || 0 : e.target.value)}
          className={`form-control ${errors[field] ? 'is-invalid' : ''}`}
          required={required}
          aria-label={label}
          placeholder={`Ingrese ${label.toLowerCase()}`}
        />
      )}

      {errors[field] && (
        <span className="error-message">{errors[field]}</span>
      )}
    </div>
  );
};

const EditarEnvio: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [loadingData, setLoadingData] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [envio, setEnvio] = useState<any>(null);

  const [formData, setFormData] = useState<EnvioFormData>({
    descripcion: '',
    peso: 0,
    alto: 0,
    ancho: 0,
    largo: 0,
    valor_declarado: 0,
    remitente_nombre: '',
    remitente_direccion: '',
    remitente_telefono: '',
    remitente_email: '',
    destinatario_nombre: '',
    destinatario_direccion: '',
    destinatario_telefono: '',
    destinatario_email: '',
    fecha_estimada_entrega: '',
    notas: ''
  });

  // Cargar datos del envío
  const cargarEnvio = async () => {
    try {
      setLoadingData(true);
      const response = await api.get(`/envios/${id}/`);
      const envioData = response.data as any;

      setEnvio(envioData);
      setFormData({
        descripcion: envioData.descripcion || '',
        peso: envioData.peso || 0,
        alto: envioData.alto || 0,
        ancho: envioData.ancho || 0,
        largo: envioData.largo || 0,
        valor_declarado: envioData.valor_declarado || 0,
        remitente_nombre: envioData.remitente_nombre || '',
        remitente_direccion: envioData.remitente_direccion || '',
        remitente_telefono: envioData.remitente_telefono || '',
        remitente_email: envioData.remitente_email || '',
        destinatario_nombre: envioData.destinatario_nombre || '',
        destinatario_direccion: envioData.destinatario_direccion || '',
        destinatario_telefono: envioData.destinatario_telefono || '',
        destinatario_email: envioData.destinatario_email || '',
        fecha_estimada_entrega: envioData.fecha_estimada_entrega || '',
        notas: envioData.notas || ''
      });

    } catch (error: any) {
      console.error('Error al cargar envío:', error);
      setError(error.response?.data?.detail || 'Error al cargar los datos del envío');
    } finally {
      setLoadingData(false);
    }
  };

  // Cargar datos al montar
  useEffect(() => {
    if (id) {
      cargarEnvio();
    }
  }, [id]);

  // Manejar cambios en el formulario
  const handleChange = (field: string, value: string | number) => {
    setFormData(prev => ({ ...prev, [field]: value }));

    // Limpiar error del campo al cambiar
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  // Validar formulario
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.descripcion.trim()) newErrors.descripcion = 'Descripción requerida';
    if (!formData.peso || formData.peso <= 0) newErrors.peso = 'Peso válido requerido';
    if (!formData.remitente_nombre.trim()) newErrors.remitente_nombre = 'Nombre del remitente requerido';
    if (!formData.remitente_telefono.trim()) newErrors.remitente_telefono = 'Teléfono del remitente requerido';
    if (!formData.remitente_direccion.trim()) newErrors.remitente_direccion = 'Dirección del remitente requerida';
    if (!formData.destinatario_nombre.trim()) newErrors.destinatario_nombre = 'Nombre del destinatario requerido';
    if (!formData.destinatario_telefono.trim()) newErrors.destinatario_telefono = 'Teléfono del destinatario requerido';
    if (!formData.destinatario_direccion.trim()) newErrors.destinatario_direccion = 'Dirección del destinatario requerida';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Guardar cambios
  const handleSave = async () => {
    if (!validateForm()) return;

    setLoading(true);
    try {
      await api.put(`/envios/${id}/`, formData);

      navigate('/gestion', {
        state: {
          mensaje: '¡Envío actualizado exitosamente!',
          tipo: 'success'
        }
      });

    } catch (error: any) {
      console.error('Error al actualizar envío:', error);
      setErrors({ submit: error.response?.data?.detail || 'Error al actualizar el envío' });
    } finally {
      setLoading(false);
    }
  };

  // Estados de carga y error
  if (loadingData) {
    return (
      <div className="page-container">
        <div className="form-container">
          <Skeleton width={220} height={24} style={{ marginBottom: 12 }} />
          <SkeletonText lines={3} />
          <div className="mt-4">
            <SkeletonRow columns={3} />
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-container">
        <div className="alert alert-error">
          <span>
            <strong>❌ Error</strong><br />
            {error}
          </span>
          <button
            onClick={() => navigate('/gestion')}
            className="btn btn-secondary btn-sm"
          >
            🔙 Volver a Gestión
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">✏️ Editar Envío</h1>
          <p className="page-subtitle">
            Modificar información del envío #{envio?.numero_guia || id}
          </p>
        </div>
        <div className="page-actions">
          <button
            onClick={() => navigate('/gestion')}
            className="btn btn-secondary pressable hover-lift ripple"
          >
            🔙 Volver a Gestión
          </button>
        </div>
      </div>

      {/* Información del envío */}
      <div className="card mb-4">
        <div className="card-header">
          <h3 className="card-title">📦 Información del Envío</h3>
        </div>
        <div className="card-body">
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-header">
                <span className="stat-title">Número de Guía</span>
                <span className="stat-icon">📋</span>
              </div>
              <div className="stat-value">{envio?.numero_guia}</div>
            </div>

            <div className="stat-card">
              <div className="stat-header">
                <span className="stat-title">Estado</span>
                <span className="stat-icon">📊</span>
              </div>
              <div className={`stat-value ${
                envio?.estado === 'pendiente' ? 'text-warning' :
                envio?.estado === 'en_transito' ? 'text-info' :
                envio?.estado === 'entregado' ? 'text-success' : 'text-muted'
              }`}>
                {envio?.estado}
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-header">
                <span className="stat-title">Fecha Creación</span>
                <span className="stat-icon">📅</span>
              </div>
              <div className="stat-value">
                {envio?.fecha_creacion ? new Date(envio.fecha_creacion).toLocaleDateString() : 'N/A'}
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-header">
                <span className="stat-title">Precio</span>
                <span className="stat-icon">💰</span>
              </div>
              <div className="stat-value text-success">
                ${envio?.precio_total?.toFixed(2) || '0.00'}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Error global */}
      {errors.submit && (
        <div className="alert alert-error">
          <span>{errors.submit}</span>
          <button
            className="close-button"
            onClick={() => setErrors({ ...errors, submit: '' })}
          >
            ✕
          </button>
        </div>
      )}

      {/* Formulario de edición */}
      <div className="form-container">

        {/* Información del paquete */}
        <div className="form-section">
          <h3 className="form-section-title">📦 Información del Paquete</h3>
          <div className="form-row">
            <EditFormInput
              label="Peso (libras)"
              field="peso"
              value={formData.peso}
              onChange={handleChange}
              required
              type="number"
              errors={errors}
              icon="⚖️"
            />
            <EditFormInput
              label="Valor declarado (USD)"
              field="valor_declarado"
              value={formData.valor_declarado}
              onChange={handleChange}
              type="number"
              errors={errors}
              icon="💰"
            />
          </div>

          <EditFormInput
            label="Descripción del contenido"
            field="descripcion"
            value={formData.descripcion}
            onChange={handleChange}
            required
            isTextarea
            errors={errors}
            icon="📝"
          />

          <h4 className="form-section-subtitle">📏 Dimensiones (cm)</h4>
          <div className="form-row">
            <EditFormInput
              label="Largo"
              field="largo"
              value={formData.largo}
              onChange={handleChange}
              type="number"
              errors={errors}
              icon="📏"
            />
            <EditFormInput
              label="Ancho"
              field="ancho"
              value={formData.ancho}
              onChange={handleChange}
              type="number"
              errors={errors}
              icon="📐"
            />
            <EditFormInput
              label="Alto"
              field="alto"
              value={formData.alto}
              onChange={handleChange}
              type="number"
              errors={errors}
              icon="📋"
            />
          </div>
        </div>

        {/* Información del remitente */}
        <div className="form-section">
          <h3 className="form-section-title">👤 Información del Remitente</h3>
          <div className="form-row">
            <EditFormInput
              label="Nombre completo"
              field="remitente_nombre"
              value={formData.remitente_nombre}
              onChange={handleChange}
              required
              errors={errors}
              icon="👤"
            />
            <EditFormInput
              label="Teléfono"
              field="remitente_telefono"
              value={formData.remitente_telefono}
              onChange={handleChange}
              required
              errors={errors}
              icon="📞"
            />
          </div>
          <div className="form-row">
            <EditFormInput
              label="Email"
              field="remitente_email"
              value={formData.remitente_email}
              onChange={handleChange}
              type="email"
              errors={errors}
              icon="📧"
            />
          </div>
          <EditFormInput
            label="Dirección completa"
            field="remitente_direccion"
            value={formData.remitente_direccion}
            onChange={handleChange}
            required
            isTextarea
            errors={errors}
            icon="📍"
          />
        </div>

        {/* Información del destinatario */}
        <div className="form-section">
          <h3 className="form-section-title">🎯 Información del Destinatario</h3>
          <div className="form-row">
            <EditFormInput
              label="Nombre completo"
              field="destinatario_nombre"
              value={formData.destinatario_nombre}
              onChange={handleChange}
              required
              errors={errors}
              icon="👤"
            />
            <EditFormInput
              label="Teléfono"
              field="destinatario_telefono"
              value={formData.destinatario_telefono}
              onChange={handleChange}
              required
              errors={errors}
              icon="📞"
            />
          </div>
          <div className="form-row">
            <EditFormInput
              label="Email"
              field="destinatario_email"
              value={formData.destinatario_email}
              onChange={handleChange}
              type="email"
              errors={errors}
              icon="📧"
            />
          </div>
          <EditFormInput
            label="Dirección completa"
            field="destinatario_direccion"
            value={formData.destinatario_direccion}
            onChange={handleChange}
            required
            isTextarea
            errors={errors}
            icon="📍"
          />
        </div>

        {/* Información adicional */}
        <div className="form-section">
          <h3 className="form-section-title">📋 Información Adicional</h3>
          <div className="form-row">
            <EditFormInput
              label="Fecha estimada de entrega"
              field="fecha_estimada_entrega"
              value={formData.fecha_estimada_entrega}
              onChange={handleChange}
              type="date"
              errors={errors}
              icon="📅"
            />
          </div>
          <EditFormInput
            label="Notas especiales"
            field="notas"
            value={formData.notas}
            onChange={handleChange}
            isTextarea
            errors={errors}
            icon="📝"
          />
        </div>

        {/* Botones de acción */}
        <div className="d-flex gap-3 justify-center">
          <button
            onClick={handleSave}
            className="btn btn-success btn-lg"
            disabled={loading}
          >
            {loading ? '⏳ Guardando...' : '💾 Guardar Cambios'}
          </button>

          <button
            onClick={() => navigate('/gestion')}
            className="btn btn-secondary"
            disabled={loading}
          >
            ❌ Cancelar
          </button>
        </div>
      </div>
    </div>
  );
};

export default EditarEnvio;
