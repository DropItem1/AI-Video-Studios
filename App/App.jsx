import React, { useState, useEffect } from "react";
import axios from "axios";

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [style, setStyle] = useState("realistic");
  const [jobId, setJobId] = useState(null);
  const [job, setJob] = useState(null);

  useEffect(() => {
    if (!jobId) return;
    const interval = setInterval(async () => {
      const res = await axios.get(`http://localhost:4000/api/job/${jobId}`);
      setJob(res.data);
      if (res.data.status === "done") clearInterval(interval);
    }, 1000);
    return () => clearInterval(interval);
  }, [jobId]);

  const handleGenerate = async () => {
    const res = await axios.post("http://localhost:4000/api/generate", {
      prompt,
      style,
    });
    setJobId(res.data.jobId);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>🎬 AI Video Studio (Minimal)</h2>
      <textarea
        placeholder="Describe your animation..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        rows={4}
        style={{ width: "100%" }}
      />
      <select value={style} onChange={(e) => setStyle(e.target.value)}>
        <option>realistic</option>
        <option>anime</option>
        <option>cartoon</option>
      </select>
      <button onClick={handleGenerate}>Generate</button>

      {job && (
        <pre style={{ background: "#eee", padding: 10, marginTop: 10 }}>
          {JSON.stringify(job, null, 2)}
        </pre>
      )}
    </div>
  );
}
