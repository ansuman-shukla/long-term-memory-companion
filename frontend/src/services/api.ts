import axios from 'axios';

// Session API
export const fetchSessions = async () => {
  const response = await axios.get('/api/sessions');
  return response.data;
};

export const createSession = async (name: string) => {
  const response = await axios.post('/api/sessions', { name });
  return response.data;
};

export const updateSession = async (sessionId: string, name: string) => {
  const response = await axios.put(`/api/sessions/${sessionId}`, { name });
  return response.data;
};

export const deleteSession = async (sessionId: string) => {
  await axios.delete(`/api/sessions/${sessionId}`);
};

// Chat API
export const fetchChatHistory = async (sessionId: string, limit = 50, skip = 0) => {
  const response = await axios.get(`/api/chat/${sessionId}/messages?limit=${limit}&skip=${skip}`);
  return response.data;
};

export const sendMessage = async (sessionId: string, content: string, reasoning = false) => {
  const response = await axios.post(`/api/chat/${sessionId}/messages`, { content, reasoning });
  return response.data;
};

// Memory API
export const fetchMemories = async (memoType?: string) => {
  const url = memoType ? `/api/memory?memo_type=${memoType}` : '/api/memory';
  const response = await axios.get(url);
  return response.data;
};

export const createMemory = async (content: string, memoType: string) => {
  const response = await axios.post('/api/memory', { content, memo_type: memoType });
  return response.data;
};

export const updateMemory = async (memoryId: string, data: { content?: string; memo_type?: string }) => {
  const response = await axios.put(`/api/memory/${memoryId}`, data);
  return response.data;
};

export const deleteMemory = async (memoryId: string) => {
  await axios.delete(`/api/memory/${memoryId}`);
};
