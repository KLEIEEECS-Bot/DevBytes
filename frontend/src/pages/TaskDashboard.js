import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { tasksAPI, meetingsAPI } from '../services/api';
import { 
  User, 
  CheckSquare, 
  Download, 
  Clock,
  AlertCircle,
  Loader2,
  MessageSquare
} from 'lucide-react';
import TaskCard from '../components/TaskCard';
import TaskModification from '../components/TaskModification';

const TaskDashboard = () => {
  const { meetingId } = useParams();
  const [tasks, setTasks] = useState([]);
  const [meeting, setMeeting] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showModification, setShowModification] = useState(false);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const [tasksData, meetingData] = await Promise.all([
        tasksAPI.getTasksForMeeting(meetingId),
        meetingsAPI.getMeeting(meetingId)
      ]);
      
      setTasks(tasksData);
      setMeeting(meetingData);
    } catch (err) {
      setError('Failed to load meeting data. Please try again.');
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  }, [meetingId]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleTaskComplete = async (taskId) => {
    try {
      await tasksAPI.markTaskComplete(taskId);
      setTasks(tasks.map(task => 
        task.id === taskId ? { ...task, is_completed: true } : task
      ));
    } catch (err) {
      console.error('Error marking task complete:', err);
    }
  };

  const handleExport = async () => {
    try {
      const exportData = await tasksAPI.exportTasks(meetingId);
      
      // Create and download JSON file
      const dataStr = JSON.stringify(exportData, null, 2);
      const dataBlob = new Blob([dataStr], {type: 'application/json'});
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `meeting-tasks-${meetingId}.json`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Error exporting tasks:', err);
    }
  };

  const handleExportPDF = async () => {
    try {
      const pdfBlob = await tasksAPI.exportTasksPDF(meetingId);
      
      // Create and download PDF file
      const url = URL.createObjectURL(pdfBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `meeting-tasks-${meetingId}.pdf`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Error exporting PDF:', err);
    }
  };

  const handleTaskModificationComplete = () => {
    setShowModification(false);
    fetchData(); // Refresh tasks after modification
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="text-center py-16">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-gray-600">Loading meeting data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="text-center py-16">
          <AlertCircle className="h-12 w-12 mx-auto mb-4 text-red-500" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Data</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button onClick={fetchData} className="btn-primary">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Task Dashboard
            </h1>
            {meeting && (
              <p className="text-gray-600">
                Meeting ID: {meetingId} • Created: {new Date(meeting.created_at).toLocaleDateString()}
              </p>
            )}
          </div>
          <div className="flex items-center space-x-3">
            <button
              onClick={() => setShowModification(true)}
              className="btn-secondary flex items-center"
            >
              <MessageSquare className="h-4 w-4 mr-2" />
              Modify Tasks
            </button>
            <div className="relative">
              <button
                onClick={handleExportPDF}
                className="btn-primary flex items-center"
              >
                <Download className="h-4 w-4 mr-2" />
                Export PDF
              </button>
            </div>
            <button
              onClick={handleExport}
              className="btn-secondary flex items-center"
            >
              <Download className="h-4 w-4 mr-2" />
              Export JSON
            </button>
          </div>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center">
              <div className="bg-blue-100 p-3 rounded-full mr-4">
                <CheckSquare className="h-6 w-6 text-blue-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">{tasks.length}</p>
                <p className="text-gray-600">Total Tasks</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center">
              <div className="bg-green-100 p-3 rounded-full mr-4">
                <CheckSquare className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">
                  {tasks.filter(task => task.is_completed).length}
                </p>
                <p className="text-gray-600">Completed</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center">
              <div className="bg-amber-100 p-3 rounded-full mr-4">
                <Clock className="h-6 w-6 text-amber-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">
                  {tasks.filter(task => !task.is_completed).length}
                </p>
                <p className="text-gray-600">Pending</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center">
              <div className="bg-purple-100 p-3 rounded-full mr-4">
                <User className="h-6 w-6 text-purple-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">
                  {new Set(tasks.map(task => task.assignee_name)).size}
                </p>
                <p className="text-gray-600">Assignees</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Tasks */}
      {tasks.length === 0 ? (
        <div className="text-center py-16">
          <CheckSquare className="h-12 w-12 mx-auto mb-4 text-gray-400" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No Tasks Found</h3>
          <p className="text-gray-600">No action items were extracted from this meeting.</p>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Group tasks by assignee */}
          {Object.entries(
            tasks.reduce((groups, task) => {
              const assignee = task.assignee_name;
              if (!groups[assignee]) {
                groups[assignee] = [];
              }
              groups[assignee].push(task);
              return groups;
            }, {})
          ).map(([assigneeName, assigneeTasks]) => (
            <div key={assigneeName} className="bg-white rounded-lg shadow-sm border">
              <div className="p-6 border-b">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="bg-gray-100 p-2 rounded-full mr-3">
                      <User className="h-5 w-5 text-gray-600" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        {assigneeName}
                      </h3>
                      <p className="text-gray-600">
                        {assigneeTasks.length} task{assigneeTasks.length !== 1 ? 's' : ''}
                      </p>
                    </div>
                  </div>
                  <div className="text-sm text-gray-500">
                    {assigneeTasks.filter(task => task.is_completed).length} of{' '}
                    {assigneeTasks.length} completed
                  </div>
                </div>
              </div>
              
              <div className="p-6 space-y-4">
                {assigneeTasks.map((task) => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    onComplete={() => handleTaskComplete(task.id)}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Task Modification Modal */}
      {showModification && (
        <TaskModification
          meetingId={meetingId}
          onClose={() => setShowModification(false)}
          onComplete={handleTaskModificationComplete}
        />
      )}
    </div>
  );
};

export default TaskDashboard;