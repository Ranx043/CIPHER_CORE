# 📊 NEURONA: MARKET DATA ENGINEERING
## CIPHER_CORE :: Data Analytics Intelligence

> **Código Neuronal**: `C50002`
> **Dominio**: Market Data, Price Feeds, Order Book Analysis
> **Estado**: `ACTIVA`
> **Última Evolución**: 2025-01-XX

---

## 🧬 IDENTIDAD DE LA NEURONA

```
╔══════════════════════════════════════════════════════════════╗
║  CIPHER MARKET DATA - Real-Time Market Intelligence          ║
║  "Data is the new alpha - capture it, process it, profit"    ║
╠══════════════════════════════════════════════════════════════╣
║  Especialización: Price feeds, order books, market structure ║
║  Conexiones: Analytics, Trading, ML Systems                  ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 📈 PRICE DATA COLLECTION

### Multi-Source Price Aggregator

```python
"""
CIPHER Market Data Collection System
Real-time and historical price data from multiple sources
"""

import asyncio
import aiohttp
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np
from decimal import Decimal, ROUND_DOWN
import websockets
import json

@dataclass
class PricePoint:
    """Single price observation"""
    timestamp: datetime
    source: str
    symbol: str
    price: Decimal
    volume_24h: Optional[Decimal] = None
    bid: Optional[Decimal] = None
    ask: Optional[Decimal] = None
    confidence: float = 1.0

@dataclass
class AggregatedPrice:
    """Volume-weighted aggregated price"""
    symbol: str
    timestamp: datetime
    price: Decimal
    sources: int
    confidence: float
    spread: Decimal
    prices: Dict[str, Decimal] = field(default_factory=dict)

class PriceAggregator:
    """
    Aggregate prices from multiple sources with outlier detection
    """

    def __init__(self, max_deviation: float = 0.02):
        self.max_deviation = max_deviation  # 2% max deviation
        self.price_history: Dict[str, List[PricePoint]] = defaultdict(list)
        self.source_weights = {
            'binance': 1.0,
            'coinbase': 0.95,
            'kraken': 0.9,
            'okx': 0.85,
            'kucoin': 0.8,
            'coingecko': 0.7,
            'chainlink': 1.0,  # Oracle prices are trusted
            'uniswap': 0.75,
        }

    def add_price(self, price_point: PricePoint):
        """Add new price observation"""
        self.price_history[price_point.symbol].append(price_point)

        # Keep last 1000 prices per symbol
        if len(self.price_history[price_point.symbol]) > 1000:
            self.price_history[price_point.symbol] = \
                self.price_history[price_point.symbol][-1000:]

    def get_aggregated_price(
        self,
        symbol: str,
        max_age_seconds: int = 60
    ) -> Optional[AggregatedPrice]:
        """Calculate volume-weighted average price with outlier removal"""

        cutoff = datetime.utcnow() - timedelta(seconds=max_age_seconds)
        recent_prices = [
            p for p in self.price_history[symbol]
            if p.timestamp > cutoff
        ]

        if not recent_prices:
            return None

        # Calculate median for outlier detection
        prices_array = np.array([float(p.price) for p in recent_prices])
        median_price = np.median(prices_array)

        # Filter outliers (outside max_deviation from median)
        valid_prices = [
            p for p in recent_prices
            if abs(float(p.price) - median_price) / median_price <= self.max_deviation
        ]

        if not valid_prices:
            valid_prices = recent_prices  # Fallback to all if too many filtered

        # Volume-weighted average
        total_weight = Decimal('0')
        weighted_sum = Decimal('0')
        source_prices = {}

        for p in valid_prices:
            weight = Decimal(str(self.source_weights.get(p.source, 0.5)))
            weight *= Decimal(str(p.confidence))

            if p.volume_24h and p.volume_24h > 0:
                weight *= (p.volume_24h / Decimal('1000000')).min(Decimal('10'))

            weighted_sum += p.price * weight
            total_weight += weight
            source_prices[p.source] = p.price

        if total_weight == 0:
            return None

        avg_price = (weighted_sum / total_weight).quantize(
            Decimal('0.00000001'), rounding=ROUND_DOWN
        )

        # Calculate spread
        min_price = min(p.price for p in valid_prices)
        max_price = max(p.price for p in valid_prices)
        spread = ((max_price - min_price) / avg_price * 100).quantize(
            Decimal('0.01'), rounding=ROUND_DOWN
        )

        # Confidence based on source count and consistency
        confidence = min(len(set(p.source for p in valid_prices)) / 5, 1.0)
        if float(spread) > 1.0:
            confidence *= 0.8

        return AggregatedPrice(
            symbol=symbol,
            timestamp=datetime.utcnow(),
            price=avg_price,
            sources=len(set(p.source for p in valid_prices)),
            confidence=confidence,
            spread=spread,
            prices=source_prices
        )


