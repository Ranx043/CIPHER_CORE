# 📈 NEURONA: PORTFOLIO ANALYTICS
## CIPHER_CORE :: Portfolio Intelligence & Risk Management

> **Código Neuronal**: `C50005`
> **Dominio**: Portfolio Analysis, Risk Metrics, Optimization
> **Estado**: `ACTIVA`
> **Última Evolución**: 2025-01-XX

---

## 🧬 IDENTIDAD DE LA NEURONA

```
╔══════════════════════════════════════════════════════════════╗
║  CIPHER PORTFOLIO - Intelligence-Driven Wealth Management    ║
║  "Diversification is protection against ignorance"           ║
╠══════════════════════════════════════════════════════════════╣
║  Especialización: Portfolio construction, risk, optimization ║
║  Conexiones: Market Data, ML Trading, DeFi Protocols         ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 📊 PORTFOLIO ANALYSIS

### Core Portfolio Analytics

```python
"""
CIPHER Portfolio Analytics
Comprehensive portfolio analysis and metrics
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from scipy import stats
from scipy.optimize import minimize

@dataclass
class Position:
    """Portfolio position"""
    symbol: str
    quantity: float
    avg_cost: float
    current_price: float
    sector: str = 'crypto'
    chain: str = 'ethereum'

    @property
    def market_value(self) -> float:
        return self.quantity * self.current_price

    @property
    def cost_basis(self) -> float:
        return self.quantity * self.avg_cost

    @property
    def unrealized_pnl(self) -> float:
        return self.market_value - self.cost_basis

    @property
    def unrealized_pnl_pct(self) -> float:
        return (self.current_price - self.avg_cost) / self.avg_cost * 100

@dataclass
class Portfolio:
    """Complete portfolio"""
    positions: List[Position]
    cash: float = 0.0
    stablecoins: float = 0.0

    @property
    def total_value(self) -> float:
        return sum(p.market_value for p in self.positions) + self.cash + self.stablecoins

    @property
    def total_cost(self) -> float:
        return sum(p.cost_basis for p in self.positions) + self.cash + self.stablecoins

    @property
    def total_pnl(self) -> float:
        return self.total_value - self.total_cost

    @property
    def total_pnl_pct(self) -> float:
        return self.total_pnl / self.total_cost * 100 if self.total_cost > 0 else 0


class PortfolioAnalyzer:
    """
    Comprehensive portfolio analysis
    """

    def __init__(
        self,
        portfolio: Portfolio,
        price_history: pd.DataFrame,  # Columns = symbols, Index = dates
        risk_free_rate: float = 0.04  # 4% annual
    ):
        self.portfolio = portfolio
        self.price_history = price_history
        self.risk_free_rate = risk_free_rate

        # Calculate returns
        self.returns = price_history.pct_change().dropna()

        # Portfolio weights
        self.weights = self._calculate_weights()

        # Portfolio returns
        self.portfolio_returns = self._calculate_portfolio_returns()

    def _calculate_weights(self) -> Dict[str, float]:
        """Calculate current portfolio weights"""

        total = self.portfolio.total_value
        weights = {}

        for position in self.portfolio.positions:
            weights[position.symbol] = position.market_value / total

        weights['_cash'] = (self.portfolio.cash + self.portfolio.stablecoins) / total

        return weights

    def _calculate_portfolio_returns(self) -> pd.Series:
        """Calculate historical portfolio returns"""

        portfolio_returns = pd.Series(0, index=self.returns.index)

        for symbol, weight in self.weights.items():
            if symbol != '_cash' and symbol in self.returns.columns:
                portfolio_returns += self.returns[symbol] * weight

        return portfolio_returns

    def analyze(self) -> Dict:
        """Complete portfolio analysis"""

        return {
            'summary': self._summary(),
            'performance': self._performance_metrics(),
            'risk': self._risk_metrics(),
            'diversification': self._diversification_analysis(),
            'correlation': self._correlation_analysis(),
            'attribution': self._attribution_analysis(),
            'drawdown': self._drawdown_analysis(),
        }

    def _summary(self) -> Dict:
        """Portfolio summary"""

        by_sector = {}
        by_chain = {}

        for p in self.portfolio.positions:
            by_sector[p.sector] = by_sector.get(p.sector, 0) + p.market_value
            by_chain[p.chain] = by_chain.get(p.chain, 0) + p.market_value

        total = self.portfolio.total_value

        return {
            'total_value': total,
            'total_cost': self.portfolio.total_cost,
            'total_pnl': self.portfolio.total_pnl,
            'total_pnl_pct': self.portfolio.total_pnl_pct,
            'position_count': len(self.portfolio.positions),
            'cash_allocation': (self.portfolio.cash + self.portfolio.stablecoins) / total * 100,
            'by_sector': {k: v / total * 100 for k, v in by_sector.items()},
            'by_chain': {k: v / total * 100 for k, v in by_chain.items()},
            'top_positions': sorted(
                [(p.symbol, p.market_value / total * 100) for p in self.portfolio.positions],
                key=lambda x: x[1], reverse=True
            )[:5]
        }

    def _performance_metrics(self) -> Dict:
        """Calculate performance metrics"""

        returns = self.portfolio_returns
        annual_factor = 365  # Crypto trades 24/7

        # Total return
        total_return = (1 + returns).prod() - 1

        # Annualized return
        days = len(returns)
        annual_return = (1 + total_return) ** (annual_factor / days) - 1

        # Volatility
        daily_vol = returns.std()
        annual_vol = daily_vol * np.sqrt(annual_factor)

        # Sharpe Ratio
        excess_return = annual_return - self.risk_free_rate
        sharpe = excess_return / annual_vol if annual_vol > 0 else 0

        # Sortino Ratio
        downside_returns = returns[returns < 0]
        downside_vol = downside_returns.std() * np.sqrt(annual_factor)
        sortino = excess_return / downside_vol if downside_vol > 0 else 0

        # Calmar Ratio
        max_dd = self._max_drawdown(returns)
        calmar = annual_return / abs(max_dd) if max_dd != 0 else 0

        return {
            'total_return': total_return * 100,
            'annual_return': annual_return * 100,
            'daily_volatility': daily_vol * 100,
            'annual_volatility': annual_vol * 100,
            'sharpe_ratio': sharpe,
            'sortino_ratio': sortino,
            'calmar_ratio': calmar,
            'positive_days': (returns > 0).sum(),
            'negative_days': (returns < 0).sum(),
            'win_rate': (returns > 0).mean() * 100,
            'best_day': returns.max() * 100,
            'worst_day': returns.min() * 100,
            'avg_daily_return': returns.mean() * 100,
        }

    def _risk_metrics(self) -> Dict:
        """Calculate risk metrics"""

        returns = self.portfolio_returns

        # VaR (Value at Risk)
        var_95 = np.percentile(returns, 5)
        var_99 = np.percentile(returns, 1)

        # CVaR (Conditional VaR / Expected Shortfall)
        cvar_95 = returns[returns <= var_95].mean()
        cvar_99 = returns[returns <= var_99].mean()

        # Maximum Drawdown
        max_dd = self._max_drawdown(returns)

        # Beta (vs BTC if available)
        if 'BTC' in self.returns.columns:
            cov = returns.cov(self.returns['BTC'])
            btc_var = self.returns['BTC'].var()
            beta = cov / btc_var if btc_var > 0 else 1
        else:
            beta = None

        # Skewness and Kurtosis
        skew = returns.skew()
        kurtosis = returns.kurtosis()

        return {
            'var_95': var_95 * 100,
            'var_99': var_99 * 100,
            'cvar_95': cvar_95 * 100,
            'cvar_99': cvar_99 * 100,
            'max_drawdown': max_dd * 100,
            'beta_btc': beta,
            'skewness': skew,
            'kurtosis': kurtosis,
            'downside_deviation': returns[returns < 0].std() * 100,
        }

    def _max_drawdown(self, returns: pd.Series) -> float:
        """Calculate maximum drawdown"""

        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max

        return drawdown.min()

    def _diversification_analysis(self) -> Dict:
        """Analyze portfolio diversification"""

        weights = np.array([
            self.weights.get(s, 0)
            for s in self.returns.columns
            if s in self.weights
        ])

        # Effective Number of Assets
        # ENB = 1 / sum(w^2) - Higher = more diversified
        if len(weights) > 0 and weights.sum() > 0:
            weights_normalized = weights / weights.sum()
            enb = 1 / (weights_normalized ** 2).sum()
        else:
            enb = 1

        # Concentration metrics
        sorted_weights = sorted(self.weights.values(), reverse=True)
        top_1 = sorted_weights[0] if sorted_weights else 0
        top_3 = sum(sorted_weights[:3]) if len(sorted_weights) >= 3 else sum(sorted_weights)
        top_5 = sum(sorted_weights[:5]) if len(sorted_weights) >= 5 else sum(sorted_weights)

        # HHI (Herfindahl-Hirschman Index)
        hhi = sum(w ** 2 for w in self.weights.values())

        return {
            'effective_number_of_assets': enb,
            'herfindahl_index': hhi,
            'top_1_concentration': top_1 * 100,
            'top_3_concentration': top_3 * 100,
            'top_5_concentration': top_5 * 100,
            'diversification_score': min(enb / len(self.weights) * 100, 100),
        }

    def _correlation_analysis(self) -> Dict:
        """Analyze correlations"""

        # Correlation matrix
        corr_matrix = self.returns.corr()

        # Average correlation
        upper_triangle = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )
        avg_correlation = upper_triangle.stack().mean()

        # Highest correlations
        correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                correlations.append({
                    'pair': (corr_matrix.columns[i], corr_matrix.columns[j]),
                    'correlation': corr_matrix.iloc[i, j]
                })

        correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)

        return {
            'avg_correlation': avg_correlation,
            'highest_correlations': correlations[:5],
            'lowest_correlations': sorted(correlations, key=lambda x: x['correlation'])[:5],
            'correlation_matrix': corr_matrix.to_dict(),
        }

    def _attribution_analysis(self) -> Dict:
        """Performance attribution by asset"""

        attribution = []

        for position in self.portfolio.positions:
            symbol = position.symbol
            weight = self.weights.get(symbol, 0)

            if symbol in self.returns.columns:
                asset_return = (1 + self.returns[symbol]).prod() - 1
                contribution = weight * asset_return

                attribution.append({
                    'symbol': symbol,
                    'weight': weight * 100,
                    'return': asset_return * 100,
                    'contribution': contribution * 100,
                })

        # Sort by contribution
        attribution.sort(key=lambda x: x['contribution'], reverse=True)

        return {
            'top_contributors': attribution[:5],
            'worst_contributors': attribution[-5:] if len(attribution) >= 5 else attribution,
            'all_attribution': attribution,
        }

    def _drawdown_analysis(self) -> Dict:
        """Detailed drawdown analysis"""

        returns = self.portfolio_returns
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max

        # Find drawdown periods
        in_drawdown = drawdown < 0
        drawdown_starts = in_drawdown & ~in_drawdown.shift(1).fillna(False)
        drawdown_ends = ~in_drawdown & in_drawdown.shift(1).fillna(False)

        periods = []
        current_start = None

        for date, is_start in drawdown_starts.items():
            if is_start:
                current_start = date

        for date, is_end in drawdown_ends.items():
            if is_end and current_start:
                periods.append({
                    'start': current_start,
                    'end': date,
                    'max_drawdown': drawdown[current_start:date].min() * 100,
                    'duration_days': (date - current_start).days,
                })
                current_start = None

        # Current drawdown
        current_dd = drawdown.iloc[-1]

        return {
            'current_drawdown': current_dd * 100,
            'max_drawdown': drawdown.min() * 100,
            'avg_drawdown': drawdown[drawdown < 0].mean() * 100 if (drawdown < 0).any() else 0,
            'drawdown_periods': sorted(periods, key=lambda x: x['max_drawdown'])[:5],
            'time_in_drawdown': (drawdown < -0.05).mean() * 100,  # % of time in >5% DD
        }
```

---

## 🎯 PORTFOLIO OPTIMIZATION

### Modern Portfolio Theory & Beyond

```python
"""
CIPHER Portfolio Optimization
Mean-Variance, Risk Parity, and Advanced Optimization
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from scipy.optimize import minimize, Bounds, LinearConstraint
from dataclasses import dataclass

