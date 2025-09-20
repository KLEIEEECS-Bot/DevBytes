import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { meetingsAPI } from '../services/api';
import { 
  Calendar, 
  Users, 
  Clock, 
  CheckCircle, 
  AlertCircle, 
  ArrowRight,
  Loader2
} from 'lucide-react';

const MeetingHistory = () => {
  const [meetings, setMeetings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchMeetings();
  }, []);

  const fetchMeetings = async () => {
    try {
      const data = await meetingsAPI.getAllMeetings();
      setMeetings(data);
    } catch (err) {
      setError('Failed to load meeting history. Please try again.');
      console.error('Error fetching meetings:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'active':
        return <Clock className="h-5 w-5 text-blue-500" />;
      case 'failed':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Clock className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'active':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'failed':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center py-16">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-gray-600">Loading meeting history...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center py-16">
          <AlertCircle className="h-12 w-12 mx-auto mb-4 text-red-500" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading History</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button onClick={fetchMeetings} className="btn-primary">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Meeting History</h1>
          <p className="text-gray-600">
            View and manage your processed meetings and task assignments.
          </p>
        </div>
        <Link to="/setup" className="btn-primary flex items-center">
          <Users className="h-4 w-4 mr-2" />
          New Meeting
        </Link>
      </div>

      {meetings.length === 0 ? (
        <div className="text-center py-16">
          <Calendar className="h-12 w-12 mx-auto mb-4 text-gray-400" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No Meetings Yet</h3>
          <p className="text-gray-600 mb-6">
            You haven't processed any meetings yet. Start by adding a Google Meet link.
          </p>
          <Link to="/setup" className="btn-primary inline-flex items-center">
            <Users className="h-4 w-4 mr-2" />
            Process Your First Meeting
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {meetings.map((meeting) => (
            <div key={meeting.id} className="bg-white rounded-lg shadow-sm border hover:shadow-md transition-shadow">
              <div className="p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-start space-x-4 flex-1">
                    <div className="bg-blue-100 p-2 rounded-full">
                      <Calendar className="h-5 w-5 text-blue-600" />
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-lg font-semibold text-gray-900">
                          {meeting.meeting_id}
                        </h3>
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(meeting.status)}`}>
                          {getStatusIcon(meeting.status)}
                          <span className="ml-1 capitalize">{meeting.status}</span>
                        </span>
                      </div>
                      
                      <p className="text-gray-600 mb-2">
                        Bot: {meeting.bot_name}
                      </p>
                      
                      <div className="flex items-center space-x-6 text-sm text-gray-500">
                        <span>
                          Created: {new Date(meeting.created_at).toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'short',
                            day: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </span>
                        {meeting.completed_at && (
                          <span>
                            Completed: {new Date(meeting.completed_at).toLocaleDateString('en-US', {
                              year: 'numeric',
                              month: 'short',
                              day: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  {meeting.status === 'completed' && (
                    <Link
                      to={`/dashboard/${meeting.meeting_id}`}
                      className="btn-primary flex items-center"
                    >
                      View Tasks
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Link>
                  )}
                  
                  {meeting.status === 'active' && (
                    <div className="text-right">
                      <p className="text-sm text-blue-600 font-medium mb-1">Meeting Active</p>
                      <p className="text-xs text-gray-500">Bot is recording</p>
                    </div>
                  )}
                  
                  {meeting.status === 'pending' && (
                    <div className="text-right">
                      <p className="text-sm text-gray-600 font-medium mb-1">Pending</p>
                      <p className="text-xs text-gray-500">Waiting to start</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MeetingHistory;