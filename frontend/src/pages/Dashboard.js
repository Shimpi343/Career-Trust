import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bookmark, TrendingUp, LogOut, Settings, User } from 'lucide-react';
import api from '../api';

export default function Dashboard() {
  const navigate = useNavigate();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const response = await api.get('/analytics/dashboard');
      setDashboardData(response.data.dashboard);
      setError('');
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation */}
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-blue-600">CareerTrust</h1>
          <div className="flex gap-4 items-center">
            <button
              onClick={() => navigate('/profile')}
              className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-blue-600"
            >
              <User size={20} />
              Profile
            </button>
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 px-4 py-2 text-red-600 hover:bg-red-50 rounded"
            >
              <LogOut size={20} />
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-2">Welcome Back!</h2>
          <p className="text-gray-600">
            Discover AI-powered job recommendations tailored to your skills
          </p>
        </div>

        {/* Analytics Cards */}
        {dashboardData && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            {/* Profile Completion */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm font-medium">Profile Completion</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">
                    {dashboardData.profile_completion || 0}%
                  </p>
                </div>
                <div className="p-3 bg-blue-100 rounded-lg">
                  <User size={24} className="text-blue-600" />
                </div>
              </div>
              <div className="mt-4 w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full"
                  style={{ width: `${dashboardData.profile_completion || 0}%` }}
                ></div>
              </div>
            </div>

            {/* Saved Jobs */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm font-medium">Saved Jobs</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">
                    {dashboardData.total_saved_jobs || 0}
                  </p>
                </div>
                <div className="p-3 bg-green-100 rounded-lg">
                  <Bookmark size={24} className="text-green-600" />
                </div>
              </div>
            </div>

            {/* Applied To */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm font-medium">Applied To</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">
                    {dashboardData.jobs_applied_to || 0}
                  </p>
                </div>
                <div className="p-3 bg-purple-100 rounded-lg">
                  <TrendingUp size={24} className="text-purple-600" />
                </div>
              </div>
            </div>

            {/* Avg Match Score */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm font-medium">Avg Match Score</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">
                    {(dashboardData.average_match_score || 0).toFixed(1)}%
                  </p>
                </div>
                <div className="p-3 bg-orange-100 rounded-lg">
                  <TrendingUp size={24} className="text-orange-600" />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="mb-12">
          <h3 className="text-2xl font-bold text-gray-900 mb-6">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Search Jobs */}
            <button
              onClick={() => navigate('/recommendations')}
              className="bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg shadow p-8 hover:shadow-lg transition text-left"
            >
              <div className="text-3xl mb-2">🔍</div>
              <h4 className="text-xl font-bold mb-2">Get Recommendations</h4>
              <p className="text-blue-100">Find jobs matching your skills</p>
            </button>

            {/* View Saved Jobs */}
            <button
              onClick={() => navigate('/opportunities')}
              className="bg-gradient-to-r from-green-600 to-green-700 text-white rounded-lg shadow p-8 hover:shadow-lg transition text-left"
            >
              <div className="text-3xl mb-2">💾</div>
              <h4 className="text-xl font-bold mb-2">Browse Jobs</h4>
              <p className="text-green-100">Browse all job opportunities</p>
            </button>

            {/* View Analytics */}
            <button
              onClick={() => navigate('/jobs/integration')}
              className="bg-gradient-to-r from-purple-600 to-purple-700 text-white rounded-lg shadow p-8 hover:shadow-lg transition text-left"
            >
              <div className="text-3xl mb-2">📊</div>
              <h4 className="text-xl font-bold mb-2">Job Integration</h4>
              <p className="text-purple-100">Explore market insights</p>
            </button>
          </div>
        </div>

        {/* User Skills */}
        {dashboardData?.user_skills && dashboardData.user_skills.length > 0 && (
          <div className="bg-white rounded-lg shadow p-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Your Skills</h3>
            <div className="flex flex-wrap gap-3">
              {dashboardData.user_skills.map((skill, idx) => (
                <span
                  key={idx}
                  className="bg-blue-100 text-blue-800 px-4 py-2 rounded-full font-medium"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}

        {error && (
          <div className="mt-8 p-4 bg-red-100 text-red-700 rounded-lg">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}
