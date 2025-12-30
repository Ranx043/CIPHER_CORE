# 📈 NEURONA: TRADING STRATEGIES
## CIPHER_CORE :: Algorithmic Trading Intelligence

> **Código Neuronal**: `C70001`
> **Dominio**: Trading Strategies, Execution, Risk Management
> **Estado**: `ACTIVA`
> **Última Evolución**: 2025-01-XX

---

## 🧬 IDENTIDAD DE LA NEURONA

```
╔══════════════════════════════════════════════════════════════╗
║  CIPHER TRADING - Systematic Alpha Generation                ║
║  "The market is a device for transferring money to patient"  ║
╠══════════════════════════════════════════════════════════════╣
║  Especialización: Algorithmic trading, strategy execution    ║
║  Conexiones: Market Data, ML Trading, Portfolio Analytics    ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 📊 TREND FOLLOWING STRATEGIES

### Moving Average Systems

```python
"""
CIPHER Trend Following Strategies
Classic and advanced trend-following systems
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

class Signal(Enum):
    STRONG_BUY = 2
    BUY = 1
    NEUTRAL = 0
    SELL = -1
    STRONG_SELL = -2

@dataclass
class TradeSignal:
    """Trading signal output"""
    symbol: str
    signal: Signal
    confidence: float
    entry_price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    position_size: Optional[float] = None
    metadata: Dict = None

class BaseStrategy(ABC):
    """Base class for all strategies"""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generate_signal(self, df: pd.DataFrame) -> TradeSignal:
        pass


class MovingAverageCrossover(BaseStrategy):
    """
    Classic MA crossover strategy
    """

    def __init__(
        self,
        fast_period: int = 10,
        slow_period: int = 50,
        signal_period: int = 9
    ):
        super().__init__("MA_Crossover")
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

    def generate_signal(self, df: pd.DataFrame) -> TradeSignal:
        """Generate crossover signal"""

        close = df['close']

        # Calculate MAs
        fast_ma = close.rolling(self.fast_period).mean()
        slow_ma = close.rolling(self.slow_period).mean()

        # Current position
        current_fast = fast_ma.iloc[-1]
        current_slow = slow_ma.iloc[-1]
        prev_fast = fast_ma.iloc[-2]
        prev_slow = slow_ma.iloc[-2]

        # Determine signal
        if current_fast > current_slow and prev_fast <= prev_slow:
            # Golden cross
            signal = Signal.BUY
            confidence = (current_fast - current_slow) / current_slow
        elif current_fast < current_slow and prev_fast >= prev_slow:
            # Death cross
            signal = Signal.SELL
            confidence = (current_slow - current_fast) / current_fast
        elif current_fast > current_slow:
            signal = Signal.NEUTRAL  # Already in uptrend
            confidence = 0.3
        else:
            signal = Signal.NEUTRAL  # Already in downtrend
            confidence = 0.3

        # Calculate stops
        atr = self._calculate_atr(df)
        current_price = close.iloc[-1]

        if signal == Signal.BUY:
            stop_loss = current_price - 2 * atr
            take_profit = current_price + 3 * atr
        elif signal == Signal.SELL:
            stop_loss = current_price + 2 * atr
            take_profit = current_price - 3 * atr
        else:
            stop_loss = None
            take_profit = None

        return TradeSignal(
            symbol=df.name if hasattr(df, 'name') else 'UNKNOWN',
            signal=signal,
            confidence=min(confidence, 1.0),
            entry_price=current_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            metadata={
                'fast_ma': current_fast,
                'slow_ma': current_slow,
                'atr': atr
            }
        )

    def _calculate_atr(self, df: pd.DataFrame, period: int = 14) -> float:
        """Calculate Average True Range"""

        high = df['high']
        low = df['low']
        close = df['close']

        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(period).mean()

        return atr.iloc[-1]


class TripleScreenTrading(BaseStrategy):
    """
    Elder's Triple Screen Trading System
    Uses multiple timeframes for confirmation
    """

    def __init__(self):
        super().__init__("Triple_Screen")

    def generate_signal(
        self,
        df_weekly: pd.DataFrame,
        df_daily: pd.DataFrame,
        df_hourly: pd.DataFrame
    ) -> TradeSignal:
        """
        Screen 1 (Weekly): Trend direction using MACD histogram
        Screen 2 (Daily): Counter-trend entry using Force Index
        Screen 3 (Hourly): Entry timing using trailing stops
        """

        # Screen 1: Weekly trend
        weekly_trend = self._screen1_trend(df_weekly)

        # Screen 2: Daily oscillator
        daily_signal = self._screen2_oscillator(df_daily)

        # Screen 3: Entry timing
        entry = self._screen3_entry(df_hourly)

        # Combine screens
        if weekly_trend == 1 and daily_signal == 1:
            signal = Signal.BUY
            confidence = 0.8
        elif weekly_trend == -1 and daily_signal == -1:
            signal = Signal.SELL
            confidence = 0.8
        else:
            signal = Signal.NEUTRAL
            confidence = 0.3

        current_price = df_hourly['close'].iloc[-1]

        return TradeSignal(
            symbol='',
            signal=signal,
            confidence=confidence,
            entry_price=current_price if entry else None,
            metadata={
                'weekly_trend': weekly_trend,
                'daily_signal': daily_signal,
                'entry_ready': entry
            }
        )

    def _screen1_trend(self, df: pd.DataFrame) -> int:
        """Screen 1: Weekly MACD histogram for trend"""

        close = df['close']

        ema12 = close.ewm(span=12).mean()
        ema26 = close.ewm(span=26).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9).mean()
        histogram = macd - signal

        # Trend is direction of histogram slope
        if histogram.iloc[-1] > histogram.iloc[-2]:
            return 1  # Uptrend
        else:
            return -1  # Downtrend

    def _screen2_oscillator(self, df: pd.DataFrame) -> int:
        """Screen 2: Daily Force Index for pullback entry"""

        close = df['close']
        volume = df['volume']

        # Force Index = (Close - Previous Close) * Volume
        force_index = (close - close.shift(1)) * volume
        force_index_ema = force_index.ewm(span=13).mean()

        # Look for pullback in direction of trend
        if force_index_ema.iloc[-1] < 0 < force_index_ema.iloc[-2]:
            return 1  # Buy signal (pullback in uptrend)
        elif force_index_ema.iloc[-1] > 0 > force_index_ema.iloc[-2]:
            return -1  # Sell signal (rally in downtrend)
        else:
            return 0

    def _screen3_entry(self, df: pd.DataFrame) -> bool:
        """Screen 3: Hourly trailing stop for entry"""

        high = df['high']
        low = df['low']

        # Use 2-period high/low as trailing stop
        trailing_buy_stop = high.rolling(2).max().iloc[-2]
        trailing_sell_stop = low.rolling(2).min().iloc[-2]

        current_close = df['close'].iloc[-1]

        # Entry when price breaks trailing stop
        return (
            current_close > trailing_buy_stop or
            current_close < trailing_sell_stop
        )


class TurtleTrading(BaseStrategy):
    """
    Turtle Trading System
    Famous trend-following breakout system
    """

    def __init__(
        self,
        entry_period: int = 20,
        exit_period: int = 10,
        atr_period: int = 20
    ):
        super().__init__("Turtle")
        self.entry_period = entry_period
        self.exit_period = exit_period
        self.atr_period = atr_period

    def generate_signal(self, df: pd.DataFrame) -> TradeSignal:
        """Generate Turtle trading signal"""

        high = df['high']
        low = df['low']
        close = df['close']

        # Entry breakout levels
        entry_high = high.rolling(self.entry_period).max()
        entry_low = low.rolling(self.entry_period).min()

        # Exit breakout levels
        exit_high = high.rolling(self.exit_period).max()
        exit_low = low.rolling(self.exit_period).min()

        # ATR for position sizing
        atr = self._calculate_atr(df, self.atr_period)

        current_close = close.iloc[-1]
        prev_entry_high = entry_high.iloc[-2]
        prev_entry_low = entry_low.iloc[-2]

        # Determine signal
        if current_close > prev_entry_high:
            signal = Signal.BUY
            stop_loss = current_close - 2 * atr
        elif current_close < prev_entry_low:
            signal = Signal.SELL
            stop_loss = current_close + 2 * atr
        else:
            signal = Signal.NEUTRAL
            stop_loss = None

        return TradeSignal(
            symbol='',
            signal=signal,
            confidence=0.7 if signal != Signal.NEUTRAL else 0.3,
            entry_price=current_close,
            stop_loss=stop_loss,
            metadata={
                'entry_high': prev_entry_high,
                'entry_low': prev_entry_low,
                'atr': atr,
                'unit_size': self._calculate_unit_size(100000, atr, current_close)
            }
        )

    def _calculate_atr(self, df: pd.DataFrame, period: int) -> float:
        """Calculate ATR"""

        high = df['high']
        low = df['low']
        close = df['close']

        tr = pd.concat([
            high - low,
            abs(high - close.shift(1)),
            abs(low - close.shift(1))
        ], axis=1).max(axis=1)

        return tr.rolling(period).mean().iloc[-1]

    def _calculate_unit_size(
        self,
        account_size: float,
        atr: float,
        price: float,
        risk_per_unit: float = 0.01  # 1% risk per unit
    ) -> float:
        """Calculate position size (Turtle unit)"""

        dollar_volatility = atr * price
        unit_size = (account_size * risk_per_unit) / dollar_volatility

        return unit_size
```

---

## 📉 MEAN REVERSION STRATEGIES

### Statistical Arbitrage

```python
"""
CIPHER Mean Reversion Strategies
Statistical arbitrage and mean reversion systems
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from scipy import stats
from statsmodels.tsa.stattools import coint, adfuller

