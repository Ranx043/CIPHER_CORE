"""
CIPHER Sniper Bot - Database Manager
SQLite async database for tracking tokens, creators, and trades
"""
import aiosqlite
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import json

from config import DB_PATH


class Database:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.conn: Optional[aiosqlite.Connection] = None

    async def connect(self):
        """Initialize database connection and create tables"""
        self.conn = await aiosqlite.connect(self.db_path)
        self.conn.row_factory = aiosqlite.Row
        await self._create_tables()
        print(f"[DB] Connected to {self.db_path}")

    async def close(self):
        """Close database connection"""
        if self.conn:
            await self.conn.close()

    async def _create_tables(self):
        """Create all required tables"""
        await self.conn.executescript("""
            -- TOKENS: Every token created on Pump.fun
            CREATE TABLE IF NOT EXISTS tokens (
                mint TEXT PRIMARY KEY,
                name TEXT,
                symbol TEXT,
                creator_wallet TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                uri TEXT,

                -- Metrics
                initial_mcap REAL DEFAULT 0,
                peak_mcap REAL DEFAULT 0,
                current_mcap REAL DEFAULT 0,
                peak_price REAL DEFAULT 0,
                current_price REAL DEFAULT 0,

                -- Status
                status TEXT DEFAULT 'active',
                graduated_at TIMESTAMP,

                -- Analysis
                time_to_peak_seconds INTEGER,
                simulated_profit_percent REAL
            );

            -- CREATORS: Wallet history and scoring
            CREATE TABLE IF NOT EXISTS creators (
                wallet TEXT PRIMARY KEY,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                -- Aggregated metrics
                tokens_created INTEGER DEFAULT 0,
                tokens_graduated INTEGER DEFAULT 0,
                avg_peak_mcap REAL DEFAULT 0,
                total_volume REAL DEFAULT 0,

                -- Scoring
                trust_score REAL DEFAULT 50,
                risk_level TEXT DEFAULT 'unknown',

                -- Flags
                is_blacklisted BOOLEAN DEFAULT FALSE,
                blacklist_reason TEXT
            );

            -- PRICE HISTORY: Snapshots for analysis
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mint TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                price REAL,
                mcap REAL,
                FOREIGN KEY (mint) REFERENCES tokens(mint)
            );

            -- PAPER TRADES: Simulated trades
            CREATE TABLE IF NOT EXISTS paper_trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mint TEXT,
                creator_wallet TEXT,

                -- Entry
                entry_timestamp TIMESTAMP,
                entry_price REAL,
                entry_mcap REAL,
                entry_amount_sol REAL,
                creator_score_at_entry REAL,

                -- Exit
                exit_timestamp TIMESTAMP,
                exit_price REAL,
                exit_amount_sol REAL,
                exit_reason TEXT,

                -- Results
                profit_sol REAL,
                profit_percent REAL,
                hold_time_seconds INTEGER,

                -- Status
                status TEXT DEFAULT 'open',

                FOREIGN KEY (mint) REFERENCES tokens(mint)
            );

            -- PAPER PORTFOLIO: Current state
            CREATE TABLE IF NOT EXISTS paper_portfolio (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                balance_sol REAL,
                total_profit REAL DEFAULT 0,
                total_trades INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            -- Indexes for performance
            CREATE INDEX IF NOT EXISTS idx_tokens_creator ON tokens(creator_wallet);
            CREATE INDEX IF NOT EXISTS idx_tokens_status ON tokens(status);
            CREATE INDEX IF NOT EXISTS idx_tokens_created ON tokens(created_at);
            CREATE INDEX IF NOT EXISTS idx_price_mint ON price_history(mint);
            CREATE INDEX IF NOT EXISTS idx_trades_status ON paper_trades(status);
        """)
        await self.conn.commit()

    # ==================== TOKEN OPERATIONS ====================

    async def add_token(self, mint: str, name: str, symbol: str,
                       creator: str, uri: str = None) -> bool:
        """Add new token to database"""
        try:
            await self.conn.execute("""
                INSERT OR IGNORE INTO tokens (mint, name, symbol, creator_wallet, uri)
                VALUES (?, ?, ?, ?, ?)
            """, (mint, name, symbol, creator, uri))
            await self.conn.commit()

            # Update creator stats
            await self._update_creator_on_new_token(creator)
            return True
        except Exception as e:
            print(f"[DB] Error adding token: {e}")
            return False

    async def update_token_price(self, mint: str, price: float, mcap: float):
        """Update token current price and track peak"""
        try:
            # Get current peak
            cursor = await self.conn.execute(
                "SELECT peak_mcap, peak_price FROM tokens WHERE mint = ?", (mint,)
            )
            row = await cursor.fetchone()

            if row:
                new_peak_mcap = max(row['peak_mcap'] or 0, mcap)
                new_peak_price = max(row['peak_price'] or 0, price)

                await self.conn.execute("""
                    UPDATE tokens
                    SET current_price = ?, current_mcap = ?,
                        peak_price = ?, peak_mcap = ?
                    WHERE mint = ?
                """, (price, mcap, new_peak_price, new_peak_mcap, mint))

                # Add to price history
                await self.conn.execute("""
                    INSERT INTO price_history (mint, price, mcap)
                    VALUES (?, ?, ?)
                """, (mint, price, mcap))

                await self.conn.commit()
        except Exception as e:
            print(f"[DB] Error updating price: {e}")

    async def get_token(self, mint: str) -> Optional[Dict]:
        """Get token by mint address"""
        cursor = await self.conn.execute(
            "SELECT * FROM tokens WHERE mint = ?", (mint,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def get_active_tokens(self, limit: int = 100) -> List[Dict]:
        """Get recently active tokens"""
        cursor = await self.conn.execute("""
            SELECT * FROM tokens
            WHERE status = 'active'
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    # ==================== CREATOR OPERATIONS ====================

    async def _update_creator_on_new_token(self, wallet: str):
        """Update creator stats when they create a new token"""
        await self.conn.execute("""
            INSERT INTO creators (wallet, tokens_created, last_seen)
            VALUES (?, 1, CURRENT_TIMESTAMP)
            ON CONFLICT(wallet) DO UPDATE SET
                tokens_created = tokens_created + 1,
                last_seen = CURRENT_TIMESTAMP
        """, (wallet,))
        await self.conn.commit()

    async def get_creator(self, wallet: str) -> Optional[Dict]:
        """Get creator by wallet address"""
        cursor = await self.conn.execute(
            "SELECT * FROM creators WHERE wallet = ?", (wallet,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def update_creator_score(self, wallet: str, score: float, risk: str):
        """Update creator trust score"""
        await self.conn.execute("""
            UPDATE creators
            SET trust_score = ?, risk_level = ?
            WHERE wallet = ?
        """, (score, risk, wallet))
        await self.conn.commit()

    async def blacklist_creator(self, wallet: str, reason: str):
        """Add creator to blacklist"""
        await self.conn.execute("""
            UPDATE creators
            SET is_blacklisted = TRUE, blacklist_reason = ?
            WHERE wallet = ?
        """, (reason, wallet))
        await self.conn.commit()

    async def get_creator_leaderboard(self, limit: int = 20) -> List[Dict]:
        """Get top creators by score"""
        cursor = await self.conn.execute("""
            SELECT * FROM creators
            WHERE is_blacklisted = FALSE AND tokens_created >= 2
            ORDER BY trust_score DESC
            LIMIT ?
        """, (limit,))
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    # ==================== PAPER TRADING OPERATIONS ====================

    async def init_paper_portfolio(self, initial_balance: float):
        """Initialize paper trading portfolio"""
        await self.conn.execute("""
            INSERT OR REPLACE INTO paper_portfolio (id, balance_sol)
            VALUES (1, ?)
        """, (initial_balance,))
        await self.conn.commit()

    async def get_paper_portfolio(self) -> Dict:
        """Get current paper portfolio state"""
        cursor = await self.conn.execute(
            "SELECT * FROM paper_portfolio WHERE id = 1"
        )
        row = await cursor.fetchone()
        return dict(row) if row else {"balance_sol": 0}

    async def open_paper_trade(self, mint: str, creator: str,
                               price: float, mcap: float,
                               amount_sol: float, creator_score: float) -> int:
        """Open a new paper trade"""
        cursor = await self.conn.execute("""
            INSERT INTO paper_trades
            (mint, creator_wallet, entry_timestamp, entry_price, entry_mcap,
             entry_amount_sol, creator_score_at_entry, status)
            VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?, ?, ?, 'open')
        """, (mint, creator, price, mcap, amount_sol, creator_score))

        # Deduct from balance
        await self.conn.execute("""
            UPDATE paper_portfolio
            SET balance_sol = balance_sol - ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
        """, (amount_sol,))

        await self.conn.commit()
        return cursor.lastrowid

    async def close_paper_trade(self, trade_id: int, exit_price: float,
                                exit_reason: str) -> Dict:
        """Close a paper trade and calculate profit"""
        # Get trade details
        cursor = await self.conn.execute(
            "SELECT * FROM paper_trades WHERE id = ?", (trade_id,)
        )
        trade = await cursor.fetchone()

        if not trade:
            return {}

        trade = dict(trade)

        # Calculate profit
        price_change = (exit_price - trade['entry_price']) / trade['entry_price']
        exit_amount = trade['entry_amount_sol'] * (1 + price_change)
        profit_sol = exit_amount - trade['entry_amount_sol']
        profit_percent = price_change * 100

        # Calculate hold time
        entry_time = datetime.fromisoformat(trade['entry_timestamp'])
        hold_time = int((datetime.now() - entry_time).total_seconds())

        # Update trade
        await self.conn.execute("""
            UPDATE paper_trades SET
                exit_timestamp = CURRENT_TIMESTAMP,
                exit_price = ?,
                exit_amount_sol = ?,
                exit_reason = ?,
                profit_sol = ?,
                profit_percent = ?,
                hold_time_seconds = ?,
                status = 'closed'
            WHERE id = ?
        """, (exit_price, exit_amount, exit_reason, profit_sol,
              profit_percent, hold_time, trade_id))

        # Update portfolio
        is_win = profit_sol > 0
        await self.conn.execute("""
            UPDATE paper_portfolio SET
                balance_sol = balance_sol + ?,
                total_profit = total_profit + ?,
                total_trades = total_trades + 1,
                wins = wins + ?,
                losses = losses + ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
        """, (exit_amount, profit_sol, 1 if is_win else 0, 0 if is_win else 1))

        await self.conn.commit()

        return {
            "trade_id": trade_id,
            "profit_sol": profit_sol,
            "profit_percent": profit_percent,
            "hold_time_seconds": hold_time,
            "exit_reason": exit_reason
        }

    async def get_open_trades(self) -> List[Dict]:
        """Get all open paper trades"""
        cursor = await self.conn.execute(
            "SELECT * FROM paper_trades WHERE status = 'open'"
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    # ==================== STATISTICS ====================

    async def get_stats(self) -> Dict:
        """Get overall statistics"""
        stats = {}

        # Token stats
        cursor = await self.conn.execute(
            "SELECT COUNT(*) as total, "
            "SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active "
            "FROM tokens"
        )
        row = await cursor.fetchone()
        stats['tokens'] = dict(row)

        # Creator stats
        cursor = await self.conn.execute(
            "SELECT COUNT(*) as total, "
            "AVG(trust_score) as avg_score "
            "FROM creators WHERE tokens_created >= 2"
        )
        row = await cursor.fetchone()
        stats['creators'] = dict(row)

        # Portfolio stats
        stats['portfolio'] = await self.get_paper_portfolio()

        # Trade stats
        cursor = await self.conn.execute("""
            SELECT
                COUNT(*) as total_trades,
                SUM(CASE WHEN profit_sol > 0 THEN 1 ELSE 0 END) as wins,
                AVG(profit_percent) as avg_profit_percent,
                SUM(profit_sol) as total_profit_sol
            FROM paper_trades WHERE status = 'closed'
        """)
        row = await cursor.fetchone()
        stats['trades'] = dict(row)

        return stats


# Singleton instance
db = Database()
