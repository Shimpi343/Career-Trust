import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Briefcase, FileUp, ShieldCheck, SlidersHorizontal, Sparkles, Target } from 'lucide-react';

function Home() {
  return (
    <div className="page-shell space-y-8">
      <section className="hero-panel overflow-hidden p-8 md:p-12">
        <div className="grid gap-10 lg:grid-cols-[1.25fr_0.75fr] lg:items-center">
          <div>
            <span className="section-kicker border border-white/15 bg-white/10 text-white">CareerTrust Platform</span>
            <h1 className="mt-5 max-w-3xl text-4xl font-black tracking-tight md:text-6xl">
              Verified opportunities, smarter matching, and safer decisions in one place.
            </h1>
            <p className="mt-5 max-w-2xl text-lg leading-8 text-blue-100">
              CareerTrust helps students and early-career professionals discover real jobs faster.
              It combines resume parsing, skill matching, trust scoring, and live job aggregation so every next step feels clearer.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link to="/opportunities" className="inline-flex items-center gap-2 rounded-full bg-white px-6 py-3 font-semibold text-slate-900 transition hover:bg-slate-100">
                Explore Opportunities
                <ArrowRight size={18} />
              </Link>
              <Link to="/profile" className="rounded-full border border-white/35 px-6 py-3 font-semibold text-white transition hover:bg-white/10">
                Build My Profile
              </Link>
              <Link to="/register" className="rounded-full border border-white/20 px-6 py-3 font-semibold text-blue-50 transition hover:bg-white/10">
                Create Account
              </Link>
            </div>
          </div>

          <div className="grid gap-4">
            <div className="rounded-3xl border border-white/10 bg-white/10 p-5 backdrop-blur">
              <div className="flex items-center gap-3 text-blue-50">
                <ShieldCheck size={20} />
                <span className="text-sm font-semibold uppercase tracking-[0.2em]">Trust Layer</span>
              </div>
              <p className="mt-3 text-sm leading-6 text-blue-100">
                Scam awareness, source credibility, and transparent job metadata help make the demo feel credible.
              </p>
            </div>
            <div className="rounded-3xl border border-white/10 bg-white/10 p-5 backdrop-blur">
              <div className="flex items-center gap-3 text-blue-50">
                <Sparkles size={20} />
                <span className="text-sm font-semibold uppercase tracking-[0.2em]">AI Matching</span>
              </div>
              <p className="mt-3 text-sm leading-6 text-blue-100">
                Match scores, missing skills, and recommended next steps turn a job list into a guided workflow.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        {[
          {
            title: 'Upload Resume',
            desc: 'Extract skills from PDF or DOCX automatically and keep the profile current.',
            icon: FileUp,
          },
          {
            title: 'Set Preferences',
            desc: 'Define location, salary, and role preferences to narrow the search.',
            icon: SlidersHorizontal,
          },
          {
            title: 'See Match Status',
            desc: 'Every recommendation shows a clear match label and confidence score.',
            icon: Target,
          },
        ].map(({ title, desc, icon: Icon }) => (
          <div key={title} className="surface-card p-6">
            <Icon size={24} className="text-blue-700" />
            <h3 className="mt-3 text-xl font-bold text-slate-900">{title}</h3>
            <p className="mt-2 text-sm leading-6 text-slate-600">{desc}</p>
          </div>
        ))}
      </section>

      <section className="grid gap-4 md:grid-cols-[1.1fr_0.9fr]">
        <div className="surface-card p-6 md:p-8">
          <span className="section-kicker">Why it matters</span>
          <h2 className="mt-3 text-3xl font-bold tracking-tight text-slate-900">A presentation-ready story for industry reviewers</h2>
          <p className="mt-4 max-w-2xl leading-7 text-slate-600">
            The product demonstrates practical AI: collecting real listings, ranking them against user skills, and surfacing trust signals.
            It is easy to explain, easy to demo, and grounded in a real workflow rather than a concept slide.
          </p>
          <div className="mt-6 flex flex-wrap gap-3 text-sm font-medium text-slate-700">
            <span className="rounded-full bg-blue-50 px-4 py-2 text-blue-700">Live job sources</span>
            <span className="rounded-full bg-emerald-50 px-4 py-2 text-emerald-700">Scoring engine</span>
            <span className="rounded-full bg-amber-50 px-4 py-2 text-amber-700">Trust signals</span>
          </div>
        </div>

        <div className="surface-card p-6 md:p-8">
          <div className="flex items-center gap-3 text-slate-900">
            <Briefcase size={20} className="text-blue-700" />
            <h2 className="text-2xl font-bold tracking-tight">Recommended next step</h2>
          </div>
          <p className="mt-4 text-sm leading-7 text-slate-600">
            Start with profile setup, then open Recommendations to show how the system ranks opportunities.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link to="/profile" className="inline-flex items-center gap-2 rounded-full bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800">
              Open Profile
              <ArrowRight size={16} />
            </Link>
            <Link to="/jobs/integration" className="rounded-full border border-slate-200 px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50">
              Import Jobs
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;
