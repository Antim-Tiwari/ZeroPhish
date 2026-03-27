import express from "express";
import { PythonShell } from "python-shell";
import path from "path";
import { fileURLToPath } from "url";

const router = express.Router();
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

router.post("/", async (req, res) => {
  const { url } = req.body;

  if (!url) return res.status(400).json({ error: "URL is required" });

  const scriptPath = path.join(__dirname, "../app"); // ✅ go to app folder

  let options = {
    mode: "json", // keep this since your Python returns JSON
    pythonOptions: ["-u"],
    scriptPath: scriptPath,
    args: [url],
  };

  try {
    const results = await PythonShell.run("predict_simple.py", options);

    if (!results || !results[0]) {
      return res.status(500).json({ error: "No response from ML model" });
    }

    res.json(results[0]);

  } catch (err) {
    console.error("Python Error:", err);

    res.status(500).json({
      error: "Prediction failed",
      details: err.message,
    });
  }
});

export default router;