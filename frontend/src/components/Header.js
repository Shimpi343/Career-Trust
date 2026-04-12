import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="bg-blue-600 text-white">
      <nav className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold">CareerTrust</Link>
        <ul className="flex space-x-6">
          <li><Link to="/">Home</Link></li>
          <li><Link to="/opportunities">Opportunities</Link></li>
          <li><Link to="/recommendations">Recommendations</Link></li>
          <li><Link to="/jobs/integration">Job Import</Link></li>
          <li><Link to="/dashboard">Dashboard</Link></li>
          <li><Link to="/profile">Profile</Link></li>
          <li><Link to="/register" className="bg-white text-blue-600 px-4 py-2 rounded font-semibold hover:bg-gray-100">Register</Link></li>
          <li><Link to="/login" className="border-2 border-white px-4 py-2 rounded hover:bg-blue-700">Login</Link></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;
