import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { databaseService } from '../../services/databaseService';
import './DatabaseWindow.css';

export function UploadWindow() {
    const [content, setContent] = useState('');
    const [title, setTitle] = useState('');

    const uploadMutation = useMutation({
        mutationFn: databaseService.uploadDocument,
        onSuccess: () => {
            setContent('');
            setTitle('');
        },
    });

    const handleUpload = () => {
        if (!content.trim() || !title.trim()) return;

        uploadMutation.mutate({
            title: title.trim(),
            content: content.trim(),
        });
    };

    return (
        <div className="database-window">
            <div className="database-content">
                <h1>Upload Documents</h1>
                <p className="description">Upload documents to enhance your AI's knowledge base</p>

                <div className="input-group">
                    <input
                        type="text"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        placeholder="Document Title..."
                        className="title-input"
                    />
                </div>

                <div className="input-group">
                    <textarea
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        placeholder="Paste your document content here..."
                        className="content-input"
                        rows={10}
                    />
                </div>

                <button 
                    onClick={handleUpload}
                    disabled={uploadMutation.isPending || !content.trim() || !title.trim()}
                    className="upload-button"
                >
                    {uploadMutation.isPending ? 'Uploading...' : 'Upload Document'}
                </button>

                {uploadMutation.isSuccess && (
                    <div className="success-message">Document uploaded successfully!</div>
                )}

                {uploadMutation.isError && (
                    <div className="error-message">Failed to upload document. Please try again.</div>
                )}
            </div>
        </div>
    );
} 