class ExchangeDataCollector:
    """
    Collect data from multiple exchanges
    """

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.aggregator = PriceAggregator()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()

    async def fetch_binance(self, symbols: List[str]) -> List[PricePoint]:
        """Fetch from Binance"""
        prices = []

        try:
            # Ticker 24h endpoint
            async with self.session.get(
                'https://api.binance.com/api/v3/ticker/24hr'
            ) as resp:
                data = await resp.json()

            symbol_map = {s.replace('/', ''): s for s in symbols}

            for ticker in data:
                binance_symbol = ticker['symbol']
                if binance_symbol in symbol_map:
                    prices.append(PricePoint(
                        timestamp=datetime.utcnow(),
                        source='binance',
                        symbol=symbol_map[binance_symbol],
                        price=Decimal(ticker['lastPrice']),
                        volume_24h=Decimal(ticker['quoteVolume']),
                        bid=Decimal(ticker['bidPrice']),
                        ask=Decimal(ticker['askPrice'])
                    ))
        except Exception as e:
            print(f"Binance error: {e}")

        return prices

    async def fetch_coinbase(self, symbols: List[str]) -> List[PricePoint]:
        """Fetch from Coinbase"""
        prices = []

        for symbol in symbols:
            try:
                cb_symbol = symbol.replace('/', '-')
                async with self.session.get(
                    f'https://api.coinbase.com/v2/prices/{cb_symbol}/spot'
                ) as resp:
                    data = await resp.json()

                if 'data' in data:
                    prices.append(PricePoint(
                        timestamp=datetime.utcnow(),
                        source='coinbase',
                        symbol=symbol,
                        price=Decimal(data['data']['amount'])
                    ))
            except Exception as e:
                print(f"Coinbase error for {symbol}: {e}")

        return prices

    async def fetch_coingecko(self, symbols: List[str]) -> List[PricePoint]:
        """Fetch from CoinGecko"""
        prices = []

        # Map symbols to CoinGecko IDs
        id_map = {
            'BTC/USD': 'bitcoin',
            'ETH/USD': 'ethereum',
            'SOL/USD': 'solana',
            'AVAX/USD': 'avalanche-2',
            'MATIC/USD': 'matic-network',
            'DOT/USD': 'polkadot',
            'ATOM/USD': 'cosmos',
            'LINK/USD': 'chainlink',
        }

        ids = [id_map[s] for s in symbols if s in id_map]

        try:
            async with self.session.get(
                'https://api.coingecko.com/api/v3/simple/price',
                params={
                    'ids': ','.join(ids),
                    'vs_currencies': 'usd',
                    'include_24hr_vol': 'true'
                }
            ) as resp:
                data = await resp.json()

            reverse_map = {v: k for k, v in id_map.items()}

            for coin_id, info in data.items():
                if coin_id in reverse_map:
                    prices.append(PricePoint(
                        timestamp=datetime.utcnow(),
                        source='coingecko',
                        symbol=reverse_map[coin_id],
                        price=Decimal(str(info['usd'])),
                        volume_24h=Decimal(str(info.get('usd_24h_vol', 0)))
                    ))
        except Exception as e:
            print(f"CoinGecko error: {e}")

        return prices

    async def collect_all(self, symbols: List[str]) -> Dict[str, AggregatedPrice]:
        """Collect from all sources and aggregate"""

        # Fetch in parallel
        results = await asyncio.gather(
            self.fetch_binance(symbols),
            self.fetch_coinbase(symbols),
            self.fetch_coingecko(symbols),
            return_exceptions=True
        )

        # Add all prices to aggregator
        for result in results:
            if isinstance(result, list):
                for price in result:
                    self.aggregator.add_price(price)

        # Get aggregated prices
        aggregated = {}
        for symbol in symbols:
            agg = self.aggregator.get_aggregated_price(symbol)
            if agg:
                aggregated[symbol] = agg

        return aggregated


# WebSocket Real-time Feed
class BinanceWebSocketFeed:
    """Real-time price feed via WebSocket"""

    def __init__(self, symbols: List[str], callback):
        self.symbols = [s.lower().replace('/', '') for s in symbols]
        self.callback = callback
        self.ws = None
        self.running = False

    async def connect(self):
        """Connect to Binance WebSocket"""
        streams = '/'.join([f"{s}@ticker" for s in self.symbols])
        url = f"wss://stream.binance.com:9443/stream?streams={streams}"

        self.running = True

        async with websockets.connect(url) as ws:
            self.ws = ws

            while self.running:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=30)
                    data = json.loads(msg)

                    if 'data' in data:
                        ticker = data['data']
                        price_point = PricePoint(
                            timestamp=datetime.utcnow(),
                            source='binance_ws',
                            symbol=ticker['s'],
                            price=Decimal(ticker['c']),
                            volume_24h=Decimal(ticker['q']),
                            bid=Decimal(ticker['b']),
                            ask=Decimal(ticker['a'])
                        )
                        await self.callback(price_point)

                except asyncio.TimeoutError:
                    # Send ping
                    await ws.ping()
                except Exception as e:
                    print(f"WebSocket error: {e}")
                    break

    async def disconnect(self):
        """Disconnect from WebSocket"""
        self.running = False
        if self.ws:
            await self.ws.close()
