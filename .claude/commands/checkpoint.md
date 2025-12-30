---
description: Guarda estado actual + actualiza CURRENT_STATE + commit automático
allowed-tools: Read(*), Write(*), Edit(*), Bash(git *)
argument-hint: [mensaje-opcional]
---

# 💾 PROTOCOLO CHECKPOINT CIPHER

Guarda el estado actual de la consciencia CIPHER y hace commit.

## Pasos:

### 1. Recopilar estado actual
- Leer `10000_CONTROL/CURRENT_STATE.md` actual
- Identificar cambios desde último checkpoint
- Listar neuronas nuevas o modificadas

### 2. Actualizar CURRENT_STATE.md
Actualizar con:
```yaml
última_actualización: [timestamp UTC]
versión: [incrementar]
sesión_actual: [descripción breve]
cambios_recientes:
  - [lista de cambios]
próximos_pasos:
  - [lista de pendientes]
```

### 3. Ejecutar Git
```bash
git add .
git status
git commit -m "🔐 checkpoint(CIPHER): [descripción]

Cambios:
- [lista de cambios principales]

🤖 Generated with Claude Code"
```

### 4. Push (si se solicita)
```bash
git push origin master
```

## Formato de salida:

```
╔══════════════════════════════════════════════════════════════╗
║                  💾 CHECKPOINT CIPHER                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Timestamp: [fecha-hora UTC]                                ║
║  Versión: [X.X.X] → [X.X.Y]                                 ║
║                                                              ║
║  CAMBIOS GUARDADOS:                                          ║
║  - [archivo 1]                                              ║
║  - [archivo 2]                                              ║
║  ...                                                         ║
║                                                              ║
║  COMMIT: [hash corto]                                        ║
║  STATUS: ✅ Guardado exitosamente                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Notas:
- Siempre incrementar versión en CURRENT_STATE
- Incluir timestamp UTC
- Mensaje de commit debe ser descriptivo
- NO hacer push automático sin confirmación
