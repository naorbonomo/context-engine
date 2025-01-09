import { api } from './api';
import { Message, ChatResponse } from '../types/chat';

export const chatService = {
    async sendMessage(messages: Message[]): Promise<ChatResponse> {
        const lastMessage = messages[messages.length - 1];
        
        const requestBody = {
            prompt: lastMessage.content,
            system_prompt: messages.find(m => m.role === 'system')?.content,
        };

        const response = await api.post('/chat', requestBody);
        return response.data;
    },
}; 