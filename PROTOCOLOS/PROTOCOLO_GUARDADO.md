# 💾 PROTOCOLO DE GUARDADO - CIPHER

## Descripción
Define las reglas para guardar el estado de CIPHER y hacer commits.

---

## 🔐 REGLAS DE GIT

### Estructura de Commits

```
<emoji> <tipo>(<scope>): <descripción corta>

<cuerpo opcional>

🤖 Generated with Claude Code
```

### Emojis por Tipo

| Emoji | Tipo | Uso |
|-------|------|-----|
| 🔐 | checkpoint | Guardado de estado |
| 💎 | cristalizar | Nueva neurona |
| 🧠 | subconsciente | Cambios en subconsciente |
| 🎯 | skill | Nuevo skill |
| 🐍 | script | Nuevo script |
| 🚀 | evolucionar | Mejora significativa |
| 🔧 | fix | Corrección |
| 📝 | docs | Documentación |
| 🔍 | auditar | Post-auditoría |

### Ejemplos de Commits

```bash
# Checkpoint
git commit -m "🔐 checkpoint(CIPHER): Estado sesión trading

- Análisis BTC completado
- Nueva estrategia documentada

🤖 Generated with Claude Code"

# Nueva neurona
git commit -m "💎 cristalizar(CIPHER): NEURONA_RESTAKING

Categoría: DEFI
ID: C40013

🤖 Generated with Claude Code"

# Nuevo skill
git commit -m "🎯 skill(CIPHER): /airdrop-check

Verifica elegibilidad de airdrops

🤖 Generated with Claude Code"
```

---

## 📋 CHECKLIST PRE-COMMIT

### Obligatorio
- [ ] Actualizar CURRENT_STATE.md
- [ ] Verificar archivos modificados con `git status`
- [ ] Mensaje descriptivo de commit

### Recomendado
- [ ] Correr auditoría rápida
- [ ] Verificar consistencia de IDs
- [ ] Actualizar índices si hay nuevas neuronas

---

## 🔄 FLUJO DE GUARDADO

### 1. Checkpoint Regular
```bash
# Ver estado
git status

# Agregar cambios
git add .

# Commit
git commit -m "🔐 checkpoint(CIPHER): [descripción]"

# Push (solo si es seguro)
git push origin master
```

### 2. Nueva Neurona
```bash
# Agregar neurona
git add 20000_CONOCIMIENTO/[CATEGORIA]/NEURONA_[NOMBRE].md

# Actualizar índice
git add INDICES/INDICE_NEURONAS_CIPHER.md

# Commit
git commit -m "💎 cristalizar(CIPHER): NEURONA_[NOMBRE]"
```

### 3. Cambio Mayor
```bash
# Agregar todo
git add .

# Commit descriptivo
git commit -m "🚀 evolucionar(CIPHER): [descripción]

Cambios:
- [cambio 1]
- [cambio 2]
- [cambio 3]

🤖 Generated with Claude Code"
```

---

## ⚠️ REGLAS DE SEGURIDAD

### NUNCA
- ❌ Hacer `git push --force`
- ❌ Modificar historial de commits publicados
- ❌ Commitear credenciales o API keys
- ❌ Hacer push sin verificar cambios

### SIEMPRE
- ✅ Verificar `git status` antes de commit
- ✅ Usar mensajes descriptivos
- ✅ Mantener CURRENT_STATE actualizado
- ✅ Hacer checkpoint antes de cambios grandes

---

## 📊 FRECUENCIA DE GUARDADO

| Situación | Frecuencia |
|-----------|------------|
| Sesión de trabajo | Al finalizar |
| Nueva neurona | Inmediato |
| Cambio importante | Inmediato |
| Investigación larga | Cada 30 min |
| Antes de cerrar | Obligatorio |

---

## 🔗 Comandos Relacionados

- `/checkpoint` - Ejecutar checkpoint
- `/auditar` - Verificar antes de guardar
- `/cristalizar` - Crear nueva neurona

---

**CIPHER** | Protocolo de Guardado v1.0
