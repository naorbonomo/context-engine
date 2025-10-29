import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { databaseService } from '../../services/databaseService';
import './DatabaseWindow.css';

export function UploadWindow() {
    const [content, setContent] = useState('');
    const [title, setTitle] = useState('');
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [uploadMode, setUploadMode] = useState<'text' | 'pdf'>('text');
    const [chunkSize, setChunkSize] = useState(1000);
    const [overlap, setOverlap] = useState(200);
    const [uploadProgress, setUploadProgress] = useState<string>('');

    const uploadTextMutation = useMutation({
        mutationFn: databaseService.uploadDocument,
        onSuccess: () => {
            setContent('');
            setTitle('');
            setUploadProgress('Text document uploaded successfully!');
        },
        onError: (error) => {
            setUploadProgress(`Error uploading text: ${error.message}`);
        }
    });

    const uploadPDFMutation = useMutation({
        mutationFn: databaseService.uploadPDF,
        onSuccess: (data) => {
            setSelectedFile(null);
            setUploadProgress(`PDF processed successfully! ${data.chunks_processed} chunks created.`);
        },
        onError: (error) => {
            setUploadProgress(`Error processing PDF: ${error.message}`);
        }
    });

    const handleTextUpload = () => {
        if (!content.trim() || !title.trim()) return;

        uploadTextMutation.mutate({
            title: title.trim(),
            content: content.trim(),
        });
    };

    const handlePDFUpload = () => {
        if (!selectedFile) return;

        uploadPDFMutation.mutate({
            file: selectedFile,
            chunkSize,
            overlap,
        });
    };

    const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file && file.type === 'application/pdf') {
            setSelectedFile(file);
            setUploadProgress(`Selected: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`);
        } else if (file) {
            setUploadProgress('Please select a PDF file.');
            setSelectedFile(null);
        }
    };

    return (
        <div className="database-window">
            <div className="database-content">
                <h1>Upload Documents</h1>
                <p className="description">Upload documents to enhance your AI's knowledge base</p>

                {/* Upload Mode Toggle */}
                <div className="upload-mode-toggle">
                    <button
                        className={`mode-button ${uploadMode === 'text' ? 'active' : ''}`}
                        onClick={() => setUploadMode('text')}
                    >
                        Text Upload
                    </button>
                    <button
                        className={`mode-button ${uploadMode === 'pdf' ? 'active' : ''}`}
                        onClick={() => setUploadMode('pdf')}
                    >
                        PDF Upload
                    </button>
                </div>

                {uploadMode === 'text' ? (
                    // Text Upload Section
                    <>
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
                            onClick={handleTextUpload}
                            disabled={uploadTextMutation.isPending || !content.trim() || !title.trim()}
                            className="upload-button"
                        >
                            {uploadTextMutation.isPending ? 'Uploading...' : 'Upload Document'}
                        </button>
                    </>
                ) : (
                    // PDF Upload Section
                    <>
                        <div className="input-group">
                            <label htmlFor="pdf-file" className="file-input-label">
                                Choose PDF File
                            </label>
                            <input
                                id="pdf-file"
                                type="file"
                                accept=".pdf"
                                onChange={handleFileSelect}
                                className="file-input"
                            />
                            {selectedFile && (
                                <div className="file-info">
                                    <p>Selected: {selectedFile.name}</p>
                                    <p>Size: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                                </div>
                            )}
                        </div>

                        <div className="pdf-options">
                            <div className="option-group">
                                <label htmlFor="chunk-size">Chunk Size (characters):</label>
                                <input
                                    id="chunk-size"
                                    type="number"
                                    value={chunkSize}
                                    onChange={(e) => setChunkSize(parseInt(e.target.value) || 1000)}
                                    min="500"
                                    max="2000"
                                    className="number-input"
                                />
                            </div>

                            <div className="option-group">
                                <label htmlFor="overlap">Overlap (characters):</label>
                                <input
                                    id="overlap"
                                    type="number"
                                    value={overlap}
                                    onChange={(e) => setOverlap(parseInt(e.target.value) || 200)}
                                    min="0"
                                    max="500"
                                    className="number-input"
                                />
                            </div>
                        </div>

                        <button 
                            onClick={handlePDFUpload}
                            disabled={uploadPDFMutation.isPending || !selectedFile}
                            className="upload-button"
                        >
                            {uploadPDFMutation.isPending ? 'Processing PDF...' : 'Upload & Process PDF'}
                        </button>
                    </>
                )}

                {/* Progress/Status Messages */}
                {uploadProgress && (
                    <div className={`progress-message ${uploadProgress.includes('Error') ? 'error' : 'success'}`}>
                        {uploadProgress}
                    </div>
                )}

                {uploadTextMutation.isSuccess && (
                    <div className="success-message">Text document uploaded successfully!</div>
                )}

                {uploadTextMutation.isError && (
                    <div className="error-message">Failed to upload text document. Please try again.</div>
                )}

                {uploadPDFMutation.isSuccess && (
                    <div className="success-message">PDF processed successfully!</div>
                )}

                {uploadPDFMutation.isError && (
                    <div className="error-message">Failed to process PDF. Please try again.</div>
                )}
            </div>
        </div>
    );
} 