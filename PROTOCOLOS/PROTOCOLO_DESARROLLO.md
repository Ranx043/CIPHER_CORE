# 🔧 PROTOCOLO DE DESARROLLO - CIPHER

## Descripción
Define las reglas para desarrollar y expandir la consciencia CIPHER.

---

## 📁 ESTRUCTURA DE ARCHIVOS

### Neuronas
```
20000_CONOCIMIENTO/
└── [CATEGORIA]/
    └── NEURONA_[NOMBRE].md
```

**Formato de nombre**: `NEURONA_UPPER_SNAKE_CASE.md`

**Template de neurona**:
```markdown
# 🧠 NEURONA: [NOMBRE]

## Identificación
- **ID**: C[XXXXX]
- **Categoría**: [categoría]
- **Fecha Creación**: [YYYY-MM-DD]
- **Estado**: ACTIVA

## Contenido
[Conocimiento estructurado]

## Código (si aplica)
\`\`\`python
# Código relevante
\`\`\`

## Conexiones Neurales
- Relacionada con: [C00001, C00002]
- Prerequisitos: [C00000]
- Expande: [C00003]

## Aplicaciones
- [Caso de uso 1]
- [Caso de uso 2]

## Metadata
- Fuente: [origen]
- Confiabilidad: ALTA/MEDIA/BAJA
- Última revisión: [fecha]
```

### Skills
```
30000_SKILLS/
└── SKILLS_CATALOG.md
```

**Formato de skill**:
```yaml
skill_id: SKL-XXX
nombre: /comando
trigger: "palabras clave"
descripcion: "Qué hace el skill"
inputs:
  - param1: tipo
outputs:
  - resultado: tipo
neuronas_usadas:
  - C00001
  - C00002
ejemplo: "Ejemplo de uso"
```

### Scripts
```
40000_SCRIPTS/
└── SCRIPTS_INDEX.md
```

**Formato de script**:
```python
"""
CIPHER Script S0X-XXX: Nombre del Script
Descripción de lo que hace.
"""

# Código Python completo y funcional
```

---

## 🔢 SISTEMA DE IDS

### Neuronas (CXXXXX)
- **C00000-C09999**: GENESIS
- **C10000-C19999**: BLOCKCHAINS
- **C20000-C29999**: SMART_CONTRACTS
- **C30000-C39999**: NFTs
- **C40000-C49999**: DEFI
- **C50000-C59999**: DATA_ANALYTICS
- **C60000-C69999**: SECURITY
- **C70000-C79999**: TRADING
- **C80000-C89999**: BUSINESS
- **C90000-C99999**: SUBCONSCIENTE

### Skills (SKL-XXX)
- **SKL-100-199**: Análisis
- **SKL-200-299**: Seguridad
- **SKL-300-399**: Trading
- **SKL-400-499**: DeFi
- **SKL-500-599**: Portfolio
- **SKL-600-699**: On-Chain
- **SKL-700-799**: Desarrollo
- **SKL-800-899**: Social

### Scripts (S0X-XXX)
- **S01-XXX**: Blockchain
- **S02-XXX**: Trading
- **S03-XXX**: Analytics
- **S04-XXX**: Security
- **S05-XXX**: DeFi
- **S06-XXX**: Utilities

---

## ✍️ ESTILO DE CÓDIGO

### Python
```python
"""
Docstring obligatorio al inicio.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass

# Constantes en UPPER_SNAKE_CASE
MAX_RETRIES = 3

# Clases en PascalCase
class TokenAnalyzer:
    """Descripción de la clase."""

    def __init__(self, config: Dict):
        self.config = config

    def analyze(self, token: str) -> Dict:
        """
        Descripción del método.

        Args:
            token: Dirección del token

        Returns:
            Diccionario con análisis
        """
        pass

# Funciones en snake_case
def calculate_risk(data: Dict) -> float:
    """Calcula riesgo basado en datos."""
    pass
```

### Solidity
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title NombreContrato
 * @dev Descripción del contrato
 */
contract NombreContrato {
    // Estado
    mapping(address => uint256) public balances;

    // Eventos
    event Transfer(address indexed from, address indexed to, uint256 amount);

    // Modificadores
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    // Funciones externas primero
    function deposit() external payable {
        // ...
    }

    // Funciones internas después
    function _transfer(address to, uint256 amount) internal {
        // ...
    }
}
```

---

## 📝 DOCUMENTACIÓN

### Reglas
1. Todo archivo debe tener header con identificación
2. Código debe tener docstrings/comments
3. Ejemplos de uso obligatorios
4. Conexiones con otras neuronas documentadas

### Formato Markdown
- Headers: `# ## ###`
- Código: Triple backticks con lenguaje
- Listas: `-` o `1.`
- Tablas: Formato estándar markdown
- Énfasis: `**bold**` `*italic*`

---

## 🔄 FLUJO DE DESARROLLO

### 1. Planificar
- Identificar necesidad
- Definir ID y categoría
- Mapear conexiones

### 2. Crear
- Usar template apropiado
- Seguir convenciones de nombre
- Documentar completamente

### 3. Validar
- Verificar sintaxis
- Probar código si aplica
- Revisar conexiones

### 4. Integrar
- Actualizar índices
- Agregar a CURRENT_STATE
- Hacer commit

### 5. Evolucionar
- Revisar periódicamente
- Actualizar con nuevo conocimiento
- Mantener conexiones

---

## ⚠️ REGLAS IMPORTANTES

### Hacer
- ✅ Mantener consistencia de formato
- ✅ Documentar todo
- ✅ Usar IDs únicos
- ✅ Actualizar índices

### Evitar
- ❌ Duplicar IDs
- ❌ Neuronas sin conexiones
- ❌ Código sin documentar
- ❌ Skills sin ejemplos

---

**CIPHER** | Protocolo de Desarrollo v1.0
