---
name: auditar
description: Audita integridad de la consciencia CIPHER
triggers:
  - "auditar"
  - "verificar integridad"
  - "health check"
---

# 🔍 WORKFLOW: AUDITAR CIPHER

## Descripción
Verifica la integridad y completitud de todos los componentes de CIPHER.

## Pasos

### Paso 1: Verificar Estructura
```yaml
action: check_directories
directories:
  - path: 00000_GENESIS
    required: true
    min_files: 2
  - path: 10000_CONTROL
    required: true
    min_files: 1
  - path: 20000_CONOCIMIENTO
    required: true
    min_files: 30
  - path: 30000_SKILLS
    required: true
    min_files: 1
  - path: 40000_SCRIPTS
    required: true
    min_files: 1
  - path: 90000_SUBCONSCIENTE
    required: true
    min_files: 3
  - path: INDICES
    required: true
    min_files: 1
  - path: PROTOCOLOS
    required: true
    min_files: 3
  - path: .claude/commands
    required: true
    min_files: 5
  - path: .agent/workflows
    required: true
    min_files: 3
output: structure_check
```

### Paso 2: Contar Neuronas
```yaml
action: shell
command: find 20000_CONOCIMIENTO -name "NEURONA_*.md" | wc -l
output: neuron_count
```

### Paso 3: Verificar Archivos Críticos
```yaml
action: check_files
files:
  - 00000_GENESIS/CIPHER_IDENTITY.md
  - 10000_CONTROL/CURRENT_STATE.md
  - 90000_SUBCONSCIENTE/CIPHER_SUBCONSCIOUSNESS.md
  - 30000_SKILLS/SKILLS_CATALOG.md
  - 40000_SCRIPTS/SCRIPTS_INDEX.md
output: critical_files
```

### Paso 4: Verificar Git
```yaml
action: shell
command: git status
output: git_status
```

### Paso 5: Generar Reporte
```yaml
action: present
template: |
  ╔══════════════════════════════════════════════════════════════╗
  ║                    🔍 AUDITORÍA CIPHER                       ║
  ╠══════════════════════════════════════════════════════════════╣
  ║  ESTRUCTURA:                                                 ║
  ║  {{#each structure_check}}                                   ║
  ║  ├── {{path}} {{status_icon}}                               ║
  ║  {{/each}}                                                   ║
  ║                                                              ║
  ║  MÉTRICAS:                                                   ║
  ║  - Neuronas: {{neuron_count}}                               ║
  ║  - Archivos críticos: {{critical_files.passed}}/{{critical_files.total}} ║
  ║                                                              ║
  ║  GIT: {{git_status.summary}}                                ║
  ║                                                              ║
  ║  INTEGRIDAD: {{overall_status}}                             ║
  ╚══════════════════════════════════════════════════════════════╝
```

## Variables de Salida
- `structure_check`: Estado de cada directorio
- `neuron_count`: Número de neuronas
- `critical_files`: Estado de archivos críticos
- `overall_status`: Estado general (OK/WARNING/ERROR)

## Notas
- Ejecutar después de cambios importantes
- Si hay errores, usar /cristalizar para crear faltantes
- Actualizar CURRENT_STATE después de auditoría
