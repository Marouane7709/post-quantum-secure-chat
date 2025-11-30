import { Outlet, NavLink } from "react-router-dom";

export function AuthLayout() {
  return (
    <div className="auth-layout">
      <div className="auth-card">
        <div className="auth-header">
          <p className="auth-label">PROJECT QUANTUM SECURE</p>
          <h1 className="auth-title">Post-Quantum Messenger</h1>
          <p className="auth-subtitle">
            Kyber512 key exchange · Dilithium2 signatures · AES-256-GCM transport
          </p>
        </div>

        <div className="auth-tabs">
          <NavLink
            to="/auth/login"
            className={({ isActive }) => (isActive ? "auth-tab active" : "auth-tab")}
          >
            Login
          </NavLink>
          <NavLink
            to="/auth/register"
            className={({ isActive }) => (isActive ? "auth-tab active" : "auth-tab")}
          >
            Register
          </NavLink>
        </div>

        <div className="auth-content">
          <Outlet />
        </div>
      </div>
    </div>
  );
}

