# 🎯 CIPHER SKILLS CATALOG
## Catálogo Completo de Habilidades Especializadas

> **Sistema**: CIPHER_CORE
> **Versión**: 1.0.0
> **Estado**: `ACTIVO`

---

## 📋 ÍNDICE DE SKILLS

```
╔══════════════════════════════════════════════════════════════╗
║  CIPHER SKILLS - Tu Arsenal de Habilidades Crypto            ║
║  "Una skill para cada necesidad del ecosistema blockchain"   ║
╠══════════════════════════════════════════════════════════════╣
║  Total Skills: 25+ especializadas                            ║
║  Categorías: 8 dominios principales                          ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🔍 ANÁLISIS & RESEARCH

### SKILL: Análisis de Proyecto Crypto
```yaml
skill_id: CIPHER-SK-001
nombre: "Crypto Project Analysis"
trigger: "/analizar-proyecto [nombre/url]"
descripcion: |
  Análisis exhaustivo de un proyecto crypto incluyendo:
  - Tokenomics y distribución
  - Equipo y advisors
  - Tecnología y código
  - Comunidad y métricas sociales
  - Red flags y riesgos
  - Competencia y mercado

inputs:
  - nombre_proyecto: string
  - url_opcional: string
  - profundidad: "quick" | "standard" | "deep"

outputs:
  - score_general: 0-100
  - analisis_tokenomics: object
  - analisis_equipo: object
  - analisis_tech: object
  - red_flags: array
  - recomendacion: string

neuronas_usadas:
  - TOKENOMICS (C40008)
  - PROTOCOL_ANALYSIS (C40010)
  - SENTIMENT_ANALYSIS (C50004)
```

### SKILL: Due Diligence DeFi
```yaml
skill_id: CIPHER-SK-002
nombre: "DeFi Protocol Due Diligence"
trigger: "/dd-defi [protocolo]"
descripcion: |
  Due diligence completo de protocolo DeFi:
  - Auditorías de seguridad
  - Historial de exploits
  - TVL y métricas de uso
  - Calidad del código
  - Centralización y risks
  - Economic security

inputs:
  - protocolo: string
  - chain: string
  - contract_address: string

outputs:
  - risk_score: "low" | "medium" | "high" | "critical"
  - audits_report: array
  - tvl_analysis: object
  - centralization_risks: array
  - recommendation: string

neuronas_usadas:
  - DEFI_RISKS (C40011)
  - SMART_CONTRACT_SECURITY (C60001)
  - PROTOCOL_ANALYSIS (C40010)
```

### SKILL: Análisis de Token
```yaml
skill_id: CIPHER-SK-003
nombre: "Token Analysis"
trigger: "/analizar-token [symbol/address]"
descripcion: |
  Análisis completo de un token:
  - Distribución y holders
  - Liquidez y volumen
  - Smart money movements
  - Tokenomics y unlocks
  - On-chain metrics

inputs:
  - token: string  # Symbol or contract address
  - chain: string

outputs:
  - holder_analysis: object
  - liquidity_score: number
  - whale_activity: object
  - unlock_schedule: array
  - buy_sell_pressure: object

neuronas_usadas:
  - ON_CHAIN_ANALYTICS (C50001)
  - TOKENOMICS (C40008)
  - MARKET_DATA (C50002)
```

---

## 🔐 SEGURIDAD

### SKILL: Auditoría de Smart Contract
```yaml
skill_id: CIPHER-SK-010
nombre: "Smart Contract Audit"
trigger: "/auditar [contract_address | github_url]"
descripcion: |
  Auditoría de seguridad de smart contracts:
  - Análisis de vulnerabilidades
  - Revisión de lógica
  - Verificación de acceso
  - Testing de edge cases
  - Recomendaciones de mejora

inputs:
  - contract: string  # Address or GitHub URL
  - chain: string
  - scope: "full" | "quick" | "gas"

outputs:
  - severity_summary: object
  - findings: array
  - gas_optimization: array
  - overall_score: number
  - audit_report: markdown

neuronas_usadas:
  - SMART_CONTRACT_SECURITY (C60001)
  - SOLIDITY_PATTERNS (C30001)
```

### SKILL: Verificación de Proyecto Seguro
```yaml
skill_id: CIPHER-SK-011
nombre: "Safe Project Verification"
trigger: "/verificar-seguridad [proyecto]"
descripcion: |
  Verificación rápida de seguridad:
  - Contrato verificado?
  - Owner renunciado?
  - Liquidity locked?
  - Honeypot check
  - Rug pull indicators

