import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import { KeyBundle } from "../types";

export function RegisterPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [keyBundle, setKeyBundle] = useState<KeyBundle | null>(null);

  const handleSubmit = async (evt: FormEvent) => {
    evt.preventDefault();
    setLoading(true);
    setError("");
    try {
      const { data } = await api.post<KeyBundle>("/auth/register", form);
      setKeyBundle(data);
      setTimeout(() => {
        navigate("/auth/login");
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      <p className="auth-form-description">
        Generates Kyber + Dilithium key pairs and an Argon2-hashed credential.
      </p>

      {error && <div className="auth-error">{error}</div>}

      {keyBundle && (
        <div className="auth-success">
          <p>Registration successful! Save your private keys:</p>
          <pre className="key-bundle">{JSON.stringify(keyBundle, null, 2)}</pre>
          <p>Redirecting to login...</p>
        </div>
      )}

      {!keyBundle && (
        <>
          <div className="form-group">
            <label htmlFor="reg-username">Username</label>
            <input
              id="reg-username"
              type="text"
              required
              placeholder="Username"
              value={form.username}
              onChange={(e) => setForm((prev) => ({ ...prev, username: e.target.value }))}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="reg-password">Password</label>
            <input
              id="reg-password"
              type="password"
              required
              placeholder="Password"
              value={form.password}
              onChange={(e) => setForm((prev) => ({ ...prev, password: e.target.value }))}
              disabled={loading}
            />
          </div>

          <button type="submit" className="auth-button" disabled={loading}>
            {loading ? "Creating..." : "Create Secure Identity"}
          </button>
        </>
      )}
    </form>
  );
}

