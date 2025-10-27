import type { ApiResponse, EmailListData, FullEmail, AuthStatus } from '@/types';

const API_BASE = 'http://localhost:8080/api';
const AUTH_BASE = 'http://localhost:8080/auth';

export class ApiService {
  
    static async checkAuthStatus(): Promise<AuthStatus> {
        try {
            const response = await fetch(`${API_BASE}/auth/status`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Auth check failed:', error);
            // Return not authenticated on error
            return {
                authenticated: false,
                message: 'Failed to check authentication'
            };
        }

    }

    static startAuth(): void {
        window.location.href = `${AUTH_BASE}/start`;
    }

    static async logout(): Promise<{ success: boolean; message: string }> {
        try {
            const response = await fetch(`${API_BASE}/auth/logout`, {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Logout failed:', error);
            throw error;
        }
    }

    static async listEmails(
        maxResults: number = 20,
        query: string = ''
    ): Promise<ApiResponse<EmailListData>> {
        try {
        const response = await fetch(`${API_BASE}/emails/list`, {
            method: 'POST',
            headers: { 
            'Content-Type': 'application/json' 
            },
            body: JSON.stringify({ 
            max_results: maxResults, 
            query 
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        
        // If the response is a string (from MCP), parse it
        if (typeof data === 'string') {
            return JSON.parse(data);
        }
        
        return data;
        } catch (error) {
        console.error('List emails failed:', error);
        throw error;
        }
    }

    static async readEmail(emailId: string): Promise<ApiResponse<FullEmail>> {
        try {
        const response = await fetch(`${API_BASE}/emails/read`, {
            method: 'POST',
            headers: { 
            'Content-Type': 'application/json' 
            },
            body: JSON.stringify({ 
            email_id: emailId 
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        
        // If the response is a string (from MCP), parse it
        if (typeof data === 'string') {
            return JSON.parse(data);
        }
        
        return data;
        } catch (error) {
        console.error('Read email failed:', error);
        throw error;
        }
    }

    static async sendEmail(
        to: string,
        subject: string,
        body: string
    ): Promise<ApiResponse<string>> {
        try {
        const response = await fetch(`${API_BASE}/emails/send`, {
            method: 'POST',
            headers: { 
            'Content-Type': 'application/json' 
            },
            body: JSON.stringify({ 
            to, 
            subject, 
            body 
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        
        if (typeof data === 'string') {
            return JSON.parse(data);
        }
        
        return data;
        } catch (error) {
        console.error('Send email failed:', error);
        throw error;
        }
    }
    
    static async sendChatMessage(message: string): Promise<{response: string, error?: string}> {
        try {
            const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
            });

            if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Chat failed:', error);
            return {
            response: '',
            error: String(error)
            };
        }
    }
}
