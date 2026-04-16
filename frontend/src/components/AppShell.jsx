import { Link, useLocation } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

const navItems = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/submit", label: "Submit Post" },
  { to: "/tasks", label: "Task Page" },
];

export default function AppShell({ children }) {
  const { user, logout } = useAuth();
  const location = useLocation();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <p className="eyebrow">RealLike System</p>
          <h1>Real engagement exchange</h1>
          <p className="muted">Earn credits by liking real Instagram posts from other verified users.</p>
        </div>

        <nav className="nav">
          {navItems.map((item) => (
            <Link key={item.to} className={location.pathname === item.to ? "active" : ""} to={item.to}>
              {item.label}
            </Link>
          ))}
          {user?.is_admin ? <Link className={location.pathname === "/admin" ? "active" : ""} to="/admin">Admin Panel</Link> : null}
        </nav>

        <div className="user-card">
          <strong>{user?.username}</strong>
          <span>{user?.email}</span>
          <span>{user?.credits ?? 0} credits</span>
          <button className="ghost-button" onClick={logout} type="button">
            Sign out
          </button>
        </div>
      </aside>

      <main className="content">{children}</main>
    </div>
  );
}
