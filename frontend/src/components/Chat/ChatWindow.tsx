import { useState } from 'react';
import { Message } from '../../types/chat';
import { useMutation } from '@tanstack/react-query';
import { chatService } from '../../services/chatService';
import './ChatWindow.css';

export function ChatWindow() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');

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
                <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Message Context Engine..."
                    onKeyPress={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            handleSend();
                        }
                    }}
                    rows={1}
                    className="message-input"
                />
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