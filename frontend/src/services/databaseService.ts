import { api } from './api';

interface DocumentUpload {
    title: string;
    content: string;
}

interface SearchRequest {
    query: string;
    top_k?: number;
}

interface PDFUploadRequest {
    file: File;
    chunkSize?: number;
    overlap?: number;
}

interface PDFUploadResponse {
    success: boolean;
    message: string;
    chunks_processed: number;
    total_pages: number;
}

interface Document {
    id: string; // Assuming each document has a unique ID
    content: string;
}

export const databaseService = {
    uploadDocument: async ({ title, content }: DocumentUpload) => {
        const response = await api.post('/ollama-embeddings/embed', {
            contents: [content], // API expects array of strings
        });
        return response.data;
    },

    uploadPDF: async ({ file, chunkSize = 1000, overlap = 200 }: PDFUploadRequest): Promise<PDFUploadResponse> => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('chunk_size', chunkSize.toString());
        formData.append('overlap', overlap.toString());

        const response = await api.post('/documents/upload-pdf', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
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

    /**
     * Fetches all documents from the backend.
     * @returns A promise that resolves to an array of documents.
     */
    async listDocuments(): Promise<Document[]> { // Add return type
        try {
            const response = await api.get('/documents'); // Replace with your actual endpoint
            return response.data; // Return the data
        } catch (error) {
            console.error('Error fetching documents:', error); // Log the error
            throw error; // Propagate the error
        }
    }, // End of listDocuments
}; 