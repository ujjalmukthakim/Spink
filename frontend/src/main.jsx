import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import App from "./App";
import { ApiStatusProvider } from "./context/ApiStatusContext";
import { AuthProvider } from "./context/AuthContext";
import "./styles.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <ApiStatusProvider>
        <AuthProvider>
          <App />
        </AuthProvider>
      </ApiStatusProvider>
    </BrowserRouter>
  </React.StrictMode>
);
