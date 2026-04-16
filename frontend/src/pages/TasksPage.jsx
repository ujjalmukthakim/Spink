import { useEffect, useMemo, useState } from "react";

import { apiRequest } from "../lib/api";

export default function TasksPage() {
  const [tasks, setTasks] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTaskId, setSelectedTaskId] = useState(null);
  const [timer, setTimer] = useState(7);
  const [message, setMessage] = useState("");

  async function loadData() {
    setLoading(true);
    try {
      const [available, taskHistory] = await Promise.all([
        apiRequest("/tasks/available/"),
        apiRequest("/tasks/history/"),
      ]);
      setTasks(available.results || []);
      setHistory(taskHistory.results || []);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    if (!selectedTaskId || timer <= 0) {
      return undefined;
    }
    const timeout = window.setTimeout(() => setTimer((current) => current - 1), 1000);
    return () => window.clearTimeout(timeout);
  }, [selectedTaskId, timer]);

  const selectedTask = useMemo(
    () => tasks.find((task) => task.id === selectedTaskId) || null,
    [tasks, selectedTaskId]
  );

  function startTask(task) {
    setSelectedTaskId(task.id);
    setTimer(7);
    setMessage("");
    window.open(task.post_url, "_blank", "noopener,noreferrer");
  }

  async function confirmLike() {
    if (!selectedTask) {
      return;
    }

    try {
      await apiRequest("/tasks/confirm/", {
        method: "POST",
        body: { post_id: selectedTask.id },
      });
      setMessage("Like confirmed. You earned 1 credit.");
      setSelectedTaskId(null);
      await loadData();
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <div className="stack">
      <section className="panel">
        <h2>Available tasks</h2>
        <p className="muted">Open the Instagram post, wait 7 seconds, then confirm your like.</p>
        {loading ? (
          <p>Loading tasks...</p>
        ) : (
          <div className="task-grid">
            {tasks.map((task) => (
              <article key={task.id} className="task-card">
                <strong>@{task.owner_username}</strong>
                <a href={task.post_url} rel="noreferrer" target="_blank">
                  Open post
                </a>
                <span>
                  {task.current_likes}/{task.required_likes} likes
                </span>
                <button onClick={() => startTask(task)} type="button">
                  Start Task
                </button>
              </article>
            ))}
            {tasks.length === 0 ? <p>No tasks available right now.</p> : null}
          </div>
        )}
      </section>

      <section className="panel">
        <h3>Confirm like</h3>
        {selectedTask ? (
          <>
            <p className="muted">Task for @{selectedTask.owner_username}. Confirm unlocks after {timer} seconds.</p>
            <button disabled={timer > 0} onClick={confirmLike} type="button">
              {timer > 0 ? `Wait ${timer}s` : "Confirm Like"}
            </button>
          </>
        ) : (
          <p>Select a task to begin.</p>
        )}
        {message ? <p className="muted">{message}</p> : null}
      </section>

      <section className="panel">
        <h3>Recent task history</h3>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Post owner</th>
                <th>Credit earned</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {history.map((entry) => (
                <tr key={entry.id}>
                  <td>@{entry.post.owner_username}</td>
                  <td>{entry.credit_delta}</td>
                  <td>{new Date(entry.created_at).toLocaleString()}</td>
                </tr>
              ))}
              {history.length === 0 ? (
                <tr>
                  <td colSpan="3">No task history yet.</td>
                </tr>
              ) : null}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
