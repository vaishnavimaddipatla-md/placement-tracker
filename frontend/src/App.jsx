import { useEffect, useState } from "react";
import Login from "./Login";
import { api } from "./api";
import Dashboard from "./Dashboard";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (!token) return;
    api("/me")
      .then(setUser)
      .catch(() => logout());
  }, [token]);

  function logout() {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  }

  if (!token) return <Login onLogin={setToken} />;

  return (
    <div className="page">
      <header className="topbar">
        <strong>Placement Tracker</strong>
        <button className="ghost" onClick={logout}>Log out</button>
      </header>
      <h2>Welcome{user ? `, ${user.name}` : ""}</h2>
      <Dashboard />
    </div>
  );
}