@dataclass
class OptimizationResult:
    """Portfolio optimization result"""
    weights: Dict[str, float]
    expected_return: float
    expected_volatility: float
    sharpe_ratio: float
    method: str

class PortfolioOptimizer:
    """
    Advanced portfolio optimization
    """

    def __init__(
        self,
        returns: pd.DataFrame,
        risk_free_rate: float = 0.04,
        transaction_cost: float = 0.001
    ):
        self.returns = returns
        self.risk_free_rate = risk_free_rate / 365  # Daily
        self.transaction_cost = transaction_cost

        self.mean_returns = returns.mean()
        self.cov_matrix = returns.cov()
        self.n_assets = len(returns.columns)
        self.assets = returns.columns.tolist()

    def optimize_sharpe(
        self,
        constraints: Optional[Dict] = None
    ) -> OptimizationResult:
        """Maximize Sharpe Ratio"""

        def neg_sharpe(weights):
            port_return = np.sum(self.mean_returns * weights) * 365
            port_vol = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix * 365, weights)))
            return -(port_return - self.risk_free_rate * 365) / port_vol

        return self._optimize(neg_sharpe, 'max_sharpe', constraints)

    def optimize_min_volatility(
        self,
        constraints: Optional[Dict] = None
    ) -> OptimizationResult:
        """Minimize portfolio volatility"""

        def volatility(weights):
            return np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix * 365, weights)))

        return self._optimize(volatility, 'min_volatility', constraints)

    def optimize_max_return(
        self,
        target_volatility: float,
        constraints: Optional[Dict] = None
    ) -> OptimizationResult:
        """Maximize return for target volatility"""

        def neg_return(weights):
            return -np.sum(self.mean_returns * weights) * 365

        # Add volatility constraint
        vol_constraint = {
            'type': 'eq',
            'fun': lambda w: np.sqrt(np.dot(w.T, np.dot(self.cov_matrix * 365, w))) - target_volatility
        }

        all_constraints = [vol_constraint]
        if constraints and 'constraints' in constraints:
            all_constraints.extend(constraints['constraints'])

        return self._optimize(
            neg_return,
            'max_return',
            {'constraints': all_constraints, **constraints} if constraints else {'constraints': all_constraints}
        )

    def optimize_risk_parity(self) -> OptimizationResult:
        """Risk Parity - equal risk contribution"""

        def risk_parity_objective(weights):
            port_vol = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
            marginal_risk = np.dot(self.cov_matrix, weights) / port_vol
            risk_contrib = weights * marginal_risk

            target_risk = port_vol / self.n_assets
            return np.sum((risk_contrib - target_risk) ** 2)

        return self._optimize(risk_parity_objective, 'risk_parity', None)

    def optimize_black_litterman(
        self,
        views: List[Dict],
        tau: float = 0.05
    ) -> OptimizationResult:
        """
        Black-Litterman optimization with investor views

        views: List of dicts with:
            - 'assets': list of asset symbols
            - 'weights': weights for view (sum to 0 for relative, 1 for absolute)
            - 'view': expected return
            - 'confidence': confidence level (0-1)
        """

        # Prior (market equilibrium)
        market_weights = np.ones(self.n_assets) / self.n_assets
        pi = tau * np.dot(self.cov_matrix, market_weights)  # Implied returns

        # Create P matrix (pick matrix) and Q vector (views)
        P = []
        Q = []
        omega_diag = []

        for view in views:
            p_row = np.zeros(self.n_assets)
            for asset, weight in zip(view['assets'], view['weights']):
                if asset in self.assets:
                    p_row[self.assets.index(asset)] = weight
            P.append(p_row)
            Q.append(view['view'])

            # Omega (uncertainty of views)
            view_var = np.dot(p_row, np.dot(self.cov_matrix, p_row))
            omega_diag.append(view_var * (1 - view['confidence']) / view['confidence'])

        P = np.array(P)
        Q = np.array(Q)
        omega = np.diag(omega_diag)

        # Black-Litterman formula
        tau_sigma = tau * self.cov_matrix

        # M = [(tau*Sigma)^-1 + P'*Omega^-1*P]^-1
        M = np.linalg.inv(
            np.linalg.inv(tau_sigma) + np.dot(P.T, np.dot(np.linalg.inv(omega), P))
        )

        # BL expected returns = M * [(tau*Sigma)^-1 * pi + P' * Omega^-1 * Q]
        bl_returns = np.dot(
            M,
            np.dot(np.linalg.inv(tau_sigma), pi) + np.dot(P.T, np.dot(np.linalg.inv(omega), Q))
        )

        # Optimize with BL returns
        def neg_sharpe_bl(weights):
            port_return = np.sum(bl_returns * weights) * 365
            port_vol = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix * 365, weights)))
            return -(port_return - self.risk_free_rate * 365) / port_vol

        return self._optimize(neg_sharpe_bl, 'black_litterman', None)

    def _optimize(
        self,
        objective: callable,
        method: str,
        constraints: Optional[Dict]
    ) -> OptimizationResult:
        """Run optimization"""

        # Default constraints
        bounds = Bounds(0, 1)  # Long only, max 100% per asset

        default_constraints = [
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}  # Weights sum to 1
        ]

        if constraints:
            # Max position constraint
            if 'max_position' in constraints:
                bounds = Bounds(0, constraints['max_position'])

            # Min position constraint
            if 'min_position' in constraints:
                bounds = Bounds(constraints['min_position'], bounds.ub)

            # Custom constraints
            if 'constraints' in constraints:
                default_constraints.extend(constraints['constraints'])

        # Initial weights
        x0 = np.ones(self.n_assets) / self.n_assets

        # Optimize
        result = minimize(
            objective,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=default_constraints,
            options={'maxiter': 1000}
        )

        weights = dict(zip(self.assets, result.x))

        # Calculate metrics
        port_return = np.sum(self.mean_returns * result.x) * 365
        port_vol = np.sqrt(np.dot(result.x.T, np.dot(self.cov_matrix * 365, result.x)))
        sharpe = (port_return - self.risk_free_rate * 365) / port_vol

        return OptimizationResult(
            weights=weights,
            expected_return=port_return,
            expected_volatility=port_vol,
            sharpe_ratio=sharpe,
            method=method
        )

    def efficient_frontier(
        self,
        n_points: int = 50
    ) -> List[OptimizationResult]:
        """Calculate efficient frontier"""

        # Get min and max return portfolios
        min_vol = self.optimize_min_volatility()
        max_ret = self.optimize_sharpe()  # Approximate max return

        min_return = min_vol.expected_return
        max_return = max_ret.expected_return

        target_returns = np.linspace(min_return, max_return, n_points)
        frontier = []

        for target in target_returns:
            try:
                def neg_return(weights):
                    return -np.sum(self.mean_returns * weights) * 365

                constraints = [{
                    'type': 'eq',
                    'fun': lambda w, t=target: np.sum(self.mean_returns * w) * 365 - t
                }]

                result = self._optimize(
                    lambda w: np.sqrt(np.dot(w.T, np.dot(self.cov_matrix * 365, w))),
                    'efficient_frontier',
                    {'constraints': constraints}
                )
                frontier.append(result)
            except Exception:
                continue

        return frontier


