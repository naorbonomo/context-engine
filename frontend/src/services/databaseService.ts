import { api } from './api';

interface Document {
    title: string;
    content: string;
}

export const databaseService = {
    async uploadDocument(document: Document) {
        const response = await api.post('/documents', document);
        return response.data;
    },
}; 