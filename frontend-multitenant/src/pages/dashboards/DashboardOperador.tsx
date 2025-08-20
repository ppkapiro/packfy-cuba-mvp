import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Package, Truck, MapPin, Clock, CheckCircle, AlertCircle } from 'lucide-react';
import { enviosAPI } from '../../services/api';
import { Empresa, PerfilUsuario } from '../../types';

interface DashboardOperadorProps {
  empresa: Empresa;
  perfil: PerfilUsuario;
}

interface EnvioOperacion {
  id: string;
  numero_guia: string;
  estado_actual: string;
  descripcion: string;
  destinatario_nombre: string;
  fecha_creacion: string;
  prioridad: 'alta' | 'media' | 'baja';
}

/**
 * 🚚 DASHBOARD PARA OPERADORES (MIAMI/CUBA)
 *
 * Funcionalidades específicas por ubicación:
 * - Operador Miami: Recogida, procesamiento, envío al aeropuerto
 * - Operador Cuba: Recepción del aeropuerto, distribución, entrega
 */

const DashboardOperador: React.FC<DashboardOperadorProps> = ({ empresa, perfil }) => {
  const [enviosPendientes, setEnviosPendientes] = useState<EnvioOperacion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const esMiami = perfil.rol === 'operador_miami';
  const esCuba = perfil.rol === 'operador_cuba';

  useEffect(() => {
    cargarEnviosPendientes();
  }, [perfil.rol]);

  const cargarEnviosPendientes = async () => {
    try {
      setLoading(true);

      // En producción, filtrar envíos según la ubicación del operador
      const response = await enviosAPI.getAll();
      const envios = Array.isArray(response.data.results) ? response.data.results : [];

      // Simular envíos pendientes para el operador
      const enviosProcesados = envios.slice(0, 5).map((envio: any, index: number) => ({
        id: envio.id || `sim-${index}`,
        numero_guia: envio.numero_guia || `PK${Date.now()}${index}`,
        estado_actual: esMiami ? 'RECIBIDO' : 'EN_TRANSITO',
        descripcion: envio.descripcion || 'Paquete sin descripción',
        destinatario_nombre: envio.destinatario_nombre || 'Destinatario',
        fecha_creacion: envio.fecha_creacion || new Date().toISOString(),
        prioridad: index % 3 === 0 ? 'alta' : index % 2 === 0 ? 'media' : 'baja'
      }));

      setEnviosPendientes(enviosProcesados);

    } catch (err: any) {
      console.error('Error cargando envíos:', err);
      setError('Error al cargar envíos pendientes');
    } finally {
      setLoading(false);
    }
  };

  const obtenerTareasSegunRol = () => {
    if (esMiami) {
      return [
        { icono: <Package size={20} />, tarea: 'Recibir paquetes de remitentes', count: 3 },
        { icono: <CheckCircle size={20} />, tarea: 'Verificar documentación', count: 2 },
        { icono: <Truck size={20} />, tarea: 'Preparar envío aeropuerto', count: 1 },
        { icono: <AlertCircle size={20} />, tarea: 'Resolver incidencias', count: 0 }
      ];
    } else {
      return [
        { icono: <MapPin size={20} />, tarea: 'Recibir del aeropuerto', count: 2 },
        { icono: <Truck size={20} />, tarea: 'Organizar reparto', count: 4 },
        { icono: <CheckCircle size={20} />, tarea: 'Realizar entregas', count: 3 },
        { icono: <Clock size={20} />, tarea: 'Confirmar recepciones', count: 1 }
      ];
    }
  };

  if (loading) {
    return (
      <div className="dashboard-operador-loading">
        <div className="loading-spinner"></div>
        <p>Cargando tareas operativas...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-operador">
      {/* Header específico por ubicación */}
      <div className="dashboard-welcome">
        <h2>
          {esMiami ? '🌴 Operaciones Miami' : '🏝️ Operaciones Cuba'}
        </h2>
        <p>
          {esMiami
            ? 'Gestiona la recogida y procesamiento de envíos en Miami'
            : 'Gestiona la recepción y entrega de envíos en Cuba'
          }
        </p>
      </div>

      {/* Tareas pendientes */}
      <div className="dashboard-tasks">
        <h3>📋 Tareas Pendientes</h3>
        <div className="tasks-grid">
          {obtenerTareasSegunRol().map((tarea, index) => (
            <div key={index} className={`task-card ${tarea.count > 0 ? 'pending' : 'completed'}`}>
              <div className="task-icon">{tarea.icono}</div>
              <div className="task-content">
                <span className="task-description">{tarea.tarea}</span>
                <span className="task-count">{tarea.count} pendientes</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Envíos para procesar */}
      <div className="dashboard-shipments">
        <h3>📦 Envíos para Procesar</h3>
        {enviosPendientes.length > 0 ? (
          <div className="shipments-list">
            {enviosPendientes.map((envio) => (
              <div key={envio.id} className="shipment-item">
                <div className="shipment-header">
                  <span className="shipment-guide">{envio.numero_guia}</span>
                  <span className={`priority-badge ${envio.prioridad}`}>
                    {envio.prioridad === 'alta' ? '🔴' : envio.prioridad === 'media' ? '🟡' : '🟢'}
                    {envio.prioridad}
                  </span>
                </div>
                <div className="shipment-content">
                  <p><strong>Destinatario:</strong> {envio.destinatario_nombre}</p>
                  <p><strong>Descripción:</strong> {envio.descripcion}</p>
                  <p><strong>Estado:</strong> {envio.estado_actual}</p>
                </div>
                <div className="shipment-actions">
                  <Link to={`/envios/${envio.id}`} className="btn-action view">
                    Ver Detalles
                  </Link>
                  <button className="btn-action process">
                    {esMiami ? 'Procesar' : 'Entregar'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-shipments">
            <p>✅ No hay envíos pendientes en este momento</p>
          </div>
        )}
      </div>

      {/* Acciones rápidas */}
      <div className="dashboard-actions">
        <h3>🚀 Acciones Rápidas</h3>
        <div className="actions-grid">
          <Link to="/envios" className="action-card">
            <Package size={20} />
            <span>Ver Todos los Envíos</span>
          </Link>

          {esMiami && (
            <Link to="/recogida" className="action-card">
              <Truck size={20} />
              <span>Programar Recogida</span>
            </Link>
          )}

          {esCuba && (
            <Link to="/entregas" className="action-card">
              <MapPin size={20} />
              <span>Gestionar Entregas</span>
            </Link>
          )}

          <Link to="/envios/nuevo" className="action-card primary">
            <Package size={20} />
            <span>Crear Nuevo Envío</span>
          </Link>
        </div>
      </div>

      {/* Información operativa */}
      <div className="dashboard-info">
        <p><strong>Ubicación:</strong> {esMiami ? 'Miami, FL' : 'La Habana, Cuba'}</p>
        <p><strong>Empresa:</strong> {empresa.name}</p>
        <p><strong>Tu rol:</strong> {esMiami ? 'Operador Miami' : 'Operador Cuba'}</p>
      </div>
    </div>
  );
};

export default DashboardOperador;
