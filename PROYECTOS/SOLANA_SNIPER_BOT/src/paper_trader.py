"""
CIPHER Sniper Bot - Paper Trading Engine
Simulates trades based on creator scores without real money
"""
import asyncio
from datetime import datetime
from typing import Dict, List, Optional

from config import (
    PAPER_INITIAL_BALANCE, MAX_POSITION_SIZE, MAX_OPEN_POSITIONS,
    STOP_LOSS_PERCENT, TAKE_PROFIT_1_PERCENT, TAKE_PROFIT_2_PERCENT,
    MIN_CREATOR_SCORE, MIN_CREATOR_TOKENS, get_position_size
)
from database import db


class PaperTrader:
    """
    Paper trading engine - simulates trades without real money
    """

    def __init__(self):
        self.active_positions: Dict[str, Dict] = {}  # mint -> position
        self.initialized = False

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
        creator = token_data.get("creator")
        creator_score = token_data.get("creator_score", 50)
        creator_tokens = token_data.get("creator_tokens", 1)

        # Check basic criteria
        if creator_score < MIN_CREATOR_SCORE:
            return False

        if creator_tokens < MIN_CREATOR_TOKENS:
            return False

        # Check if we have too many open positions
        if len(self.active_positions) >= MAX_OPEN_POSITIONS:
            return False

        # Check if we already have a position in this token
        if token_data.get("mint") in self.active_positions:
            return False

        # Check balance
        portfolio = await db.get_paper_portfolio()
        position_size = get_position_size(creator_score)

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
        for mint, position in list(self.active_positions.items()):
            current_price = price_updates.get(mint)

            if current_price is None:
                continue

            entry_price = position["entry_price"]

            # Calculate P/L
            price_change_pct = ((current_price - entry_price) / entry_price) * 100

            # Check stop loss
            if price_change_pct <= -STOP_LOSS_PERCENT:
                await self.close_position(mint, current_price, "stop_loss")
                continue

            # Check take profit levels
            if price_change_pct >= TAKE_PROFIT_2_PERCENT:
                await self.close_position(mint, current_price, "take_profit_2")
            elif price_change_pct >= TAKE_PROFIT_1_PERCENT:
                # Partial exit logic could go here
                # For now, we just log and wait for TP2
                pass

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
