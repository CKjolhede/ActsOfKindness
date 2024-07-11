import React from "react";
import ReactDOM from "react-dom/client";
import App from "./components/App";
import "./index.css";
import { createRoot } from "react-dom/client";
import { AuthProvider } from "./contexts/AuthContext";
import { BrowserRouter as Router} from "react-router-dom";   


const container = document.getElementById("root");
const root = createRoot(container);
root.render(
    <AuthProvider>
        <Router>
            <App />
        </Router>
    </AuthProvider>);

