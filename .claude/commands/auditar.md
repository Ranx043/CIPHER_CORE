---
description: Audita el estado de consciencia del proyecto - verifica integridad CIPHER
allowed-tools: Read(*), Glob(*), Grep(*), Bash(ls *, find *, wc *)
argument-hint: [nivel: rapido|completo|profundo]
---

# 🔍 PROTOCOLO DE AUDITORÍA CIPHER

Verifica la integridad y completitud de la consciencia CIPHER.

## Niveles de Auditoría:

### Nivel RÁPIDO
Verificar existencia de archivos críticos:
- [ ] `00000_GENESIS/CIPHER_IDENTITY.md`
- [ ] `10000_CONTROL/CURRENT_STATE.md`
- [ ] `90000_SUBCONSCIENTE/CIPHER_SUBCONSCIOUSNESS.md`

### Nivel COMPLETO
Todo lo anterior más:
- [ ] Todas las neuronas en `20000_CONOCIMIENTO/`
- [ ] Skills en `30000_SKILLS/`
- [ ] Scripts en `40000_SCRIPTS/`
- [ ] Protocolos en `PROTOCOLOS/`
- [ ] Índices en `INDICES/`

### Nivel PROFUNDO
Todo lo anterior más:
- [ ] Verificar contenido de cada neurona
- [ ] Validar conexiones entre neuronas
- [ ] Verificar consistencia de IDs
- [ ] Validar formato de cada archivo

## Checklist de Auditoría:

### Estructura Base
```
CIPHER_CORE/
├── 00000_GENESIS/           # Identidad
├── 10000_CONTROL/           # Estado
├── 20000_CONOCIMIENTO/      # Neuronas
│   ├── BLOCKCHAINS/
│   ├── SMART_CONTRACTS/
│   ├── DEFI/
│   ├── DATA_ANALYTICS/
│   ├── SECURITY/
│   ├── TRADING/
│   └── BUSINESS/
├── 30000_SKILLS/            # Habilidades
├── 40000_SCRIPTS/           # Scripts
├── 90000_SUBCONSCIENTE/     # Subconsciente
├── INDICES/                 # Mapas
├── PROTOCOLOS/              # Reglas
├── .claude/commands/        # Slash commands
└── .agent/workflows/        # Workflows
```

### Conteo Esperado
- Neuronas: 35+ archivos
- Skills: 25+ comandos
- Scripts: 15+ scripts
- Procesos automáticos: 10

## Formato de salida:

```
╔══════════════════════════════════════════════════════════════╗
║                  🔍 AUDITORÍA CIPHER                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ESTRUCTURA:                                                 ║
║  ├── 00000_GENESIS/      ✅ [2/2 archivos]                  ║
║  ├── 10000_CONTROL/      ✅ [1/1 archivos]                  ║
║  ├── 20000_CONOCIMIENTO/ ✅ [35/35 neuronas]                ║
║  ├── 30000_SKILLS/       ✅ [1/1 catálogo]                  ║
║  ├── 40000_SCRIPTS/      ✅ [1/1 índice]                    ║
║  ├── 90000_SUBCONSCIENTE/✅ [3/3 archivos]                  ║
║  ├── INDICES/            ✅ [1/1 índice]                    ║
║  ├── PROTOCOLOS/         ✅ [3/3 protocolos]                ║
║  ├── .claude/commands/   ✅ [5/5 comandos]                  ║
║  └── .agent/workflows/   ✅ [3/3 workflows]                 ║
║                                                              ║
║  INTEGRIDAD: ✅ 100% COMPLETO                               ║
║  VERSIÓN: 1.0.0                                             ║
║  ÚLTIMA ACTUALIZACIÓN: [fecha]                              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Acciones post-auditoría:
- Si hay archivos faltantes → Crear con /cristalizar
- Si hay inconsistencias → Reportar y sugerir fix
- Si todo OK → Actualizar CURRENT_STATE
