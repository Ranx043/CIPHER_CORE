# 🤖 NEURONA: MACHINE LEARNING TRADING
## CIPHER_CORE :: AI-Powered Trading Intelligence

> **Código Neuronal**: `C50003`
> **Dominio**: ML Models, Predictive Analytics, Algorithmic Trading
> **Estado**: `ACTIVA`
> **Última Evolución**: 2025-01-XX

---

## 🧬 IDENTIDAD DE LA NEURONA

```
╔══════════════════════════════════════════════════════════════╗
║  CIPHER ML TRADING - Artificial Intelligence for Alpha       ║
║  "Where human intuition meets machine precision"             ║
╠══════════════════════════════════════════════════════════════╣
║  Especialización: ML models, feature engineering, prediction ║
║  Conexiones: Market Data, Sentiment, Portfolio Management    ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🔧 FEATURE ENGINEERING

### Technical Feature Extraction

```python
"""
CIPHER Feature Engineering for ML Trading
Comprehensive feature extraction from market data
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import talib
from scipy import stats
from sklearn.preprocessing import StandardScaler, RobustScaler

class TechnicalFeatureExtractor:
    """
    Extract technical analysis features for ML models
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize with OHLCV DataFrame
        Expected columns: open, high, low, close, volume
        """
        self.df = df.copy()
        self.features = pd.DataFrame(index=df.index)

    def extract_all(self) -> pd.DataFrame:
        """Extract all features"""

        self._price_features()
        self._momentum_features()
        self._volatility_features()
        self._volume_features()
        self._pattern_features()
        self._statistical_features()
        self._cyclical_features()

        return self.features

    def _price_features(self):
        """Price-based features"""

        close = self.df['close']
        high = self.df['high']
        low = self.df['low']
        open_ = self.df['open']

        # Moving averages
        for period in [5, 10, 20, 50, 100, 200]:
            self.features[f'sma_{period}'] = talib.SMA(close, timeperiod=period)
            self.features[f'ema_{period}'] = talib.EMA(close, timeperiod=period)

            # Price relative to MA
            self.features[f'price_to_sma_{period}'] = close / self.features[f'sma_{period}']

        # Moving average crossovers
        self.features['sma_5_20_cross'] = (
            self.features['sma_5'] > self.features['sma_20']
        ).astype(int)
        self.features['sma_20_50_cross'] = (
            self.features['sma_20'] > self.features['sma_50']
        ).astype(int)
        self.features['golden_cross'] = (
            self.features['sma_50'] > self.features['sma_200']
        ).astype(int)

        # VWAP
        typical_price = (high + low + close) / 3
        cumulative_tp_vol = (typical_price * self.df['volume']).cumsum()
        cumulative_vol = self.df['volume'].cumsum()
        self.features['vwap'] = cumulative_tp_vol / cumulative_vol
        self.features['price_to_vwap'] = close / self.features['vwap']

        # Price changes
        for period in [1, 5, 10, 20]:
            self.features[f'return_{period}'] = close.pct_change(period)
            self.features[f'log_return_{period}'] = np.log(close / close.shift(period))

        # High-Low range
        self.features['hl_range'] = (high - low) / close
        self.features['hl_range_sma'] = self.features['hl_range'].rolling(20).mean()

        # Gaps
        self.features['gap'] = (open_ - close.shift(1)) / close.shift(1)

    def _momentum_features(self):
        """Momentum indicators"""

        close = self.df['close']
        high = self.df['high']
        low = self.df['low']

        # RSI
        for period in [7, 14, 21]:
            self.features[f'rsi_{period}'] = talib.RSI(close, timeperiod=period)

        # Stochastic
        slowk, slowd = talib.STOCH(
            high, low, close,
            fastk_period=14, slowk_period=3, slowd_period=3
        )
        self.features['stoch_k'] = slowk
        self.features['stoch_d'] = slowd
        self.features['stoch_cross'] = (slowk > slowd).astype(int)

        # MACD
        macd, macd_signal, macd_hist = talib.MACD(
            close, fastperiod=12, slowperiod=26, signalperiod=9
        )
        self.features['macd'] = macd
        self.features['macd_signal'] = macd_signal
        self.features['macd_hist'] = macd_hist
        self.features['macd_cross'] = (macd > macd_signal).astype(int)

        # Williams %R
        self.features['willr'] = talib.WILLR(high, low, close, timeperiod=14)

        # CCI
        self.features['cci'] = talib.CCI(high, low, close, timeperiod=20)

        # ROC
        for period in [10, 20]:
            self.features[f'roc_{period}'] = talib.ROC(close, timeperiod=period)

        # ADX (trend strength)
        self.features['adx'] = talib.ADX(high, low, close, timeperiod=14)
        self.features['plus_di'] = talib.PLUS_DI(high, low, close, timeperiod=14)
        self.features['minus_di'] = talib.MINUS_DI(high, low, close, timeperiod=14)

        # Aroon
        aroon_up, aroon_down = talib.AROON(high, low, timeperiod=25)
        self.features['aroon_up'] = aroon_up
        self.features['aroon_down'] = aroon_down
        self.features['aroon_osc'] = aroon_up - aroon_down

    def _volatility_features(self):
        """Volatility indicators"""

        close = self.df['close']
        high = self.df['high']
        low = self.df['low']

        # Bollinger Bands
        upper, middle, lower = talib.BBANDS(
            close, timeperiod=20, nbdevup=2, nbdevdn=2
        )
        self.features['bb_upper'] = upper
        self.features['bb_middle'] = middle
        self.features['bb_lower'] = lower
        self.features['bb_width'] = (upper - lower) / middle
        self.features['bb_position'] = (close - lower) / (upper - lower)

        # ATR
        for period in [7, 14, 21]:
            self.features[f'atr_{period}'] = talib.ATR(high, low, close, timeperiod=period)

        # ATR normalized
        self.features['atr_pct'] = self.features['atr_14'] / close * 100

        # Keltner Channels
        ema_20 = talib.EMA(close, timeperiod=20)
        atr_10 = talib.ATR(high, low, close, timeperiod=10)
        self.features['keltner_upper'] = ema_20 + 2 * atr_10
        self.features['keltner_lower'] = ema_20 - 2 * atr_10
        self.features['keltner_position'] = (
            (close - self.features['keltner_lower']) /
            (self.features['keltner_upper'] - self.features['keltner_lower'])
        )

        # Historical volatility
        for period in [10, 20, 30]:
            log_returns = np.log(close / close.shift(1))
            self.features[f'volatility_{period}'] = log_returns.rolling(period).std() * np.sqrt(252)

        # Volatility ratio
        self.features['vol_ratio'] = (
            self.features['volatility_10'] / self.features['volatility_30']
        )

        # Parkinson volatility (uses high-low)
        self.features['parkinson_vol'] = np.sqrt(
            (1 / (4 * np.log(2))) *
            (np.log(high / low) ** 2).rolling(20).mean()
        ) * np.sqrt(252)

    def _volume_features(self):
        """Volume-based features"""

        close = self.df['close']
        volume = self.df['volume']
        high = self.df['high']
        low = self.df['low']

        # Volume moving averages
        for period in [5, 10, 20, 50]:
            self.features[f'volume_sma_{period}'] = volume.rolling(period).mean()

        # Volume ratio
        self.features['volume_ratio'] = volume / self.features['volume_sma_20']

        # On-Balance Volume
        self.features['obv'] = talib.OBV(close, volume)
        self.features['obv_sma'] = self.features['obv'].rolling(20).mean()

        # Money Flow Index
        self.features['mfi'] = talib.MFI(high, low, close, volume, timeperiod=14)

        # Accumulation/Distribution
        self.features['ad'] = talib.AD(high, low, close, volume)
        self.features['ad_sma'] = self.features['ad'].rolling(20).mean()

        # Chaikin Money Flow
        clv = ((close - low) - (high - close)) / (high - low)
        clv = clv.fillna(0)
        self.features['cmf'] = (clv * volume).rolling(20).sum() / volume.rolling(20).sum()

        # VWAP deviation
        self.features['vwap_dev'] = (close - self.features['vwap']) / self.features['vwap']

        # Volume-price trend
        self.features['vpt'] = (volume * close.pct_change()).cumsum()

        # Force Index
        self.features['force_index'] = close.diff() * volume
        self.features['force_index_13'] = self.features['force_index'].ewm(span=13).mean()

    def _pattern_features(self):
        """Candlestick pattern recognition"""

        open_ = self.df['open']
        high = self.df['high']
        low = self.df['low']
        close = self.df['close']

        # Body characteristics
        self.features['body_size'] = abs(close - open_) / open_
        self.features['upper_shadow'] = (high - np.maximum(open_, close)) / close
        self.features['lower_shadow'] = (np.minimum(open_, close) - low) / close
        self.features['body_to_range'] = abs(close - open_) / (high - low + 0.0001)

        # Candlestick patterns (using TA-Lib)
        patterns = {
            'doji': talib.CDLDOJI,
            'hammer': talib.CDLHAMMER,
            'inverted_hammer': talib.CDLINVERTEDHAMMER,
            'engulfing': talib.CDLENGULFING,
            'morning_star': talib.CDLMORNINGSTAR,
            'evening_star': talib.CDLEVENINGSTAR,
            'three_white_soldiers': talib.CDL3WHITESOLDIERS,
            'three_black_crows': talib.CDL3BLACKCROWS,
            'harami': talib.CDLHARAMI,
            'piercing': talib.CDLPIERCING,
            'dark_cloud': talib.CDLDARKCLOUDCOVER,
            'spinning_top': talib.CDLSPINNINGTOP,
            'marubozu': talib.CDLMARUBOZU,
        }

        for name, func in patterns.items():
            self.features[f'pattern_{name}'] = func(open_, high, low, close) / 100

    def _statistical_features(self):
        """Statistical features"""

        close = self.df['close']
        returns = close.pct_change()

        # Skewness and Kurtosis
        for period in [20, 60]:
            self.features[f'skew_{period}'] = returns.rolling(period).skew()
            self.features[f'kurtosis_{period}'] = returns.rolling(period).kurt()

        # Z-score
        for period in [20, 50]:
            mean = close.rolling(period).mean()
            std = close.rolling(period).std()
            self.features[f'zscore_{period}'] = (close - mean) / std

        # Percentile rank
        def percentile_rank(x):
            return stats.percentileofscore(x.dropna(), x.iloc[-1]) / 100 if len(x.dropna()) > 0 else 0.5

        self.features['percentile_20'] = close.rolling(20).apply(percentile_rank)
        self.features['percentile_60'] = close.rolling(60).apply(percentile_rank)

        # Hurst exponent (trend persistence)
        def hurst(ts, max_lag=20):
            lags = range(2, min(max_lag, len(ts)))
            tau = [np.std(np.subtract(ts[lag:], ts[:-lag])) for lag in lags]
            reg = np.polyfit(np.log(lags), np.log(tau), 1)
            return reg[0]

        self.features['hurst'] = close.rolling(100).apply(
            lambda x: hurst(x.values) if len(x) >= 100 else 0.5
        )

    def _cyclical_features(self):
        """Time-based cyclical features"""

        # Extract datetime components if index is datetime
        if isinstance(self.df.index, pd.DatetimeIndex):
            # Hour of day (for intraday)
            if hasattr(self.df.index, 'hour'):
                self.features['hour_sin'] = np.sin(2 * np.pi * self.df.index.hour / 24)
                self.features['hour_cos'] = np.cos(2 * np.pi * self.df.index.hour / 24)

            # Day of week
            self.features['dow_sin'] = np.sin(2 * np.pi * self.df.index.dayofweek / 7)
            self.features['dow_cos'] = np.cos(2 * np.pi * self.df.index.dayofweek / 7)

            # Day of month
            self.features['dom_sin'] = np.sin(2 * np.pi * self.df.index.day / 31)
            self.features['dom_cos'] = np.cos(2 * np.pi * self.df.index.day / 31)

            # Month of year
            self.features['month_sin'] = np.sin(2 * np.pi * self.df.index.month / 12)
            self.features['month_cos'] = np.cos(2 * np.pi * self.df.index.month / 12)


class FeatureSelector:
    """
    Select most predictive features
    """

    def __init__(self, features: pd.DataFrame, target: pd.Series):
        self.features = features
        self.target = target

    def correlation_filter(self, threshold: float = 0.02) -> List[str]:
        """Filter features by correlation with target"""

        correlations = self.features.corrwith(self.target).abs()
        selected = correlations[correlations > threshold].index.tolist()

        return selected

    def mutual_information_filter(self, k: int = 50) -> List[str]:
        """Select top k features by mutual information"""
        from sklearn.feature_selection import mutual_info_regression

        # Remove NaN
        valid_idx = ~(self.features.isna().any(axis=1) | self.target.isna())
        X = self.features[valid_idx]
        y = self.target[valid_idx]

        mi_scores = mutual_info_regression(X, y)
        mi_df = pd.Series(mi_scores, index=X.columns).sort_values(ascending=False)

        return mi_df.head(k).index.tolist()

    def remove_multicollinearity(
        self,
        features: List[str],
        threshold: float = 0.95
    ) -> List[str]:
        """Remove highly correlated features"""

        df = self.features[features]
        corr_matrix = df.corr().abs()

        # Find pairs with high correlation
        upper = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )

        to_drop = [
            column for column in upper.columns
            if any(upper[column] > threshold)
        ]

        return [f for f in features if f not in to_drop]
```

---

## 🧠 ML MODELS FOR TRADING

### Price Direction Prediction

```python
"""
CIPHER ML Models for Trading
Classification and regression models for market prediction
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from sklearn.ensemble import (
    RandomForestClassifier, GradientBoostingClassifier,
    RandomForestRegressor, GradientBoostingRegressor
)
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, mean_squared_error, mean_absolute_error
)
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import lightgbm as lgb
from sklearn.neural_network import MLPClassifier, MLPRegressor
import joblib

