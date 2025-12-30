"""
CIPHER Sniper Bot - Configuration
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Mode
MODE = os.getenv("MODE", "paper")  # "paper" or "live"
IS_PAPER = MODE == "paper"

# RPC
RPC_URL = os.getenv("RPC_URL", "https://api.mainnet-beta.solana.com")

# Pump.fun WebSocket
PUMP_FUN_WS = "wss://pumpportal.fun/api/data"

# Pump.fun Program ID
PUMP_FUN_PROGRAM = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"

# Paper Trading
PAPER_INITIAL_BALANCE = float(os.getenv("PAPER_INITIAL_BALANCE", "1.0"))

# Trading Parameters
MAX_POSITION_SIZE = float(os.getenv("MAX_POSITION_SIZE", "0.1"))
MAX_OPEN_POSITIONS = int(os.getenv("MAX_OPEN_POSITIONS", "5"))
STOP_LOSS_PERCENT = float(os.getenv("STOP_LOSS_PERCENT", "25"))
TAKE_PROFIT_1_PERCENT = float(os.getenv("TAKE_PROFIT_1_PERCENT", "50"))
TAKE_PROFIT_2_PERCENT = float(os.getenv("TAKE_PROFIT_2_PERCENT", "100"))

# Creator Scoring
MIN_CREATOR_SCORE = float(os.getenv("MIN_CREATOR_SCORE", "50"))
MIN_CREATOR_TOKENS = int(os.getenv("MIN_CREATOR_TOKENS", "2"))

# Database
DB_PATH = DATA_DIR / "cipher_sniper.db"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Position sizing by creator score
def get_position_size(creator_score: float) -> float:
    """Determine position size based on creator score"""
    if creator_score >= 80:
        return MAX_POSITION_SIZE
    elif creator_score >= 60:
        return MAX_POSITION_SIZE * 0.5
    else:
        return MAX_POSITION_SIZE * 0.25
