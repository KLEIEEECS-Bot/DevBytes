import React from 'react';
import { CheckSquare, Clock, AlertTriangle, Plus } from 'lucide-react';

const TaskCard = ({ task, onComplete }) => {
  const getPriorityColor = (priority) => {
    switch (priority?.toLowerCase()) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getPriorityIcon = (priority) => {
    switch (priority?.toLowerCase()) {
      case 'high':
        return <AlertTriangle className="h-4 w-4" />;
      default:
        return <Clock className="h-4 w-4" />;
    }
  };

  const addToGoogleCalendar = () => {
    const title = encodeURIComponent(`Task: ${task.task_description}`);
    const details = encodeURIComponent(
      `Assigned to: ${task.assignee_name}\n\nTask: ${task.task_description}${
        task.deadline ? `\n\nDeadline: ${task.deadline}` : ''
      }${task.priority ? `\n\nPriority: ${task.priority}` : ''}`
    );
    
    let dates = '';
    if (task.deadline) {
      // Try to parse deadline into a date
      const deadline = new Date(task.deadline);
      if (!isNaN(deadline.getTime())) {
        const startDate = deadline.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
        const endDate = new Date(deadline.getTime() + 60 * 60 * 1000).toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
        dates = `&dates=${startDate}/${endDate}`;
      }
    }

    const calendarUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${title}&details=${details}${dates}`;
    window.open(calendarUrl, '_blank');
  };

  return (
    <div className={`border rounded-lg p-4 ${task.is_completed ? 'bg-gray-50 border-gray-200' : 'bg-white border-gray-200'} hover:shadow-sm transition-shadow`}>
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3 flex-1">
          <button
            onClick={() => !task.is_completed && onComplete()}
            className={`mt-1 flex-shrink-0 ${
              task.is_completed 
                ? 'text-green-600 cursor-default' 
                : 'text-gray-400 hover:text-green-600 cursor-pointer'
            }`}
          >
            <CheckSquare 
              className={`h-5 w-5 ${task.is_completed ? 'fill-current' : ''}`} 
            />
          </button>
          
          <div className="flex-1">
            <p className={`text-gray-900 ${task.is_completed ? 'line-through text-gray-500' : ''}`}>
              {task.task_description}
            </p>
            
            <div className="flex items-center space-x-4 mt-2">
              {task.deadline && (
                <div className="flex items-center text-sm text-gray-600">
                  <Clock className="h-4 w-4 mr-1" />
                  {task.deadline}
                </div>
              )}
              
              {task.priority && (
                <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${getPriorityColor(task.priority)}`}>
                  {getPriorityIcon(task.priority)}
                  <span className="ml-1">{task.priority}</span>
                </span>
              )}
            </div>
          </div>
        </div>
        
        {!task.is_completed && (
          <button
            onClick={addToGoogleCalendar}
            className="flex-shrink-0 p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
            title="Add to Google Calendar"
          >
            <Plus className="h-4 w-4" />
          </button>
        )}
      </div>
    </div>
  );
};

export default TaskCard;