class BollingerBandsMeanReversion(BaseStrategy):
    """
    Bollinger Bands mean reversion strategy
    """

    def __init__(
        self,
        period: int = 20,
        std_dev: float = 2.0,
        rsi_period: int = 14
    ):
        super().__init__("BB_MeanReversion")
        self.period = period
        self.std_dev = std_dev
        self.rsi_period = rsi_period

    def generate_signal(self, df: pd.DataFrame) -> TradeSignal:
        """Generate mean reversion signal"""

        close = df['close']

        # Bollinger Bands
        sma = close.rolling(self.period).mean()
        std = close.rolling(self.period).std()
        upper_band = sma + self.std_dev * std
        lower_band = sma - self.std_dev * std

        # RSI for confirmation
        rsi = self._calculate_rsi(close, self.rsi_period)

        current_close = close.iloc[-1]
        current_upper = upper_band.iloc[-1]
        current_lower = lower_band.iloc[-1]
        current_sma = sma.iloc[-1]
        current_rsi = rsi.iloc[-1]

        # Percent B (position within bands)
        percent_b = (current_close - current_lower) / (current_upper - current_lower)

        # Mean reversion signals
        if current_close < current_lower and current_rsi < 30:
            signal = Signal.STRONG_BUY
            confidence = min((current_lower - current_close) / current_lower + 0.5, 1.0)
            stop_loss = current_close * 0.95  # 5% below
            take_profit = current_sma  # Target middle band
        elif current_close > current_upper and current_rsi > 70:
            signal = Signal.STRONG_SELL
            confidence = min((current_close - current_upper) / current_upper + 0.5, 1.0)
            stop_loss = current_close * 1.05  # 5% above
            take_profit = current_sma
        elif percent_b < 0.2:
            signal = Signal.BUY
            confidence = 0.6
            stop_loss = current_lower * 0.98
            take_profit = current_sma
        elif percent_b > 0.8:
            signal = Signal.SELL
            confidence = 0.6
            stop_loss = current_upper * 1.02
            take_profit = current_sma
        else:
            signal = Signal.NEUTRAL
            confidence = 0.3
            stop_loss = None
            take_profit = None

        return TradeSignal(
            symbol='',
            signal=signal,
            confidence=confidence,
            entry_price=current_close,
            stop_loss=stop_loss,
            take_profit=take_profit,
            metadata={
                'upper_band': current_upper,
                'lower_band': current_lower,
                'sma': current_sma,
                'percent_b': percent_b,
                'rsi': current_rsi
            }
        )

    def _calculate_rsi(self, close: pd.Series, period: int) -> pd.Series:
        """Calculate RSI"""

        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi


