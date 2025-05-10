import { useState } from 'react';
import { createSession, deleteSession } from '../services/api';
import '../assets/styles/SessionList.css';

interface Session {
  id: string;
  name: string;
  created_at: string;
  updated_at: string;
  last_message_at: string | null;
}

interface SessionListProps {
  sessions: Session[];
  activeSessionId: string | null;
  onSelectSession: (sessionId: string) => void;
  onSessionsChange: () => void;
}

const SessionList = ({ sessions, activeSessionId, onSelectSession, onSessionsChange }: SessionListProps) => {
  const [newSessionName, setNewSessionName] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  const [error, setError] = useState('');

  const handleCreateSession = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSessionName.trim()) return;

    setError('');
    try {
      const newSession = await createSession(newSessionName);
      setNewSessionName('');
      setIsCreating(false);
      onSessionsChange();
      onSelectSession(newSession.id);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create session');
    }
  };

  const handleDeleteSession = async (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this session?')) return;

    try {
      await deleteSession(sessionId);
      onSessionsChange();
      if (activeSessionId === sessionId) {
        onSelectSession(sessions.length > 1 ? sessions[0].id : '');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete session');
    }
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'Never';
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  return (
    <div className="session-list-container pixel-border">
      <h2 className="session-list-title pixel-text">Chat Sessions</h2>
      {error && <div className="error-message">{error}</div>}
      
      <div className="session-list">
        {sessions.length === 0 ? (
          <p className="no-sessions">No sessions yet. Create one to start chatting!</p>
        ) : (
          sessions.map(session => (
            <div 
              key={session.id} 
              className={`session-item ${activeSessionId === session.id ? 'active' : ''}`}
              onClick={() => onSelectSession(session.id)}
            >
              <div className="session-name">{session.name}</div>
              <div className="session-date">Last active: {formatDate(session.last_message_at || session.updated_at)}</div>
              <button 
                className="session-delete-btn"
                onClick={(e) => handleDeleteSession(session.id, e)}
                title="Delete session"
              >
                ×
              </button>
            </div>
          ))
        )}
      </div>
      
      {isCreating ? (
        <form onSubmit={handleCreateSession} className="new-session-form">
          <input
            type="text"
            className="form-input"
            value={newSessionName}
            onChange={(e) => setNewSessionName(e.target.value)}
            placeholder="Session name"
            autoFocus
            required
          />
          <div className="new-session-actions">
            <button type="submit" className="btn btn-primary">Create</button>
            <button 
              type="button" 
              className="btn"
              onClick={() => {
                setIsCreating(false);
                setNewSessionName('');
              }}
            >
              Cancel
            </button>
          </div>
        </form>
      ) : (
        <button 
          className="btn btn-primary new-session-btn"
          onClick={() => setIsCreating(true)}
        >
          New Session
        </button>
      )}
    </div>
  );
};

export default SessionList;
