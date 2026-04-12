import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">Welcome to CareerTrust</h1>
          <p className="text-xl text-gray-700 mb-8">
            Discover legitimate career opportunities and protect yourself from scams.
          </p>
          <div className="flex gap-4 justify-center">
            <Link to="/opportunities" className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition">
              Browse Opportunities
            </Link>
            <Link to="/register" className="border-2 border-blue-600 text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition">
              Get Started
            </Link>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-white py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Why Choose CareerTrust?</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-blue-50 border-2 border-blue-200 p-8 rounded-lg">
              <h3 className="text-2xl font-bold text-blue-900 mb-4">🔍 Find Opportunities</h3>
              <p className="text-gray-700 text-lg">
                Browse internships, hackathons, and entry-level jobs aggregated from trusted sources. All in one place.
              </p>
            </div>
            <div className="bg-green-50 border-2 border-green-200 p-8 rounded-lg">
              <h3 className="text-2xl font-bold text-green-900 mb-4">✅ Trust Score</h3>
              <p className="text-gray-700 text-lg">
                Get AI-powered analysis of job postings to identify suspicious patterns and verify authenticity.
              </p>
            </div>
            <div className="bg-purple-50 border-2 border-purple-200 p-8 rounded-lg">
              <h3 className="text-2xl font-bold text-purple-900 mb-4">🎯 Smart Recommendations</h3>
              <p className="text-gray-700 text-lg">
                Personalized opportunity recommendations based on your skills, interests, and experience.
              </p>
            </div>
            <div className="bg-orange-50 border-2 border-orange-200 p-8 rounded-lg">
              <h3 className="text-2xl font-bold text-orange-900 mb-4">🛡️ Stay Safe</h3>
              <p className="text-gray-700 text-lg">
                Protect yourself from fraudulent postings and scam emails with our ML-powered detection system.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
          <div>
            <div className="text-4xl font-bold text-blue-600">500+</div>
            <p className="text-gray-700">Opportunities Listed</p>
          </div>
          <div>
            <div className="text-4xl font-bold text-blue-600">10K+</div>
            <p className="text-gray-700">Active Users</p>
          </div>
          <div>
            <div className="text-4xl font-bold text-blue-600">99%</div>
            <p className="text-gray-700">Scams Detected</p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-blue-600 text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
          <p className="text-xl mb-8 text-blue-100">Join thousands of students finding legitimate opportunities</p>
          <Link to="/register" className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition inline-block">
            Create Free Account
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Home;
