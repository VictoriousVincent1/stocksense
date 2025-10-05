const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');
const app = express();

app.use(cors());
app.use(express.json());

// PostgreSQL connection
const pool = new Pool({
  user: 'victoriousvincent', // replace with your PostgreSQL username
  host: 'localhost',
  database: 'stocksense',
  password: '#E!#bx*f2Hr4yvK', // replace with your PostgreSQL password
  port: 5432,
});

// Test connection
pool.query('SELECT NOW()', (err, res) => {
  if (err) {
    console.error('PostgreSQL connection error:', err);
  } else {
    console.log('PostgreSQL connected at:', res.rows[0].now);
  }
});


// User Profile Route
app.get('/api/user/:clerkId', async (req, res) => {
  try {
    const result = await pool.query(
      'SELECT * FROM users WHERE clerk_id = $1',
      [req.params.clerkId]
    );
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Create/Update User Profile
app.post('/api/user', async (req, res) => {
  const { clerkId, username, sensebucks, favoriteStock, credentials } = req.body;
  try {
    const result = await pool.query(
      `INSERT INTO users (clerk_id, username, sensebucks, favorite_stock, credentials)
       VALUES ($1, $2, $3, $4, $5)
       ON CONFLICT (clerk_id) DO UPDATE SET
         username = EXCLUDED.username,
         sensebucks = EXCLUDED.sensebucks,
         favorite_stock = EXCLUDED.favorite_stock,
         credentials = EXCLUDED.credentials
       RETURNING *`,
      [clerkId, username, sensebucks, favoriteStock, credentials]
    );
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Transaction Route
app.post('/api/transaction', async (req, res) => {
  const { clerkId, stockSymbol, action, amount, timeChanged } = req.body;
  try {
    const result = await pool.query(
      `INSERT INTO transactions (clerk_id, stock_symbol, action, amount, time_changed)
       VALUES ($1, $2, $3, $4, $5)
       RETURNING *`,
      [clerkId, stockSymbol, action, amount, timeChanged]
    );
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Get all transactions for a user
app.get('/api/transactions/:clerkId', async (req, res) => {
  try {
    const result = await pool.query(
      'SELECT * FROM transactions WHERE clerk_id = $1',
      [req.params.clerkId]
    );
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(5000, () => console.log('Backend server running on port 5000'));