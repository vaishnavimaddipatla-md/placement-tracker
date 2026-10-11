import { useState } from "react";

const STATUSES = ["Wishlist", "Applied", "Online Test", "Interview", "Offer", "Rejected"];

export default function Board({ apps, onMove, onDelete }) {
  const [dragId, setDragId] = useState(null);
  const [overColumn, setOverColumn] = useState(null);

  function handleDrop(e, status) {
    e.preventDefault();
    const id = Number(e.dataTransfer.getData("text/plain")) || dragId;
    setOverColumn(null);
    setDragId(null);
    const card = apps.find((a) => a.id === id);
    if (card && card.status !== status) onMove(id, status);
  }

  return (
    <div className="board">
      {STATUSES.map((status) => {
        const cards = apps.filter((a) => a.status === status);
        return (
          <div
            key={status}
            className={`column ${overColumn === status ? "over" : ""}`}
            onDragOver={(e) => {
              e.preventDefault();
              setOverColumn(status);
            }}
            onDragLeave={() => setOverColumn(null)}
            onDrop={(e) => handleDrop(e, status)}
          >
            <div className="column-head">
              <span>{status}</span>
              <span className="count">{cards.length}</span>
            </div>

            {cards.map((a) => (
              <div
                key={a.id}
                className={`app-card ${dragId === a.id ? "dragging" : ""}`}
                draggable
                onDragStart={(e) => {
                  e.dataTransfer.setData("text/plain", String(a.id));
                  e.dataTransfer.effectAllowed = "move";
                  setDragId(a.id);
                }}
                onDragEnd={() => {
                  setDragId(null);
                  setOverColumn(null);
                }}
              >
                <strong>{a.company}</strong>
                <span className="muted">{a.role}</span>
                {a.location && <span className="muted">{a.location}</span>}
                <div className="card-actions">
                  <select value={a.status} onChange={(e) => onMove(a.id, e.target.value)}>
                    {STATUSES.map((s) => (
                      <option key={s}>{s}</option>
                    ))}
                  </select>
                  <button className="ghost small" onClick={() => onDelete(a.id)}>
                    Delete
                  </button>
                </div>
              </div>
            ))}

            {cards.length === 0 && <p className="empty">Drop here</p>}
          </div>
        );
      })}
    </div>
  );
}