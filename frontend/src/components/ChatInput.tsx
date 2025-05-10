import { useState } from 'react';
import '../assets/styles/ChatInput.css';

interface ChatInputProps {
  onSendMessage: (content: string, reasoning: boolean) => Promise<void>;
  isLoading: boolean;
}

const ChatInput = ({ onSendMessage, isLoading }: ChatInputProps) => {
  const [message, setMessage] = useState('');
  // Always use false for reasoning to use gemini-2.0-flash-lite
  const reasoning = false;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || isLoading) return;

    try {
      await onSendMessage(message, reasoning);
      setMessage('');
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="chat-input-container pixel-border">
      <div className="chat-input-row">
        <textarea
          className="chat-input"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
        />
        <button
          type="submit"
          className="btn btn-primary send-button"
          disabled={isLoading || !message.trim()}
        >
          {isLoading ? '...' : 'Send'}
        </button>
      </div>
    </form>
  );
};

export default ChatInput;
