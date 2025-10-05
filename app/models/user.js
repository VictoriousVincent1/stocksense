// PostgreSQL version: Export helper functions for user queries
const { Pool } = require('pg');
const pool = new Pool({
  user: 'vincentwu', // replace with your PostgreSQL username
  host: 'localhost',
  database: 'stocksense',
  password: '#E!#bx*f2Hr4yvK', // replace with your PostgreSQL password
  port: 5432,
});

async function getUserByClerkId(clerkId) {
  const result = await pool.query('SELECT * FROM users WHERE clerk_id = $1', [clerkId]);
  return result.rows[0];
}

async function upsertUser({ clerkId, username, sensebucks, favoriteStock, credentials }) {
  const result = await pool.query(
    `INSERT INTO users (clerk_id, username, sensebucks, favorite_stock, credentials, current_asset_stocks)
     VALUES ($1, $2, $3, $4, $5, $6)
     ON CONFLICT (clerk_id) DO UPDATE SET
       username = EXCLUDED.username,
       sensebucks = EXCLUDED.sensebucks,
       favorite_stock = EXCLUDED.favorite_stock,
       credentials = EXCLUDED.credentials,
       current_asset_stocks = EXCLUDED.current_asset_stocks
     RETURNING *`,
    [clerkId, username, sensebucks, favoriteStock, credentials, []]
  );
  return result.rows[0];
}

module.exports = { getUserByClerkId, upsertUser };