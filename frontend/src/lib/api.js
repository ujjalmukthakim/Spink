const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";
const ACCESS_KEY = "reallike_access";
const REFRESH_KEY = "reallike_refresh";

let authCallbacks = {
  onUnauthorized: null,
  onWakeStateChange: null,
};

export function setAuthCallbacks(callbacks) {
  authCallbacks = { ...authCallbacks, ...callbacks };
}

export function getAccessToken() {
  return localStorage.getItem(ACCESS_KEY);
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_KEY);
}

export function setTokens(access, refresh) {
  localStorage.setItem(ACCESS_KEY, access);
  localStorage.setItem(REFRESH_KEY, refresh);
}

export function clearTokens() {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
}

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function refreshAccessToken() {
  const refresh = getRefreshToken();
  if (!refresh) {
    throw new Error("No refresh token");
  }

  const response = await fetch(`${API_BASE_URL}/auth/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh }),
  });

  if (!response.ok) {
    throw new Error("Refresh failed");
  }

  const data = await response.json();
  localStorage.setItem(ACCESS_KEY, data.access);
  return data.access;
}

export async function apiRequest(path, options = {}) {
  const {
    method = "GET",
    body,
    auth = true,
    retries = 4,
    retryDelay = 2500,
    retriedAuth = false,
  } = options;

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (auth && getAccessToken()) {
    headers.Authorization = `Bearer ${getAccessToken()}`;
  }

  for (let attempt = 0; attempt <= retries; attempt += 1) {
    try {
      const response = await fetch(`${API_BASE_URL}${path}`, {
        method,
        headers,
        body: body ? JSON.stringify(body) : undefined,
      });

      if ([502, 503, 504].includes(response.status)) {
        throw new Error("wake-up");
      }

      if (response.status === 401 && auth && !retriedAuth) {
        try {
          const newAccess = await refreshAccessToken();
          return apiRequest(path, {
            ...options,
            headers: { ...options.headers, Authorization: `Bearer ${newAccess}` },
            retriedAuth: true,
          });
        } catch {
          clearTokens();
          authCallbacks.onUnauthorized?.();
          throw new Error("Unauthorized");
        }
      }

      const contentType = response.headers.get("content-type") || "";
      const data = contentType.includes("application/json") ? await response.json() : null;

      if (!response.ok) {
        const message =
          data?.detail ||
          data?.non_field_errors?.[0] ||
          Object.values(data || {})?.flat?.()?.[0] ||
          "Request failed";
        throw new Error(message);
      }

      authCallbacks.onWakeStateChange?.(false);
      return data;
    } catch (error) {
      const shouldRetry = attempt < retries && (error.message === "wake-up" || error.message === "Failed to fetch");
      if (!shouldRetry) {
        authCallbacks.onWakeStateChange?.(false);
        throw error;
      }

      authCallbacks.onWakeStateChange?.(true, "Server is waking up, please wait...");
      await sleep(retryDelay);
    }
  }

  authCallbacks.onWakeStateChange?.(false);
  throw new Error("Request failed");
}
