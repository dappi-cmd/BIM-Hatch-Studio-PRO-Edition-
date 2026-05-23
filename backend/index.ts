import express from 'react'; // wait, express from express
// Let me write a proper express app
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 5000;

app.get('/api/status', (req, res) => {
  res.json({ status: 'BIM Hatch Studio Backend is running' });
});

app.listen(PORT, () => {
  console.log(`Backend Server running on port ${PORT}`);
});