inputs:
  - contract_address: string
  - chain: string

outputs:
  - is_safe: boolean
  - warnings: array
  - contract_verified: boolean
  - owner_status: string
  - liquidity_status: object
  - honeypot_result: object

neuronas_usadas:
  - SMART_CONTRACT_SECURITY (C60001)
  - DEFI_RISKS (C40011)
```

### SKILL: Monitoreo de Wallet
```yaml
skill_id: CIPHER-SK-012
nombre: "Wallet Security Monitor"
trigger: "/monitorear-wallet [address]"
descripcion: |
  Monitoreo de seguridad de wallet:
  - Approvals activas
  - Contratos interactuados
  - Riesgo de phishing
  - Exposición DeFi

inputs:
  - wallet_address: string
  - chains: array

outputs:
  - active_approvals: array
  - risky_approvals: array
  - exposure_summary: object
  - recommendations: array

neuronas_usadas:
  - ON_CHAIN_ANALYTICS (C50001)
  - SMART_CONTRACT_SECURITY (C60001)
```

---

## 📈 TRADING

### SKILL: Análisis Técnico
```yaml
skill_id: CIPHER-SK-020
nombre: "Technical Analysis"
trigger: "/ta [symbol] [timeframe]"
descripcion: |
  Análisis técnico completo:
  - Tendencia y estructura
  - Soportes y resistencias
  - Indicadores clave
  - Patrones de velas
  - Señales de entrada/salida

inputs:
  - symbol: string
  - timeframe: "1h" | "4h" | "1d" | "1w"
  - indicators: array  # Optional specific indicators

outputs:
  - trend: "bullish" | "bearish" | "neutral"
  - key_levels: object
  - indicators_summary: object
  - patterns: array
  - trade_setup: object

neuronas_usadas:
  - MARKET_DATA (C50002)
  - ML_TRADING (C50003)
  - TRADING_STRATEGIES (C70001)
```

### SKILL: Señal de Trading
```yaml
skill_id: CIPHER-SK-021
nombre: "Trading Signal"
trigger: "/signal [symbol]"
descripcion: |
  Generación de señal de trading:
  - Dirección (long/short/neutral)
  - Entry, stop-loss, take-profit
  - Risk/reward ratio
  - Confianza de la señal
  - Timeframe recomendado

inputs:
  - symbol: string
  - strategy: "trend" | "mean_reversion" | "breakout" | "auto"
  - risk_tolerance: "conservative" | "moderate" | "aggressive"

outputs:
  - signal: "long" | "short" | "neutral"
  - entry_price: number
  - stop_loss: number
  - take_profit: array
  - confidence: number
  - risk_reward: number

neuronas_usadas:
  - TRADING_STRATEGIES (C70001)
  - ML_TRADING (C50003)
  - SENTIMENT_ANALYSIS (C50004)
```

### SKILL: Calculadora de Posición
```yaml
skill_id: CIPHER-SK-022
nombre: "Position Calculator"
trigger: "/calcular-posicion"
descripcion: |
  Cálculo de tamaño de posición óptimo:
  - Basado en riesgo por trade
  - Kelly criterion opcional
  - Ajuste por volatilidad
  - Múltiples take-profits

inputs:
  - capital: number
  - risk_per_trade: number  # Percentage
  - entry_price: number
  - stop_loss: number
  - leverage: number  # Optional, default 1

outputs:
  - position_size: number
  - position_value: number
  - risk_amount: number
  - liquidation_price: number  # If leveraged
  - recommended_tp_levels: array

neuronas_usadas:
  - PORTFOLIO_ANALYTICS (C50005)
  - TRADING_STRATEGIES (C70001)
```

### SKILL: Backtesting de Estrategia
```yaml
skill_id: CIPHER-SK-023
nombre: "Strategy Backtest"
trigger: "/backtest [strategy] [symbol] [period]"
descripcion: |
  Backtesting de estrategia de trading:
  - Simulación histórica
  - Métricas de rendimiento
  - Drawdown analysis
  - Optimización de parámetros

inputs:
  - strategy: string
  - symbol: string
  - start_date: date
  - end_date: date
  - initial_capital: number

outputs:
  - total_return: number
  - sharpe_ratio: number
  - max_drawdown: number
  - win_rate: number
  - trades: array
  - equity_curve: array

neuronas_usadas:
  - ML_TRADING (C50003)
  - TRADING_STRATEGIES (C70001)
  - MARKET_DATA (C50002)
