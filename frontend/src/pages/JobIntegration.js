import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export default function JobIntegration() {
  const [activeTab, setActiveTab] = useState('status');
  const [sources, setSources] = useState({});
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSource, setSelectedSource] = useState('github_jobs');
  const [loading, setLoading] = useState(false);
  const [fetchedJobs, setFetchedJobs] = useState([]);
  const [importStatus, setImportStatus] = useState(null);
  const [sourcesList, setSourcesList] = useState([]);

  // Fetch available sources on mount
  useEffect(() => {
    fetchAvailableSources();
  }, []);

  const fetchAvailableSources = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/jobs/sources`);
      if (response.data.success) {
        setSourcesList(response.data.sources);
      }
    } catch (error) {
      console.error('Error fetching sources:', error);
    }
  };

  const handleFetchFromSource = async () => {
    setLoading(true);
    setImportStatus(null);
    
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.post(
        `${API_BASE_URL}/jobs/fetch/${selectedSource}`,
        {
          search_term: searchTerm || 'software engineer',
          location: 'USA',
          limit: 10
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      if (response.data.success) {
        setFetchedJobs(response.data.jobs);
        setImportStatus({
          type: 'success',
          message: `Fetched ${response.data.count} jobs from ${response.data.source}`
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

  const handleFetchAllSources = async () => {
    setLoading(true);
    setImportStatus(null);

    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.post(
        `${API_BASE_URL}/jobs/fetch`,
        {
          search_term: searchTerm || 'software engineer',
          limit_per_source: 5,
          auto_add: false
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      if (response.data.success) {
        // Flatten all jobs
        const allJobs = [];
        Object.values(response.data.aggregated).forEach(jobs => {
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
      const token = localStorage.getItem('access_token');
      const response = await axios.post(
        `${API_BASE_URL}/jobs/import`,
        {
          jobs: fetchedJobs,
          deduplicate: true
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

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

  const getSourceStatus = (source) => {
    const sourceData = sourcesList[source];
    if (!sourceData) return 'unknown';
    return sourceData.status;
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Job Integration</h1>
          <p className="text-gray-600">Fetch real jobs from GitHub, Indeed, and LinkedIn</p>
        </div>

        {/* Tabs */}
        <div className="flex gap-4 mb-6 border-b border-gray-200">
          <button
            onClick={() => setActiveTab('status')}
            className={`px-4 py-2 font-medium ${
              activeTab === 'status'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Source Status
          </button>
          <button
            onClick={() => setActiveTab('import')}
            className={`px-4 py-2 font-medium ${
              activeTab === 'import'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Import Jobs
          </button>
        </div>

        {/* Status Tab */}
        {activeTab === 'status' && (
          <div className="space-y-4">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
              <p className="text-blue-900">
                <strong>💡 Tip:</strong> RemoteOK and Dev.to are the most reliable. Stack Overflow & JustJoinIT APIs may be rate-limited or unavailable. Use Demo Jobs for testing.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {Object.entries(sourcesList).map(([key, source]) => {
                // Highlight recommended sources
                const isRecommended = ['remoteok', 'devto', 'demo'].includes(key);
                
                return (
                  <div key={key} className={`rounded-lg shadow p-6 ${
                    isRecommended ? 'bg-white border-2 border-green-400' : 'bg-white'
                  }`}>
                    <div className="flex items-start justify-between mb-4">
                      <h3 className="text-lg font-semibold text-gray-900">{source.name}</h3>
                      <div className="flex gap-2">
                        {isRecommended && <span className="bg-green-100 text-green-800 text-xs font-bold px-2 py-1 rounded">⭐ BEST</span>}
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                          source.status === 'available'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {source.status.replace('_', ' ')}
                        </span>
                      </div>
                    </div>
                    
                    <p className="text-gray-600 text-sm mb-4">{source.description}</p>
                    
                    {source.requires_auth && (
                      <div className="bg-blue-50 border border-blue-200 rounded p-3 mb-4">
                        <p className="text-sm text-blue-900">
                          <strong>Requires:</strong> {key === 'indeed' ? 'INDEED_API_KEY' : 'LINKEDIN_EMAIL, LINKEDIN_PASSWORD'}
                        </p>
                      </div>
                    )}
                    
                    {source.setup_url && (
                      <a 
                        href={source.setup_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                      >
                        View API Setup →
                      </a>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Import Tab */}
        {activeTab === 'import' && (
          <div className="space-y-6">
            {/* Search & Fetch Section */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Fetch Jobs</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <input
                  type="text"
                  placeholder="Search for job titles (e.g., 'Python Developer')"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                
                <select
                  value={selectedSource}
                  onChange={(e) => setSelectedSource(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <optgroup label="⭐ Recommended (Most Reliable)">
                    <option value="remoteok">RemoteOK - Remote Jobs Worldwide</option>
                    <option value="devto">Dev.to - Developer Jobs</option>
                    <option value="demo">Demo Jobs - For Testing</option>
                  </optgroup>
                  <optgroup label="Other Sources (May be Rate-Limited)">
                    <option value="stackoverflow">Stack Overflow - Verified Jobs</option>
                    <option value="justjoinit">JustJoinIT - European Tech Jobs</option>
                  </optgroup>
                  <optgroup label="Requires Configuration">
                    <option value="indeed">Indeed - Large Job Board (API Key)</option>
                    <option value="linkedin">LinkedIn - Professional Network (Login)</option>
                  </optgroup>
                </select>
              </div>

              <div className="flex gap-4">
                <button
                  onClick={handleFetchFromSource}
                  disabled={loading}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 font-medium"
                >
                  {loading ? 'Fetching...' : 'Fetch from Selected Source'}
                </button>
                
                <button
                  onClick={handleFetchAllSources}
                  disabled={loading}
                  className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 font-medium"
                >
                  {loading ? 'Fetching...' : 'Fetch from All Sources'}
                </button>
              </div>
            </div>

            {/* Status Messages */}
            {importStatus && (
              <div className={`p-4 rounded-lg ${
                importStatus.type === 'success'
                  ? 'bg-green-50 border border-green-200'
                  : 'bg-red-50 border border-red-200'
              }`}>
                <p className={importStatus.type === 'success' ? 'text-green-800' : 'text-red-800'}>
                  {importStatus.message}
                </p>
              </div>
            )}

            {/* Jobs Preview */}
            {fetchedJobs.length > 0 && (
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">
                    Jobs Preview ({fetchedJobs.length})
                  </h2>
                  <button
                    onClick={handleImportJobs}
                    disabled={loading}
                    className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 font-medium"
                  >
                    {loading ? 'Importing...' : 'Import All'}
                  </button>
                </div>

                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {fetchedJobs.map((job, idx) => (
                    <div key={idx} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <h3 className="font-semibold text-gray-900">{job.title}</h3>
                          <p className="text-sm text-gray-600">{job.company}</p>
                        </div>
                        <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded">
                          {job.source}
                        </span>
                      </div>
                      
                      <p className="text-sm text-gray-600 line-clamp-2 mb-2">{job.description}</p>
                      
                      <div className="flex gap-4 text-xs text-gray-600">
                        {job.location && <span>📍 {job.location}</span>}
                        {job.salary && <span>💰 {job.salary}</span>}
                        <span>⭐ Trust: {job.trust_score}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
