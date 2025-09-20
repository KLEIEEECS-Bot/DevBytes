import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Meetings API
export const meetingsAPI = {
  startBot: async (meetingUrl, botName = 'MeetingBot') => {
    const response = await api.post('/meetings/start', {
      meeting_url: meetingUrl,
      bot_name: botName,
    });
    return response.data;
  },

  getMeetingStatus: async (meetingId) => {
    const response = await api.get(`/meetings/${meetingId}/status`);
    return response.data;
  },

  completeMeeting: async (meetingId) => {
    const response = await api.post(`/meetings/${meetingId}/complete`);
    return response.data;
  },

  getAllMeetings: async () => {
    const response = await api.get('/meetings/');
    return response.data;
  },

  getMeeting: async (meetingId) => {
    const response = await api.get(`/meetings/${meetingId}`);
    return response.data;
  },
};

// Transcripts API
export const transcriptsAPI = {
  processTranscript: async (meetingId, additionalContext = '') => {
    const response = await api.post(`/transcripts/${meetingId}/process`, {
      additional_context: additionalContext,
    });
    return response.data;
  },

  getTranscript: async (meetingId) => {
    const response = await api.get(`/transcripts/${meetingId}`);
    return response.data;
  },
};

// Tasks API
export const tasksAPI = {
  getTasksForMeeting: async (meetingId) => {
    const response = await api.get(`/tasks/${meetingId}`);
    return response.data;
  },

  modifyTasks: async (meetingId, modificationRequest) => {
    const response = await api.post(`/tasks/${meetingId}/modify`, {
      meeting_id: parseInt(meetingId),
      modification_request: modificationRequest,
    });
    return response.data;
  },

  markTaskComplete: async (taskId) => {
    const response = await api.patch(`/tasks/${taskId}/complete`);
    return response.data;
  },

  exportTasks: async (meetingId) => {
    const response = await api.get(`/tasks/${meetingId}/export`);
    return response.data;
  },

  exportTasksPDF: async (meetingId) => {
    const response = await api.get(`/exports/${meetingId}/pdf`, {
      responseType: 'blob'
    });
    return response.data;
  },
};

export default api;