import { useEffect, useState } from "react";

import { apiRequest } from "../lib/api";

export default function AdminPage() {
  const [users, setUsers] = useState([]);
  const [logs, setLogs] = useState([]);
  const [verifications, setVerifications] = useState([]);
  const [creditForm, setCreditForm] = useState({ user_id: "", credits: "", reason: "" });
  const [banReason, setBanReason] = useState("Policy review");
  const [message, setMessage] = useState("");

  async function loadAdminData() {
    const [usersRes, logsRes, verificationsRes] = await Promise.all([
      apiRequest("/admin/users/"),
      apiRequest("/admin/logs/"),
      apiRequest("/admin/verifications/"),
    ]);
    setUsers(usersRes.results || []);
    setLogs(logsRes.results || []);
    setVerifications(verificationsRes.results || []);
  }

  useEffect(() => {
    loadAdminData();
  }, []);

  async function updateCredits(event) {
    event.preventDefault();
    try {
      await apiRequest("/admin/credit-control/", {
        method: "POST",
        body: {
          user_id: Number(creditForm.user_id),
          credits: Number(creditForm.credits),
          reason: creditForm.reason,
        },
      });
      setMessage("Credits updated.");
      setCreditForm({ user_id: "", credits: "", reason: "" });
      loadAdminData();
    } catch (error) {
      setMessage(error.message);
    }
  }

  async function toggleBan(user) {
    try {
      await apiRequest("/admin/ban-control/", {
        method: "POST",
        body: {
          user_id: user.id,
          is_banned: !user.is_banned,
          reason: banReason,
        },
      });
      setMessage("User status updated.");
      loadAdminData();
    } catch (error) {
      setMessage(error.message);
    }
  }

  async function reviewVerification(id, approve) {
    try {
      await apiRequest("/admin/verifications/", {
        method: "POST",
        body: { verification_id: id, approve },
      });
      setMessage(`Verification ${approve ? "approved" : "rejected"}.`);
      loadAdminData();
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <div className="stack">
      <section className="panel">
        <h2>CEO Control System</h2>
        <p className="muted">Manage credits, moderation, and verification approvals.</p>
        {message ? <p className="muted">{message}</p> : null}
      </section>

      <section className="panel">
        <h3>Credit control</h3>
        <form className="form-grid" onSubmit={updateCredits}>
          <input placeholder="User ID" value={creditForm.user_id} onChange={(event) => setCreditForm({ ...creditForm, user_id: event.target.value })} />
          <input placeholder="Credits" value={creditForm.credits} onChange={(event) => setCreditForm({ ...creditForm, credits: event.target.value })} />
          <input placeholder="Reason" value={creditForm.reason} onChange={(event) => setCreditForm({ ...creditForm, reason: event.target.value })} />
          <button type="submit">Apply credits</button>
        </form>
      </section>

      <section className="panel">
        <h3>Pending verifications</h3>
        <div className="task-grid">
          {verifications.map((verification) => (
            <article key={verification.id} className="task-card">
              <strong>Request #{verification.id}</strong>
              <span>User: {verification.user_username}</span>
              <span>@{verification.instagram_username}</span>
              <span>Code: {verification.verification_code}</span>
              <div className="button-row">
                <button onClick={() => reviewVerification(verification.id, true)} type="button">Approve</button>
                <button className="ghost-button" onClick={() => reviewVerification(verification.id, false)} type="button">Reject</button>
              </div>
            </article>
          ))}
          {verifications.length === 0 ? <p>No pending verifications.</p> : null}
        </div>
      </section>

      <section className="panel">
        <h3>Users</h3>
        <input placeholder="Ban reason" value={banReason} onChange={(event) => setBanReason(event.target.value)} />
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Credits</th>
                <th>Verified</th>
                <th>Banned</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.username}</td>
                  <td>{user.credits}</td>
                  <td>{user.is_verified ? "Yes" : "No"}</td>
                  <td>{user.is_banned ? "Yes" : "No"}</td>
                  <td>
                    <button onClick={() => toggleBan(user)} type="button">
                      {user.is_banned ? "Unban" : "Ban"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="panel">
        <h3>Admin logs</h3>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Admin</th>
                <th>Target</th>
                <th>Action</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log) => (
                <tr key={log.id}>
                  <td>{log.admin_username}</td>
                  <td>{log.target_username || "-"}</td>
                  <td>{log.action}</td>
                  <td>{new Date(log.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
