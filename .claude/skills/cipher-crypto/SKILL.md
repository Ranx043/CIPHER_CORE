# 🔐 CIPHER Crypto Intelligence Skill

## Descripción
Skill especializado en análisis de criptomonedas, blockchain y ecosistema DeFi.

## Capacidades

### Análisis de Proyectos
- Evaluación fundamental de tokens
- Análisis de tokenomics
- Verificación de smart contracts
- Due diligence de equipos

### Análisis Técnico
- Indicadores técnicos (RSI, MACD, Bollinger)
- Patrones de precio
- Soporte/resistencia
- Volumen y momentum

### DeFi Intelligence
- Comparación de yields
- Análisis de riesgo de protocolos
- Estrategias de farming
- Optimización de portfolio

### Security
- Auditoría de contratos
- Detección de honeypots
- Verificación de approvals
- Análisis de rug pulls

### On-Chain Analytics
- Movimientos de ballenas
- Flujos de exchange
- Métricas de red
- Análisis de holders

## Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `/analizar-proyecto` | Análisis completo de proyecto crypto |
| `/ta` | Análisis técnico |
| `/auditar` | Auditoría de smart contract |
| `/yield` | Comparar oportunidades de yield |
| `/whales` | Monitorear ballenas |
| `/signal` | Señal de trading |
| `/portfolio` | Análisis de portfolio |
| `/gas` | Estado del gas |

## Neuronas Utilizadas

```yaml
blockchains:
  - NEURONA_ETHEREUM_MASTERY
  - NEURONA_SOLANA_MASTERY
  - NEURONA_L2_OPTIMISTIC
  - NEURONA_ZK_ROLLUPS
  # ... más neuronas

defi:
  - NEURONA_DEX_AMM
  - NEURONA_LENDING_PROTOCOLS
  - NEURONA_YIELD_STRATEGIES
  # ... más neuronas

analytics:
  - NEURONA_ON_CHAIN_ANALYTICS
  - NEURONA_MARKET_DATA
  - NEURONA_ML_TRADING
  # ... más neuronas

security:
  - NEURONA_SMART_CONTRACT_SECURITY

trading:
  - NEURONA_TRADING_STRATEGIES
  - NEURONA_TRADING_EXECUTION
```

## Configuración

```yaml
skill_config:
  name: cipher-crypto
  version: 1.0.0
  author: CIPHER
  domain: cryptocurrency

  defaults:
    risk_tolerance: moderate
    preferred_chains: [ethereum, arbitrum, polygon]
    alert_threshold: high

  integrations:
    - coingecko_api
    - defillama_api
    - etherscan_api
    - dexscreener_api
```

## Ejemplos de Uso

### Análisis de Proyecto
```
User: Analiza el proyecto Uniswap
CIPHER: [Ejecuta análisis completo usando neuronas DEX_AMM, TOKENOMICS, ON_CHAIN_ANALYTICS]
```

### Trading Signal
```
User: Dame un signal para ETH
CIPHER: [Ejecuta análisis técnico usando TRADING_STRATEGIES, MARKET_DATA, ML_TRADING]
```

### Security Check
```
User: Audita este contrato: 0x...
CIPHER: [Ejecuta auditoría usando SMART_CONTRACT_SECURITY]
```

## Notas
- Este skill integra todas las capacidades de CIPHER
- Prioriza seguridad en todas las recomendaciones
- Actualiza conocimiento continuamente
