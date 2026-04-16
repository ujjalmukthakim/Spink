import { useEffect, useState } from "react";

import { apiRequest } from "../lib/api";

export default function SubmitPostPage() {
  const [posts, setPosts] = useState([]);
  const [form, setForm] = useState({ post_url: "", required_likes: 10 });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  async function loadPosts() {
    setLoading(true);
    try {
      const response = await apiRequest("/posts/");
      setPosts(response.results || []);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadPosts();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setSaving(true);
    setMessage("");
    try {
      await apiRequest("/posts/", {
        method: "POST",
        body: {
          post_url: form.post_url,
          required_likes: Number(form.required_likes),
        },
      });
      setForm({ post_url: "", required_likes: 10 });
      setMessage("Post added to the exchange queue.");
      loadPosts();
    } catch (error) {
      setMessage(error.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="stack">
      <section className="panel">
        <h2>Submit an Instagram post</h2>
        <p className="muted">Only post URLs are stored. Media never touches the server.</p>
        <form className="form-grid" onSubmit={handleSubmit}>
          <input placeholder="https://www.instagram.com/p/..." value={form.post_url} onChange={(event) => setForm({ ...form, post_url: event.target.value })} />
          <input
            min="1"
            max="500"
            type="number"
            value={form.required_likes}
            onChange={(event) => setForm({ ...form, required_likes: event.target.value })}
          />
          <button disabled={saving} type="submit">
            {saving ? "Submitting..." : "Submit Post"}
          </button>
        </form>
        {message ? <p className="muted">{message}</p> : null}
      </section>

      <section className="panel">
        <h3>Your submitted posts</h3>
        {loading ? (
          <p>Loading posts...</p>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Post URL</th>
                  <th>Required</th>
                  <th>Current</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {posts.map((post) => (
                  <tr key={post.id}>
                    <td><a href={post.post_url} rel="noreferrer" target="_blank">{post.post_url}</a></td>
                    <td>{post.required_likes}</td>
                    <td>{post.current_likes}</td>
                    <td>{post.status}</td>
                  </tr>
                ))}
                {posts.length === 0 ? (
                  <tr>
                    <td colSpan="4">No posts submitted yet.</td>
                  </tr>
                ) : null}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}
