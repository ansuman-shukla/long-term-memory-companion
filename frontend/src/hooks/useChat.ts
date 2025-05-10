import { useState, useEffect, useCallback } from 'react';
import { fetchChatHistory, sendMessage } from '../services/api';

interface Message {
  id: string;
  content: string;
  message_type: string;
  timestamp: string;
  model_used?: string;
  reasoning?: boolean;
}

export const useChat = (sessionId: string | null) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const loadMessages = useCallback(async () => {
    if (!sessionId) {
      setMessages([]);
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchChatHistory(sessionId);
      setMessages(data.messages);
      return data.messages;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load messages');
      return [];
    } finally {
      setIsLoading(false);
    }
  }, [sessionId]);

  const sendChatMessage = useCallback(async (content: string, reasoning: boolean = false) => {
    if (!sessionId) return;

    setIsLoading(true);
    setError(null);
    try {
      // Optimistically add user message to UI
      const tempUserMessage: Message = {
        id: 'temp-' + Date.now(),
        content,
        message_type: 'user',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, tempUserMessage]);

      // Send message to API
      const botResponse = await sendMessage(sessionId, content, reasoning);
      
      // Update messages with actual response
      setMessages(prev => {
        // Replace temp message with actual one and add bot response
        const filtered = prev.filter(msg => msg.id !== tempUserMessage.id);
        return [...filtered, {
          id: 'user-' + botResponse.id,
          content,
          message_type: 'user',
          timestamp: botResponse.timestamp,
        }, botResponse];
      });
      
      return botResponse;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to send message');
      // Remove temp message on error
      setMessages(prev => prev.filter(msg => !msg.id.startsWith('temp-')));
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [sessionId]);

  useEffect(() => {
    loadMessages();
  }, [sessionId, loadMessages]);

  return {
    messages,
    isLoading,
    error,
    loadMessages,
    sendChatMessage
  };
};