class PairsTrading(BaseStrategy):
    """
    Statistical arbitrage pairs trading
    """

    def __init__(
        self,
        lookback: int = 60,
        entry_zscore: float = 2.0,
        exit_zscore: float = 0.5
    ):
        super().__init__("Pairs_Trading")
        self.lookback = lookback
        self.entry_zscore = entry_zscore
        self.exit_zscore = exit_zscore

    def find_cointegrated_pairs(
        self,
        price_data: pd.DataFrame,
        significance: float = 0.05
    ) -> List[Tuple[str, str, float]]:
        """Find cointegrated pairs"""

        symbols = price_data.columns
        n = len(symbols)
        pairs = []

        for i in range(n):
            for j in range(i + 1, n):
                s1 = price_data[symbols[i]]
                s2 = price_data[symbols[j]]

                # Cointegration test
                result = coint(s1, s2)
                p_value = result[1]

                if p_value < significance:
                    # Calculate hedge ratio
                    hedge_ratio = self._calculate_hedge_ratio(s1, s2)

                    pairs.append((
                        symbols[i],
                        symbols[j],
                        p_value,
                        hedge_ratio
                    ))

        return sorted(pairs, key=lambda x: x[2])  # Sort by p-value

    def _calculate_hedge_ratio(
        self,
        s1: pd.Series,
        s2: pd.Series
    ) -> float:
        """Calculate hedge ratio using OLS"""

        from sklearn.linear_model import LinearRegression

        model = LinearRegression()
        model.fit(s2.values.reshape(-1, 1), s1.values)

        return model.coef_[0]

    def generate_signal(
        self,
        s1: pd.Series,
        s2: pd.Series,
        hedge_ratio: float
    ) -> TradeSignal:
        """Generate pairs trading signal"""

        # Calculate spread
        spread = s1 - hedge_ratio * s2

        # Calculate z-score
        spread_mean = spread.rolling(self.lookback).mean()
        spread_std = spread.rolling(self.lookback).std()
        zscore = (spread - spread_mean) / spread_std

        current_zscore = zscore.iloc[-1]

        # Generate signal
        if current_zscore > self.entry_zscore:
            # Spread is high - short s1, long s2
            signal = Signal.SELL
            confidence = min(current_zscore / 3, 1.0)
        elif current_zscore < -self.entry_zscore:
            # Spread is low - long s1, short s2
            signal = Signal.BUY
            confidence = min(abs(current_zscore) / 3, 1.0)
        elif abs(current_zscore) < self.exit_zscore:
            # Close position
            signal = Signal.NEUTRAL
            confidence = 0.5
        else:
            signal = Signal.NEUTRAL
            confidence = 0.3

        return TradeSignal(
            symbol=f"{s1.name}/{s2.name}",
            signal=signal,
            confidence=confidence,
            metadata={
                'zscore': current_zscore,
                'spread': spread.iloc[-1],
                'hedge_ratio': hedge_ratio,
                's1_price': s1.iloc[-1],
                's2_price': s2.iloc[-1]
            }
        )


