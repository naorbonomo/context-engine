import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

export function Navbar() {
    const location = useLocation();
    
    return (
        <nav className="navbar">
            <div className="nav-content">
                <div className="nav-brand">Context Engine</div>
                <div className="nav-links">
                    <Link 
                        to="/chat" 
                        className={`nav-link ${location.pathname === '/chat' ? 'active' : ''}`}
                    >
                        Chat
                    </Link>
                    <Link 
                        to="/upload" 
                        className={`nav-link ${location.pathname === '/upload' ? 'active' : ''}`}
                    >
                        Upload
                    </Link>
                    <Link 
                        to="/search" 
                        className={`nav-link ${location.pathname === '/search' ? 'active' : ''}`}
                    >
                        Search
                    </Link>
                    <Link 
                        to="/document-chat" 
                        className={`nav-link ${location.pathname === '/document-chat' ? 'active' : ''}`}
                    >
                        Document Chat
                    </Link>
                </div>
            </div>
        </nav>
    );
} 