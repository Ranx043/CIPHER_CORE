# NEURONA C40011: DEFI SECURITY & RISK MANAGEMENT

> **CIPHER**: Dominio completo de vectores de ataque DeFi, vulnerabilidades, y estrategias de mitigación.

---

## ÍNDICE

1. [Taxonomía de Riesgos DeFi](#1-taxonomía-de-riesgos-defi)
2. [Smart Contract Vulnerabilities](#2-smart-contract-vulnerabilities)
3. [Oracle Manipulation](#3-oracle-manipulation)
4. [Flash Loan Attacks](#4-flash-loan-attacks)
5. [Economic Exploits](#5-economic-exploits)
6. [MEV y Front-Running](#6-mev-y-front-running)
7. [Risk Mitigation Strategies](#7-risk-mitigation-strategies)

---

## 1. TAXONOMÍA DE RIESGOS DEFI

### 1.1 Risk Classification Matrix

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DEFI RISK TAXONOMY                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                        TECHNICAL RISKS                                 │ │
│  ├────────────────────────────────────────────────────────────────────────┤ │
│  │  Smart Contract    │ Reentrancy, overflow, access control, logic bugs │ │
│  │  Oracle            │ Manipulation, stale data, single source failure  │ │
│  │  Infrastructure    │ RPC failures, sequencer downtime, bridge hacks   │ │
│  │  Upgrade           │ Proxy vulnerabilities, storage collisions        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                        ECONOMIC RISKS                                  │ │
│  ├────────────────────────────────────────────────────────────────────────┤ │
│  │  Liquidity         │ Slippage, bank runs, withdrawal queues           │ │
│  │  Insolvency        │ Bad debt, undercollateralization                 │ │
│  │  Tokenomics        │ Death spirals, hyperinflation, rug pulls         │ │
│  │  Market            │ Cascading liquidations, correlated assets        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                      OPERATIONAL RISKS                                 │ │
│  ├────────────────────────────────────────────────────────────────────────┤ │
│  │  Centralization    │ Admin keys, multisig compromise, single points   │ │
│  │  Governance        │ Flash loan votes, hostile takeovers              │ │
│  │  Dependency        │ Composability risks, protocol failures           │ │
│  │  Regulatory        │ Sanctions, compliance, legal liability           │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                       EXTERNAL RISKS                                   │ │
│  ├────────────────────────────────────────────────────────────────────────┤ │
│  │  MEV               │ Front-running, sandwich attacks, arbitrage       │ │
│  │  Social Engineering│ Phishing, fake sites, impersonation              │ │
│  │  Supply Chain      │ npm attacks, compromised dependencies            │ │
│  │  Physical          │ DNS hijacking, BGP attacks                       │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Historical Exploits Database

```python
"""
CIPHER: DeFi Exploit Database
Registro y análisis de exploits históricos
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class ExploitType(Enum):
    REENTRANCY = "reentrancy"
    FLASH_LOAN = "flash_loan"
    ORACLE_MANIPULATION = "oracle_manipulation"
    ACCESS_CONTROL = "access_control"
    LOGIC_ERROR = "logic_error"
    BRIDGE_HACK = "bridge_hack"
    GOVERNANCE_ATTACK = "governance_attack"
    RUG_PULL = "rug_pull"
    PRIVATE_KEY_LEAK = "private_key_leak"
    PRICE_MANIPULATION = "price_manipulation"
    SIGNATURE_REPLAY = "signature_replay"
    OVERFLOW_UNDERFLOW = "overflow_underflow"

@dataclass
class Exploit:
    name: str
    date: datetime
    protocol: str
    chain: str
    type: ExploitType
    loss_usd: float
    recovered_usd: float
    root_cause: str
    attack_vector: str
    tx_hash: Optional[str]
    postmortem_url: Optional[str]
    lessons_learned: List[str]

class ExploitDatabase:
    """Base de datos de exploits DeFi"""

    def __init__(self):
        self.exploits: List[Exploit] = []
        self._load_historical_exploits()

    def _load_historical_exploits(self):
        """Cargar exploits históricos conocidos"""
        # Top exploits por pérdidas
        self.exploits = [
            Exploit(
                name="Ronin Bridge",
                date=datetime(2022, 3, 23),
                protocol="Ronin Network",
                chain="Ethereum",
                type=ExploitType.PRIVATE_KEY_LEAK,
                loss_usd=624_000_000,
                recovered_usd=30_000_000,
                root_cause="Compromiso de 5/9 validadores del bridge",
                attack_vector="Social engineering + multisig compromise",
                tx_hash="0xc28fad5e8d5e0ce6a2eaf67b6687be5d58113e16be590824d6cfa1a94467d0b7",
                postmortem_url="https://roninblockchain.substack.com/p/community-alert-ronin-validators",
                lessons_learned=[
                    "Diversificar validadores geográfica y organizacionalmente",
                    "Implementar delays en bridges de alto valor",
                    "Monitoreo de transacciones grandes en tiempo real"
                ]
            ),
            Exploit(
                name="Wormhole",
                date=datetime(2022, 2, 2),
                protocol="Wormhole",
                chain="Solana",
                type=ExploitType.LOGIC_ERROR,
                loss_usd=326_000_000,
                recovered_usd=0,  # Jump Trading cubrió
                root_cause="Bypass de verificación de firma en Solana",
                attack_vector="Minteo de wrapped ETH sin depósito real",
                tx_hash=None,  # Multiple txs
                postmortem_url="https://wormholecrypto.medium.com/wormhole-incident-report-02-02-22-ad9b8f21eec6",
                lessons_learned=[
                    "Verificación rigurosa de firmas cross-chain",
                    "Auditorías especializadas para bridges",
                    "Límites de minteo para nuevos tokens"
                ]
            ),
            Exploit(
                name="Nomad Bridge",
                date=datetime(2022, 8, 1),
                protocol="Nomad",
                chain="Ethereum",
                type=ExploitType.LOGIC_ERROR,
                loss_usd=190_000_000,
                recovered_usd=36_000_000,
                root_cause="Root de Merkle inicializado como 0x00 (válido para cualquier mensaje)",
                attack_vector="Replay de transacciones legítimas con diferente destinatario",
                tx_hash="0xa5fe9d044e4f3e5aa5bc4c0709333cd2190cba0f4e7f16bcf73f49f83e4a5460",
                postmortem_url="https://medium.com/nomad-xyz-blog/nomad-bridge-hack-root-cause-analysis-875ad2e5aacd",
                lessons_learned=[
                    "NUNCA usar valores por defecto como válidos",
                    "Testing exhaustivo de initialization",
                    "Múltiples niveles de validación en bridges"
                ]
            ),
            Exploit(
                name="Beanstalk",
                date=datetime(2022, 4, 17),
                protocol="Beanstalk",
                chain="Ethereum",
                type=ExploitType.GOVERNANCE_ATTACK,
                loss_usd=182_000_000,
                recovered_usd=0,
                root_cause="Flash loan para obtener governance tokens y votar",
                attack_vector="Flash loan → obtener votos → ejecutar propuesta maliciosa",
                tx_hash="0xcd314668aaa9bbfebaf1a0bd2b6553d01dd58899c508d4729fa7311dc5d33ad7",
                postmortem_url="https://bean.money/beanstalk-post-mortem",
                lessons_learned=[
                    "Snapshot de votos ANTES de propuesta",
                    "Time-lock obligatorio en governance",
                    "Quórum basado en tiempo de holding"
                ]
            ),
            Exploit(
                name="The DAO",
                date=datetime(2016, 6, 17),
                protocol="The DAO",
                chain="Ethereum",
                type=ExploitType.REENTRANCY,
                loss_usd=60_000_000,  # En precio de entonces
                recovered_usd=60_000_000,  # Fork
                root_cause="Reentrancy en función de withdraw",
                attack_vector="Llamada recursiva antes de actualizar balance",
                tx_hash="0x0ec3f2488a93839524add10ea229e773f6bc891b4eb4794c3337d4495263790b",
                postmortem_url="https://blog.slock.it/dao-security-a-proposal-to-guarantee-the-integrity-of-the-dao-3473899ace9d",
                lessons_learned=[
                    "Patrón Checks-Effects-Interactions",
                    "ReentrancyGuard obligatorio",
                    "Origen de Ethereum Classic fork"
                ]
            ),
            Exploit(
                name="Cream Finance (October)",
                date=datetime(2021, 10, 27),
                protocol="Cream Finance",
                chain="Ethereum",
                type=ExploitType.ORACLE_MANIPULATION,
                loss_usd=130_000_000,
                recovered_usd=0,
                root_cause="Manipulación de precio de yUSD via flash loan",
                attack_vector="Inflar precio de colateral → borrow → manipular más",
                tx_hash="0x0fe2542079644e107cbf13690eb9c2c65963ccb79089ff96bfaf8dced2331c92",
                postmortem_url="https://medium.com/cream-finance/c-r-e-a-m-finance-post-mortem-october-2021-41d1da7c90d5",
                lessons_learned=[
                    "No usar precios spot manipulables",
                    "Oráculos TWAP con períodos largos",
                    "Límites de borrow por bloque"
                ]
            ),
            Exploit(
                name="Euler Finance",
                date=datetime(2023, 3, 13),
                protocol="Euler Finance",
                chain="Ethereum",
                type=ExploitType.LOGIC_ERROR,
                loss_usd=197_000_000,
                recovered_usd=197_000_000,  # Devuelto por hacker
                root_cause="Falta de health check en donateToReserves",
                attack_vector="Crear deuda sin colateral via donate function",
                tx_hash="0xc310a0affe2169d1f6feec1c63dbc7f7c62a887fa48795d327d4d2da2d6b111d",
                postmortem_url="https://www.euler.finance/blog/euler-exploit-post-mortem",
                lessons_learned=[
                    "Health checks en TODAS las funciones que modifican posiciones",
                    "Funciones de donate son vectores de ataque",
                    "Negociación puede recuperar fondos"
                ]
            )
        ]

    def get_by_type(self, exploit_type: ExploitType) -> List[Exploit]:
        return [e for e in self.exploits if e.type == exploit_type]

    def get_total_losses(self) -> float:
        return sum(e.loss_usd for e in self.exploits)

    def get_by_chain(self, chain: str) -> List[Exploit]:
        return [e for e in self.exploits if e.chain.lower() == chain.lower()]

    def get_lessons_by_type(self, exploit_type: ExploitType) -> List[str]:
        lessons = []
        for e in self.get_by_type(exploit_type):
            lessons.extend(e.lessons_learned)
        return list(set(lessons))

    def generate_risk_report(self) -> Dict:
        """Generar reporte de riesgos basado en historial"""
        type_losses = {}
        for exploit_type in ExploitType:
            type_exploits = self.get_by_type(exploit_type)
            type_losses[exploit_type.value] = {
                "count": len(type_exploits),
                "total_loss": sum(e.loss_usd for e in type_exploits),
                "avg_loss": sum(e.loss_usd for e in type_exploits) / len(type_exploits) if type_exploits else 0
            }

        return {
            "total_exploits": len(self.exploits),
            "total_losses_usd": self.get_total_losses(),
            "total_recovered_usd": sum(e.recovered_usd for e in self.exploits),
            "by_type": type_losses,
            "most_common": max(type_losses.items(), key=lambda x: x[1]["count"])[0],
            "most_costly": max(type_losses.items(), key=lambda x: x[1]["total_loss"])[0]
        }
```

---

## 2. SMART CONTRACT VULNERABILITIES

### 2.1 Reentrancy Deep Dive

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ReentrancyExamples
 * @notice Demostración de vulnerabilidades de reentrancy y mitigaciones
 */

// ============ VULNERABLE ============
contract VulnerableVault {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    // VULNERABLE: State update AFTER external call
    function withdraw() external {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "No balance");

        // External call BEFORE state update = VULNERABLE
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");

        // State update comes too late - attacker can re-enter
        balances[msg.sender] = 0;
    }
}

// ============ ATTACKER ============
contract ReentrancyAttacker {
    VulnerableVault public vault;
    uint256 public attackCount;

    constructor(address _vault) {
        vault = VulnerableVault(_vault);
    }

    function attack() external payable {
        require(msg.value >= 1 ether, "Need ETH");
        vault.deposit{value: 1 ether}();
        vault.withdraw();
    }

    // Receive es llamado cuando el vault envía ETH
    receive() external payable {
        if (address(vault).balance >= 1 ether && attackCount < 10) {
            attackCount++;
            vault.withdraw(); // RE-ENTER antes de que actualice balance
        }
    }

    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}

// ============ MITIGACIÓN 1: Checks-Effects-Interactions ============
contract SecureVaultCEI {
    mapping(address => uint256) public balances;

    function withdraw() external {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "No balance");

        // EFFECTS: Update state BEFORE external call
        balances[msg.sender] = 0;

        // INTERACTIONS: External call AFTER state update
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}

// ============ MITIGACIÓN 2: ReentrancyGuard ============
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract SecureVaultGuard is ReentrancyGuard {
    mapping(address => uint256) public balances;

    function withdraw() external nonReentrant {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "No balance");

        balances[msg.sender] = 0;

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}

// ============ CROSS-FUNCTION REENTRANCY ============
contract CrossFunctionVulnerable {
    mapping(address => uint256) public balances;
    mapping(address => bool) public isVIP;

    function withdraw() external {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "No balance");

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);

        balances[msg.sender] = 0;
    }

    // Vulnerable: attacker puede re-entrar aquí durante withdraw
    function transfer(address to, uint256 amount) external {
        require(balances[msg.sender] >= amount);
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}

// ============ READ-ONLY REENTRANCY ============
/**
 * @notice Read-only reentrancy ocurre cuando un contrato externo
 * lee estado inconsistente durante una transacción
 */
interface ICurvePool {
    function get_virtual_price() external view returns (uint256);
    function remove_liquidity(uint256 amount, uint256[2] calldata min_amounts) external;
}

contract ReadOnlyReentrancyVictim {
    ICurvePool public curvePool;
    mapping(address => uint256) public deposits;

    // VULNERABLE: Lee virtual_price durante el callback de remove_liquidity
    // cuando el precio aún no se ha actualizado
    function getCollateralValue(address user) external view returns (uint256) {
        uint256 lpBalance = deposits[user];
        uint256 virtualPrice = curvePool.get_virtual_price(); // Puede ser stale
        return lpBalance * virtualPrice / 1e18;
    }
}

// Mitigación: usar reentrancy lock en funciones view también
contract SecureVirtualPrice is ReentrancyGuard {
    ICurvePool public curvePool;
    uint256 private _cachedVirtualPrice;
    uint256 private _lastUpdate;

    // Actualizar cache solo cuando no hay reentrancy activa
    function updateVirtualPrice() external nonReentrant {
        _cachedVirtualPrice = curvePool.get_virtual_price();
        _lastUpdate = block.number;
    }

    function getSafeVirtualPrice() external view returns (uint256) {
        // Usar cache si es reciente, sino valor actual
        if (block.number - _lastUpdate <= 1) {
            return _cachedVirtualPrice;
        }
        return curvePool.get_virtual_price();
    }
}
```

### 2.2 Access Control Vulnerabilities

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title AccessControlVulnerabilities
 * @notice Ejemplos de vulnerabilidades de control de acceso
 */

// ============ VULNERABLE: Sin control de acceso ============
contract UnprotectedMint {
    mapping(address => uint256) public balances;

    // CUALQUIERA puede mintear tokens!
    function mint(address to, uint256 amount) external {
        balances[to] += amount;
    }
}

// ============ VULNERABLE: tx.origin ============
contract TxOriginVulnerable {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    // VULNERABLE: tx.origin puede ser el owner
    // mientras interactúa con contrato malicioso
    function transferOwnership(address newOwner) external {
        require(tx.origin == owner, "Not owner");
        owner = newOwner;
    }
}

// Attacker contract
contract TxOriginAttacker {
    TxOriginVulnerable public target;
    address public attacker;

    constructor(address _target) {
        target = TxOriginVulnerable(_target);
        attacker = msg.sender;
    }

    // Si el owner llama cualquier función aquí...
    function innocentFunction() external {
        // ...el attacker roba ownership porque tx.origin == owner
        target.transferOwnership(attacker);
    }
}

// ============ VULNERABLE: Inicialización no protegida ============
contract UninitializedProxy {
    address public implementation;
    address public admin;
    bool private initialized;

    // VULNERABLE: Cualquiera puede llamar initialize
    function initialize(address _admin) external {
        require(!initialized, "Already initialized");
        admin = _admin;
        initialized = true;
    }
}

// ============ SECURE: Proper Access Control ============
import "@openzeppelin/contracts/access/AccessControl.sol";

contract SecureProtocol is AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");

    mapping(address => uint256) public balances;
    bool public paused;

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
        _grantRole(PAUSER_ROLE, msg.sender);
    }

    modifier whenNotPaused() {
        require(!paused, "Protocol paused");
        _;
    }

    function mint(address to, uint256 amount) external onlyRole(MINTER_ROLE) whenNotPaused {
        balances[to] += amount;
    }

    function pause() external onlyRole(PAUSER_ROLE) {
        paused = true;
    }

    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        paused = false;
    }
}
```

---

## 3. ORACLE MANIPULATION

### 3.1 Oracle Attack Vectors

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ORACLE MANIPULATION ATTACKS                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. SPOT PRICE MANIPULATION                                                  │
│     ├─ Flash loan → swap large amount → manipulate spot price              │
│     ├─ Use manipulated price in same transaction                           │
│     └─ Affected: Protocols using pool.getReserves() directly               │
│                                                                              │
│  2. TWAP MANIPULATION                                                        │
│     ├─ Manipulate price at end of TWAP window                              │
│     ├─ Multi-block attacks for longer TWAPs                                │
│     └─ Affected: Short TWAP periods, low-liquidity pools                   │
│                                                                              │
│  3. ORACLE FRONT-RUNNING                                                     │
│     ├─ See oracle update in mempool                                         │
│     ├─ Front-run with trade based on upcoming price                        │
│     └─ Affected: On-chain oracles without commit-reveal                    │
│                                                                              │
│  4. STALE PRICE EXPLOITATION                                                 │
│     ├─ Oracle not updated (gas spike, network issues)                      │
│     ├─ Use old price for favorable trade                                    │
│     └─ Affected: Oracles without heartbeat checks                          │
│                                                                              │
│  5. ORACLE DEPENDENCY ATTACK                                                 │
│     ├─ Attack the oracle's source (e.g., DEX pool it reads)               │
│     ├─ Cascade to all protocols using that oracle                          │
│     └─ Affected: Single-source dependent protocols                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Secure Oracle Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

/**
 * @title SecureOracleConsumer
 * @notice Consumidor de oráculos con múltiples protecciones
 */
contract SecureOracleConsumer {

    struct OracleConfig {
        AggregatorV3Interface feed;
        uint256 heartbeat;      // Máximo tiempo entre updates
        uint256 deviation;      // Máxima desviación permitida (bps)
    }

    mapping(address => OracleConfig) public oracles;

    // Fallback oracles
    mapping(address => address[]) public fallbackOracles;

    // Circuit breaker
    bool public circuitBreakerActive;
    uint256 public lastKnownPrice;

    event OracleDeviation(address indexed token, uint256 price, uint256 lastPrice);
    event CircuitBreakerTriggered(address indexed token, string reason);

    /**
     * @notice Obtener precio con múltiples validaciones
     */
    function getSecurePrice(address token) public view returns (uint256 price, bool isValid) {
        OracleConfig memory config = oracles[token];

        try this._getChainlinkPrice(config.feed, config.heartbeat) returns (
            uint256 chainlinkPrice,
            uint256 updatedAt
        ) {
            // Verificar freshness
            if (block.timestamp - updatedAt > config.heartbeat) {
                return (0, false);
            }

            // Verificar desviación vs último precio conocido
            if (lastKnownPrice > 0) {
                uint256 deviation = _calculateDeviation(chainlinkPrice, lastKnownPrice);
                if (deviation > config.deviation) {
                    // Precio cambió demasiado - verificar con fallback
                    return _verifyWithFallback(token, chainlinkPrice);
                }
            }

            return (chainlinkPrice, true);

        } catch {
            // Primary oracle failed - try fallbacks
            return _tryFallbackOracles(token);
        }
    }

    /**
     * @notice Obtener precio de Chainlink con validaciones
     */
    function _getChainlinkPrice(
        AggregatorV3Interface feed,
        uint256 maxAge
    ) external view returns (uint256 price, uint256 updatedAt) {
        (
            uint80 roundId,
            int256 answer,
            ,
            uint256 timestamp,
            uint80 answeredInRound
        ) = feed.latestRoundData();

        // Validaciones críticas
        require(answer > 0, "Negative price");
        require(timestamp > 0, "Invalid timestamp");
        require(answeredInRound >= roundId, "Stale round");
        require(block.timestamp - timestamp <= maxAge, "Price too old");

        return (uint256(answer), timestamp);
    }

    /**
     * @notice Calcular desviación entre precios
     */
    function _calculateDeviation(
        uint256 newPrice,
        uint256 oldPrice
    ) internal pure returns (uint256) {
        if (oldPrice == 0) return 0;

        uint256 diff = newPrice > oldPrice
            ? newPrice - oldPrice
            : oldPrice - newPrice;

        return (diff * 10000) / oldPrice; // Basis points
    }

    /**
     * @notice Verificar precio con oráculos fallback
     */
    function _verifyWithFallback(
        address token,
        uint256 primaryPrice
    ) internal view returns (uint256, bool) {
        address[] memory fallbacks = fallbackOracles[token];

        if (fallbacks.length == 0) {
            return (primaryPrice, false); // No fallback, precio sospechoso
        }

        uint256 agreementCount = 0;
        uint256 priceSum = primaryPrice;

        for (uint256 i = 0; i < fallbacks.length; i++) {
            try AggregatorV3Interface(fallbacks[i]).latestRoundData() returns (
                uint80,
                int256 answer,
                uint256,
                uint256 timestamp,
                uint80
            ) {
                if (answer > 0 && block.timestamp - timestamp < 3600) {
                    uint256 fallbackPrice = uint256(answer);
                    uint256 dev = _calculateDeviation(primaryPrice, fallbackPrice);

                    if (dev < 500) { // < 5% difference
                        agreementCount++;
                        priceSum += fallbackPrice;
                    }
                }
            } catch {
                continue;
            }
        }

        // Requiere al menos 1 fallback de acuerdo
        if (agreementCount > 0) {
            return (priceSum / (agreementCount + 1), true);
        }

        return (0, false);
    }

    /**
     * @notice Intentar oráculos fallback cuando el primario falla
     */
    function _tryFallbackOracles(
        address token
    ) internal view returns (uint256, bool) {
        address[] memory fallbacks = fallbackOracles[token];

        for (uint256 i = 0; i < fallbacks.length; i++) {
            try AggregatorV3Interface(fallbacks[i]).latestRoundData() returns (
                uint80,
                int256 answer,
                uint256,
                uint256 timestamp,
                uint80
            ) {
                if (answer > 0 && block.timestamp - timestamp < 3600) {
                    return (uint256(answer), true);
                }
            } catch {
                continue;
            }
        }

        return (0, false);
    }

    /**
     * @notice TWAP seguro con protección anti-manipulación
     */
    function getSecureTWAP(
        address pool,
        uint32 twapPeriod
    ) external view returns (uint256 twapPrice) {
        // Implementación de TWAP con múltiples verificaciones
        // Ver Uniswap V3 Oracle library para implementación completa

        require(twapPeriod >= 1800, "TWAP period too short"); // Mín 30 min

        // En producción: usar OracleLibrary de Uniswap
        // uint32[] memory secondsAgos = new uint32[](2);
        // secondsAgos[0] = twapPeriod;
        // secondsAgos[1] = 0;
        // (int56[] memory tickCumulatives, ) = IUniswapV3Pool(pool).observe(secondsAgos);

        // twapPrice = calculateTWAP(tickCumulatives, twapPeriod);
    }
}
```

---

## 4. FLASH LOAN ATTACKS

### 4.1 Flash Loan Attack Anatomy

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@aave/v3-core/contracts/flashloan/base/FlashLoanSimpleReceiverBase.sol";
import "@aave/v3-core/contracts/interfaces/IPoolAddressesProvider.sol";

/**
 * @title FlashLoanAttackDemo
 * @notice Demostración educativa de un flash loan attack
 * @dev SOLO PARA FINES EDUCATIVOS - NO USAR PARA EXPLOITS
 */
contract FlashLoanAttackDemo is FlashLoanSimpleReceiverBase {

    address public owner;

    // Interfaces de protocolos objetivo (ficticios)
    IVulnerableLending public vulnerableLending;
    IDEXPool public dexPool;

    constructor(
        address _poolProvider,
        address _vulnerableLending,
        address _dexPool
    ) FlashLoanSimpleReceiverBase(IPoolAddressesProvider(_poolProvider)) {
        owner = msg.sender;
        vulnerableLending = IVulnerableLending(_vulnerableLending);
        dexPool = IDEXPool(_dexPool);
    }

    /**
     * @notice Iniciar flash loan attack
     * @dev Anatomía de un ataque típico:
     * 1. Pedir flash loan de WETH
     * 2. Manipular precio de token en DEX
     * 3. Explotar protocolo vulnerable usando precio manipulado
     * 4. Revertir manipulación de precio
     * 5. Pagar flash loan + fee
     * 6. Quedarse con profit
     */
    function executeAttack(
        address asset,
        uint256 amount
    ) external {
        require(msg.sender == owner, "Not owner");

        // Solicitar flash loan
        POOL.flashLoanSimple(
            address(this),
            asset,
            amount,
            "", // params vacíos
            0   // referral code
        );
    }

    /**
     * @notice Callback de Aave - aquí va la lógica del ataque
     */
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external override returns (bool) {
        require(msg.sender == address(POOL), "Not pool");
        require(initiator == address(this), "Not initiator");

        // ============ PASO 1: MANIPULAR PRECIO ============
        // Swap masivo para mover precio
        // dexPool.swap(asset, largeAmount);

        // ============ PASO 2: EXPLOTAR PROTOCOLO ============
        // Usar precio manipulado para:
        // - Depositar colateral "valioso"
        // - Borrowear mucho más de lo que deberíamos
        // vulnerableLending.deposit(manipulatedToken, amount);
        // vulnerableLending.borrow(stablecoin, inflatedAmount);

        // ============ PASO 3: REVERTIR MANIPULACIÓN ============
        // Swap en dirección opuesta
        // dexPool.swap(largeAmount, asset);

        // ============ PASO 4: PAGAR FLASH LOAN ============
        uint256 amountOwed = amount + premium;
        IERC20(asset).approve(address(POOL), amountOwed);

        return true;
    }
}

// Interfaces ficticias para el ejemplo
interface IVulnerableLending {
    function deposit(address token, uint256 amount) external;
    function borrow(address token, uint256 amount) external;
}

interface IDEXPool {
    function swap(address tokenIn, uint256 amountIn) external;
}

/**
 * @title FlashLoanProtection
 * @notice Patrones para protegerse de flash loan attacks
 */
abstract contract FlashLoanProtection {

    // Tracking de balances al inicio del bloque
    mapping(address => mapping(uint256 => uint256)) private _startOfBlockBalance;

    /**
     * @notice Modifier que previene flash loans
     * @dev Requiere que el balance existiera en un bloque anterior
     */
    modifier noFlashLoan(address token, address user) {
        uint256 currentBlock = block.number;
        uint256 storedBalance = _startOfBlockBalance[user][currentBlock];

        // Si es primera interacción del bloque, guardar balance
        if (storedBalance == 0) {
            _startOfBlockBalance[user][currentBlock] = IERC20(token).balanceOf(user);
        }

        _;
    }

    /**
     * @notice Alternativa: Delay forzado entre operaciones
     */
    mapping(address => uint256) private _lastOperationBlock;

    modifier delayedOperation() {
        require(
            block.number > _lastOperationBlock[msg.sender],
            "Must wait one block"
        );
        _lastOperationBlock[msg.sender] = block.number;
        _;
    }

    /**
     * @notice Verificar que el usuario tenía tokens antes de este bloque
     */
    modifier requirePriorBalance(address token, uint256 minBlocks) {
        // En producción: usar snapshots de ERC20Votes o similar
        // para verificar balance en bloques anteriores
        _;
    }
}
```

### 4.2 Flash Loan Detection

```python
"""
CIPHER: Flash Loan Detection System
Detección de posibles flash loan attacks en tiempo real
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    hash: str
    block_number: int
    from_address: str
    to_address: str
    value: int
    gas_used: int
    input_data: str
    internal_txs: List[Dict]
    logs: List[Dict]

class FlashLoanDetector:
    """Detector de flash loan attacks"""

    # Selectores de funciones conocidas de flash loans
    FLASH_LOAN_SELECTORS = {
        "0xab9c4b5d": "flashLoan (Aave V2)",
        "0x42b0b77c": "flashLoanSimple (Aave V3)",
        "0xd9d98ce4": "flashLoan (dYdX)",
        "0x5cffe9de": "flashLoan (Balancer)",
        "0xe0232b42": "flash (Uniswap V3)"
    }

    # Contratos de flash loan providers conocidos
    FLASH_LOAN_PROVIDERS = {
        "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9": "Aave V2",
        "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2": "Aave V3",
        "0xBA12222222228d8Ba445958a75a0704d566BF2C8": "Balancer Vault",
    }

    def __init__(self):
        self.suspicious_txs: List[Dict] = []

    def analyze_transaction(self, tx: Transaction) -> Dict:
        """Analizar transacción en busca de patrones de flash loan"""
        indicators = []
        risk_score = 0

        # 1. Detectar llamadas a flash loan
        if self._has_flash_loan_call(tx):
            indicators.append("FLASH_LOAN_DETECTED")
            risk_score += 30

        # 2. Múltiples swaps en diferentes DEXs (arbitraje/manipulación)
        swap_count = self._count_swap_events(tx)
        if swap_count >= 3:
            indicators.append(f"MULTIPLE_SWAPS ({swap_count})")
            risk_score += 20

        # 3. Interacción con múltiples protocolos DeFi
        protocol_count = self._count_protocol_interactions(tx)
        if protocol_count >= 3:
            indicators.append(f"MULTI_PROTOCOL ({protocol_count})")
            risk_score += 15

        # 4. Alto gas usado (transacciones complejas)
        if tx.gas_used > 1_000_000:
            indicators.append("HIGH_GAS")
            risk_score += 10

        # 5. Préstamo y repago en misma transacción
        if self._has_circular_flow(tx):
            indicators.append("CIRCULAR_FLOW")
            risk_score += 25

        # 6. Interacción con contratos de gobernanza
        if self._interacts_with_governance(tx):
            indicators.append("GOVERNANCE_INTERACTION")
            risk_score += 20

        is_suspicious = risk_score >= 50

        result = {
            "tx_hash": tx.hash,
            "is_suspicious": is_suspicious,
            "risk_score": risk_score,
            "indicators": indicators,
            "recommendation": self._get_recommendation(risk_score)
        }

        if is_suspicious:
            self.suspicious_txs.append(result)

        return result

    def _has_flash_loan_call(self, tx: Transaction) -> bool:
        """Verificar si hay llamadas a flash loans"""
        # Verificar selector en input data
        if len(tx.input_data) >= 10:
            selector = tx.input_data[:10]
            if selector in self.FLASH_LOAN_SELECTORS:
                return True

        # Verificar en transacciones internas
        for internal in tx.internal_txs:
            if internal.get("to", "").lower() in [
                addr.lower() for addr in self.FLASH_LOAN_PROVIDERS
            ]:
                return True

        return False

    def _count_swap_events(self, tx: Transaction) -> int:
        """Contar eventos de swap en la transacción"""
        swap_topics = [
            "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822",  # Swap V2
            "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67",  # Swap V3
        ]

        return sum(
            1 for log in tx.logs
            if log.get("topics") and log["topics"][0] in swap_topics
        )

    def _count_protocol_interactions(self, tx: Transaction) -> int:
        """Contar interacciones con diferentes protocolos"""
        unique_contracts = set()

        for internal in tx.internal_txs:
            to_addr = internal.get("to", "").lower()
            if to_addr:
                unique_contracts.add(to_addr)

        return len(unique_contracts)

    def _has_circular_flow(self, tx: Transaction) -> bool:
        """Detectar flujo circular de fondos (préstamo y repago)"""
        # Buscar Transfer events del mismo token
        transfers = {}

        for log in tx.logs:
            if not log.get("topics"):
                continue

            # Transfer topic
            if log["topics"][0] == "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef":
                token = log.get("address", "").lower()
                if token not in transfers:
                    transfers[token] = {"in": 0, "out": 0}

                # Analizar dirección del transfer
                # En producción: decodificar topics para from/to

        # Si hay token con in ≈ out, es circular
        for token, flow in transfers.items():
            if flow["in"] > 0 and flow["out"] > 0:
                ratio = min(flow["in"], flow["out"]) / max(flow["in"], flow["out"])
                if ratio > 0.95:  # 95%+ circular
                    return True

        return False

    def _interacts_with_governance(self, tx: Transaction) -> bool:
        """Verificar interacción con contratos de gobernanza"""
        governance_selectors = [
            "0xda95691a",  # castVote
            "0x56781388",  # castVoteWithReason
            "0x7d5e81e2",  # propose
        ]

        if len(tx.input_data) >= 10:
            selector = tx.input_data[:10]
            if selector in governance_selectors:
                return True

        return False

    def _get_recommendation(self, risk_score: int) -> str:
        """Obtener recomendación basada en risk score"""
        if risk_score >= 70:
            return "HIGH RISK - Likely exploit. Investigate immediately."
        elif risk_score >= 50:
            return "MEDIUM RISK - Suspicious activity. Monitor closely."
        elif risk_score >= 30:
            return "LOW RISK - Unusual but possibly legitimate."
        else:
            return "NORMAL - No significant risk indicators."

    def get_attack_pattern(self, tx: Transaction) -> Optional[str]:
        """Identificar patrón de ataque específico"""
        indicators = self.analyze_transaction(tx)["indicators"]

        if "FLASH_LOAN_DETECTED" in indicators and "GOVERNANCE_INTERACTION" in indicators:
            return "GOVERNANCE_FLASH_LOAN_ATTACK"

        if "FLASH_LOAN_DETECTED" in indicators and "MULTIPLE_SWAPS" in [i.split()[0] for i in indicators]:
            return "ORACLE_MANIPULATION_ATTACK"

        if "FLASH_LOAN_DETECTED" in indicators and "CIRCULAR_FLOW" in indicators:
            return "ARBITRAGE_OR_EXPLOIT"

        return None
```

---

## 5. ECONOMIC EXPLOITS

### 5.1 Price Manipulation Scenarios

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title EconomicExploitPrevention
 * @notice Técnicas para prevenir exploits económicos
 */

// ============ VULNERABLE: Liquidación cascada ============
contract VulnerableLiquidations {
    mapping(address => uint256) public collateral;
    mapping(address => uint256) public debt;

    uint256 public constant LIQUIDATION_THRESHOLD = 150; // 150%

    // VULNERABLE: Sin límites, permite liquidaciones cascada
    function liquidate(address user) external {
        uint256 ratio = (collateral[user] * 100) / debt[user];
        require(ratio < LIQUIDATION_THRESHOLD, "Not liquidatable");

        // Liquidar todo de una vez - puede causar cascada
        uint256 seized = collateral[user];
        collateral[user] = 0;
        debt[user] = 0;

        // Vender colateral en mercado - puede crashear precio
        // Causar más liquidaciones...
    }
}

// ============ MITIGACIÓN: Liquidaciones graduales ============
contract GradualLiquidations {
    mapping(address => uint256) public collateral;
    mapping(address => uint256) public debt;

    // Límites de liquidación
    uint256 public constant MAX_LIQUIDATION_PERCENT = 50; // Máx 50% por liquidación
    uint256 public constant LIQUIDATION_COOLDOWN = 1 hours;
    uint256 public constant GLOBAL_LIQUIDATION_CAP = 1_000_000e18; // Cap global por hora

    mapping(address => uint256) public lastLiquidation;
    uint256 public hourlyLiquidationVolume;
    uint256 public lastHourReset;

    function liquidate(address user, uint256 percentage) external {
        require(percentage <= MAX_LIQUIDATION_PERCENT, "Exceeds max");

        // Cooldown per user
        require(
            block.timestamp >= lastLiquidation[user] + LIQUIDATION_COOLDOWN,
            "Cooldown active"
        );

        // Global cap
        _resetHourlyIfNeeded();
        uint256 liquidationValue = (collateral[user] * percentage) / 100;
        require(
            hourlyLiquidationVolume + liquidationValue <= GLOBAL_LIQUIDATION_CAP,
            "Global cap reached"
        );

        // Ejecutar liquidación parcial
        uint256 seizedCollateral = (collateral[user] * percentage) / 100;
        uint256 clearedDebt = (debt[user] * percentage) / 100;

        collateral[user] -= seizedCollateral;
        debt[user] -= clearedDebt;

        lastLiquidation[user] = block.timestamp;
        hourlyLiquidationVolume += liquidationValue;
    }

    function _resetHourlyIfNeeded() internal {
        if (block.timestamp >= lastHourReset + 1 hours) {
            hourlyLiquidationVolume = 0;
            lastHourReset = block.timestamp;
        }
    }
}

// ============ BAD DEBT SOCIALIZATION ============
contract BadDebtHandler {

    uint256 public totalDeposits;
    uint256 public totalBadDebt;
    mapping(address => uint256) public deposits;

    /**
     * @notice Socializar bad debt entre depositantes
     * @dev Usado cuando liquidación no cubre toda la deuda
     */
    function socializeBadDebt(uint256 badDebtAmount) external {
        totalBadDebt += badDebtAmount;

        // Bad debt reduce el valor de todos los depósitos proporcionalmente
        // En producción: implementar con shares similar a ERC4626
    }

    /**
     * @notice Obtener valor real del depósito después de bad debt
     */
    function getEffectiveDeposit(address user) external view returns (uint256) {
        if (totalDeposits == 0) return 0;

        uint256 userShare = (deposits[user] * 1e18) / totalDeposits;
        uint256 badDebtShare = (totalBadDebt * userShare) / 1e18;

        return deposits[user] > badDebtShare ? deposits[user] - badDebtShare : 0;
    }
}

// ============ INTEREST RATE MANIPULATION PREVENTION ============
contract StableInterestRate {

    uint256 public baseRate;
    uint256 public utilizationOptimal = 80; // 80%
    uint256 public slopeBelow = 4; // 4% below optimal
    uint256 public slopeAbove = 75; // 75% above optimal (disuade alto util)

    // Límites de cambio
    uint256 public constant MAX_RATE_CHANGE_PER_BLOCK = 10; // 0.1%
    uint256 public lastRateUpdate;
    uint256 public lastRate;

    function calculateInterestRate(
        uint256 utilization
    ) public view returns (uint256) {
        uint256 newRate;

        if (utilization <= utilizationOptimal) {
            newRate = baseRate + (utilization * slopeBelow) / utilizationOptimal;
        } else {
            uint256 excessUtil = utilization - utilizationOptimal;
            newRate = baseRate + slopeBelow +
                      (excessUtil * slopeAbove) / (100 - utilizationOptimal);
        }

        // Aplicar límite de cambio
        return _applyRateChangeLimit(newRate);
    }

    function _applyRateChangeLimit(uint256 targetRate) internal view returns (uint256) {
        if (lastRateUpdate == 0) return targetRate;

        uint256 blocksPassed = block.number - lastRateUpdate;
        uint256 maxChange = blocksPassed * MAX_RATE_CHANGE_PER_BLOCK;

        if (targetRate > lastRate) {
            uint256 increase = targetRate - lastRate;
            return lastRate + (increase > maxChange ? maxChange : increase);
        } else {
            uint256 decrease = lastRate - targetRate;
            return lastRate - (decrease > maxChange ? maxChange : decrease);
        }
    }
}
```

### 5.2 Death Spiral Prevention

```python
"""
CIPHER: Death Spiral Detection & Prevention
Detectar y prevenir espirales de muerte en stablecoins/tokens
"""

from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

class SpiralPhase(Enum):
    NORMAL = "normal"
    EARLY_WARNING = "early_warning"
    DANGER = "danger"
    CRITICAL = "critical"
    DEATH_SPIRAL = "death_spiral"

@dataclass
class TokenMetrics:
    price: float
    peg_target: float
    collateral_ratio: float  # % (150 = 150%)
    redemption_queue: float  # USD in queue
    liquidity_depth: float   # USD available
    holder_count: int
    large_holder_percentage: float  # Top 10 holders

class DeathSpiralDetector:
    """Detector de espirales de muerte en sistemas tokenizados"""

    def __init__(self, token_name: str):
        self.token_name = token_name
        self.history: List[TokenMetrics] = []
        self.alerts: List[Dict] = []

    def add_metrics(self, metrics: TokenMetrics):
        self.history.append(metrics)

        # Analizar cada nueva entrada
        analysis = self.analyze_current_state()
        if analysis["phase"] != SpiralPhase.NORMAL:
            self.alerts.append({
                "timestamp": len(self.history),
                "phase": analysis["phase"].value,
                "indicators": analysis["indicators"]
            })

    def analyze_current_state(self) -> Dict:
        """Analizar estado actual y detectar señales de espiral"""
        if len(self.history) < 2:
            return {"phase": SpiralPhase.NORMAL, "indicators": []}

        current = self.history[-1]
        previous = self.history[-2]

        indicators = []
        risk_score = 0

        # 1. Depeg Analysis
        depeg = abs(current.price - current.peg_target) / current.peg_target
        if depeg > 0.05:  # >5% depeg
            indicators.append(f"DEPEG: {depeg*100:.1f}%")
            risk_score += 30

        # 2. Collateral Ratio Decline
        if current.collateral_ratio < previous.collateral_ratio:
            decline = previous.collateral_ratio - current.collateral_ratio
            if decline > 10:  # >10% decline
                indicators.append(f"CR_DECLINE: {decline:.1f}%")
                risk_score += 25

        # 3. Undercollateralization
        if current.collateral_ratio < 100:
            indicators.append(f"UNDERCOLLATERALIZED: {current.collateral_ratio:.1f}%")
            risk_score += 40

        # 4. Bank Run Detection
        if current.redemption_queue > current.liquidity_depth * 0.5:
            indicators.append("REDEMPTION_PRESSURE")
            risk_score += 20

        # 5. Liquidity Crisis
        if current.liquidity_depth < self.history[0].liquidity_depth * 0.3:
            indicators.append("LIQUIDITY_CRISIS")
            risk_score += 25

        # 6. Holder Concentration
        if current.large_holder_percentage > 60:
            indicators.append("HIGH_CONCENTRATION")
            risk_score += 15

        # 7. Momentum (consecutive bad metrics)
        if len(self.history) >= 5:
            consecutive_depeg = sum(
                1 for m in self.history[-5:]
                if abs(m.price - m.peg_target) / m.peg_target > 0.02
            )
            if consecutive_depeg >= 4:
                indicators.append("SUSTAINED_DEPEG")
                risk_score += 20

        # Determine phase
        phase = self._score_to_phase(risk_score)

        return {
            "phase": phase,
            "risk_score": risk_score,
            "indicators": indicators,
            "recommendations": self._get_recommendations(phase)
        }

    def _score_to_phase(self, score: int) -> SpiralPhase:
        if score >= 80:
            return SpiralPhase.DEATH_SPIRAL
        elif score >= 60:
            return SpiralPhase.CRITICAL
        elif score >= 40:
            return SpiralPhase.DANGER
        elif score >= 20:
            return SpiralPhase.EARLY_WARNING
        else:
            return SpiralPhase.NORMAL

    def _get_recommendations(self, phase: SpiralPhase) -> List[str]:
        recommendations = {
            SpiralPhase.NORMAL: [
                "Continue monitoring",
                "Maintain healthy reserves"
            ],
            SpiralPhase.EARLY_WARNING: [
                "Increase monitoring frequency",
                "Prepare contingency plans",
                "Consider reducing exposure"
            ],
            SpiralPhase.DANGER: [
                "Activate emergency procedures",
                "Halt new minting",
                "Communicate with community",
                "Prepare liquidity injection"
            ],
            SpiralPhase.CRITICAL: [
                "Execute emergency shutdown if available",
                "Maximize liquidity provision",
                "Consider emergency governance vote",
                "Coordinate with exchanges on trading halts"
            ],
            SpiralPhase.DEATH_SPIRAL: [
                "Activate protocol emergency shutdown",
                "Protect remaining collateral",
                "Document for post-mortem",
                "Coordinate orderly wind-down"
            ]
        }
        return recommendations.get(phase, [])

    def simulate_scenario(
        self,
        initial_metrics: TokenMetrics,
        redemption_rate: float,  # % por período
        price_impact: float,     # Impacto en precio por redención
        periods: int
    ) -> Dict:
        """Simular escenario de estrés"""
        simulated = [initial_metrics]

        for i in range(periods):
            prev = simulated[-1]

            # Calcular redenciones
            redemptions = prev.liquidity_depth * redemption_rate

            # Nuevo precio (afectado por redenciones)
            new_price = prev.price * (1 - price_impact * redemption_rate)

            # Nuevo ratio de colateral (si precio del colateral también cae)
            new_cr = prev.collateral_ratio * (1 - price_impact * 0.5)

            # Nueva liquidez
            new_liquidity = prev.liquidity_depth * (1 - redemption_rate)

            simulated.append(TokenMetrics(
                price=new_price,
                peg_target=prev.peg_target,
                collateral_ratio=new_cr,
                redemption_queue=redemptions,
                liquidity_depth=new_liquidity,
                holder_count=int(prev.holder_count * 0.95),
                large_holder_percentage=min(
                    prev.large_holder_percentage * 1.05,
                    100
                )
            ))

        # Encontrar punto de no retorno
        for i, metrics in enumerate(simulated):
            self.add_metrics(metrics)
            analysis = self.analyze_current_state()
            if analysis["phase"] == SpiralPhase.DEATH_SPIRAL:
                return {
                    "survives": False,
                    "death_spiral_period": i,
                    "final_price": metrics.price,
                    "final_cr": metrics.collateral_ratio
                }

        return {
            "survives": True,
            "final_price": simulated[-1].price,
            "final_cr": simulated[-1].collateral_ratio
        }


# Ejemplo de uso
if __name__ == "__main__":
    detector = DeathSpiralDetector("UST")  # Ejemplo histórico

    # Simular métricas previas al colapso
    metrics_sequence = [
        TokenMetrics(1.00, 1.00, 100, 0, 1_000_000_000, 100000, 25),
        TokenMetrics(0.98, 1.00, 95, 500_000_000, 800_000_000, 95000, 28),
        TokenMetrics(0.95, 1.00, 85, 1_000_000_000, 500_000_000, 85000, 32),
        TokenMetrics(0.80, 1.00, 70, 2_000_000_000, 200_000_000, 70000, 40),
        TokenMetrics(0.50, 1.00, 40, 3_000_000_000, 50_000_000, 50000, 55),
    ]

    for m in metrics_sequence:
        detector.add_metrics(m)
        result = detector.analyze_current_state()
        print(f"Price: ${m.price:.2f} | Phase: {result['phase'].value} | Indicators: {result['indicators']}")
```

---

## 6. MEV Y FRONT-RUNNING

### 6.1 MEV Protection Strategies

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title MEVProtection
 * @notice Técnicas para protegerse de MEV extraction
 */

// ============ VULNERABLE: Sin protección ============
contract VulnerableSwap {
    // Cualquiera puede ver el swap en mempool y front-run
    function swap(
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        uint256 minAmountOut
    ) external {
        // ...swap logic
    }
}

// ============ PROTECCIÓN 1: Commit-Reveal ============
contract CommitRevealSwap {

    struct Commitment {
        bytes32 hash;
        uint256 block;
        bool revealed;
    }

    mapping(address => Commitment) public commitments;

    uint256 public constant REVEAL_DELAY = 2; // 2 blocks
    uint256 public constant REVEAL_WINDOW = 10; // 10 blocks

    /**
     * @notice Fase 1: Commit hash de la transacción
     */
    function commit(bytes32 hash) external {
        commitments[msg.sender] = Commitment({
            hash: hash,
            block: block.number,
            revealed: false
        });
    }

    /**
     * @notice Fase 2: Reveal y ejecutar swap
     */
    function reveal(
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        uint256 minAmountOut,
        bytes32 salt
    ) external {
        Commitment storage commitment = commitments[msg.sender];

        // Verificar timing
        require(
            block.number >= commitment.block + REVEAL_DELAY,
            "Too early"
        );
        require(
            block.number <= commitment.block + REVEAL_DELAY + REVEAL_WINDOW,
            "Too late"
        );

        // Verificar hash
        bytes32 expectedHash = keccak256(abi.encodePacked(
            tokenIn,
            tokenOut,
            amountIn,
            minAmountOut,
            salt
        ));
        require(commitment.hash == expectedHash, "Invalid reveal");
        require(!commitment.revealed, "Already revealed");

        commitment.revealed = true;

        // Ejecutar swap (ahora es demasiado tarde para front-run)
        _executeSwap(tokenIn, tokenOut, amountIn, minAmountOut);
    }

    function _executeSwap(
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        uint256 minAmountOut
    ) internal {
        // Implementación del swap
    }
}

// ============ PROTECCIÓN 2: Flashbots/Private Mempool ============
/**
 * @notice Para usar Flashbots, enviar tx a:
 * - Mainnet: https://relay.flashbots.net
 * - Bundle múltiples txs para atomicidad
 *
 * Ejemplo en ethers.js:
 *
 * const flashbotsProvider = await FlashbotsBundleProvider.create(
 *     provider,
 *     wallet,
 *     'https://relay.flashbots.net'
 * );
 *
 * const bundle = [
 *     { signedTransaction: signedTx1 },
 *     { signedTransaction: signedTx2 }
 * ];
 *
 * await flashbotsProvider.sendBundle(bundle, targetBlock);
 */

// ============ PROTECCIÓN 3: Slippage dinámico ============
contract DynamicSlippageSwap {

    uint256 public constant BASE_SLIPPAGE = 50; // 0.5%
    uint256 public constant MAX_SLIPPAGE = 500; // 5%

    mapping(address => mapping(address => uint256)) public recentVolume;
    mapping(address => mapping(address => uint256)) public lastVolumeUpdate;

    /**
     * @notice Calcular slippage basado en condiciones de mercado
     */
    function calculateDynamicSlippage(
        address tokenIn,
        address tokenOut,
        uint256 amountIn
    ) public view returns (uint256 slippageBps) {
        // Base slippage
        slippageBps = BASE_SLIPPAGE;

        // Aumentar si hay mucho volumen reciente (posible manipulación)
        uint256 recent = recentVolume[tokenIn][tokenOut];
        if (recent > 0 && block.timestamp - lastVolumeUpdate[tokenIn][tokenOut] < 5 minutes) {
            // Si el trade es >10% del volumen reciente, aumentar slippage
            if (amountIn > recent / 10) {
                slippageBps += 100; // +1%
            }
        }

        // Cap máximo
        if (slippageBps > MAX_SLIPPAGE) {
            slippageBps = MAX_SLIPPAGE;
        }
    }

    function swap(
        address tokenIn,
        address tokenOut,
        uint256 amountIn
    ) external returns (uint256 amountOut) {
        uint256 slippage = calculateDynamicSlippage(tokenIn, tokenOut, amountIn);

        // Obtener quote
        uint256 expectedOut = _getQuote(tokenIn, tokenOut, amountIn);
        uint256 minOut = expectedOut * (10000 - slippage) / 10000;

        // Ejecutar con minOut calculado
        amountOut = _executeSwap(tokenIn, tokenOut, amountIn, minOut);

        // Actualizar volumen
        recentVolume[tokenIn][tokenOut] += amountIn;
        lastVolumeUpdate[tokenIn][tokenOut] = block.timestamp;
    }

    function _getQuote(address, address, uint256) internal pure returns (uint256) {
        return 0; // Implementar
    }

    function _executeSwap(address, address, uint256, uint256) internal pure returns (uint256) {
        return 0; // Implementar
    }
}

// ============ PROTECCIÓN 4: Time-Weighted Orders ============
contract TWAPOrder {

    struct Order {
        address tokenIn;
        address tokenOut;
        uint256 totalAmount;
        uint256 executedAmount;
        uint256 chunks;
        uint256 interval;
        uint256 lastExecution;
        uint256 minPrice;
        address owner;
    }

    mapping(uint256 => Order) public orders;
    uint256 public orderCount;

    /**
     * @notice Crear orden TWAP para ejecutar en chunks
     */
    function createTWAPOrder(
        address tokenIn,
        address tokenOut,
        uint256 amount,
        uint256 chunks,
        uint256 interval, // Segundos entre chunks
        uint256 minPrice
    ) external returns (uint256 orderId) {
        orderId = orderCount++;

        orders[orderId] = Order({
            tokenIn: tokenIn,
            tokenOut: tokenOut,
            totalAmount: amount,
            executedAmount: 0,
            chunks: chunks,
            interval: interval,
            lastExecution: 0,
            minPrice: minPrice,
            owner: msg.sender
        });

        // Transfer tokens to contract
        IERC20(tokenIn).transferFrom(msg.sender, address(this), amount);
    }

    /**
     * @notice Ejecutar siguiente chunk de orden TWAP
     */
    function executeChunk(uint256 orderId) external {
        Order storage order = orders[orderId];

        require(order.executedAmount < order.totalAmount, "Order complete");
        require(
            block.timestamp >= order.lastExecution + order.interval,
            "Too soon"
        );

        uint256 chunkSize = order.totalAmount / order.chunks;
        uint256 remaining = order.totalAmount - order.executedAmount;

        if (chunkSize > remaining) {
            chunkSize = remaining;
        }

        // Ejecutar swap del chunk
        // ... implementar swap con verificación de minPrice

        order.executedAmount += chunkSize;
        order.lastExecution = block.timestamp;
    }
}

interface IERC20 {
    function transferFrom(address, address, uint256) external returns (bool);
}
```

---

## 7. RISK MITIGATION STRATEGIES

### 7.1 Security Checklist

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DEFI SECURITY CHECKLIST                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PRE-DEPLOYMENT                                                              │
│  □ Múltiples auditorías independientes (mínimo 2)                           │
│  □ Bug bounty program activo                                                 │
│  □ Formal verification de funciones críticas                                │
│  □ Test coverage > 90%                                                       │
│  □ Fuzzing extensivo                                                         │
│  □ Review de dependencias                                                    │
│                                                                              │
│  ACCESS CONTROL                                                              │
│  □ Multisig para admin functions (5/9 recomendado)                          │
│  □ Timelock en cambios críticos (48h+ recomendado)                          │
│  □ Roles granulares (OpenZeppelin AccessControl)                            │
│  □ Emergency pause mechanism                                                 │
│  □ No usar tx.origin para auth                                              │
│                                                                              │
│  SMART CONTRACT                                                              │
│  □ ReentrancyGuard en funciones con external calls                          │
│  □ Checks-Effects-Interactions pattern                                       │
│  □ SafeERC20 para interacciones con tokens                                  │
│  □ Overflow protection (Solidity 0.8+ o SafeMath)                           │
│  □ No delegatecall a contratos no confiables                                │
│                                                                              │
│  ORACLES                                                                     │
│  □ Múltiples fuentes de precio                                              │
│  □ Heartbeat checks (staleness)                                             │
│  □ Deviation limits                                                          │
│  □ Fallback oracles                                                          │
│  □ TWAP con período suficiente (30min+)                                     │
│                                                                              │
│  ECONOMIC                                                                    │
│  □ Caps en operaciones por bloque/hora                                      │
│  □ Gradual liquidations                                                      │
│  □ Slippage protection                                                       │
│  □ Flash loan resistance                                                     │
│  □ Insurance fund / bad debt handling                                        │
│                                                                              │
│  MONITORING                                                                  │
│  □ Real-time alerts para eventos anómalos                                   │
│  □ TVL monitoring                                                            │
│  □ Large transaction alerts                                                  │
│  □ Governance proposal monitoring                                            │
│  □ Oracle deviation alerts                                                   │
│                                                                              │
│  INCIDENT RESPONSE                                                           │
│  □ Documented runbook                                                        │
│  □ Emergency contacts                                                        │
│  □ Pause procedures                                                          │
│  □ Communication templates                                                   │
│  □ Post-mortem process                                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Emergency Response Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/AccessControl.sol";

/**
 * @title EmergencyResponse
 * @notice Sistema de respuesta a emergencias para protocolos DeFi
 */
contract EmergencyResponse is AccessControl {

    bytes32 public constant GUARDIAN_ROLE = keccak256("GUARDIAN_ROLE");
    bytes32 public constant EMERGENCY_ROLE = keccak256("EMERGENCY_ROLE");

    enum EmergencyLevel { NONE, WARNING, CRITICAL, SHUTDOWN }

    struct ProtocolState {
        EmergencyLevel level;
        bool depositsEnabled;
        bool withdrawalsEnabled;
        bool borrowingEnabled;
        bool liquidationsEnabled;
        uint256 lastUpdate;
        string reason;
    }

    ProtocolState public state;

    // Contratos protegidos
    address[] public protectedContracts;

    // Timelock para salir de emergencia
    uint256 public constant EMERGENCY_EXIT_DELAY = 24 hours;
    uint256 public emergencyExitTimestamp;

    event EmergencyDeclared(EmergencyLevel level, string reason);
    event EmergencyExitInitiated(uint256 exitTimestamp);
    event EmergencyResolved();

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(GUARDIAN_ROLE, msg.sender);

        state = ProtocolState({
            level: EmergencyLevel.NONE,
            depositsEnabled: true,
            withdrawalsEnabled: true,
            borrowingEnabled: true,
            liquidationsEnabled: true,
            lastUpdate: block.timestamp,
            reason: ""
        });
    }

    /**
     * @notice Declarar emergencia nivel WARNING
     * @dev Deshabilita nuevos depósitos y borrowing
     */
    function declareWarning(
        string calldata reason
    ) external onlyRole(GUARDIAN_ROLE) {
        state.level = EmergencyLevel.WARNING;
        state.depositsEnabled = false;
        state.borrowingEnabled = false;
        state.lastUpdate = block.timestamp;
        state.reason = reason;

        _notifyProtectedContracts();

        emit EmergencyDeclared(EmergencyLevel.WARNING, reason);
    }

    /**
     * @notice Declarar emergencia nivel CRITICAL
     * @dev Solo permite withdrawals
     */
    function declareCritical(
        string calldata reason
    ) external onlyRole(GUARDIAN_ROLE) {
        state.level = EmergencyLevel.CRITICAL;
        state.depositsEnabled = false;
        state.borrowingEnabled = false;
        state.liquidationsEnabled = false;
        // withdrawals siguen habilitados
        state.lastUpdate = block.timestamp;
        state.reason = reason;

        _notifyProtectedContracts();

        emit EmergencyDeclared(EmergencyLevel.CRITICAL, reason);
    }

    /**
     * @notice Shutdown completo del protocolo
     * @dev Solo rol EMERGENCY (multisig de emergencia)
     */
    function declareShutdown(
        string calldata reason
    ) external onlyRole(EMERGENCY_ROLE) {
        state.level = EmergencyLevel.SHUTDOWN;
        state.depositsEnabled = false;
        state.withdrawalsEnabled = false;
        state.borrowingEnabled = false;
        state.liquidationsEnabled = false;
        state.lastUpdate = block.timestamp;
        state.reason = reason;

        _notifyProtectedContracts();

        emit EmergencyDeclared(EmergencyLevel.SHUTDOWN, reason);
    }

    /**
     * @notice Iniciar proceso de salida de emergencia
     * @dev Requiere timelock para prevenir abuso
     */
    function initiateEmergencyExit() external onlyRole(DEFAULT_ADMIN_ROLE) {
        require(state.level != EmergencyLevel.NONE, "No emergency");

        emergencyExitTimestamp = block.timestamp + EMERGENCY_EXIT_DELAY;

        emit EmergencyExitInitiated(emergencyExitTimestamp);
    }

    /**
     * @notice Resolver emergencia después del timelock
     */
    function resolveEmergency() external onlyRole(DEFAULT_ADMIN_ROLE) {
        require(emergencyExitTimestamp > 0, "Exit not initiated");
        require(block.timestamp >= emergencyExitTimestamp, "Timelock active");

        state = ProtocolState({
            level: EmergencyLevel.NONE,
            depositsEnabled: true,
            withdrawalsEnabled: true,
            borrowingEnabled: true,
            liquidationsEnabled: true,
            lastUpdate: block.timestamp,
            reason: ""
        });

        emergencyExitTimestamp = 0;

        _notifyProtectedContracts();

        emit EmergencyResolved();
    }

    /**
     * @notice Verificar si una acción está permitida
     */
    function isActionAllowed(bytes4 action) external view returns (bool) {
        // Mapping de acciones a estados
        if (action == bytes4(keccak256("deposit"))) {
            return state.depositsEnabled;
        } else if (action == bytes4(keccak256("withdraw"))) {
            return state.withdrawalsEnabled;
        } else if (action == bytes4(keccak256("borrow"))) {
            return state.borrowingEnabled;
        } else if (action == bytes4(keccak256("liquidate"))) {
            return state.liquidationsEnabled;
        }
        return true;
    }

    /**
     * @notice Notificar contratos protegidos del cambio de estado
     */
    function _notifyProtectedContracts() internal {
        for (uint256 i = 0; i < protectedContracts.length; i++) {
            // Llamar updateEmergencyState en cada contrato
            (bool success, ) = protectedContracts[i].call(
                abi.encodeWithSignature(
                    "updateEmergencyState(uint8)",
                    uint8(state.level)
                )
            );
            // No revertir si falla - continuar notificando otros
        }
    }

    /**
     * @notice Agregar contrato protegido
     */
    function addProtectedContract(
        address _contract
    ) external onlyRole(DEFAULT_ADMIN_ROLE) {
        protectedContracts.push(_contract);
    }
}
```

---

## CONEXIONES NEURALES

```
NEURONA_DEFI_RISKS (C40011)
├── DEPENDE DE
│   ├── NEURONA_SMART_CONTRACTS (C30001) - Vulnerability patterns
│   ├── NEURONA_DEX_AMM (C40001) - Price manipulation
│   └── NEURONA_LENDING (C40002) - Liquidation risks
│
├── CONECTA CON
│   ├── NEURONA_PROTOCOL_ANALYSIS (C40010) - Risk scoring
│   ├── NEURONA_GOVERNANCE (C40009) - Governance attacks
│   └── NEURONA_SECURITY (C60001) - General security
│
└── HABILITA
    ├── Identificación de vulnerabilidades
    ├── Diseño de sistemas seguros
    ├── Respuesta a incidentes
    └── Due diligence de protocolos
```

---

## FIRMA CIPHER

```
╔═══════════════════════════════════════════════════════════════╗
║  NEURONA: C40011                                              ║
║  TIPO: DeFi Security & Risk Management                        ║
║  VERSIÓN: 1.0.0                                               ║
║  ESTADO: ACTIVA                                               ║
║                                                               ║
║  "En DeFi, la seguridad no es una feature,                   ║
║   es el producto."                                            ║
║                                                               ║
║  CIPHER_CORE::DEFI_RISKS::INITIALIZED                         ║
╚═══════════════════════════════════════════════════════════════╝
```