class GridTrading(BaseStrategy):
    """
    Grid trading strategy for ranging markets
    """

    def __init__(
        self,
        grid_levels: int = 10,
        grid_spacing_pct: float = 0.02,  # 2% between levels
        capital_per_grid: float = 0.1  # 10% of capital per grid
    ):
        super().__init__("Grid_Trading")
        self.grid_levels = grid_levels
        self.grid_spacing_pct = grid_spacing_pct
        self.capital_per_grid = capital_per_grid

    def setup_grid(
        self,
        current_price: float,
        capital: float
    ) -> Dict:
        """Set up grid levels"""

        # Calculate grid boundaries
        half_levels = self.grid_levels // 2

        levels = []
        for i in range(-half_levels, half_levels + 1):
            price = current_price * (1 + i * self.grid_spacing_pct)
            position_size = capital * self.capital_per_grid / price

            levels.append({
                'level': i,
                'price': price,
                'position_size': position_size,
                'order_type': 'buy' if i < 0 else 'sell',
                'filled': False
            })

        return {
            'base_price': current_price,
            'levels': levels,
            'capital': capital,
            'total_position': 0
        }

    def update_grid(
        self,
        grid: Dict,
        current_price: float
    ) -> List[Dict]:
        """Update grid and return orders to execute"""

        orders_to_execute = []

        for level in grid['levels']:
            if level['filled']:
                continue

            if level['order_type'] == 'buy' and current_price <= level['price']:
                orders_to_execute.append({
                    'type': 'buy',
                    'price': level['price'],
                    'size': level['position_size'],
                    'level': level['level']
                })
                level['filled'] = True
                grid['total_position'] += level['position_size']

            elif level['order_type'] == 'sell' and current_price >= level['price']:
                orders_to_execute.append({
                    'type': 'sell',
                    'price': level['price'],
                    'size': level['position_size'],
                    'level': level['level']
                })
                level['filled'] = True
                grid['total_position'] -= level['position_size']

        return orders_to_execute

    def generate_signal(self, df: pd.DataFrame) -> TradeSignal:
        """Generate grid trading signal based on range detection"""

        close = df['close']

        # Detect if market is ranging
        atr = self._calculate_atr(df)
        volatility = close.rolling(20).std() / close.rolling(20).mean()

        # ADX for trend strength
        adx = self._calculate_adx(df)

        current_close = close.iloc[-1]
        current_adx = adx.iloc[-1] if not pd.isna(adx.iloc[-1]) else 25

        # Grid trading works best in low ADX (ranging) markets
        if current_adx < 20:
            signal = Signal.BUY  # Start grid
            confidence = 0.8
            recommendation = "Deploy grid - ranging market detected"
        elif current_adx > 40:
            signal = Signal.NEUTRAL  # Don't grid in trending market
            confidence = 0.3
            recommendation = "Avoid grid - strong trend detected"
        else:
            signal = Signal.NEUTRAL
            confidence = 0.5
            recommendation = "Uncertain market conditions"

        return TradeSignal(
            symbol='',
            signal=signal,
            confidence=confidence,
            entry_price=current_close,
            metadata={
                'adx': current_adx,
                'volatility': volatility.iloc[-1] * 100,
                'recommendation': recommendation,
                'grid_setup': self.setup_grid(current_close, 100000) if signal == Signal.BUY else None
            }
        )

    def _calculate_atr(self, df: pd.DataFrame, period: int = 14) -> float:
        """Calculate ATR"""
        high = df['high']
        low = df['low']
        close = df['close']

        tr = pd.concat([
            high - low,
            abs(high - close.shift(1)),
            abs(low - close.shift(1))
        ], axis=1).max(axis=1)

        return tr.rolling(period).mean().iloc[-1]

    def _calculate_adx(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate ADX"""
        high = df['high']
        low = df['low']
        close = df['close']

        # +DM and -DM
        plus_dm = high.diff()
        minus_dm = -low.diff()
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm < 0] = 0

        # True Range
        tr = pd.concat([
            high - low,
            abs(high - close.shift(1)),
            abs(low - close.shift(1))
        ], axis=1).max(axis=1)

        # Smoothed values
        atr = tr.ewm(span=period).mean()
        plus_di = 100 * (plus_dm.ewm(span=period).mean() / atr)
        minus_di = 100 * (minus_dm.ewm(span=period).mean() / atr)

        # DX and ADX
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.ewm(span=period).mean()

        return adx
```

---

## ⚡ DeFi SPECIFIC STRATEGIES

### DEX Arbitrage & Yield Optimization

```python
"""
CIPHER DeFi Trading Strategies
DEX arbitrage, yield farming optimization
"""

from typing import Dict, List, Optional, Tuple
from decimal import Decimal
import asyncio

class DEXArbitrage(BaseStrategy):
    """
    Cross-DEX arbitrage strategy
    """

    def __init__(
        self,
        min_profit_bps: int = 30,  # 0.30% minimum profit
        gas_estimate: int = 300000,
        max_slippage_bps: int = 50
    ):
        super().__init__("DEX_Arbitrage")
        self.min_profit_bps = min_profit_bps
        self.gas_estimate = gas_estimate
        self.max_slippage_bps = max_slippage_bps

    def find_arbitrage(
        self,
        token_pair: Tuple[str, str],
        dex_prices: Dict[str, Dict],
        gas_price_gwei: float,
        eth_price: float
    ) -> Optional[Dict]:
        """
        Find arbitrage opportunity across DEXes

        dex_prices format:
        {
            'uniswap': {'price': 1.0, 'liquidity': 1000000, 'fee': 0.003},
            'sushiswap': {'price': 1.02, 'liquidity': 500000, 'fee': 0.003},
        }
        """

        if len(dex_prices) < 2:
            return None

        # Find best buy and sell prices
        buy_dex = min(dex_prices.items(), key=lambda x: x[1]['price'])
        sell_dex = max(dex_prices.items(), key=lambda x: x[1]['price'])

        buy_price = buy_dex[1]['price']
        sell_price = sell_dex[1]['price']

        # Calculate spread
        spread_bps = (sell_price - buy_price) / buy_price * 10000

        # Calculate gas cost
        gas_cost_eth = self.gas_estimate * gas_price_gwei / 1e9
        gas_cost_usd = gas_cost_eth * eth_price

        # Calculate fees
        buy_fee_bps = buy_dex[1]['fee'] * 10000
        sell_fee_bps = sell_dex[1]['fee'] * 10000
        total_fee_bps = buy_fee_bps + sell_fee_bps

        # Net profit in bps (before gas)
        net_spread_bps = spread_bps - total_fee_bps - self.max_slippage_bps

        if net_spread_bps < self.min_profit_bps:
            return None

        # Calculate optimal trade size
        min_liquidity = min(buy_dex[1]['liquidity'], sell_dex[1]['liquidity'])
        optimal_size = min_liquidity * 0.1  # 10% of smaller pool

        # Calculate profit
        gross_profit = optimal_size * net_spread_bps / 10000
        net_profit = gross_profit - gas_cost_usd

        if net_profit <= 0:
            return None

        return {
            'token_pair': token_pair,
            'buy_dex': buy_dex[0],
            'sell_dex': sell_dex[0],
            'buy_price': buy_price,
            'sell_price': sell_price,
            'spread_bps': spread_bps,
            'net_spread_bps': net_spread_bps,
            'optimal_size_usd': optimal_size,
            'estimated_profit_usd': net_profit,
            'profit_margin_pct': net_profit / optimal_size * 100,
            'gas_cost_usd': gas_cost_usd
        }

    def generate_signal(self, df: pd.DataFrame) -> TradeSignal:
        # This strategy generates signals differently - via find_arbitrage
        pass


class FlashLoanArbitrage:
    """
    Flash loan powered arbitrage
    """

    def __init__(self, min_profit_eth: float = 0.1):
        self.min_profit_eth = min_profit_eth

    def calculate_triangular_arb(
        self,
        pool_a: Dict,  # A -> B
        pool_b: Dict,  # B -> C
        pool_c: Dict,  # C -> A
        loan_amount: float
    ) -> Optional[Dict]:
        """
        Calculate triangular arbitrage opportunity

        Flow: Borrow A -> Swap A->B -> Swap B->C -> Swap C->A -> Repay A + profit
        """

        # Step 1: A -> B
        amount_b = self._get_amount_out(
            loan_amount,
            pool_a['reserve_a'],
            pool_a['reserve_b'],
            pool_a['fee']
        )

        # Step 2: B -> C
        amount_c = self._get_amount_out(
            amount_b,
            pool_b['reserve_b'],
            pool_b['reserve_c'],
            pool_b['fee']
        )

        # Step 3: C -> A
        amount_a_out = self._get_amount_out(
            amount_c,
            pool_c['reserve_c'],
            pool_c['reserve_a'],
            pool_c['fee']
        )

        # Flash loan fee (usually 0.09% on Aave)
        flash_loan_fee = loan_amount * 0.0009
        amount_to_repay = loan_amount + flash_loan_fee

        profit = amount_a_out - amount_to_repay

        if profit < self.min_profit_eth:
            return None

        return {
            'loan_amount': loan_amount,
            'token_a_out': amount_a_out,
            'amount_to_repay': amount_to_repay,
            'profit': profit,
            'profit_pct': profit / loan_amount * 100,
            'path': ['A', 'B', 'C', 'A'],
            'amounts': [loan_amount, amount_b, amount_c, amount_a_out]
        }

    def _get_amount_out(
        self,
        amount_in: float,
        reserve_in: float,
        reserve_out: float,
        fee: float = 0.003
    ) -> float:
        """Calculate output amount using constant product formula"""

        amount_in_with_fee = amount_in * (1 - fee)
        numerator = amount_in_with_fee * reserve_out
        denominator = reserve_in + amount_in_with_fee

        return numerator / denominator

    def optimize_loan_amount(
        self,
        pool_a: Dict,
        pool_b: Dict,
        pool_c: Dict,
        max_loan: float = 1000
    ) -> Tuple[float, float]:
        """Find optimal loan amount for maximum profit"""

        best_profit = 0
        best_amount = 0

        # Binary search for optimal amount
        amounts = np.linspace(0.1, max_loan, 100)

        for amount in amounts:
            result = self.calculate_triangular_arb(pool_a, pool_b, pool_c, amount)
            if result and result['profit'] > best_profit:
                best_profit = result['profit']
                best_amount = amount

        return best_amount, best_profit


class LiquidationBot:
    """
    DeFi liquidation strategy
    """

    def __init__(
        self,
        min_profit_usd: float = 50,
        gas_buffer: float = 1.5  # 50% gas buffer
    ):
        self.min_profit_usd = min_profit_usd
        self.gas_buffer = gas_buffer

    def find_liquidatable_positions(
        self,
        positions: List[Dict],
        prices: Dict[str, float]
    ) -> List[Dict]:
        """
        Find positions eligible for liquidation

        position format:
        {
            'user': '0x...',
            'collateral_token': 'ETH',
            'collateral_amount': 10.0,
            'debt_token': 'USDC',
            'debt_amount': 15000,
            'liquidation_threshold': 0.825,  # 82.5%
            'liquidation_bonus': 0.05  # 5%
        }
        """

        liquidatable = []

        for pos in positions:
            collateral_value = (
                pos['collateral_amount'] *
                prices[pos['collateral_token']]
            )
            debt_value = (
                pos['debt_amount'] *
                prices.get(pos['debt_token'], 1.0)  # Stablecoins = 1
            )

            # Health factor = (collateral * liquidation_threshold) / debt
            health_factor = (
                collateral_value * pos['liquidation_threshold']
            ) / debt_value if debt_value > 0 else float('inf')

            if health_factor < 1.0:
                # Position is liquidatable
                # Calculate max liquidation (usually 50% of debt)
                max_liquidation = debt_value * 0.5

                # Calculate profit (liquidation bonus)
                liquidation_bonus_usd = max_liquidation * pos['liquidation_bonus']

                liquidatable.append({
                    'user': pos['user'],
                    'health_factor': health_factor,
                    'collateral_value': collateral_value,
                    'debt_value': debt_value,
                    'max_liquidation_usd': max_liquidation,
                    'estimated_profit_usd': liquidation_bonus_usd,
                    'collateral_token': pos['collateral_token'],
                    'debt_token': pos['debt_token'],
                    'priority': liquidation_bonus_usd  # Higher profit = higher priority
                })

        # Sort by profit potential
        return sorted(liquidatable, key=lambda x: x['priority'], reverse=True)

    def calculate_liquidation_profit(
        self,
        position: Dict,
        gas_price_gwei: float,
        eth_price: float
    ) -> Dict:
        """Calculate net profit after gas"""

        # Estimate gas for liquidation (varies by protocol)
        gas_estimate = 500000  # Conservative estimate
        gas_cost_eth = gas_estimate * gas_price_gwei / 1e9 * self.gas_buffer
        gas_cost_usd = gas_cost_eth * eth_price

        net_profit = position['estimated_profit_usd'] - gas_cost_usd

        return {
            'gross_profit': position['estimated_profit_usd'],
            'gas_cost_usd': gas_cost_usd,
            'net_profit': net_profit,
            'profitable': net_profit > self.min_profit_usd,
            'roi_pct': net_profit / position['max_liquidation_usd'] * 100 if position['max_liquidation_usd'] > 0 else 0
        }
```

---

## 🔗 CONEXIONES NEURONALES

```yaml
conexiones_primarias:
  - neurona: "MARKET_DATA"
    tipo: "data_source"
    desc: "Datos de mercado en tiempo real"

  - neurona: "ML_TRADING"
    tipo: "signal_enhancement"
    desc: "ML mejora señales de estrategias"

  - neurona: "PORTFOLIO_ANALYTICS"
    tipo: "integration"
    desc: "Portfolio management de posiciones"

conexiones_secundarias:
  - neurona: "DEFI_PROTOCOLS"
    tipo: "execution"
    desc: "Ejecución en protocolos DeFi"

  - neurona: "SMART_CONTRACT_SECURITY"
    tipo: "risk_assessment"
    desc: "Análisis de riesgo de contratos"
```

---

## 📊 MÉTRICAS DE LA NEURONA

```yaml
metricas_salud:
  - nombre: "Strategy Win Rate"
    valor: 55%+
    umbral_alerta: 45%

  - nombre: "Sharpe Ratio"
    valor: ">1.5"
    umbral_alerta: "1.0"

  - nombre: "Max Drawdown"
    valor: "<20%"
    umbral_alerta: "25%"

  - nombre: "Profit Factor"
    valor: ">1.5"
    umbral_alerta: "1.2"
```

---

## 🔄 CHANGELOG

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0.0 | 2025-01-XX | Creación inicial - Trend following, mean reversion |
| 1.1.0 | 2025-01-XX | Grid trading, pairs trading |
| 1.2.0 | 2025-01-XX | DeFi strategies - arbitrage, liquidations |

---

> **CIPHER**: "El mercado paga por la paciencia y castiga la impaciencia."