class RebalancingEngine:
    """
    Portfolio rebalancing logic
    """

    def __init__(
        self,
        current_portfolio: Portfolio,
        target_weights: Dict[str, float],
        transaction_cost: float = 0.001
    ):
        self.portfolio = current_portfolio
        self.target_weights = target_weights
        self.transaction_cost = transaction_cost

    def calculate_trades(
        self,
        threshold: float = 0.02  # Min 2% deviation to trade
    ) -> List[Dict]:
        """Calculate required trades to rebalance"""

        total_value = self.portfolio.total_value
        trades = []

        current_weights = {}
        for p in self.portfolio.positions:
            current_weights[p.symbol] = p.market_value / total_value

        # Add cash as a "position"
        cash_weight = (self.portfolio.cash + self.portfolio.stablecoins) / total_value
        current_weights['_cash'] = cash_weight

        # Calculate required changes
        for symbol, target in self.target_weights.items():
            current = current_weights.get(symbol, 0)
            diff = target - current

            if abs(diff) >= threshold:
                trade_value = diff * total_value

                trades.append({
                    'symbol': symbol,
                    'current_weight': current * 100,
                    'target_weight': target * 100,
                    'trade_value': trade_value,
                    'trade_type': 'buy' if trade_value > 0 else 'sell',
                    'estimated_cost': abs(trade_value) * self.transaction_cost
                })

        # Sort by absolute trade size
        trades.sort(key=lambda x: abs(x['trade_value']), reverse=True)

        return trades

    def estimate_rebalancing_cost(self, trades: List[Dict]) -> Dict:
        """Estimate total cost of rebalancing"""

        total_trade_value = sum(abs(t['trade_value']) for t in trades)
        total_cost = sum(t['estimated_cost'] for t in trades)

        return {
            'total_trade_value': total_trade_value,
            'total_cost': total_cost,
            'cost_percentage': total_cost / self.portfolio.total_value * 100,
            'trade_count': len(trades),
        }
