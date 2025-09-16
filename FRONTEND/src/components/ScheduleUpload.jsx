import { useState } from "react";
import { uploadSchedule } from "../api";

export default function ScheduleUpload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  async function handleUpload() {
    if (!file) return;
    try {
      await uploadSchedule(file);
      setStatus("✅ Schedule uploaded successfully!");
    } catch {
      setStatus("❌ Failed to upload schedule.");
    }
  }

  return (
    <div className="p-4 border rounded-lg shadow-md">
      <h2 className="font-bold mb-2">Upload Static Train Schedule</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button
        onClick={handleUpload}
        className="ml-2 px-3 py-1 bg-blue-500 text-white rounded"
      >
        Upload
      </button>
      <p className="mt-2">{status}</p>
    </div>
  );
}
