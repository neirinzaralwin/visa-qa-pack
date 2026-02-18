import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export interface ChatMessage {
  role: 'client' | 'consultant';
  message: string;
}

export interface GenerateReplyRequest {
  clientSequence: string;
  chatHistory: ChatMessage[];
}

export interface GenerateReplyResponse {
  aiReply: string;
}

export interface ImproveAIRequest {
  clientSequence: string;
  chatHistory: ChatMessage[];
  consultantReply: string;
}

export interface ImproveAIResponse {
  predictedReply: string;
  updatedPrompt: string;
}

export interface ImproveAIManuallyRequest {
  instructions: string;
}

export interface ImproveAIManuallyResponse {
  updatedPrompt: string;
}

export interface GetPromptResponse {
  prompt: string;
}

export interface UpdatePromptRequest {
  prompt: string;
}

export interface UpdatePromptResponse {
  message: string;
  prompt: string;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const aiAssistantApi = {
  generateReply: async (data: GenerateReplyRequest): Promise<GenerateReplyResponse> => {
    const response = await api.post('/generate-reply', data);
    return response.data;
  },

  improveAI: async (data: ImproveAIRequest): Promise<ImproveAIResponse> => {
    const response = await api.post('/improve-ai', data);
    return response.data;
  },

  improveAIManually: async (data: ImproveAIManuallyRequest): Promise<ImproveAIManuallyResponse> => {
    const response = await api.post('/improve-ai-manually', data);
    return response.data;
  },

  getPrompt: async (): Promise<GetPromptResponse> => {
    const response = await api.get('/prompt');
    return response.data;
  },

  updatePrompt: async (data: UpdatePromptRequest): Promise<UpdatePromptResponse> => {
    const response = await api.put('/prompt', data);
    return response.data;
  },
};
