import { useState, useEffect, useCallback } from 'react';
import { fetchMemories, createMemory, updateMemory, deleteMemory } from '../services/api';

interface Memory {
  id: string;
  content: string;
  memo_type: string;
  created_at: string;
}

export const useMemory = (initialType: string = 'core_memory') => {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [memoryType, setMemoryType] = useState<string>(initialType);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const loadMemories = useCallback(async (type?: string) => {
    const memoType = type || memoryType;
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchMemories(memoType);
      setMemories(data);
      return data;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load memories');
      return [];
    } finally {
      setIsLoading(false);
    }
  }, [memoryType]);

  const addMemory = useCallback(async (content: string, type?: string) => {
    const memoType = type || memoryType;
    setIsLoading(true);
    setError(null);
    try {
      const newMemory = await createMemory(content, memoType);
      await loadMemories(memoType);
      return newMemory;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create memory');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [memoryType, loadMemories]);

  const editMemory = useCallback(async (id: string, content: string, type?: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const updatedMemory = await updateMemory(id, { 
        content, 
        ...(type && { memo_type: type })
      });
      await loadMemories();
      return updatedMemory;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update memory');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [loadMemories]);

  const removeMemory = useCallback(async (id: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await deleteMemory(id);
      await loadMemories();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete memory');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [loadMemories]);

  useEffect(() => {
    loadMemories();
  }, [memoryType, loadMemories]);

  return {
    memories,
    memoryType,
    setMemoryType,
    isLoading,
    error,
    loadMemories,
    addMemory,
    editMemory,
    removeMemory
  };
};
