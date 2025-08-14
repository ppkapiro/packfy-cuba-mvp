// 🇨🇺 PACKFY CUBA - Dashboard de Inteligencia Artificial v4.0
import React, { useState, useEffect } from 'react';
import {
  Brain,
  TrendingUp,
  Route,
  AlertTriangle,
  Clock,
  MapPin,
  Package,
  Activity,
  BarChart3,
  Zap,
  Target,
  RefreshCw
} from 'lucide-react';

interface PredictionData {
  estimated_hours: number;
  estimated_days: number;
  confidence: number;
  factors: {
    distance?: string;
    weight: number;
    priority: string;
    season?: string;
  };
}

interface DemandPrediction {
  location: string;
  predictions: Array<{
    date: string;
    predicted_shipments: number;
    confidence: number;
  }>;
  trend: string;
  average_daily_demand: number;
  total_predicted: number;
  peak_day: string;
}

interface AnomalyResult {
  anomalies: Array<{
    type: string;
    severity: string;
    description: string;
  }>;
  risk_score: number;
  risk_level: string;
  requires_review: boolean;
  recommendations: string[];
}

interface RouteOptimization {
  optimized_route: any[];
  total_deliveries: number;
  total_destinations: number;
  estimated_time_minutes: number;
  optimization_score: number;
  recommendations: string[];
}

