import { api } from './api';
import { Message, ChatResponse, AutocompleteResponse } from '../types/chat';

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

    async getAutocomplete(partial_prompt: string): Promise<AutocompleteResponse> {
        console.log('Sending autocomplete request:', partial_prompt);
        const response = await api.post('/autocomplete', {
            partial_prompt,
            max_tokens: 20
        });
        console.log('Received autocomplete response:', response.data);
        return response.data;
    },
}; 