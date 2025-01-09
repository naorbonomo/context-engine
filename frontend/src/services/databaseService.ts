import { api } from './api';

interface DocumentUpload {
    title: string;
    content: string;
}

interface SearchRequest {
    query: string;
    top_k?: number;
}

export const databaseService = {
    uploadDocument: async ({ title, content }: DocumentUpload) => {
        const response = await api.post('/ollama-embeddings/embed', {
            contents: [content], // API expects array of strings
        });
        return response.data;
    },

    searchDocuments: async ({ query, top_k = 2 }: SearchRequest) => {
        const response = await api.post('/ollama-embeddings/search', {
            query,
            top_k,
        });
        return response.data;
    },
}; 