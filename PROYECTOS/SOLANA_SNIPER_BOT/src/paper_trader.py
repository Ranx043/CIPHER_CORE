"""
CIPHER Sniper Bot - Paper Trading Engine
Simulates trades based on creator scores without real money
"""
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from config import (
    PAPER_INITIAL_BALANCE, MAX_POSITION_SIZE, MAX_OPEN_POSITIONS,
    STOP_LOSS_PERCENT, TAKE_PROFIT_1_PERCENT, TAKE_PROFIT_2_PERCENT,
    MIN_CREATOR_SCORE, MIN_CREATOR_TOKENS, get_position_size, BASE_DIR
)
from database import db

# Control file for real-time adjustments
CONTROL_FILE = BASE_DIR / "control.json"


class PaperTrader:
    """
    Paper trading engine - simulates trades without real money
    """

    def __init__(self):
        self.active_positions: Dict[str, Dict] = {}  # mint -> position
        self.initialized = False
        self.control = {}  # Real-time control settings
        self._load_control()

    def _load_control(self) -> Dict:
        """Load control settings from JSON file (hot reload)"""
        try:
            if CONTROL_FILE.exists():
                with open(CONTROL_FILE, 'r') as f:
                    self.control = json.load(f)
        except Exception as e:
            print(f"[CONTROL] Error loading control file: {e}")
        return self.control

    def get_control(self, key: str, default=None):
        """Get control value with fallback to default"""
        self._load_control()  # Reload each time for hot updates
        return self.control.get(key, default)

    async def initialize(self):
        """Initialize paper trading portfolio"""
        portfolio = await db.get_paper_portfolio()

        if not portfolio or portfolio.get("balance_sol") is None:
            await db.init_paper_portfolio(PAPER_INITIAL_BALANCE)
            print(f"[PAPER] Initialized portfolio with {PAPER_INITIAL_BALANCE} SOL")
        else:
            print(f"[PAPER] Portfolio loaded: {portfolio['balance_sol']:.4f} SOL")

        # Load open positions
        open_trades = await db.get_open_trades()
        for trade in open_trades:
            self.active_positions[trade['mint']] = trade

        print(f"[PAPER] Open positions: {len(self.active_positions)}")
        self.initialized = True

    async def evaluate_token(self, token_data: Dict) -> bool:
        """
        Evaluate if we should paper-trade this token
        Returns True if we should buy
        """
        # Check control settings (hot reload)
        if not self.get_control("trading_enabled", True):
            return False

        if self.get_control("pause_new_trades", False):
            return False

        creator = token_data.get("creator")
        creator_score = token_data.get("creator_score", 50)
        creator_tokens = token_data.get("creator_tokens", 1)

        # Check blacklist/whitelist from control
        blacklist = self.get_control("blacklist_creators", [])
        whitelist = self.get_control("whitelist_creators", [])

        if creator in blacklist:
            print(f"[SKIP] Creator {creator[:16]}... is blacklisted")
            return False

        # If whitelist exists and is not empty, only trade whitelisted
        if whitelist and creator not in whitelist:
            return False

        # Check basic criteria (use control values or defaults)
        min_score = self.get_control("min_creator_score", MIN_CREATOR_SCORE)
        min_tokens = self.get_control("min_creator_tokens", MIN_CREATOR_TOKENS)

        if creator_score < min_score:
            return False

        if creator_tokens < min_tokens:
            return False

        # Check if we have too many open positions
        if len(self.active_positions) >= MAX_OPEN_POSITIONS:
            return False

        # Check if we already have a position in this token
        if token_data.get("mint") in self.active_positions:
            return False

        # Check balance
        portfolio = await db.get_paper_portfolio()
        max_size = self.get_control("max_position_size", MAX_POSITION_SIZE)
        position_size = min(get_position_size(creator_score), max_size)

        if portfolio.get("balance_sol", 0) < position_size:
            return False

        return True

    async def open_position(self, token_data: Dict) -> Optional[int]:
        """
        Open a paper trade position
        """
        mint = token_data.get("mint")
        creator = token_data.get("creator")
        creator_score = token_data.get("creator_score", 50)

        # Get position size based on creator score
        position_size = get_position_size(creator_score)

        # Simulate entry price (in paper mode, we assume instant fill)
        entry_price = 0.000001  # Initial pump.fun price is usually very small
        entry_mcap = 30000  # ~30k SOL initial mcap typical

        # Open the trade
        trade_id = await db.open_paper_trade(
            mint=mint,
            creator=creator,
            price=entry_price,
            mcap=entry_mcap,
            amount_sol=position_size,
            creator_score=creator_score
        )

        # Track locally
        self.active_positions[mint] = {
            "trade_id": trade_id,
            "mint": mint,
            "entry_price": entry_price,
            "entry_mcap": entry_mcap,
            "amount_sol": position_size,
            "creator_score": creator_score,
            "entry_time": datetime.now()
        }

        print(f"\n[PAPER BUY] {token_data.get('symbol', 'Unknown')}")
        print(f"  Position: {position_size} SOL")
        print(f"  Creator Score: {creator_score}")
        print(f"  Trade ID: {trade_id}")

        return trade_id

    async def check_exits(self, price_updates: Dict[str, float]):
        """
        Check all positions for exit conditions
        price_updates: {mint: current_price}
        """
        # Check if we should close all positions (emergency exit)
        if self.get_control("close_all_positions", False):
            print("[CONTROL] Emergency close all positions triggered!")
            for mint in list(self.active_positions.keys()):
                current_price = price_updates.get(mint, 0)
                await self.close_position(mint, current_price, "emergency_close")
            return

        # Get control values for exits
        stop_loss = self.get_control("stop_loss_percent", STOP_LOSS_PERCENT)
        take_profit = self.get_control("take_profit_percent", TAKE_PROFIT_2_PERCENT)

        for mint, position in list(self.active_positions.items()):
            current_price = price_updates.get(mint)

            if current_price is None:
                continue

            entry_price = position["entry_price"]

            # Calculate P/L
            price_change_pct = ((current_price - entry_price) / entry_price) * 100

            # Check stop loss
            if price_change_pct <= -stop_loss:
                await self.close_position(mint, current_price, "stop_loss")
                continue

            # Check take profit
            if price_change_pct >= take_profit:
                await self.close_position(mint, current_price, "take_profit")

    async def close_position(self, mint: str, exit_price: float, reason: str):
        """
        Close a paper trade position
        """
        if mint not in self.active_positions:
            return

        position = self.active_positions[mint]
        trade_id = position["trade_id"]

        # Close in database
        result = await db.close_paper_trade(trade_id, exit_price, reason)

        # Remove from local tracking
        del self.active_positions[mint]

        profit_sol = result.get("profit_sol", 0)
        profit_pct = result.get("profit_percent", 0)
        hold_time = result.get("hold_time_seconds", 0)

        emoji = "+" if profit_sol > 0 else ""

        print(f"\n[PAPER SELL] Trade #{trade_id}")
        print(f"  Reason: {reason}")
        print(f"  Profit: {emoji}{profit_sol:.4f} SOL ({emoji}{profit_pct:.1f}%)")
        print(f"  Hold time: {hold_time}s")

        return result

    async def get_status(self) -> Dict:
        """Get current paper trading status"""
        portfolio = await db.get_paper_portfolio()
        stats = await db.get_stats()

        return {
            "balance": portfolio.get("balance_sol", 0),
            "total_profit": portfolio.get("total_profit", 0),
            "total_trades": portfolio.get("total_trades", 0),
            "wins": portfolio.get("wins", 0),
            "losses": portfolio.get("losses", 0),
            "win_rate": (portfolio.get("wins", 0) / max(portfolio.get("total_trades", 1), 1)) * 100,
            "open_positions": len(self.active_positions),
            "tokens_tracked": stats.get("tokens", {}).get("total", 0),
            "creators_tracked": stats.get("creators", {}).get("total", 0)
        }

    async def print_status(self):
        """Print formatted status"""
        status = await self.get_status()

        print("\n" + "=" * 50)
        print("CIPHER PAPER TRADING STATUS")
        print("=" * 50)
        print(f"Balance:        {status['balance']:.4f} SOL")
        print(f"Total Profit:   {status['total_profit']:+.4f} SOL")
        print(f"Total Trades:   {status['total_trades']}")
        print(f"Win Rate:       {status['win_rate']:.1f}% ({status['wins']}W/{status['losses']}L)")
        print(f"Open Positions: {status['open_positions']}/{MAX_OPEN_POSITIONS}")
        print(f"Tokens Tracked: {status['tokens_tracked']}")
        print(f"Creators:       {status['creators_tracked']}")
        print("=" * 50)


# Singleton
paper_trader = PaperTrader()
