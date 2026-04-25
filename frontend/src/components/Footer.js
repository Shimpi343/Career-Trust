import React from 'react';
import { Link } from 'react-router-dom';
import { Mail, Link as LinkIcon, Code2 } from 'lucide-react';

function Footer() {
  return (
    <footer className="mt-auto border-t border-slate-200 bg-slate-950 text-slate-300">
      <div className="mx-auto w-full max-w-7xl px-4 py-12 sm:px-6">
        <div className="grid gap-10 md:grid-cols-4">
          <div>
            <div className="mb-4 flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-400 font-extrabold text-white shadow-lg shadow-blue-500/20">CT</div>
              <span className="text-lg font-bold text-white">CareerTrust</span>
            </div>
            <p className="max-w-sm text-sm leading-6 text-slate-400">
              Finding legitimate opportunities and protecting against scams.
            </p>
          </div>

          <div>
            <h4 className="mb-4 text-sm font-semibold uppercase tracking-[0.18em] text-white">Platform</h4>
            <ul className="space-y-3 text-sm">
              <li><Link to="/opportunities" className="transition hover:text-white">Browse Opportunities</Link></li>
              <li><Link to="/recommendations" className="transition hover:text-white">Recommendations</Link></li>
              <li><Link to="/dashboard" className="transition hover:text-white">Dashboard</Link></li>
              <li><Link to="/profile" className="transition hover:text-white">Profile</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="mb-4 text-sm font-semibold uppercase tracking-[0.18em] text-white">Resources</h4>
            <ul className="space-y-3 text-sm">
              <li><a href="/#blog" className="transition hover:text-white">Blog</a></li>
              <li><a href="/#safety-guide" className="transition hover:text-white">Safety Guide</a></li>
              <li><a href="/#help-center" className="transition hover:text-white">Help Center</a></li>
              <li><a href="/#contact" className="transition hover:text-white">Contact</a></li>
            </ul>
          </div>

          <div>
            <h4 className="mb-4 text-sm font-semibold uppercase tracking-[0.18em] text-white">Connect</h4>
            <div className="flex gap-4">
              <a href="mailto:support@careertrust.com" className="transition hover:text-white">
                <Mail size={20} />
              </a>
              <button type="button" className="transition hover:text-white" aria-label="LinkedIn">
                <LinkIcon size={20} />
              </button>
              <button type="button" className="transition hover:text-white" aria-label="GitHub">
                <Code2 size={20} />
              </button>
            </div>
            <p className="mt-4 text-sm text-slate-400">support@careertrust.com</p>
          </div>
        </div>

        <div className="mt-10 border-t border-white/10 pt-6">
          <div className="flex flex-col items-center justify-between gap-4 text-sm text-slate-400 md:flex-row">
            <p>&copy; 2026 CareerTrust. All rights reserved.</p>
            <div className="flex gap-6">
              <a href="/#privacy-policy" className="transition hover:text-white">Privacy Policy</a>
              <a href="/#terms-of-service" className="transition hover:text-white">Terms of Service</a>
              <a href="/#cookie-policy" className="transition hover:text-white">Cookie Policy</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
