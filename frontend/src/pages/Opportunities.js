import React, { useMemo, useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';

function Opportunities() {
  const [opportunities, setOpportunities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    search: '',
    location: '',
    jobType: '',
    source: '',
    remoteOnly: false,
  });

  useEffect(() => {
    fetchOpportunities();
  }, []);

  const fetchOpportunities = async () => {
    try {
      const response = await api.get('/opportunities');
      setOpportunities(response.data.opportunities);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const filteredOpportunities = useMemo(() => {
    const searchText = filters.search.trim().toLowerCase();
    const locationText = filters.location.trim().toLowerCase();
    const sourceText = filters.source.trim().toLowerCase();

    return opportunities.filter((opp) => {
      const title = (opp.title || '').toLowerCase();
      const company = (opp.company || '').toLowerCase();
      const description = (opp.description || '').toLowerCase();
      const location = (opp.location || '').toLowerCase();
      const source = (opp.source || '').toLowerCase();
      const jobType = (opp.job_type || '').toLowerCase();

      const matchesSearch = !searchText || [title, company, description].some((field) => field.includes(searchText));
      const matchesLocation = !locationText || location.includes(locationText);
      const matchesJobType = !filters.jobType || jobType === filters.jobType.toLowerCase();
      const matchesSource = !sourceText || source.includes(sourceText);
      const matchesRemote = !filters.remoteOnly || location.includes('remote') || source.includes('remote');

      return matchesSearch && matchesLocation && matchesJobType && matchesSource && matchesRemote;
    });
  }, [filters, opportunities]);

  const jobTypes = useMemo(() => {
    return Array.from(new Set(opportunities.map((item) => item.job_type).filter(Boolean)));
  }, [opportunities]);

  const sources = useMemo(() => {
    return Array.from(new Set(opportunities.map((item) => item.source).filter(Boolean)));
  }, [opportunities]);

  const renderSkeleton = () => (
    <div className="surface-card animate-pulse p-6 md:p-8">
      <div className="h-6 w-1/3 rounded bg-slate-200" />
      <div className="mt-4 h-4 w-1/2 rounded bg-slate-100" />
      <div className="mt-6 grid gap-4 md:grid-cols-3">
        <div className="h-24 rounded-2xl bg-slate-100" />
        <div className="h-24 rounded-2xl bg-slate-100" />
        <div className="h-24 rounded-2xl bg-slate-100" />
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="page-shell">
        {renderSkeleton()}
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-shell">
        <div className="surface-card px-6 py-16 text-center text-red-700">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="page-shell space-y-8">
      <section className="surface-card p-6 md:p-8">
        <span className="section-kicker">Browse</span>
        <h1 className="section-title mt-3">Career Opportunities</h1>
        <p className="section-lead mt-3 max-w-3xl">
          Discover internships, hackathons, and entry-level jobs from trusted sources in one place.
        </p>
      </section>

      <section className="surface-card p-6 md:p-8">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
          <input
            type="text"
            value={filters.search}
            onChange={(e) => setFilters((prev) => ({ ...prev, search: e.target.value }))}
            placeholder="Search title, company, or keyword"
            className="rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 xl:col-span-2"
          />
          <input
            type="text"
            value={filters.location}
            onChange={(e) => setFilters((prev) => ({ ...prev, location: e.target.value }))}
            placeholder="Filter location"
            className="rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <select
            value={filters.jobType}
            onChange={(e) => setFilters((prev) => ({ ...prev, jobType: e.target.value }))}
            className="rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All job types</option>
            {jobTypes.map((type) => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
          <select
            value={filters.source}
            onChange={(e) => setFilters((prev) => ({ ...prev, source: e.target.value }))}
            className="rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All sources</option>
            {sources.map((source) => (
              <option key={source} value={source}>{source}</option>
            ))}
          </select>
        </div>

        <label className="mt-4 inline-flex items-center gap-3 text-sm font-medium text-slate-700">
          <input
            type="checkbox"
            checked={filters.remoteOnly}
            onChange={(e) => setFilters((prev) => ({ ...prev, remoteOnly: e.target.checked }))}
            className="h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
          />
          Remote only
        </label>

        <button
          type="button"
          onClick={() => setFilters({ search: '', location: '', jobType: '', source: '', remoteOnly: false })}
          className="ml-4 mt-4 rounded-full border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50"
        >
          Clear filters
        </button>
      </section>

      {filteredOpportunities.length > 0 ? (
        <div className="grid grid-cols-1 gap-5">
          {filteredOpportunities.map((opp) => (
            <div key={opp.id} className="surface-card p-6 transition hover:-translate-y-0.5 hover:shadow-2xl">
              <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
                <div className="space-y-3">
                  <Link to={`/opportunities/${opp.id}`} className="text-2xl font-bold text-slate-900 transition hover:text-blue-700">
                    {opp.title}
                  </Link>
                  <p className="text-lg font-medium text-slate-600">{opp.company}</p>
                  <p className="text-sm text-slate-500">{opp.location}</p>
                </div>
                <div className="rounded-full bg-emerald-50 px-4 py-2 text-sm font-semibold text-emerald-700">
                  Trust Score: {opp.trust_score}/100
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="surface-card p-8 text-center">
          <h2 className="text-2xl font-bold text-slate-900">No opportunities yet</h2>
          <p className="mt-3 text-slate-600">
            {opportunities.length === 0
              ? 'Import jobs from the integration page to populate this list with real opportunities.'
              : 'No jobs match your current filters. Try clearing one or more filters.'}
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-3">
            <button
              type="button"
              onClick={() => setFilters({ search: '', location: '', jobType: '', source: '', remoteOnly: false })}
              className="inline-flex rounded-full bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
            >
              Reset Filters
            </button>
            <Link
              to="/jobs/integration"
              className="inline-flex rounded-full border border-slate-200 px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50"
            >
              Open Job Import
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}

export default Opportunities;