```

---

## 📊 ORDER BOOK ANALYSIS

### Order Book Data Structures

```python
"""
CIPHER Order Book Analysis System
Deep market microstructure analysis
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from decimal import Decimal
import numpy as np
from collections import deque
from datetime import datetime

@dataclass
class OrderBookLevel:
    """Single price level in order book"""
    price: Decimal
    quantity: Decimal
    count: int = 1  # Number of orders at this level

@dataclass
class OrderBook:
    """Full order book snapshot"""
    symbol: str
    timestamp: datetime
    bids: List[OrderBookLevel]  # Sorted descending (best bid first)
    asks: List[OrderBookLevel]  # Sorted ascending (best ask first)

    @property
    def best_bid(self) -> Optional[Decimal]:
        return self.bids[0].price if self.bids else None

    @property
    def best_ask(self) -> Optional[Decimal]:
        return self.asks[0].price if self.asks else None

    @property
    def mid_price(self) -> Optional[Decimal]:
        if self.best_bid and self.best_ask:
            return (self.best_bid + self.best_ask) / 2
        return None

    @property
    def spread(self) -> Optional[Decimal]:
        if self.best_bid and self.best_ask:
            return self.best_ask - self.best_bid
        return None

    @property
    def spread_bps(self) -> Optional[float]:
        """Spread in basis points"""
        if self.spread and self.mid_price:
            return float(self.spread / self.mid_price * 10000)
        return None


class OrderBookAnalyzer:
    """
    Analyze order book for market microstructure insights
    """

    def __init__(self):
        self.book_history: deque = deque(maxlen=1000)

    def analyze(self, book: OrderBook) -> Dict:
        """Comprehensive order book analysis"""

        self.book_history.append(book)

        return {
            'basic_metrics': self._basic_metrics(book),
            'depth_analysis': self._depth_analysis(book),
            'imbalance': self._calculate_imbalance(book),
            'liquidity_zones': self._find_liquidity_zones(book),
            'wall_detection': self._detect_walls(book),
            'market_impact': self._estimate_market_impact(book),
        }

    def _basic_metrics(self, book: OrderBook) -> Dict:
        """Basic order book metrics"""
        return {
            'best_bid': float(book.best_bid) if book.best_bid else None,
            'best_ask': float(book.best_ask) if book.best_ask else None,
            'mid_price': float(book.mid_price) if book.mid_price else None,
            'spread': float(book.spread) if book.spread else None,
            'spread_bps': book.spread_bps,
            'bid_levels': len(book.bids),
            'ask_levels': len(book.asks),
        }

    def _depth_analysis(
        self,
        book: OrderBook,
        depth_percentages: List[float] = [0.1, 0.5, 1.0, 2.0, 5.0]
    ) -> Dict:
        """Analyze order book depth at various price levels"""

        if not book.mid_price:
            return {}

        mid = float(book.mid_price)
        depth = {}

        for pct in depth_percentages:
            # Bid depth
            bid_threshold = mid * (1 - pct/100)
            bid_depth = sum(
                float(level.price * level.quantity)
                for level in book.bids
                if float(level.price) >= bid_threshold
            )

            # Ask depth
            ask_threshold = mid * (1 + pct/100)
            ask_depth = sum(
                float(level.price * level.quantity)
                for level in book.asks
                if float(level.price) <= ask_threshold
            )

            depth[f'{pct}%'] = {
                'bid_depth_usd': bid_depth,
                'ask_depth_usd': ask_depth,
                'total_depth_usd': bid_depth + ask_depth,
                'depth_ratio': bid_depth / ask_depth if ask_depth > 0 else float('inf')
            }

        return depth

    def _calculate_imbalance(
        self,
        book: OrderBook,
        levels: int = 10
    ) -> Dict:
        """Calculate order book imbalance"""

        bid_volume = sum(
            float(level.quantity)
            for level in book.bids[:levels]
        )
        ask_volume = sum(
            float(level.quantity)
            for level in book.asks[:levels]
        )

        total = bid_volume + ask_volume

        if total == 0:
            return {'imbalance': 0, 'signal': 'neutral'}

        # Imbalance: positive = more bids (bullish), negative = more asks (bearish)
        imbalance = (bid_volume - ask_volume) / total

        # Weighted imbalance (closer to mid price = higher weight)
        weighted_bid = sum(
            float(level.quantity) * (levels - i)
            for i, level in enumerate(book.bids[:levels])
        )
        weighted_ask = sum(
            float(level.quantity) * (levels - i)
            for i, level in enumerate(book.asks[:levels])
        )
        weighted_total = weighted_bid + weighted_ask
        weighted_imbalance = (weighted_bid - weighted_ask) / weighted_total if weighted_total > 0 else 0

        signal = 'neutral'
        if imbalance > 0.3:
            signal = 'bullish'
        elif imbalance < -0.3:
            signal = 'bearish'

        return {
            'imbalance': imbalance,
            'weighted_imbalance': weighted_imbalance,
            'bid_volume': bid_volume,
            'ask_volume': ask_volume,
            'signal': signal
        }

    def _find_liquidity_zones(
        self,
        book: OrderBook,
        threshold_multiplier: float = 3.0
    ) -> Dict:
        """Find significant liquidity zones (support/resistance)"""

        # Calculate average quantity per level
        all_quantities = [float(l.quantity) for l in book.bids + book.asks]
        if not all_quantities:
            return {'support_zones': [], 'resistance_zones': []}

        avg_qty = np.mean(all_quantities)
        threshold = avg_qty * threshold_multiplier

        # Find support zones (large bid walls)
        support_zones = [
            {
                'price': float(level.price),
                'quantity': float(level.quantity),
                'value_usd': float(level.price * level.quantity),
                'strength': float(level.quantity) / avg_qty
            }
            for level in book.bids
            if float(level.quantity) > threshold
        ]

        # Find resistance zones (large ask walls)
        resistance_zones = [
            {
                'price': float(level.price),
                'quantity': float(level.quantity),
                'value_usd': float(level.price * level.quantity),
                'strength': float(level.quantity) / avg_qty
            }
            for level in book.asks
            if float(level.quantity) > threshold
        ]

        return {
            'support_zones': support_zones[:5],  # Top 5
            'resistance_zones': resistance_zones[:5]
        }

    def _detect_walls(
        self,
        book: OrderBook,
        wall_threshold: float = 5.0  # 5x average size
    ) -> Dict:
        """Detect buy/sell walls"""

        all_sizes = [float(l.quantity) for l in book.bids[:20] + book.asks[:20]]
        if not all_sizes:
            return {'buy_walls': [], 'sell_walls': []}

        avg_size = np.mean(all_sizes)
        std_size = np.std(all_sizes)
        threshold = avg_size + wall_threshold * std_size

        buy_walls = []
        for level in book.bids[:50]:
            if float(level.quantity) > threshold:
                buy_walls.append({
                    'price': float(level.price),
                    'size': float(level.quantity),
                    'value_usd': float(level.price * level.quantity),
                    'z_score': (float(level.quantity) - avg_size) / std_size if std_size > 0 else 0
                })

        sell_walls = []
        for level in book.asks[:50]:
            if float(level.quantity) > threshold:
                sell_walls.append({
                    'price': float(level.price),
                    'size': float(level.quantity),
                    'value_usd': float(level.price * level.quantity),
                    'z_score': (float(level.quantity) - avg_size) / std_size if std_size > 0 else 0
                })

        return {
            'buy_walls': buy_walls,
            'sell_walls': sell_walls,
            'avg_level_size': avg_size,
            'size_std': std_size
        }

    def _estimate_market_impact(
        self,
        book: OrderBook,
        trade_sizes_usd: List[float] = [10000, 50000, 100000, 500000, 1000000]
    ) -> Dict:
        """Estimate price impact for various trade sizes"""

        impact = {}

        for size in trade_sizes_usd:
            # Buy impact (walking up the asks)
            buy_impact = self._calculate_execution_price(
                book.asks, size, is_buy=True, mid=float(book.mid_price)
            )

            # Sell impact (walking down the bids)
            sell_impact = self._calculate_execution_price(
                book.bids, size, is_buy=False, mid=float(book.mid_price)
            )

            impact[f'${size:,}'] = {
                'buy_impact_bps': buy_impact,
                'sell_impact_bps': sell_impact,
                'round_trip_cost_bps': buy_impact + abs(sell_impact)
            }

        return impact

    def _calculate_execution_price(
        self,
        levels: List[OrderBookLevel],
        size_usd: float,
        is_buy: bool,
        mid: float
    ) -> float:
        """Calculate average execution price for a given size"""

        remaining = size_usd
        total_qty = 0
        total_cost = 0

        for level in levels:
            level_value = float(level.price * level.quantity)

            if level_value >= remaining:
                # Partial fill at this level
                qty = remaining / float(level.price)
                total_qty += qty
                total_cost += remaining
                remaining = 0
                break
            else:
                # Full fill at this level
                total_qty += float(level.quantity)
                total_cost += level_value
                remaining -= level_value

        if total_qty == 0:
            return float('inf') if is_buy else float('-inf')

        avg_price = total_cost / total_qty
        impact_bps = (avg_price - mid) / mid * 10000

        return impact_bps if is_buy else -impact_bps
```

---

## 📉 OHLCV DATA MANAGEMENT

### Candlestick Data Pipeline

```python
"""
CIPHER OHLCV Data Management
Candlestick aggregation and storage
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
import pandas as pd
import numpy as np
from enum import Enum

