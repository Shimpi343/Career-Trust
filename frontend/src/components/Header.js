import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Home as HomeIcon, Star, User, LogIn, UserPlus, Briefcase, LayoutDashboard, Compass, LogOut } from 'lucide-react';

function Header() {
  const location = useLocation();
  const navigate = useNavigate();
  const isAuthenticated = Boolean(localStorage.getItem('access_token'));

  const isActive = (path) => location.pathname === path;

  const publicNavLinks = [
    { path: '/', label: 'Home', icon: HomeIcon },
  ];

  const privateNavLinks = [
    { path: '/recommendations', label: 'Recommendations', icon: Star },
    { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/jobs/integration', label: 'Jobs', icon: Briefcase },
    { path: '/profile', label: 'Profile', icon: User },
  ];

  const navLinks = isAuthenticated ? privateNavLinks : publicNavLinks;

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200/80 bg-white/85 backdrop-blur-xl shadow-sm">
      <nav className="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-4 sm:px-6">
        <Link to={isAuthenticated ? '/dashboard' : '/'} className="flex items-center gap-3 transition hover:opacity-80">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-cyan-500 text-sm font-extrabold text-white shadow-lg shadow-blue-500/20">
            CT
          </div>
          <div>
            <span className="block text-lg font-extrabold tracking-tight text-slate-900">CareerTrust</span>
            <span className="block text-xs font-medium uppercase tracking-[0.24em] text-slate-500">Verified opportunities</span>
          </div>
        </Link>

        <ul className="hidden items-center gap-1 rounded-full border border-slate-200 bg-slate-50/80 p-1 lg:flex">
          {navLinks.map(({ path, label, icon: Icon }) => (
            <li key={path}>
              <Link
                to={path}
                className={`flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium transition ${
                  isActive(path)
                    ? 'bg-slate-900 text-white shadow-sm'
                    : 'text-slate-600 hover:bg-white hover:text-slate-900'
                }`}
              >
                <Icon size={18} />
                <span>{label}</span>
              </Link>
            </li>
          ))}
        </ul>

        <div className="flex items-center gap-2 sm:gap-3">
          {isAuthenticated ? (
            <>
              <button
                type="button"
                onClick={handleLogout}
                className="flex items-center gap-2 rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-slate-900/15 transition hover:bg-slate-800"
              >
                <LogOut size={18} />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="flex items-center gap-2 rounded-full border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50"
              >
                <LogIn size={18} />
                <span className="hidden sm:inline">Login</span>
              </Link>

              <Link
                to="/register"
                className="flex items-center gap-2 rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-slate-900/15 transition hover:bg-slate-800"
              >
                <UserPlus size={18} />
                <span className="hidden sm:inline">Register</span>
              </Link>
            </>
          )}
        </div>
      </nav>

      <div className="border-t border-slate-200/80 px-4 py-3 lg:hidden sm:px-6">
        <div className="flex gap-2 overflow-x-auto">
          {navLinks.map(({ path, label, icon: Icon }) => (
            <Link
              key={path}
              to={path}
              className={`flex items-center gap-2 whitespace-nowrap rounded-full px-3 py-2 text-sm font-medium transition ${
                isActive(path)
                  ? 'bg-slate-900 text-white'
                  : 'border border-slate-200 bg-white text-slate-600 hover:border-slate-300 hover:text-slate-900'
              }`}
            >
              <Icon size={16} />
              <span className="text-sm">{label}</span>
            </Link>
          ))}
        </div>
      </div>
    </header>
  );
}

export default Header;
