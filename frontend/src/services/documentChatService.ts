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

interface StreamingChatRequest {
    messages: Message[];
    top_k?: number;
    model?: string;
    provider?: string;
}

interface StreamingEvent {
    type: 'context' | 'token' | 'done' | 'error';
    content?: string;
    contexts?: string[];
    provider?: string;
    error?: string;
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

    sendStreamingMessage: async (
        request: StreamingChatRequest,
        onToken: (token: string) => void,
        onContext: (contexts: string[], provider: string) => void,
        onComplete: () => void,
        onError: (error: string) => void
    ): Promise<void> => {
        try {
            const response = await fetch(`${api.defaults.baseURL}/document-chat/stream`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(request),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const reader = response.body?.getReader();
            if (!reader) {
                throw new Error('No response body reader available');
            }

            const decoder = new TextDecoder();
            let buffer = '';

            while (true) {
                const { done, value } = await reader.read();
                
                if (done) {
                    break;
                }

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop() || ''; // Keep incomplete line in buffer

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6); // Remove 'data: ' prefix
                        
                        if (data === '[DONE]') {
                            onComplete();
                            return;
                        }

                        try {
                            const parsed = JSON.parse(data) as StreamingEvent;
                            
                            switch (parsed.type) {
                                case 'context':
                                    if (parsed.contexts && parsed.provider) {
                                        onContext(parsed.contexts, parsed.provider);
                                    }
                                    break;
                                case 'token':
                                    if (parsed.content) {
                                        onToken(parsed.content);
                                    }
                                    break;
                                case 'done':
                                    onComplete();
                                    return;
                                case 'error':
                                    if (parsed.error) {
                                        onError(parsed.error);
                                    }
                                    return;
                            }
                        } catch (parseError) {
                            console.error('Error parsing SSE data:', parseError);
                            // Continue processing other lines
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Error in streaming document chat service:', error);
            onError(error instanceof Error ? error.message : 'Unknown error occurred');
        }
    },

    // Alternative EventSource-based streaming (simpler approach)
    sendStreamingMessageWithEventSource: (
        request: StreamingChatRequest,
        onToken: (token: string) => void,
        onContext: (contexts: string[], provider: string) => void,
        onComplete: () => void,
        onError: (error: string) => void
    ): (() => void) => {
        // Create URL with query parameters for GET request
        const params = new URLSearchParams({
            messages: JSON.stringify(request.messages),
            top_k: request.top_k?.toString() || '5',
            ...(request.model && { model: request.model }),
            ...(request.provider && { provider: request.provider }),
        });

        const eventSource = new EventSource(`${api.defaults.baseURL}/document-chat/stream?${params}`);

        eventSource.onmessage = (event) => {
            if (event.data === '[DONE]') {
                eventSource.close();
                onComplete();
                return;
            }

            try {
                const parsed = JSON.parse(event.data) as StreamingEvent;
                
                switch (parsed.type) {
                    case 'context':
                        if (parsed.contexts && parsed.provider) {
                            onContext(parsed.contexts, parsed.provider);
                        }
                        break;
                    case 'token':
                        if (parsed.content) {
                            onToken(parsed.content);
                        }
                        break;
                    case 'done':
                        eventSource.close();
                        onComplete();
                        return;
                    case 'error':
                        if (parsed.error) {
                            onError(parsed.error);
                        }
                        eventSource.close();
                        return;
                }
            } catch (parseError) {
                console.error('Error parsing EventSource data:', parseError);
            }
        };

        eventSource.onerror = (error) => {
            console.error('EventSource error:', error);
            eventSource.close();
            onError('Connection error occurred');
        };

        // Return cleanup function
        return () => {
            eventSource.close();
        };
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