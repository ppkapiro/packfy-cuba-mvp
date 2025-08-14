// 🇨🇺 PACKFY CUBA - Componente Chatbot Inteligente v4.0
import React, { useState, useEffect, useRef } from 'react';
import {
  MessageCircle,
  X,
  Send,
  Bot,
  User,
  Minimize2,
  Maximize2,
  RefreshCw,
  AlertCircle
} from 'lucide-react';

interface Message {
  id: string;
  type: 'user' | 'bot';
  content: string;
  timestamp: Date;
  intent?: string;
  confidence?: number;
  actions?: string[];
  quickReplies?: string[];
}

interface ChatbotProps {
  className?: string;
  position?: 'bottom-right' | 'bottom-left' | 'center';
  initialOpen?: boolean;
}

export const Chatbot: React.FC<ChatbotProps> = ({
  className = '',
  position = 'bottom-right',
  initialOpen = false
}) => {
  const [isOpen, setIsOpen] = useState(initialOpen);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected' | 'connecting'>('disconnected');

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Posicionamiento dinámico
  const getPositionClasses = () => {
    switch (position) {
      case 'bottom-left':
        return 'bottom-4 left-4';
      case 'center':
        return 'top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2';
      default:
        return 'bottom-4 right-4';
    }
  };

  useEffect(() => {
    if (isOpen && messages.length === 0) {
      initializeChat();
    }
  }, [isOpen]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen, isMinimized]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const initializeChat = async () => {
    setConnectionStatus('connecting');

    try {
      // Verificar estado del chatbot
      const healthResponse = await fetch('/api/chatbot/health/');

      if (healthResponse.ok) {
        setConnectionStatus('connected');

        // Mensaje de bienvenida
        const welcomeMessage: Message = {
          id: `msg_${Date.now()}`,
          type: 'bot',
          content: '¡Hola! 👋 Soy el asistente virtual de PACKFY CUBA 🇨🇺\n\n¿En qué puedo ayudarte hoy?',
          timestamp: new Date(),
          quickReplies: [
            'Rastrear envío',
            'Ver precios',
            'Tiempos de entrega',
            'Hacer pregunta'
          ]
        };

        setMessages([welcomeMessage]);
      } else {
        throw new Error('Chatbot no disponible');
      }
    } catch (error) {
      console.error('Error initializing chatbot:', error);
      setConnectionStatus('disconnected');

      const errorMessage: Message = {
        id: `msg_${Date.now()}`,
        type: 'bot',
        content: '😅 Lo siento, tengo problemas de conexión en este momento.\n\nPor favor intenta más tarde o contacta a nuestro soporte.',
        timestamp: new Date(),
        quickReplies: ['Reintentar', 'Contactar soporte']
      };

      setMessages([errorMessage]);
    }
  };

  const sendMessage = async (content: string, isQuickReply: boolean = false) => {
    if (!content.trim() || isLoading) return;

    // Limpiar input si no es respuesta rápida
    if (!isQuickReply) {
      setInputMessage('');
    }

    // Agregar mensaje del usuario
    const userMessage: Message = {
      id: `msg_${Date.now()}_user`,
      type: 'user',
      content: content.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setIsTyping(true);

    try {
      // Simular delay de escritura
      await new Promise(resolve => setTimeout(resolve, 1000));

      const response = await fetch('/api/chatbot/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          message: content,
          context: {
            timestamp: new Date().toISOString(),
            user_agent: navigator.userAgent
          }
        })
      });

      if (!response.ok) {
        throw new Error('Error en respuesta del servidor');
      }

      const data = await response.json();

      if (data.success && data.response) {
        const botMessage: Message = {
          id: `msg_${Date.now()}_bot`,
          type: 'bot',
          content: data.response.text,
          timestamp: new Date(),
          intent: data.response.intent,
          confidence: data.response.confidence,
          actions: data.response.actions,
          quickReplies: data.response.quick_replies
        };

        setMessages(prev => [...prev, botMessage]);
        setConnectionStatus('connected');
      } else {
        throw new Error(data.error || 'Error procesando mensaje');
      }

    } catch (error) {
      console.error('Error sending message:', error);
      setConnectionStatus('disconnected');

      const errorMessage: Message = {
        id: `msg_${Date.now()}_error`,
        type: 'bot',
        content: '😅 Disculpa, tuve un problema procesando tu mensaje.\n\n¿Podrías intentar reformulándolo?',
        timestamp: new Date(),
        quickReplies: ['Reintentar', 'Hablar con humano']
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(inputMessage);
    }
  };

  const handleQuickReply = (reply: string) => {
    sendMessage(reply, true);
  };

  const clearChat = () => {
    setMessages([]);
    initializeChat();
  };

  const toggleMinimize = () => {
    setIsMinimized(!isMinimized);
  };

  const formatMessageContent = (content: string) => {
    // Convertir saltos de línea a elementos <br>
    return content.split('\n').map((line, index) => (
      <React.Fragment key={index}>
        {line}
        {index < content.split('\n').length - 1 && <br />}
      </React.Fragment>
    ));
  };

  const getConnectionStatusColor = () => {
    switch (connectionStatus) {
      case 'connected':
        return 'text-green-400';
      case 'connecting':
        return 'text-yellow-400';
      default:
        return 'text-red-400';
    }
  };

  if (!isOpen) {
    return (
      <div className={`fixed ${getPositionClasses()} z-50`}>
        <button
          onClick={() => setIsOpen(true)}
          className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white p-4 rounded-full shadow-lg transition-all duration-300 hover:scale-110 animate-pulse"
        >
          <MessageCircle className="w-6 h-6" />
        </button>
      </div>
    );
  }

  return (
    <div className={`fixed ${getPositionClasses()} z-50 ${className}`}>
      <div className={`bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl shadow-2xl transition-all duration-300 ${
        isMinimized ? 'h-16 w-80' : 'h-[600px] w-96'
      }`}>

        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-white/20">
          <div className="flex items-center gap-3">
            <div className="relative">
              <Bot className="w-8 h-8 text-blue-400" />
              <div className={`absolute -top-1 -right-1 w-3 h-3 rounded-full ${
                connectionStatus === 'connected' ? 'bg-green-400' :
                connectionStatus === 'connecting' ? 'bg-yellow-400' : 'bg-red-400'
              }`} />
            </div>
            <div>
              <h3 className="font-bold text-white">PACKFY Assistant</h3>
              <p className={`text-xs ${getConnectionStatusColor()}`}>
                {connectionStatus === 'connected' ? 'En línea' :
                 connectionStatus === 'connecting' ? 'Conectando...' : 'Desconectado'}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={toggleMinimize}
              className="p-1 text-gray-300 hover:text-white transition-colors"
            >
              {isMinimized ? <Maximize2 className="w-4 h-4" /> : <Minimize2 className="w-4 h-4" />}
            </button>
            <button
              onClick={clearChat}
              className="p-1 text-gray-300 hover:text-white transition-colors"
              title="Limpiar chat"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1 text-gray-300 hover:text-white transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Chat Area */}
        {!isMinimized && (
          <>
            <div
              ref={chatContainerRef}
              className="flex-1 overflow-y-auto p-4 space-y-4 h-[440px]"
            >
              {messages.length === 0 && connectionStatus === 'disconnected' && (
                <div className="flex items-center justify-center h-full">
                  <div className="text-center text-gray-400">
                    <AlertCircle className="w-8 h-8 mx-auto mb-2" />
                    <p>Error de conexión</p>
                    <button
                      onClick={initializeChat}
                      className="mt-2 px-3 py-1 bg-blue-500/20 text-blue-200 rounded-lg hover:bg-blue-500/30"
                    >
                      Reintentar
                    </button>
                  </div>
                </div>
              )}

              {messages.map((message) => (
                <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`flex items-start gap-2 max-w-[80%] ${message.type === 'user' ? 'flex-row-reverse' : ''}`}>

                    {/* Avatar */}
                    <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                      message.type === 'user'
                        ? 'bg-blue-500/20 text-blue-200'
                        : 'bg-purple-500/20 text-purple-200'
                    }`}>
                      {message.type === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                    </div>

                    {/* Message Content */}
                    <div className={`p-3 rounded-2xl ${
                      message.type === 'user'
                        ? 'bg-blue-500/20 text-blue-100 rounded-br-md'
                        : 'bg-white/10 text-white rounded-bl-md'
                    }`}>
                      <div className="text-sm">
                        {formatMessageContent(message.content)}
                      </div>

                      {/* Metadata for bot messages */}
                      {message.type === 'bot' && message.intent && message.confidence && (
                        <div className="mt-2 text-xs text-gray-400">
                          Intención: {message.intent} ({Math.round(message.confidence * 100)}%)
                        </div>
                      )}

                      {/* Quick Replies */}
                      {message.type === 'bot' && message.quickReplies && message.quickReplies.length > 0 && (
                        <div className="mt-3 flex flex-wrap gap-2">
                          {message.quickReplies.map((reply, index) => (
                            <button
                              key={index}
                              onClick={() => handleQuickReply(reply)}
                              className="px-3 py-1 bg-white/10 hover:bg-white/20 text-xs text-white rounded-full border border-white/20 transition-colors"
                            >
                              {reply}
                            </button>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}

              {/* Typing Indicator */}
              {isTyping && (
                <div className="flex justify-start">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-full bg-purple-500/20 text-purple-200 flex items-center justify-center">
                      <Bot className="w-4 h-4" />
                    </div>
                    <div className="bg-white/10 p-3 rounded-2xl rounded-bl-md">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-white/50 rounded-full animate-bounce" />
                        <div className="w-2 h-2 bg-white/50 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                        <div className="w-2 h-2 bg-white/50 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 border-t border-white/20">
              <div className="flex items-center gap-2">
                <input
                  ref={inputRef}
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Escribe tu mensaje..."
                  disabled={isLoading || connectionStatus === 'disconnected'}
                  className="flex-1 bg-white/10 border border-white/20 rounded-xl px-4 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-400 disabled:opacity-50"
                />
                <button
                  onClick={() => sendMessage(inputMessage)}
                  disabled={!inputMessage.trim() || isLoading || connectionStatus === 'disconnected'}
                  className="p-2 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-500 disabled:opacity-50 text-white rounded-xl transition-colors"
                >
                  {isLoading ? (
                    <RefreshCw className="w-5 h-5 animate-spin" />
                  ) : (
                    <Send className="w-5 h-5" />
                  )}
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Chatbot;
