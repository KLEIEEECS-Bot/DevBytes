import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { meetingsAPI, transcriptsAPI } from '../services/api';
import { Link2, Users, FileText, Loader2, CheckCircle, AlertCircle } from 'lucide-react';

const MeetingSetup = () => {
  const [meetingUrl, setMeetingUrl] = useState('');
  const [botName, setBotName] = useState('MeetingBot');
  const [additionalContext, setAdditionalContext] = useState('');
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [meetingData, setMeetingData] = useState(null);
  const navigate = useNavigate();

  const validateMeetingUrl = (url) => {
    return url.includes('meet.google.com/');
  };

  const handleStartBot = async () => {
    if (!validateMeetingUrl(meetingUrl)) {
      setError('Please enter a valid Google Meet URL');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await meetingsAPI.startBot(meetingUrl, botName);
      setMeetingData(result);
      setCurrentStep(2);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start bot. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleProcessTranscript = async () => {
    if (!meetingData) return;

    setLoading(true);
    setError('');

    try {
      await transcriptsAPI.processTranscript(
        meetingData.meeting_id, 
        additionalContext
      );
      
      // Navigate to dashboard
      navigate(`/dashboard/${meetingData.meeting_id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process transcript. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteAndProcess = async () => {
    if (!meetingData) return;

    setLoading(true);
    setError('');

    try {
      // Complete the meeting first
      await meetingsAPI.completeMeeting(meetingData.meeting_id);
      
      // Then process transcript
      await handleProcessTranscript();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process meeting. Please try again.');
      setLoading(false);
    }
  };

  if (currentStep === 1) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Set Up Your Meeting
          </h1>
          <p className="text-gray-600">
            Enter your Google Meet link to get started with automatic transcription and task extraction.
          </p>
        </div>

        <div className="card">
          <div className="space-y-6">
            {/* Meeting URL Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Google Meet URL *
              </label>
              <div className="relative">
                <Link2 className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="url"
                  value={meetingUrl}
                  onChange={(e) => setMeetingUrl(e.target.value)}
                  placeholder="https://meet.google.com/abc-def-ghi"
                  className="input-field pl-10"
                  required
                />
              </div>
            </div>

            {/* Bot Name Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Bot Name (Optional)
              </label>
              <div className="relative">
                <Users className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  value={botName}
                  onChange={(e) => setBotName(e.target.value)}
                  placeholder="MeetingBot"
                  className="input-field pl-10"
                />
              </div>
              <p className="text-sm text-gray-500 mt-1">
                This is the name that will appear in your meeting when the bot joins.
              </p>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center">
                <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
                <span className="text-red-700">{error}</span>
              </div>
            )}

            <button
              onClick={handleStartBot}
              disabled={loading || !meetingUrl}
              className="btn-primary w-full flex items-center justify-center"
            >
              {loading ? (
                <Loader2 className="animate-spin h-5 w-5 mr-2" />
              ) : (
                <Users className="h-5 w-5 mr-2" />
              )}
              {loading ? 'Starting Bot...' : 'Start Bot'}
            </button>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="font-medium text-blue-900 mb-2">What happens next?</h3>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• The bot will join your Google Meet session</li>
                <li>• It will record the meeting conversation</li>
                <li>• After the meeting ends, come back to process the transcript</li>
                <li>• We'll extract action items and assign tasks automatically</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Bot Started Successfully!
        </h1>
        <p className="text-gray-600">
          The bot has joined your meeting. When the meeting ends, return here to process the transcript.
        </p>
      </div>

      <div className="card">
        <div className="space-y-6">
          {/* Status */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-center">
            <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
            <div>
              <span className="text-green-700 font-medium">Bot Active</span>
              <p className="text-green-600 text-sm">Recording meeting: {meetingData?.meeting_id}</p>
            </div>
          </div>

          {/* Additional Context */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Additional Context (Optional)
            </label>
            <div className="relative">
              <FileText className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
              <textarea
                value={additionalContext}
                onChange={(e) => setAdditionalContext(e.target.value)}
                placeholder="Add any additional context about the meeting, project details, or specific instructions for task assignment..."
                rows="4"
                className="textarea-field pl-10"
              />
            </div>
            <p className="text-sm text-gray-500 mt-1">
              This context will help the AI better understand and assign tasks from your meeting.
            </p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center">
              <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
              <span className="text-red-700">{error}</span>
            </div>
          )}

          <div className="space-y-3">
            <button
              onClick={handleCompleteAndProcess}
              disabled={loading}
              className="btn-primary w-full flex items-center justify-center"
            >
              {loading ? (
                <Loader2 className="animate-spin h-5 w-5 mr-2" />
              ) : (
                <FileText className="h-5 w-5 mr-2" />
              )}
              {loading ? 'Processing...' : 'Meeting Ended - Process Transcript'}
            </button>
            
            <button
              onClick={handleProcessTranscript}
              disabled={loading}
              className="btn-secondary w-full flex items-center justify-center"
            >
              Process Without Ending Meeting
            </button>
          </div>

          <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
            <h3 className="font-medium text-amber-900 mb-2">Instructions:</h3>
            <ol className="text-sm text-amber-800 space-y-1 list-decimal list-inside">
              <li>Go to your Google Meet and start/continue your meeting</li>
              <li>The bot should now be visible in the meeting</li>
              <li>When your meeting ends, click "Meeting Ended - Process Transcript"</li>
              <li>Or click "Process Without Ending Meeting" if you want to process while the meeting is still active</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MeetingSetup;