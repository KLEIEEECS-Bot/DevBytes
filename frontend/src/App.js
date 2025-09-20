import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import MeetingSetup from './pages/MeetingSetup';
import TaskDashboard from './pages/TaskDashboard';
import MeetingHistory from './pages/MeetingHistory';
import Header from './components/Header';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/setup" element={<MeetingSetup />} />
            <Route path="/dashboard/:meetingId" element={<TaskDashboard />} />
            <Route path="/history" element={<MeetingHistory />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;