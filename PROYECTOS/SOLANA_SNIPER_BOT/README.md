# CIPHER SNIPER BOT

Paper trading bot for Pump.fun tokens on Solana.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run in paper trading mode
python main.py
```

## Commands

```bash
# Full paper trading (collect + simulate trades)
python main.py

# Only collect data (no trading)
python main.py --collect

# Show current status
python main.py --status
```

## Configuration

Edit `.env` to adjust parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| MODE | paper | paper or live (live not implemented) |
| PAPER_INITIAL_BALANCE | 1.0 | Starting SOL balance |
| MAX_POSITION_SIZE | 0.1 | Max SOL per trade |
| MAX_OPEN_POSITIONS | 5 | Max concurrent positions |
| STOP_LOSS_PERCENT | 25 | Stop loss trigger |
| TAKE_PROFIT_1_PERCENT | 50 | First take profit level |
| TAKE_PROFIT_2_PERCENT | 100 | Second take profit level |
| MIN_CREATOR_SCORE | 60 | Minimum creator score to trade |
| MIN_CREATOR_TOKENS | 2 | Min previous tokens by creator |

## How It Works

1. **Data Collection**: Connects to Pump.fun WebSocket and collects all new tokens
2. **Creator Scoring**: Tracks creator wallets and their historical performance
3. **Trade Decision**: Only trades tokens from creators with good track record
4. **Paper Trading**: Simulates trades without real money

## Database

SQLite database in `data/cipher_sniper.db` stores:
- All tokens created
- Creator wallet history and scores
- Price history
- Paper trades and portfolio

## Files

```
SOLANA_SNIPER_BOT/
├── main.py           # Entry point
├── requirements.txt  # Python dependencies
├── .env              # Configuration
├── data/             # Database storage
└── src/
    ├── config.py     # Configuration loader
    ├── database.py   # SQLite async database
    ├── collector.py  # Pump.fun WebSocket collector
    └── paper_trader.py # Paper trading engine
```

---
CIPHER | Data-Driven Trading
