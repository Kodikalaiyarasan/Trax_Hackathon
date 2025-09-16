
import { useState } from "react";
import { setPriority } from "../api";

export default function PriorityForm() {
  const [trainNumber, setTrainNumber] = useState("");
  const [priority, setPriorityVal] = useState(1);
  const [status, setStatus] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      await setPriority(trainNumber, priority);
      setStatus(`✅ Priority set for ${trainNumber}`);
    } catch {
      setStatus("❌ Failed to set priority");
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="p-4 border rounded-lg shadow-md space-y-2"
    >
      <h2 className="font-bold">Set Train Priority</h2>
      <input
        type="text"
        placeholder="Train Number"
        value={trainNumber}
        onChange={(e) => setTrainNumber(e.target.value)}
        className="border p-1 rounded w-full"
      />
      <input
        type="number"
        min="1"
        max="10"
        value={priority}
        onChange={(e) => setPriorityVal(Number(e.target.value))}
        className="border p-1 rounded w-full"
      />
      <button
        type="submit"
        className="px-3 py-1 bg-green-600 text-white rounded"
      >
        Save Priority
      </button>
      <p>{status}</p>
    </form>
  );
}
