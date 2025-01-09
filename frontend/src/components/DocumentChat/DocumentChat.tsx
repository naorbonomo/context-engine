import { useState } from 'react';
import { Message } from '../../types/chat';
import { useMutation } from '@tanstack/react-query';
import { documentChatService } from '../../services/documentChatService';
import './DocumentChat.css';

/**
 * DocumentChat component that combines chat functionality with document context
 * Allows users to ask questions about their documents and receive AI-powered responses
 * based on document embeddings and natural language processing
 */
export function DocumentChat() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [relevantContexts, setRelevantContexts] = useState<string[]>([]); // Store retrieved contexts
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const chatMutation = useMutation({
        mutationFn: documentChatService.sendMessage,
        onMutate: () => setIsLoading(true),
        onSettled: () => setIsLoading(false),
        onSuccess: (response) => {
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: response.response,
                timestamp: new Date()
            }]);
            // Update relevant contexts from the response
            if (response.contexts) {
                setRelevantContexts(response.contexts);
            }
        },
        onError: (error) => {
            setError('Failed to get response. Please try again.');
            setTimeout(() => setError(null), 3000);
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
        chatMutation.mutate({
            messages: [...messages, newMessage],
            top_k: 5, // Number of relevant contexts to retrieve
        });
        setInput('');
    };

    return (
        <div className="chat-window">
            <div className="messages-container">
                {messages.length === 0 ? (
                    <div className="welcome-message">
                        <h1>Document Assistant</h1>
                        <p>Ask questions about your documents and get AI-powered answers</p>
                    </div>
                ) : (
                    <>
                        {messages.map((msg, index) => (
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
                                {msg.role === 'assistant' && relevantContexts.length > 0 && (
                                    <div className="context-references">
                                        <h4>Referenced from:</h4>
                                        {relevantContexts.map((context, idx) => (
                                            <div key={idx} className="context-item">
                                                {context}
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        ))}
                        {isLoading && (
                            <div className="message-box assistant loading">
                                <div className="loading-indicator">Thinking...</div>
                            </div>
                        )}
                        {error && <div className="error-message">{error}</div>}
                    </>
                )}
            </div>

            <div className="input-wrapper">
                <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask about your documents..."
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
                    {chatMutation.isPending ? 'Processing...' : 'Send'}
                </button>
            </div>
        </div>
    );
} 