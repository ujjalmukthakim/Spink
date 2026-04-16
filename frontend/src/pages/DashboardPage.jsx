import { useEffect, useState } from "react";

import StatCard from "../components/StatCard";
import { useAuth } from "../context/AuthContext";
import { apiRequest } from "../lib/api";

export default function DashboardPage() {
  const { refreshUser } = useAuth();
  const [dashboard, setDashboard] = useState(null);
  const [verificationUsername, setVerificationUsername] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState("");

  async function loadDashboard() {
    setLoading(true);
    try {
      const data = await apiRequest("/users/dashboard/");
      setDashboard(data);
      setVerificationUsername(data.user.instagram_username || "");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  async function handleVerification(event) {
    event.preventDefault();
    setSubmitting(true);
    setMessage("");
    try {
      await apiRequest("/users/verification/", {
        method: "POST",
        body: { instagram_username: verificationUsername },
      });
      await refreshUser();
      await loadDashboard();
      setMessage("Verification code generated. Add it to your Instagram bio and wait for admin approval.");
    } catch (error) {
      setMessage(error.message);
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <section className="panel">Loading dashboard...</section>;
  }

  return (
    <div className="stack">
      <section className="hero-panel">
        <div>
          <p className="eyebrow">Dashboard</p>
          <h2>{dashboard.user.is_verified ? "Verified and active" : "Verification required"}</h2>
          <p className="muted">
            Credits: {dashboard.user.credits} | Trust score: {dashboard.user.trust_score}
          </p>
        </div>
        <div className={`pill ${dashboard.user.is_verified ? "ok" : "warn"}`}>
          {dashboard.user.is_verified ? "Instagram verified" : "Pending verification"}
        </div>
      </section>

      <section className="stats-grid">
        <StatCard label="Credits" value={dashboard.user.credits} accent="accent-a" />
        <StatCard label="Likes given" value={dashboard.stats.likes_given} accent="accent-b" />
        <StatCard label="Likes received" value={dashboard.stats.likes_received} accent="accent-c" />
        <StatCard label="Active posts" value={dashboard.stats.active_posts} accent="accent-d" />
      </section>

      <section className="panel">
        <h3>Instagram verification</h3>
        <p className="muted">Enter your Instagram username, get a verification code, place it in your bio, and wait for manual approval.</p>
        <form className="inline-form" onSubmit={handleVerification}>
          <input value={verificationUsername} onChange={(event) => setVerificationUsername(event.target.value)} placeholder="Instagram username" />
          <button disabled={submitting} type="submit">
            {submitting ? "Submitting..." : "Generate Code"}
          </button>
        </form>
        {dashboard.pending_verification ? (
          <div className="callout">
            <strong>Current code:</strong> {dashboard.pending_verification.verification_code}
          </div>
        ) : null}
        {message ? <p className="muted">{message}</p> : null}
      </section>
    </div>
  );
}
