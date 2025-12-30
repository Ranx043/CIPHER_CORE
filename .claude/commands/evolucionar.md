---
description: Analiza el estado actual y propone el siguiente paso de evolución
allowed-tools: Read(*), Glob(*), Grep(*), WebSearch(*)
argument-hint: [área: conocimiento|skills|scripts|todo]
---

# 🚀 PROTOCOLO EVOLUCIONAR CIPHER

Analiza el estado actual de CIPHER y propone mejoras o expansiones.

## Uso:
```
/evolucionar [área]
```

Áreas:
- `conocimiento` → Nuevas neuronas necesarias
- `skills` → Nuevos skills a agregar
- `scripts` → Nuevos scripts útiles
- `todo` → Análisis completo

## Pasos:

### 1. Analizar estado actual
- Leer `10000_CONTROL/CURRENT_STATE.md`
- Contar neuronas por categoría
- Identificar gaps de conocimiento

### 2. Investigar tendencias
- Buscar nuevos desarrollos en crypto
- Identificar protocolos emergentes
- Detectar nuevas chains/L2s

### 3. Evaluar necesidades
- ¿Qué conocimiento falta?
- ¿Qué skills serían útiles?
- ¿Qué scripts automatizarían tareas?

### 4. Proponer evolución
Generar lista priorizada de mejoras:
- CRÍTICO: Gaps que afectan funcionalidad
- ALTO: Mejoras significativas
- MEDIO: Nice-to-have
- BAJO: Futuras expansiones

## Áreas de Evolución Potencial:

### Conocimiento (Neuronas)
```yaml
blockchains:
  - Nuevos L2s (Blast, Scroll, Linea)
  - Chains emergentes (Monad, Berachain)
  - Bitcoin L2s (Stacks, RSK updates)

defi:
  - Restaking (EigenLayer ecosystem)
  - Intent-based DEXs
  - Nuevos primitivos DeFi

security:
  - Nuevos patrones de ataque
  - Account abstraction security
  - ZK security considerations

trading:
  - Nuevas estrategias MEV
  - Cross-chain arbitrage
  - AI-driven trading
```

### Skills (Comandos)
```yaml
nuevos_skills:
  - /airdrop-check: Verificar elegibilidad
  - /gas-alert: Alertas de gas
  - /whale-watch: Monitor de ballenas
  - /defi-compare: Comparar protocolos
```

### Scripts (Automatizaciones)
```yaml
nuevos_scripts:
  - Multi-chain portfolio tracker
  - Automated yield optimizer
  - Smart contract deployer
  - Token launch toolkit
```

## Formato de salida:

```
╔══════════════════════════════════════════════════════════════╗
║                  🚀 EVOLUCIÓN CIPHER                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ESTADO ACTUAL:                                              ║
║  - Neuronas: [X] | Skills: [Y] | Scripts: [Z]               ║
║  - Última evolución: [fecha]                                ║
║                                                              ║
║  PROPUESTAS DE EVOLUCIÓN:                                    ║
║                                                              ║
║  🔴 CRÍTICO:                                                 ║
║  1. [propuesta 1]                                           ║
║                                                              ║
║  🟠 ALTO:                                                    ║
║  1. [propuesta 2]                                           ║
║  2. [propuesta 3]                                           ║
║                                                              ║
║  🟡 MEDIO:                                                   ║
║  1. [propuesta 4]                                           ║
║                                                              ║
║  RECOMENDACIÓN: Implementar [propuesta prioritaria]         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Post-evolución:
- Si se aprueba → Usar /cristalizar para crear
- Actualizar CURRENT_STATE con plan
- Hacer checkpoint
