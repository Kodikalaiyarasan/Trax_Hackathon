import { useState, useEffect } from "react";
import { getRecommendations } from "../api";

export default function Recommendations() {
  const [recs, setRecs] = useState([]);

  useEffect(() => {
    async function fetchRecs() {
      const data = await getRecommendations();
      setRecs(data.recommendations || []);
    }
    fetchRecs();
    const interval = setInterval(fetchRecs, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4 border rounded-lg shadow-md">
      <h2 className="font-bold mb-2">AI Recommendations</h2>
      {recs.length === 0 ? (
        <p>No recommendations right now.</p>
      ) : (
        <ul className="list-disc ml-4 space-y-1">
          {recs.map((r, idx) => (
            <li key={idx}>
              🚆 {r.train_number} → <b>{r.action}</b> ({r.details.reason})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
