// 🇨🇺 PACKFY CUBA - Página de Inteligencia Artificial v4.0
import React from 'react';
import AIDashboard from '../components/AIDashboard';
import Chatbot from '../components/Chatbot';

const AIPage: React.FC = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-4">
          🤖 Inteligencia Artificial
        </h1>
        <p className="text-xl text-gray-300 max-w-3xl mx-auto">
          Sistema avanzado de IA para optimización, predicciones y automatización
          del servicio de paquetería en Cuba
        </p>
      </div>

      {/* Dashboard y Chatbot */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Dashboard Principal */}
        <div className="xl:col-span-2">
          <AIDashboard />
        </div>

        {/* Chatbot Lateral */}
        <div className="xl:col-span-1">
          <Chatbot />
        </div>
      </div>

      {/* Información adicional */}
      <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-6">
        <h2 className="text-2xl font-bold text-white mb-4">
          🚀 Características del Sistema de IA
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white/5 rounded-xl p-4 border border-white/10">
            <div className="text-purple-400 text-3xl mb-2">🔮</div>
            <h3 className="font-semibold text-white mb-2">Predicciones</h3>
            <p className="text-sm text-gray-300">
              Tiempo de entrega estimado con alta precisión basado en múltiples factores
            </p>
          </div>

          <div className="bg-white/5 rounded-xl p-4 border border-white/10">
            <div className="text-blue-400 text-3xl mb-2">🗺️</div>
            <h3 className="font-semibold text-white mb-2">Optimización</h3>
            <p className="text-sm text-gray-300">
              Rutas optimizadas para maximizar eficiencia y reducir costos operativos
            </p>
          </div>

          <div className="bg-white/5 rounded-xl p-4 border border-white/10">
            <div className="text-red-400 text-3xl mb-2">⚠️</div>
            <h3 className="font-semibold text-white mb-2">Detección</h3>
            <p className="text-sm text-gray-300">
              Identificación automática de anomalías y comportamientos sospechosos
            </p>
          </div>

          <div className="bg-white/5 rounded-xl p-4 border border-white/10">
            <div className="text-green-400 text-3xl mb-2">🤖</div>
            <h3 className="font-semibold text-white mb-2">Asistente</h3>
            <p className="text-sm text-gray-300">
              Chatbot inteligente para soporte 24/7 con conocimiento especializado
            </p>
          </div>
        </div>
      </div>

      {/* Estadísticas de Rendimiento */}
      <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-6">
        <h2 className="text-2xl font-bold text-white mb-4">
          📊 Impacto del Sistema de IA
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-4xl font-bold text-green-400 mb-2">+85%</div>
            <div className="text-lg text-white mb-1">Precisión en Predicciones</div>
            <div className="text-sm text-gray-300">
              Tiempo de entrega estimado con margen de error mínimo
            </div>
          </div>

          <div className="text-center">
            <div className="text-4xl font-bold text-blue-400 mb-2">-40%</div>
            <div className="text-lg text-white mb-1">Tiempo de Rutas</div>
            <div className="text-sm text-gray-300">
              Optimización inteligente reduce tiempo de entrega
            </div>
          </div>

          <div className="text-center">
            <div className="text-4xl font-bold text-purple-400 mb-2">24/7</div>
            <div className="text-lg text-white mb-1">Soporte Automatizado</div>
            <div className="text-sm text-gray-300">
              Asistencia continua con respuestas inmediatas
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIPage;
