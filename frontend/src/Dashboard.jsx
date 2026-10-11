import { useEffect, useState } from "react";
import { api } from "./api";
import Analytics from "./Analytics";
import Board from "./Board";

const STATUSES = ["Wishlist", "Applied", "Online Test", "Interview", "Offer", "Rejected"];
const EMPTY_FORM = { company: "", role: "", location: "", status: "Wishlist" };

export default function Dashboard() {
  const [apps, setApps] = useState([]);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [form, setForm] = useState(EMPTY_FORM);
  const [error, setError] = useState("");
  const [view, setView] = useState("board");

  async function load(s = search, f = statusFilter) {
    try {
      const params = new URLSearchParams({ limit: "100" });
      if (s) params.set("search", s);
      if (f) params.set("status", f);
      setApps(await api(`/applications?${params}`));
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, [search, statusFilter]);

  function switchView(next) {
    setView(next);
    if (next === "board") setStatusFilter("");
  }

  async function addApplication(e) {
    e.preventDefault();
    setError("");
    try {
      await api("/applications", { method: "POST", body: JSON.stringify(form) });
      setForm(EMPTY_FORM);
      setSearch("");
      setStatusFilter("");
      load("", "");
    } catch (err) {
      setError(err.message);
    }
  }

  async function changeStatus(id, status) {
    const previous = apps;
    setApps(apps.map((a) => (a.id === id ? { ...a, status } : a)));
    try {
      await api(`/applications/${id}`, { method: "PATCH", body: JSON.stringify({ status }) });
      load();
    } catch (err) {
      setApps(previous);
      setError(err.message);
    }
  }

  async function remove(id) {
    if (!window.confirm("Delete this application?")) return;
    try {
      await api(`/applications/${id}`, { method: "DELETE" });
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <Analytics refresh={apps} />

      <form className="panel add-form" onSubmit={addApplication}>
        <input
          placeholder="Company"
          value={form.company}
          onChange={(e) => setForm({ ...form, company: e.target.value })}
          required
        />
        <input
          placeholder="Role"
          value={form.role}
          onChange={(e) => setForm({ ...form, role: e.target.value })}
          required
        />
        <input
          placeholder="Location"
          value={form.location}
          onChange={(e) => setForm({ ...form, location: e.target.value })}
        />
        <select
          value={form.status}
          onChange={(e) => setForm({ ...form, status: e.target.value })}
        >
          {STATUSES.map((s) => (
            <option key={s}>{s}</option>
          ))}
        </select>
        <button type="submit">Add</button>
      </form>

      <div className="view-toggle">
        <button className={view === "board" ? "" : "ghost"} onClick={() => switchView("board")}>
          Board
        </button>
        <button className={view === "list" ? "" : "ghost"} onClick={() => switchView("list")}>
          List
        </button>
      </div>

      <div className="filters">
        <input
          placeholder="Search company or role"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        {view === "list" && (
          <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
            <option value="">All statuses</option>
            {STATUSES.map((s) => (
              <option key={s}>{s}</option>
            ))}
          </select>
        )}
      </div>

      {error && <div className="error">{error}</div>}

      {view === "board" ? (
        <Board apps={apps} onMove={changeStatus} onDelete={remove} />
      ) : apps.length === 0 ? (
        <p className="muted">No applications yet. Add your first one above.</p>
      ) : (
        <div className="panel table-wrap">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Company</th>
                <th>Role</th>
                <th>Location</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {apps.map((a, i) => (
                <tr key={a.id}>
                  <td>{i + 1}</td>
                  <td>{a.company}</td>
                  <td>{a.role}</td>
                  <td>{a.location || "-"}</td>
                  <td>
                    <select value={a.status} onChange={(e) => changeStatus(a.id, e.target.value)}>
                      {STATUSES.map((s) => (
                        <option key={s}>{s}</option>
                      ))}
                    </select>
                  </td>
                  <td>
                    <button className="ghost small" onClick={() => remove(a.id)}>
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}