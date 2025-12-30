"""
CIPHER Sniper Bot - Pump.fun Data Collector
WebSocket connection to collect new tokens in real-time
"""
import asyncio
import json
import websockets
from datetime import datetime
from typing import Optional, Callable, Dict, Any

from config import PUMP_FUN_WS
from database import db


class PumpFunCollector:
    """
    Connects to Pump.fun WebSocket and collects new token data
    """

    def __init__(self):
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.running = False
        self.tokens_collected = 0
        self.on_new_token: Optional[Callable] = None  # Callback for new tokens

    async def connect(self):
        """Establish WebSocket connection"""
        print(f"[COLLECTOR] Connecting to {PUMP_FUN_WS}...")

        try:
            self.ws = await websockets.connect(
                PUMP_FUN_WS,
                ping_interval=30,
                ping_timeout=10
            )
            print("[COLLECTOR] Connected to Pump.fun WebSocket")

            # Subscribe to new token events
            await self._subscribe()
            return True

        except Exception as e:
            print(f"[COLLECTOR] Connection failed: {e}")
            return False

    async def _subscribe(self):
        """Subscribe to new token creation events"""
        # Subscribe to newTokens channel
        subscribe_msg = {
            "method": "subscribeNewToken"
        }
        await self.ws.send(json.dumps(subscribe_msg))
        print("[COLLECTOR] Subscribed to newToken events")

    async def start(self):
        """Start collecting data"""
        self.running = True

        while self.running:
            try:
                if not self.ws or self.ws.closed:
                    success = await self.connect()
                    if not success:
                        print("[COLLECTOR] Retrying in 5 seconds...")
                        await asyncio.sleep(5)
                        continue

                # Listen for messages
                async for message in self.ws:
                    await self._handle_message(message)

            except websockets.ConnectionClosed:
                print("[COLLECTOR] Connection closed, reconnecting...")
                await asyncio.sleep(2)

            except Exception as e:
                print(f"[COLLECTOR] Error: {e}")
                await asyncio.sleep(5)

    async def _handle_message(self, message: str):
        """Process incoming WebSocket message"""
        try:
            data = json.loads(message)

            # Handle different message types
            if "mint" in data:
                await self._process_new_token(data)
            elif "txType" in data:
                await self._process_trade(data)

        except json.JSONDecodeError:
            print(f"[COLLECTOR] Invalid JSON: {message[:100]}")
        except Exception as e:
            print(f"[COLLECTOR] Error processing message: {e}")

    async def _process_new_token(self, data: Dict[str, Any]):
        """Process new token creation event"""
        mint = data.get("mint")
        name = data.get("name", "Unknown")
        symbol = data.get("symbol", "???")
        creator = data.get("traderPublicKey") or data.get("creator")
        uri = data.get("uri")

        if not mint or not creator:
            return

        # Save to database
        saved = await db.add_token(mint, name, symbol, creator, uri)

        if saved:
            self.tokens_collected += 1

            # Get creator info
            creator_info = await db.get_creator(creator)
            tokens_by_creator = creator_info.get("tokens_created", 1) if creator_info else 1
            trust_score = creator_info.get("trust_score", 50) if creator_info else 50

            print(f"\n[NEW TOKEN] {symbol} ({name})")
            print(f"  Mint: {mint[:20]}...")
            print(f"  Creator: {creator[:20]}... (tokens: {tokens_by_creator}, score: {trust_score})")
            print(f"  Total collected: {self.tokens_collected}")

            # Trigger callback if set
            if self.on_new_token:
                await self.on_new_token({
                    "mint": mint,
                    "name": name,
                    "symbol": symbol,
                    "creator": creator,
                    "uri": uri,
                    "creator_tokens": tokens_by_creator,
                    "creator_score": trust_score,
                    "timestamp": datetime.now()
                })

    async def _process_trade(self, data: Dict[str, Any]):
        """Process trade event (buy/sell)"""
        tx_type = data.get("txType")
        mint = data.get("mint")

        if not mint:
            return

        # Extract price info if available
        sol_amount = data.get("solAmount", 0)
        token_amount = data.get("tokenAmount", 0)

        if sol_amount and token_amount:
            # Calculate approximate price
            price = sol_amount / token_amount if token_amount > 0 else 0
            mcap = data.get("marketCapSol", 0)

            # Update token price in database
            await db.update_token_price(mint, price, mcap)

    async def stop(self):
        """Stop the collector"""
        self.running = False
        if self.ws:
            await self.ws.close()
        print(f"[COLLECTOR] Stopped. Total tokens collected: {self.tokens_collected}")


# Singleton instance
collector = PumpFunCollector()


# Test runner
async def test_collector():
    """Test the collector for a few minutes"""
    await db.connect()

    print("=" * 60)
    print("CIPHER PUMP.FUN DATA COLLECTOR")
    print("=" * 60)
    print("Collecting new tokens... Press Ctrl+C to stop\n")

    try:
        await collector.start()
    except KeyboardInterrupt:
        await collector.stop()
        await db.close()


if __name__ == "__main__":
    asyncio.run(test_collector())
