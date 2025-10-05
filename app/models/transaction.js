// PostgreSQL version: Export helper functions for transaction queries
const { Pool } = require('pg');
const pool = new Pool({
  user: 'vincentwu', // replace with your PostgreSQL username
  host: 'localhost',
  database: 'stocksense',
  password: '#E!#bx*f2Hr4yvK', // replace with your PostgreSQL password
  port: 5432,
});

async function createTransaction({ clerkId, stockSymbol, action, amount, timeChanged }) {
  const result = await pool.query(
    `INSERT INTO transactions (clerk_id, stock_symbol, action, amount, time_changed)
     VALUES ($1, $2, $3, $4, $5)
     RETURNING *`,
    [clerkId, stockSymbol, action, amount, timeChanged]
  );
  return result.rows[0];
}

async function getTransactionsByClerkId(clerkId) {
  const result = await pool.query('SELECT * FROM transactions WHERE clerk_id = $1', [clerkId]);
  return result.rows;
}

module.exports = { createTransaction, getTransactionsByClerkId };