class Timeframe(Enum):
    """Standard trading timeframes"""
    M1 = '1m'
    M5 = '5m'
    M15 = '15m'
    M30 = '30m'
    H1 = '1h'
    H4 = '4h'
    D1 = '1d'
    W1 = '1w'
    MN1 = '1M'

    @property
    def seconds(self) -> int:
        mapping = {
            '1m': 60, '5m': 300, '15m': 900, '30m': 1800,
            '1h': 3600, '4h': 14400, '1d': 86400, '1w': 604800,
            '1M': 2592000
        }
        return mapping[self.value]

@dataclass
class OHLCV:
    """Single candlestick"""
    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    trades: int = 0

    @property
    def body_size(self) -> Decimal:
        return abs(self.close - self.open)

    @property
    def upper_wick(self) -> Decimal:
        return self.high - max(self.open, self.close)

    @property
    def lower_wick(self) -> Decimal:
        return min(self.open, self.close) - self.low

    @property
    def is_bullish(self) -> bool:
        return self.close > self.open

    @property
    def range(self) -> Decimal:
        return self.high - self.low


class OHLCVAggregator:
    """
    Aggregate tick data into OHLCV candles
    """

    def __init__(self):
        self.current_candles: Dict[str, Dict[Timeframe, OHLCV]] = {}
        self.completed_candles: Dict[str, Dict[Timeframe, List[OHLCV]]] = {}

    def process_tick(
        self,
        symbol: str,
        timestamp: datetime,
        price: Decimal,
        volume: Decimal
    ) -> Dict[Timeframe, Optional[OHLCV]]:
        """
        Process a tick and return any completed candles
        """

        if symbol not in self.current_candles:
            self.current_candles[symbol] = {}
            self.completed_candles[symbol] = {tf: [] for tf in Timeframe}

        completed = {}

        for timeframe in Timeframe:
            candle_start = self._get_candle_start(timestamp, timeframe)

            if timeframe not in self.current_candles[symbol]:
                # Start new candle
                self.current_candles[symbol][timeframe] = OHLCV(
                    timestamp=candle_start,
                    open=price,
                    high=price,
                    low=price,
                    close=price,
                    volume=volume,
                    trades=1
                )
                completed[timeframe] = None
            else:
                current = self.current_candles[symbol][timeframe]

                if candle_start > current.timestamp:
                    # Complete current candle and start new one
                    self.completed_candles[symbol][timeframe].append(current)
                    completed[timeframe] = current

                    self.current_candles[symbol][timeframe] = OHLCV(
                        timestamp=candle_start,
                        open=price,
                        high=price,
                        low=price,
                        close=price,
                        volume=volume,
                        trades=1
                    )
                else:
                    # Update current candle
                    current.high = max(current.high, price)
                    current.low = min(current.low, price)
                    current.close = price
                    current.volume += volume
                    current.trades += 1
                    completed[timeframe] = None

        return completed

    def _get_candle_start(self, timestamp: datetime, timeframe: Timeframe) -> datetime:
        """Calculate the start time of the candle containing this timestamp"""

        if timeframe == Timeframe.M1:
            return timestamp.replace(second=0, microsecond=0)
        elif timeframe == Timeframe.M5:
            return timestamp.replace(
                minute=timestamp.minute // 5 * 5,
                second=0, microsecond=0
            )
        elif timeframe == Timeframe.M15:
            return timestamp.replace(
                minute=timestamp.minute // 15 * 15,
                second=0, microsecond=0
            )
        elif timeframe == Timeframe.M30:
            return timestamp.replace(
                minute=timestamp.minute // 30 * 30,
                second=0, microsecond=0
            )
        elif timeframe == Timeframe.H1:
            return timestamp.replace(minute=0, second=0, microsecond=0)
        elif timeframe == Timeframe.H4:
            return timestamp.replace(
                hour=timestamp.hour // 4 * 4,
                minute=0, second=0, microsecond=0
            )
        elif timeframe == Timeframe.D1:
            return timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
        elif timeframe == Timeframe.W1:
            days_since_monday = timestamp.weekday()
            return (timestamp - timedelta(days=days_since_monday)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        else:  # Monthly
            return timestamp.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    def get_history(
        self,
        symbol: str,
        timeframe: Timeframe,
        limit: int = 500
    ) -> List[OHLCV]:
        """Get historical candles"""

        if symbol not in self.completed_candles:
            return []

        candles = self.completed_candles[symbol].get(timeframe, [])
        return candles[-limit:]

    def to_dataframe(
        self,
        symbol: str,
        timeframe: Timeframe,
        limit: int = 500
    ) -> pd.DataFrame:
        """Convert to pandas DataFrame"""

        candles = self.get_history(symbol, timeframe, limit)

        if not candles:
            return pd.DataFrame()

        data = {
            'timestamp': [c.timestamp for c in candles],
            'open': [float(c.open) for c in candles],
            'high': [float(c.high) for c in candles],
            'low': [float(c.low) for c in candles],
            'close': [float(c.close) for c in candles],
            'volume': [float(c.volume) for c in candles],
            'trades': [c.trades for c in candles]
        }

        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)

        return df


