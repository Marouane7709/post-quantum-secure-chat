import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import api from "../api";
import { UserPublic } from "../types";

interface AuthContextType {
  token: string | null;
  currentUser: UserPublic | null;
  setToken: (token: string | null) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setTokenState] = useState<string | null>(
    localStorage.getItem("pq_token") || null
  );
  const [currentUser, setCurrentUser] = useState<UserPublic | null>(null);

  const setToken = (newToken: string | null) => {
    if (newToken) {
      localStorage.setItem("pq_token", newToken);
    } else {
      localStorage.removeItem("pq_token");
    }
    setTokenState(newToken);
  };

  const logout = () => {
    setToken(null);
    setCurrentUser(null);
  };

  useEffect(() => {
    if (token) {
      const authHeaders = { Authorization: `Bearer ${token}` };
      api
        .get<UserPublic>("/auth/me", { headers: authHeaders })
        .then(({ data }) => setCurrentUser(data))
        .catch(() => {
          setToken(null);
          setCurrentUser(null);
        });
    } else {
      setCurrentUser(null);
    }
  }, [token]);

  return (
    <AuthContext.Provider value={{ token, currentUser, setToken, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

