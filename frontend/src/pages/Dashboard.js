import React from 'react';

function Dashboard() {
  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">Your Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg border">
          <h2 className="text-2xl font-bold">Applications</h2>
          <p className="text-3xl font-bold text-blue-600">0</p>
        </div>
        <div className="bg-white p-6 rounded-lg border">
          <h2 className="text-2xl font-bold">Saved Opportunities</h2>
          <p className="text-3xl font-bold text-blue-600">0</p>
        </div>
        <div className="bg-white p-6 rounded-lg border">
          <h2 className="text-2xl font-bold">Alerts</h2>
          <p className="text-3xl font-bold text-red-600">0</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
