import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Users, FileText, Calendar, CheckSquare } from 'lucide-react';

const HomePage = () => {
  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="text-center py-16">
        <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
          Transform Meeting Notes into 
          <span className="text-blue-600"> Action Items</span>
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Automatically process meeting transcripts, extract actionable tasks, and assign them to team members with deadlines.
        </p>
        <Link to="/setup" className="btn-primary inline-flex items-center text-lg px-8 py-3">
          Get Started
          <ArrowRight className="ml-2 h-5 w-5" />
        </Link>
      </div>

      {/* Features Section */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 py-16">
        <div className="text-center">
          <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
            <Users className="h-8 w-8 text-blue-600" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Join Meeting</h3>
          <p className="text-gray-600">
            Our bot joins your Google Meet session automatically to capture the conversation.
          </p>
        </div>

        <div className="text-center">
          <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
            <FileText className="h-8 w-8 text-green-600" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Extract Transcript</h3>
          <p className="text-gray-600">
            Get clean, processed transcripts with speaker identification after the meeting ends.
          </p>
        </div>

        <div className="text-center">
          <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckSquare className="h-8 w-8 text-purple-600" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Generate Tasks</h3>
          <p className="text-gray-600">
            AI analyzes the transcript and automatically extracts actionable tasks with assignments.
          </p>
        </div>

        <div className="text-center">
          <div className="bg-orange-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
            <Calendar className="h-8 w-8 text-orange-600" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Track & Export</h3>
          <p className="text-gray-600">
            Export to Google Calendar, generate PDFs, and track task completion.
          </p>
        </div>
      </div>

      {/* How it Works Section */}
      <div className="py-16">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          How It Works
        </h2>
        <div className="max-w-4xl mx-auto">
          <div className="space-y-8">
            <div className="flex items-start space-x-4">
              <div className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold flex-shrink-0">
                1
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Enter Meeting Link</h3>
                <p className="text-gray-600">
                  Paste your Google Meet link and our bot will join the meeting to record the conversation.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold flex-shrink-0">
                2
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Meeting Ends</h3>
                <p className="text-gray-600">
                  After the meeting ends, the bot automatically leaves and processes the transcript.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold flex-shrink-0">
                3
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Process & Extract</h3>
                <p className="text-gray-600">
                  AI analyzes the transcript and extracts actionable tasks, assigning them to the right people.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold flex-shrink-0">
                4
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Review & Export</h3>
                <p className="text-gray-600">
                  Review the generated tasks, make adjustments if needed, and export to your preferred tools.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-blue-600 rounded-2xl p-12 text-center text-white">
        <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
        <p className="text-xl mb-8 opacity-90">
          Transform your meetings into actionable insights in minutes.
        </p>
        <Link to="/setup" className="bg-white text-blue-600 font-bold py-3 px-8 rounded-lg hover:bg-gray-100 transition-colors inline-flex items-center">
          Start Processing Meetings
          <ArrowRight className="ml-2 h-5 w-5" />
        </Link>
      </div>
    </div>
  );
};

export default HomePage;