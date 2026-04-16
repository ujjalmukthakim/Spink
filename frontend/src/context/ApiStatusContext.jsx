import { createContext, useContext, useMemo, useState } from "react";

const ApiStatusContext = createContext(null);

export function ApiStatusProvider({ children }) {
  const [isWakingUp, setIsWakingUp] = useState(false);
  const [wakeMessage, setWakeMessage] = useState("Server is waking up, please wait...");

  const value = useMemo(
    () => ({
      isWakingUp,
      wakeMessage,
      setApiWakeState(active, message = "Server is waking up, please wait...") {
        setIsWakingUp(active);
        setWakeMessage(message);
      },
    }),
    [isWakingUp, wakeMessage]
  );

  return <ApiStatusContext.Provider value={value}>{children}</ApiStatusContext.Provider>;
}

export function useApiStatus() {
  const context = useContext(ApiStatusContext);
  if (!context) {
    throw new Error("useApiStatus must be used within ApiStatusProvider");
  }
  return context;
}
