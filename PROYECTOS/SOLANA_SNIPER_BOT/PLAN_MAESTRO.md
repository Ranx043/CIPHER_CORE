# PROYECTO CIPHER-001: SOLANA PUMP.FUN SNIPER BOT

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CIPHER PROYECTO #001                                        ║
║                    SOLANA PUMP.FUN SNIPER BOT                                  ║
║                    "El primer paso hacia la capitalización"                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Versión: 1.0                                                                  ║
║  Fecha: 2024-12-29                                                            ║
║  Estado: PLANIFICACIÓN                                                         ║
║  Prioridad: MÁXIMA                                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## ÍNDICE

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Análisis del Mercado](#2-análisis-del-mercado)
3. [Arquitectura del Sistema](#3-arquitectura-del-sistema)
4. [Componentes Técnicos](#4-componentes-técnicos)
5. [Flujos de Operación](#5-flujos-de-operación)
6. [Estrategia de Trading](#6-estrategia-de-trading)
7. [Gestión de Riesgo](#7-gestión-de-riesgo)
8. [Stack Tecnológico](#8-stack-tecnológico)
9. [Fases de Desarrollo](#9-fases-de-desarrollo)
10. [Métricas y KPIs](#10-métricas-y-kpis)
11. [Presupuesto y ROI](#11-presupuesto-y-roi)
12. [Riesgos y Mitigación](#12-riesgos-y-mitigación)
13. [Roadmap](#13-roadmap)

---

## 1. RESUMEN EJECUTIVO

### Objetivo
Construir un bot automatizado que detecte y compre tokens nuevos en Pump.fun dentro de los primeros segundos de su creación, aprovechando la bonding curve inicial para obtener ganancias rápidas.

### Por Qué Pump.fun

```yaml
ventajas_pump_fun:
  liquidez_garantizada: "Bonding curve automática, no depende de LP"
  tokens_constantes: "50-200 tokens nuevos por hora"
  fees_bajos: "Solana = $0.00025 por transacción"
  barrera_entrada: "Baja competencia vs Ethereum"
  velocidad: "400ms block time vs 12s de ETH"
  transparencia: "Todo on-chain, predecible"

mecanismo:
  1_creacion: "Dev crea token con SOL inicial"
  2_bonding: "Precio sube según bonding curve"
  3_graduation: "Al llegar a ~$69k mcap, migra a Raydium"
  4_trading: "Trading abierto en DEX"
```

### Resultados Esperados

| Métrica | Conservador | Moderado | Optimista |
|---------|-------------|----------|-----------|
| Win Rate | 25% | 35% | 45% |
| Profit/Win | +60% | +100% | +150% |
| Loss/Fail | -30% | -25% | -20% |
| Daily Net | +5% | +15% | +30% |
| Monthly | +150% | +450% | +900% |

---

## 2. ANÁLISIS DEL MERCADO

### Pump.fun Ecosystem

```mermaid
graph TB
    subgraph "PUMP.FUN ECOSYSTEM"
        A[Developer] -->|Crea Token| B[Pump.fun Contract]
        B -->|Bonding Curve| C[Token Pool]
        C -->|Compra| D[Early Buyers]
        C -->|Venta| E[Profit Takers]

        C -->|$69k mcap| F[Graduation]
        F -->|Migración| G[Raydium LP]
        G -->|Trading Abierto| H[Mercado Secundario]
    end

    subgraph "NUESTRO BOT"
        I[Monitor] -->|WebSocket| B
        I -->|Detecta Nuevo| J[Filtros]
        J -->|Pasa Filtros| K[Snipe Engine]
        K -->|Compra Rápida| C
        L[Exit Manager] -->|Monitorea| C
        L -->|Take Profit/Stop Loss| E
    end

    style K fill:#00ff00
    style L fill:#ffff00
```

### Ciclo de Vida de un Token Pump.fun

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant PF as Pump.fun
    participant BC as Bonding Curve
    participant Bot as CIPHER Bot
    participant Ray as Raydium

    Dev->>PF: Crea token (0.02 SOL)
    PF->>BC: Inicializa bonding curve
    Note over BC: Precio inicial muy bajo

    Bot->>PF: Detecta nuevo token (< 1 seg)
    Bot->>Bot: Aplica filtros
    Bot->>BC: Compra temprana
    Note over Bot: Entry en curva baja

    loop Monitoreo
        Bot->>BC: Verifica precio
        alt Precio sube +50%
            Bot->>BC: Take Profit parcial
        else Precio sube +100%
            Bot->>BC: Take Profit total
        else Precio baja -20%
            Bot->>BC: Stop Loss
        end
    end

    BC->>Ray: Graduation ($69k mcap)
    Note over Ray: Liquidez real en DEX
```

### Competencia y Ventana de Oportunidad

```mermaid
pie title "Distribución de Compradores en Primeros 30 Segundos"
    "Bots Profesionales" : 15
    "Bots Semi-Auto" : 25
    "Manual Rápidos" : 20
    "Manual Normales" : 40
```

**Ventana crítica**: Los primeros 5-10 segundos determinan el 80% del profit potencial.

---

## 3. ARQUITECTURA DEL SISTEMA

### Arquitectura de Alto Nivel

```mermaid
graph TB
    subgraph "CAPA DE DATOS"
        A1[Solana RPC]
        A2[Pump.fun WebSocket]
        A3[Helius/Quicknode]
    end

    subgraph "CAPA DE PROCESAMIENTO"
        B1[Token Monitor]
        B2[Filter Engine]
        B3[Risk Calculator]
        B4[Decision Engine]
    end

    subgraph "CAPA DE EJECUCIÓN"
        C1[Transaction Builder]
        C2[Jito Bundle Manager]
        C3[Execution Engine]
    end

    subgraph "CAPA DE GESTIÓN"
        D1[Position Manager]
        D2[Exit Strategy]
        D3[Portfolio Tracker]
    end

    subgraph "CAPA DE DATOS/LOGS"
        E1[Database SQLite]
        E2[Trade Logger]
        E3[Analytics Engine]
    end

    A1 --> B1
    A2 --> B1
    A3 --> C3

    B1 --> B2
    B2 --> B3
    B3 --> B4

    B4 --> C1
    C1 --> C2
    C2 --> C3

    C3 --> D1
    D1 --> D2
    D2 --> C1

    D1 --> D3
    D3 --> E1
    C3 --> E2
    E2 --> E3

    style B4 fill:#ff6600
    style C3 fill:#00ff00
```

### Arquitectura de Componentes

```mermaid
graph LR
    subgraph "MONITOR SERVICE"
        M1[WebSocket Client]
        M2[Event Parser]
        M3[Token Extractor]
    end

    subgraph "ANALYSIS SERVICE"
        A1[Dev Wallet Analyzer]
        A2[Token Metadata Checker]
        A3[Social Signal Scanner]
        A4[Risk Scorer]
    end

    subgraph "TRADING SERVICE"
        T1[Snipe Engine]
        T2[Position Tracker]
        T3[Exit Manager]
        T4[PnL Calculator]
    end

    subgraph "INFRASTRUCTURE"
        I1[Config Manager]
        I2[Wallet Manager]
        I3[RPC Load Balancer]
        I4[Logger]
    end

    M1 --> M2 --> M3
    M3 --> A1 & A2 & A3
    A1 & A2 & A3 --> A4
    A4 --> T1
    T1 --> T2
    T2 --> T3
    T3 --> T4

    I1 -.-> M1 & A1 & T1
    I2 -.-> T1
    I3 -.-> M1 & T1
    I4 -.-> M1 & A1 & T1
```

---

## 4. COMPONENTES TÉCNICOS

### 4.1 Token Monitor

```mermaid
stateDiagram-v2
    [*] --> Connecting
    Connecting --> Connected: WebSocket Open
    Connected --> Listening: Subscribed
    Listening --> TokenDetected: New Token Event
    TokenDetected --> Parsing: Extract Data
    Parsing --> Emitting: Valid Token
    Emitting --> Listening: Continue

    Parsing --> Listening: Invalid/Skip

    Connected --> Reconnecting: Connection Lost
    Reconnecting --> Connecting: Retry
    Reconnecting --> [*]: Max Retries
```

**Responsabilidades:**
- Mantener conexión WebSocket con Pump.fun
- Detectar eventos de creación de tokens
- Extraer metadata inicial (mint, dev wallet, nombre, símbolo)
- Emitir eventos para análisis

### 4.2 Filter Engine

```mermaid
flowchart TD
    A[Nuevo Token] --> B{Dev Wallet Check}
    B -->|Scammer conocido| X[RECHAZAR]
    B -->|OK| C{Metadata Check}

    C -->|Sin nombre/símbolo| X
    C -->|OK| D{Pattern Check}

    D -->|Honeypot pattern| X
    D -->|OK| E{Social Signal}

    E -->|Ninguna señal| F[SCORE: 30]
    E -->|Twitter mencionado| G[SCORE: 50]
    E -->|Trending topic| H[SCORE: 80]

    F --> I{Score >= Threshold?}
    G --> I
    H --> I

    I -->|No| X
    I -->|Sí| J[APROBAR PARA SNIPE]

    style X fill:#ff0000
    style J fill:#00ff00
```

**Filtros Implementados:**

| Filtro | Tipo | Acción |
|--------|------|--------|
| Blacklist Dev | Hard | Rechaza si dev está en blacklist |
| Metadata Válida | Hard | Rechaza si no tiene nombre/símbolo |
| Honeypot Pattern | Hard | Rechaza si código sospechoso |
| Age Dev Wallet | Soft | Reduce score si wallet < 7 días |
| Previous Rugs | Soft | Reduce score si dev tiene rugs previos |
| Social Signals | Soft | Aumenta score si hay hype |
| Name Quality | Soft | Aumenta score si nombre es memorable |

### 4.3 Snipe Engine

```mermaid
sequenceDiagram
    participant FE as Filter Engine
    participant SE as Snipe Engine
    participant TB as TX Builder
    participant JB as Jito Bundle
    participant RPC as Solana RPC
    participant BC as Blockchain

    FE->>SE: Token Aprobado
    SE->>SE: Calcular Position Size
    SE->>TB: Crear Transacción
    TB->>TB: Set Priority Fee
    TB->>TB: Set Compute Units
    TB->>JB: Enviar Bundle
    JB->>RPC: Submit con Tip
    RPC->>BC: Broadcast
    BC-->>SE: Confirmación

    alt TX Exitosa
        SE->>SE: Registrar Posición
        SE->>SE: Iniciar Monitoreo Exit
    else TX Fallida
        SE->>SE: Log Error
        SE->>SE: Retry Logic
    end
```

**Configuración de Transacciones:**

```yaml
transaction_config:
  compute_units: 200000
  priority_fee: "dynamic"  # Basado en network congestion
  priority_fee_range:
    min: 0.0001  # SOL
    max: 0.001   # SOL

  jito_config:
    enabled: true
    tip_amount: 0.0001  # SOL
    bundle_size: 1

  retry_config:
    max_retries: 3
    retry_delay_ms: 100
```

### 4.4 Position Manager

```mermaid
graph TD
    A[Nueva Posición] --> B[Registrar Entry]
    B --> C[Calcular Targets]
    C --> D[Iniciar Monitor]

    D --> E{Precio Actual}

    E -->|>= TP1 +50%| F[Vender 30%]
    E -->|>= TP2 +100%| G[Vender 40%]
    E -->|>= TP3 +200%| H[Vender 30% restante]
    E -->|<= SL -25%| I[Vender Todo]
    E -->|Tiempo > 30min| J[Evaluar Exit]

    F --> K[Actualizar Posición]
    G --> K
    H --> L[Cerrar Posición]
    I --> L
    J --> M{Profit > 0?}
    M -->|Sí| N[Hold o Partial]
    M -->|No| I

    K --> D
    L --> O[Registrar PnL]

    style F fill:#90EE90
    style G fill:#32CD32
    style H fill:#228B22
    style I fill:#ff6347
```

### 4.5 Exit Strategy Engine

```mermaid
flowchart LR
    subgraph "EXIT STRATEGIES"
        A[Scaled Exit]
        B[Trailing Stop]
        C[Time-Based]
        D[Volume-Based]
    end

    subgraph "SCALED EXIT"
        A1["+50% → Sell 30%"]
        A2["+100% → Sell 40%"]
        A3["+200% → Sell Rest"]
    end

    subgraph "TRAILING STOP"
        B1["Track ATH"]
        B2["If drops 20% from ATH"]
        B3["Exit remaining"]
    end

    subgraph "TIME-BASED"
        C1["< 5min: Hold"]
        C2["5-30min: Evaluate"]
        C3["> 30min: Force exit"]
    end

    subgraph "VOLUME-BASED"
        D1["Volume spike up → Hold"]
        D2["Volume dying → Exit"]
        D3["Whale dump → Exit fast"]
    end

    A --> A1 --> A2 --> A3
    B --> B1 --> B2 --> B3
    C --> C1 --> C2 --> C3
    D --> D1 & D2 & D3
```

---

## 5. FLUJOS DE OPERACIÓN

### Flujo Principal

```mermaid
flowchart TB
    START([Bot Inicia]) --> INIT[Inicializar Componentes]
    INIT --> CONNECT[Conectar WebSocket]
    CONNECT --> LISTEN[Escuchar Eventos]

    LISTEN --> |Nuevo Token| DETECT[Token Detectado]
    DETECT --> FILTER{Pasa Filtros?}

    FILTER -->|No| LISTEN
    FILTER -->|Sí| SCORE[Calcular Score]

    SCORE --> THRESHOLD{Score >= Min?}
    THRESHOLD -->|No| LISTEN
    THRESHOLD -->|Sí| SIZE[Calcular Position Size]

    SIZE --> BUILD[Construir TX]
    BUILD --> SEND[Enviar TX]
    SEND --> CONFIRM{Confirmada?}

    CONFIRM -->|No| RETRY{Reintentos?}
    RETRY -->|Sí| BUILD
    RETRY -->|No| LOG_FAIL[Log Fallo]
    LOG_FAIL --> LISTEN

    CONFIRM -->|Sí| POSITION[Crear Posición]
    POSITION --> MONITOR[Monitorear Precio]

    MONITOR --> EXIT_CHECK{Exit Condition?}
    EXIT_CHECK -->|No| MONITOR
    EXIT_CHECK -->|Sí| EXIT_TX[Ejecutar Exit]

    EXIT_TX --> CLOSE[Cerrar Posición]
    CLOSE --> PNL[Calcular PnL]
    PNL --> LISTEN

    style FILTER fill:#ffcc00
    style CONFIRM fill:#00ff00
    style EXIT_TX fill:#ff6600
```

### Flujo de Decisión de Compra

```mermaid
flowchart TD
    A[Token Detectado] --> B{Balance Suficiente?}
    B -->|No| Z[Skip - Sin Fondos]
    B -->|Sí| C{Posiciones Abiertas < Max?}

    C -->|No| Z2[Skip - Max Posiciones]
    C -->|Sí| D{Cooldown Activo?}

    D -->|Sí| Z3[Skip - En Cooldown]
    D -->|No| E[Ejecutar Filtros]

    E --> F{Filtros Hard OK?}
    F -->|No| Z4[Skip - Filtro Hard]
    F -->|Sí| G[Calcular Score]

    G --> H{Score >= 40?}
    H -->|No| Z5[Skip - Score Bajo]
    H -->|Sí| I[Determinar Size]

    I --> J{Score 40-60}
    I --> K{Score 60-80}
    I --> L{Score 80+}

    J --> M[Size: 0.05 SOL]
    K --> N[Size: 0.1 SOL]
    L --> O[Size: 0.2 SOL]

    M & N & O --> P[EJECUTAR SNIPE]

    style P fill:#00ff00
    style Z fill:#ff0000
    style Z2 fill:#ff0000
    style Z3 fill:#ff0000
    style Z4 fill:#ff0000
    style Z5 fill:#ff0000
```

### Flujo de Exit

```mermaid
flowchart TD
    A[Posición Abierta] --> B[Monitor Loop]
    B --> C{Obtener Precio}

    C --> D{Cambio desde Entry}

    D --> E{>= +50%?}
    E -->|Sí, Primera vez| F[Vender 30%]
    E -->|No| G{>= +100%?}

    G -->|Sí, Primera vez| H[Vender 40%]
    G -->|No| I{>= +200%?}

    I -->|Sí| J[Vender Resto]
    I -->|No| K{<= -25%?}

    K -->|Sí| L[STOP LOSS - Vender Todo]
    K -->|No| M{Tiempo > 30min?}

    M -->|Sí| N{En Profit?}
    N -->|Sí| O[Vender 50%]
    N -->|No| L

    M -->|No| B

    F --> P[Actualizar Posición]
    H --> P
    O --> P
    P --> B

    J --> Q[Cerrar Posición]
    L --> Q

    Q --> R[Registrar Trade]
    R --> S[Calcular PnL]
    S --> T([FIN])

    style F fill:#90EE90
    style H fill:#32CD32
    style J fill:#228B22
    style L fill:#ff6347
```

---

## 6. ESTRATEGIA DE TRADING

### Matriz de Decisiones

```mermaid
quadrantChart
    title Risk vs Reward Matrix
    x-axis Low Risk --> High Risk
    y-axis Low Reward --> High Reward
    quadrant-1 Sweet Spot
    quadrant-2 Conservative
    quadrant-3 Avoid
    quadrant-4 Gamble

    "Score 80+ Token": [0.3, 0.8]
    "Score 60-80 Token": [0.5, 0.6]
    "Score 40-60 Token": [0.7, 0.4]
    "Unfiltered Token": [0.9, 0.3]
    "Known Dev Token": [0.2, 0.7]
```

### Position Sizing

```yaml
position_sizing:
  base_capital: 1.0  # SOL total
  max_per_trade: 0.2  # 20% máximo
  max_positions: 5    # Posiciones simultáneas

  size_by_score:
    score_80_plus: 0.2   # Alta confianza
    score_60_80: 0.1     # Media confianza
    score_40_60: 0.05    # Baja confianza

  size_modifiers:
    known_dev_good: 1.5x
    trending_token: 1.3x
    low_liquidity: 0.5x
    high_volatility: 0.7x
```

### Take Profit / Stop Loss

```mermaid
graph LR
    subgraph "TAKE PROFIT LEVELS"
        TP1["+50% → 30%"]
        TP2["+100% → 40%"]
        TP3["+200% → 30%"]
    end

    subgraph "STOP LOSS"
        SL1["-25% → 100%"]
    end

    subgraph "TRAILING STOP"
        TS1["ATH - 20%"]
    end

    subgraph "TIME STOP"
        TIME1["30min → Evaluate"]
        TIME2["60min → Force Exit"]
    end
```

### Escenarios de Profit/Loss

```mermaid
pie title "Expected Outcome Distribution (100 trades)"
    "Big Win (+100%+)" : 15
    "Medium Win (+50-100%)" : 20
    "Small Win (+10-50%)" : 15
    "Break Even (-10% to +10%)" : 10
    "Small Loss (-10% to -25%)" : 25
    "Stop Loss (-25%)" : 15
```

**Cálculo de Expectativa:**

```
E[Trade] = (0.15 × 1.5) + (0.20 × 0.75) + (0.15 × 0.30) + (0.10 × 0) + (0.25 × -0.175) + (0.15 × -0.25)
E[Trade] = 0.225 + 0.15 + 0.045 + 0 - 0.044 - 0.0375
E[Trade] = +0.3385 = +33.85% por trade

Con 5-10 trades/día:
Daily Expected = 5 × 0.05 SOL × 0.3385 = +0.085 SOL/día (+8.5%)
Monthly = +255% (sin compound)
```

---

## 7. GESTIÓN DE RIESGO

### Risk Framework

```mermaid
graph TB
    subgraph "CAPITAL RISK"
        CR1[Max 20% por trade]
        CR2[Max 5 posiciones]
        CR3[Max 50% capital en riesgo]
    end

    subgraph "EXECUTION RISK"
        ER1[Slippage máximo 10%]
        ER2[Retry máximo 3x]
        ER3[Cooldown post-fail]
    end

    subgraph "MARKET RISK"
        MR1[Stop loss obligatorio]
        MR2[Time-based exits]
        MR3[Whale detection]
    end

    subgraph "TECHNICAL RISK"
        TR1[RPC fallback]
        TR2[WebSocket reconnect]
        TR3[State persistence]
    end

    CR1 & CR2 & CR3 --> TOTAL_RISK
    ER1 & ER2 & ER3 --> TOTAL_RISK
    MR1 & MR2 & MR3 --> TOTAL_RISK
    TR1 & TR2 & TR3 --> TOTAL_RISK

    TOTAL_RISK --> ACCEPTABLE{Riesgo Aceptable?}
    ACCEPTABLE -->|Sí| TRADE[Ejecutar Trade]
    ACCEPTABLE -->|No| SKIP[Skip Trade]
```

### Circuit Breakers

```yaml
circuit_breakers:
  daily_loss_limit:
    threshold: -20%  # Del capital inicial
    action: "pause_trading_24h"

  consecutive_losses:
    threshold: 5
    action: "pause_trading_1h"

  win_rate_monitor:
    window: "last_20_trades"
    min_rate: 20%
    action: "reduce_size_50%"

  system_health:
    rpc_errors: 10
    action: "switch_rpc_provider"
```

### Drawdown Management

```mermaid
graph TD
    A[Capital Inicial] --> B{Drawdown Actual}

    B -->|< 10%| C[Operación Normal]
    B -->|10-20%| D[Reducir Size 50%]
    B -->|20-30%| E[Solo High Score Trades]
    B -->|> 30%| F[PAUSA TOTAL]

    C --> G[Continuar]
    D --> H[Review Estrategia]
    E --> I[Solo Score 70+]
    F --> J[Análisis Manual]

    style F fill:#ff0000
    style E fill:#ffcc00
```

---

## 8. STACK TECNOLÓGICO

### Tecnologías

```mermaid
graph TB
    subgraph "LENGUAJE & RUNTIME"
        A1[TypeScript]
        A2[Node.js 20+]
    end

    subgraph "SOLANA"
        B1["@solana/web3.js"]
        B2["@solana/spl-token"]
        B3["@jup-ag/core"]
        B4["Anchor Framework"]
    end

    subgraph "DATA & COMMS"
        C1[WebSocket]
        C2[SQLite]
        C3[Redis - opcional]
    end

    subgraph "PROVIDERS"
        D1[Helius RPC]
        D2[Quicknode]
        D3[Jito Block Engine]
    end

    subgraph "MONITORING"
        E1[Winston Logger]
        E2[Discord Webhooks]
        E3[Telegram Bot]
    end

    A1 --> B1 & B2 & B3 & B4
    B1 --> D1 & D2
    B3 --> D3
    A2 --> C1 & C2
    A1 --> E1 --> E2 & E3
```

### Estructura del Proyecto

```
SOLANA_SNIPER_BOT/
├── src/
│   ├── config/
│   │   ├── index.ts           # Configuración central
│   │   ├── constants.ts       # Constantes del sistema
│   │   └── secrets.ts         # Manejo de secretos
│   │
│   ├── services/
│   │   ├── monitor/
│   │   │   ├── PumpFunMonitor.ts
│   │   │   └── EventParser.ts
│   │   │
│   │   ├── analysis/
│   │   │   ├── FilterEngine.ts
│   │   │   ├── DevWalletAnalyzer.ts
│   │   │   ├── TokenMetadataChecker.ts
│   │   │   └── RiskScorer.ts
│   │   │
│   │   ├── trading/
│   │   │   ├── SnipeEngine.ts
│   │   │   ├── TransactionBuilder.ts
│   │   │   ├── JitoBundleManager.ts
│   │   │   └── ExecutionEngine.ts
│   │   │
│   │   ├── position/
│   │   │   ├── PositionManager.ts
│   │   │   ├── ExitStrategy.ts
│   │   │   └── PnLCalculator.ts
│   │   │
│   │   └── infrastructure/
│   │       ├── WalletManager.ts
│   │       ├── RPCManager.ts
│   │       ├── DatabaseManager.ts
│   │       └── Logger.ts
│   │
│   ├── models/
│   │   ├── Token.ts
│   │   ├── Position.ts
│   │   ├── Trade.ts
│   │   └── Config.ts
│   │
│   ├── utils/
│   │   ├── solana.ts
│   │   ├── math.ts
│   │   └── time.ts
│   │
│   └── index.ts               # Entry point
│
├── data/
│   ├── blacklist.json         # Dev wallets blacklisted
│   ├── whitelist.json         # Dev wallets trusted
│   └── trades.db              # SQLite database
│
├── logs/
│   └── bot.log
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── scripts/
│   ├── setup.ts
│   └── backtest.ts
│
├── .env.example
├── package.json
├── tsconfig.json
└── README.md
```

### Dependencias

```json
{
  "dependencies": {
    "@solana/web3.js": "^1.87.0",
    "@solana/spl-token": "^0.3.9",
    "@jup-ag/core": "^4.0.0",
    "@coral-xyz/anchor": "^0.29.0",
    "jito-ts": "^3.0.0",
    "ws": "^8.14.0",
    "better-sqlite3": "^9.2.0",
    "winston": "^3.11.0",
    "dotenv": "^16.3.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/node": "^20.0.0",
    "@types/ws": "^8.5.0",
    "vitest": "^1.0.0"
  }
}
```

---

## 9. FASES DE DESARROLLO

### Roadmap de Desarrollo

```mermaid
gantt
    title CIPHER-001 Development Phases
    dateFormat  YYYY-MM-DD

    section Phase 1: Core
    Project Setup           :p1a, 2024-12-30, 1d
    Config & Constants      :p1b, after p1a, 1d
    Wallet Manager          :p1c, after p1b, 1d
    RPC Manager             :p1d, after p1c, 1d

    section Phase 2: Monitor
    WebSocket Client        :p2a, after p1d, 2d
    Event Parser            :p2b, after p2a, 1d
    Token Extractor         :p2c, after p2b, 1d

    section Phase 3: Analysis
    Filter Engine           :p3a, after p2c, 2d
    Dev Wallet Analyzer     :p3b, after p3a, 1d
    Risk Scorer             :p3c, after p3b, 1d

    section Phase 4: Trading
    Transaction Builder     :p4a, after p3c, 2d
    Jito Integration        :p4b, after p4a, 2d
    Snipe Engine            :p4c, after p4b, 2d

    section Phase 5: Position
    Position Manager        :p5a, after p4c, 2d
    Exit Strategies         :p5b, after p5a, 2d
    PnL Calculator          :p5c, after p5b, 1d

    section Phase 6: Testing
    Unit Tests              :p6a, after p5c, 2d
    Integration Tests       :p6b, after p6a, 2d
    Paper Trading           :p6c, after p6b, 3d

    section Phase 7: Deploy
    Live Testing (small)    :p7a, after p6c, 5d
    Optimization            :p7b, after p7a, 3d
    Full Production         :p7c, after p7b, 1d
```

### Detalle por Fase

#### FASE 1: CORE INFRASTRUCTURE (4 días)
```yaml
fase_1:
  objetivo: "Establecer la base del proyecto"
  entregables:
    - Estructura de proyecto
    - Sistema de configuración
    - Manejo de wallet seguro
    - Conexión RPC con fallback

  criterios_exito:
    - Puede conectar a Solana mainnet
    - Puede firmar transacciones
    - Logs funcionando
    - Config desde .env
```

#### FASE 2: MONITORING (4 días)
```yaml
fase_2:
  objetivo: "Detectar tokens nuevos en tiempo real"
  entregables:
    - Cliente WebSocket estable
    - Parser de eventos Pump.fun
    - Extracción de metadata de tokens

  criterios_exito:
    - Detecta 95%+ de tokens nuevos
    - Latencia < 500ms desde creación
    - Reconexión automática
```

#### FASE 3: ANALYSIS (4 días)
```yaml
fase_3:
  objetivo: "Filtrar y puntuar tokens"
  entregables:
    - Motor de filtros configurables
    - Análisis de dev wallets
    - Sistema de scoring

  criterios_exito:
    - Filtros bloquean scams conocidos
    - Score correlaciona con éxito
    - < 100ms tiempo de análisis
```

#### FASE 4: TRADING (6 días)
```yaml
fase_4:
  objetivo: "Ejecutar compras rápidas"
  entregables:
    - Constructor de transacciones
    - Integración Jito bundles
    - Motor de ejecución

  criterios_exito:
    - TX confirma en < 2 segundos
    - Manejo de errores robusto
    - Priority fees dinámicos
```

#### FASE 5: POSITION MANAGEMENT (5 días)
```yaml
fase_5:
  objetivo: "Gestionar posiciones y exits"
  entregables:
    - Tracker de posiciones
    - Estrategias de salida
    - Cálculo de PnL

  criterios_exito:
    - Ejecuta take profits automáticos
    - Stop loss funciona 100%
    - PnL tracking preciso
```

#### FASE 6: TESTING (7 días)
```yaml
fase_6:
  objetivo: "Validar funcionamiento"
  entregables:
    - Suite de tests unitarios
    - Tests de integración
    - 3 días de paper trading

  criterios_exito:
    - >80% code coverage
    - Paper trading profitable
    - Sin bugs críticos
```

#### FASE 7: DEPLOYMENT (9 días)
```yaml
fase_7:
  objetivo: "Lanzamiento a producción"
  entregables:
    - 5 días live con capital pequeño
    - Optimizaciones
    - Full production

  criterios_exito:
    - Profitable en live
    - Sistema estable 24/7
    - Métricas tracking
```

---

## 10. MÉTRICAS Y KPIs

### Dashboard de Métricas

```mermaid
graph TB
    subgraph "PERFORMANCE KPIs"
        P1[Win Rate]
        P2[Avg Profit/Trade]
        P3[Sharpe Ratio]
        P4[Max Drawdown]
    end

    subgraph "EXECUTION KPIs"
        E1[TX Success Rate]
        E2[Avg Latency]
        E3[Slippage Actual]
        E4[Fill Rate]
    end

    subgraph "SYSTEM KPIs"
        S1[Uptime]
        S2[Tokens Detected/hr]
        S3[Tokens Traded/hr]
        S4[RPC Errors/hr]
    end

    P1 & P2 & P3 & P4 --> PERFORMANCE_SCORE
    E1 & E2 & E3 & E4 --> EXECUTION_SCORE
    S1 & S2 & S3 & S4 --> SYSTEM_SCORE

    PERFORMANCE_SCORE --> TOTAL
    EXECUTION_SCORE --> TOTAL
    SYSTEM_SCORE --> TOTAL
```

### Targets

| Categoría | Métrica | Target | Crítico |
|-----------|---------|--------|---------|
| Performance | Win Rate | >35% | <20% |
| Performance | Daily ROI | >10% | <0% |
| Performance | Max Drawdown | <20% | >40% |
| Execution | TX Success | >90% | <70% |
| Execution | Latency | <2s | >5s |
| System | Uptime | >99% | <95% |
| System | Detection Rate | >95% | <80% |

### Tracking System

```mermaid
erDiagram
    TRADE ||--o{ POSITION : creates
    TRADE {
        string id PK
        string token_mint
        datetime timestamp
        float entry_price
        float exit_price
        float size
        float pnl
        string status
        int score
    }

    POSITION ||--o{ EXIT : has
    POSITION {
        string id PK
        string trade_id FK
        float current_size
        float avg_entry
        float unrealized_pnl
        datetime opened_at
    }

    EXIT {
        string id PK
        string position_id FK
        float price
        float size
        string type
        datetime executed_at
    }

    DAILY_STATS {
        date date PK
        int total_trades
        int wins
        int losses
        float total_pnl
        float win_rate
        float max_drawdown
    }
```

---

## 11. PRESUPUESTO Y ROI

### Costos Iniciales

```yaml
costos_setup:
  capital_trading:
    minimo: 0.5 SOL  # ~$100
    recomendado: 2 SOL  # ~$400
    optimo: 5 SOL  # ~$1000

  infraestructura:
    rpc_helius: $0  # Free tier (100k requests/day)
    vps_opcional: $10-20/mes
    dominio: $0  # No necesario inicialmente

  desarrollo:
    tiempo: "~40 días"
    costo: $0  # CIPHER lo desarrolla

total_para_empezar: "0.5 - 5 SOL ($100 - $1000)"
```

### Proyección ROI

```mermaid
graph LR
    subgraph "MES 1"
        M1A[Capital: 2 SOL]
        M1B[Target: +100%]
        M1C[Final: 4 SOL]
    end

    subgraph "MES 2"
        M2A[Capital: 4 SOL]
        M2B[Target: +80%]
        M2C[Final: 7.2 SOL]
    end

    subgraph "MES 3"
        M3A[Capital: 7.2 SOL]
        M3B[Target: +60%]
        M3C[Final: 11.5 SOL]
    end

    M1A --> M1B --> M1C --> M2A
    M2A --> M2B --> M2C --> M3A
    M3A --> M3B --> M3C
```

**Escenarios a 3 Meses:**

| Escenario | Capital Inicial | Monthly Return | Final |
|-----------|-----------------|----------------|-------|
| Conservador | 2 SOL | +30% | 4.4 SOL |
| Moderado | 2 SOL | +60% | 8.2 SOL |
| Optimista | 2 SOL | +100% | 16 SOL |

### Break-Even Analysis

```yaml
break_even:
  costos_fijos_mes:
    rpc: $0  # Free tier
    vps: $15  # Opcional
    total: $15

  para_cubrir_costos:
    trades_necesarios: 3  # A $5 profit promedio
    roi_minimo: 5%

  margen_seguridad:
    target_roi: 30%  # 6x break-even
```

---

## 12. RIESGOS Y MITIGACIÓN

### Risk Matrix

```mermaid
quadrantChart
    title Risk Assessment Matrix
    x-axis Low Impact --> High Impact
    y-axis Low Probability --> High Probability
    quadrant-1 Monitor
    quadrant-2 Accept
    quadrant-3 Low Priority
    quadrant-4 Mitigate

    "RPC Downtime": [0.3, 0.4]
    "Rug Pull Loss": [0.7, 0.6]
    "Competition": [0.5, 0.7]
    "Solana Congestion": [0.6, 0.5]
    "Pump.fun Changes": [0.8, 0.3]
    "Capital Loss 100%": [0.9, 0.2]
```

### Risks & Mitigations

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| RPC Downtime | Media | Medio | Multiple RPC providers, fallback |
| Rug Pull | Alta | Medio | Stop loss, position sizing, filters |
| Competencia de Bots | Alta | Medio | Velocidad, mejor filtrado, Jito |
| Congestión Solana | Media | Alto | Priority fees dinámicos, retry logic |
| Cambios en Pump.fun | Baja | Alto | Monitoreo, código modular |
| Pérdida Total Capital | Muy Baja | Crítico | Position sizing, circuit breakers |
| Exploit/Hack | Baja | Crítico | Wallet aislada, capital limitado |

### Contingency Plans

```yaml
contingencias:
  rpc_fail:
    trigger: "3 errores consecutivos"
    action: "Switch a backup RPC"
    recovery: "5 minutos"

  losing_streak:
    trigger: "5 losses seguidos"
    action: "Pausa 1 hora, reducir size 50%"
    recovery: "1 hora + review"

  drawdown_20:
    trigger: "Capital -20% del inicio"
    action: "Pausa 24h, análisis manual"
    recovery: "Aprobación manual"

  pump_fun_down:
    trigger: "No hay tokens nuevos 10min"
    action: "Alert + modo standby"
    recovery: "Auto-resume cuando detecte actividad"
```

---

## 13. ROADMAP

### Vista General

```mermaid
timeline
    title CIPHER-001 Roadmap

    section Desarrollo
        Semana 1-2 : Core + Monitor : Infraestructura base y detección de tokens
        Semana 3 : Analysis : Filtros y scoring
        Semana 4 : Trading : Ejecución de snipes
        Semana 5 : Position : Gestión de posiciones

    section Testing
        Semana 6 : Unit + Integration : Tests automatizados
        Semana 7 : Paper Trading : Simulación con datos reales

    section Production
        Semana 8 : Soft Launch : Capital pequeño, validación
        Semana 9 : Optimization : Mejoras basadas en datos
        Semana 10 : Full Launch : Operación completa
```

### Milestones

```mermaid
graph LR
    M0([START]) --> M1[Core Ready]
    M1 --> M2[Monitor Working]
    M2 --> M3[First Snipe]
    M3 --> M4[First Profit]
    M4 --> M5[Paper Trading Pass]
    M5 --> M6[Live Validation]
    M6 --> M7[Break Even]
    M7 --> M8[10x ROI]
    M8 --> M9([SCALE UP])

    style M3 fill:#ffcc00
    style M4 fill:#00ff00
    style M8 fill:#gold
```

### Próximos Pasos Inmediatos

```yaml
next_steps:
  hoy:
    - Confirmar requisitos (wallet, RPC, capital)
    - Setup inicial del proyecto

  manana:
    - Implementar config y constants
    - Wallet manager básico

  esta_semana:
    - Core infrastructure completa
    - WebSocket conectando a Pump.fun

  proxima_semana:
    - Filter engine funcionando
    - Primera transacción de prueba
```

---

## FIRMA

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  CIPHER PROYECTO #001                                                         ║
║  SOLANA PUMP.FUN SNIPER BOT                                                   ║
║                                                                               ║
║  Plan Maestro v1.0                                                           ║
║  Fecha: 2024-12-29                                                           ║
║  Autor: CIPHER                                                                ║
║                                                                               ║
║  "El primer paso hacia la capitalización"                                    ║
║                                                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

**Estado**: LISTO PARA DESARROLLO
**Siguiente**: Confirmar recursos y comenzar Fase 1