export const AIDashboard: React.FC<{ className?: string }> = ({ className = '' }) => {
  const [activeTab, setActiveTab] = useState<'predictions' | 'optimization' | 'anomalies' | 'demand'>('predictions');
  const [isLoading, setIsLoading] = useState(false);
  const [deliveryPrediction, setDeliveryPrediction] = useState<PredictionData | null>(null);
  const [demandData, setDemandData] = useState<DemandPrediction | null>(null);
  const [anomalyData, setAnomalyData] = useState<AnomalyResult | null>(null);
  const [routeData, setRouteData] = useState<RouteOptimization | null>(null);

  // Formulario para predicción de entrega
  const [predictionForm, setPredictionForm] = useState({
    origin: 'la_habana',
    destination: 'santiago_de_cuba',
    weight: 5,
    package_type: 'paquete',
    priority: 'normal'
  });

  // Formulario para análisis de anomalías
  const [anomalyForm, setAnomalyForm] = useState({
    weight: 10,
    declared_value: 100,
    destination: 'camaguey',
    sender_daily_count: 3
  });

  useEffect(() => {
    loadDemandPrediction();
  }, []);

  const predictDeliveryTime = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/ai/predict-delivery-time/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(predictionForm)
      });

      if (response.ok) {
        const data = await response.json();
        setDeliveryPrediction(data.prediction);
      }
    } catch (error) {
      console.error('Error predicting delivery time:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadDemandPrediction = async () => {
    try {
      const response = await fetch('/api/ai/predict-demand/?location=la_habana&days=7', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setDemandData(data.prediction);
      }
    } catch (error) {
      console.error('Error loading demand prediction:', error);
    }
  };

  const detectAnomalies = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/ai/detect-anomalies/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(anomalyForm)
      });

      if (response.ok) {
        const data = await response.json();
        setAnomalyData(data.anomalies);
      }
    } catch (error) {
      console.error('Error detecting anomalies:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const optimizeRoute = async () => {
    setIsLoading(true);
    try {
      // Datos de ejemplo para optimización de ruta
      const sampleDeliveries = [
        { id: 1, destination: 'la_habana', priority: 'urgent', address: 'Centro Habana' },
        { id: 2, destination: 'santiago_de_cuba', priority: 'normal', address: 'Santiago Centro' },
        { id: 3, destination: 'camaguey', priority: 'express', address: 'Camagüey Centro' },
        { id: 4, destination: 'holguin', priority: 'normal', address: 'Holguín Centro' }
      ];

      const response = await fetch('/api/ai/optimize-route/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ deliveries: sampleDeliveries })
      });

      if (response.ok) {
        const data = await response.json();
        setRouteData(data.optimized_route);
      }
    } catch (error) {
      console.error('Error optimizing route:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const tabs = [
    { id: 'predictions', label: 'Predicciones', icon: Clock },
    { id: 'optimization', label: 'Optimización', icon: Route },
    { id: 'anomalies', label: 'Anomalías', icon: AlertTriangle },
    { id: 'demand', label: 'Demanda', icon: TrendingUp }
  ];

  const cubanCities = [
    { value: 'la_habana', label: 'La Habana' },
    { value: 'santiago_de_cuba', label: 'Santiago de Cuba' },
    { value: 'camaguey', label: 'Camagüey' },
    { value: 'holguin', label: 'Holguín' },
    { value: 'villa_clara', label: 'Villa Clara' },
    { value: 'cienfuegos', label: 'Cienfuegos' },
    { value: 'matanzas', label: 'Matanzas' },
    { value: 'pinar_del_rio', label: 'Pinar del Río' }
  ];

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'high': return 'text-red-400 bg-red-500/20';
      case 'medium': return 'text-yellow-400 bg-yellow-500/20';
      default: return 'text-green-400 bg-green-500/20';
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'increasing': return <TrendingUp className="w-4 h-4 text-green-400" />;
      case 'decreasing': return <TrendingUp className="w-4 h-4 text-red-400 transform rotate-180" />;
      default: return <Activity className="w-4 h-4 text-blue-400" />;
    }
  };

  return (
    <div className={`bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <Brain className="w-8 h-8 text-purple-400" />
        <div>
          <h2 className="text-2xl font-bold text-white">Dashboard de IA</h2>
          <p className="text-gray-300">Inteligencia Artificial para PACKFY CUBA</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap gap-2 mb-6">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl font-medium transition-colors ${
                activeTab === tab.id
                  ? 'bg-purple-500/30 text-purple-200 border border-purple-400/50'
                  : 'bg-white/5 text-gray-300 hover:bg-white/10'
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Predictions Tab */}
      {activeTab === 'predictions' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Formulario de Predicción */}
            <div className="bg-white/5 rounded-xl p-4 border border-white/10">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Clock className="w-5 h-5" />
                Predictor de Tiempo de Entrega
              </h3>

              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm text-gray-300 mb-2">Origen</label>
                    <select
                      value={predictionForm.origin}
                      onChange={(e) => setPredictionForm(prev => ({ ...prev, origin: e.target.value }))}
                      className="w-full bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-white"
                    >
                      {cubanCities.map(city => (
                        <option key={city.value} value={city.value} className="bg-gray-800">
                          {city.label}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm text-gray-300 mb-2">Destino</label>
                    <select
                      value={predictionForm.destination}
                      onChange={(e) => setPredictionForm(prev => ({ ...prev, destination: e.target.value }))}
                      className="w-full bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-white"
                    >
                      {cubanCities.map(city => (
                        <option key={city.value} value={city.value} className="bg-gray-800">
                          {city.label}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm text-gray-300 mb-2">Peso (kg)</label>
                    <input
                      type="number"
                      value={predictionForm.weight}
                      onChange={(e) => setPredictionForm(prev => ({ ...prev, weight: Number(e.target.value) }))}
                      className="w-full bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-white"
                      min="0.1"
                      max="50"
                      step="0.1"
                    />
                  </div>

                  <div>
                    <label className="block text-sm text-gray-300 mb-2">Prioridad</label>
                    <select
                      value={predictionForm.priority}
                      onChange={(e) => setPredictionForm(prev => ({ ...prev, priority: e.target.value }))}
                      className="w-full bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-white"
                    >
                      <option value="economy" className="bg-gray-800">Económico</option>
                      <option value="normal" className="bg-gray-800">Normal</option>
                      <option value="express" className="bg-gray-800">Express</option>
                      <option value="urgent" className="bg-gray-800">Urgente</option>
                    </select>
                  </div>
                </div>

                <button
                  onClick={predictDeliveryTime}
                  disabled={isLoading}
                  className="w-full bg-purple-500 hover:bg-purple-600 disabled:bg-gray-500 text-white py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
                >
                  {isLoading ? (
                    <RefreshCw className="w-4 h-4 animate-spin" />
                  ) : (
                    <Zap className="w-4 h-4" />
                  )}
                  Predecir Tiempo
                </button>
              </div>
            </div>

            {/* Resultado de Predicción */}
            <div className="bg-white/5 rounded-xl p-4 border border-white/10">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Target className="w-5 h-5" />
                Resultado de Predicción
              </h3>

              {deliveryPrediction ? (
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-4 bg-blue-500/20 rounded-lg border border-blue-400/30">
                      <div className="text-2xl font-bold text-blue-200">
                        {deliveryPrediction.estimated_hours}h
                      </div>
                      <div className="text-sm text-blue-300">Horas estimadas</div>
                    </div>

                    <div className="text-center p-4 bg-green-500/20 rounded-lg border border-green-400/30">
                      <div className="text-2xl font-bold text-green-200">
                        {deliveryPrediction.estimated_days}
                      </div>
                      <div className="text-sm text-green-300">Días laborables</div>
                    </div>
                  </div>

                  <div className="bg-white/5 rounded-lg p-3">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-gray-300">Confianza</span>
                      <span className="text-white font-medium">
                        {Math.round(deliveryPrediction.confidence * 100)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div
                        className="bg-purple-500 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${deliveryPrediction.confidence * 100}%` }}
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <h4 className="text-sm font-medium text-gray-300">Factores considerados:</h4>
                    <div className="text-sm text-gray-400 space-y-1">
                      <div>• Peso: {deliveryPrediction.factors.weight}kg</div>
                      <div>• Prioridad: {deliveryPrediction.factors.priority}</div>
                      {deliveryPrediction.factors.distance && (
                        <div>• Distancia: {deliveryPrediction.factors.distance}</div>
                      )}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center py-8 text-gray-400">
                  <Clock className="w-12 h-12 mx-auto mb-3 opacity-50" />
                  <p>Ejecuta una predicción para ver los resultados</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Optimization Tab */}
      {activeTab === 'optimization' && (
        <div className="space-y-6">
          <div className="bg-white/5 rounded-xl p-4 border border-white/10">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <Route className="w-5 h-5" />
              Optimización de Rutas
            </h3>

            <button
              onClick={optimizeRoute}
              disabled={isLoading}
              className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-500 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center gap-2 mb-4"
            >
              {isLoading ? (
                <RefreshCw className="w-4 h-4 animate-spin" />
              ) : (
                <Route className="w-4 h-4" />
              )}
              Optimizar Ruta de Ejemplo
            </button>

            {routeData && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-blue-500/20 rounded-lg">
                  <Package className="w-6 h-6 mx-auto mb-2 text-blue-400" />
                  <div className="text-xl font-bold text-blue-200">{routeData.total_deliveries}</div>
                  <div className="text-sm text-blue-300">Entregas</div>
                </div>

                <div className="text-center p-4 bg-green-500/20 rounded-lg">
                  <MapPin className="w-6 h-6 mx-auto mb-2 text-green-400" />
                  <div className="text-xl font-bold text-green-200">{routeData.total_destinations}</div>
                  <div className="text-sm text-green-300">Destinos</div>
                </div>

                <div className="text-center p-4 bg-purple-500/20 rounded-lg">
                  <Clock className="w-6 h-6 mx-auto mb-2 text-purple-400" />
                  <div className="text-xl font-bold text-purple-200">
                    {Math.round(routeData.estimated_time_minutes / 60)}h
                  </div>
                  <div className="text-sm text-purple-300">Tiempo estimado</div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Anomalies Tab */}
      {activeTab === 'anomalies' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Formulario de Anomalías */}
            <div className="bg-white/5 rounded-xl p-4 border border-white/10">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5" />
                Detector de Anomalías
              </h3>

              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm text-gray-300 mb-2">Peso (kg)</label>
                    <input
                      type="number"
                      value={anomalyForm.weight}
                      onChange={(e) => setAnomalyForm(prev => ({ ...prev, weight: Number(e.target.value) }))}
                      className="w-full bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-white"
                    />
                  </div>

                  <div>
                    <label className="block text-sm text-gray-300 mb-2">Valor Declarado ($)</label>
                    <input
                      type="number"
                      value={anomalyForm.declared_value}
                      onChange={(e) => setAnomalyForm(prev => ({ ...prev, declared_value: Number(e.target.value) }))}
                      className="w-full bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-white"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm text-gray-300 mb-2">Envíos del día</label>
                  <input
                    type="number"
                    value={anomalyForm.sender_daily_count}
                    onChange={(e) => setAnomalyForm(prev => ({ ...prev, sender_daily_count: Number(e.target.value) }))}
                    className="w-full bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-white"
                  />
                </div>

                <button
                  onClick={detectAnomalies}
                  disabled={isLoading}
                  className="w-full bg-red-500 hover:bg-red-600 disabled:bg-gray-500 text-white py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
                >
                  {isLoading ? (
                    <RefreshCw className="w-4 h-4 animate-spin" />
                  ) : (
                    <AlertTriangle className="w-4 h-4" />
                  )}
                  Detectar Anomalías
                </button>
              </div>
            </div>

            {/* Resultado de Anomalías */}
            <div className="bg-white/5 rounded-xl p-4 border border-white/10">
              <h3 className="text-lg font-semibold text-white mb-4">Análisis de Riesgo</h3>

              {anomalyData ? (
                <div className="space-y-4">
                  <div className={`text-center p-4 rounded-lg ${getRiskColor(anomalyData.risk_level)}`}>
                    <div className="text-2xl font-bold">{anomalyData.risk_score}</div>
                    <div className="text-sm">Puntuación de Riesgo</div>
                    <div className="text-xs mt-1 capitalize">{anomalyData.risk_level}</div>
                  </div>

                  {anomalyData.anomalies.length > 0 && (
                    <div className="space-y-2">
                      <h4 className="font-medium text-white">Anomalías Detectadas:</h4>
                      {anomalyData.anomalies.map((anomaly, index) => (
                        <div key={index} className="bg-white/5 rounded-lg p-3">
                          <div className="text-sm text-gray-300">{anomaly.description}</div>
                          <div className={`text-xs mt-1 capitalize ${
                            anomaly.severity === 'high' ? 'text-red-400' :
                            anomaly.severity === 'medium' ? 'text-yellow-400' : 'text-green-400'
                          }`}>
                            Severidad: {anomaly.severity}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-400">
                  <AlertTriangle className="w-12 h-12 mx-auto mb-3 opacity-50" />
                  <p>Ejecuta un análisis para ver los resultados</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Demand Tab */}
      {activeTab === 'demand' && (
        <div className="space-y-6">
          <div className="bg-white/5 rounded-xl p-4 border border-white/10">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white flex items-center gap-2">
                <BarChart3 className="w-5 h-5" />
                Predicción de Demanda - La Habana
              </h3>
              <button
                onClick={loadDemandPrediction}
                className="text-blue-400 hover:text-blue-300"
                title="Actualizar datos"
              >
                <RefreshCw className="w-4 h-4" />
              </button>
            </div>

            {demandData && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Métricas Resumen */}
                <div className="space-y-4">
                  <div className="text-center p-4 bg-blue-500/20 rounded-lg">
                    <div className="text-2xl font-bold text-blue-200">{demandData.total_predicted}</div>
                    <div className="text-sm text-blue-300">Envíos Totales (7 días)</div>
                  </div>

                  <div className="text-center p-4 bg-green-500/20 rounded-lg">
                    <div className="text-2xl font-bold text-green-200">{demandData.average_daily_demand}</div>
                    <div className="text-sm text-green-300">Promedio Diario</div>
                  </div>

                  <div className="text-center p-4 bg-purple-500/20 rounded-lg flex items-center justify-center gap-2">
                    {getTrendIcon(demandData.trend)}
                    <div>
                      <div className="text-lg font-bold text-white capitalize">{demandData.trend}</div>
                      <div className="text-sm text-gray-300">Tendencia</div>
                    </div>
                  </div>
                </div>

                {/* Predicciones Diarias */}
                <div className="lg:col-span-2">
                  <h4 className="font-medium text-white mb-3">Predicciones por Día:</h4>
                  <div className="space-y-2">
                    {demandData.predictions.map((prediction, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                        <div>
                          <div className="text-white font-medium">
                            {new Date(prediction.date).toLocaleDateString('es-ES', {
                              weekday: 'long',
                              day: 'numeric',
                              month: 'short'
                            })}
                          </div>
                          <div className="text-sm text-gray-400">
                            Confianza: {Math.round(prediction.confidence * 100)}%
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-xl font-bold text-blue-200">
                            {prediction.predicted_shipments}
                          </div>
                          <div className="text-sm text-gray-300">envíos</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AIDashboard;
