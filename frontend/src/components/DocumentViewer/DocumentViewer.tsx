import { useEffect, useState } from 'react'; // Import React hooks
import { databaseService } from '../../services/databaseService'; // Import the service
import './DocumentViewer.css'; // Import CSS for styling

interface Document {
    id: string;
    content: string;
}

export function DocumentViewer() {
    const [documents, setDocuments] = useState<Document[]>([]); // State to hold documents
    const [loading, setLoading] = useState<boolean>(true); // State for loading
    const [error, setError] = useState<string | null>(null); // State for error
    const [expandedDocs, setExpandedDocs] = useState<Set<string>>(new Set()); // State to track expanded documents

    useEffect(() => { // Fetch documents on component mount
        databaseService.listDocuments()
            .then((docs) => setDocuments(docs)) // Set fetched documents
            .catch((err) => setError('Failed to fetch documents.')) // Set error message
            .finally(() => setLoading(false)); // Set loading to false
    }, []); // Empty dependency array ensures this runs once

    const toggleExpand = (id: string) => { // Function to toggle document expansion
        setExpandedDocs(prev => {
            const newSet = new Set(prev);
            if (newSet.has(id)) {
                newSet.delete(id); // Collapse if already expanded
            } else {
                newSet.add(id); // Expand if collapsed
            }
            return newSet;
        });
    };

    if (loading) { // If data is loading
        return <div>Loading documents...</div>; // Display loading message
    }

    if (error) { // If there's an error
        return <div>{error}</div>; // Display error message
    }

    return ( // Render the list of documents
        <div className="document-viewer"> {/* Container for the viewer */}
            <h1>Documents</h1> {/* Header */}
            {documents.length === 0 ? ( // Check if there are documents
                <p>No documents found.</p> // Display message if none
            ) : (
                <ul className="document-list"> {/* List of documents */}
                    {documents.map((doc) => ( // Iterate over documents
                        <li key={doc.id} className="document-item" onClick={() => toggleExpand(doc.id)} style={{ cursor: 'pointer' }}> {/* Each document item with click handler */}
                            <h2>{doc.id}</h2> {/* Document ID */}
                            {expandedDocs.has(doc.id) ? ( // Check if document is expanded
                                <p>{doc.content}</p> // Display full content
                            ) : (
                                <p>{doc.content.substring(0, 200)}...</p> // Display truncated content for preview
                            )}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
} 