```

---

## 📉 RISK MANAGEMENT

### Position Sizing & Risk Control

```python
"""
CIPHER Risk Management
Position sizing, stop losses, and risk controls
"""

import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class PositionSizeResult:
    """Position sizing result"""
    symbol: str
    recommended_size: float
    max_size: float
    risk_per_trade: float
    stop_loss_price: float
    take_profit_price: float
    risk_reward_ratio: float

class RiskManager:
    """
    Portfolio risk management
    """

    def __init__(
        self,
        portfolio_value: float,
        max_portfolio_risk: float = 0.02,  # 2% max risk per trade
        max_position_size: float = 0.10,  # 10% max per position
        max_correlated_exposure: float = 0.30  # 30% max in correlated assets
    ):
        self.portfolio_value = portfolio_value
        self.max_portfolio_risk = max_portfolio_risk
        self.max_position_size = max_position_size
        self.max_correlated_exposure = max_correlated_exposure

    def calculate_position_size(
        self,
        symbol: str,
        entry_price: float,
        stop_loss_pct: float,
        volatility: float,
        correlation_exposure: float = 0
    ) -> PositionSizeResult:
        """
        Calculate optimal position size

        Args:
            symbol: Asset symbol
            entry_price: Entry price
            stop_loss_pct: Stop loss percentage (e.g., 0.05 for 5%)
            volatility: Asset volatility
            correlation_exposure: Current exposure to correlated assets
        """

        # Method 1: Fixed risk per trade
        risk_amount = self.portfolio_value * self.max_portfolio_risk
        position_size_risk = risk_amount / stop_loss_pct

        # Method 2: Volatility-adjusted
        vol_adjusted_risk = self.max_portfolio_risk / (volatility * np.sqrt(252))
        position_size_vol = self.portfolio_value * vol_adjusted_risk

        # Method 3: Kelly Criterion (simplified)
        # Assuming 55% win rate and 2:1 reward-risk
        win_rate = 0.55
        rr_ratio = 2.0
        kelly_fraction = (win_rate * rr_ratio - (1 - win_rate)) / rr_ratio
        kelly_fraction = max(0, min(kelly_fraction, 0.25))  # Cap at 25%
        position_size_kelly = self.portfolio_value * kelly_fraction

        # Take minimum of all methods
        recommended_size = min(position_size_risk, position_size_vol, position_size_kelly)

        # Apply max position constraint
        max_size = self.portfolio_value * self.max_position_size

        # Apply correlation constraint
        available_for_correlated = (
            self.max_correlated_exposure * self.portfolio_value - correlation_exposure
        )
        if available_for_correlated < recommended_size:
            recommended_size = max(0, available_for_correlated)

        # Final size
        final_size = min(recommended_size, max_size)

        # Calculate stops
        stop_loss_price = entry_price * (1 - stop_loss_pct)
        take_profit_price = entry_price * (1 + stop_loss_pct * rr_ratio)

        return PositionSizeResult(
            symbol=symbol,
            recommended_size=final_size,
            max_size=max_size,
            risk_per_trade=final_size * stop_loss_pct / self.portfolio_value,
            stop_loss_price=stop_loss_price,
            take_profit_price=take_profit_price,
            risk_reward_ratio=rr_ratio
        )

    def calculate_portfolio_var(
        self,
        positions: List[Dict],
        returns: np.ndarray,
        confidence: float = 0.95
    ) -> Dict:
        """Calculate Portfolio VaR"""

        weights = np.array([p['weight'] for p in positions])

        # Historical VaR
        portfolio_returns = np.dot(returns, weights)
        var_historical = np.percentile(portfolio_returns, (1 - confidence) * 100)

        # Parametric VaR
        port_mean = np.mean(portfolio_returns)
        port_std = np.std(portfolio_returns)
        z_score = stats.norm.ppf(1 - confidence)
        var_parametric = port_mean + z_score * port_std

        # CVaR (Expected Shortfall)
        cvar = portfolio_returns[portfolio_returns <= var_historical].mean()

        return {
            'var_historical': var_historical * self.portfolio_value,
            'var_parametric': var_parametric * self.portfolio_value,
            'cvar': cvar * self.portfolio_value,
            'var_percentage': var_historical * 100,
            'cvar_percentage': cvar * 100,
        }

    def stress_test(
        self,
        positions: List[Dict],
        scenarios: Dict[str, Dict[str, float]]
    ) -> Dict:
        """
        Run stress test scenarios

        scenarios: Dict of scenario name -> asset returns
        Example: {'crash': {'BTC': -0.50, 'ETH': -0.60}}
        """

        results = {}

        for scenario_name, asset_returns in scenarios.items():
            portfolio_impact = 0

            for position in positions:
                symbol = position['symbol']
                weight = position['weight']

                if symbol in asset_returns:
                    position_impact = weight * asset_returns[symbol]
                    portfolio_impact += position_impact

            results[scenario_name] = {
                'portfolio_return': portfolio_impact * 100,
                'dollar_impact': portfolio_impact * self.portfolio_value,
            }

        return results

    def concentration_risk(self, positions: List[Dict]) -> Dict:
        """Analyze concentration risk"""

        weights = [p['weight'] for p in positions]

        # Herfindahl Index
        hhi = sum(w ** 2 for w in weights)

        # Top concentration
        sorted_weights = sorted(weights, reverse=True)

        # Effective number of positions
        enp = 1 / hhi if hhi > 0 else len(positions)

        risk_level = 'low'
        if hhi > 0.25:
            risk_level = 'high'
        elif hhi > 0.15:
            risk_level = 'medium'

        return {
            'herfindahl_index': hhi,
            'effective_positions': enp,
            'top_1_weight': sorted_weights[0] * 100 if sorted_weights else 0,
            'top_3_weight': sum(sorted_weights[:3]) * 100 if len(sorted_weights) >= 3 else sum(sorted_weights) * 100,
            'risk_level': risk_level,
            'recommendation': self._concentration_recommendation(hhi, enp)
        }

    def _concentration_recommendation(self, hhi: float, enp: float) -> str:
        """Generate concentration risk recommendation"""

        if hhi > 0.25:
            return "High concentration risk. Consider diversifying into more assets."
        elif hhi > 0.15:
            return "Moderate concentration. Monitor top positions closely."
        elif enp < 5:
            return "Few effective positions. May want to add uncorrelated assets."
        else:
            return "Good diversification level."


