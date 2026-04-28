import React, { useEffect, useMemo, useState } from 'react';
import { CheckCircle2, Database, ExternalLink, Upload, WifiOff } from 'lucide-react';
import api from '../api';

export default function JobIntegration() {
  const [activeTab, setActiveTab] = useState('status');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSource, setSelectedSource] = useState('remoteok');
  const [loading, setLoading] = useState(false);
  const [fetchedJobs, setFetchedJobs] = useState([]);
  const [importStatus, setImportStatus] = useState(null);
  const [sourcesList, setSourcesList] = useState({});

  const sourceEntries = useMemo(() => Object.entries(sourcesList), [sourcesList]);

  useEffect(() => {
    fetchAvailableSources();
  }, []);

  const fetchAvailableSources = async () => {
    try {
      const response = await api.get('/jobs/sources');
      if (response.data.success) {
        setSourcesList(response.data.sources || {});
      }
    } catch (error) {
      console.error('Error fetching sources:', error);
      setImportStatus({
        type: 'error',
        message: 'Unable to load source status right now.'
      });
    }
  };

  const importFetchedJobs = async (jobs) => {
    if (!jobs || jobs.length === 0) {
      return null;
    }

    try {
      const response = await api.post('/jobs/import', {
        jobs,
        deduplicate: true
      });

      return response.data.success ? response.data : null;
    } catch (error) {
      console.error('Error auto-importing jobs:', error);
      return null;
    }
  };

  const handleFetchFromSource = async () => {
    setLoading(true);
    setImportStatus(null);
    setFetchedJobs([]);

    try {
      const response = await api.post(`/jobs/fetch/${selectedSource}`, {
        search_term: searchTerm || 'software engineer',
        location: 'USA',
        limit: 10
      });

      if (response.data.success) {
        const jobs = response.data.jobs || [];
        setFetchedJobs(jobs);
        setImportStatus({
          type: 'success',
          message: `Fetched ${response.data.count} jobs from ${response.data.source}`
        });

        const importedJobs = await importFetchedJobs(jobs);
        if (importedJobs) {
          setImportStatus({
            type: 'success',
            message: `Fetched ${response.data.count} jobs from ${response.data.source} and imported ${importedJobs.added} of them (${importedJobs.duplicates} duplicates skipped)`
          });
        }
      }
    } catch (error) {
      console.error('Error fetching jobs:', error);
      setImportStatus({
        type: 'error',
        message: error.response?.data?.error || 'Failed to fetch jobs'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleFetchAllSources = async () => {
    setLoading(true);
    setImportStatus(null);
    setFetchedJobs([]);

    try {
      const response = await api.post('/jobs/fetch', {
        search_term: searchTerm || 'software engineer',
        limit_per_source: 5,
        auto_add: true
      });

      if (response.data.success) {
        const allJobs = [];
        Object.values(response.data.aggregated || {}).forEach((jobs) => {
          allJobs.push(...jobs);
        });
        setFetchedJobs(allJobs);
        setImportStatus({
          type: 'success',
          message: `Fetched ${response.data.total_jobs} jobs from all sources`
        });
      }
    } catch (error) {
      console.error('Error fetching jobs:', error);
      setImportStatus({
        type: 'error',
        message: error.response?.data?.error || 'Failed to fetch jobs'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleImportJobs = async () => {
    if (fetchedJobs.length === 0) {
      setImportStatus({
        type: 'error',
        message: 'No jobs to import. Fetch jobs first.'
      });
      return;
    }

    setLoading(true);

    try {
      const response = await api.post('/jobs/import', {
        jobs: fetchedJobs,
        deduplicate: true
      });

      if (response.data.success) {
        setImportStatus({
          type: 'success',
          message: `Imported ${response.data.added} jobs (${response.data.duplicates} duplicates skipped)`
        });
        setFetchedJobs([]);
      }
    } catch (error) {
      console.error('Error importing jobs:', error);
      setImportStatus({
        type: 'error',
        message: error.response?.data?.error || 'Failed to import jobs'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-shell space-y-8">
      <section className="surface-card p-6 md:p-8">
        <span className="section-kicker">Import</span>
        <h1 className="section-title mt-3">Job Integration</h1>
        <p className="section-lead mt-3 max-w-3xl">
          Fetch real jobs from the sources wired into CareerTrust, preview them, and import only the ones you want to present.
        </p>

        <div className="mt-6 grid gap-4 md:grid-cols-3">
          {[
            { label: 'Supported now', value: 'RemoteOK, Dev.to, JustJoinIT, Stack Overflow' },
            { label: 'Optional sources', value: 'Adzuna, Jooble, Indeed, LinkedIn' },
            { label: 'Demo-friendly', value: 'Preview first, import after review' },
          ].map((item) => (
            <div key={item.label} className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">{item.label}</p>
              <p className="mt-2 text-sm leading-6 text-slate-700">{item.value}</p>
            </div>
          ))}
        </div>
      </section>

      <div className="space-y-6">
        <div className="flex gap-4 border-b border-slate-200">
          <button
            onClick={() => setActiveTab('status')}
            className={`px-4 py-2 font-medium ${
              activeTab === 'status'
                ? 'border-b-2 border-blue-600 text-blue-600'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Source Status
          </button>
          <button
            onClick={() => setActiveTab('import')}
            className={`px-4 py-2 font-medium ${
              activeTab === 'import'
                ? 'border-b-2 border-blue-600 text-blue-600'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Import Jobs
          </button>
        </div>

        {activeTab === 'status' && (
          <div className="space-y-4">
            <div className="surface-card border-blue-200 bg-blue-50 p-4">
              <p className="text-blue-900">
                <strong>Tip:</strong> RemoteOK and Dev.to are the most reliable sources for live demos. Adzuna and Jooble work when their API keys are configured.
              </p>
            </div>

            <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
              {sourceEntries.length > 0 ? (
                sourceEntries.map(([key, source]) => {
                  const isRecommended = ['remoteok', 'devto', 'demo'].includes(key);
                  const isAvailable = source.status === 'available';
                  const requiresAuthText =
                    key === 'indeed'
                      ? 'INDEED_API_KEY'
                      : key === 'linkedin'
                        ? 'LINKEDIN_EMAIL, LINKEDIN_PASSWORD'
                        : key === 'adzuna'
                          ? 'ADZUNA_APP_ID and ADZUNA_APP_KEY'
                          : key === 'jooble'
                            ? 'JOOBLE_API_KEY'
                            : 'No extra setup';

                  return (
                    <div
                      key={key}
                      className={`surface-card p-6 ${isRecommended ? 'border-2 border-green-400 bg-white' : 'bg-white'}`}
                    >
                      <div className="mb-4 flex items-start justify-between gap-3">
                        <h3 className="text-lg font-semibold text-slate-900">{source.name}</h3>
                        <div className="flex flex-wrap gap-2">
                          {isRecommended && <span className="rounded bg-green-100 px-2 py-1 text-xs font-bold text-green-800">BEST</span>}
                          <span
                            className={`rounded-full px-3 py-1 text-sm font-medium ${
                              isAvailable ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                            }`}
                          >
                            {isAvailable ? 'Available' : 'Needs config'}
                          </span>
                        </div>
                      </div>

                      <p className="mb-4 text-sm text-slate-600">{source.description}</p>

                      {source.requires_auth && (
                        <div className="mb-4 rounded border border-blue-200 bg-blue-50 p-3">
                          <p className="text-sm text-blue-900">
                            <strong>Requires:</strong> {requiresAuthText}
                          </p>
                        </div>
                      )}

                      {source.setup_url && (
                        <a
                          href={source.setup_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-sm font-medium text-blue-600 hover:text-blue-800"
                        >
                          View API setup →
                        </a>
                      )}
                    </div>
                  );
                })
              ) : (
                <div className="surface-card col-span-full p-8 text-center text-slate-600">
                  <WifiOff className="mx-auto mb-3 text-slate-400" size={28} />
                  <p>Source status is loading. Try again in a moment.</p>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'import' && (
          <div className="space-y-6">
            <div className="surface-card p-6">
              <h2 className="mb-4 text-xl font-semibold text-slate-900">Fetch Jobs</h2>

              <div className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-2">
                <input
                  type="text"
                  placeholder="Search for job titles (for example: Python Developer)"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />

                <select
                  value={selectedSource}
                  onChange={(e) => setSelectedSource(e.target.value)}
                  className="w-full rounded-xl border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <optgroup label="Recommended (Most Reliable)">
                    <option value="remoteok">RemoteOK - Remote Jobs Worldwide</option>
                    <option value="devto">Dev.to - Developer Jobs</option>
                    <option value="demo">Demo Jobs - For Testing</option>
                  </optgroup>
                  <optgroup label="Aggregator APIs">
                    <option value="adzuna">Adzuna - Aggregated Jobs</option>
                    <option value="jooble">Jooble - Aggregated Jobs</option>
                  </optgroup>
                  <optgroup label="Other Sources">
                    <option value="stackoverflow">Stack Overflow - Verified Jobs</option>
                    <option value="justjoinit">JustJoinIT - European Tech Jobs</option>
                  </optgroup>
                  <optgroup label="Requires Configuration">
                    <option value="indeed">Indeed - Large Job Board</option>
                    <option value="linkedin">LinkedIn - Professional Network</option>
                  </optgroup>
                </select>
              </div>

              <div className="flex flex-wrap gap-4">
                <button
                  onClick={handleFetchFromSource}
                  disabled={loading}
                  className="inline-flex items-center gap-2 rounded-full bg-slate-900 px-6 py-2.5 font-medium text-white transition hover:bg-slate-800 disabled:opacity-50"
                >
                  {loading ? 'Fetching...' : 'Fetch Selected Source'}
                </button>

                <button
                  onClick={handleFetchAllSources}
                  disabled={loading}
                  className="inline-flex items-center gap-2 rounded-full bg-blue-600 px-6 py-2.5 font-medium text-white transition hover:bg-blue-700 disabled:opacity-50"
                >
                  {loading ? 'Fetching...' : 'Fetch All Sources'}
                </button>
              </div>
            </div>

            {importStatus && (
              <div
                className={`surface-card p-4 ${
                  importStatus.type === 'success'
                    ? 'border border-green-200 bg-green-50'
                    : 'border border-red-200 bg-red-50'
                }`}
              >
                <p className={importStatus.type === 'success' ? 'text-green-800' : 'text-red-800'}>
                  {importStatus.type === 'success' ? <CheckCircle2 className="mr-2 inline-block" size={16} /> : null}
                  {importStatus.message}
                </p>
              </div>
            )}

            {fetchedJobs.length > 0 && (
              <div className="bg-white rounded-lg shadow p-6">
                <div className="mb-4 flex items-center justify-between gap-4">
                  <h2 className="text-xl font-semibold text-gray-900">Jobs Preview ({fetchedJobs.length})</h2>
                  <button
                    onClick={handleImportJobs}
                    disabled={loading}
                    className="inline-flex items-center gap-2 rounded-lg bg-green-600 px-6 py-2 text-white hover:bg-green-700 disabled:opacity-50 font-medium"
                  >
                    <Upload size={16} />
                    {loading ? 'Importing...' : 'Import All'}
                  </button>
                </div>

                <div className="max-h-96 space-y-4 overflow-y-auto">
                  {fetchedJobs.map((job, idx) => (
                    <div key={idx} className="rounded-lg border border-gray-200 p-4 transition hover:shadow-md">
                      <div className="mb-2 flex items-start justify-between gap-3">
                        <div>
                          <h3 className="font-semibold text-gray-900">{job.title}</h3>
                          <p className="text-sm text-gray-600">{job.company}</p>
                        </div>
                        <span className="rounded bg-blue-100 px-2 py-1 text-xs font-medium text-blue-800">{job.source}</span>
                      </div>

                      <p className="mb-2 line-clamp-2 text-sm text-gray-600">{job.description}</p>

                      <div className="flex flex-wrap gap-4 text-xs text-gray-600">
                        {job.location && <span>Location: {job.location}</span>}
                        {job.salary && <span>Salary: {job.salary}</span>}
                        <span>Trust: {job.trust_score}%</span>
                      </div>

                      {job.job_url && (
                        <a
                          href={job.job_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="mt-3 inline-flex items-center gap-2 text-sm font-semibold text-blue-700 hover:text-blue-900"
                        >
                          View source
                          <ExternalLink size={14} />
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {fetchedJobs.length === 0 && importStatus?.type === 'success' && (
              <div className="surface-card p-6 text-center text-slate-600">
                <Database className="mx-auto mb-3 text-slate-400" size={28} />
                <p>No preview rows yet. Try a broader search term or fetch from all sources.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
