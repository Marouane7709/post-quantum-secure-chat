import { Outlet } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export function AppLayout() {
  const { currentUser, logout } = useAuth();

  return (
    <div className="app-layout">
      <header className="app-header">
        <div className="app-header-content">
          <h1 className="app-header-title">Post-Quantum Messenger</h1>
          <div className="app-header-right">
            {currentUser && (
              <span className="app-username">{currentUser.username}</span>
            )}
            <button className="app-logout-btn" onClick={logout}>
              Logout
            </button>
          </div>
        </div>
      </header>
      <main className="app-main">
        <Outlet />
      </main>
    </div>
  );
}

