import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, Plus, X, Save, LogOut } from 'lucide-react';
import api from '../api';

export default function Profile() {
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('profile');
  // Resume upload
  const [uploading, setUploading] = useState(false);
  const [resumeInfo, setResumeInfo] = useState(null);

  // Skills
  const [skillInput, setSkillInput] = useState('');
  const [skillsList, setSkillsList] = useState([]);

  // Preferences
  const [preferences, setPreferences] = useState({
    min_salary: '',
    max_salary: '',
    job_type: [],
    location: [],
    industries: [],
    company_size: []
  });

  const jobTypes = ['full-time', 'part-time', 'contract', 'internship', 'freelance'];
  const locations = ['remote', 'san francisco', 'new york', 'los angeles', 'chicago'];
  const industries = ['tech', 'fintech', 'AI/ML', 'healthcare', 'education'];
  const companySizes = ['startup', 'scale-up', 'mid-size', 'enterprise'];

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await api.get('/profile/me');
      setProfile(response.data.profile);
      setSkillsList(response.data.profile.skills || []);
      setLoading(false);
    } catch (err) {
      setError('Failed to load profile');
      setLoading(false);
    }
  };

  const handleResumeUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await api.post('/profile/resume', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (response.data.success) {
        setResumeInfo(response.data);
        setSkillsList(response.data.extracted_skills || []);
        alert('Resume uploaded successfully!');
      }
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to upload resume');
    } finally {
      setUploading(false);
    }
  };

  const addSkill = () => {
    if (skillInput.trim() && !skillsList.includes(skillInput.trim())) {
      setSkillsList([...skillsList, skillInput.trim()]);
      setSkillInput('');
    }
  };

  const removeSkill = (skill) => {
    setSkillsList(skillsList.filter(s => s !== skill));
  };

  const saveSkills = async () => {
    try {
      await api.post('/profile/skills', {
        skills: skillsList,
        experience_years: profile.experience_years
      });
      alert('Skills saved!');
    } catch (err) {
      alert('Failed to save skills');
    }
  };

  const togglePreference = (key, value) => {
    if (preferences[key].includes(value)) {
      setPreferences({
        ...preferences,
        [key]: preferences[key].filter(v => v !== value)
      });
    } else {
      setPreferences({
        ...preferences,
        [key]: [...preferences[key], value]
      });
    }
  };

  const savePreferences = async () => {
    try {
      await api.post('/profile/preferences', preferences);
      alert('Preferences saved!');
    } catch (err) {
      alert('Failed to save preferences');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };

  if (loading) return <div className="text-center py-12">Loading profile...</div>;

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-6">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900">My Profile</h1>
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded font-medium"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>

        {error && <div className="mb-4 p-4 bg-red-100 text-red-700 rounded">{error}</div>}

        {/* Tabs */}
        <div className="flex gap-4 mb-8 border-b">
          <button
            onClick={() => setActiveTab('profile')}
            className={`px-4 py-2 font-medium border-b-2 ${
              activeTab === 'profile'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            Profile
          </button>
          <button
            onClick={() => setActiveTab('skills')}
            className={`px-4 py-2 font-medium border-b-2 ${
              activeTab === 'skills'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            Skills & Resume
          </button>
          <button
            onClick={() => setActiveTab('preferences')}
            className={`px-4 py-2 font-medium border-b-2 ${
              activeTab === 'preferences'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            Job Preferences
          </button>
        </div>

        {/* Profile Tab */}
        {activeTab === 'profile' && profile && (
          <div className="bg-white rounded-lg shadow p-8">
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700">Email</label>
                <p className="mt-1 text-lg text-gray-900">{profile.email}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Username</label>
                <p className="mt-1 text-lg text-gray-900">{profile.username}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Experience Level</label>
                <p className="mt-1 text-lg text-gray-900">
                  {profile.experience_years ? `${profile.experience_years} years` : 'Not specified'}
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Resume Status</label>
                {profile.resume_text ? (
                  <div className="mt-2 p-4 bg-green-50 rounded">
                    <p className="text-green-800">✅ Resume uploaded ({profile.resume_text.length} characters)</p>
                  </div>
                ) : (
                  <div className="mt-2 p-4 bg-yellow-50 rounded">
                    <p className="text-yellow-800">⚠️ No resume uploaded yet</p>
                  </div>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Member Since</label>
                <p className="text-gray-600">
                  {new Date(profile.created_at).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Skills & Resume Tab */}
        {activeTab === 'skills' && (
          <div className="space-y-8">
            {/* Resume Upload */}
            <div className="bg-white rounded-lg shadow p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Upload Resume</h2>
              <p className="text-gray-600 mb-6">
                Upload your resume to auto-extract skills and experience level. Supports PDF and DOCX files.
              </p>

              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-500 transition cursor-pointer">
                <input
                  type="file"
                  onChange={handleResumeUpload}
                  accept=".pdf,.docx,.doc"
                  disabled={uploading}
                  className="hidden"
                  id="resume-input"
                />
                <label htmlFor="resume-input" className="cursor-pointer">
                  <Upload className="mx-auto mb-3 text-gray-400" size={48} />
                  <p className="text-lg font-medium text-gray-900">
                    {uploading ? 'Uploading...' : 'Drop resume here or click to select'}
                  </p>
                  <p className="text-sm text-gray-500 mt-1">PDF, DOCX (max 5MB)</p>
                </label>
              </div>

              {resumeInfo && (
                <div className="mt-6 p-4 bg-green-50 rounded">
                  <h3 className="font-bold text-green-900 mb-2">✅ Resume Parsed Successfully</h3>
                  <p className="text-sm text-green-700">Extracted {resumeInfo.extracted_skills?.length || 0} skills</p>
                  {resumeInfo.experience_years && (
                    <p className="text-sm text-green-700">Experience: ~{resumeInfo.experience_years} years</p>
                  )}
                </div>
              )}
            </div>

            {/* Skills Management */}
            <div className="bg-white rounded-lg shadow p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Skills</h2>

              {/* Add Skill */}
              <div className="flex gap-2 mb-6">
                <input
                  type="text"
                  value={skillInput}
                  onChange={(e) => setSkillInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && addSkill()}
                  placeholder="e.g., Python, React, AWS"
                  className="flex-1 px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  onClick={addSkill}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-medium"
                >
                  <Plus size={18} />
                  Add Skill
                </button>
              </div>

              {/* Skills List */}
              <div className="flex flex-wrap gap-3 mb-8">
                {skillsList.length > 0 ? (
                  skillsList.map((skill, idx) => (
                    <div
                      key={idx}
                      className="flex items-center gap-2 bg-blue-100 text-blue-800 px-4 py-2 rounded-full"
                    >
                      <span>{skill}</span>
                      <button
                        onClick={() => removeSkill(skill)}
                        className="hover:text-blue-900"
                      >
                        <X size={16} />
                      </button>
                    </div>
                  ))
                ) : (
                  <p className="text-gray-500">No skills added yet</p>
                )}
              </div>

              <button
                onClick={saveSkills}
                className="flex items-center gap-2 px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded font-medium"
              >
                <Save size={18} />
                Save Skills
              </button>
            </div>
          </div>
        )}

        {/* Preferences Tab */}
        {activeTab === 'preferences' && (
          <div className="bg-white rounded-lg shadow p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-8">Job Search Preferences</h2>

            <div className="space-y-8">
              {/* Salary */}
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Min Salary</label>
                  <input
                    type="number"
                    value={preferences.min_salary}
                    onChange={(e) => setPreferences({ ...preferences, min_salary: e.target.value })}
                    placeholder="e.g., 60000"
                    className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Max Salary</label>
                  <input
                    type="number"
                    value={preferences.max_salary}
                    onChange={(e) => setPreferences({ ...preferences, max_salary: e.target.value })}
                    placeholder="e.g., 150000"
                    className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              {/* Job Type */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">Job Type</label>
                <div className="flex flex-wrap gap-2">
                  {jobTypes.map((type) => (
                    <button
                      key={type}
                      onClick={() => togglePreference('job_type', type)}
                      className={`px-4 py-2 rounded font-medium transition ${
                        preferences.job_type.includes(type)
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      {type}
                    </button>
                  ))}
                </div>
              </div>

              {/* Location */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">Preferred Locations</label>
                <div className="flex flex-wrap gap-2">
                  {locations.map((loc) => (
                    <button
                      key={loc}
                      onClick={() => togglePreference('location', loc)}
                      className={`px-4 py-2 rounded font-medium transition ${
                        preferences.location.includes(loc)
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      {loc}
                    </button>
                  ))}
                </div>
              </div>

              {/* Industries */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">Industries</label>
                <div className="flex flex-wrap gap-2">
                  {industries.map((ind) => (
                    <button
                      key={ind}
                      onClick={() => togglePreference('industries', ind)}
                      className={`px-4 py-2 rounded font-medium transition ${
                        preferences.industries.includes(ind)
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      {ind}
                    </button>
                  ))}
                </div>
              </div>

              {/* Company Size */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">Company Size</label>
                <div className="flex flex-wrap gap-2">
                  {companySizes.map((size) => (
                    <button
                      key={size}
                      onClick={() => togglePreference('company_size', size)}
                      className={`px-4 py-2 rounded font-medium transition ${
                        preferences.company_size.includes(size)
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      {size}
                    </button>
                  ))}
                </div>
              </div>

              <button
                onClick={savePreferences}
                className="flex items-center gap-2 px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded font-medium text-lg"
              >
                <Save size={18} />
                Save Preferences
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
