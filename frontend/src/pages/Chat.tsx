import { useRef, useState } from 'react';
import Navbar from '../components/Navbar';
import SessionList from '../components/SessionList';
import ChatMessage from '../components/ChatMessage';
import ChatInput from '../components/ChatInput';
import MemoryManager from '../components/MemoryManager';
import LoadingSpinner from '../components/LoadingSpinner';
import { useSession } from '../hooks/useSession';
import { useChat } from '../hooks/useChat';
import '../assets/styles/Chat.css';

const Chat = () => {
  const {
    sessions,
    activeSessionId,
    setActiveSessionId,
    isLoading: sessionsLoading,
    loadSessions
  } = useSession();

  const {
    messages,
    isLoading: chatLoading,
    error: chatError,
    sendChatMessage
  } = useChat(activeSessionId);

  const [showMemoryManager, setShowMemoryManager] = useState<boolean>(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const isLoading = sessionsLoading || chatLoading;
  const error = chatError || '';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const toggleMemoryManager = () => {
    setShowMemoryManager(prev => !prev);
  };

  return (
    <div className="chat-page">
      <Navbar />
      <div className={`chat-container ${showMemoryManager ? 'memory-manager-visible' : ''}`}>
        <div className="chat-sidebar">
          <SessionList
            sessions={sessions}
            activeSessionId={activeSessionId}
            onSelectSession={setActiveSessionId}
            onSessionsChange={loadSessions}
          />
          <button
            className="btn memory-toggle-btn"
            onClick={toggleMemoryManager}
          >
            {showMemoryManager ? 'Hide Memory Manager' : 'Show Memory Manager'}
          </button>
        </div>

        <div className="chat-main">
          {activeSessionId ? (
            <>
              <div className="chat-header pixel-border">
                <h2 className="chat-title">
                  {sessions.find(s => s.id === activeSessionId)?.name || 'Chat'}
                </h2>
              </div>

              <div className="chat-messages">
                {error && <div className="error-message">{error}</div>}
                {isLoading && messages.length === 0 && (
                  <div className="loading-container">
                    <LoadingSpinner size="large" color="primary" />
                  </div>
                )}
                {!isLoading && messages.length === 0 ? (
                  <div className="empty-chat">
                    <p>No messages yet. Start the conversation!</p>
                  </div>
                ) : (
                  messages.map(message => (
                    <ChatMessage key={message.id} message={message} />
                  ))
                )}
                <div ref={messagesEndRef} />
              </div>

              <ChatInput
                onSendMessage={sendChatMessage}
                isLoading={isLoading}
              />
            </>
          ) : (
            <div className="no-session-selected">
              <p>Select a session or create a new one to start chatting.</p>
            </div>
          )}
        </div>

        {showMemoryManager && (
          <div className="memory-sidebar">
            <MemoryManager />
          </div>
        )}
      </div>
    </div>
  );
};

export default Chat;
