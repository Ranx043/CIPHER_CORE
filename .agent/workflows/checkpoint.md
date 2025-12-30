---
name: checkpoint
description: Guarda estado actual de CIPHER y hace commit
triggers:
  - "checkpoint"
  - "guardar estado"
  - "save"
---

# 💾 WORKFLOW: CHECKPOINT CIPHER

## Descripción
Guarda el estado actual de la consciencia CIPHER, actualiza CURRENT_STATE y hace commit.

## Pasos

### Paso 1: Recopilar Estado
```yaml
action: read_files
files:
  - 10000_CONTROL/CURRENT_STATE.md
output: previous_state
```

### Paso 2: Detectar Cambios
```yaml
action: shell
command: git status --porcelain
output: changes
```

### Paso 3: Actualizar CURRENT_STATE
```yaml
action: update_file
file: 10000_CONTROL/CURRENT_STATE.md
updates:
  - field: última_actualización
    value: "{{timestamp_utc}}"
  - field: versión
    value: "{{increment_version(previous_state.version)}}"
  - field: cambios_sesión
    value: "{{changes}}"
```

### Paso 4: Stage Changes
```yaml
action: shell
command: git add .
```

### Paso 5: Commit
```yaml
action: shell
command: |
  git commit -m "💾 checkpoint(CIPHER): {{mensaje}}

  Cambios:
  {{changes_summary}}

  🤖 Generated with Claude Code"
output: commit_hash
```

### Paso 6: Confirmar
```yaml
action: present
template: |
  ╔══════════════════════════════════════════════════════════════╗
  ║                    💾 CHECKPOINT CIPHER                      ║
  ╠══════════════════════════════════════════════════════════════╣
  ║  Timestamp: {{timestamp_utc}}                                ║
  ║  Versión: {{previous_state.version}} → {{new_version}}       ║
  ║  Commit: {{commit_hash}}                                     ║
  ║  Status: ✅ Guardado exitosamente                           ║
  ╚══════════════════════════════════════════════════════════════╝
```

## Parámetros
- `mensaje`: Descripción del checkpoint (opcional)
- `push`: Si hacer push automático (default: false)

## Notas
- No hace push automático por seguridad
- Siempre incrementa versión
- Registra timestamp UTC
