'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, RefreshCw, ThumbsUp, ThumbsDown, Copy, Check } from 'lucide-react';
import { aiAssistantApi, ChatMessage } from '@/lib/api';

export default function ChatInterface() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copiedMessageId, setCopiedMessageId] = useState<number | null>(null);
  const [feedback, setFeedback] = useState<{ [key: number]: 'up' | 'down' | null }>({});
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      role: 'client',
      message: input.trim(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await aiAssistantApi.generateReply({
        clientSequence: userMessage.message,
        chatHistory: messages.filter(m => m !== userMessage),
      });

      const aiMessage: ChatMessage = {
        role: 'consultant',
        message: response.aiReply,
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error generating reply:', error);
      const errorMessage = error instanceof Error ? error.message : 'Failed to generate response';
      setError(errorMessage);
      
      const errorBotMessage: ChatMessage = {
        role: 'consultant',
        message: 'Sorry, I encountered an error. Please try again or contact support if the issue persists.',
      };
      setMessages(prev => [...prev, errorBotMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleRetry = async () => {
    if (messages.length < 2) return;
    
    const lastUserMessage = messages.filter(m => m.role === 'client').pop();
    if (!lastUserMessage) return;

    // Remove the last AI message and retry
    setMessages(prev => prev.slice(0, -1));
    setInput(lastUserMessage.message);
  };

  const handleCopy = async (message: string, index: number) => {
    try {
      await navigator.clipboard.writeText(message);
      setCopiedMessageId(index);
      setTimeout(() => setCopiedMessageId(null), 2000);
    } catch (error) {
      console.error('Failed to copy message:', error);
    }
  };

  const handleFeedback = (messageIndex: number, type: 'up' | 'down') => {
    setFeedback(prev => ({
      ...prev,
      [messageIndex]: prev[messageIndex] === type ? null : type
    }));
  };

  const handleClearChat = () => {
    setMessages([]);
    setError(null);
    setFeedback({});
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg border border-gray-200">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-4 rounded-t-lg">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold flex items-center gap-2">
              <Bot size={24} />
              Visa AI Assistant
            </h1>
            <p className="text-sm opacity-90 mt-1">
              Get help with your visa application questions
            </p>
          </div>
          <button
            onClick={handleClearChat}
            className="px-3 py-1 text-sm bg-white/20 hover:bg-white/30 rounded-lg transition-colors"
          >
            Clear Chat
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mx-4 mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center justify-between">
            <p className="text-sm text-red-700">{error}</p>
            <button
              onClick={handleRetry}
              className="flex items-center gap-1 px-2 py-1 text-sm bg-red-100 hover:bg-red-200 text-red-700 rounded transition-colors"
            >
              <RefreshCw size={14} />
              Retry
            </button>
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 mt-8">
            <Bot size={48} className="mx-auto mb-4 opacity-50" />
            <h2 className="text-lg font-medium text-gray-700 mb-2">Hello! I'm here to help 🌟</h2>
            <p className="text-sm mb-4">Ask me anything about visa applications, requirements, or processes.</p>
            <div className="flex flex-wrap justify-center gap-2 max-w-md mx-auto">
              {[
                "How do I apply for a DTV visa?",
                "What documents do I need?",
                "How long does processing take?",
                "Can I apply from another country?"
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => setInput(suggestion)}
                  className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              className={`flex gap-3 ${
                message.role === 'client' ? 'justify-end' : 'justify-start'
              }`}
            >
              {message.role === 'consultant' && (
                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                  <Bot size={16} className="text-white" />
                </div>
              )}
              <div className="max-w-xs md:max-w-md lg:max-w-xl">
                <div
                  className={`px-4 py-2 rounded-lg ${
                    message.role === 'client'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 border border-gray-200 text-gray-800'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.message}</p>
                </div>
                {message.role === 'consultant' && (
                  <div className="flex items-center gap-2 mt-2 ml-2">
                    <button
                      onClick={() => handleCopy(message.message, index)}
                      className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                      title="Copy message"
                    >
                      {copiedMessageId === index ? <Check size={14} /> : <Copy size={14} />}
                    </button>
                    <button
                      onClick={() => handleFeedback(index, 'up')}
                      className={`p-1 transition-colors ${
                        feedback[index] === 'up' ? 'text-green-600' : 'text-gray-400 hover:text-gray-600'
                      }`}
                      title="Helpful"
                    >
                      <ThumbsUp size={14} />
                    </button>
                    <button
                      onClick={() => handleFeedback(index, 'down')}
                      className={`p-1 transition-colors ${
                        feedback[index] === 'down' ? 'text-red-600' : 'text-gray-400 hover:text-gray-600'
                      }`}
                      title="Not helpful"
                    >
                      <ThumbsDown size={14} />
                    </button>
                  </div>
                )}
              </div>
              {message.role === 'client' && (
                <div className="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center flex-shrink-0">
                  <User size={16} className="text-white" />
                </div>
              )}
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex gap-3 justify-start">
            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
              <Bot size={16} className="text-white" />
            </div>
            <div className="bg-gray-100 border border-gray-200 px-4 py-2 rounded-lg">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t bg-gray-50 p-4 rounded-b-lg">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message... (Press Enter to send, Shift+Enter for new line)"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            disabled={isLoading}
            rows={1}
            style={{ minHeight: '40px', maxHeight: '120px' }}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2 self-end"
          >
            <Send size={18} />
            Send
          </button>
        </div>
        <div className="mt-2 text-xs text-gray-500 text-center">
          AI responses are for guidance only. Please consult with immigration professionals for official advice.
        </div>
      </div>
    </div>
  );
}
