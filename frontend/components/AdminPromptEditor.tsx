'use client';

import { useState, useEffect } from 'react';
import { Save, Download, Upload, RefreshCw, Settings, Eye, EyeOff } from 'lucide-react';
import { aiAssistantApi } from '@/lib/api';

export default function AdminPromptEditor() {
  const [prompt, setPrompt] = useState('');
  const [originalPrompt, setOriginalPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [showPreview, setShowPreview] = useState(false);

  useEffect(() => {
    loadPrompt();
  }, []);

  const loadPrompt = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await aiAssistantApi.getPrompt();
      setPrompt(response.prompt);
      setOriginalPrompt(response.prompt);
    } catch (error) {
      console.error('Failed to load prompt:', error);
      setError('Failed to load current prompt from server');
    } finally {
      setIsLoading(false);
    }
  };

  const savePrompt = async () => {
    try {
      setIsSaving(true);
      setError(null);
      setSuccess(null);
      
      const response = await aiAssistantApi.updatePrompt({ prompt });
      setOriginalPrompt(prompt);
      setSuccess('Prompt updated successfully!');
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(null), 3000);
    } catch (error) {
      console.error('Failed to save prompt:', error);
      setError('Failed to save prompt. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  const resetPrompt = () => {
    setPrompt(originalPrompt);
    setError(null);
    setSuccess(null);
  };

  const downloadPrompt = () => {
    const blob = new Blob([prompt], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'ai-prompt-backup.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const uploadPrompt = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result as string;
      setPrompt(content);
      setSuccess('Prompt loaded from file');
      setTimeout(() => setSuccess(null), 3000);
    };
    reader.onerror = () => {
      setError('Failed to read file');
    };
    reader.readAsText(file);
  };

  const hasChanges = prompt !== originalPrompt;

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-3">
                <Settings className="text-blue-600" size={28} />
                AI Prompt Editor
              </h1>
              <p className="text-gray-600 mt-2">
                Modify the AI assistant's behavior and response style by editing the prompt below.
              </p>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setShowPreview(!showPreview)}
                className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              >
                {showPreview ? <EyeOff size={18} /> : <Eye size={18} />}
                {showPreview ? 'Hide Preview' : 'Show Preview'}
              </button>
            </div>
          </div>
        </div>

        {/* Status Messages */}
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-700">{error}</p>
          </div>
        )}
        
        {success && (
          <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-green-700">{success}</p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Editor */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200">
            <div className="border-b border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900">Prompt Editor</h2>
                <div className="flex items-center gap-2">
                  {hasChanges && (
                    <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
                      Unsaved changes
                    </span>
                  )}
                </div>
              </div>
            </div>
            
            <div className="p-4">
              {isLoading ? (
                <div className="flex items-center justify-center py-12">
                  <RefreshCw className="animate-spin text-blue-600" size={24} />
                  <span className="ml-2 text-gray-600">Loading prompt...</span>
                </div>
              ) : (
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  className="w-full h-96 p-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm resize-none text-gray-900 placeholder-gray-500"
                  placeholder="Enter your AI prompt here..."
                  disabled={isSaving}
                />
              )}
            </div>

            {/* Action Buttons */}
            <div className="border-t border-gray-200 p-4 bg-gray-50 rounded-b-lg">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div className="flex items-center gap-2">
                  <button
                    onClick={savePrompt}
                    disabled={isSaving || !hasChanges || isLoading}
                    className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    <Save size={18} />
                    {isSaving ? 'Saving...' : 'Save Changes'}
                  </button>
                  
                  <button
                    onClick={resetPrompt}
                    disabled={!hasChanges || isLoading}
                    className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    <RefreshCw size={18} />
                    Reset
                  </button>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={downloadPrompt}
                    className="flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                    title="Download prompt as file"
                  >
                    <Download size={18} />
                    Export
                  </button>
                  
                  <label className="flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors cursor-pointer">
                    <Upload size={18} />
                    Import
                    <input
                      type="file"
                      accept=".txt"
                      onChange={uploadPrompt}
                      className="hidden"
                    />
                  </label>
                </div>
              </div>
            </div>
          </div>

          {/* Preview Panel */}
          {showPreview && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200">
              <div className="border-b border-gray-200 p-4">
                <h2 className="text-lg font-semibold text-gray-900">Preview</h2>
                <p className="text-sm text-gray-600 mt-1">
                  See how your prompt will appear to the AI
                </p>
              </div>
              
              <div className="p-4">
                <div className="bg-gray-50 rounded-lg p-4 h-96 overflow-y-auto">
                  <pre className="whitespace-pre-wrap text-sm text-gray-800 font-mono">
                    {prompt || 'No prompt content to preview...'}
                  </pre>
                </div>
              </div>

              {/* Prompt Info */}
              <div className="border-t border-gray-200 p-4 bg-gray-50 rounded-b-lg">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">Character count:</span>
                    <span className="ml-2 font-medium text-gray-900">{prompt.length}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Word count:</span>
                    <span className="ml-2 font-medium text-gray-900">{prompt.split(/\s+/).filter(word => word.length > 0).length}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Line count:</span>
                    <span className="ml-2 font-medium text-gray-900">{prompt.split('\n').length}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Status:</span>
                    <span className={`ml-2 font-medium ${hasChanges ? 'text-yellow-600' : 'text-green-600'}`}>
                      {hasChanges ? 'Modified' : 'Saved'}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Instructions */}
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">Quick Tips</h3>
          <ul className="space-y-2 text-blue-800">
            <li className="flex items-start gap-2">
              <span className="text-blue-600 mt-1">•</span>
              <span>Be specific about the AI's personality, tone, and response style</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-600 mt-1">•</span>
              <span>Include examples of desired responses for better consistency</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-600 mt-1">•</span>
              <span>Test changes by having a conversation after saving</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-600 mt-1">•</span>
              <span>Export backups before making major changes</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