# Predefined stress scenarios
STRESS_SCENARIOS = {
    'crypto_winter': {
        'BTC': -0.70, 'ETH': -0.80, 'SOL': -0.90,
        'AVAX': -0.85, 'MATIC': -0.85, 'DOT': -0.85
    },
    'btc_flash_crash': {
        'BTC': -0.30, 'ETH': -0.35, 'SOL': -0.40,
        'AVAX': -0.40, 'MATIC': -0.40
    },
    'defi_exploit': {
        'UNI': -0.50, 'AAVE': -0.50, 'CRV': -0.60,
        'MKR': -0.40
    },
    'regulatory_crackdown': {
        'BTC': -0.20, 'ETH': -0.25, 'BNB': -0.40,
        'SOL': -0.30, 'USDT': -0.05, 'USDC': -0.02
    },
    'stablecoin_depeg': {
        'USDT': -0.10, 'USDC': -0.05, 'DAI': -0.03,
        'BTC': 0.05, 'ETH': 0.03
    },
    'bull_run': {
        'BTC': 1.00, 'ETH': 1.50, 'SOL': 3.00,
        'AVAX': 2.00, 'MATIC': 2.50
    }
}
```

---

## 📊 REPORTING & VISUALIZATION

### Portfolio Reports

```python
"""
CIPHER Portfolio Reporting
Generate comprehensive portfolio reports
"""

