import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import '../assets/styles/ChatMessage.css';

interface Message {
  id: string;
  content: string;
  message_type: string;
  timestamp: string;
  model_used?: string;
  reasoning?: boolean;
}

interface ChatMessageProps {
  message: Message;
}

const ChatMessage = ({ message }: ChatMessageProps) => {
  const { user } = useContext(AuthContext);
  const isUser = message.message_type === 'user';

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`message-container ${isUser ? 'user-message' : 'bot-message'}`}>
      <div className="message-content pixel-border">
        <div className="message-header">
          <span className="message-time">{formatTime(message.timestamp)}</span>
        </div>
        <div className="message-text">{message.content}</div>
      </div>
    </div>
  );
};

export default ChatMessage;
