'use client';

import { useState } from 'react';
import { Settings, MessageCircle } from 'lucide-react';
import ChatInterface from '@/components/ChatInterface';
import AdminPromptEditor from '@/components/AdminPromptEditor';

export default function Home() {
  const [currentView, setCurrentView] = useState<'chat' | 'admin'>('chat');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">Visa AI Assistant</h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setCurrentView('chat')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                  currentView === 'chat'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <MessageCircle size={18} />
                Chat
              </button>
              <button
                onClick={() => setCurrentView('admin')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                  currentView === 'admin'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <Settings size={18} />
                Admin
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="p-4">
        {currentView === 'chat' ? (
          <div className="max-w-4xl mx-auto">
            <ChatInterface />
          </div>
        ) : (
          <AdminPromptEditor />
        )}
      </div>
    </div>
  );
}
