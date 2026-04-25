import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';

function Opportunities() {
  const [opportunities, setOpportunities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

  if (loading) {
    return (
      <div className="page-shell">
        <div className="surface-card px-6 py-16 text-center text-slate-600">Loading opportunities...</div>
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

      {opportunities.length > 0 ? (
        <div className="grid grid-cols-1 gap-5">
          {opportunities.map((opp) => (
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
            Import jobs from the integration page to populate this list with real opportunities.
          </p>
          <Link
            to="/jobs/integration"
            className="mt-6 inline-flex rounded-full bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
          >
            Open Job Import
          </Link>
        </div>
      )}
    </div>
  );
}

export default Opportunities;
