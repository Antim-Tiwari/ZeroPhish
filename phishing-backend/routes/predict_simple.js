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

  let options = {
    mode: "json",
    pythonOptions: ["-u"],
    scriptPath: path.join(__dirname, ".."), 
    args: [url],
  };

  try {
    const results = await PythonShell.run("app/predict_simple.py", options);
    res.json(results[0]);
  } catch (err) {
    console.error("Simple Prediction Error:", err);
    res.status(500).json({ error: "Prediction failed", details: err.message });
  }
});

export default router;
