const { Pool } = require('pg');
const readline = require('readline');

const pool = new Pool({
  user: 'vincentwu', // replace with your PostgreSQL username
  host: 'localhost',
  database: 'stocksense',
  password: '#E!#bx*f2Hr4yvK', // replace with your PostgreSQL password
  port: 5432,
});

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function ask(question) {
  return new Promise(resolve => rl.question(question, resolve));
}

async function addUser() {
  const clerkId = await ask('Clerk ID: ');
  const username = await ask('Username: ');
  const sensebucks = await ask('Sensebucks: ');
  const favoriteStock = await ask('Favorite Stock: ');
  const email = await ask('Email: ');
  const credentials = { email };

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
  console.log('User added/updated:', result.rows[0]);
}

async function addTransaction() {
  const clerkId = await ask('Clerk ID: ');
  // Check if clerkId exists in users table
  const userRes = await pool.query('SELECT * FROM users WHERE clerk_id = $1', [clerkId]);
  if (userRes.rows.length === 0) {
    console.log('Error: Clerk ID does not exist in users table. Transaction not added.');
    return;
  }
  const user = userRes.rows[0];
  const stockSymbol = await ask('Stock Symbol: ');
  const action = await ask('Action (buy/sell): ');
  const amount = parseFloat(await ask('Amount per stock: '));
  const quantity = parseInt(await ask('Quantity: '), 10);
  const totalAmount = amount * quantity;

  // Update current_asset_stocks array
  let assets = user.current_asset_stocks || [];
  let found = false;
  for (let i = 0; i < assets.length; i++) {
    if (assets[i][0] === stockSymbol) {
      if (action === 'buy') {
        assets[i][1] += quantity;
        assets[i][2] = amount; // update price to latest
      } else if (action === 'sell') {
        assets[i][1] -= quantity;
        if (assets[i][1] < 0) assets[i][1] = 0;
      }
      found = true;
      break;
    }
  }
  if (!found && action === 'buy') {
    assets.push([stockSymbol, quantity, amount]);
  }
  // Remove stocks with zero quantity
  assets = assets.filter(item => item[1] > 0);

  // Adjust sensebucks
  let newSensebucks = parseFloat(user.sensebucks);
  if (action === 'buy') {
    newSensebucks -= totalAmount;
  } else if (action === 'sell') {
    newSensebucks += totalAmount;
  }

  // Save updated user
  await pool.query(
    `UPDATE users SET current_asset_stocks = $1, sensebucks = $2 WHERE clerk_id = $3`,
    [JSON.stringify(assets), newSensebucks, clerkId]
  );

  // Save transaction
  const result = await pool.query(
    `INSERT INTO transactions (clerk_id, stock_symbol, action, amount, time_changed)
     VALUES ($1, $2, $3, $4, NOW())
     RETURNING *`,
    [clerkId, stockSymbol, action, totalAmount]
  );
  console.log(`Transaction added: ${quantity} x ${stockSymbol} at $${amount} each. Total: $${totalAmount}`);
}

async function main() {
  const choice = await ask('Add (1) User or (2) Transaction? ');
  if (choice === '1') {
    await addUser();
  } else if (choice === '2') {
    await addTransaction();
  } else {
    console.log('Invalid choice.');
  }
  rl.close();
  pool.end();
}

main();
