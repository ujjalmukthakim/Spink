import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function RegisterPage() {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    instagram_username: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      await register(form);
      setSuccess("Account created. You can log in now.");
      setTimeout(() => navigate("/login"), 1000);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <p className="eyebrow">Get Started</p>
        <h1>Create your account</h1>
        <input placeholder="Username" value={form.username} onChange={(event) => setForm({ ...form, username: event.target.value })} />
        <input placeholder="Email" type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} />
        <input placeholder="Password" type="password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} />
        <input
          placeholder="Instagram username"
          value={form.instagram_username}
          onChange={(event) => setForm({ ...form, instagram_username: event.target.value })}
        />
        {error ? <p className="error-text">{error}</p> : null}
        {success ? <p className="success-text">{success}</p> : null}
        <button disabled={loading} type="submit">
          {loading ? "Creating..." : "Register"}
        </button>
        <p className="muted small">
          Already registered? <Link to="/login">Login</Link>
        </p>
      </form>
    </div>
  );
}
