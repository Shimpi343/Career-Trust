import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bookmark, TrendingUp, LogOut, User, BadgeAlert, CheckCircle2 } from 'lucide-react';
import api from '../api';

export default function Dashboard() {
  const navigate = useNavigate();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const metricStyles = {
    blue: 'bg-blue-100 text-blue-600',
    emerald: 'bg-emerald-100 text-emerald-600',
    violet: 'bg-violet-100 text-violet-600',
    amber: 'bg-amber-100 text-amber-600',
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const response = await api.get('/analytics/dashboard');
      setDashboardData(response.data.dashboard);
      setError('');
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="page-shell">
        <div className="surface-card flex items-center justify-center px-6 py-20 text-lg text-slate-600">
          Loading dashboard...
        </div>
      </div>
    );
  }

  return (
    <div className="page-shell space-y-8">
      <section className="surface-card flex flex-col gap-6 p-6 md:flex-row md:items-end md:justify-between md:p-8">
        <div>
          <span className="section-kicker">Dashboard</span>
          <h1 className="section-title mt-3">Welcome Back</h1>
          <p className="section-lead mt-3 max-w-2xl">
            Track your profile, saved jobs, and recommendations from one clean workspace.
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <button
            onClick={() => navigate('/profile')}
            className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50"
          >
            <User size={18} />
            Profile
          </button>
          <button
            onClick={handleLogout}
            className="inline-flex items-center gap-2 rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-slate-900/10 transition hover:bg-slate-800"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>
      </section>

      {dashboardData && (
        <section className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
          {[
            {
              label: 'Profile Completion',
              value: `${dashboardData.profile_completion || 0}%`,
              tone: 'blue',
              icon: User,
              progress: dashboardData.profile_completion || 0,
            },
            {
              label: 'Saved Jobs',
              value: dashboardData.total_saved_jobs || 0,
              tone: 'emerald',
              icon: Bookmark,
            },
            {
              label: 'Applied To',
              value: dashboardData.jobs_applied_to || 0,
              tone: 'violet',
              icon: TrendingUp,
            },
            {
              label: 'Avg Match Score',
              value: `${(dashboardData.average_match_score || 0).toFixed(1)}%`,
              tone: 'amber',
              icon: TrendingUp,
            },
          ].map(({ label, value, tone, icon: Icon, progress }) => (
            <div key={label} className="surface-card p-6">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-sm font-medium text-slate-500">{label}</p>
                  <p className="mt-2 text-3xl font-extrabold tracking-tight text-slate-900">{value}</p>
                </div>
                <div className={`flex h-12 w-12 items-center justify-center rounded-2xl ${metricStyles[tone]}`}>
                  <Icon size={24} />
                </div>
              </div>
              {typeof progress === 'number' && (
                <div className="mt-4 h-2 rounded-full bg-slate-100">
                  <div
                    className="h-2 rounded-full bg-blue-600"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              )}
            </div>
          ))}
        </section>
      )}

      {dashboardData && (
        <section className="surface-card p-6 md:p-8">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <h2 className="text-2xl font-bold tracking-tight text-slate-900">Profile progress</h2>
              <p className="mt-2 text-sm text-slate-500">A quick view of your completion and the sections still missing.</p>
            </div>
            <div className="rounded-2xl bg-blue-50 px-4 py-3 text-blue-700">
              <p className="text-xs font-semibold uppercase tracking-[0.18em]">Completion</p>
              <p className="mt-1 text-3xl font-black">{dashboardData.profile_completion || 0}%</p>
            </div>
          </div>

          <div className="mt-6 h-3 rounded-full bg-slate-100">
            <div className="h-3 rounded-full bg-blue-600" style={{ width: `${dashboardData.profile_completion || 0}%` }} />
          </div>

          <div className="mt-6 grid gap-4 md:grid-cols-2">
            <div className="rounded-2xl bg-emerald-50 p-4">
              <div className="flex items-center gap-2 text-emerald-700">
                <CheckCircle2 size={18} />
                <h3 className="font-semibold">Completed</h3>
              </div>
              <p className="mt-2 text-sm text-emerald-800">
                Resume, skills, and saved activity all contribute to stronger matches.
              </p>
            </div>

            <div className="rounded-2xl bg-amber-50 p-4">
              <div className="flex items-center gap-2 text-amber-700">
                <BadgeAlert size={18} />
                <h3 className="font-semibold">Missing sections</h3>
              </div>
              {dashboardData.missing_sections?.length ? (
                <div className="mt-3 flex flex-wrap gap-2">
                  {dashboardData.missing_sections.map((section) => (
                    <span key={section} className="rounded-full bg-white px-3 py-1 text-sm font-medium text-amber-800">
                      {section}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="mt-2 text-sm text-amber-800">No missing sections right now. Nice work.</p>
              )}
            </div>
          </div>
        </section>
      )}

      <section>
        <div className="mb-6 flex items-end justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold tracking-tight text-slate-900">Quick Actions</h2>
            <p className="mt-2 text-sm text-slate-500">Move into the most common tasks in one click.</p>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          <button
            onClick={() => navigate('/recommendations')}
            className="surface-card group p-6 text-left transition hover:-translate-y-1 hover:shadow-2xl"
          >
            <div className="text-3xl mb-3">🔍</div>
            <h3 className="text-xl font-bold text-slate-900">Get Recommendations</h3>
            <p className="mt-2 text-sm leading-6 text-slate-600">Find jobs matching your skills.</p>
          </button>

          <button
            onClick={() => navigate('/saved-jobs')}
            className="surface-card group p-6 text-left transition hover:-translate-y-1 hover:shadow-2xl"
          >
            <div className="text-3xl mb-3">💾</div>
            <h3 className="text-xl font-bold text-slate-900">Saved Jobs</h3>
            <p className="mt-2 text-sm leading-6 text-slate-600">Review bookmarked jobs and mark them applied.</p>
          </button>

          <button
            onClick={() => navigate('/jobs/integration')}
            className="surface-card group p-6 text-left transition hover:-translate-y-1 hover:shadow-2xl"
          >
            <div className="text-3xl mb-3">📊</div>
            <h3 className="text-xl font-bold text-slate-900">Job Integration</h3>
            <p className="mt-2 text-sm leading-6 text-slate-600">Explore market insights.</p>
          </button>
        </div>
      </section>

      {dashboardData?.user_skills && dashboardData.user_skills.length > 0 && (
        <section className="surface-card p-6 md:p-8">
          <h2 className="text-2xl font-bold tracking-tight text-slate-900">Your Skills</h2>
          <div className="mt-5 flex flex-wrap gap-3">
            {dashboardData.user_skills.map((skill, idx) => (
              <span
                key={idx}
                className="inline-flex items-center rounded-full bg-blue-50 px-4 py-2 text-sm font-semibold text-blue-700"
              >
                {skill}
              </span>
            ))}
          </div>
        </section>
      )}

      {error && (
        <div className="surface-card border-red-200 bg-red-50 px-5 py-4 text-red-700">
          {error}
        </div>
      )}
    </div>
  );
}