@dataclass
class ModelResult:
    """Model training result"""
    model_name: str
    train_score: float
    test_score: float
    cv_scores: List[float]
    feature_importance: Dict[str, float]
    predictions: np.ndarray
    model: Any

class DirectionPredictor:
    """
    Predict price direction (up/down/neutral)
    """

    def __init__(
        self,
        features: pd.DataFrame,
        prices: pd.Series,
        prediction_horizon: int = 1,  # bars ahead
        threshold: float = 0.001  # 0.1% threshold for direction
    ):
        self.features = features
        self.prices = prices
        self.horizon = prediction_horizon
        self.threshold = threshold

        # Create target
        future_returns = prices.shift(-prediction_horizon) / prices - 1
        self.target = pd.Series(index=prices.index, dtype=int)
        self.target[future_returns > threshold] = 1  # Up
        self.target[future_returns < -threshold] = -1  # Down
        self.target[(future_returns >= -threshold) & (future_returns <= threshold)] = 0  # Neutral

        # Align data
        valid_idx = ~(features.isna().any(axis=1) | self.target.isna())
        self.X = features[valid_idx]
        self.y = self.target[valid_idx]

        # Scaler
        self.scaler = StandardScaler()

    def train_test_split(
        self,
        test_ratio: float = 0.2
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Time-series aware train/test split"""

        split_idx = int(len(self.X) * (1 - test_ratio))

        X_train = self.X.iloc[:split_idx]
        X_test = self.X.iloc[split_idx:]
        y_train = self.y.iloc[:split_idx]
        y_test = self.y.iloc[split_idx:]

        return X_train, X_test, y_train, y_test

    def train_models(self) -> Dict[str, ModelResult]:
        """Train multiple classification models"""

        X_train, X_test, y_train, y_test = self.train_test_split()

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        models = {
            'random_forest': RandomForestClassifier(
                n_estimators=100, max_depth=10, min_samples_split=20,
                random_state=42, n_jobs=-1
            ),
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=100, max_depth=5, learning_rate=0.1,
                random_state=42
            ),
            'xgboost': xgb.XGBClassifier(
                n_estimators=100, max_depth=5, learning_rate=0.1,
                random_state=42, use_label_encoder=False, eval_metric='mlogloss'
            ),
            'lightgbm': lgb.LGBMClassifier(
                n_estimators=100, max_depth=5, learning_rate=0.1,
                random_state=42, verbose=-1
            ),
            'mlp': MLPClassifier(
                hidden_layer_sizes=(100, 50), max_iter=500,
                early_stopping=True, random_state=42
            )
        }

        results = {}

        for name, model in models.items():
            print(f"Training {name}...")

            # Train
            if name == 'mlp':
                model.fit(X_train_scaled, y_train)
                train_pred = model.predict(X_train_scaled)
                test_pred = model.predict(X_test_scaled)
            else:
                model.fit(X_train, y_train)
                train_pred = model.predict(X_train)
                test_pred = model.predict(X_test)

            # Cross-validation
            tscv = TimeSeriesSplit(n_splits=5)
            if name == 'mlp':
                cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=tscv)
            else:
                cv_scores = cross_val_score(model, X_train, y_train, cv=tscv)

            # Feature importance
            if hasattr(model, 'feature_importances_'):
                importance = dict(zip(self.X.columns, model.feature_importances_))
            else:
                importance = {}

            results[name] = ModelResult(
                model_name=name,
                train_score=accuracy_score(y_train, train_pred),
                test_score=accuracy_score(y_test, test_pred),
                cv_scores=cv_scores.tolist(),
                feature_importance=importance,
                predictions=test_pred,
                model=model
            )

        return results

    def evaluate(self, results: Dict[str, ModelResult]) -> pd.DataFrame:
        """Detailed evaluation of all models"""

        _, X_test, _, y_test = self.train_test_split()

        metrics = []

        for name, result in results.items():
            pred = result.predictions

            metrics.append({
                'model': name,
                'accuracy': accuracy_score(y_test, pred),
                'precision_macro': precision_score(y_test, pred, average='macro', zero_division=0),
                'recall_macro': recall_score(y_test, pred, average='macro', zero_division=0),
                'f1_macro': f1_score(y_test, pred, average='macro', zero_division=0),
                'cv_mean': np.mean(result.cv_scores),
                'cv_std': np.std(result.cv_scores),
            })

        return pd.DataFrame(metrics).sort_values('f1_macro', ascending=False)


class ReturnPredictor:
    """
    Predict future returns (regression)
    """

    def __init__(
        self,
        features: pd.DataFrame,
        prices: pd.Series,
        prediction_horizon: int = 1
    ):
        self.features = features
        self.prices = prices
        self.horizon = prediction_horizon

        # Create target (future return)
        self.target = prices.shift(-prediction_horizon) / prices - 1

        # Align data
        valid_idx = ~(features.isna().any(axis=1) | self.target.isna())
        self.X = features[valid_idx]
        self.y = self.target[valid_idx]

        self.scaler = StandardScaler()

    def train_models(self) -> Dict[str, ModelResult]:
        """Train multiple regression models"""

        split_idx = int(len(self.X) * 0.8)

        X_train = self.X.iloc[:split_idx]
        X_test = self.X.iloc[split_idx:]
        y_train = self.y.iloc[:split_idx]
        y_test = self.y.iloc[split_idx:]

        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        models = {
            'random_forest': RandomForestRegressor(
                n_estimators=100, max_depth=10, random_state=42, n_jobs=-1
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42
            ),
            'xgboost': xgb.XGBRegressor(
                n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42
            ),
            'lightgbm': lgb.LGBMRegressor(
                n_estimators=100, max_depth=5, learning_rate=0.1,
                random_state=42, verbose=-1
            ),
        }

        results = {}

        for name, model in models.items():
            print(f"Training {name}...")

            model.fit(X_train, y_train)
            train_pred = model.predict(X_train)
            test_pred = model.predict(X_test)

            # Metrics
            train_mse = mean_squared_error(y_train, train_pred)
            test_mse = mean_squared_error(y_test, test_pred)

            # Direction accuracy (important for trading)
            direction_accuracy = np.mean(
                np.sign(test_pred) == np.sign(y_test)
            )

            if hasattr(model, 'feature_importances_'):
                importance = dict(zip(self.X.columns, model.feature_importances_))
            else:
                importance = {}

            results[name] = ModelResult(
                model_name=name,
                train_score=-train_mse,  # Negative because lower is better
                test_score=-test_mse,
                cv_scores=[direction_accuracy],  # Store direction accuracy
                feature_importance=importance,
                predictions=test_pred,
                model=model
            )

        return results
```

---

## 📈 STRATEGY BACKTESTING

### ML-Based Strategy Backtester

```python
"""
CIPHER ML Strategy Backtesting
Backtest ML-powered trading strategies
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Trade:
    """Individual trade record"""
    entry_time: datetime
    exit_time: datetime
    side: str  # 'long' or 'short'
    entry_price: float
    exit_price: float
    size: float
    pnl: float
    pnl_pct: float
    fees: float
    signal_confidence: float

@dataclass
class BacktestResult:
    """Backtest result summary"""
    total_return: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    total_trades: int
    avg_trade_pnl: float
    avg_win: float
    avg_loss: float
    largest_win: float
    largest_loss: float
    trades: List[Trade]
    equity_curve: pd.Series

class MLStrategyBacktester:
    """
    Backtest ML-powered trading strategies
    """

    def __init__(
        self,
        prices: pd.DataFrame,  # OHLCV data
        predictions: pd.Series,  # Model predictions
        initial_capital: float = 100000,
        commission: float = 0.001,  # 0.1%
        slippage: float = 0.0005  # 0.05%
    ):
        self.prices = prices
        self.predictions = predictions
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage

    def run(
        self,
        position_size: float = 0.1,  # 10% of capital per trade
        stop_loss: float = 0.02,  # 2% stop loss
        take_profit: float = 0.04,  # 4% take profit
        max_holding_period: int = 10,  # Max bars to hold
        confidence_threshold: float = 0.6  # Min prediction confidence
    ) -> BacktestResult:
        """Run backtest with given parameters"""

        capital = self.initial_capital
        position = 0
        entry_price = 0
        entry_time = None
        entry_confidence = 0
        bars_held = 0

        trades = []
        equity = [capital]
        equity_times = [self.prices.index[0]]

        for i in range(1, len(self.prices)):
            current_time = self.prices.index[i]
            current_price = self.prices['close'].iloc[i]
            high = self.prices['high'].iloc[i]
            low = self.prices['low'].iloc[i]

            prediction = self.predictions.iloc[i] if i < len(self.predictions) else 0

            # Check exit conditions for existing position
            if position != 0:
                bars_held += 1
                current_pnl_pct = (current_price - entry_price) / entry_price * position

                # Check stop loss / take profit using high/low
                if position == 1:  # Long
                    stop_hit = low <= entry_price * (1 - stop_loss)
                    tp_hit = high >= entry_price * (1 + take_profit)
                else:  # Short
                    stop_hit = high >= entry_price * (1 + stop_loss)
                    tp_hit = low <= entry_price * (1 - take_profit)

                exit_signal = (
                    stop_hit or
                    tp_hit or
                    bars_held >= max_holding_period or
                    (position == 1 and prediction == -1) or
                    (position == -1 and prediction == 1)
                )

                if exit_signal:
                    # Determine exit price
                    if stop_hit:
                        exit_price = entry_price * (1 - stop_loss * position)
                    elif tp_hit:
                        exit_price = entry_price * (1 + take_profit * position)
                    else:
                        exit_price = current_price

                    # Apply slippage
                    exit_price *= (1 - self.slippage * position)

                    # Calculate PnL
                    trade_size = capital * position_size
                    gross_pnl = (exit_price - entry_price) / entry_price * trade_size * position
                    fees = trade_size * self.commission * 2  # Entry + exit
                    net_pnl = gross_pnl - fees

                    capital += net_pnl

                    trades.append(Trade(
                        entry_time=entry_time,
                        exit_time=current_time,
                        side='long' if position == 1 else 'short',
                        entry_price=entry_price,
                        exit_price=exit_price,
                        size=trade_size,
                        pnl=net_pnl,
                        pnl_pct=net_pnl / trade_size,
                        fees=fees,
                        signal_confidence=entry_confidence
                    ))

                    position = 0
                    bars_held = 0

            # Check entry conditions
            if position == 0 and abs(prediction) >= confidence_threshold:
                # Apply slippage to entry
                if prediction > 0:  # Long
                    entry_price = current_price * (1 + self.slippage)
                    position = 1
                else:  # Short
                    entry_price = current_price * (1 - self.slippage)
                    position = -1

                entry_time = current_time
                entry_confidence = abs(prediction)
                bars_held = 0

            equity.append(capital)
            equity_times.append(current_time)

        # Calculate metrics
        equity_curve = pd.Series(equity, index=equity_times)

        return self._calculate_metrics(trades, equity_curve)

    def _calculate_metrics(
        self,
        trades: List[Trade],
        equity_curve: pd.Series
    ) -> BacktestResult:
        """Calculate performance metrics"""

        if not trades:
            return BacktestResult(
                total_return=0, sharpe_ratio=0, sortino_ratio=0,
                max_drawdown=0, win_rate=0, profit_factor=0,
                total_trades=0, avg_trade_pnl=0, avg_win=0, avg_loss=0,
                largest_win=0, largest_loss=0, trades=[], equity_curve=equity_curve
            )

        # Total return
        total_return = (equity_curve.iloc[-1] - self.initial_capital) / self.initial_capital

        # Returns series
        returns = equity_curve.pct_change().dropna()

        # Sharpe ratio (annualized)
        if len(returns) > 0 and returns.std() > 0:
            sharpe = np.sqrt(252) * returns.mean() / returns.std()
        else:
            sharpe = 0

        # Sortino ratio
        negative_returns = returns[returns < 0]
        if len(negative_returns) > 0:
            downside_std = negative_returns.std()
            sortino = np.sqrt(252) * returns.mean() / downside_std if downside_std > 0 else 0
        else:
            sortino = sharpe

        # Max drawdown
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = abs(drawdown.min())

        # Trade metrics
        pnls = [t.pnl for t in trades]
        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p < 0]

        win_rate = len(wins) / len(trades) if trades else 0
        profit_factor = sum(wins) / abs(sum(losses)) if losses else float('inf')

        return BacktestResult(
            total_return=total_return,
            sharpe_ratio=sharpe,
            sortino_ratio=sortino,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            profit_factor=profit_factor,
            total_trades=len(trades),
            avg_trade_pnl=np.mean(pnls) if pnls else 0,
            avg_win=np.mean(wins) if wins else 0,
            avg_loss=np.mean(losses) if losses else 0,
            largest_win=max(pnls) if pnls else 0,
            largest_loss=min(pnls) if pnls else 0,
            trades=trades,
            equity_curve=equity_curve
        )


