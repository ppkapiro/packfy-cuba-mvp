# 🇨🇺 PACKFY CUBA - Chatbot Inteligente v4.0
import difflib
import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


class PackfyChatbot:
    """Chatbot inteligente para atención al cliente de PACKFY CUBA"""

    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()
        self.conversation_context = {}
        self.user_sessions = {}
        self.intent_patterns = self._compile_intent_patterns()

    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Cargar base de conocimiento del chatbot"""
        return {
            "greetings": {
                "patterns": [
                    "hola",
                    "buenos días",
                    "buenas tardes",
                    "saludos",
                    "hey",
                ],
                "responses": [
                    "¡Hola! 👋 Soy el asistente virtual de PACKFY CUBA 🇨🇺",
                    "¡Buenos días! Bienvenido a PACKFY CUBA. ¿En qué puedo ayudarte?",
                    "¡Saludos! Estoy aquí para ayudarte con tus envíos a Cuba 📦",
                ],
            },
            "tracking": {
                "patterns": [
                    "rastrear",
                    "seguimiento",
                    "dónde está",
                    "ubicación",
                    "estado",
                ],
                "responses": [
                    "Para rastrear tu envío, necesito el número de guía. ¿Podrías proporcionármelo?",
                    "🔍 ¿Tienes el número de seguimiento? Te ayudo a verificar el estado de tu paquete.",
                    "Claro, puedo ayudarte a rastrear tu envío. Compárteme el número de guía.",
                ],
            },
            "pricing": {
                "patterns": [
                    "precio",
                    "costo",
                    "tarifa",
                    "cuánto cuesta",
                    "cotizar",
                ],
                "responses": [
                    "💰 Nuestras tarifas dependen del peso, destino y tipo de envío. ¿Qué necesitas enviar?",
                    "Los precios varían según el peso y destino. ¿Podrías decirme el peso y destino?",
                    "Para darte un precio exacto, necesito: peso, dimensiones y ciudad de destino en Cuba.",
                ],
            },
            "shipping_time": {
                "patterns": [
                    "cuánto demora",
                    "tiempo",
                    "entrega",
                    "cuándo llega",
                ],
                "responses": [
                    "⏰ Los tiempos de entrega varían: 2-5 días para La Habana, 3-7 días otras provincias.",
                    "Depende del destino: zonas urbanas 2-5 días, zonas rurales 5-10 días.",
                    "El tiempo estimado es 3-7 días laborables, dependiendo de la provincia de destino.",
                ],
            },
            "prohibited_items": {
                "patterns": [
                    "qué puedo enviar",
                    "prohibido",
                    "restringido",
                    "no permitido",
                ],
                "responses": [
                    "❌ No se pueden enviar: líquidos, baterías, medicinas, dinero en efectivo.",
                    "Artículos permitidos: ropa, electrónicos (sin batería), alimentos secos, documentos.",
                    "Consulta nuestra lista completa de artículos prohibidos en la web.",
                ],
            },
            "documentation": {
                "patterns": [
                    "documentos",
                    "papeles",
                    "requisitos",
                    "qué necesito",
                ],
                "responses": [
                    "📄 Necesitas: ID del remitente, datos completos del destinatario, inventario detallado.",
                    "Documentación requerida: identificación, dirección completa, descripción del contenido.",
                    "Para enviar necesitas completar el formulario con datos del remitente y destinatario.",
                ],
            },
            "payment": {
                "patterns": [
                    "pagar",
                    "pago",
                    "forma de pago",
                    "tarjeta",
                    "transferencia",
                ],
                "responses": [
                    "💳 Aceptamos: tarjetas de crédito, débito, transferencias bancarias y PayPal.",
                    "Formas de pago disponibles: Visa, Mastercard, transferencia y pagos digitales.",
                    "Puedes pagar con tarjeta, transferencia o plataformas digitales seguras.",
                ],
            },
            "complaints": {
                "patterns": [
                    "problema",
                    "queja",
                    "reclamo",
                    "perdido",
                    "dañado",
                ],
                "responses": [
                    "😟 Lamento el inconveniente. Te conectaré con un agente especializado.",
                    "Entiendo tu preocupación. Necesito más detalles para ayudarte mejor.",
                    "Voy a escalar tu caso al departamento correspondiente inmediatamente.",
                ],
            },
            "cuba_info": {
                "patterns": ["cuba", "provincias", "ciudades", "destinos"],
                "responses": [
                    "🇨🇺 Enviamos a todas las provincias de Cuba: La Habana, Santiago, Camagüey, etc.",
                    "Cobertura nacional en Cuba: 15 provincias, más de 160 municipios.",
                    "Destinos disponibles en Cuba: todas las provincias y principales municipios.",
                ],
            },
            "farewells": {
                "patterns": ["gracias", "adiós", "hasta luego", "bye"],
                "responses": [
                    "¡De nada! Que tengas un excelente día. ¡Viva Cuba! 🇨🇺",
                    "Gracias por elegir PACKFY CUBA. ¡Hasta pronto! 📦",
                    "¡Fue un placer ayudarte! ¡Que tus envíos lleguen seguros a Cuba! 🚀",
                ],
            },
        }

    def _compile_intent_patterns(self) -> Dict[str, List[str]]:
        """Compilar patrones de intención optimizados"""
        patterns = {}
        for intent, data in self.knowledge_base.items():
            patterns[intent] = data.get("patterns", [])
        return patterns

    def process_message(
        self, user_id: str, message: str, context: Dict = None
    ) -> Dict[str, Any]:
        """
        Procesar mensaje del usuario y generar respuesta

        Args:
            user_id: ID único del usuario
            message: Mensaje del usuario
            context: Contexto adicional (envíos, usuario, etc.)

        Returns:
            Respuesta del chatbot con metadatos
        """
        try:
            # Inicializar sesión del usuario si no existe
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = {
                    "messages": [],
                    "context": {},
                    "created_at": timezone.now(),
                    "last_activity": timezone.now(),
                }

            session = self.user_sessions[user_id]
            session["last_activity"] = timezone.now()
            session["messages"].append(
                {
                    "type": "user",
                    "content": message,
                    "timestamp": timezone.now(),
                }
            )

            # Limpiar y normalizar mensaje
            clean_message = self._clean_message(message)

            # Detectar intención
            intent, confidence = self._detect_intent(clean_message)

            # Generar respuesta basada en intención
            response_data = self._generate_response(
                intent, clean_message, context, session
            )

            # Guardar respuesta en sesión
            session["messages"].append(
                {
                    "type": "bot",
                    "content": response_data["text"],
                    "timestamp": timezone.now(),
                    "intent": intent,
                    "confidence": confidence,
                }
            )

            # Actualizar contexto
            if context:
                session["context"].update(context)

            return {
                "text": response_data["text"],
                "intent": intent,
                "confidence": confidence,
                "actions": response_data.get("actions", []),
                "quick_replies": response_data.get("quick_replies", []),
                "metadata": {
                    "user_id": user_id,
                    "timestamp": timezone.now().isoformat(),
                    "session_length": len(session["messages"]),
                },
            }

        except Exception as e:
            logger.error(f"Error processing chatbot message: {e}")
            return self._error_response()

    def _clean_message(self, message: str) -> str:
        """Limpiar y normalizar mensaje del usuario"""
        # Convertir a minúsculas
        clean = message.lower().strip()

        # Remover caracteres especiales excepto espacios y números
        clean = re.sub(r"[^\w\s\dñáéíóúü]", " ", clean)

        # Normalizar espacios múltiples
        clean = re.sub(r"\s+", " ", clean).strip()

        return clean

    def _detect_intent(self, message: str) -> Tuple[str, float]:
        """
        Detectar la intención del usuario basada en el mensaje

        Returns:
            Tupla con (intención, confianza)
        """
        best_intent = "unknown"
        best_confidence = 0.0

        # Verificar patrones exactos primero
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern in message:
                    confidence = len(pattern) / len(
                        message
                    )  # Confianza basada en longitud
                    if confidence > best_confidence:
                        best_intent = intent
                        best_confidence = min(confidence, 0.95)  # Máximo 95%

        # Si no hay coincidencia exacta, usar similitud difusa
        if best_confidence < 0.3:
            for intent, patterns in self.intent_patterns.items():
                for pattern in patterns:
                    similarity = difflib.SequenceMatcher(
                        None, pattern, message
                    ).ratio()
                    if similarity > best_confidence and similarity > 0.5:
                        best_intent = intent
                        best_confidence = similarity

        # Detectar números de guía (patrón específico)
        if re.search(r"\b[A-Z]{2}\d{6,10}\b", message.upper()):
            return "tracking_number", 0.9

        return best_intent, best_confidence

    def _generate_response(
        self, intent: str, message: str, context: Dict, session: Dict
    ) -> Dict[str, Any]:
        """Generar respuesta basada en la intención detectada"""

        if intent == "tracking_number":
            return self._handle_tracking_number(message, context)
        elif intent == "tracking":
            return self._handle_tracking_request(context)
        elif intent == "pricing":
            return self._handle_pricing_request(message, context)
        elif intent == "complaints":
            return self._handle_complaint(message, context)
        elif intent in self.knowledge_base:
            return self._handle_general_intent(intent)
        else:
            return self._handle_unknown_intent(message)

    def _handle_tracking_number(
        self, message: str, context: Dict
    ) -> Dict[str, Any]:
        """Manejar solicitud con número de guía específico"""
        # Extraer número de guía
        tracking_match = re.search(r"\b[A-Z]{2}\d{6,10}\b", message.upper())
        if tracking_match:
            tracking_number = tracking_match.group()

            # Simular búsqueda de envío (en producción, consultar BD)
            if context and "shipments" in context:
                shipment = next(
                    (
                        s
                        for s in context["shipments"]
                        if s.get("numero_guia") == tracking_number
                    ),
                    None,
                )
                if shipment:
                    status = shipment.get("estado", "En tránsito")
                    return {
                        "text": f"📦 Tu envío {tracking_number} está: {status}\n"
                        f'Destino: {shipment.get("destinatario_ciudad", "Cuba")}\n'
                        f'Última actualización: {shipment.get("fecha_actualizacion", "Hoy")}',
                        "actions": ["view_details"],
                        "quick_replies": [
                            "Ver más detalles",
                            "Rastrear otro envío",
                        ],
                    }

            return {
                "text": f"🔍 Buscando información para el envío {tracking_number}...\n"
                "Si no encuentro resultados, verifica que el número sea correcto.",
                "quick_replies": ["Ayuda con rastreo", "Contactar agente"],
            }

        return {
            "text": "No pude identificar un número de guía válido. Los números tienen formato: AB123456789",
            "quick_replies": ["Ejemplo de número", "Ayuda"],
        }

    def _handle_tracking_request(self, context: Dict) -> Dict[str, Any]:
        """Manejar solicitud general de rastreo"""
        if context and "user_shipments" in context:
            recent_shipments = context["user_shipments"][
                :3
            ]  # Últimos 3 envíos
            if recent_shipments:
                response = "📦 Tus envíos recientes:\n\n"
                for shipment in recent_shipments:
                    response += f"• {shipment.get('numero_guia')}: {shipment.get('estado')}\n"

                return {
                    "text": response + "\n¿Cuál te interesa revisar?",
                    "quick_replies": [
                        s.get("numero_guia") for s in recent_shipments
                    ],
                }

        return {
            "text": "Para rastrear tu envío, compárteme el número de guía de 9-11 caracteres.",
            "quick_replies": ["¿Dónde encuentro el número?", "Ejemplos"],
        }

    def _handle_pricing_request(
        self, message: str, context: Dict
    ) -> Dict[str, Any]:
        """Manejar solicitud de precios"""
        # Extraer información de peso si está presente
        weight_match = re.search(
            r"(\d+(?:\.\d+)?)\s*(?:kg|kilos?|libras?)", message
        )

        if weight_match:
            weight = float(weight_match.group(1))
            estimated_price = self._calculate_estimated_price(weight)

            return {
                "text": f"💰 Para {weight}kg el precio estimado es ${estimated_price:.2f} USD\n"
                "Precio final depende del destino exacto en Cuba.",
                "actions": ["calculate_exact"],
                "quick_replies": [
                    "Calcular precio exacto",
                    "Ver todas las tarifas",
                ],
            }

        return {
            "text": "💰 Para cotizar necesito:\n• Peso del paquete\n• Ciudad de destino en Cuba\n"
            "¿Cuánto pesa lo que quieres enviar?",
            "quick_replies": ["1-5 kg", "5-10 kg", "10+ kg"],
        }

    def _handle_complaint(self, message: str, context: Dict) -> Dict[str, Any]:
        """Manejar quejas o problemas"""
        # Detectar tipo de problema
        if "perdido" in message or "extraviado" in message:
            problem_type = "Paquete perdido"
        elif "dañado" in message or "roto" in message:
            problem_type = "Paquete dañado"
        elif "demora" in message or "retrasado" in message:
            problem_type = "Retraso en entrega"
        else:
            problem_type = "Problema general"

        return {
            "text": f"😟 Lamento mucho este inconveniente con tu envío.\n"
            f"He clasificado tu caso como: {problem_type}\n\n"
            f"Un agente especializado te contactará en máximo 2 horas.\n"
            f"Mientras tanto, ¿podrías compartir el número de guía?",
            "actions": ["escalate_to_human", "create_ticket"],
            "quick_replies": [
                "Hablar con agente ahora",
                "Enviar número de guía",
            ],
        }

    def _handle_general_intent(self, intent: str) -> Dict[str, Any]:
        """Manejar intenciones generales de la base de conocimiento"""
        responses = self.knowledge_base[intent]["responses"]
        import random

        selected_response = random.choice(responses)

        # Agregar quick replies relevantes según la intención
        quick_replies = self._get_quick_replies_for_intent(intent)

        return {"text": selected_response, "quick_replies": quick_replies}

    def _handle_unknown_intent(self, message: str) -> Dict[str, Any]:
        """Manejar mensajes no reconocidos"""
        return {
            "text": "🤔 No estoy seguro de entender tu pregunta.\n"
            "¿Podrías reformularla o elegir una de estas opciones?",
            "quick_replies": [
                "Rastrear envío",
                "Precios y tarifas",
                "Tiempos de entrega",
                "Hablar con humano",
            ],
        }

    def _get_quick_replies_for_intent(self, intent: str) -> List[str]:
        """Obtener respuestas rápidas relevantes para cada intención"""
        quick_replies_map = {
            "greetings": ["Rastrear envío", "Ver precios", "Hacer pregunta"],
            "tracking": [
                "Tengo número de guía",
                "No tengo número",
                "Envíos recientes",
            ],
            "pricing": [
                "Cotizar envío",
                "Ver todas las tarifas",
                "Calculadora",
            ],
            "shipping_time": ["Envío urgente", "Envío normal", "Ver opciones"],
            "prohibited_items": [
                "Lista completa",
                "Consultar artículo",
                "Alternativas",
            ],
            "cuba_info": [
                "Ver provincias",
                "Cobertura",
                "Tiempos por destino",
            ],
            "payment": [
                "Métodos disponibles",
                "Pagar ahora",
                "Ayuda con pago",
            ],
            "farewells": ["Nueva consulta", "Rastrear otro envío", "Contacto"],
        }

        return quick_replies_map.get(intent, ["Ayuda", "Menú principal"])

    def _calculate_estimated_price(self, weight: float) -> float:
        """Calcular precio estimado basado en peso"""
        # Tarifas simplificadas
        if weight <= 1:
            return 15.0
        elif weight <= 5:
            return 15.0 + (weight - 1) * 8.0
        elif weight <= 10:
            return 47.0 + (weight - 5) * 6.0
        else:
            return 77.0 + (weight - 10) * 4.0

    def _error_response(self) -> Dict[str, Any]:
        """Respuesta de error genérica"""
        return {
            "text": "😅 Disculpa, tuve un pequeño problema técnico.\n"
            "Por favor intenta nuevamente o contacta a nuestro soporte.",
            "intent": "error",
            "confidence": 1.0,
            "quick_replies": ["Reintentar", "Contactar soporte"],
            "metadata": {
                "timestamp": timezone.now().isoformat(),
                "error": True,
            },
        }

    def get_conversation_summary(self, user_id: str) -> Dict[str, Any]:
        """Obtener resumen de conversación del usuario"""
        if user_id not in self.user_sessions:
            return {"error": "Session not found"}

        session = self.user_sessions[user_id]
        messages = session["messages"]

        # Analizar intenciones más comunes
        intents = [msg.get("intent") for msg in messages if msg.get("intent")]
        intent_counts = {}
        for intent in intents:
            intent_counts[intent] = intent_counts.get(intent, 0) + 1

        return {
            "user_id": user_id,
            "total_messages": len(messages),
            "session_duration": (
                session["last_activity"] - session["created_at"]
            ).total_seconds(),
            "top_intents": sorted(
                intent_counts.items(), key=lambda x: x[1], reverse=True
            )[:3],
            "created_at": session["created_at"].isoformat(),
            "last_activity": session["last_activity"].isoformat(),
        }

    def clear_old_sessions(self, max_age_hours: int = 24):
        """Limpiar sesiones antiguas"""
        cutoff_time = timezone.now() - timezone.timedelta(hours=max_age_hours)
        old_sessions = [
            user_id
            for user_id, session in self.user_sessions.items()
            if session["last_activity"] < cutoff_time
        ]

        for user_id in old_sessions:
            del self.user_sessions[user_id]

        logger.info(f"Cleared {len(old_sessions)} old chatbot sessions")
        return len(old_sessions)


# Instancia global del chatbot
packfy_chatbot = PackfyChatbot()
