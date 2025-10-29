import { useState, useRef } from 'react';
import { Message } from '../../types/chat';
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
    const [currentStreamingMessage, setCurrentStreamingMessage] = useState<string>('');
    const [currentProvider, setCurrentProvider] = useState<string>('');
    const [isThinking, setIsThinking] = useState(false);
    const [thinkingContent, setThinkingContent] = useState<string>('');
    const [useEventSource, setUseEventSource] = useState(false); // Toggle between methods
    const abortControllerRef = useRef<AbortController | null>(null);
    const eventSourceCleanupRef = useRef<(() => void) | null>(null);

    // Function to parse and handle thinking content
    const handleStreamingContent = (content: string) => {
        if (content.includes('<think>')) {
            setIsThinking(true);
            // Extract content after <think> tag
            const thinkStart = content.indexOf('<think>') + 7;
            const remainingContent = content.substring(thinkStart);
            setThinkingContent(prev => prev + remainingContent);
        } else if (content.includes('</think>')) {
            setIsThinking(false);
            // Extract content before </think> tag
            const thinkEnd = content.indexOf('</think>');
            const beforeThinkEnd = content.substring(0, thinkEnd);
            setThinkingContent(prev => prev + beforeThinkEnd);
            // Clear thinking content and add to streaming message
            setCurrentStreamingMessage(prev => prev + thinkingContent + beforeThinkEnd);
            setThinkingContent('');
        } else if (isThinking) {
            // Add to thinking content
            setThinkingContent(prev => prev + content);
        } else {
            // Add to regular streaming message
            setCurrentStreamingMessage(prev => prev + content);
        }
    };

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const newMessage: Message = {
            role: 'user',
            content: input.trim(),
            timestamp: new Date()
        };

        setMessages(prev => [...prev, newMessage]);
        setInput('');
        setIsLoading(true);
        setError(null);
        setCurrentStreamingMessage('');
        setCurrentProvider('');
        setIsThinking(false);
        setThinkingContent('');

        const streamingRequest = {
            messages: [...messages, newMessage],
            top_k: 5, // Number of relevant contexts to retrieve
        };

        try {
            if (useEventSource) {
                // Use EventSource approach
                const cleanup = documentChatService.sendStreamingMessageWithEventSource(
                    streamingRequest,
                    // onToken callback
                    (token: string) => {
                        if (token && token.trim()) {
                            handleStreamingContent(token);
                        }
                    },
                    // onContext callback
                    (contexts: string[], provider: string) => {
                        setRelevantContexts(contexts);
                        setCurrentProvider(provider);
                    },
                    // onComplete callback
                    () => {
                        if (currentStreamingMessage.trim()) {
                            setMessages(prev => [...prev, {
                                role: 'assistant',
                                content: currentStreamingMessage,
                                timestamp: new Date()
                            }]);
                        }
                        setCurrentStreamingMessage('');
                        setIsLoading(false);
                        setIsThinking(false);
                        setThinkingContent('');
                    },
                    // onError callback
                    (errorMessage: string) => {
                        setError(errorMessage);
                        setIsLoading(false);
                        setCurrentStreamingMessage('');
                        setIsThinking(false);
                        setThinkingContent('');
                    }
                );
                
                eventSourceCleanupRef.current = cleanup;
            } else {
                // Use fetch approach
                abortControllerRef.current = new AbortController();

                await documentChatService.sendStreamingMessage(
                    streamingRequest,
                    // onToken callback
                    (token: string) => {
                        if (token && token.trim()) {
                            handleStreamingContent(token);
                        }
                    },
                    // onContext callback
                    (contexts: string[], provider: string) => {
                        setRelevantContexts(contexts);
                        setCurrentProvider(provider);
                    },
                    // onComplete callback
                    () => {
                        if (currentStreamingMessage.trim()) {
                            setMessages(prev => [...prev, {
                                role: 'assistant',
                                content: currentStreamingMessage,
                                timestamp: new Date()
                            }]);
                        }
                        setCurrentStreamingMessage('');
                        setIsLoading(false);
                        setIsThinking(false);
                        setThinkingContent('');
                    },
                    // onError callback
                    (errorMessage: string) => {
                        setError(errorMessage);
                        setIsLoading(false);
                        setCurrentStreamingMessage('');
                        setIsThinking(false);
                        setThinkingContent('');
                    }
                );
            }
        } catch (error) {
            setError('Failed to get response. Please try again.');
            setIsLoading(false);
            setCurrentStreamingMessage('');
            setIsThinking(false);
            setThinkingContent('');
        }
    };

    const handleCancel = () => {
        if (useEventSource && eventSourceCleanupRef.current) {
            eventSourceCleanupRef.current();
            eventSourceCleanupRef.current = null;
        } else if (abortControllerRef.current) {
            abortControllerRef.current.abort();
        }
        setIsLoading(false);
        setCurrentStreamingMessage('');
        setIsThinking(false);
        setThinkingContent('');
    };

    return (
        <div className="chat-window">
            <div className="chat-header">
                <h1>Document Assistant</h1>
                <div className="streaming-toggle">
                    <label>
                        <input
                            type="checkbox"
                            checked={useEventSource}
                            onChange={(e) => setUseEventSource(e.target.checked)}
                            disabled={isLoading}
                        />
                        Use EventSource (simpler method)
                    </label>
                </div>
            </div>
            
            <div className="messages-container">
                {messages.length === 0 && !isLoading ? (
                    <div className="welcome-message">
                        <p>Ask questions about your documents and get AI-powered answers</p>
                        <p className="method-info">
                            Currently using: <strong>{useEventSource ? 'EventSource' : 'Fetch'}</strong> streaming
                        </p>
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
                                    {msg.role === 'assistant' && currentProvider && (
                                        <span className="provider-badge">({currentProvider})</span>
                                    )}
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
                        
                        {/* Show streaming message */}
                        {isLoading && (currentStreamingMessage || thinkingContent) && (
                            <div className="message-box assistant streaming">
                                <div className="message-header">
                                    Assistant
                                    {currentProvider && (
                                        <span className="provider-badge">({currentProvider})</span>
                                    )}
                                </div>
                                
                                {/* Show thinking content if available */}
                                {thinkingContent && (
                                    <div className="thinking-content">
                                        <div className="thinking-header">
                                            <span className="thinking-icon">🧠</span>
                                            <span>Thinking Process</span>
                                        </div>
                                        <div className="thinking-text">
                                            {thinkingContent}
                                            {isThinking && <span className="cursor">|</span>}
                                        </div>
                                    </div>
                                )}
                                
                                {/* Show streaming response */}
                                {currentStreamingMessage && (
                                    <div className="message-text">
                                        {currentStreamingMessage}
                                        {!isThinking && <span className="cursor">|</span>}
                                    </div>
                                )}
                                
                                {relevantContexts.length > 0 && (
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
                        )}
                        
                        {isLoading && !currentStreamingMessage && !thinkingContent && (
                            <div className="message-box assistant loading">
                                <div className="loading-indicator">Processing...</div>
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
                    disabled={isLoading}
                />
                {isLoading ? (
                    <button 
                        onClick={handleCancel}
                        className="cancel-button"
                    >
                        Cancel
                    </button>
                ) : (
                    <button 
                        onClick={handleSend}
                        disabled={!input.trim()}
                        className="send-button"
                    >
                        Send
                    </button>
                )}
            </div>
        </div>
    );
} 