class WalkForwardOptimizer:
    """
    Walk-forward optimization for ML strategies
    """

    def __init__(
        self,
        features: pd.DataFrame,
        prices: pd.DataFrame,
        model_class,
        model_params: Dict
    ):
        self.features = features
        self.prices = prices
        self.model_class = model_class
        self.model_params = model_params

    def optimize(
        self,
        train_periods: int = 252,  # 1 year
        test_periods: int = 63,  # 3 months
        step: int = 21  # 1 month
    ) -> Dict:
        """Walk-forward optimization"""

        results = []
        all_predictions = []

        start_idx = train_periods

        while start_idx + test_periods <= len(self.features):
            # Define train/test periods
            train_start = start_idx - train_periods
            train_end = start_idx
            test_end = start_idx + test_periods

            # Split data
            X_train = self.features.iloc[train_start:train_end]
            X_test = self.features.iloc[train_end:test_end]

            # Create target
            returns = self.prices['close'].pct_change()
            y_train = np.sign(returns.iloc[train_start:train_end].shift(-1)).fillna(0)

            # Train model
            model = self.model_class(**self.model_params)
            model.fit(X_train, y_train)

            # Predict
            predictions = model.predict(X_test)
            all_predictions.extend(zip(self.features.index[train_end:test_end], predictions))

            # Store period results
            results.append({
                'train_period': (self.features.index[train_start], self.features.index[train_end]),
                'test_period': (self.features.index[train_end], self.features.index[test_end]),
                'model': model
            })

            start_idx += step

        # Combine predictions
        pred_series = pd.Series(
            dict(all_predictions)
        ).sort_index()

        return {
            'predictions': pred_series,
            'period_results': results
        }