from typing import Dict, List
from datetime import datetime
import json

class PortfolioReporter:
    """
    Generate portfolio reports
    """

    def __init__(
        self,
        portfolio: Portfolio,
        analyzer: PortfolioAnalyzer
    ):
        self.portfolio = portfolio
        self.analyzer = analyzer

    def generate_summary_report(self) -> Dict:
        """Generate summary report"""

        analysis = self.analyzer.analyze()

        return {
            'report_date': datetime.utcnow().isoformat(),
            'portfolio_value': self.portfolio.total_value,
            'total_pnl': self.portfolio.total_pnl,
            'total_pnl_pct': self.portfolio.total_pnl_pct,

            # Performance
            'performance': {
                'total_return': analysis['performance']['total_return'],
                'sharpe_ratio': analysis['performance']['sharpe_ratio'],
                'sortino_ratio': analysis['performance']['sortino_ratio'],
                'win_rate': analysis['performance']['win_rate'],
            },

            # Risk
            'risk': {
                'volatility': analysis['performance']['annual_volatility'],
                'max_drawdown': analysis['risk']['max_drawdown'],
                'var_95': analysis['risk']['var_95'],
                'current_drawdown': analysis['drawdown']['current_drawdown'],
            },

            # Diversification
            'diversification': {
                'effective_assets': analysis['diversification']['effective_number_of_assets'],
                'top_concentration': analysis['diversification']['top_3_concentration'],
                'avg_correlation': analysis['correlation']['avg_correlation'],
            },

            # Top positions
            'top_positions': analysis['summary']['top_positions'],

            # Allocation
            'allocation': {
                'by_sector': analysis['summary']['by_sector'],
                'by_chain': analysis['summary']['by_chain'],
                'cash': analysis['summary']['cash_allocation'],
            }
        }

    def generate_risk_report(self) -> Dict:
        """Generate detailed risk report"""

        analysis = self.analyzer.analyze()

        return {
            'report_date': datetime.utcnow().isoformat(),

            'risk_metrics': analysis['risk'],

            'drawdown_analysis': analysis['drawdown'],

            'concentration_risk': analysis['diversification'],

            'correlation_risk': {
                'avg_correlation': analysis['correlation']['avg_correlation'],
                'highest_correlations': analysis['correlation']['highest_correlations'],
            },

            'recommendations': self._generate_risk_recommendations(analysis)
        }

    def _generate_risk_recommendations(self, analysis: Dict) -> List[str]:
        """Generate risk-based recommendations"""

        recommendations = []

        # Drawdown
        if analysis['drawdown']['current_drawdown'] < -20:
            recommendations.append(
                "Portfolio is in significant drawdown. Consider reducing risk exposure."
            )

        # Concentration
        if analysis['diversification']['top_3_concentration'] > 60:
            recommendations.append(
                "High concentration in top 3 positions. Consider diversifying."
            )

        # Correlation
        if analysis['correlation']['avg_correlation'] > 0.7:
            recommendations.append(
                "High average correlation. Portfolio may not be well diversified."
            )

        # Volatility
        if analysis['performance']['annual_volatility'] > 100:
            recommendations.append(
                "Very high volatility. Consider adding stable assets or hedges."
            )

        # Sharpe
        if analysis['performance']['sharpe_ratio'] < 0.5:
            recommendations.append(
                "Low risk-adjusted returns. Review asset selection and timing."
            )

        if not recommendations:
            recommendations.append("Portfolio risk metrics look healthy.")

        return recommendations
