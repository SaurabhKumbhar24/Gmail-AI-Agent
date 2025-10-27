import { useState } from 'react';
import { AuthGuard } from '@/components/AuthGuard';
import { EmailList } from '@/components/EmailList';
import { EmailView } from '@/components/EmailView';
import { ChatInterface } from '@/components/ChatInterface';
import { Button } from './components/ui/button';
import { ApiService } from '@/services/api';
import { LogOut } from 'lucide-react';

function App() {
  const [selectedEmailId, setSelectedEmailId] = useState<string | null>(null);
  const [view, setView] = useState<'chat' | 'email'>('chat');

  const handleLogout = async () => {
    try {
      await ApiService.logout();
      window.location.reload();
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <AuthGuard>
      <div className="h-screen flex flex-col">
        {/* Header */}
        <header className="text-black p-4 shadow-lg">
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-light">Gmail AI Agent</h1>

            {/* View toggle and logout */}
            <div className="flex gap-2 items-center">
              <Button
                onClick={() => setView('chat')}
                className='px-4 py-2 rounded-lg cursor-pointer'
                variant={ view === 'chat' ? 'default' : 'ghost'}
              >
                Chat
              </Button>
              <Button
                onClick={() => setView('email')}
                className='px-4 py-2 rounded-lg cursor-pointer'
                variant={ view === 'email' ? 'default' : 'ghost'}
              >
                Emails
              </Button>
              <Button
                onClick={handleLogout}
                variant="ghost"
                size="icon"
                className="ml-2"
                title="Logout"
              >
                <LogOut className="w-5 h-5" />
              </Button>
            </div>
          </div>
        </header>

        {/* Main content */}
        <div className="flex-1 flex w-full overflow-hidden">
          {view === 'chat' ? (
            <ChatInterface />
          ) : (
            <>
              {/* Email list sidebar */}
              <div className="w-80 hidden md:block">
                <EmailList
                  onSelectEmail={setSelectedEmailId}
                  selectedEmailId={selectedEmailId}
                />
              </div>

              {/* Email view */}
              <div className="flex-1">
                <EmailView
                  emailId={selectedEmailId}
                  onBack={() => setSelectedEmailId(null)}
                />
              </div>
            </>
          )}
        </div>
      </div>
    </AuthGuard>
  );
}

export default App;