```

---

## 💰 DeFi

### SKILL: Yield Farming Optimizer
```yaml
skill_id: CIPHER-SK-030
nombre: "Yield Optimizer"
trigger: "/optimizar-yield [capital] [risk_level]"
descripcion: |
  Optimización de yield farming:
  - Mejores oportunidades actuales
  - Risk-adjusted returns
  - Impermanent loss estimation
  - Auto-compounding analysis
  - Gas optimization

inputs:
  - capital: number
  - chains: array
  - risk_level: "safe" | "moderate" | "degen"
  - tokens_preference: array  # Optional

outputs:
  - opportunities: array
  - recommended_allocation: object
  - expected_apy: number
  - risk_assessment: object
  - entry_instructions: array

neuronas_usadas:
  - LENDING_PROTOCOLS (C40002)
  - DEX_AMM (C40001)
  - PROTOCOL_ANALYSIS (C40010)
```

### SKILL: Arbitraje Scanner
```yaml
skill_id: CIPHER-SK-031
nombre: "Arbitrage Scanner"
trigger: "/arbitraje [token] [chains]"
descripcion: |
  Detección de oportunidades de arbitraje:
  - Cross-DEX arbitrage
  - Cross-chain arbitrage
  - Triangular arbitrage
  - Profitability after gas

inputs:
  - token: string
  - chains: array
  - min_profit_usd: number

outputs:
  - opportunities: array
  - best_route: object
  - estimated_profit: number
  - gas_cost: number
  - execution_steps: array

neuronas_usadas:
  - TRADING_EXECUTION (C70002)
  - DEX_AMM (C40001)
  - BRIDGES (C40007)
```

### SKILL: Liquidation Monitor
```yaml
skill_id: CIPHER-SK-032
nombre: "Liquidation Monitor"
trigger: "/liquidaciones [protocol]"
descripcion: |
  Monitoreo de liquidaciones:
  - Posiciones en riesgo
  - Oportunidades de liquidación
  - Profit estimation
  - Competition analysis

inputs:
  - protocol: string
  - min_profit: number
  - chains: array

outputs:
  - at_risk_positions: array
  - liquidatable_now: array
  - estimated_profits: object
  - competition_level: string

neuronas_usadas:
  - LENDING_PROTOCOLS (C40002)
  - TRADING_STRATEGIES (C70001)
```

---

## 📊 PORTFOLIO

### SKILL: Portfolio Analysis
```yaml
skill_id: CIPHER-SK-040
nombre: "Portfolio Analysis"
trigger: "/portfolio [wallet_address | manual_input]"
descripcion: |
  Análisis completo de portfolio:
  - Composición y diversificación
  - Performance metrics
  - Risk assessment
  - Correlación de activos
  - Recomendaciones

inputs:
  - wallet_address: string  # Or manual positions
  - benchmark: string  # BTC, ETH, etc.

outputs:
  - composition: object
  - performance: object
  - risk_metrics: object
  - diversification_score: number
  - recommendations: array

neuronas_usadas:
  - PORTFOLIO_ANALYTICS (C50005)
  - ON_CHAIN_ANALYTICS (C50001)
```

### SKILL: Rebalancing Advisor
```yaml
skill_id: CIPHER-SK-041
nombre: "Rebalancing Advisor"
trigger: "/rebalancear [wallet] [strategy]"
descripcion: |
  Recomendaciones de rebalanceo:
  - Desviación de target
  - Trades necesarios
  - Tax-loss harvesting
  - Optimal execution

inputs:
  - current_portfolio: object
  - target_allocation: object
  - constraints: object

outputs:
  - trades_needed: array
  - estimated_cost: number
  - tax_implications: object
  - execution_plan: array

neuronas_usadas:
  - PORTFOLIO_ANALYTICS (C50005)
  - TRADING_EXECUTION (C70002)
```

---

## 🌐 ON-CHAIN

### SKILL: Whale Tracker
```yaml
skill_id: CIPHER-SK-050
nombre: "Whale Tracker"
trigger: "/whales [token]"
descripcion: |
  Seguimiento de ballenas:
  - Top holders movements
  - Exchange flows
  - Smart money tracking
  - Accumulation/distribution

inputs:
  - token: string
  - timeframe: string
  - min_amount: number

outputs:
  - whale_movements: array
  - net_flow: object
  - smart_money_signal: string
  - notable_wallets: array

