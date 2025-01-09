import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ChatWindow } from './components/Chat/ChatWindow';
import { UploadWindow } from './components/Database/UploadWindow';
import { SearchWindow } from './components/Database/SearchWindow';
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
                    <Route path="/upload" element={<UploadWindow />} />
                    <Route path="/search" element={<SearchWindow />} />
                    <Route path="/" element={<Navigate to="/chat" replace />} />
                </Routes>
            </QueryClientProvider>
        </BrowserRouter>
    );
}

export default App;
