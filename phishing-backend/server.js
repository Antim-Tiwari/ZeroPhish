import express from "express";
import cors from "cors";
import predictSimple from "./routes/predict_simple.js";


const app = express();
app.use(cors({
  origin: "https://zero-phish-eight.vercel.app",
  methods: ["GET", "POST"],
  credentials: true
}));
app.use(express.json());

app.use("/predict", predictSimple);


const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Backend running on port ${PORT}`);
});
