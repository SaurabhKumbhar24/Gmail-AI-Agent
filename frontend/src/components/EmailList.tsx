import { useEffect, useState } from 'react';
import { ApiService } from '@/services/api';
import type { Email } from '@/types';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Search, Loader2, Mail, RefreshCw } from 'lucide-react';
import { ScrollArea } from '@/components/ui/scroll-area';

interface EmailListProps {
  onSelectEmail: (emailId: string) => void;
  selectedEmailId: string | null;
}

export function EmailList({ onSelectEmail, selectedEmailId }: EmailListProps) {
  const [emails, setEmails] = useState<Email[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchEmails();
  }, [searchQuery]);

  
  const fetchEmails = async () => {
    setLoading(true);
    try {
      const response = await ApiService.listEmails(50, searchQuery);
      
      if (response.status === 200 && response.data) {
        setEmails(response.data.messages);
      }
    } catch (error) {
      console.error('Failed to fetch emails:', error);
    } finally {
      setLoading(false);
    }
  };

  
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setSearchQuery(query);
  };

  
  const formatSender = (from: string) => {
    const match = from.match(/^(.*?)\s*<.*>$/);
    return match ? match[1].replace(/"/g, '') : from;
  };

  
  const truncateSubject = (subject: string, maxLength: number = 40) => {
    if (subject.length <= maxLength) return subject;
    return subject.substring(0, maxLength) + '...';
  };

  return (
    <div className="flex flex-col h-full border-r bg-gray-50">
      {/* Header */}
      <div className="p-4 border-b bg-white shrink-0">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
            <Mail className="w-5 h-5" />
            Inbox
          </h2>
          <Button
            variant="ghost"
            size="sm"
            onClick={fetchEmails}
            disabled={loading}
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>

        {/* Search bar */}
        <form onSubmit={handleSearch} className="flex gap-2">
          <Input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search emails..."
            className="flex-1"
          />
          <Button type="submit" size="sm">
            <Search className="w-4 h-4" />
          </Button>
        </form>

        <p className="text-xs text-gray-500 mt-2">
          Try: is:unread, from:user@example.com
        </p>
      </div>

      {/* Email list */}
      <div className="flex-1 overflow-hidden">
        <ScrollArea className="h-full">
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <Loader2 className="w-8 h-8 animate-spin text-gray-600" />
            </div>
          ) : emails.length === 0 ? (
            <div className="text-center py-12 px-4">
              <Mail className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500">No emails found</p>
            </div>
          ) : (
            <div className="divide-y">
              {emails.map((email) => (
                <div
                  key={email.id}
                  onClick={() => onSelectEmail(email.id)}
                  className={`p-4 cursor-pointer transition hover:bg-gray-100 ${
                    selectedEmailId === email.id ? 'bg-gray-200 border-l-4 border-black' : ''
                  }`}
                >
                  <div className="flex justify-between items-start mb-1">
                    <p className="font-semibold text-sm text-gray-900 truncate flex-1">
                      {formatSender(email.from)}
                    </p>
                    <span className="text-xs text-gray-500 ml-2 whitespace-nowrap">
                      {new Date(email.date).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="text-sm text-gray-700 truncate">
                    {truncateSubject(email.subject || '(No subject)')}
                  </p>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>
      </div>
    </div>
  );
}
