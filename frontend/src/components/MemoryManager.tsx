import { useState } from 'react';
import { useMemory } from '../hooks/useMemory';
import LoadingSpinner from './LoadingSpinner';
import ConfirmDialog from './ConfirmDialog';
import '../assets/styles/MemoryManager.css';

interface Memory {
  id: string;
  content: string;
  memo_type: string;
  created_at: string;
}

const MemoryManager = () => {
  const {
    memories,
    memoryType,
    setMemoryType,
    isLoading,
    error: memoryError,
    addMemory,
    editMemory,
    removeMemory
  } = useMemory('core_memory');

  const [newMemory, setNewMemory] = useState<string>('');
  const [editingMemory, setEditingMemory] = useState<Memory | null>(null);
  const [success, setSuccess] = useState<string>('');
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState<boolean>(false);
  const [memoryToDelete, setMemoryToDelete] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleCreateMemory = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMemory.trim()) return;

    setError('');
    setSuccess('');
    try {
      await addMemory(newMemory);
      setNewMemory('');
      setSuccess('Memory created successfully');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create memory');
    }
  };

  const handleUpdateMemory = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingMemory || !editingMemory.content.trim()) return;

    setError('');
    setSuccess('');
    try {
      await editMemory(editingMemory.id, editingMemory.content);
      setEditingMemory(null);
      setSuccess('Memory updated successfully');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update memory');
    }
  };

  const openDeleteConfirm = (memoryId: string) => {
    setMemoryToDelete(memoryId);
    setDeleteConfirmOpen(true);
  };

  const handleDeleteMemory = async () => {
    if (!memoryToDelete) return;

    setError('');
    setSuccess('');
    try {
      await removeMemory(memoryToDelete);
      setSuccess('Memory deleted successfully');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete memory');
    }
  };

  return (
    <div className="memory-manager pixel-border">
      <h2 className="memory-title pixel-text">Memory Manager</h2>

      <div className="memory-tabs">
        <button
          className={`memory-tab ${memoryType === 'core_memory' ? 'active' : ''}`}
          onClick={() => setMemoryType('core_memory')}
        >
          Core Memories
        </button>
        <button
          className={`memory-tab ${memoryType === 'environment_memory' ? 'active' : ''}`}
          onClick={() => setMemoryType('environment_memory')}
        >
          Environment Memories
        </button>
      </div>

      {(error || memoryError) && <div className="error-message">{error || memoryError}</div>}
      {success && <div className="success-message">{success}</div>}

      <div className="memory-list">
        {isLoading ? (
          <div className="loading-text">
            <LoadingSpinner size="medium" color="primary" />
          </div>
        ) : memories.length === 0 ? (
          <p className="no-memories">No {memoryType === 'core_memory' ? 'core' : 'environment'} memories yet.</p>
        ) : (
          memories.map(memory => (
            <div key={memory.id} className="memory-item">
              {editingMemory?.id === memory.id ? (
                <form onSubmit={handleUpdateMemory} className="edit-memory-form">
                  <textarea
                    className="form-input memory-textarea"
                    value={editingMemory.content}
                    onChange={(e) => setEditingMemory({...editingMemory, content: e.target.value})}
                    required
                  />
                  <div className="memory-actions">
                    <button
                      type="submit"
                      className="icon-btn icon-btn-edit icon-save"
                      title="Save"
                    >
                    </button>
                    <button
                      type="button"
                      className="icon-btn icon-btn-delete icon-cancel"
                      onClick={() => setEditingMemory(null)}
                      title="Cancel"
                    >
                    </button>
                  </div>
                </form>
              ) : (
                <>
                  <div className="memory-content">{memory.content}</div>
                  <div className="memory-actions">
                    <button
                      className="icon-btn icon-btn-edit icon-edit"
                      onClick={() => setEditingMemory(memory)}
                      title="Edit"
                    >
                    </button>
                    <button
                      className="icon-btn icon-btn-delete icon-delete"
                      onClick={() => openDeleteConfirm(memory.id)}
                      title="Delete"
                    >
                    </button>
                  </div>
                </>
              )}
            </div>
          ))
        )}
      </div>

      <form onSubmit={handleCreateMemory} className="new-memory-form">
        <h3 className="new-memory-title">
          Add New {memoryType === 'core_memory' ? 'Core' : 'Environment'} Memory
        </h3>
        <textarea
          className="form-input memory-textarea"
          value={newMemory}
          onChange={(e) => setNewMemory(e.target.value)}
          placeholder={`Enter new ${memoryType === 'core_memory' ? 'core' : 'environment'} memory...`}
          required
        />
        <button
          type="submit"
          className="btn btn-primary new-memory-btn"
          disabled={isLoading}
        >
          Add Memory
        </button>
      </form>

      <ConfirmDialog
        isOpen={deleteConfirmOpen}
        onClose={() => setDeleteConfirmOpen(false)}
        onConfirm={handleDeleteMemory}
        title="Delete Memory"
        message="Are you sure you want to delete this memory? This action cannot be undone."
        confirmText="Delete"
        isDestructive={true}
      />
    </div>
  );
};

export default MemoryManager;