```

---

## 🔗 CONEXIONES NEURONALES

```yaml
conexiones_primarias:
  - neurona: "MARKET_DATA"
    tipo: "price_source"
    desc: "Precios para valoración y análisis"

  - neurona: "ML_TRADING"
    tipo: "signal_source"
    desc: "Señales para rebalanceo"

  - neurona: "DEFI_PROTOCOLS"
    tipo: "yield_source"
    desc: "Oportunidades de yield"

conexiones_secundarias:
  - neurona: "SENTIMENT_ANALYSIS"
    tipo: "risk_input"
    desc: "Sentimiento para timing"

  - neurona: "ON_CHAIN_ANALYTICS"
    tipo: "whale_tracking"
    desc: "Seguimiento de ballenas"
```

---

## 📊 MÉTRICAS DE LA NEURONA

```yaml
metricas_salud:
  - nombre: "Sharpe Ratio"
    valor: ">1.5"
    umbral_alerta: "1.0"

  - nombre: "Max Drawdown"
    valor: "<25%"
    umbral_alerta: "30%"

  - nombre: "Diversification Score"
    valor: ">60"
    umbral_alerta: "40"

  - nombre: "VaR Coverage"
    valor: "95%"
    umbral_minimo: "90%"
```

---

## 🔄 CHANGELOG

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0.0 | 2025-01-XX | Creación inicial - Portfolio analytics |
| 1.1.0 | 2025-01-XX | Optimization engine, efficient frontier |
| 1.2.0 | 2025-01-XX | Risk management, stress testing |

---

> **CIPHER**: "El portfolio perfecto no existe - pero el óptimo para ti, sí."
