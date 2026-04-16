import { Navigate, Route, Routes } from "react-router-dom";

import { useAuth } from "./context/AuthContext";
import { useApiStatus } from "./context/ApiStatusContext";
import AppShell from "./components/AppShell";
import LoadingScreen from "./components/LoadingScreen";
import AdminPage from "./pages/AdminPage";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import SubmitPostPage from "./pages/SubmitPostPage";
import TasksPage from "./pages/TasksPage";

function ProtectedRoute({ children, adminOnly = false }) {
  const { isAuthenticated, loading, user } = useAuth();

  if (loading) {
    return <LoadingScreen message="Checking your session..." />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (adminOnly && !user?.is_admin) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}

export default function App() {
  const { isWakingUp, wakeMessage } = useApiStatus();

  return (
    <>
      {isWakingUp ? <LoadingScreen message={wakeMessage} subtle /> : null}
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <AppShell>
                <DashboardPage />
              </AppShell>
            </ProtectedRoute>
          }
        />
        <Route
          path="/submit"
          element={
            <ProtectedRoute>
              <AppShell>
                <SubmitPostPage />
              </AppShell>
            </ProtectedRoute>
          }
        />
        <Route
          path="/tasks"
          element={
            <ProtectedRoute>
              <AppShell>
                <TasksPage />
              </AppShell>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin"
          element={
            <ProtectedRoute adminOnly>
              <AppShell>
                <AdminPage />
              </AppShell>
            </ProtectedRoute>
          }
        />
      </Routes>
    </>
  );
}
