"""
CIPHER SNIPER BOT - Main Entry Point
=====================================
Paper trading bot for Pump.fun tokens

Usage:
    python main.py              # Run collector + paper trader
    python main.py --collect    # Only collect data (no trading)
    python main.py --status     # Show current status
"""
import asyncio
import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import MODE, IS_PAPER, PAPER_INITIAL_BALANCE
from database import db
from collector import collector
from paper_trader import paper_trader


BANNER = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║      ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗               ║
║     ██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗              ║
║     ██║     ██║██████╔╝███████║█████╗  ██████╔╝              ║
║     ██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗              ║
║     ╚██████╗██║██║     ██║  ██║███████╗██║  ██║              ║
║      ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝              ║
║                                                               ║
║              PUMP.FUN SNIPER BOT v0.1                         ║
║              Paper Trading Mode                               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""


async def on_new_token(token_data: dict):
    """Callback when new token is detected"""
    # Evaluate if we should trade
    should_trade = await paper_trader.evaluate_token(token_data)

    if should_trade:
        await paper_trader.open_position(token_data)


async def run_collector_only():
    """Run only the data collector (no trading)"""
    print(BANNER)
    print("[MODE] Data Collection Only - No trading")
    print("=" * 60)

    await db.connect()

    try:
        await collector.start()
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Stopping collector...")
        await collector.stop()
        await db.close()


async def run_paper_trading():
    """Run full paper trading bot"""
    print(BANNER)
    print(f"[MODE] Paper Trading - Initial Balance: {PAPER_INITIAL_BALANCE} SOL")
    print("=" * 60)

    # Initialize
    await db.connect()
    await paper_trader.initialize()

    # Set callback for new tokens
    collector.on_new_token = on_new_token

    # Print initial status
    await paper_trader.print_status()

    print("\nListening for new tokens... Press Ctrl+C to stop\n")

    # Start status printer (every 5 minutes)
    async def status_printer():
        while True:
            await asyncio.sleep(300)  # 5 minutes
            await paper_trader.print_status()

    try:
        # Run collector and status printer concurrently
        await asyncio.gather(
            collector.start(),
            status_printer()
        )
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Stopping bot...")
        await collector.stop()
        await paper_trader.print_status()
        await db.close()


async def show_status():
    """Show current status and exit"""
    print(BANNER)
    await db.connect()
    await paper_trader.initialize()
    await paper_trader.print_status()

    # Show top creators
    creators = await db.get_creator_leaderboard(10)
    if creators:
        print("\nTOP CREATORS:")
        print("-" * 50)
        for i, c in enumerate(creators, 1):
            print(f"{i}. {c['wallet'][:20]}... | Score: {c['trust_score']:.1f} | Tokens: {c['tokens_created']}")

    await db.close()


def main():
    parser = argparse.ArgumentParser(description="CIPHER Pump.fun Sniper Bot")
    parser.add_argument("--collect", action="store_true", help="Only collect data, no trading")
    parser.add_argument("--status", action="store_true", help="Show current status")

    args = parser.parse_args()

    if args.status:
        asyncio.run(show_status())
    elif args.collect:
        asyncio.run(run_collector_only())
    else:
        if not IS_PAPER:
            print("[WARNING] Live trading not implemented yet. Running in paper mode.")
        asyncio.run(run_paper_trading())


if __name__ == "__main__":
    main()