```

---

## 🔮 ENSEMBLE & ADVANCED METHODS

### Model Ensembling

```python
"""
CIPHER Ensemble Methods
Combine multiple models for robust predictions
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any
from sklearn.base import BaseEstimator, ClassifierMixin

class StackingEnsemble(BaseEstimator, ClassifierMixin):
    """
    Stacking ensemble of trading models
    """

    def __init__(
        self,
        base_models: List[Any],
        meta_model: Any,
        use_probabilities: bool = True
    ):
        self.base_models = base_models
        self.meta_model = meta_model
        self.use_probabilities = use_probabilities

    def fit(self, X, y):
        """Fit base models and meta model"""

        # Fit base models
        base_predictions = []

        for model in self.base_models:
            model.fit(X, y)

            if self.use_probabilities and hasattr(model, 'predict_proba'):
                preds = model.predict_proba(X)
            else:
                preds = model.predict(X).reshape(-1, 1)

            base_predictions.append(preds)

        # Create meta features
        meta_features = np.hstack(base_predictions)

        # Fit meta model
        self.meta_model.fit(meta_features, y)

        return self

    def predict(self, X):
        """Predict using ensemble"""

        base_predictions = []

        for model in self.base_models:
            if self.use_probabilities and hasattr(model, 'predict_proba'):
                preds = model.predict_proba(X)
            else:
                preds = model.predict(X).reshape(-1, 1)

            base_predictions.append(preds)

        meta_features = np.hstack(base_predictions)

        return self.meta_model.predict(meta_features)

    def predict_proba(self, X):
        """Predict probabilities"""

        base_predictions = []

        for model in self.base_models:
            if self.use_probabilities and hasattr(model, 'predict_proba'):
                preds = model.predict_proba(X)
            else:
                preds = model.predict(X).reshape(-1, 1)

            base_predictions.append(preds)

        meta_features = np.hstack(base_predictions)

        if hasattr(self.meta_model, 'predict_proba'):
            return self.meta_model.predict_proba(meta_features)
        else:
            return self.meta_model.predict(meta_features)


class WeightedVotingEnsemble:
    """
    Weighted voting ensemble with dynamic weight adjustment
    """

    def __init__(
        self,
        models: Dict[str, Any],
        initial_weights: Optional[Dict[str, float]] = None,
        performance_window: int = 100
    ):
        self.models = models
        self.weights = initial_weights or {name: 1.0 for name in models}
        self.performance_window = performance_window
        self.prediction_history: Dict[str, List] = {name: [] for name in models}
        self.actual_history: List = []

    def fit(self, X, y):
        """Fit all models"""

        for name, model in self.models.items():
            model.fit(X, y)

        return self

    def predict(self, X, y_actual=None):
        """Predict with weighted voting"""

        predictions = {}

        for name, model in self.models.items():
            pred = model.predict(X)
            predictions[name] = pred

            # Track for performance-based weighting
            if y_actual is not None:
                self.prediction_history[name].extend(pred)

        if y_actual is not None:
            self.actual_history.extend(y_actual)
            self._update_weights()

        # Weighted voting
        weighted_sum = np.zeros(len(X))

        for name, pred in predictions.items():
            weighted_sum += pred * self.weights[name]

        total_weight = sum(self.weights.values())

        return np.sign(weighted_sum / total_weight)

    def _update_weights(self):
        """Update weights based on recent performance"""

        if len(self.actual_history) < self.performance_window:
            return

        recent_actual = np.array(self.actual_history[-self.performance_window:])

        for name in self.models:
            recent_preds = np.array(self.prediction_history[name][-self.performance_window:])

            # Calculate accuracy
            accuracy = np.mean(recent_preds == recent_actual)

            # Update weight (higher accuracy = higher weight)
            self.weights[name] = max(0.1, accuracy ** 2)  # Square to emphasize differences

        # Normalize weights
        total = sum(self.weights.values())
        self.weights = {k: v / total for k, v in self.weights.items()}


class OnlineLearningModel:
    """
    Online learning model that updates with each new observation
    """

    def __init__(
        self,
        base_model: Any,
        learning_rate: float = 0.01,
        batch_size: int = 32,
        max_samples: int = 10000
    ):
        self.base_model = base_model
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.max_samples = max_samples

        self.X_buffer = []
        self.y_buffer = []
        self.is_fitted = False

    def partial_fit(self, X, y):
        """Update model with new data"""

        # Add to buffer
        if hasattr(X, 'values'):
            self.X_buffer.extend(X.values.tolist())
        else:
            self.X_buffer.extend(X.tolist())

        if hasattr(y, 'values'):
            self.y_buffer.extend(y.values.tolist())
        else:
            self.y_buffer.extend(y.tolist())

        # Trim buffer if too large
        if len(self.X_buffer) > self.max_samples:
            self.X_buffer = self.X_buffer[-self.max_samples:]
            self.y_buffer = self.y_buffer[-self.max_samples:]

        # Retrain if enough samples
        if len(self.X_buffer) >= self.batch_size:
            X_train = np.array(self.X_buffer)
            y_train = np.array(self.y_buffer)

            if hasattr(self.base_model, 'partial_fit'):
                self.base_model.partial_fit(X_train, y_train)
            else:
                self.base_model.fit(X_train, y_train)

            self.is_fitted = True

    def predict(self, X):
        """Make prediction"""

        if not self.is_fitted:
            raise ValueError("Model not fitted yet")

        return self.base_model.predict(X)
```

---

## 🔗 CONEXIONES NEURONALES

```yaml
conexiones_primarias:
  - neurona: "MARKET_DATA"
    tipo: "data_source"
    desc: "Fuente de datos de mercado para features"

  - neurona: "SENTIMENT_ANALYSIS"
    tipo: "feature_source"
    desc: "Features de sentimiento para modelos"

  - neurona: "TRADING_STRATEGIES"
    tipo: "integration"
    desc: "Estrategias ejecutan señales ML"

conexiones_secundarias:
  - neurona: "PORTFOLIO_ANALYTICS"
    tipo: "consumer"
    desc: "Portfolio optimization usa predicciones"

  - neurona: "DEFI_RISKS"
    tipo: "input"
    desc: "Risk features para modelos"
```

---

## 📊 MÉTRICAS DE LA NEURONA

```yaml
metricas_salud:
  - nombre: "Model Accuracy"
    valor: 55%+
    umbral_alerta: 50%

  - nombre: "Sharpe Ratio"
    valor: ">1.5"
    umbral_alerta: "1.0"

  - nombre: "Feature Count"
    valor: 150+
    umbral_minimo: 50

  - nombre: "Training Freshness"
    valor: "<24h"
    umbral_alerta: "48h"
```

---

## 🔄 CHANGELOG

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0.0 | 2025-01-XX | Creación inicial - Feature engineering, classifiers |
| 1.1.0 | 2025-01-XX | Backtesting framework, walk-forward optimization |
| 1.2.0 | 2025-01-XX | Ensemble methods, online learning |

---

> **CIPHER**: "El alpha está en los datos - el ML es solo el extractor."
