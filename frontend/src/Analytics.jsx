import { useEffect, useState } from "react";
import { api } from "./api";

export default function Analytics({ refresh }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    api("/analytics")
      .then(setData)
      .catch(() => {});
  }, [refresh]);

  if (!data) return null;
  const max = Math.max(1, ...data.by_status.map((s) => s.count));

  return (
    <div className="analytics">
      <div className="stat-cards">
        <div className="panel stat">
          <span className="stat-num">{data.total}</span>
          <span className="muted">Total applications</span>
        </div>
        <div className="panel stat">
          <span className="stat-num">{data.interviews}</span>
          <span className="muted">Reached interview</span>
        </div>
        <div className="panel stat">
          <span className="stat-num">{data.offers}</span>
          <span className="muted">Offers</span>
        </div>
        <div className="panel stat">
          <span className="stat-num">{data.response_rate}%</span>
          <span className="muted">Response rate</span>
        </div>
      </div>

      <div className="panel">
        <h3 className="chart-title">Applications by stage</h3>
        {data.by_status.map((s) => (
          <div className="bar-row" key={s.status}>
            <span className="bar-label">{s.status}</span>
            <div className="bar-track">
              <div className="bar-fill" style={{ width: `${(s.count / max) * 100}%` }} />
            </div>
            <span className="bar-count">{s.count}</span>
          </div>
        ))}
      </div>
    </div>
  );
}