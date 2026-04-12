import React, { useState, useEffect } from 'react';
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

  if (loading) return <div className="container mx-auto px-4 py-12">Loading...</div>;
  if (error) return <div className="container mx-auto px-4 py-12">Error: {error}</div>;

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">Career Opportunities</h1>
      <div className="grid grid-cols-1 gap-6">
        {opportunities.map((opp) => (
          <div key={opp.id} className="border rounded-lg p-6 hover:shadow-lg">
            <h2 className="text-2xl font-bold">{opp.title}</h2>
            <p className="text-gray-700">{opp.company}</p>
            <p className="text-sm text-gray-500 mt-2">{opp.location}</p>
            <div className="mt-4">
              <span className="inline-block bg-green-200 px-3 py-1 rounded-full text-sm">
                Trust Score: {opp.trust_score}/100
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Opportunities;
