import React from 'react';
import { Link } from 'react-router-dom';
import { Calendar } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-2">
            <Calendar className="h-8 w-8 text-blue-600" />
            <span className="text-xl font-bold text-gray-900">Meeting Notes Processor</span>
          </Link>
          
          <nav className="flex items-center space-x-6">
            <Link 
              to="/" 
              className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
            >
              Home
            </Link>
            <Link 
              to="/history" 
              className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
            >
              Meeting History
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;