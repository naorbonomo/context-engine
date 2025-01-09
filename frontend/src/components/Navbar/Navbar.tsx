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
                        to="/database" 
                        className={`nav-link ${location.pathname === '/database' ? 'active' : ''}`}
                    >
                        Database
                    </Link>
                </div>
            </div>
        </nav>
    );
} 