import { Navigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export function RequireAuth({ children }: { children: React.ReactNode }) {
  const { token } = useAuth();

  if (!token) {
    return <Navigate to="/auth/login" replace />;
  }

  return <>{children}</>;
}