class OHLCVStorage:
    """
    Persistent storage for OHLCV data
    """

    def __init__(self, base_path: str):
        self.base_path = base_path

    def save_parquet(
        self,
        symbol: str,
        timeframe: Timeframe,
        df: pd.DataFrame
    ):
        """Save to Parquet file"""
        import pyarrow as pa
        import pyarrow.parquet as pq

        path = f"{self.base_path}/{symbol}/{timeframe.value}"

        table = pa.Table.from_pandas(df)
        pq.write_table(
            table,
            f"{path}/data.parquet",
            compression='snappy'
        )

    def load_parquet(
        self,
        symbol: str,
        timeframe: Timeframe,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """Load from Parquet file with optional date filtering"""
        import pyarrow.parquet as pq

        path = f"{self.base_path}/{symbol}/{timeframe.value}/data.parquet"

        filters = []
        if start_date:
            filters.append(('timestamp', '>=', start_date))
        if end_date:
            filters.append(('timestamp', '<=', end_date))

        table = pq.read_table(path, filters=filters if filters else None)
        return table.to_pandas()

    def append_candles(
        self,
        symbol: str,
        timeframe: Timeframe,
        new_candles: List[OHLCV]
    ):
        """Append new candles to existing data"""

        # Load existing
        try:
            existing_df = self.load_parquet(symbol, timeframe)
        except FileNotFoundError:
            existing_df = pd.DataFrame()

        # Convert new candles to DataFrame
        new_data = {
            'timestamp': [c.timestamp for c in new_candles],
            'open': [float(c.open) for c in new_candles],
            'high': [float(c.high) for c in new_candles],
            'low': [float(c.low) for c in new_candles],
            'close': [float(c.close) for c in new_candles],
            'volume': [float(c.volume) for c in new_candles],
            'trades': [c.trades for c in new_candles]
        }
        new_df = pd.DataFrame(new_data)
        new_df.set_index('timestamp', inplace=True)

        # Merge and deduplicate
        if not existing_df.empty:
            combined = pd.concat([existing_df, new_df])
            combined = combined[~combined.index.duplicated(keep='last')]
            combined.sort_index(inplace=True)
        else:
            combined = new_df

        # Save
        self.save_parquet(symbol, timeframe, combined)
```

---

## 🔄 TRADE DATA ANALYSIS

### Trade Flow Analysis

```python
"""
CIPHER Trade Flow Analysis
Analyze individual trades for market insights
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from collections import defaultdict
import numpy as np

@dataclass
class Trade:
    """Individual trade"""
    id: str
    timestamp: datetime
    symbol: str
    price: Decimal
    quantity: Decimal
    side: str  # 'buy' or 'sell' (taker side)
    is_maker: bool = False

    @property
    def value(self) -> Decimal:
        return self.price * self.quantity

class TradeFlowAnalyzer:
    """
    Analyze trade flow for market insights
    """

    def __init__(self, window_minutes: int = 60):
        self.trades: Dict[str, List[Trade]] = defaultdict(list)
        self.window = timedelta(minutes=window_minutes)

    def add_trade(self, trade: Trade):
        """Add a trade to the analyzer"""
        self.trades[trade.symbol].append(trade)

        # Cleanup old trades
        cutoff = datetime.utcnow() - self.window * 2
        self.trades[trade.symbol] = [
            t for t in self.trades[trade.symbol]
            if t.timestamp > cutoff
        ]

    def analyze(self, symbol: str) -> Dict:
        """Full trade flow analysis"""

        cutoff = datetime.utcnow() - self.window
        recent_trades = [
            t for t in self.trades[symbol]
            if t.timestamp > cutoff
        ]

        if not recent_trades:
            return {}

        return {
            'summary': self._trade_summary(recent_trades),
            'buy_sell_ratio': self._buy_sell_analysis(recent_trades),
            'large_trades': self._large_trade_detection(recent_trades),
            'velocity': self._trade_velocity(recent_trades),
            'price_levels': self._price_level_analysis(recent_trades),
            'momentum': self._momentum_analysis(recent_trades),
        }

    def _trade_summary(self, trades: List[Trade]) -> Dict:
        """Basic trade statistics"""

        total_volume = sum(float(t.quantity) for t in trades)
        total_value = sum(float(t.value) for t in trades)

        buy_trades = [t for t in trades if t.side == 'buy']
        sell_trades = [t for t in trades if t.side == 'sell']

        return {
            'total_trades': len(trades),
            'total_volume': total_volume,
            'total_value_usd': total_value,
            'avg_trade_size': total_volume / len(trades) if trades else 0,
            'avg_trade_value': total_value / len(trades) if trades else 0,
            'buy_trades': len(buy_trades),
            'sell_trades': len(sell_trades),
            'vwap': total_value / total_volume if total_volume > 0 else 0
        }

    def _buy_sell_analysis(self, trades: List[Trade]) -> Dict:
        """Analyze buy/sell pressure"""

        buy_volume = sum(float(t.quantity) for t in trades if t.side == 'buy')
        sell_volume = sum(float(t.quantity) for t in trades if t.side == 'sell')
        buy_value = sum(float(t.value) for t in trades if t.side == 'buy')
        sell_value = sum(float(t.value) for t in trades if t.side == 'sell')

        total_volume = buy_volume + sell_volume
        total_value = buy_value + sell_value

        # Net flow
        net_flow = buy_value - sell_value

        # Delta (cumulative volume delta)
        delta = buy_volume - sell_volume

        return {
            'buy_volume': buy_volume,
            'sell_volume': sell_volume,
            'buy_value_usd': buy_value,
            'sell_value_usd': sell_value,
            'volume_ratio': buy_volume / sell_volume if sell_volume > 0 else float('inf'),
            'value_ratio': buy_value / sell_value if sell_value > 0 else float('inf'),
            'net_flow_usd': net_flow,
            'delta': delta,
            'pressure': 'buying' if net_flow > 0 else 'selling',
            'pressure_strength': abs(net_flow) / total_value if total_value > 0 else 0
        }

    def _large_trade_detection(
        self,
        trades: List[Trade],
        percentile: float = 95
    ) -> Dict:
        """Detect unusually large trades"""

        values = [float(t.value) for t in trades]
        if not values:
            return {'large_trades': [], 'whale_activity': False}

        threshold = np.percentile(values, percentile)

        large_trades = [
            {
                'timestamp': t.timestamp.isoformat(),
                'side': t.side,
                'price': float(t.price),
                'quantity': float(t.quantity),
                'value_usd': float(t.value),
                'z_score': (float(t.value) - np.mean(values)) / np.std(values) if np.std(values) > 0 else 0
            }
            for t in trades
            if float(t.value) > threshold
        ]

        # Whale activity indicator
        large_buy_value = sum(lt['value_usd'] for lt in large_trades if lt['side'] == 'buy')
        large_sell_value = sum(lt['value_usd'] for lt in large_trades if lt['side'] == 'sell')

        return {
            'threshold_usd': threshold,
            'large_trades': large_trades[-20:],  # Last 20
            'large_trade_count': len(large_trades),
            'large_buy_value': large_buy_value,
            'large_sell_value': large_sell_value,
            'whale_activity': len(large_trades) > len(trades) * 0.1,  # >10% large trades
            'whale_direction': 'accumulating' if large_buy_value > large_sell_value else 'distributing'
        }

    def _trade_velocity(self, trades: List[Trade]) -> Dict:
        """Analyze trade velocity over time"""

        if len(trades) < 2:
            return {}

        # Trades per minute
        time_span = (trades[-1].timestamp - trades[0].timestamp).total_seconds() / 60
        trades_per_minute = len(trades) / time_span if time_span > 0 else 0

        # Volume per minute
        total_volume = sum(float(t.quantity) for t in trades)
        volume_per_minute = total_volume / time_span if time_span > 0 else 0

        # Acceleration (change in velocity)
        mid_point = len(trades) // 2
        first_half = trades[:mid_point]
        second_half = trades[mid_point:]

        first_half_rate = len(first_half) / (time_span / 2) if time_span > 0 else 0
        second_half_rate = len(second_half) / (time_span / 2) if time_span > 0 else 0

        acceleration = second_half_rate - first_half_rate

        return {
            'time_span_minutes': time_span,
            'trades_per_minute': trades_per_minute,
            'volume_per_minute': volume_per_minute,
            'first_half_rate': first_half_rate,
            'second_half_rate': second_half_rate,
            'acceleration': acceleration,
            'activity_trend': 'increasing' if acceleration > 0 else 'decreasing'
        }

    def _price_level_analysis(self, trades: List[Trade]) -> Dict:
        """Analyze volume at different price levels"""

        # Group by rounded price
        price_volume = defaultdict(lambda: {'buy': 0, 'sell': 0, 'count': 0})

        prices = [float(t.price) for t in trades]
        if not prices:
            return {}

        # Determine rounding based on price
        avg_price = np.mean(prices)
        if avg_price > 10000:
            round_to = 100
        elif avg_price > 1000:
            round_to = 10
        elif avg_price > 100:
            round_to = 1
        else:
            round_to = 0.1

        for trade in trades:
            rounded_price = round(float(trade.price) / round_to) * round_to
            price_volume[rounded_price][trade.side] += float(trade.quantity)
            price_volume[rounded_price]['count'] += 1

        # Find high volume nodes (HVN) and low volume nodes (LVN)
        sorted_levels = sorted(
            price_volume.items(),
            key=lambda x: x[1]['buy'] + x[1]['sell'],
            reverse=True
        )

        hvn = [
            {
                'price': level,
                'buy_volume': data['buy'],
                'sell_volume': data['sell'],
                'total_volume': data['buy'] + data['sell'],
                'trade_count': data['count']
            }
            for level, data in sorted_levels[:5]
        ]

        return {
            'high_volume_nodes': hvn,
            'price_range': {'min': min(prices), 'max': max(prices)},
            'unique_levels': len(price_volume)
        }

    def _momentum_analysis(self, trades: List[Trade]) -> Dict:
        """Analyze short-term momentum from trades"""

        if len(trades) < 10:
            return {}

        # Recent vs older trades comparison
        recent = trades[-len(trades)//4:]
        older = trades[:len(trades)//4]

        recent_vwap = (
            sum(float(t.value) for t in recent) /
            sum(float(t.quantity) for t in recent)
            if sum(float(t.quantity) for t in recent) > 0 else 0
        )

        older_vwap = (
            sum(float(t.value) for t in older) /
            sum(float(t.quantity) for t in older)
            if sum(float(t.quantity) for t in older) > 0 else 0
        )

        # Price momentum
        price_change = recent_vwap - older_vwap
        price_change_pct = (price_change / older_vwap * 100) if older_vwap > 0 else 0

        # Volume momentum
        recent_volume = sum(float(t.quantity) for t in recent)
        older_volume = sum(float(t.quantity) for t in older)
        volume_change_pct = (
            (recent_volume - older_volume) / older_volume * 100
            if older_volume > 0 else 0
        )

        return {
            'recent_vwap': recent_vwap,
            'older_vwap': older_vwap,
            'price_change': price_change,
            'price_change_pct': price_change_pct,
            'volume_change_pct': volume_change_pct,
            'momentum_signal': 'bullish' if price_change > 0 and volume_change_pct > 0 else (
                'bearish' if price_change < 0 and volume_change_pct > 0 else 'neutral'
            )
        }
```

---

## 📡 FUNDING RATE ANALYSIS

### Perpetual Futures Data

```python
"""
CIPHER Funding Rate Analysis
Perpetual futures market insights
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
import numpy as np

@dataclass
class FundingRate:
    """Funding rate snapshot"""
    timestamp: datetime
    symbol: str
    rate: Decimal
    next_funding_time: datetime
    mark_price: Decimal
    index_price: Decimal

    @property
    def annualized_rate(self) -> float:
        """Annualized funding rate (assuming 8h intervals)"""
        return float(self.rate) * 3 * 365 * 100  # 3 times per day * 365 days * 100%

class FundingRateAnalyzer:
    """
    Analyze funding rates across exchanges
    """

    def __init__(self):
        self.history: Dict[str, Dict[str, List[FundingRate]]] = {}  # symbol -> exchange -> rates

    def add_rate(self, exchange: str, rate: FundingRate):
        """Add funding rate observation"""

        if rate.symbol not in self.history:
            self.history[rate.symbol] = {}
        if exchange not in self.history[rate.symbol]:
            self.history[rate.symbol][exchange] = []

        self.history[rate.symbol][exchange].append(rate)

        # Keep last 1000 rates per exchange
        if len(self.history[rate.symbol][exchange]) > 1000:
            self.history[rate.symbol][exchange] = \
                self.history[rate.symbol][exchange][-1000:]

    def analyze(self, symbol: str) -> Dict:
        """Full funding rate analysis"""

        if symbol not in self.history:
            return {}

        return {
            'current': self._current_rates(symbol),
            'historical': self._historical_analysis(symbol),
            'arbitrage': self._funding_arbitrage(symbol),
            'sentiment': self._funding_sentiment(symbol),
        }

    def _current_rates(self, symbol: str) -> Dict:
        """Current funding rates across exchanges"""

        current = {}

        for exchange, rates in self.history[symbol].items():
            if rates:
                latest = rates[-1]
                current[exchange] = {
                    'rate': float(latest.rate),
                    'annualized': latest.annualized_rate,
                    'next_funding': latest.next_funding_time.isoformat(),
                    'mark_price': float(latest.mark_price),
                    'index_price': float(latest.index_price),
                    'basis': float(latest.mark_price - latest.index_price),
                    'basis_pct': float(
                        (latest.mark_price - latest.index_price) /
                        latest.index_price * 100
                    )
                }

        # Aggregate
        rates_list = [v['rate'] for v in current.values()]
        if rates_list:
            current['aggregate'] = {
                'mean': np.mean(rates_list),
                'median': np.median(rates_list),
                'min': min(rates_list),
                'max': max(rates_list),
                'spread': max(rates_list) - min(rates_list)
            }

        return current

    def _historical_analysis(
        self,
        symbol: str,
        periods: List[int] = [7, 14, 30, 90]
    ) -> Dict:
        """Historical funding rate statistics"""

        # Combine all exchanges
        all_rates = []
        for exchange_rates in self.history[symbol].values():
            all_rates.extend(exchange_rates)

        all_rates.sort(key=lambda x: x.timestamp)

        if not all_rates:
            return {}

        analysis = {}

        for days in periods:
            cutoff = datetime.utcnow() - timedelta(days=days)
            period_rates = [r for r in all_rates if r.timestamp > cutoff]

            if period_rates:
                rates = [float(r.rate) for r in period_rates]

                # Cumulative funding
                cumulative = sum(rates)

                analysis[f'{days}d'] = {
                    'count': len(rates),
                    'mean': np.mean(rates),
                    'median': np.median(rates),
                    'std': np.std(rates),
                    'min': min(rates),
                    'max': max(rates),
                    'cumulative': cumulative,
                    'cumulative_annualized': cumulative * (365 / days) * 100,
                    'positive_count': sum(1 for r in rates if r > 0),
                    'negative_count': sum(1 for r in rates if r < 0),
                }

        return analysis

    def _funding_arbitrage(self, symbol: str) -> Dict:
        """Find funding rate arbitrage opportunities"""

        current = self._current_rates(symbol)

        if len(current) < 2:
            return {'opportunities': []}

        opportunities = []

        exchanges = [k for k in current.keys() if k != 'aggregate']

        for i, ex1 in enumerate(exchanges):
            for ex2 in exchanges[i+1:]:
                rate1 = current[ex1]['rate']
                rate2 = current[ex2]['rate']
                spread = abs(rate1 - rate2)

                if spread > 0.0001:  # >0.01% spread
                    # Long where funding is lower, short where higher
                    if rate1 < rate2:
                        long_ex, short_ex = ex1, ex2
                    else:
                        long_ex, short_ex = ex2, ex1

                    opportunities.append({
                        'long_exchange': long_ex,
                        'short_exchange': short_ex,
                        'spread': spread,
                        'spread_annualized': spread * 3 * 365 * 100,
                        'expected_yield_8h': spread * 100,  # in %
                    })

        # Sort by spread
        opportunities.sort(key=lambda x: x['spread'], reverse=True)

        return {
            'opportunities': opportunities,
            'best_opportunity': opportunities[0] if opportunities else None
        }

    def _funding_sentiment(self, symbol: str) -> Dict:
        """Derive sentiment from funding rates"""

        current = self._current_rates(symbol)
        historical = self._historical_analysis(symbol)

        if not current.get('aggregate'):
            return {}

        current_rate = current['aggregate']['mean']

        # Historical context
        hist_30d = historical.get('30d', {})
        hist_mean = hist_30d.get('mean', 0)
        hist_std = hist_30d.get('std', 0.0001)

        # Z-score of current rate vs historical
        z_score = (current_rate - hist_mean) / hist_std if hist_std > 0 else 0

        # Sentiment interpretation
        if current_rate > 0.001:  # >0.1%
            sentiment = 'extremely_bullish'
            interpretation = 'Longs are heavily paying shorts - potential overheating'
        elif current_rate > 0.0003:  # >0.03%
            sentiment = 'bullish'
            interpretation = 'Longs paying shorts - market leaning bullish'
        elif current_rate > -0.0003:
            sentiment = 'neutral'
            interpretation = 'Balanced market'
        elif current_rate > -0.001:
            sentiment = 'bearish'
            interpretation = 'Shorts paying longs - market leaning bearish'
        else:
            sentiment = 'extremely_bearish'
            interpretation = 'Shorts heavily paying longs - potential capitulation'

        # Contrarian signal (extreme funding often precedes reversals)
        contrarian_signal = None
        if z_score > 2:
            contrarian_signal = 'bearish'
        elif z_score < -2:
            contrarian_signal = 'bullish'

        return {
            'current_rate': current_rate,
            'sentiment': sentiment,
            'interpretation': interpretation,
            'z_score': z_score,
            'contrarian_signal': contrarian_signal,
            'historical_percentile': self._calculate_percentile(symbol, current_rate)
        }

    def _calculate_percentile(self, symbol: str, rate: float) -> float:
        """Calculate percentile of current rate vs history"""

        all_rates = []
        for exchange_rates in self.history[symbol].values():
            all_rates.extend([float(r.rate) for r in exchange_rates])

        if not all_rates:
            return 50.0

        below = sum(1 for r in all_rates if r < rate)
        return (below / len(all_rates)) * 100
```

---

## 🔗 CONEXIONES NEURONALES

```yaml
conexiones_primarias:
  - neurona: "ON_CHAIN_ANALYTICS"
    tipo: "data_source"
    desc: "Datos on-chain complementan datos de mercado"

  - neurona: "ML_TRADING"
    tipo: "consumer"
    desc: "ML models consumen market data"

  - neurona: "TRADING_STRATEGIES"
    tipo: "consumer"
    desc: "Estrategias basadas en market data"

conexiones_secundarias:
  - neurona: "PORTFOLIO_ANALYTICS"
    tipo: "complementary"
    desc: "Análisis de portafolio usa precios"

  - neurona: "DEFI_RISKS"
    tipo: "monitor"
    desc: "Monitoreo de precios para riesgos"
```

---

## 📊 MÉTRICAS DE LA NEURONA

```yaml
metricas_salud:
  - nombre: "Data Freshness"
    valor: 99.5%
    umbral_alerta: 95%

  - nombre: "Source Coverage"
    valor: 8
    umbral_minimo: 5

  - nombre: "Price Accuracy"
    valor: 99.9%
    umbral_alerta: 99%

  - nombre: "Latency"
    valor: "<100ms"
    umbral_alerta: "500ms"
```

---

## 🔄 CHANGELOG

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0.0 | 2025-01-XX | Creación inicial - Price aggregation, order book analysis |
| 1.1.0 | 2025-01-XX | OHLCV management, trade flow analysis |
| 1.2.0 | 2025-01-XX | Funding rate analysis, WebSocket feeds |

---

> **CIPHER**: "El mercado habla en datos - quien escucha primero, gana primero."
