import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import { useAuth } from "../contexts/AuthContext";

export function LoginPage() {
  const navigate = useNavigate();
  const { setToken } = useAuth();
  const [form, setForm] = useState({ username: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (evt: FormEvent) => {
    evt.preventDefault();
    setLoading(true);
    setError("");
    try {
      const { data } = await api.post<{ access_token: string }>("/auth/login", form);
      setToken(data.access_token);
      navigate("/app");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      <p className="auth-form-description">
        Obtain a JWT-signed access token to use the secure messaging API.
      </p>

      {error && <div className="auth-error">{error}</div>}

      <div className="form-group">
        <label htmlFor="login-username">Username</label>
        <input
          id="login-username"
          type="text"
          required
          placeholder="Username"
          value={form.username}
          onChange={(e) => setForm((prev) => ({ ...prev, username: e.target.value }))}
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="login-password">Password</label>
        <input
          id="login-password"
          type="password"
          required
          placeholder="Password"
          value={form.password}
          onChange={(e) => setForm((prev) => ({ ...prev, password: e.target.value }))}
          disabled={loading}
        />
      </div>

      <button type="submit" className="auth-button" disabled={loading}>
        {loading ? "Authenticating..." : "Login Securely"}
      </button>
    </form>
  );
}

