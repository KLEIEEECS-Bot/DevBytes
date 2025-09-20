import React, { useState } from 'react';
import { tasksAPI } from '../services/api';
import { X, Send, Loader2, MessageSquare } from 'lucide-react';

const TaskModification = ({ meetingId, onClose, onComplete }) => {
  const [modificationRequest, setModificationRequest] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!modificationRequest.trim()) {
      setError('Please enter your modification request');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await tasksAPI.modifyTasks(meetingId, modificationRequest.trim());
      onComplete();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to modify tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const exampleRequests = [
    "Change John's deadline to next Friday",
    "Add a high priority task for Sarah to review the proposal",
    "Remove the task about updating documentation",
    "Reassign Mike's tasks to Jennifer",
    "Add deadline 'end of week' to all tasks without deadlines"
  ];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <div className="flex items-center">
            <MessageSquare className="h-6 w-6 text-blue-600 mr-3" />
            <h2 className="text-xl font-semibold text-gray-900">
              Modify Task Assignments
            </h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 max-h-[calc(90vh-120px)] overflow-y-auto">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                What changes would you like to make?
              </label>
              <textarea
                value={modificationRequest}
                onChange={(e) => setModificationRequest(e.target.value)}
                placeholder="Describe the changes you want to make to the task assignments..."
                rows="6"
                className="textarea-field"
                required
              />
              <p className="text-sm text-gray-500 mt-1">
                Be specific about what you want to change. The AI will understand natural language instructions.
              </p>
            </div>

            {/* Examples */}
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-3">Example requests:</h3>
              <div className="space-y-2">
                {exampleRequests.map((example, index) => (
                  <button
                    key={index}
                    type="button"
                    onClick={() => setModificationRequest(example)}
                    className="block w-full text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg text-sm text-gray-700 transition-colors"
                  >
                    "{example}"
                  </button>
                ))}
              </div>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-red-700">{error}</p>
              </div>
            )}

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-medium text-blue-900 mb-2">How it works:</h4>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• Describe your changes in natural language</li>
                <li>• The AI will update the task assignments based on your request</li>
                <li>• You can add, remove, or modify tasks and deadlines</li>
                <li>• Changes will be applied to the current meeting's tasks</li>
              </ul>
            </div>

            <div className="flex space-x-3">
              <button
                type="submit"
                disabled={loading || !modificationRequest.trim()}
                className="btn-primary flex items-center flex-1"
              >
                {loading ? (
                  <Loader2 className="animate-spin h-4 w-4 mr-2" />
                ) : (
                  <Send className="h-4 w-4 mr-2" />
                )}
                {loading ? 'Processing Changes...' : 'Apply Changes'}
              </button>
              
              <button
                type="button"
                onClick={onClose}
                disabled={loading}
                className="btn-secondary flex-shrink-0"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default TaskModification;