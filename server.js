// server.js — minimal commit-safe version
import express from "express";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

let jobs = {};

app.post("/api/generate", (req, res) => {
  const id = Date.now().toString();
  const { prompt, style } = req.body;
  jobs[id] = { id, prompt, style, status: "processing" };
  console.log("Job created:", jobs[id]);
  setTimeout(() => (jobs[id].status = "done"), 2000);
  res.json({ jobId: id });
});

app.get("/api/job/:id", (req, res) => {
  const job = jobs[req.params.id];
  if (!job) return res.status(404).json({ error: "Not found" });
  res.json(job);
});

app.listen(4000, () => console.log("✅ Server running on port 4000"));
