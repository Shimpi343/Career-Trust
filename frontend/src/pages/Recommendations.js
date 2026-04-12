import React, { useState, useEffect } from 'react';
import api from '../api';

function Recommendations() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [skills, setSkills] = useState('');
  const [interests, setInterests] = useState('');
  const [showProfileForm, setShowProfileForm] = useState(false);

  useEffect(() => {
    fetchUserProfile();
    fetchRecommendations();
  }, []);

  const fetchUserProfile = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) return;

      const response = await api.get('/auth/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setSkills((response.data.skills || []).join(', '));
      setInterests((response.data.interests || []).join(', '));
    } catch (err) {
      console.error('Failed to fetch profile:', err);
    }
  };

  const fetchRecommendations = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setError('Please login to see recommendations');
        setLoading(false);
        return;
      }

      const response = await api.get('/recommendations', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setRecommendations(response.data.recommendations || []);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch recommendations');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('access_token');
      const skillsList = skills.split(',').map(s => s.trim()).filter(s => s);
      const interestsList = interests.split(',').map(i => i.trim()).filter(i => i);

      await api.post('/auth/me/profile', {
        skills: skillsList,
        interests: interestsList
      }, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      setShowProfileForm(false);
      fetchRecommendations();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update profile');
    }
  };

  if (loading) return <div className="container mx-auto px-4 py-12">Loading recommendations...</div>;

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">Personalized Recommendations</h1>

      {/* Profile Section */}
      <div className="bg-blue-50 border-2 border-blue-200 p-6 rounded-lg mb-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-blue-900">Your Profile</h2>
          <button
            onClick={() => setShowProfileForm(!showProfileForm)}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            {showProfileForm ? 'Cancel' : 'Edit Profile'}
          </button>
        </div>

        {showProfileForm ? (
          <form onSubmit={handleUpdateProfile} className="space-y-4">
            <div>
              <label className="block text-gray-700 font-bold mb-2">
                Skills (comma-separated)
              </label>
              <input
                type="text"
                value={skills}
                onChange={(e) => setSkills(e.target.value)}
                placeholder="e.g., Python, React, JavaScript"
                className="w-full border rounded px-3 py-2"
              />
              <p className="text-sm text-gray-600 mt-1">
                Examples: Python, JavaScript, React, Data Science, UI/UX, etc.
              </p>
            </div>
            <div>
              <label className="block text-gray-700 font-bold mb-2">
                Interests (comma-separated)
              </label>
              <input
                type="text"
                value={interests}
                onChange={(e) => setInterests(e.target.value)}
                placeholder="e.g., Web Development, Machine Learning"
                className="w-full border rounded px-3 py-2"
              />
              <p className="text-sm text-gray-600 mt-1">
                Examples: Web Development, Mobile Apps, Cloud, Security, etc.
              </p>
            </div>
            <button
              type="submit"
              className="bg-green-600 text-white px-6 py-2 rounded font-bold hover:bg-green-700"
            >
              Save Profile
            </button>
          </form>
        ) : (
          <div>
            <p className="text-gray-700">
              <span className="font-bold">Skills:</span> {skills || 'Not specified'}
            </p>
            <p className="text-gray-700 mt-2">
              <span className="font-bold">Interests:</span> {interests || 'Not specified'}
            </p>
          </div>
        )}
      </div>

      {/* Recommendations List */}
      {error && (
        <div className="bg-red-100 border-2 border-red-200 text-red-700 p-4 rounded mb-6">
          {error}
        </div>
      )}

      {recommendations.length === 0 ? (
        <div className="bg-yellow-50 border-2 border-yellow-200 p-8 rounded text-center">
          <p className="text-gray-700 text-lg">
            {localStorage.getItem('access_token')
              ? 'No recommendations yet. Update your profile with skills and interests!'
              : 'Please login to see personalized recommendations'}
          </p>
        </div>
      ) : (
        <div>
          <h2 className="text-2xl font-bold mb-4">
            Recommended for You ({recommendations.length} matches)
          </h2>
          <div className="space-y-4">
            {recommendations.map((opp) => (
              <div
                key={opp.id}
                className="border-2 border-gray-200 rounded-lg p-6 hover:shadow-lg transition"
              >
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900">{opp.title}</h3>
                    <p className="text-gray-600 text-lg">{opp.company}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-3xl font-bold text-green-600">
                      {opp.match_score}%
                    </div>
                    <p className="text-sm text-gray-600">Match Score</p>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <span className="inline-block bg-purple-200 text-purple-800 px-3 py-1 rounded-full text-sm font-semibold">
                      {opp.job_type}
                    </span>
                  </div>
                  <div className="text-right">
                    <span className="inline-block bg-green-200 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">
                      Trust: {opp.trust_score}/100
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 mb-4 text-gray-700">
                  <div>
                    <span className="font-bold">📍 Location:</span> {opp.location}
                  </div>
                  <div>
                    <span className="font-bold">💰 Salary:</span> {opp.salary}
                  </div>
                </div>

                <p className="text-gray-700 mb-4">{opp.description}</p>

                <div className="flex gap-2">
                  <button className="bg-blue-600 text-white px-6 py-2 rounded font-semibold hover:bg-blue-700">
                    Learn More
                  </button>
                  <button className="border-2 border-blue-600 text-blue-600 px-6 py-2 rounded font-semibold hover:bg-blue-50">
                    Save
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default Recommendations;
