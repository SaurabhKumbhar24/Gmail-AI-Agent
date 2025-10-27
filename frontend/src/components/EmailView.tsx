import { useEffect, useState } from 'react';
import { ApiService } from '@/services/api';
import type { FullEmail } from '@/types';
import { Button } from '@/components/ui/button';
import { Loader2, Mail, ArrowLeft } from 'lucide-react';
import { ScrollArea } from '@/components/ui/scroll-area';

interface EmailViewProps {
  emailId: string | null;
  onBack: () => void;
}

export function EmailView({ emailId, onBack }: EmailViewProps) {
    const [email, setEmail] = useState<FullEmail | null>(null);
    const [loading, setLoading] = useState(false);

    
    useEffect(() => {
        if (emailId) {
        fetchEmail(emailId);
        }
    }, [emailId]);

    
    const fetchEmail = async (id: string) => {
        setLoading(true);
        try {
        
        const response = await ApiService.readEmail(id);
        
        if (response.status === 200 && response.data) {
            setEmail(response.data as FullEmail);
        }
        } catch (error) {
        console.error('Failed to fetch email:', error);
        } finally {
        setLoading(false);
        }
    };

    if (!emailId) {
        return (
        <div className="flex items-center justify-center h-full bg-gray-50">
            <div className="text-center text-gray-400">
            <Mail className="w-16 h-16 mx-auto mb-4" />
            <p className="text-lg">Select an email to view</p>
            </div>
        </div>
        );
    }

    if (loading) {
        return (
        <div className="flex items-center justify-center h-full">
            <Loader2 className="w-8 h-8 animate-spin text-gray-600" />
        </div>
        );
    }

    if (!email) {
        return (
        <div className="flex items-center justify-center h-full">
            <p className="text-gray-500">Failed to load email</p>
        </div>
        );
    }

    return (
        <div className="flex flex-col h-full bg-white">
        {/* Header */}
        <div className="p-6 border-b shrink-0">
            <Button
                variant="ghost"
                size="sm"
                onClick={onBack}
                className="mb-4 md:hidden"
            >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
            </Button>

            <h1 className="text-2xl font-bold text-gray-900 mb-4">
            {email.subject || '(No subject)'}
            </h1>

            <div className="space-y-2 text-sm">
            <div className="flex">
                <span className="font-semibold text-gray-600 w-16">From:</span>
                <span className="text-gray-900">{email.from}</span>
            </div>
            {email.to && (
                <div className="flex">
                <span className="font-semibold text-gray-600 w-16">To:</span>
                <span className="text-gray-900">{email.to}</span>
                </div>
            )}
            <div className="flex">
                <span className="font-semibold text-gray-600 w-16">Date:</span>
                <span className="text-gray-900">
                {new Date(email.date).toLocaleString()}
                </span>
            </div>
            </div>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-hidden">
            <ScrollArea className="h-full">
                <div className="p-6 prose max-w-none">
                <pre className="whitespace-pre-wrap font-sans text-gray-800">
                    {email.body}
                </pre>
                </div>
            </ScrollArea>
        </div>
        </div>
    );
}