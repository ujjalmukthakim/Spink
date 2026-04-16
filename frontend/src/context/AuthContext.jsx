import { createContext, useContext, useEffect, useMemo, useState } from "react";

import { apiRequest, clearTokens, getAccessToken, getRefreshToken, setAuthCallbacks, setTokens } from "../lib/api";
import { useApiStatus } from "./ApiStatusContext";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const { setApiWakeState } = useApiStatus();

  useEffect(() => {
    setAuthCallbacks({
      onUnauthorized: () => {
        clearTokens();
        setUser(null);
      },
      onWakeStateChange: setApiWakeState,
    });
  }, [setApiWakeState]);

  useEffect(() => {
    async function bootstrap() {
      if (!getAccessToken() && !getRefreshToken()) {
        setLoading(false);
        return;
      }

      try {
        const me = await apiRequest("/users/me/");
        setUser(me);
      } catch {
        clearTokens();
        setUser(null);
      } finally {
        setLoading(false);
      }
    }

    bootstrap();
  }, []);

  const value = useMemo(
    () => ({
      user,
      loading,
      isAuthenticated: Boolean(user),
      async login(email, password) {
        const response = await apiRequest("/auth/login/", {
          method: "POST",
          body: { email, password },
          auth: false,
        });
        setTokens(response.access, response.refresh);
        setUser(response.user);
        return response.user;
      },
      async register(payload) {
        await apiRequest("/auth/register/", {
          method: "POST",
          body: payload,
          auth: false,
        });
      },
      async refreshUser() {
        const me = await apiRequest("/users/me/");
        setUser(me);
        return me;
      },
      logout() {
        clearTokens();
        setUser(null);
      },
    }),
    [user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
