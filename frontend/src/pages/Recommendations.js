import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bookmark, ExternalLink, Star, MapPin, DollarSign } from 'lucide-react';
import api from '../api';

export default function Recommendations() {
  const navigate = useNavigate();
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userProfile, setUserProfile] = useState(null);
  const [selectedSkills, setSelectedSkills] = useState([]);

  const fetchUserProfile = async () => {
    try {
      const response = await api.get('/profile/me');
      setUserProfile(response.data.profile);
      setSelectedSkills(response.data.profile.skills || []);
      setLoading(false);
    } catch (err) {
      setError('Failed to load your profile');
      setLoading(false);
    }
  };

  const fetchRecommendations = React.useCallback(async () => {
    try {
      setLoading(true);
      const response = await api.post('/jobs/recommendations', {
        skills: selectedSkills,
        top_n: 10
      });
      setRecommendations(response.data.recommendations || []);
      setError(null);
    } catch (err) {
      setError('Failed to fetch recommendations');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [selectedSkills]);

  const saveJob = async (jobId) => {
    try {
      const job = recommendations.find(j => j.id === jobId);
      await api.post('/profile/save-job', {
        opportunity_id: jobId,
        match_score: job.match_score,
        notes: `Saved ${job.title} at ${job.company}`
      });
      alert('Job saved successfully!');
    } catch (err) {
      alert('Failed to save job');
      console.error(err);
    }
  };

  useEffect(() => {
    fetchUserProfile();
  }, []);

  useEffect(() => {
    if (selectedSkills.length > 0) {
      fetchRecommendations();
    }
  }, [selectedSkills, fetchRecommendations]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading recommendations...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-6xl mx-auto px-6">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            AI-Powered Job Recommendations
          </h1>
          <p className="text-gray-600 text-lg">
            Based on your skills and profile - powered by TF-IDF matching
          </p>
        </div>

        {/* Profile Card */}
        {userProfile && (
          <div className="bg-white rounded-lg shadow p-6 mb-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Your Skills</h2>
            <div className="flex flex-wrap gap-2 mb-6">
              {userProfile.skills && userProfile.skills.length > 0 ? (
                userProfile.skills.map((skill, idx) => (
                  <span
                    key={idx}
                    className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium"
                  >
                    {skill}
                  </span>
                ))
              ) : (
                <p className="text-gray-600">No skills added. Update your profile to get better recommendations.</p>
              )}
            </div>
            <button
              onClick={() => navigate('/profile')}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded font-medium"
            >
              Update Profile
            </button>
          </div>
        )}

        {error && (
          <div className="mb-8 p-4 bg-red-100 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* Recommendations List */}
        {recommendations.length > 0 ? (
          <div className="space-y-6">
            <div className="text-gray-600 mb-6">
              Found {recommendations.length} jobs matching your skills
            </div>

            {recommendations.map((job) => (
              <div
                key={job.id}
                className="bg-white rounded-lg shadow hover:shadow-lg transition p-8"
              >
                {/* Job Header */}
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">
                      {job.title}
                    </h3>
                    <p className="text-lg text-gray-600 font-medium mb-4 text-blue-600">
                      {job.company}
                    </p>

                    {/* Job Details */}
                    <div className="flex flex-wrap gap-6 mb-4 text-gray-600">
                      <div className="flex items-center gap-2">
                        <MapPin size={18} className="text-gray-400" />
                        <span>{job.location || 'Location not specified'}</span>
                      </div>
                      {job.salary && (
                        <div className="flex items-center gap-2">
                          <DollarSign size={18} className="text-gray-400" />
                          <span>{job.salary}</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Match Score Badge */}
                  <div className="text-right">
                    <div className="text-4xl font-bold text-green-600 mb-2">
                      {job.match_score.toFixed(1)}%
                    </div>
                    <p className="text-gray-600 text-sm">Match Score</p>
                  </div>
                </div>

                {/* Trust Score */}
                <div className="mb-4 flex items-center gap-2">
                  <Star fill="gold" size={20} className="text-yellow-500" />
                  <span className="text-gray-700">
                    Trust Score: <strong>{job.trust_score}/100</strong>
                  </span>
                </div>

                {/* Skills */}
                <div className="grid grid-cols-2 gap-6 mb-6">
                  <div>
                    <h4 className="font-bold text-green-700 mb-2">✅ Matched Skills</h4>
                    <div className="flex flex-wrap gap-2">
                      {job.matched_skills && job.matched_skills.length > 0 ? (
                        job.matched_skills.map((skill, idx) => (
                          <span
                            key={idx}
                            className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm"
                          >
                            {skill}
                          </span>
                        ))
                      ) : (
                        <p className="text-gray-500 text-sm">None</p>
                      )}
                    </div>
                  </div>

                  <div>
                    <h4 className="font-bold text-red-700 mb-2">❌ Missing Skills</h4>
                    <div className="flex flex-wrap gap-2">
                      {job.missing_skills && job.missing_skills.length > 0 ? (
                        job.missing_skills.map((skill, idx) => (
                          <span
                            key={idx}
                            className="bg-red-100 text-red-800 px-2 py-1 rounded text-sm"
                          >
                            {skill}
                          </span>
                        ))
                      ) : (
                        <p className="text-gray-500 text-sm">None - Great match!</p>
                      )}
                    </div>
                  </div>
                </div>

                {/* Description */}
                {job.description && (
                  <div className="mb-6">
                    <h4 className="font-bold text-gray-900 mb-2">Description</h4>
                    <p className="text-gray-600 line-clamp-3">
                      {job.description.substring(0, 300)}...
                    </p>
                  </div>
                )}

                {/* Actions */}
                <div className="flex gap-4">
                  <button
                    onClick={() => saveJob(job.id)}
                    className="flex items-center gap-2 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-medium transition"
                  >
                    <Bookmark size={18} />
                    Save Job
                  </button>
                  {job.job_url && (
                    <a
                      href={job.job_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2 px-6 py-2 bg-gray-200 hover:bg-gray-300 text-gray-900 rounded font-medium transition"
                    >
                      <ExternalLink size={18} />
                      View Job
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <p className="text-xl text-gray-600 mb-4">
              No recommendations yet. Add skills to your profile to get started!
            </p>
            <button
              onClick={() => navigate('/profile')}
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded font-medium"
            >
              Update Profile with Skills
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
