import { useState, useEffect, useCallback } from 'react';
import { fetchSessions, createSession, updateSession, deleteSession } from '../services/api';

interface Session {
  id: string;
  name: string;
  created_at: string;
  updated_at: string;
  last_message_at: string | null;
}

export const useSession = () => {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const loadSessions = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchSessions();
      setSessions(data);
      if (data.length > 0 && !activeSessionId) {
        setActiveSessionId(data[0].id);
      }
      return data;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load sessions');
      return [];
    } finally {
      setIsLoading(false);
    }
  }, [activeSessionId]);

  const createNewSession = useCallback(async (name: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const newSession = await createSession(name);
      await loadSessions();
      setActiveSessionId(newSession.id);
      return newSession;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create session');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [loadSessions]);

  const updateCurrentSession = useCallback(async (name: string) => {
    if (!activeSessionId) return null;
    
    setIsLoading(true);
    setError(null);
    try {
      const updatedSession = await updateSession(activeSessionId, name);
      await loadSessions();
      return updatedSession;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update session');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [activeSessionId, loadSessions]);

  const deleteCurrentSession = useCallback(async () => {
    if (!activeSessionId) return;
    
    setIsLoading(true);
    setError(null);
    try {
      await deleteSession(activeSessionId);
      const updatedSessions = await loadSessions();
      if (updatedSessions.length > 0) {
        setActiveSessionId(updatedSessions[0].id);
      } else {
        setActiveSessionId(null);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete session');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [activeSessionId, loadSessions]);

  useEffect(() => {
    loadSessions();
  }, []);

  return {
    sessions,
    activeSessionId,
    setActiveSessionId,
    isLoading,
    error,
    loadSessions,
    createNewSession,
    updateCurrentSession,
    deleteCurrentSession
  };
};
