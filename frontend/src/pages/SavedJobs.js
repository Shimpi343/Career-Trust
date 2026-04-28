import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { BookmarkCheck, BriefcaseBusiness, ExternalLink, Trash2, BadgeCheck } from 'lucide-react';
import api from '../api';

export default function SavedJobs() {
  const navigate = useNavigate();
  const [savedJobs, setSavedJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [actionLoadingId, setActionLoadingId] = useState(null);
  const [filters, setFilters] = useState({
    status: 'all',
    source: '',
    search: '',
  });

  useEffect(() => {
    fetchSavedJobs();
  }, []);

  const fetchSavedJobs = async () => {
    try {
      setLoading(true);
      const response = await api.get('/profile/saved-jobs');
      setSavedJobs(response.data.saved_jobs || []);
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load saved jobs');
    } finally {
      setLoading(false);
    }
  };

  const filteredJobs = useMemo(() => {
    const search = filters.search.trim().toLowerCase();
    const source = filters.source.trim().toLowerCase();

    return savedJobs.filter((entry) => {
      const job = entry.job || {};
      const statusMatch =
        filters.status === 'all' ||
        (filters.status === 'applied' && entry.applied) ||
        (filters.status === 'saved' && !entry.applied);
      const sourceMatch = !source || (job.source || '').toLowerCase().includes(source);
      const searchMatch =
        !search ||
        [job.title, job.company, job.location, job.source]
          .filter(Boolean)
          .some((field) => field.toLowerCase().includes(search));

      return statusMatch && sourceMatch && searchMatch;
    });
  }, [filters, savedJobs]);

  const uniqueSources = useMemo(() => {
    return Array.from(new Set(savedJobs.map((entry) => entry.job?.source).filter(Boolean)));
  }, [savedJobs]);

  const markApplied = async (savedJobId) => {
    try {
      setActionLoadingId(savedJobId);
      await api.post('/profile/mark-applied', { saved_job_id: savedJobId });
      await fetchSavedJobs();
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to update job status');
    } finally {
      setActionLoadingId(null);
    }
  };

  const removeSavedJob = async (savedJobId) => {
    try {
      setActionLoadingId(savedJobId);
      await api.delete(`/profile/unsave-job/${savedJobId}`);
      setSavedJobs((prev) => prev.filter((entry) => entry.saved_job_id !== savedJobId));
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to remove saved job');
    } finally {
      setActionLoadingId(null);
    }
  };

  const renderSkeleton = () => (
    <div className="surface-card animate-pulse space-y-4 p-6 md:p-8">
      <div className="h-8 w-1/3 rounded bg-slate-200" />
      <div className="grid gap-4 md:grid-cols-3">
        <div className="h-12 rounded-xl bg-slate-100" />
        <div className="h-12 rounded-xl bg-slate-100" />
        <div className="h-12 rounded-xl bg-slate-100" />
      </div>
      <div className="h-40 rounded-2xl bg-slate-100" />
      <div className="h-40 rounded-2xl bg-slate-100" />
    </div>
  );

  if (loading) {
    return <div className="page-shell">{renderSkeleton()}</div>;
  }

  return (
    <div className="page-shell space-y-8">
      <section className="surface-card p-6 md:p-8">
        <span className="section-kicker">Saved</span>
        <h1 className="section-title mt-3">Saved Jobs</h1>
        <p className="section-lead mt-3 max-w-3xl">
          Keep every bookmarked job in one place, mark applications as you go, and filter by status or source.
        </p>
      </section>

      <section className="surface-card p-6 md:p-8">
        <div className="grid gap-4 md:grid-cols-3">
          <input
            type="text"
            value={filters.search}
            onChange={(e) => setFilters((prev) => ({ ...prev, search: e.target.value }))}
            placeholder="Search title, company, or location"
            className="rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <select
            value={filters.status}
            onChange={(e) => setFilters((prev) => ({ ...prev, status: e.target.value }))}
            className="rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All jobs</option>
            <option value="saved">Saved only</option>
            <option value="applied">Applied only</option>
          </select>
          <select
            value={filters.source}
            onChange={(e) => setFilters((prev) => ({ ...prev, source: e.target.value }))}
            className="rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All sources</option>
            {uniqueSources.map((source) => (
              <option key={source} value={source}>{source}</option>
            ))}
          </select>
        </div>

        <button
          type="button"
          onClick={() => setFilters({ status: 'all', source: '', search: '' })}
          className="mt-4 rounded-full border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50"
        >
          Clear filters
        </button>
      </section>

      {error && (
        <div className="surface-card border border-rose-200 bg-rose-50 p-4 text-rose-700">{error}</div>
      )}

      {filteredJobs.length > 0 ? (
        <div className="space-y-5">
          {filteredJobs.map((entry) => {
            const job = entry.job || {};
            const applied = Boolean(entry.applied);
            const sourceUrl = job.url || job.job_url || '#';

            return (
              <article key={entry.saved_job_id} className="surface-card p-6 md:p-8 transition hover:-translate-y-0.5 hover:shadow-2xl">
                <div className="flex flex-col gap-5 md:flex-row md:items-start md:justify-between">
                  <div className="flex-1 space-y-3">
                    <div className="flex items-center gap-2">
                      <BookmarkCheck className={applied ? 'text-emerald-600' : 'text-slate-400'} size={20} />
                      <span className={`rounded-full px-3 py-1 text-xs font-semibold ${applied ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}`}>
                        {applied ? 'Applied' : 'Saved'}
                      </span>
                    </div>

                    <h2 className="text-2xl font-bold text-slate-900">{job.title}</h2>
                    <p className="text-lg font-medium text-blue-700">{job.company}</p>
                    <p className="text-sm text-slate-500">{job.location || 'Location not specified'}</p>
                    <p className="text-sm text-slate-500">Source: {job.source || 'Unknown'}</p>
                    {entry.applied_at && (
                      <p className="text-sm text-slate-500">Applied on {new Date(entry.applied_at).toLocaleDateString()}</p>
                    )}
                  </div>

                  <div className="flex flex-wrap gap-3 md:justify-end">
                    <a
                      href={sourceUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 rounded-full bg-slate-100 px-4 py-2 text-sm font-semibold text-slate-800 transition hover:bg-slate-200"
                    >
                      <ExternalLink size={16} />
                      Open Source
                    </a>
                    {!applied && (
                      <button
                        type="button"
                        onClick={() => markApplied(entry.saved_job_id)}
                        disabled={actionLoadingId === entry.saved_job_id}
                        className="inline-flex items-center gap-2 rounded-full bg-emerald-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-emerald-700 disabled:opacity-60"
                      >
                        <BadgeCheck size={16} />
                        {actionLoadingId === entry.saved_job_id ? 'Updating...' : 'Mark Applied'}
                      </button>
                    )}
                    <button
                      type="button"
                      onClick={() => removeSavedJob(entry.saved_job_id)}
                      disabled={actionLoadingId === entry.saved_job_id}
                      className="inline-flex items-center gap-2 rounded-full border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-rose-200 hover:bg-rose-50 hover:text-rose-700 disabled:opacity-60"
                    >
                      <Trash2 size={16} />
                      Remove
                    </button>
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      ) : (
        <div className="surface-card p-8 text-center">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-slate-100 text-slate-500">
            <BriefcaseBusiness size={28} />
          </div>
          <h2 className="mt-4 text-2xl font-bold text-slate-900">
            {savedJobs.length === 0 ? 'No saved jobs yet' : 'No jobs match your filters'}
          </h2>
          <p className="mt-3 text-slate-600">
            {savedJobs.length === 0
              ? 'Save jobs from Recommendations or Browse Jobs to keep them here.'
              : 'Try clearing the filters to see more saved jobs.'}
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-3">
            <button
              type="button"
              onClick={() => navigate('/recommendations')}
              className="inline-flex rounded-full bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
            >
              Explore Recommendations
            </button>
            <button
              type="button"
              onClick={() => setFilters({ status: 'all', source: '', search: '' })}
              className="inline-flex rounded-full border border-slate-200 px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50"
            >
              Reset Filters
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
