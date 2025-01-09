export interface Message {
    role: 'user' | 'assistant' | 'system';
    content: string;
    timestamp?: Date;
}

export interface ChatResponse {
    message: string;
    model: string;
    timestamp: Date;
} 