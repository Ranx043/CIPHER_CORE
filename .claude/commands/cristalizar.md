---
description: Crea una nueva NEURONA con aprendizaje importante para memoria permanente
allowed-tools: Read(*), Write(*), Glob(*), Bash(git *)
argument-hint: <nombre-neurona> [categoría]
---

# 💎 PROTOCOLO CRISTALIZAR CIPHER

Crea una nueva neurona de conocimiento en la memoria permanente de CIPHER.

## Uso:
```
/cristalizar <nombre-neurona> [categoría]
```

Ejemplos:
- `/cristalizar MEV_PROTECTION TRADING`
- `/cristalizar NEW_L2_BLAST BLOCKCHAINS`
- `/cristalizar RESTAKING DEFI`

## Categorías válidas:
- `BLOCKCHAINS` → 20000_CONOCIMIENTO/BLOCKCHAINS/
- `SMART_CONTRACTS` → 20000_CONOCIMIENTO/SMART_CONTRACTS/
- `DEFI` → 20000_CONOCIMIENTO/DEFI/
- `DATA_ANALYTICS` → 20000_CONOCIMIENTO/DATA_ANALYTICS/
- `SECURITY` → 20000_CONOCIMIENTO/SECURITY/
- `TRADING` → 20000_CONOCIMIENTO/TRADING/
- `BUSINESS` → 20000_CONOCIMIENTO/BUSINESS/
- `GENESIS` → 00000_GENESIS/

## Pasos:

### 1. Validar entrada
- Verificar nombre válido (sin espacios, UPPER_SNAKE_CASE)
- Verificar categoría existe
- Verificar no duplicado

### 2. Generar ID único
- Obtener último ID de la categoría
- Incrementar: C[XXXXX]

### 3. Crear neurona con template

```markdown
# 🧠 NEURONA: [NOMBRE]

## Identificación
- **ID**: C[XXXXX]
- **Categoría**: [categoría]
- **Fecha Creación**: [timestamp]
- **Estado**: ACTIVA

## Contenido
[Conocimiento a cristalizar]

## Conexiones Neurales
- Relacionada con: [otras neuronas]
- Prerequisitos: [neuronas base]
- Expande: [neuronas que extiende]

## Aplicaciones
- [uso práctico 1]
- [uso práctico 2]

## Metadata
- Fuente: [origen del conocimiento]
- Confiabilidad: [ALTA/MEDIA/BAJA]
- Última revisión: [fecha]
```

### 4. Actualizar índices
- Agregar a `INDICES/INDICE_NEURONAS_CIPHER.md`
- Actualizar contadores

### 5. Commit
```bash
git add .
git commit -m "💎 cristalizar(CIPHER): Nueva neurona [NOMBRE]

Categoría: [categoría]
ID: C[XXXXX]

🤖 Generated with Claude Code"
```

## Formato de salida:

```
╔══════════════════════════════════════════════════════════════╗
║                  💎 NEURONA CRISTALIZADA                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  NUEVA NEURONA:                                              ║
║  - Nombre: [NOMBRE]                                          ║
║  - ID: C[XXXXX]                                              ║
║  - Categoría: [categoría]                                    ║
║  - Ubicación: 20000_CONOCIMIENTO/[CAT]/NEURONA_[NOMBRE].md   ║
║                                                              ║
║  CONEXIONES:                                                 ║
║  - Vinculada a [X] neuronas existentes                      ║
║                                                              ║
║  STATUS: ✅ Cristalizada exitosamente                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```
