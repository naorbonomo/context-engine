import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { databaseService } from '../../services/databaseService';
import './DatabaseWindow.css';

export function SearchWindow() {
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState<string[]>([]);

    const searchMutation = useMutation({
        mutationFn: databaseService.searchDocuments,
        onSuccess: (data) => {
            setSearchResults(data.contexts);
        },
    });

    const handleSearch = () => {
        if (!searchQuery.trim()) return;

        searchMutation.mutate({
            query: searchQuery.trim(),
            top_k: 5,
        });
    };

    return (
        <div className="database-window">
            <div className="database-content">
                <h1>Search Documents</h1>
                <p className="description">Search through your uploaded documents</p>

                <div className="search-container">
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="Enter your search query..."
                        className="search-input"
                    />
                    <button
                        onClick={handleSearch}
                        disabled={searchMutation.isPending || !searchQuery.trim()}
                        className="search-button"
                    >
                        {searchMutation.isPending ? 'Searching...' : 'Search'}
                    </button>
                </div>

                {searchMutation.isSuccess && searchResults.length > 0 && (
                    <div className="search-results">
                        <h3>Search Results:</h3>
                        {searchResults.map((result, index) => (
                            <div key={index} className="search-result-item">
                                {result}
                            </div>
                        ))}
                    </div>
                )}

                {searchMutation.isError && (
                    <div className="error-message">Failed to search documents. Please try again.</div>
                )}
            </div>
        </div>
    );
} 