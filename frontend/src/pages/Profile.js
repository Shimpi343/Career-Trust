import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, Plus, X, Save, ArrowRight } from 'lucide-react';
import api from '../api';

export default function Profile() {
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const [resumeInfo, setResumeInfo] = useState(null);
  const [skillInput, setSkillInput] = useState('');
  const [skillsList, setSkillsList] = useState([]);

  const [preferences, setPreferences] = useState({
    min_salary: '',
    max_salary: '',
    job_type: [],
    location: [],
    industries: [],
    company_size: []
  });

  const [locationInput, setLocationInput] = useState('');
  const [industryInput, setIndustryInput] = useState('');

  const jobTypes = ['full-time', 'part-time', 'internship', 'contract'];
  const companySizes = ['startup', 'mid-size', 'enterprise'];

  const parseCsvToArray = (value) => {
    return value
      .split(',')
      .map((item) => item.trim().toLowerCase())
      .filter(Boolean);
  };

  const extractApiError = (err, fallback) => {
    const message =
      err?.response?.data?.error ||
      err?.response?.data?.msg ||
      err?.response?.data?.message ||
      err?.message;

    return typeof message === 'string' && message.trim() ? message : fallback;
  };

  const fetchProfile = useCallback(async () => {
    try {
      const response = await api.get('/profile/me');
      const profileData = response.data.profile || {};
      const pref = profileData.preferences || {};

      setProfile(profileData);
      setSkillsList(profileData.skills || []);
      setPreferences({
        min_salary: pref.min_salary || '',
        max_salary: pref.max_salary || '',
        job_type: pref.job_type || [],
        location: pref.location || [],
        industries: pref.industries || [],
        company_size: pref.company_size || []
      });
      setLocationInput((pref.location || []).join(', '));
      setIndustryInput((pref.industries || []).join(', '));
      setError('');
    } catch (err) {
      setError(extractApiError(err, 'Failed to load profile'));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  const addSkill = () => {
    const trimmed = skillInput.trim().toLowerCase();
    if (!trimmed) return;

    if (!skillsList.includes(trimmed)) {
      setSkillsList((prev) => [...prev, trimmed]);
    }
    setSkillInput('');
  };

  const removeSkill = (skill) => {
    setSkillsList((prev) => prev.filter((s) => s !== skill));
  };

  const togglePreference = (key, value) => {
    setPreferences((prev) => ({
      ...prev,
      [key]: prev[key].includes(value)
        ? prev[key].filter((v) => v !== value)
        : [...prev[key], value]
    }));
  };

  const handleResumeUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    setError('');
    setSuccess('');

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await api.post('/profile/resume', formData);

      if (response.data.success) {
        setResumeInfo(response.data);
        if (response.data.extracted_skills?.length) {
          setSkillsList((prev) => {
            const merged = new Set([...prev, ...response.data.extracted_skills.map((s) => s.toLowerCase())]);
            return [...merged];
          });
        }
        setSuccess('Resume uploaded and parsed successfully.');
        setProfile((prev) => (prev ? { ...prev, resume_text: true } : prev));
      }
    } catch (err) {
      setError(extractApiError(err, 'Failed to upload resume'));
    } finally {
      setUploading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setError('');
    setSuccess('');

    const normalizedPreferences = {
      ...preferences,
      location: parseCsvToArray(locationInput),
      industries: parseCsvToArray(industryInput)
    };

    try {
      await api.post('/profile/skills', {
        skills: skillsList,
        experience_years: profile?.experience_years || 0
      });

      await api.post('/profile/preferences', normalizedPreferences);

      setPreferences(normalizedPreferences);
      setSuccess('Profile saved successfully. You can now check match results.');
    } catch (err) {
      setError(extractApiError(err, 'Failed to save profile'));
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="page-shell">
        <div className="surface-card px-6 py-16 text-center text-slate-600">Loading profile...</div>
      </div>
    );
  }

  return (
    <div className="page-shell space-y-6">
      <section className="surface-card p-6 md:p-8">
        <span className="section-kicker">Step 1</span>
        <h1 className="section-title mt-3">Build Your Match Profile</h1>
        <p className="section-lead mt-3 max-w-3xl">
          Keep it simple: upload resume, add your skills, and set preferences.
          Then check recommendations with clear match status.
        </p>

        {error && <div className="mt-5 rounded-xl border border-rose-200 bg-rose-50 p-4 text-rose-700">{error}</div>}
        {success && <div className="mt-5 rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-emerald-700">{success}</div>}
      </section>

      <section className="surface-card p-6 md:p-8">
        <h2 className="text-2xl font-bold text-slate-900">Resume</h2>
        <p className="mt-2 text-slate-600">Upload PDF or DOCX and we will auto-extract skills.</p>

        <div className="mt-5 rounded-2xl border-2 border-dashed border-slate-300 p-8 text-center transition hover:border-blue-500">
          <input
            id="resume-input"
            type="file"
            accept=".pdf,.docx"
            onChange={handleResumeUpload}
            disabled={uploading}
            className="hidden"
          />
          <label htmlFor="resume-input" className="cursor-pointer">
            <Upload className="mx-auto text-slate-400" size={40} />
            <p className="mt-3 text-lg font-semibold text-slate-900">
              {uploading ? 'Uploading...' : 'Click to upload resume'}
            </p>
            <p className="mt-1 text-sm text-slate-500">PDF, DOCX</p>
          </label>
        </div>

        <div className="mt-4 text-sm text-slate-600">
          Resume status: {profile?.resume_text ? 'Uploaded' : 'Not uploaded'}
        </div>

        {resumeInfo && (
          <div className="mt-4 rounded-xl bg-blue-50 p-4 text-sm text-blue-800">
            Parsed skills: {resumeInfo.extracted_skills?.length || 0}
          </div>
        )}
      </section>

      <section className="surface-card p-6 md:p-8">
        <h2 className="text-2xl font-bold text-slate-900">Skills</h2>
        <p className="mt-2 text-slate-600">Add the skills you want to be matched against jobs.</p>

        <div className="mt-5 flex gap-2">
          <input
            type="text"
            value={skillInput}
            onChange={(e) => setSkillInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && addSkill()}
            placeholder="e.g. python, react, sql"
            className="w-full rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="button"
            onClick={addSkill}
            className="inline-flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-3 font-semibold text-white"
          >
            <Plus size={16} /> Add
          </button>
        </div>

        <div className="mt-4 flex flex-wrap gap-2">
          {skillsList.length > 0 ? (
            skillsList.map((skill) => (
              <span key={skill} className="inline-flex items-center gap-2 rounded-full bg-blue-50 px-3 py-1.5 text-sm font-medium text-blue-700">
                {skill}
                <button type="button" onClick={() => removeSkill(skill)} className="text-blue-800">
                  <X size={14} />
                </button>
              </span>
            ))
          ) : (
            <p className="text-sm text-slate-500">No skills added yet.</p>
          )}
        </div>
      </section>

      <section className="surface-card p-6 md:p-8">
        <h2 className="text-2xl font-bold text-slate-900">Preferences</h2>
        <p className="mt-2 text-slate-600">Set your job preferences for better recommendations.</p>

        <div className="mt-5 grid gap-4 md:grid-cols-2">
          <input
            type="number"
            value={preferences.min_salary}
            onChange={(e) => setPreferences((prev) => ({ ...prev, min_salary: e.target.value }))}
            placeholder="Minimum salary"
            className="rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="number"
            value={preferences.max_salary}
            onChange={(e) => setPreferences((prev) => ({ ...prev, max_salary: e.target.value }))}
            placeholder="Maximum salary"
            className="rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="mt-4">
          <p className="mb-2 text-sm font-semibold text-slate-700">Job Type</p>
          <div className="flex flex-wrap gap-2">
            {jobTypes.map((type) => (
              <button
                key={type}
                type="button"
                onClick={() => togglePreference('job_type', type)}
                className={`rounded-full px-4 py-2 text-sm font-medium transition ${
                  preferences.job_type.includes(type)
                    ? 'bg-slate-900 text-white'
                    : 'bg-slate-100 text-slate-700'
                }`}
              >
                {type}
              </button>
            ))}
          </div>
        </div>

        <div className="mt-4 grid gap-4 md:grid-cols-2">
          <input
            type="text"
            value={locationInput}
            onChange={(e) => setLocationInput(e.target.value)}
            placeholder="Preferred locations (comma separated)"
            className="rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="text"
            value={industryInput}
            onChange={(e) => setIndustryInput(e.target.value)}
            placeholder="Industries (comma separated)"
            className="rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="mt-4">
          <p className="mb-2 text-sm font-semibold text-slate-700">Company Size</p>
          <div className="flex flex-wrap gap-2">
            {companySizes.map((size) => (
              <button
                key={size}
                type="button"
                onClick={() => togglePreference('company_size', size)}
                className={`rounded-full px-4 py-2 text-sm font-medium transition ${
                  preferences.company_size.includes(size)
                    ? 'bg-slate-900 text-white'
                    : 'bg-slate-100 text-slate-700'
                }`}
              >
                {size}
              </button>
            ))}
          </div>
        </div>
      </section>

      <section className="surface-card flex flex-col gap-3 p-6 md:flex-row md:items-center md:justify-between">
        <div>
          <h3 className="text-xl font-bold text-slate-900">Ready to check your match?</h3>
          <p className="mt-1 text-slate-600">Save profile first, then view recommendations.</p>
        </div>

        <div className="flex gap-3">
          <button
            type="button"
            onClick={handleSave}
            disabled={saving}
            className="inline-flex items-center gap-2 rounded-full bg-slate-900 px-5 py-3 font-semibold text-white disabled:opacity-60"
          >
            <Save size={16} /> {saving ? 'Saving...' : 'Save Profile'}
          </button>
          <button
            type="button"
            onClick={() => navigate('/recommendations')}
            className="inline-flex items-center gap-2 rounded-full border border-slate-300 px-5 py-3 font-semibold text-slate-800"
          >
            View Results <ArrowRight size={16} />
          </button>
        </div>
      </section>
    </div>
  );
}
