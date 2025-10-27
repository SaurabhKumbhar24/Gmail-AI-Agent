
import { useEffect, useState } from 'react';
import { ApiService } from '@/services/api';
import type { AuthStatus } from '@/types';
import { Button } from '@/components/ui/button';
import { Mail, Loader2 } from 'lucide-react';

interface AuthGuardProps {
  children: React.ReactNode;
}

export function AuthGuard({ children }: AuthGuardProps) {
    const [authStatus, setAuthStatus] = useState<AuthStatus | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        checkAuth();
    }, []);


    const checkAuth = async () => {
        try {
        const status = await ApiService.checkAuthStatus();
        setAuthStatus(status);
        } catch (error) {
        console.error('Auth check failed:', error);
        setAuthStatus({
            authenticated: false,
            message: 'Failed to check authentication'
        });
        } finally {
        setLoading(false);
        }
    };

    const handleLogin = () => {
        ApiService.startAuth();
    };

  
    if (loading) {
        return (
        <div className="flex items-center justify-center min-h-screen bg-gray-50">
            <div className="text-center">
            <Loader2 className="w-12 h-12 animate-spin text-black mx-auto" />
            <p className="mt-4 text-gray-600">Checking authentication...</p>
            </div>
        </div>
        );
    }

    if (!authStatus?.authenticated) {
        return (
        <div className="flex items-center justify-center min-h-screen bg-gray-50">
            <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-200 max-w-md w-full mx-4">
            <div className="text-center">
                <div className="mb-6 flex justify-center">
                <div className="bg-black p-4 rounded-full">
                    <Mail className="w-12 h-12 text-white" />
                </div>
                </div>

                <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Gmail AI Agent
                </h1>

                <p className="text-gray-600 mb-8">
                Connect your Gmail account to get started with AI-powered email management
                </p>

                <Button
                    onClick={handleLogin}
                    size="lg"
                    className="w-full bg-black hover:bg-gray-800 text-white font-semibold py-6 rounded-lg transition duration-200 flex items-center justify-center gap-3"
                    >
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                        <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                        <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                        <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                    </svg>
                    Sign in with Google
                </Button>

                <p className="mt-6 text-xs text-gray-500">
                We'll never share your data. Your emails stay private.
                </p>
            </div>
            </div>
        </div>
        );
    }

    return <>{children}</>;
}