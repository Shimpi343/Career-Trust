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

  const toNumber = (value, fallback = 0) => {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : fallback;
  };

  const cleanDescription = (value) => {
    if (!value) {
      return '';
    }

    const parser = new DOMParser();
    const document = parser.parseFromString(value, 'text/html');
    return (document.body.textContent || '').replace(/\s+/g, ' ').trim();
  };

  const getMatchStatus = (score) => {
    const value = toNumber(score);
    if (value >= 80) {
      return { label: 'Perfect Match', className: 'bg-emerald-100 text-emerald-800' };
    }
    if (value >= 60) {
      return { label: 'Partial Match', className: 'bg-amber-100 text-amber-800' };
    }
    return { label: 'Needs Improvement', className: 'bg-rose-100 text-rose-800' };
  };

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
      <div className="page-shell">
        <div className="surface-card flex items-center justify-center px-6 py-16 text-lg text-slate-600">
          Loading recommendations...
        </div>
      </div>
    );
  }

  return (
    <div className="page-shell space-y-8">
      <section className="surface-card p-6 md:p-8">
        <span className="section-kicker">AI Matching</span>
        <h1 className="section-title mt-3">Your Match Results</h1>
        <p className="section-lead mt-3 max-w-3xl">
          Each opportunity is labeled clearly so you can decide quickly: Perfect Match, Partial Match, or Needs Improvement.
        </p>
      </section>

      <div className="space-y-8">
        {/* Header */}
        
        {userProfile && (
          <div className="surface-card p-6 md:p-8">
            <h2 className="text-2xl font-bold text-slate-900">Your Skills</h2>
            <div className="mt-5 flex flex-wrap gap-2">
              {userProfile.skills && userProfile.skills.length > 0 ? (
                userProfile.skills.map((skill, idx) => (
                  <span
                    key={idx}
                    className="rounded-full bg-blue-50 px-3 py-1 text-sm font-semibold text-blue-700"
                  >
                    {skill}
                  </span>
                ))
              ) : (
                <p className="text-slate-600">No skills added. Update your profile to get better recommendations.</p>
              )}
            </div>
            <button
              onClick={() => navigate('/profile')}
              className="mt-6 inline-flex items-center rounded-full bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800"
            >
              Update Profile
            </button>
          </div>
        )}

        {error && (
          <div className="surface-card border-red-200 bg-red-50 p-4 text-red-700">
            {error}
          </div>
        )}

        {/* Recommendations List */}
        {recommendations.length > 0 ? (
          <div className="space-y-6">
            <div className="text-sm text-slate-500">
              Found {recommendations.length} jobs matching your skills
            </div>

            {recommendations.map((job) => {
              const status = getMatchStatus(job.match_score);

              return (
                <div
                  key={job.id}
                  className="surface-card p-6 md:p-8 transition hover:-translate-y-0.5 hover:shadow-2xl"
                >
                  <div className="mb-4 flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="mb-2 text-2xl font-bold text-slate-900">{job.title}</h3>
                      <p className="mb-4 text-lg font-medium text-blue-700">{job.company}</p>
                      {(job.url || job.source_url || job.job_url) && (
                        <div className="mb-2">
                          <a
                            href={job.url || job.source_url || job.job_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-2 text-xs text-slate-500 hover:underline break-words"
                          >
                            <ExternalLink size={14} />
                            <span>{job.url || job.source_url || job.job_url}</span>
                          </a>
                        </div>
                      )}

                      <div className="mb-4 flex flex-wrap gap-6 text-slate-600">
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

                    <div className="text-right">
                      <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${status.className}`}>
                        {status.label}
                      </span>
                      <div className="mb-2 text-4xl font-bold text-emerald-600">
                        {toNumber(job.match_score).toFixed(1)}%
                      </div>
                      <p className="text-sm text-slate-500">Match Score</p>
                    </div>
                  </div>

                  <div className="mb-4 flex items-center gap-2">
                    <Star fill="gold" size={20} className="text-yellow-500" />
                    <span className="text-slate-700">
                      Trust Score: <strong>{toNumber(job.trust_score, 70)}/100</strong>
                    </span>
                  </div>

                  <div className="mb-6 grid gap-6 md:grid-cols-2">
                    <div>
                      <h4 className="mb-2 font-bold text-emerald-700">Matched Skills</h4>
                      <div className="flex flex-wrap gap-2">
                        {job.matched_skills && job.matched_skills.length > 0 ? (
                          job.matched_skills.map((skill, idx) => (
                            <span key={idx} className="rounded bg-emerald-50 px-2 py-1 text-sm text-emerald-700">
                              {skill}
                            </span>
                          ))
                        ) : (
                          <p className="text-sm text-slate-500">None</p>
                        )}
                      </div>
                    </div>

                    <div>
                      <h4 className="mb-2 font-bold text-rose-700">Skills Required But Missing</h4>
                      <p className="mb-2 text-xs leading-5 text-slate-500">
                        These are skills detected in the job description that are not currently in your profile.
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {job.missing_skills && job.missing_skills.length > 0 ? (
                          job.missing_skills.map((skill, idx) => (
                            <span key={idx} className="rounded bg-rose-50 px-2 py-1 text-sm text-rose-700">
                              {skill}
                            </span>
                          ))
                        ) : (
                          <p className="text-sm text-slate-500">None - Great match!</p>
                        )}
                      </div>
                    </div>
                  </div>

                  {job.description && (
                    <div className="mb-6">
                      <h4 className="mb-2 font-bold text-slate-900">Description</h4>
                      <p className="line-clamp-3 text-slate-600">
                        {(() => {
                          const description = cleanDescription(job.description);
                          return description.length > 300 ? `${description.substring(0, 300)}...` : description;
                        })()}
                      </p>
                    </div>
                  )}

                  <div className="flex gap-4">
                    <button
                      onClick={() => saveJob(job.id)}
                      className="flex items-center gap-2 rounded-full bg-slate-900 px-5 py-2.5 font-medium text-white transition hover:bg-slate-800"
                    >
                      <Bookmark size={18} />
                      Save Job
                    </button>
                    {job.job_url && (
                      <a
                        href={job.job_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-2 rounded-full bg-slate-100 px-5 py-2.5 font-medium text-slate-900 transition hover:bg-slate-200"
                      >
                        <ExternalLink size={18} />
                        View Job
                      </a>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="surface-card p-8 text-center">
            <h2 className="text-2xl font-bold text-slate-900">No recommendations yet</h2>
            <p className="mt-3 text-slate-600">
              Add a few skills in your profile, then import jobs so the recommendation engine has data to rank.
            </p>
            <div className="mt-6 flex flex-wrap justify-center gap-3">
              <button
                onClick={() => navigate('/profile')}
                className="rounded-full bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
              >
                Update Profile
              </button>
              <button
                onClick={() => navigate('/jobs/integration')}
                className="rounded-full border border-slate-200 px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50"
              >
                Import Jobs
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
