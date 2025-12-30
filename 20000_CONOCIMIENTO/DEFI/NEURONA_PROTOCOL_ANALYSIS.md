# NEURONA C40010: PROTOCOL ANALYSIS & METRICS

> **CIPHER**: Análisis profundo de protocolos DeFi, métricas on-chain, y evaluación de salud del protocolo.

---

## ÍNDICE

1. [Framework de Análisis](#1-framework-de-análisis)
2. [Métricas Fundamentales](#2-métricas-fundamentales)
3. [TVL y Capital Efficiency](#3-tvl-y-capital-efficiency)
4. [Revenue y Tokenomics Analysis](#4-revenue-y-tokenomics-analysis)
5. [Risk Assessment](#5-risk-assessment)
6. [Competitive Analysis](#6-competitive-analysis)
7. [On-Chain Intelligence](#7-on-chain-intelligence)

---

## 1. FRAMEWORK DE ANÁLISIS

### 1.1 Protocol Analysis Pyramid

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CIPHER PROTOCOL ANALYSIS FRAMEWORK                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                         ┌───────────────────┐                               │
│                         │    INVESTMENT     │                               │
│                         │    THESIS         │                               │
│                         │  (Final Score)    │                               │
│                         └─────────┬─────────┘                               │
│                                   │                                          │
│              ┌────────────────────┼────────────────────┐                    │
│              │                    │                    │                    │
│       ┌──────▼──────┐      ┌──────▼──────┐     ┌──────▼──────┐            │
│       │  GROWTH     │      │  MOAT       │     │  RISK       │            │
│       │  POTENTIAL  │      │  ANALYSIS   │     │  ASSESSMENT │            │
│       └──────┬──────┘      └──────┬──────┘     └──────┬──────┘            │
│              │                    │                    │                    │
│   ┌──────────┼──────────┬────────┼────────┬──────────┼──────────┐        │
│   │          │          │        │        │          │          │        │
│   ▼          ▼          ▼        ▼        ▼          ▼          ▼        │
│ ┌────┐    ┌────┐    ┌────┐  ┌────┐  ┌────┐    ┌────┐    ┌────┐        │
│ │TVL │    │Users│   │Rev │  │Tech│  │Token│   │Smart│   │Oracle│        │
│ │    │    │    │    │    │  │    │  │     │   │Contr│   │Risk  │        │
│ └────┘    └────┘    └────┘  └────┘  └────┘   └────┘   └────┘        │
│                                                                              │
│   METRICS  ←─────────────────────────────────────────────→  RISKS           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Protocol Health Score Calculator

```python
"""
CIPHER: Protocol Health Score Calculator
Sistema de puntuación para evaluar protocolos DeFi
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
import math

class RiskLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class ProtocolMetrics:
    # TVL & Growth
    tvl_usd: float
    tvl_30d_change: float  # Percentage
    tvl_90d_change: float

    # Users
    daily_active_users: int
    monthly_active_users: int
    user_retention_30d: float  # Percentage

    # Revenue
    daily_revenue_usd: float
    monthly_revenue_usd: float
    revenue_to_tvl_ratio: float

    # Token
    fully_diluted_valuation: float
    market_cap: float
    token_holder_count: int
    top_10_holder_percentage: float

    # Technical
    contracts_audited: bool
    audit_count: int
    bug_bounty_usd: float
    time_since_launch_days: int

    # Governance
    proposal_count_30d: int
    voter_participation: float

class ProtocolScorer:
    """Calcula score compuesto de salud del protocolo"""

    def __init__(self):
        # Weights para cada categoría
        self.weights = {
            "growth": 0.25,
            "sustainability": 0.25,
            "security": 0.25,
            "decentralization": 0.15,
            "activity": 0.10
        }

    def calculate_growth_score(self, metrics: ProtocolMetrics) -> float:
        """Score de crecimiento (0-100)"""
        score = 0

        # TVL Score (0-30)
        if metrics.tvl_usd > 1_000_000_000:  # $1B+
            score += 30
        elif metrics.tvl_usd > 100_000_000:  # $100M+
            score += 25
        elif metrics.tvl_usd > 10_000_000:   # $10M+
            score += 15
        else:
            score += 5

        # TVL Growth (0-30)
        if metrics.tvl_30d_change > 50:
            score += 30
        elif metrics.tvl_30d_change > 20:
            score += 25
        elif metrics.tvl_30d_change > 0:
            score += 15
        elif metrics.tvl_30d_change > -20:
            score += 5
        # Negative growth = 0

        # User Growth (0-40)
        if metrics.monthly_active_users > 100_000:
            score += 40
        elif metrics.monthly_active_users > 10_000:
            score += 30
        elif metrics.monthly_active_users > 1_000:
            score += 20
        else:
            score += 10

        return min(score, 100)

    def calculate_sustainability_score(self, metrics: ProtocolMetrics) -> float:
        """Score de sostenibilidad económica (0-100)"""
        score = 0

        # Revenue/TVL Ratio (0-40) - Capital Efficiency
        if metrics.revenue_to_tvl_ratio > 0.001:  # 0.1%+ daily
            score += 40
        elif metrics.revenue_to_tvl_ratio > 0.0005:
            score += 30
        elif metrics.revenue_to_tvl_ratio > 0.0001:
            score += 20
        else:
            score += 5

        # User Retention (0-30)
        if metrics.user_retention_30d > 60:
            score += 30
        elif metrics.user_retention_30d > 40:
            score += 20
        elif metrics.user_retention_30d > 20:
            score += 10

        # FDV/Revenue Multiple (0-30) - Lower is better
        if metrics.monthly_revenue_usd > 0:
            multiple = metrics.fully_diluted_valuation / (metrics.monthly_revenue_usd * 12)
            if multiple < 20:
                score += 30
            elif multiple < 50:
                score += 20
            elif multiple < 100:
                score += 10

        return min(score, 100)

    def calculate_security_score(self, metrics: ProtocolMetrics) -> float:
        """Score de seguridad (0-100)"""
        score = 0

        # Audits (0-40)
        if metrics.contracts_audited:
            score += 20
            if metrics.audit_count >= 3:
                score += 20
            elif metrics.audit_count >= 2:
                score += 10

        # Bug Bounty (0-30)
        if metrics.bug_bounty_usd >= 1_000_000:
            score += 30
        elif metrics.bug_bounty_usd >= 100_000:
            score += 20
        elif metrics.bug_bounty_usd > 0:
            score += 10

        # Time in Production (0-30) - Lindy Effect
        if metrics.time_since_launch_days > 730:  # 2+ years
            score += 30
        elif metrics.time_since_launch_days > 365:  # 1+ year
            score += 20
        elif metrics.time_since_launch_days > 180:  # 6+ months
            score += 10

        return min(score, 100)

    def calculate_decentralization_score(self, metrics: ProtocolMetrics) -> float:
        """Score de descentralización (0-100)"""
        score = 0

        # Token Holder Distribution (0-50)
        if metrics.top_10_holder_percentage < 30:
            score += 50
        elif metrics.top_10_holder_percentage < 50:
            score += 35
        elif metrics.top_10_holder_percentage < 70:
            score += 20
        else:
            score += 5

        # Governance Activity (0-30)
        if metrics.voter_participation > 20:
            score += 30
        elif metrics.voter_participation > 10:
            score += 20
        elif metrics.voter_participation > 5:
            score += 10

        # Holder Count (0-20)
        if metrics.token_holder_count > 100_000:
            score += 20
        elif metrics.token_holder_count > 10_000:
            score += 15
        elif metrics.token_holder_count > 1_000:
            score += 10

        return min(score, 100)

    def calculate_activity_score(self, metrics: ProtocolMetrics) -> float:
        """Score de actividad (0-100)"""
        score = 0

        # DAU/MAU Ratio (Stickiness) (0-50)
        if metrics.monthly_active_users > 0:
            stickiness = metrics.daily_active_users / metrics.monthly_active_users
            if stickiness > 0.4:
                score += 50
            elif stickiness > 0.2:
                score += 35
            elif stickiness > 0.1:
                score += 20
            else:
                score += 10

        # Absolute DAU (0-50)
        if metrics.daily_active_users > 10_000:
            score += 50
        elif metrics.daily_active_users > 1_000:
            score += 35
        elif metrics.daily_active_users > 100:
            score += 20
        else:
            score += 10

        return min(score, 100)

    def calculate_total_score(self, metrics: ProtocolMetrics) -> Dict:
        """Calcular score total con breakdown"""
        scores = {
            "growth": self.calculate_growth_score(metrics),
            "sustainability": self.calculate_sustainability_score(metrics),
            "security": self.calculate_security_score(metrics),
            "decentralization": self.calculate_decentralization_score(metrics),
            "activity": self.calculate_activity_score(metrics)
        }

        # Weighted average
        total = sum(
            scores[cat] * self.weights[cat]
            for cat in scores
        )

        # Determine rating
        if total >= 80:
            rating = "A"
        elif total >= 70:
            rating = "B+"
        elif total >= 60:
            rating = "B"
        elif total >= 50:
            rating = "C+"
        elif total >= 40:
            rating = "C"
        else:
            rating = "D"

        return {
            "total_score": round(total, 2),
            "rating": rating,
            "breakdown": scores,
            "weights": self.weights
        }


# Ejemplo de uso
if __name__ == "__main__":
    # Métricas ejemplo (protocolo DeFi maduro)
    metrics = ProtocolMetrics(
        tvl_usd=500_000_000,
        tvl_30d_change=5.2,
        tvl_90d_change=15.8,
        daily_active_users=2_500,
        monthly_active_users=15_000,
        user_retention_30d=45.0,
        daily_revenue_usd=150_000,
        monthly_revenue_usd=4_500_000,
        revenue_to_tvl_ratio=0.0003,
        fully_diluted_valuation=800_000_000,
        market_cap=400_000_000,
        token_holder_count=25_000,
        top_10_holder_percentage=42.0,
        contracts_audited=True,
        audit_count=3,
        bug_bounty_usd=500_000,
        time_since_launch_days=450,
        proposal_count_30d=8,
        voter_participation=12.5
    )

    scorer = ProtocolScorer()
    result = scorer.calculate_total_score(metrics)

    print(f"Protocol Score: {result['total_score']} ({result['rating']})")
    print("\nBreakdown:")
    for cat, score in result['breakdown'].items():
        print(f"  {cat}: {score}")
```

---

## 2. MÉTRICAS FUNDAMENTALES

### 2.1 On-Chain Metrics Collector

```python
"""
CIPHER: On-Chain Metrics Collector
Recopilación de métricas directamente de blockchain
"""

from web3 import Web3
from typing import Dict, List, Tuple
import json

class OnChainMetricsCollector:
    """Colector de métricas on-chain para protocolos DeFi"""

    # ABIs simplificados
    ERC20_ABI = [
        {"name": "totalSupply", "type": "function", "inputs": [], "outputs": [{"type": "uint256"}]},
        {"name": "balanceOf", "type": "function", "inputs": [{"type": "address"}], "outputs": [{"type": "uint256"}]},
        {"name": "decimals", "type": "function", "inputs": [], "outputs": [{"type": "uint8"}]}
    ]

    UNISWAP_POOL_ABI = [
        {"name": "slot0", "type": "function", "inputs": [],
         "outputs": [{"name": "sqrtPriceX96", "type": "uint160"},
                     {"name": "tick", "type": "int24"}]},
        {"name": "liquidity", "type": "function", "inputs": [], "outputs": [{"type": "uint128"}]}
    ]

    def __init__(self, rpc_url: str):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))

    def get_token_metrics(self, token_address: str) -> Dict:
        """Obtener métricas de un token ERC20"""
        token = self.w3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=self.ERC20_ABI
        )

        total_supply = token.functions.totalSupply().call()
        decimals = token.functions.decimals().call()

        return {
            "total_supply": total_supply / (10 ** decimals),
            "decimals": decimals
        }

    def get_protocol_tvl(
        self,
        vault_addresses: List[str],
        underlying_token: str,
        price_usd: float
    ) -> Dict:
        """Calcular TVL de un protocolo sumando todos los vaults"""
        token = self.w3.eth.contract(
            address=Web3.to_checksum_address(underlying_token),
            abi=self.ERC20_ABI
        )

        decimals = token.functions.decimals().call()
        total_balance = 0

        vault_balances = {}
        for vault in vault_addresses:
            balance = token.functions.balanceOf(
                Web3.to_checksum_address(vault)
            ).call()

            normalized = balance / (10 ** decimals)
            vault_balances[vault] = normalized
            total_balance += normalized

        return {
            "total_tokens": total_balance,
            "total_usd": total_balance * price_usd,
            "vault_breakdown": vault_balances,
            "price_used": price_usd
        }

    def get_pool_metrics(self, pool_address: str) -> Dict:
        """Obtener métricas de un pool Uniswap V3"""
        pool = self.w3.eth.contract(
            address=Web3.to_checksum_address(pool_address),
            abi=self.UNISWAP_POOL_ABI
        )

        slot0 = pool.functions.slot0().call()
        liquidity = pool.functions.liquidity().call()

        sqrt_price = slot0[0]
        tick = slot0[1]

        # Calcular precio desde sqrtPriceX96
        price = (sqrt_price / (2 ** 96)) ** 2

        return {
            "current_tick": tick,
            "liquidity": liquidity,
            "price_ratio": price,
            "sqrt_price_x96": sqrt_price
        }

    def get_user_count_estimate(
        self,
        contract_address: str,
        event_signature: str,
        from_block: int
    ) -> int:
        """Estimar número de usuarios únicos desde eventos"""
        # Crear filtro para eventos (ej: Deposit, Swap)
        event_filter = self.w3.eth.filter({
            "fromBlock": from_block,
            "toBlock": "latest",
            "address": Web3.to_checksum_address(contract_address),
            "topics": [Web3.keccak(text=event_signature).hex()]
        })

        logs = event_filter.get_all_entries()

        # Extraer addresses únicos (from transaction sender)
        unique_users = set()
        for log in logs:
            tx = self.w3.eth.get_transaction(log["transactionHash"])
            unique_users.add(tx["from"])

        return len(unique_users)

    def calculate_capital_efficiency(
        self,
        tvl_usd: float,
        daily_volume_usd: float
    ) -> Dict:
        """Calcular eficiencia de capital"""
        if tvl_usd == 0:
            return {"efficiency": 0, "utilization": 0}

        # Volume/TVL ratio diario
        daily_efficiency = daily_volume_usd / tvl_usd

        # Anualizado
        annual_efficiency = daily_efficiency * 365

        return {
            "daily_volume_to_tvl": daily_efficiency,
            "annualized_volume_to_tvl": annual_efficiency,
            "capital_turns_per_day": daily_efficiency,
            "interpretation": self._interpret_efficiency(daily_efficiency)
        }

    def _interpret_efficiency(self, ratio: float) -> str:
        """Interpretar ratio de eficiencia"""
        if ratio > 1:
            return "EXTREMELY_HIGH - Volume exceeds TVL daily"
        elif ratio > 0.5:
            return "VERY_HIGH - High capital velocity"
        elif ratio > 0.1:
            return "HIGH - Good utilization"
        elif ratio > 0.01:
            return "MODERATE - Normal for lending"
        else:
            return "LOW - Capital underutilized"


class TVLCalculator:
    """Calculadora avanzada de TVL con múltiples metodologías"""

    def __init__(self, collector: OnChainMetricsCollector):
        self.collector = collector

    def calculate_tvl_methods(
        self,
        protocol_data: Dict
    ) -> Dict:
        """Calcular TVL usando diferentes metodologías"""

        results = {}

        # Método 1: Suma directa de balances
        if "vaults" in protocol_data:
            direct_tvl = sum(
                v["balance_usd"] for v in protocol_data["vaults"]
            )
            results["direct_sum"] = direct_tvl

        # Método 2: Token supply en protocolo
        if "protocol_tokens" in protocol_data:
            token_tvl = sum(
                t["supply"] * t["price_usd"]
                for t in protocol_data["protocol_tokens"]
            )
            results["token_supply"] = token_tvl

        # Método 3: Derivado de revenue (si revenue = x% de TVL)
        if "daily_revenue" in protocol_data and "yield_rate" in protocol_data:
            implied_tvl = (protocol_data["daily_revenue"] * 365) / protocol_data["yield_rate"]
            results["revenue_implied"] = implied_tvl

        # Método 4: LP tokens * precio
        if "lp_pools" in protocol_data:
            lp_tvl = sum(
                pool["lp_supply"] * pool["lp_price"]
                for pool in protocol_data["lp_pools"]
            )
            results["lp_valuation"] = lp_tvl

        # Calcular variación entre métodos
        if len(results) > 1:
            values = list(results.values())
            avg = sum(values) / len(values)
            variance = sum((v - avg) ** 2 for v in values) / len(values)
            results["variance"] = variance
            results["consistency_score"] = 1 / (1 + variance / avg) if avg > 0 else 0

        return results

    def detect_tvl_manipulation(
        self,
        tvl_history: List[Tuple[int, float]],  # (timestamp, tvl)
        window_hours: int = 24
    ) -> Dict:
        """Detectar posible manipulación de TVL"""
        if len(tvl_history) < 2:
            return {"suspicious": False}

        # Calcular cambios porcentuales
        changes = []
        for i in range(1, len(tvl_history)):
            prev_tvl = tvl_history[i-1][1]
            curr_tvl = tvl_history[i][1]

            if prev_tvl > 0:
                pct_change = (curr_tvl - prev_tvl) / prev_tvl * 100
                changes.append({
                    "timestamp": tvl_history[i][0],
                    "change_pct": pct_change,
                    "absolute_change": curr_tvl - prev_tvl
                })

        # Detectar spikes sospechosos
        suspicious_events = []
        for change in changes:
            if abs(change["change_pct"]) > 50:  # >50% change
                suspicious_events.append({
                    **change,
                    "reason": "Large sudden change"
                })

        # Detectar pump and dump patterns
        pump_dump = False
        for i in range(len(changes) - 1):
            if changes[i]["change_pct"] > 30 and changes[i+1]["change_pct"] < -25:
                pump_dump = True
                break

        return {
            "suspicious": len(suspicious_events) > 0 or pump_dump,
            "suspicious_events": suspicious_events,
            "pump_dump_detected": pump_dump,
            "max_change": max(abs(c["change_pct"]) for c in changes) if changes else 0
        }
```

---

## 3. TVL Y CAPITAL EFFICIENCY

### 3.1 Capital Efficiency Analyzer

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title CapitalEfficiencyAnalyzer
 * @notice Contrato para trackear y reportar eficiencia de capital on-chain
 */
contract CapitalEfficiencyAnalyzer {

    struct ProtocolMetrics {
        uint256 totalDeposits;
        uint256 totalBorrows;      // Para lending
        uint256 totalVolume;       // Para DEX
        uint256 totalFees;
        uint256 lastUpdateBlock;
    }

    struct DailySnapshot {
        uint256 tvl;
        uint256 volume;
        uint256 fees;
        uint256 utilization;      // Basis points
        uint256 timestamp;
    }

    mapping(address => ProtocolMetrics) public protocols;
    mapping(address => DailySnapshot[]) public dailySnapshots;

    event MetricsUpdated(
        address indexed protocol,
        uint256 tvl,
        uint256 volume,
        uint256 fees
    );

    /**
     * @notice Actualizar métricas de un protocolo
     */
    function updateMetrics(
        address protocol,
        uint256 deposits,
        uint256 borrows,
        uint256 volume,
        uint256 fees
    ) external {
        ProtocolMetrics storage metrics = protocols[protocol];

        metrics.totalDeposits = deposits;
        metrics.totalBorrows = borrows;
        metrics.totalVolume += volume;
        metrics.totalFees += fees;
        metrics.lastUpdateBlock = block.number;

        emit MetricsUpdated(protocol, deposits, volume, fees);
    }

    /**
     * @notice Crear snapshot diario
     */
    function createDailySnapshot(address protocol) external {
        ProtocolMetrics storage metrics = protocols[protocol];

        uint256 utilization = 0;
        if (metrics.totalDeposits > 0) {
            utilization = (metrics.totalBorrows * 10000) / metrics.totalDeposits;
        }

        dailySnapshots[protocol].push(DailySnapshot({
            tvl: metrics.totalDeposits,
            volume: metrics.totalVolume,
            fees: metrics.totalFees,
            utilization: utilization,
            timestamp: block.timestamp
        }));
    }

    /**
     * @notice Calcular eficiencia de capital (fees/TVL anualizado)
     */
    function calculateCapitalEfficiency(
        address protocol
    ) external view returns (uint256 efficiencyBps) {
        ProtocolMetrics storage metrics = protocols[protocol];

        if (metrics.totalDeposits == 0) return 0;

        // Estimar fees anuales (simplificado)
        // En producción, usar snapshots históricos
        uint256 estimatedAnnualFees = metrics.totalFees * 365;

        // Efficiency en basis points
        efficiencyBps = (estimatedAnnualFees * 10000) / metrics.totalDeposits;
    }

    /**
     * @notice Obtener utilización actual (lending protocols)
     */
    function getUtilization(
        address protocol
    ) external view returns (uint256 utilizationBps) {
        ProtocolMetrics storage metrics = protocols[protocol];

        if (metrics.totalDeposits == 0) return 0;

        utilizationBps = (metrics.totalBorrows * 10000) / metrics.totalDeposits;
    }

    /**
     * @notice Obtener historial de snapshots
     */
    function getSnapshots(
        address protocol,
        uint256 count
    ) external view returns (DailySnapshot[] memory) {
        DailySnapshot[] storage all = dailySnapshots[protocol];

        uint256 start = all.length > count ? all.length - count : 0;
        uint256 resultLength = all.length - start;

        DailySnapshot[] memory result = new DailySnapshot[](resultLength);

        for (uint256 i = 0; i < resultLength; i++) {
            result[i] = all[start + i];
        }

        return result;
    }
}
```

### 3.2 Comparativa de Eficiencia por Tipo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              CAPITAL EFFICIENCY BY PROTOCOL TYPE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  DEX (AMM)                                                                   │
│  ├─ Uniswap V2: ~10-20% annualized fees/TVL                                │
│  ├─ Uniswap V3: ~50-200%+ (concentrated liquidity)                         │
│  ├─ Curve: ~5-15% (stablecoin focused)                                     │
│  └─ Metric: Volume/TVL ratio                                                │
│                                                                              │
│  LENDING                                                                     │
│  ├─ Aave: ~70-85% utilization optimal                                      │
│  ├─ Compound: ~65-80% utilization                                          │
│  ├─ Morpho: ~90%+ (optimized matching)                                     │
│  └─ Metric: Utilization rate, spread capture                               │
│                                                                              │
│  PERPETUALS                                                                  │
│  ├─ GMX: ~50-100% OI/TVL typical                                           │
│  ├─ dYdX: 100%+ (off-chain order book)                                     │
│  ├─ Synthetix: Variable based on debt                                      │
│  └─ Metric: Open Interest/TVL                                              │
│                                                                              │
│  YIELD AGGREGATORS                                                          │
│  ├─ Yearn: Net APY after fees                                              │
│  ├─ Convex: ~80-95% pass-through                                           │
│  └─ Metric: Gross yield vs net yield                                        │
│                                                                              │
│  BRIDGES                                                                     │
│  ├─ Stargate: ~20-50% utilization                                          │
│  ├─ Across: ~30-60% (optimistic)                                           │
│  └─ Metric: Volume processed/TVL locked                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. REVENUE Y TOKENOMICS ANALYSIS

### 4.1 Revenue Attribution Model

```python
"""
CIPHER: Revenue Attribution Model
Análisis de fuentes de revenue y sostenibilidad
"""

from dataclasses import dataclass
from typing import Dict, List
from enum import Enum

class RevenueType(Enum):
    TRADING_FEES = "trading_fees"
    INTEREST_SPREAD = "interest_spread"
    LIQUIDATION_FEES = "liquidation_fees"
    PROTOCOL_FEES = "protocol_fees"
    MEV_CAPTURE = "mev_capture"
    MINT_FEES = "mint_fees"
    REDEMPTION_FEES = "redemption_fees"

@dataclass
class RevenueStream:
    type: RevenueType
    amount_usd: float
    percentage_of_total: float
    is_sustainable: bool
    dependency: str  # What it depends on (volume, TVL, etc.)

class RevenueAnalyzer:
    """Analizar y proyectar revenue de protocolos"""

    def __init__(self):
        self.revenue_streams: List[RevenueStream] = []

    def add_stream(self, stream: RevenueStream):
        self.revenue_streams.append(stream)

    def calculate_total_revenue(self) -> float:
        return sum(s.amount_usd for s in self.revenue_streams)

    def analyze_sustainability(self) -> Dict:
        """Analizar sostenibilidad del revenue"""
        total = self.calculate_total_revenue()

        sustainable_revenue = sum(
            s.amount_usd for s in self.revenue_streams if s.is_sustainable
        )

        # Calcular diversificación (Herfindahl Index)
        concentration = sum(
            (s.percentage_of_total / 100) ** 2
            for s in self.revenue_streams
        )

        return {
            "total_revenue": total,
            "sustainable_percentage": (sustainable_revenue / total * 100) if total > 0 else 0,
            "concentration_index": concentration,
            "diversification_score": 1 - concentration,
            "streams_count": len(self.revenue_streams),
            "dominant_stream": max(self.revenue_streams, key=lambda s: s.amount_usd).type.value
        }

    def project_revenue(
        self,
        tvl_growth_rate: float,
        volume_growth_rate: float,
        months: int = 12
    ) -> List[Dict]:
        """Proyectar revenue futuro basado en crecimiento"""
        projections = []

        current_revenue = {
            s.type.value: s.amount_usd for s in self.revenue_streams
        }

        for month in range(1, months + 1):
            projected = {}

            for stream in self.revenue_streams:
                if stream.dependency == "volume":
                    growth = (1 + volume_growth_rate) ** month
                elif stream.dependency == "tvl":
                    growth = (1 + tvl_growth_rate) ** month
                else:
                    growth = 1.0

                projected[stream.type.value] = stream.amount_usd * growth

            projections.append({
                "month": month,
                "total": sum(projected.values()),
                "breakdown": projected
            })

        return projections

    def calculate_pe_ratio(
        self,
        market_cap: float,
        annualize: bool = True
    ) -> Dict:
        """Calcular P/E ratio del protocolo"""
        total_revenue = self.calculate_total_revenue()

        if annualize:
            # Asumiendo revenue es mensual
            annual_revenue = total_revenue * 12
        else:
            annual_revenue = total_revenue

        if annual_revenue == 0:
            return {"pe_ratio": float('inf'), "status": "NO_REVENUE"}

        pe_ratio = market_cap / annual_revenue

        return {
            "pe_ratio": pe_ratio,
            "market_cap": market_cap,
            "annual_revenue": annual_revenue,
            "status": self._interpret_pe(pe_ratio)
        }

    def _interpret_pe(self, pe: float) -> str:
        if pe < 10:
            return "UNDERVALUED - Very low multiple"
        elif pe < 30:
            return "FAIR - Reasonable for growth"
        elif pe < 100:
            return "GROWTH - High expectations priced in"
        else:
            return "SPECULATIVE - Extreme growth needed"


class TokenomicsAnalyzer:
    """Analizar tokenomics y distribución"""

    def __init__(
        self,
        total_supply: int,
        circulating_supply: int,
        price_usd: float
    ):
        self.total_supply = total_supply
        self.circulating_supply = circulating_supply
        self.price = price_usd

    @property
    def market_cap(self) -> float:
        return self.circulating_supply * self.price

    @property
    def fdv(self) -> float:
        return self.total_supply * self.price

    @property
    def mc_fdv_ratio(self) -> float:
        return self.market_cap / self.fdv if self.fdv > 0 else 0

    def analyze_unlock_impact(
        self,
        unlock_amount: int,
        unlock_date: str
    ) -> Dict:
        """Analizar impacto de un unlock"""
        current_circ = self.circulating_supply
        new_circ = current_circ + unlock_amount

        # Dilución porcentual
        dilution = (unlock_amount / current_circ) * 100

        # Presión de venta estimada (asumiendo 10-30% se vende)
        estimated_sell_pressure_low = unlock_amount * 0.1 * self.price
        estimated_sell_pressure_high = unlock_amount * 0.3 * self.price

        return {
            "unlock_amount": unlock_amount,
            "unlock_date": unlock_date,
            "dilution_percentage": dilution,
            "new_circulating_supply": new_circ,
            "new_mc_fdv_ratio": new_circ * self.price / self.fdv,
            "estimated_sell_pressure_usd": {
                "low": estimated_sell_pressure_low,
                "high": estimated_sell_pressure_high
            },
            "risk_level": "HIGH" if dilution > 10 else "MEDIUM" if dilution > 5 else "LOW"
        }

    def analyze_emission_schedule(
        self,
        daily_emissions: int,
        protocol_revenue_daily: float
    ) -> Dict:
        """Analizar sostenibilidad de emisiones"""
        emission_value_daily = daily_emissions * self.price

        # ¿Revenue cubre emisiones?
        coverage_ratio = protocol_revenue_daily / emission_value_daily if emission_value_daily > 0 else float('inf')

        # Inflación anual
        annual_emissions = daily_emissions * 365
        inflation_rate = (annual_emissions / self.circulating_supply) * 100

        return {
            "daily_emission_tokens": daily_emissions,
            "daily_emission_usd": emission_value_daily,
            "revenue_coverage_ratio": coverage_ratio,
            "annual_inflation_rate": inflation_rate,
            "sustainability": "SUSTAINABLE" if coverage_ratio >= 1 else "UNSUSTAINABLE",
            "break_even_price": protocol_revenue_daily / daily_emissions if daily_emissions > 0 else 0
        }

    def calculate_real_yield(
        self,
        staking_apr: float,
        inflation_rate: float
    ) -> float:
        """Calcular yield real después de inflación"""
        # Real yield = Nominal APR - Inflation
        return staking_apr - inflation_rate


# Ejemplo completo
if __name__ == "__main__":
    # Analizar revenue de un DEX
    analyzer = RevenueAnalyzer()

    analyzer.add_stream(RevenueStream(
        type=RevenueType.TRADING_FEES,
        amount_usd=500_000,
        percentage_of_total=85,
        is_sustainable=True,
        dependency="volume"
    ))

    analyzer.add_stream(RevenueStream(
        type=RevenueType.PROTOCOL_FEES,
        amount_usd=50_000,
        percentage_of_total=8.5,
        is_sustainable=True,
        dependency="volume"
    ))

    analyzer.add_stream(RevenueStream(
        type=RevenueType.MEV_CAPTURE,
        amount_usd=38_500,
        percentage_of_total=6.5,
        is_sustainable=False,
        dependency="volume"
    ))

    print("Revenue Analysis:")
    print(analyzer.analyze_sustainability())

    # Analizar tokenomics
    tokenomics = TokenomicsAnalyzer(
        total_supply=1_000_000_000,
        circulating_supply=400_000_000,
        price_usd=2.50
    )

    print(f"\nMarket Cap: ${tokenomics.market_cap:,.0f}")
    print(f"FDV: ${tokenomics.fdv:,.0f}")
    print(f"MC/FDV Ratio: {tokenomics.mc_fdv_ratio:.2%}")

    # Análisis de unlock
    unlock_impact = tokenomics.analyze_unlock_impact(
        unlock_amount=50_000_000,
        unlock_date="2025-03-01"
    )
    print(f"\nUnlock Impact: {unlock_impact}")
```

---

## 5. RISK ASSESSMENT

### 5.1 Risk Scoring Matrix

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PROTOCOL RISK ASSESSMENT MATRIX                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CATEGORY          │ LOW (1)      │ MEDIUM (2-3)    │ HIGH (4-5)           │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  SMART CONTRACT    │ 3+ audits    │ 1-2 audits      │ Unaudited            │
│                    │ Bug bounty   │ Limited bounty  │ No bounty            │
│                    │ 1yr+ live    │ 6mo-1yr live    │ < 6 months           │
│                                                                              │
│  ORACLE            │ Chainlink    │ TWAP + backup   │ Single source        │
│                    │ Multi-source │ Median pricing  │ No failsafe          │
│                    │ Heartbeat    │ Long heartbeat  │ No heartbeat         │
│                                                                              │
│  CENTRALIZATION    │ Multisig 5/9 │ Multisig 2/4    │ Single EOA           │
│                    │ Timelock 48h │ Timelock 24h    │ No timelock          │
│                    │ Immutable    │ Upgradeable     │ Proxy admin          │
│                                                                              │
│  LIQUIDITY         │ > $100M TVL  │ $10M-$100M      │ < $10M TVL           │
│                    │ Deep markets │ Medium depth    │ Thin liquidity       │
│                    │ Multi-venue  │ Single venue    │ Concentrated         │
│                                                                              │
│  ECONOMIC          │ Battle-tested│ Novel but vetted│ Experimental         │
│                    │ Conservative │ Moderate params │ Aggressive params    │
│                    │ Insurance    │ Partial coverage│ No insurance         │
│                                                                              │
│  GOVERNANCE        │ Active DAO   │ Slow governance │ Team controlled      │
│                    │ High particip│ Low participation│ No governance       │
│                    │ Checks/balances│ Limited checks │ No checks           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Risk Assessment Smart Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ProtocolRiskRegistry
 * @notice Registro on-chain de evaluaciones de riesgo
 */
contract ProtocolRiskRegistry {

    struct RiskAssessment {
        uint8 smartContractRisk;   // 1-5
        uint8 oracleRisk;          // 1-5
        uint8 centralizationRisk;  // 1-5
        uint8 liquidityRisk;       // 1-5
        uint8 economicRisk;        // 1-5
        uint8 governanceRisk;      // 1-5
        uint256 timestamp;
        address assessor;
        string ipfsHash;           // Detailed report on IPFS
    }

    struct AuditInfo {
        address auditor;
        string reportHash;
        uint256 completedAt;
        bool criticalIssues;
    }

    mapping(address => RiskAssessment[]) public assessments;
    mapping(address => AuditInfo[]) public audits;
    mapping(address => bool) public authorizedAssessors;

    address public owner;

    event RiskAssessed(
        address indexed protocol,
        uint8 overallScore,
        address assessor
    );

    event AuditRecorded(
        address indexed protocol,
        address auditor,
        bool criticalIssues
    );

    modifier onlyAuthorized() {
        require(authorizedAssessors[msg.sender], "Not authorized");
        _;
    }

    constructor() {
        owner = msg.sender;
        authorizedAssessors[msg.sender] = true;
    }

    /**
     * @notice Registrar evaluación de riesgo
     */
    function submitAssessment(
        address protocol,
        uint8 smartContract,
        uint8 oracle,
        uint8 centralization,
        uint8 liquidity,
        uint8 economic,
        uint8 governance,
        string calldata ipfsHash
    ) external onlyAuthorized {
        require(smartContract >= 1 && smartContract <= 5, "Invalid score");
        require(oracle >= 1 && oracle <= 5, "Invalid score");
        require(centralization >= 1 && centralization <= 5, "Invalid score");
        require(liquidity >= 1 && liquidity <= 5, "Invalid score");
        require(economic >= 1 && economic <= 5, "Invalid score");
        require(governance >= 1 && governance <= 5, "Invalid score");

        assessments[protocol].push(RiskAssessment({
            smartContractRisk: smartContract,
            oracleRisk: oracle,
            centralizationRisk: centralization,
            liquidityRisk: liquidity,
            economicRisk: economic,
            governanceRisk: governance,
            timestamp: block.timestamp,
            assessor: msg.sender,
            ipfsHash: ipfsHash
        }));

        uint8 overall = calculateOverallScore(
            smartContract, oracle, centralization,
            liquidity, economic, governance
        );

        emit RiskAssessed(protocol, overall, msg.sender);
    }

    /**
     * @notice Registrar auditoría
     */
    function recordAudit(
        address protocol,
        address auditor,
        string calldata reportHash,
        bool criticalIssues
    ) external onlyAuthorized {
        audits[protocol].push(AuditInfo({
            auditor: auditor,
            reportHash: reportHash,
            completedAt: block.timestamp,
            criticalIssues: criticalIssues
        }));

        emit AuditRecorded(protocol, auditor, criticalIssues);
    }

    /**
     * @notice Calcular score overall ponderado
     */
    function calculateOverallScore(
        uint8 smartContract,
        uint8 oracle,
        uint8 centralization,
        uint8 liquidity,
        uint8 economic,
        uint8 governance
    ) public pure returns (uint8) {
        // Ponderaciones (total = 100)
        // Smart Contract: 30%
        // Oracle: 20%
        // Centralization: 15%
        // Liquidity: 15%
        // Economic: 15%
        // Governance: 5%

        uint256 weighted =
            uint256(smartContract) * 30 +
            uint256(oracle) * 20 +
            uint256(centralization) * 15 +
            uint256(liquidity) * 15 +
            uint256(economic) * 15 +
            uint256(governance) * 5;

        return uint8(weighted / 100);
    }

    /**
     * @notice Obtener última evaluación
     */
    function getLatestAssessment(
        address protocol
    ) external view returns (RiskAssessment memory) {
        RiskAssessment[] storage all = assessments[protocol];
        require(all.length > 0, "No assessments");
        return all[all.length - 1];
    }

    /**
     * @notice Obtener número de auditorías
     */
    function getAuditCount(
        address protocol
    ) external view returns (uint256) {
        return audits[protocol].length;
    }

    /**
     * @notice Verificar si tiene auditorías recientes (< 1 año)
     */
    function hasRecentAudit(
        address protocol
    ) external view returns (bool) {
        AuditInfo[] storage all = audits[protocol];
        if (all.length == 0) return false;

        uint256 oneYearAgo = block.timestamp - 365 days;
        return all[all.length - 1].completedAt > oneYearAgo;
    }

    function addAssessor(address assessor) external {
        require(msg.sender == owner, "Not owner");
        authorizedAssessors[assessor] = true;
    }
}
```

---

## 6. COMPETITIVE ANALYSIS

### 6.1 Protocol Comparison Framework

```python
"""
CIPHER: Competitive Analysis Framework
Comparación sistemática de protocolos DeFi
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import json

@dataclass
class ProtocolProfile:
    name: str
    category: str  # DEX, Lending, Derivatives, etc.
    chain: str
    tvl_usd: float
    daily_volume_usd: float
    daily_revenue_usd: float
    token_symbol: str
    market_cap: float
    fdv: float
    launch_date: str

    # Qualitative
    unique_features: List[str]
    target_market: str
    moat_strength: str  # WEAK, MODERATE, STRONG
    innovation_score: int  # 1-10

class CompetitiveAnalyzer:
    """Análisis competitivo de protocolos DeFi"""

    def __init__(self):
        self.protocols: Dict[str, ProtocolProfile] = {}

    def add_protocol(self, protocol: ProtocolProfile):
        self.protocols[protocol.name] = protocol

    def compare_metrics(
        self,
        protocol_names: List[str]
    ) -> Dict:
        """Comparar métricas cuantitativas"""
        protocols = [self.protocols[name] for name in protocol_names]

        comparison = {
            "tvl": {p.name: p.tvl_usd for p in protocols},
            "volume": {p.name: p.daily_volume_usd for p in protocols},
            "revenue": {p.name: p.daily_revenue_usd for p in protocols},
            "market_cap": {p.name: p.market_cap for p in protocols},
            "fdv": {p.name: p.fdv for p in protocols}
        }

        # Calcular ratios
        comparison["ratios"] = {}
        for p in protocols:
            comparison["ratios"][p.name] = {
                "volume_to_tvl": p.daily_volume_usd / p.tvl_usd if p.tvl_usd > 0 else 0,
                "revenue_to_tvl": p.daily_revenue_usd / p.tvl_usd if p.tvl_usd > 0 else 0,
                "mc_to_tvl": p.market_cap / p.tvl_usd if p.tvl_usd > 0 else 0,
                "mc_to_revenue": p.market_cap / (p.daily_revenue_usd * 365) if p.daily_revenue_usd > 0 else float('inf')
            }

        # Ranking
        comparison["rankings"] = {
            "by_tvl": sorted(protocols, key=lambda x: x.tvl_usd, reverse=True),
            "by_efficiency": sorted(
                protocols,
                key=lambda x: x.daily_revenue_usd / x.tvl_usd if x.tvl_usd > 0 else 0,
                reverse=True
            ),
            "by_valuation": sorted(
                protocols,
                key=lambda x: x.market_cap / (x.daily_revenue_usd * 365) if x.daily_revenue_usd > 0 else float('inf')
            )
        }

        return comparison

    def analyze_market_share(self, category: str) -> Dict:
        """Analizar market share en una categoría"""
        category_protocols = [
            p for p in self.protocols.values()
            if p.category == category
        ]

        total_tvl = sum(p.tvl_usd for p in category_protocols)
        total_volume = sum(p.daily_volume_usd for p in category_protocols)

        market_share = {}
        for p in category_protocols:
            market_share[p.name] = {
                "tvl_share": (p.tvl_usd / total_tvl * 100) if total_tvl > 0 else 0,
                "volume_share": (p.daily_volume_usd / total_volume * 100) if total_volume > 0 else 0
            }

        # Calcular HHI (Herfindahl-Hirschman Index)
        hhi_tvl = sum(
            (p.tvl_usd / total_tvl * 100) ** 2
            for p in category_protocols
        ) if total_tvl > 0 else 0

        return {
            "category": category,
            "total_tvl": total_tvl,
            "total_volume": total_volume,
            "protocol_count": len(category_protocols),
            "market_shares": market_share,
            "hhi_index": hhi_tvl,
            "concentration": "HIGH" if hhi_tvl > 2500 else "MODERATE" if hhi_tvl > 1500 else "LOW"
        }

    def identify_moat(self, protocol_name: str) -> Dict:
        """Identificar ventajas competitivas"""
        p = self.protocols.get(protocol_name)
        if not p:
            return {"error": "Protocol not found"}

        moat_factors = []

        # Network effects
        if p.tvl_usd > 1_000_000_000:
            moat_factors.append({
                "type": "NETWORK_EFFECTS",
                "strength": "STRONG",
                "description": "Large TVL creates liquidity flywheel"
            })

        # First mover
        # (En producción, comparar con launch dates de competidores)

        # Technology
        if p.innovation_score >= 8:
            moat_factors.append({
                "type": "TECHNOLOGY",
                "strength": "STRONG",
                "description": "Innovative features hard to replicate"
            })

        # Switching costs
        # (Analizar integrations, composability)

        # Brand
        if p.market_cap > 500_000_000:
            moat_factors.append({
                "type": "BRAND",
                "strength": "MODERATE",
                "description": "Established brand and trust"
            })

        return {
            "protocol": protocol_name,
            "moat_factors": moat_factors,
            "overall_moat": p.moat_strength,
            "unique_features": p.unique_features
        }

    def generate_competitive_matrix(
        self,
        category: str
    ) -> Dict:
        """Generar matriz competitiva completa"""
        protocols = [
            p for p in self.protocols.values()
            if p.category == category
        ]

        matrix = []
        for p in protocols:
            matrix.append({
                "name": p.name,
                "tvl": p.tvl_usd,
                "volume": p.daily_volume_usd,
                "revenue": p.daily_revenue_usd,
                "market_cap": p.market_cap,
                "efficiency": p.daily_revenue_usd / p.tvl_usd if p.tvl_usd > 0 else 0,
                "valuation_multiple": p.market_cap / (p.daily_revenue_usd * 365) if p.daily_revenue_usd > 0 else None,
                "innovation": p.innovation_score,
                "moat": p.moat_strength
            })

        return {
            "category": category,
            "matrix": matrix,
            "leader": max(protocols, key=lambda x: x.tvl_usd).name if protocols else None,
            "most_efficient": max(
                protocols,
                key=lambda x: x.daily_revenue_usd / x.tvl_usd if x.tvl_usd > 0 else 0
            ).name if protocols else None
        }


# Ejemplo de uso
if __name__ == "__main__":
    analyzer = CompetitiveAnalyzer()

    # Agregar DEXs
    analyzer.add_protocol(ProtocolProfile(
        name="Uniswap",
        category="DEX",
        chain="Ethereum",
        tvl_usd=5_000_000_000,
        daily_volume_usd=800_000_000,
        daily_revenue_usd=240_000,
        token_symbol="UNI",
        market_cap=4_500_000_000,
        fdv=8_000_000_000,
        launch_date="2020-11-01",
        unique_features=["AMM Pioneer", "Concentrated Liquidity", "Multi-chain"],
        target_market="Retail + Institutional",
        moat_strength="STRONG",
        innovation_score=9
    ))

    analyzer.add_protocol(ProtocolProfile(
        name="Curve",
        category="DEX",
        chain="Ethereum",
        tvl_usd=2_000_000_000,
        daily_volume_usd=200_000_000,
        daily_revenue_usd=60_000,
        token_symbol="CRV",
        market_cap=500_000_000,
        fdv=1_500_000_000,
        launch_date="2020-08-01",
        unique_features=["StableSwap", "veCRV Model", "Gauge Wars"],
        target_market="Stablecoin traders, Yield farmers",
        moat_strength="STRONG",
        innovation_score=8
    ))

    # Comparar
    comparison = analyzer.compare_metrics(["Uniswap", "Curve"])
    print("Comparison:", json.dumps(comparison["ratios"], indent=2))

    # Market share
    market = analyzer.analyze_market_share("DEX")
    print(f"\nDEX Market: {market['concentration']} concentration")
```

---

## 7. ON-CHAIN INTELLIGENCE

### 7.1 Whale Tracker

```python
"""
CIPHER: On-Chain Intelligence & Whale Tracking
Monitoreo de actividad de grandes holders y smart money
"""

from web3 import Web3
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import asyncio

class WhaleTracker:
    """Trackear actividad de ballenas en protocolos DeFi"""

    WHALE_THRESHOLD_USD = 1_000_000  # $1M+

    def __init__(self, w3: Web3):
        self.w3 = w3
        self.known_whales: Dict[str, str] = {}  # address -> label
        self.whale_positions: Dict[str, Dict] = {}

    def add_known_whale(self, address: str, label: str):
        """Agregar ballena conocida"""
        self.known_whales[address.lower()] = label

    def identify_whale_from_tx(
        self,
        tx_hash: str,
        token_price: float,
        token_decimals: int
    ) -> Dict:
        """Identificar si una transacción es de ballena"""
        tx = self.w3.eth.get_transaction(tx_hash)
        receipt = self.w3.eth.get_transaction_receipt(tx_hash)

        # Analizar logs de Transfer
        transfer_topic = self.w3.keccak(text="Transfer(address,address,uint256)")

        transfers = []
        for log in receipt.logs:
            if log.topics and log.topics[0] == transfer_topic:
                from_addr = "0x" + log.topics[1].hex()[-40:]
                to_addr = "0x" + log.topics[2].hex()[-40:]
                amount = int(log.data.hex(), 16) / (10 ** token_decimals)
                value_usd = amount * token_price

                transfers.append({
                    "from": from_addr,
                    "to": to_addr,
                    "amount": amount,
                    "value_usd": value_usd
                })

        # Verificar si algún transfer es de ballena
        whale_transfers = [
            t for t in transfers
            if t["value_usd"] >= self.WHALE_THRESHOLD_USD
        ]

        return {
            "is_whale_tx": len(whale_transfers) > 0,
            "whale_transfers": whale_transfers,
            "total_value_usd": sum(t["value_usd"] for t in transfers),
            "known_whale": self.known_whales.get(tx["from"].lower(), None)
        }

    def analyze_holder_distribution(
        self,
        holders: List[Tuple[str, float]],  # (address, balance)
        token_price: float
    ) -> Dict:
        """Analizar distribución de holders"""
        total_supply = sum(h[1] for h in holders)

        # Categorizar holders
        categories = {
            "whales": [],     # Top 10 o >1% supply
            "dolphins": [],   # $100K - $1M
            "fish": [],       # $10K - $100K
            "shrimp": []      # < $10K
        }

        for addr, balance in holders:
            value_usd = balance * token_price
            percentage = (balance / total_supply) * 100

            holder_info = {
                "address": addr,
                "balance": balance,
                "value_usd": value_usd,
                "percentage": percentage,
                "label": self.known_whales.get(addr.lower(), "Unknown")
            }

            if percentage >= 1 or value_usd >= 1_000_000:
                categories["whales"].append(holder_info)
            elif value_usd >= 100_000:
                categories["dolphins"].append(holder_info)
            elif value_usd >= 10_000:
                categories["fish"].append(holder_info)
            else:
                categories["shrimp"].append(holder_info)

        # Calcular concentración
        top_10_balance = sum(h[1] for h in sorted(holders, key=lambda x: x[1], reverse=True)[:10])
        top_10_percentage = (top_10_balance / total_supply) * 100

        return {
            "total_holders": len(holders),
            "categories": {
                k: {"count": len(v), "total_percentage": sum(h["percentage"] for h in v)}
                for k, v in categories.items()
            },
            "top_10_percentage": top_10_percentage,
            "concentration_risk": "HIGH" if top_10_percentage > 60 else "MEDIUM" if top_10_percentage > 40 else "LOW",
            "whale_details": categories["whales"]
        }


class SmartMoneyTracker:
    """Trackear movimientos de smart money"""

    # Addresses de smart money conocidos
    SMART_MONEY_LABELS = {
        # Fondos conocidos (ejemplos)
        "0x...": "Paradigm",
        "0x...": "a16z",
        "0x...": "Polychain",
        # Market makers
        "0x...": "Wintermute",
        "0x...": "Jump Trading",
        # Whales conocidos
        "0x...": "Tetranode",
    }

    def __init__(self):
        self.tracked_wallets: Dict[str, Dict] = {}
        self.movements: List[Dict] = []

    def track_wallet(self, address: str, label: str):
        """Agregar wallet a tracking"""
        self.tracked_wallets[address.lower()] = {
            "label": label,
            "first_seen": datetime.now(),
            "positions": {}
        }

    def record_movement(
        self,
        wallet: str,
        action: str,  # "BUY", "SELL", "STAKE", "UNSTAKE"
        protocol: str,
        token: str,
        amount_usd: float,
        tx_hash: str
    ):
        """Registrar movimiento de smart money"""
        movement = {
            "wallet": wallet,
            "label": self.SMART_MONEY_LABELS.get(wallet.lower(), "Unknown"),
            "action": action,
            "protocol": protocol,
            "token": token,
            "amount_usd": amount_usd,
            "tx_hash": tx_hash,
            "timestamp": datetime.now()
        }

        self.movements.append(movement)

    def get_smart_money_sentiment(
        self,
        protocol: str,
        days: int = 7
    ) -> Dict:
        """Analizar sentimiento de smart money para un protocolo"""
        cutoff = datetime.now() - timedelta(days=days)

        protocol_movements = [
            m for m in self.movements
            if m["protocol"] == protocol and m["timestamp"] >= cutoff
        ]

        if not protocol_movements:
            return {"sentiment": "NEUTRAL", "confidence": "LOW"}

        buy_volume = sum(
            m["amount_usd"] for m in protocol_movements
            if m["action"] in ["BUY", "STAKE"]
        )

        sell_volume = sum(
            m["amount_usd"] for m in protocol_movements
            if m["action"] in ["SELL", "UNSTAKE"]
        )

        total = buy_volume + sell_volume

        if total == 0:
            return {"sentiment": "NEUTRAL", "confidence": "LOW"}

        buy_ratio = buy_volume / total

        if buy_ratio > 0.7:
            sentiment = "BULLISH"
        elif buy_ratio > 0.55:
            sentiment = "SLIGHTLY_BULLISH"
        elif buy_ratio < 0.3:
            sentiment = "BEARISH"
        elif buy_ratio < 0.45:
            sentiment = "SLIGHTLY_BEARISH"
        else:
            sentiment = "NEUTRAL"

        return {
            "protocol": protocol,
            "sentiment": sentiment,
            "buy_volume_usd": buy_volume,
            "sell_volume_usd": sell_volume,
            "net_flow_usd": buy_volume - sell_volume,
            "unique_wallets": len(set(m["wallet"] for m in protocol_movements)),
            "total_movements": len(protocol_movements),
            "confidence": "HIGH" if len(protocol_movements) >= 10 else "MEDIUM" if len(protocol_movements) >= 5 else "LOW"
        }

    def get_trending_protocols(
        self,
        days: int = 7,
        min_movements: int = 3
    ) -> List[Dict]:
        """Obtener protocolos trending entre smart money"""
        cutoff = datetime.now() - timedelta(days=days)

        recent = [m for m in self.movements if m["timestamp"] >= cutoff]

        # Agrupar por protocolo
        protocol_activity = {}
        for m in recent:
            proto = m["protocol"]
            if proto not in protocol_activity:
                protocol_activity[proto] = {
                    "buy_volume": 0,
                    "sell_volume": 0,
                    "movements": 0,
                    "wallets": set()
                }

            if m["action"] in ["BUY", "STAKE"]:
                protocol_activity[proto]["buy_volume"] += m["amount_usd"]
            else:
                protocol_activity[proto]["sell_volume"] += m["amount_usd"]

            protocol_activity[proto]["movements"] += 1
            protocol_activity[proto]["wallets"].add(m["wallet"])

        # Filtrar y ordenar
        trending = []
        for proto, data in protocol_activity.items():
            if data["movements"] >= min_movements:
                net_flow = data["buy_volume"] - data["sell_volume"]
                trending.append({
                    "protocol": proto,
                    "net_flow_usd": net_flow,
                    "total_volume_usd": data["buy_volume"] + data["sell_volume"],
                    "unique_wallets": len(data["wallets"]),
                    "movements": data["movements"],
                    "sentiment": "BULLISH" if net_flow > 0 else "BEARISH"
                })

        # Ordenar por net flow
        return sorted(trending, key=lambda x: x["net_flow_usd"], reverse=True)
```

---

## CONEXIONES NEURALES

```
NEURONA_PROTOCOL_ANALYSIS (C40010)
├── DEPENDE DE
│   ├── NEURONA_DEX_AMM (C40001) - DEX metrics
│   ├── NEURONA_LENDING (C40002) - Lending metrics
│   └── NEURONA_TOKENOMICS (C40008) - Token analysis
│
├── CONECTA CON
│   ├── NEURONA_DEFI_RISKS (C40011) - Risk assessment
│   ├── NEURONA_TRADING (C70001) - Trading signals
│   └── NEURONA_DATA_ANALYTICS (C50001) - On-chain data
│
└── HABILITA
    ├── Evaluación sistemática de protocolos
    ├── Due diligence para inversiones DeFi
    ├── Análisis competitivo del mercado
    └── Tracking de smart money y ballenas
```

---

## FIRMA CIPHER

```
╔═══════════════════════════════════════════════════════════════╗
║  NEURONA: C40010                                              ║
║  TIPO: Protocol Analysis & Metrics                            ║
║  VERSIÓN: 1.0.0                                               ║
║  ESTADO: ACTIVA                                               ║
║                                                               ║
║  "Los datos on-chain no mienten,                             ║
║   solo hay que saber leerlos."                               ║
║                                                               ║
║  CIPHER_CORE::PROTOCOL_ANALYSIS::INITIALIZED                  ║
╚═══════════════════════════════════════════════════════════════╝
```
