import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ChatWindow } from './components/Chat/ChatWindow';
import { DatabaseWindow } from './components/Database/DatabaseWindow';
import { Navbar } from './components/Navbar/Navbar';
import './styles/app.css';

const queryClient = new QueryClient();

function App() {
    return (
        <BrowserRouter>
            <QueryClientProvider client={queryClient}>
                <Navbar />
                <Routes>
                    <Route path="/chat" element={<ChatWindow />} />
                    <Route path="/database" element={<DatabaseWindow />} />
                    <Route path="/" element={<Navigate to="/chat" replace />} />
                </Routes>
            </QueryClientProvider>
        </BrowserRouter>
    );
}

export default App;
