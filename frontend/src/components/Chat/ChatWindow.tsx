import { useState, useCallback } from 'react';
import { Message } from '../../types/chat';
import { useMutation } from '@tanstack/react-query';
import { chatService } from '../../services/chatService';
import './ChatWindow.css';

export function ChatWindow() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [suggestion, setSuggestion] = useState('');

    const chatMutation = useMutation({
        mutationFn: chatService.sendMessage,
        onSuccess: (response) => {
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: response.response,
                timestamp: new Date()
            }]);
        },
    });

    const autocompleteMutation = useMutation({
        mutationFn: chatService.getAutocomplete,
        onSuccess: (response) => {
            console.log('Autocomplete response:', response);
            setSuggestion(response.suggestion || '');
        },
    });

    const handleAutocomplete = useCallback((text: string) => {
        if (text.endsWith(' ')) {
            console.log('Triggering autocomplete for:', text);
            autocompleteMutation.mutate(text);
        } else {
            setSuggestion('');
        }
    }, []);

    const adjustTextAreaHeight = (textarea: HTMLTextAreaElement) => {
        textarea.style.height = 'auto';
        textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        const newValue = e.target.value;
        setInput(newValue);
        handleAutocomplete(newValue);
        adjustTextAreaHeight(e.target);
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Tab' && suggestion) {
            e.preventDefault();
            setInput(prev => prev + suggestion);
            setSuggestion('');
        } else if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const handleSend = () => {
        if (!input.trim()) return;

        const newMessage: Message = {
            role: 'user',
            content: input.trim(),
            timestamp: new Date()
        };

        setMessages(prev => [...prev, newMessage]);
        chatMutation.mutate([...messages, newMessage]);
        setInput('');
        setSuggestion('');
    };

    const formatSuggestionDisplay = () => {
        return (
            <div className="suggestions-above">
                <div className="suggestion-item">
                    <span className="suggestion-text">Tab to complete: </span>
                    <span className="suggestion-value">{suggestion}</span>
                </div>
            </div>
        );
    };

    return (
        <div className="chat-window">
            <div className="messages-container">
                {messages.length === 0 ? (
                    <div className="welcome-message">
                        <h1>Welcome to Context Engine</h1>
                        <p>Your AI-powered knowledge assistant</p>
                    </div>
                ) : (
                    messages.map((msg, index) => (
                        <div 
                            key={index}
                            className={`message-box ${msg.role}`}
                        >
                            <div className="message-header">
                                {msg.role === 'user' ? 'You' : 'Assistant'}
                            </div>
                            <div className="message-text">
                                {msg.content}
                            </div>
                        </div>
                    ))
                )}
            </div>

            <div className="input-wrapper">
                {suggestion && formatSuggestionDisplay()}
                <div className="input-container">
                    <textarea
                        value={input}
                        onChange={handleInputChange}
                        onKeyDown={handleKeyDown}
                        placeholder="Message Context Engine..."
                        rows={1}
                        className="message-input"
                    />
                </div>
                <button 
                    onClick={handleSend}
                    disabled={chatMutation.isPending}
                    className="send-button"
                >
                    {chatMutation.isPending ? 'Sending...' : 'Send'}
                </button>
            </div>
        </div>
    );
} 