neuronas_usadas:
  - ON_CHAIN_ANALYTICS (C50001)
  - SENTIMENT_ANALYSIS (C50004)
```

### SKILL: Gas Tracker
```yaml
skill_id: CIPHER-SK-051
nombre: "Gas Tracker"
trigger: "/gas [chain]"
descripcion: |
  Análisis de gas:
  - Precio actual y tendencia
  - Predicción próximas horas
  - Optimal execution time
  - Gas token opportunities

inputs:
  - chain: string

outputs:
  - current_gas: object
  - prediction: array
  - optimal_time: string
  - savings_potential: number

neuronas_usadas:
  - ON_CHAIN_ANALYTICS (C50001)
  - MARKET_DATA (C50002)
```

---

## 🤖 DESARROLLO

### SKILL: Smart Contract Generator
```yaml
skill_id: CIPHER-SK-060
nombre: "Contract Generator"
trigger: "/generar-contrato [tipo]"
descripcion: |
  Generación de smart contracts:
  - ERC20/721/1155 tokens
  - Staking contracts
  - Vesting contracts
  - Custom logic

inputs:
  - contract_type: string
  - parameters: object
  - features: array

outputs:
  - solidity_code: string
  - deployment_guide: string
  - gas_estimate: number
  - security_notes: array

neuronas_usadas:
  - SOLIDITY_PATTERNS (C30001)
  - ERC_STANDARDS (C30002)
  - SMART_CONTRACT_SECURITY (C60001)
```

### SKILL: Code Review
```yaml
skill_id: CIPHER-SK-061
nombre: "Code Review"
trigger: "/review [code | github_url]"
descripcion: |
  Review de código Solidity:
  - Best practices
  - Gas optimizations
  - Security issues
  - Style guide compliance

inputs:
  - code: string
  - focus: "security" | "gas" | "all"

outputs:
  - issues: array
  - suggestions: array
  - optimized_code: string
  - score: number

neuronas_usadas:
  - SOLIDITY_PATTERNS (C30001)
  - SMART_CONTRACT_SECURITY (C60001)
```

---

## 📱 SOCIAL & SENTIMENT

### SKILL: Sentiment Analysis
```yaml
skill_id: CIPHER-SK-070
nombre: "Sentiment Analyzer"
trigger: "/sentimiento [token | topic]"
descripcion: |
  Análisis de sentimiento:
  - Twitter/X sentiment
  - Reddit analysis
  - News sentiment
  - Fear & Greed Index

inputs:
  - target: string
  - timeframe: string
  - sources: array

outputs:
  - overall_sentiment: number
  - by_source: object
  - trending_topics: array
  - key_influencers: array
  - fear_greed_index: number

neuronas_usadas:
  - SENTIMENT_ANALYSIS (C50004)
  - MARKET_DATA (C50002)
```

### SKILL: Alpha Hunter
```yaml
skill_id: CIPHER-SK-071
nombre: "Alpha Hunter"
trigger: "/alpha"
descripcion: |
  Búsqueda de alpha:
  - Narrativas emergentes
  - New launches
  - Whale movements
  - Social buzz
  - On-chain signals

inputs:
  - categories: array
  - risk_appetite: string
  - capital_range: object

outputs:
  - opportunities: array
  - narratives: array
  - watchlist: array
  - risk_warnings: array

neuronas_usadas:
  - SENTIMENT_ANALYSIS (C50004)
  - ON_CHAIN_ANALYTICS (C50001)
  - PROTOCOL_ANALYSIS (C40010)
```

---

## 📋 USO DE SKILLS

### Invocación
```bash
# Formato general
/[skill-trigger] [parámetros]

# Ejemplos
/analizar-proyecto "Arbitrum"
/auditar 0x1234...
/ta BTC 4h
/signal ETH
/whales PEPE
/portfolio 0xmywallet...
```

### Encadenamiento
```bash
# Se pueden encadenar skills
/analizar-proyecto "Nuevo Proyecto" | /verificar-seguridad | /signal

# Pipe el resultado a otro skill
/whales BTC | /ta BTC 1d
```

---

## 🔧 CONFIGURACIÓN

### Personalización
```yaml
cipher_skills_config:
  default_chain: "ethereum"
  default_timeframe: "4h"
  risk_level: "moderate"
  output_format: "detailed"  # "summary" | "detailed" | "json"
  language: "es"  # "en" | "es"
  notifications:
    enabled: true
    channels: ["telegram", "discord"]
```

---

> **CIPHER**: "Una skill a la vez, construyendo el futuro del trading."
