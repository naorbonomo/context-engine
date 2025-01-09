import { api } from "./api";
import { Message } from "../types/chat";

interface ChatRequest {
    messages: Message[];
    top_k?: number;
}

interface ChatResponse {
    response: string;
    contexts?: string[];
}

export const documentChatService = {
    sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
        try {
            const response = await api.post<ChatResponse>('/document-chat', request);
            return response.data;
        } catch (error) {
            console.error('Error in document chat service:', error);
            throw error;
        }
    },

    searchDocuments: async (query: string, top_k: number = 5) => {
        try {
            const response = await api.post('/ollama-embeddings/search', {
                query,
                top_k
            });
            return response.data;
        } catch (error) {
            console.error('Error in document search:', error);
            throw error;
        }
    }
}; 