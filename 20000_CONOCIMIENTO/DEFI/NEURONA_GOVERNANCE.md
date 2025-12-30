# NEURONA C40009: DAO GOVERNANCE & VOTING SYSTEMS

> **CIPHER**: Dominio completo de gobernanza descentralizada, sistemas de votación, y estructuras DAO.

---

## ÍNDICE

1. [Fundamentos de Gobernanza](#1-fundamentos-de-gobernanza)
2. [Sistemas de Votación On-Chain](#2-sistemas-de-votación-on-chain)
3. [Timelock y Ejecución](#3-timelock-y-ejecución)
4. [Modelos de Gobernanza](#4-modelos-de-gobernanza)
5. [Delegación y Representación](#5-delegación-y-representación)
6. [Optimistic Governance](#6-optimistic-governance)
7. [Análisis de Governance Attacks](#7-análisis-de-governance-attacks)

---

## 1. FUNDAMENTOS DE GOBERNANZA

### 1.1 Componentes Core

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DAO GOVERNANCE ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────────┐      │
│   │   TOKEN     │────▶│   VOTING    │────▶│    TIMELOCK     │      │
│   │  HOLDERS    │     │   SYSTEM    │     │    CONTROLLER   │      │
│   └─────────────┘     └─────────────┘     └─────────────────┘      │
│         │                   │                     │                 │
│         ▼                   ▼                     ▼                 │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────────┐      │
│   │ DELEGATION  │     │  PROPOSAL   │     │    EXECUTION    │      │
│   │   SYSTEM    │     │   QUEUE     │     │     TARGET      │      │
│   └─────────────┘     └─────────────┘     └─────────────────┘      │
│                                                                      │
│   FLOW: Propose → Vote → Queue → Execute (after timelock)          │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 Governance Token con Delegación (ERC20Votes)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";

/**
 * @title GovernanceToken
 * @notice Token de gobernanza con snapshots de votos y delegación
 * @dev Implementa ERC20Votes para voting power checkpoints
 */
contract GovernanceToken is ERC20, ERC20Permit, ERC20Votes {
    uint256 public constant MAX_SUPPLY = 100_000_000 * 1e18; // 100M tokens

    constructor()
        ERC20("CIPHER Governance", "CGOV")
        ERC20Permit("CIPHER Governance")
    {
        _mint(msg.sender, MAX_SUPPLY);
    }

    /**
     * @notice Override requerido para ERC20Votes
     * @dev Actualiza checkpoints en cada transfer
     */
    function _update(
        address from,
        address to,
        uint256 amount
    ) internal override(ERC20, ERC20Votes) {
        super._update(from, to, amount);
    }

    /**
     * @notice Nonces para permit
     */
    function nonces(address owner)
        public
        view
        override(ERC20Permit, Nonces)
        returns (uint256)
    {
        return super.nonces(owner);
    }

    /**
     * @notice Delegar votos a otro address
     * @dev Los tokens permanecen, solo se delega voting power
     */
    function delegateVotes(address delegatee) external {
        delegate(delegatee);
    }

    /**
     * @notice Obtener voting power en un bloque específico
     * @param account Address a consultar
     * @param blockNumber Bloque del snapshot
     */
    function getVotingPower(
        address account,
        uint256 blockNumber
    ) external view returns (uint256) {
        return getPastVotes(account, blockNumber);
    }

    /**
     * @notice Total supply en un bloque específico
     * @dev Usado para calcular quórum
     */
    function getTotalSupplyAt(uint256 blockNumber) external view returns (uint256) {
        return getPastTotalSupply(blockNumber);
    }
}
```

---

## 2. SISTEMAS DE VOTACIÓN ON-CHAIN

### 2.1 Governor Contract (OpenZeppelin Style)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/governance/Governor.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorSettings.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorCountingSimple.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorVotes.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorVotesQuorumFraction.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorTimelockControl.sol";

/**
 * @title CipherGovernor
 * @notice Sistema de gobernanza completo con timelock
 * @dev Basado en OpenZeppelin Governor modular
 */
contract CipherGovernor is
    Governor,
    GovernorSettings,
    GovernorCountingSimple,
    GovernorVotes,
    GovernorVotesQuorumFraction,
    GovernorTimelockControl
{
    // Thresholds
    uint256 public proposalThresholdValue;

    // Proposal tracking
    mapping(uint256 => ProposalMetadata) public proposalMetadata;

    struct ProposalMetadata {
        string title;
        string description;
        string discussionLink;
        uint256 createdAt;
    }

    event ProposalCreatedWithMetadata(
        uint256 indexed proposalId,
        string title,
        string discussionLink
    );

    constructor(
        IVotes _token,
        TimelockController _timelock,
        uint48 _votingDelay,      // Bloques antes de que empiece votación
        uint32 _votingPeriod,      // Bloques de duración de votación
        uint256 _proposalThreshold, // Tokens mínimos para proponer
        uint256 _quorumPercentage   // % del total supply para quórum
    )
        Governor("CIPHER Governor")
        GovernorSettings(_votingDelay, _votingPeriod, _proposalThreshold)
        GovernorVotes(_token)
        GovernorVotesQuorumFraction(_quorumPercentage)
        GovernorTimelockControl(_timelock)
    {
        proposalThresholdValue = _proposalThreshold;
    }

    /**
     * @notice Crear propuesta con metadata adicional
     */
    function proposeWithMetadata(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        string memory description,
        string memory title,
        string memory discussionLink
    ) external returns (uint256 proposalId) {
        proposalId = propose(targets, values, calldatas, description);

        proposalMetadata[proposalId] = ProposalMetadata({
            title: title,
            description: description,
            discussionLink: discussionLink,
            createdAt: block.timestamp
        });

        emit ProposalCreatedWithMetadata(proposalId, title, discussionLink);
    }

    /**
     * @notice Votar con razón
     * @param proposalId ID de la propuesta
     * @param support 0=Against, 1=For, 2=Abstain
     * @param reason Justificación del voto
     */
    function castVoteWithReason(
        uint256 proposalId,
        uint8 support,
        string calldata reason
    ) public override returns (uint256) {
        return super.castVoteWithReason(proposalId, support, reason);
    }

    // ============ OVERRIDES REQUERIDOS ============

    function votingDelay()
        public
        view
        override(Governor, GovernorSettings)
        returns (uint256)
    {
        return super.votingDelay();
    }

    function votingPeriod()
        public
        view
        override(Governor, GovernorSettings)
        returns (uint256)
    {
        return super.votingPeriod();
    }

    function quorum(uint256 blockNumber)
        public
        view
        override(Governor, GovernorVotesQuorumFraction)
        returns (uint256)
    {
        return super.quorum(blockNumber);
    }

    function state(uint256 proposalId)
        public
        view
        override(Governor, GovernorTimelockControl)
        returns (ProposalState)
    {
        return super.state(proposalId);
    }

    function proposalNeedsQueuing(uint256 proposalId)
        public
        view
        override(Governor, GovernorTimelockControl)
        returns (bool)
    {
        return super.proposalNeedsQueuing(proposalId);
    }

    function proposalThreshold()
        public
        view
        override(Governor, GovernorSettings)
        returns (uint256)
    {
        return super.proposalThreshold();
    }

    function _queueOperations(
        uint256 proposalId,
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        bytes32 descriptionHash
    ) internal override(Governor, GovernorTimelockControl) returns (uint48) {
        return super._queueOperations(
            proposalId, targets, values, calldatas, descriptionHash
        );
    }

    function _executeOperations(
        uint256 proposalId,
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        bytes32 descriptionHash
    ) internal override(Governor, GovernorTimelockControl) {
        super._executeOperations(
            proposalId, targets, values, calldatas, descriptionHash
        );
    }

    function _cancel(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        bytes32 descriptionHash
    ) internal override(Governor, GovernorTimelockControl) returns (uint256) {
        return super._cancel(targets, values, calldatas, descriptionHash);
    }

    function _executor()
        internal
        view
        override(Governor, GovernorTimelockControl)
        returns (address)
    {
        return super._executor();
    }
}
```

### 2.2 Sistema de Votación Cuadrática

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/governance/Governor.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorVotes.sol";

/**
 * @title GovernorCountingQuadratic
 * @notice Votación cuadrática donde cost(votes) = votes²
 * @dev Reduce influencia de grandes holders
 */
abstract contract GovernorCountingQuadratic is Governor {

    struct ProposalVote {
        uint256 againstVotes;
        uint256 forVotes;
        uint256 abstainVotes;
        mapping(address => bool) hasVoted;
        mapping(address => uint256) voterWeight;
    }

    mapping(uint256 => ProposalVote) private _proposalVotes;

    /**
     * @notice Calcular raíz cuadrada (Babylonian method)
     */
    function sqrt(uint256 x) internal pure returns (uint256) {
        if (x == 0) return 0;

        uint256 z = (x + 1) / 2;
        uint256 y = x;

        while (z < y) {
            y = z;
            z = (x / z + z) / 2;
        }

        return y;
    }

    /**
     * @notice Convertir tokens a votos cuadráticos
     * @param tokenBalance Balance de tokens
     * @return quadraticVotes Votos efectivos (sqrt)
     */
    function getQuadraticVotes(
        uint256 tokenBalance
    ) public pure returns (uint256 quadraticVotes) {
        // Normalizar a 18 decimales antes de sqrt
        // Ej: 100 tokens = 10 votos cuadráticos
        return sqrt(tokenBalance);
    }

    /**
     * @notice Verificar modo de conteo
     */
    function COUNTING_MODE()
        public
        pure
        virtual
        override
        returns (string memory)
    {
        return "support=bravo&quorum=quadratic";
    }

    /**
     * @notice Verificar si ya votó
     */
    function hasVoted(
        uint256 proposalId,
        address account
    ) public view virtual override returns (bool) {
        return _proposalVotes[proposalId].hasVoted[account];
    }

    /**
     * @notice Obtener resultados de votación
     */
    function proposalVotes(uint256 proposalId)
        public
        view
        returns (uint256 againstVotes, uint256 forVotes, uint256 abstainVotes)
    {
        ProposalVote storage proposal = _proposalVotes[proposalId];
        return (proposal.againstVotes, proposal.forVotes, proposal.abstainVotes);
    }

    /**
     * @notice Contar voto con peso cuadrático
     */
    function _countVote(
        uint256 proposalId,
        address account,
        uint8 support,
        uint256 weight,
        bytes memory // params - unused
    ) internal virtual override {
        ProposalVote storage proposal = _proposalVotes[proposalId];

        require(!proposal.hasVoted[account], "Already voted");
        proposal.hasVoted[account] = true;

        // Aplicar votación cuadrática
        uint256 quadraticWeight = getQuadraticVotes(weight);
        proposal.voterWeight[account] = quadraticWeight;

        if (support == 0) {
            proposal.againstVotes += quadraticWeight;
        } else if (support == 1) {
            proposal.forVotes += quadraticWeight;
        } else if (support == 2) {
            proposal.abstainVotes += quadraticWeight;
        } else {
            revert("Invalid vote type");
        }
    }

    /**
     * @notice Quórum con votos cuadráticos
     */
    function _quorumReached(
        uint256 proposalId
    ) internal view virtual override returns (bool) {
        ProposalVote storage proposal = _proposalVotes[proposalId];

        uint256 totalQuadraticVotes =
            proposal.forVotes + proposal.againstVotes + proposal.abstainVotes;

        return totalQuadraticVotes >= quorum(proposalSnapshot(proposalId));
    }

    /**
     * @notice Verificar si propuesta fue exitosa
     */
    function _voteSucceeded(
        uint256 proposalId
    ) internal view virtual override returns (bool) {
        ProposalVote storage proposal = _proposalVotes[proposalId];
        return proposal.forVotes > proposal.againstVotes;
    }
}
```

---

## 3. TIMELOCK Y EJECUCIÓN

### 3.1 Timelock Controller

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/governance/TimelockController.sol";

/**
 * @title CipherTimelock
 * @notice Timelock con roles granulares para ejecución de propuestas
 */
contract CipherTimelock is TimelockController {

    // Operaciones de emergencia
    mapping(bytes32 => bool) public emergencyOperations;
    uint256 public emergencyDelay;

    // Operaciones canceladas
    mapping(bytes32 => bool) public cancelledOperations;

    event EmergencyOperationScheduled(
        bytes32 indexed id,
        address indexed target,
        uint256 value,
        bytes data
    );

    constructor(
        uint256 _minDelay,           // Delay mínimo normal (ej: 2 días)
        uint256 _emergencyDelay,     // Delay para emergencias (ej: 6 horas)
        address[] memory _proposers, // Quién puede proponer (Governor)
        address[] memory _executors, // Quién puede ejecutar
        address _admin               // Admin inicial
    ) TimelockController(_minDelay, _proposers, _executors, _admin) {
        emergencyDelay = _emergencyDelay;
    }

    /**
     * @notice Schedule operación de emergencia con delay reducido
     * @dev Solo para situaciones críticas de seguridad
     */
    function scheduleEmergency(
        address target,
        uint256 value,
        bytes calldata data,
        bytes32 predecessor,
        bytes32 salt
    ) external onlyRole(PROPOSER_ROLE) {
        bytes32 id = hashOperation(target, value, data, predecessor, salt);

        require(!isOperationPending(id), "Already pending");

        emergencyOperations[id] = true;

        // Usar delay de emergencia
        _schedule(id, emergencyDelay);

        emit EmergencyOperationScheduled(id, target, value, data);
    }

    /**
     * @notice Cancelar operación pendiente
     * @dev Requiere rol de canceller (usualmente multisig de seguridad)
     */
    function cancelWithReason(
        bytes32 id,
        string calldata reason
    ) external onlyRole(CANCELLER_ROLE) {
        require(isOperationPending(id), "Not pending");

        cancelledOperations[id] = true;

        // Llamar cancel interno
        cancel(id);
    }

    /**
     * @notice Obtener delay efectivo para una operación
     */
    function getOperationDelay(bytes32 id) external view returns (uint256) {
        if (emergencyOperations[id]) {
            return emergencyDelay;
        }
        return getMinDelay();
    }

    /**
     * @notice Actualizar delay de emergencia
     * @dev Solo ejecutable vía governance
     */
    function updateEmergencyDelay(
        uint256 newDelay
    ) external onlyRole(TIMELOCK_ADMIN_ROLE) {
        require(newDelay >= 1 hours, "Too short");
        require(newDelay <= getMinDelay(), "Must be <= minDelay");
        emergencyDelay = newDelay;
    }
}
```

### 3.2 Executor con Batching

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title BatchExecutor
 * @notice Ejecutar múltiples operaciones atómicamente
 */
contract BatchExecutor {

    address public immutable timelock;

    struct Operation {
        address target;
        uint256 value;
        bytes data;
    }

    event BatchExecuted(
        bytes32 indexed batchId,
        uint256 operationsCount,
        bool success
    );

    constructor(address _timelock) {
        timelock = _timelock;
    }

    modifier onlyTimelock() {
        require(msg.sender == timelock, "Only timelock");
        _;
    }

    /**
     * @notice Ejecutar batch de operaciones
     * @param operations Array de operaciones a ejecutar
     * @param requireAllSuccess Si true, revierte si alguna falla
     */
    function executeBatch(
        Operation[] calldata operations,
        bool requireAllSuccess
    ) external payable onlyTimelock returns (bool[] memory results) {
        results = new bool[](operations.length);

        bytes32 batchId = keccak256(abi.encode(operations, block.number));

        for (uint256 i = 0; i < operations.length; i++) {
            (bool success, ) = operations[i].target.call{
                value: operations[i].value
            }(operations[i].data);

            results[i] = success;

            if (requireAllSuccess && !success) {
                revert("Batch operation failed");
            }
        }

        emit BatchExecuted(batchId, operations.length, true);
    }

    /**
     * @notice Ejecutar operación condicional
     * @param condition Address del contrato de condición
     * @param conditionData Calldata para verificar condición
     * @param operation Operación a ejecutar si condición es true
     */
    function executeConditional(
        address condition,
        bytes calldata conditionData,
        Operation calldata operation
    ) external payable onlyTimelock returns (bool) {
        // Verificar condición
        (bool conditionSuccess, bytes memory conditionResult) =
            condition.staticcall(conditionData);

        require(conditionSuccess, "Condition check failed");

        bool shouldExecute = abi.decode(conditionResult, (bool));

        if (shouldExecute) {
            (bool success, ) = operation.target.call{
                value: operation.value
            }(operation.data);
            return success;
        }

        return false;
    }

    receive() external payable {}
}
```

---

## 4. MODELOS DE GOBERNANZA

### 4.1 Comparativa de Modelos

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     GOVERNANCE MODELS COMPARISON                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  TOKEN-BASED (1 token = 1 vote)                                             │
│  ├─ Pros: Simple, familiar, capital-weighted                                │
│  ├─ Cons: Plutocratic, whale dominance                                      │
│  └─ Examples: Compound, Uniswap, Aave                                       │
│                                                                              │
│  QUADRATIC VOTING (cost = votes²)                                           │
│  ├─ Pros: Reduces whale power, preference intensity                         │
│  ├─ Cons: Sybil vulnerable, complex                                         │
│  └─ Examples: Gitcoin Grants, RadicalxChange                                │
│                                                                              │
│  CONVICTION VOTING (time-weighted)                                          │
│  ├─ Pros: Prevents flash-loan attacks, long-term focus                      │
│  ├─ Cons: Slow decision making                                              │
│  └─ Examples: 1Hive, Aragon                                                 │
│                                                                              │
│  HOLOGRAPHIC CONSENSUS (prediction markets)                                  │
│  ├─ Pros: Scales to many proposals, economic incentives                     │
│  ├─ Cons: Complex, requires stake                                           │
│  └─ Examples: DAOstack, Alchemy                                             │
│                                                                              │
│  OPTIMISTIC GOVERNANCE (veto-based)                                         │
│  ├─ Pros: Efficient, low participation needed                               │
│  ├─ Cons: Requires vigilance                                                │
│  └─ Examples: Optimism, some council-based DAOs                             │
│                                                                              │
│  FUTARCHY (prediction market outcomes)                                       │
│  ├─ Pros: Outcome-focused, expert input                                     │
│  ├─ Cons: Market manipulation, thin markets                                 │
│  └─ Examples: Gnosis (experimental)                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Conviction Voting Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/math/Math.sol";

/**
 * @title ConvictionVoting
 * @notice Sistema donde los votos acumulan "convicción" con el tiempo
 * @dev Resistente a flash loans ya que el peso crece exponencialmente
 */
contract ConvictionVoting {
    using Math for uint256;

    IERC20 public immutable votingToken;

    // Parámetros de decaimiento (alpha = decay rate)
    uint256 public constant DECAY_RATE = 9; // 0.9 cuando dividido por 10
    uint256 public constant DECAY_DENOMINATOR = 10;
    uint256 public constant BLOCKS_PER_PERIOD = 100; // Período de acumulación

    // Threshold como fracción del total staked
    uint256 public constant THRESHOLD_NUMERATOR = 1;
    uint256 public constant THRESHOLD_DENOMINATOR = 10; // 10% del total

    struct Proposal {
        address beneficiary;
        uint256 requestedAmount;
        uint256 stakedTokens;
        uint256 convictionLast;
        uint256 blockLast;
        bool executed;
        mapping(address => uint256) stakes;
    }

    uint256 public proposalCount;
    mapping(uint256 => Proposal) public proposals;

    address public fundingPool;

    event ProposalCreated(
        uint256 indexed proposalId,
        address beneficiary,
        uint256 amount
    );
    event StakeChanged(
        uint256 indexed proposalId,
        address voter,
        uint256 newStake
    );
    event ProposalExecuted(uint256 indexed proposalId);

    constructor(address _token, address _fundingPool) {
        votingToken = IERC20(_token);
        fundingPool = _fundingPool;
    }

    /**
     * @notice Crear nueva propuesta de financiación
     */
    function createProposal(
        address beneficiary,
        uint256 requestedAmount
    ) external returns (uint256 proposalId) {
        proposalId = proposalCount++;

        Proposal storage proposal = proposals[proposalId];
        proposal.beneficiary = beneficiary;
        proposal.requestedAmount = requestedAmount;
        proposal.blockLast = block.number;

        emit ProposalCreated(proposalId, beneficiary, requestedAmount);
    }

    /**
     * @notice Stakear tokens en una propuesta
     * @param proposalId ID de la propuesta
     * @param amount Cantidad a stakear
     */
    function stakeOnProposal(
        uint256 proposalId,
        uint256 amount
    ) external {
        Proposal storage proposal = proposals[proposalId];
        require(!proposal.executed, "Already executed");

        // Transferir tokens
        votingToken.transferFrom(msg.sender, address(this), amount);

        // Actualizar convicción antes de cambiar stake
        _updateConviction(proposalId);

        // Actualizar stakes
        proposal.stakes[msg.sender] += amount;
        proposal.stakedTokens += amount;

        emit StakeChanged(proposalId, msg.sender, proposal.stakes[msg.sender]);

        // Verificar si alcanzó threshold
        _tryExecute(proposalId);
    }

    /**
     * @notice Retirar stake de una propuesta
     */
    function unstake(uint256 proposalId, uint256 amount) external {
        Proposal storage proposal = proposals[proposalId];
        require(proposal.stakes[msg.sender] >= amount, "Insufficient stake");

        _updateConviction(proposalId);

        proposal.stakes[msg.sender] -= amount;
        proposal.stakedTokens -= amount;

        votingToken.transfer(msg.sender, amount);

        emit StakeChanged(proposalId, msg.sender, proposal.stakes[msg.sender]);
    }

    /**
     * @notice Calcular convicción actual
     * @dev conviction(t) = conviction(t-1) * alpha + stakedTokens
     */
    function calculateConviction(
        uint256 proposalId
    ) public view returns (uint256) {
        Proposal storage proposal = proposals[proposalId];

        uint256 blocksPassed = block.number - proposal.blockLast;
        uint256 periods = blocksPassed / BLOCKS_PER_PERIOD;

        if (periods == 0) {
            return proposal.convictionLast;
        }

        // Calcular decaimiento
        uint256 conviction = proposal.convictionLast;

        for (uint256 i = 0; i < periods && i < 50; i++) { // Cap iterations
            // conviction = conviction * 0.9 + stakedTokens
            conviction = (conviction * DECAY_RATE) / DECAY_DENOMINATOR +
                         proposal.stakedTokens;
        }

        return conviction;
    }

    /**
     * @notice Calcular threshold requerido
     * @dev threshold = totalSupply * THRESHOLD_NUMERATOR / THRESHOLD_DENOMINATOR
     */
    function getThreshold(uint256 proposalId) public view returns (uint256) {
        // Threshold basado en el monto solicitado
        Proposal storage proposal = proposals[proposalId];

        uint256 totalStaked = votingToken.balanceOf(address(this));

        // Más fondos solicitados = threshold más alto
        uint256 baseThreshold = (totalStaked * THRESHOLD_NUMERATOR) /
                                THRESHOLD_DENOMINATOR;

        // Escalar por monto solicitado (simplificado)
        return baseThreshold + (proposal.requestedAmount / 1000);
    }

    /**
     * @notice Actualizar convicción almacenada
     */
    function _updateConviction(uint256 proposalId) internal {
        Proposal storage proposal = proposals[proposalId];
        proposal.convictionLast = calculateConviction(proposalId);
        proposal.blockLast = block.number;
    }

    /**
     * @notice Intentar ejecutar propuesta si alcanzó threshold
     */
    function _tryExecute(uint256 proposalId) internal {
        Proposal storage proposal = proposals[proposalId];

        uint256 conviction = calculateConviction(proposalId);
        uint256 threshold = getThreshold(proposalId);

        if (conviction >= threshold && !proposal.executed) {
            proposal.executed = true;

            // Transferir fondos del pool al beneficiario
            IERC20(fundingPool).transfer(
                proposal.beneficiary,
                proposal.requestedAmount
            );

            emit ProposalExecuted(proposalId);
        }
    }

    /**
     * @notice Ver stake de un usuario en propuesta
     */
    function getUserStake(
        uint256 proposalId,
        address user
    ) external view returns (uint256) {
        return proposals[proposalId].stakes[user];
    }
}
```

---

## 5. DELEGACIÓN Y REPRESENTACIÓN

### 5.1 Sistema de Delegación Líquida

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";

/**
 * @title LiquidDelegation
 * @notice Delegación avanzada con sub-delegación y límites
 * @dev Permite delegación parcial y por categoría
 */
contract LiquidDelegation {

    ERC20Votes public immutable governanceToken;

    // Categorías de propuestas
    enum ProposalCategory { TREASURY, PROTOCOL, GRANTS, EMERGENCY }

    // Delegación por categoría
    struct CategoryDelegation {
        address delegate;
        uint256 percentage; // Basis points (10000 = 100%)
    }

    // Mapping: delegator => category => delegation
    mapping(address => mapping(ProposalCategory => CategoryDelegation))
        public categoryDelegations;

    // Límites de delegación
    mapping(address => uint256) public delegationReceived;
    uint256 public constant MAX_DELEGATION_RATIO = 100; // Max 100x own holdings

    // Historial de delegaciones
    mapping(address => address[]) public delegationHistory;

    event CategoryDelegated(
        address indexed delegator,
        address indexed delegate,
        ProposalCategory category,
        uint256 percentage
    );

    event DelegationRevoked(
        address indexed delegator,
        ProposalCategory category
    );

    constructor(address _governanceToken) {
        governanceToken = ERC20Votes(_governanceToken);
    }

    /**
     * @notice Delegar votos para una categoría específica
     * @param category Tipo de propuestas
     * @param delegate Delegado para esa categoría
     * @param percentage Porcentaje a delegar (basis points)
     */
    function delegateByCategory(
        ProposalCategory category,
        address delegate,
        uint256 percentage
    ) external {
        require(percentage <= 10000, "Max 100%");
        require(delegate != msg.sender, "Self-delegation");
        require(delegate != address(0), "Zero address");

        // Verificar límite del delegado
        uint256 delegateOwnPower = governanceToken.balanceOf(delegate);
        uint256 newDelegation = (governanceToken.balanceOf(msg.sender) *
                                 percentage) / 10000;

        require(
            delegationReceived[delegate] + newDelegation <=
            delegateOwnPower * MAX_DELEGATION_RATIO,
            "Delegate limit exceeded"
        );

        // Revocar delegación anterior si existe
        CategoryDelegation storage existing =
            categoryDelegations[msg.sender][category];
        if (existing.delegate != address(0)) {
            uint256 previousAmount = (governanceToken.balanceOf(msg.sender) *
                                      existing.percentage) / 10000;
            delegationReceived[existing.delegate] -= previousAmount;
        }

        // Establecer nueva delegación
        categoryDelegations[msg.sender][category] = CategoryDelegation({
            delegate: delegate,
            percentage: percentage
        });

        delegationReceived[delegate] += newDelegation;
        delegationHistory[msg.sender].push(delegate);

        emit CategoryDelegated(msg.sender, delegate, category, percentage);
    }

    /**
     * @notice Obtener voting power efectivo para una categoría
     * @param voter Address del votante
     * @param category Categoría de la propuesta
     */
    function getEffectiveVotingPower(
        address voter,
        ProposalCategory category
    ) public view returns (uint256) {
        uint256 ownBalance = governanceToken.balanceOf(voter);

        // Restar lo delegado
        CategoryDelegation storage delegation =
            categoryDelegations[voter][category];

        uint256 delegatedOut = (ownBalance * delegation.percentage) / 10000;
        uint256 ownPower = ownBalance - delegatedOut;

        // Sumar delegaciones recibidas (simplificado)
        return ownPower + delegationReceived[voter];
    }

    /**
     * @notice Revocar todas las delegaciones
     */
    function revokeAllDelegations() external {
        for (uint8 i = 0; i < 4; i++) {
            ProposalCategory cat = ProposalCategory(i);
            CategoryDelegation storage delegation =
                categoryDelegations[msg.sender][cat];

            if (delegation.delegate != address(0)) {
                uint256 amount = (governanceToken.balanceOf(msg.sender) *
                                  delegation.percentage) / 10000;
                delegationReceived[delegation.delegate] -= amount;

                delete categoryDelegations[msg.sender][cat];

                emit DelegationRevoked(msg.sender, cat);
            }
        }
    }

    /**
     * @notice Ver historial de delegaciones
     */
    function getDelegationHistory(
        address delegator
    ) external view returns (address[] memory) {
        return delegationHistory[delegator];
    }
}
```

### 5.2 Delegate Registry

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title DelegateRegistry
 * @notice Registro de delegados con perfiles y reputación
 */
contract DelegateRegistry {

    struct DelegateProfile {
        string name;
        string statement; // IPFS hash
        string[] platforms;
        uint256 registeredAt;
        uint256 proposalsVoted;
        uint256 proposalsCreated;
        bool isActive;
    }

    struct VotingRecord {
        uint256 proposalId;
        uint8 vote; // 0=against, 1=for, 2=abstain
        string rationale; // IPFS hash
        uint256 timestamp;
    }

    mapping(address => DelegateProfile) public delegates;
    mapping(address => VotingRecord[]) public votingHistory;
    mapping(address => mapping(address => bool)) public endorsements;

    address[] public registeredDelegates;

    event DelegateRegistered(address indexed delegate, string name);
    event VoteRecorded(
        address indexed delegate,
        uint256 proposalId,
        uint8 vote
    );
    event EndorsementGiven(
        address indexed from,
        address indexed to
    );

    /**
     * @notice Registrar como delegado
     */
    function registerDelegate(
        string calldata name,
        string calldata statement,
        string[] calldata platforms
    ) external {
        require(!delegates[msg.sender].isActive, "Already registered");

        delegates[msg.sender] = DelegateProfile({
            name: name,
            statement: statement,
            platforms: platforms,
            registeredAt: block.timestamp,
            proposalsVoted: 0,
            proposalsCreated: 0,
            isActive: true
        });

        registeredDelegates.push(msg.sender);

        emit DelegateRegistered(msg.sender, name);
    }

    /**
     * @notice Actualizar perfil de delegado
     */
    function updateProfile(
        string calldata newStatement,
        string[] calldata newPlatforms
    ) external {
        require(delegates[msg.sender].isActive, "Not registered");

        delegates[msg.sender].statement = newStatement;
        delegates[msg.sender].platforms = newPlatforms;
    }

    /**
     * @notice Registrar voto (llamado por Governor)
     */
    function recordVote(
        address delegate,
        uint256 proposalId,
        uint8 vote,
        string calldata rationale
    ) external {
        // En producción, verificar que msg.sender es el Governor

        votingHistory[delegate].push(VotingRecord({
            proposalId: proposalId,
            vote: vote,
            rationale: rationale,
            timestamp: block.timestamp
        }));

        delegates[delegate].proposalsVoted++;

        emit VoteRecorded(delegate, proposalId, vote);
    }

    /**
     * @notice Dar endorsement a otro delegado
     */
    function endorse(address delegate) external {
        require(delegates[delegate].isActive, "Not a delegate");
        require(delegate != msg.sender, "Self-endorsement");

        endorsements[msg.sender][delegate] = true;

        emit EndorsementGiven(msg.sender, delegate);
    }

    /**
     * @notice Obtener todos los delegados registrados
     */
    function getAllDelegates() external view returns (address[] memory) {
        return registeredDelegates;
    }

    /**
     * @notice Obtener historial de votos de un delegado
     */
    function getVotingHistory(
        address delegate
    ) external view returns (VotingRecord[] memory) {
        return votingHistory[delegate];
    }

    /**
     * @notice Calcular tasa de participación de un delegado
     */
    function getParticipationRate(
        address delegate,
        uint256 totalProposals
    ) external view returns (uint256) {
        if (totalProposals == 0) return 0;
        return (delegates[delegate].proposalsVoted * 10000) / totalProposals;
    }
}
```

---

## 6. OPTIMISTIC GOVERNANCE

### 6.1 Optimistic Execution

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title OptimisticGovernor
 * @notice Ejecuta propuestas automáticamente a menos que sean vetadas
 * @dev Más eficiente para DAOs con baja participación
 */
contract OptimisticGovernor {

    struct Proposal {
        address proposer;
        address target;
        bytes calldata_;
        uint256 value;
        uint256 challengePeriodEnd;
        uint256 vetoVotes;
        bool executed;
        bool vetoed;
    }

    IERC20 public immutable vetoToken;
    uint256 public immutable challengePeriod;
    uint256 public immutable vetoThreshold; // Basis points del total supply
    uint256 public immutable proposerBond;

    mapping(uint256 => Proposal) public proposals;
    mapping(uint256 => mapping(address => uint256)) public vetoVotesBy;
    uint256 public proposalCount;

    event ProposalSubmitted(
        uint256 indexed proposalId,
        address proposer,
        address target
    );
    event VetoCast(
        uint256 indexed proposalId,
        address voter,
        uint256 weight
    );
    event ProposalExecuted(uint256 indexed proposalId);
    event ProposalVetoed(uint256 indexed proposalId);

    constructor(
        address _vetoToken,
        uint256 _challengePeriod,
        uint256 _vetoThreshold,
        uint256 _proposerBond
    ) {
        vetoToken = IERC20(_vetoToken);
        challengePeriod = _challengePeriod;
        vetoThreshold = _vetoThreshold;
        proposerBond = _proposerBond;
    }

    /**
     * @notice Proponer acción (se ejecutará si no es vetada)
     */
    function propose(
        address target,
        bytes calldata calldata_,
        uint256 value
    ) external payable returns (uint256 proposalId) {
        require(msg.value >= proposerBond, "Insufficient bond");

        proposalId = proposalCount++;

        proposals[proposalId] = Proposal({
            proposer: msg.sender,
            target: target,
            calldata_: calldata_,
            value: value,
            challengePeriodEnd: block.timestamp + challengePeriod,
            vetoVotes: 0,
            executed: false,
            vetoed: false
        });

        emit ProposalSubmitted(proposalId, msg.sender, target);
    }

    /**
     * @notice Votar para vetar una propuesta
     */
    function veto(uint256 proposalId, uint256 amount) external {
        Proposal storage proposal = proposals[proposalId];

        require(
            block.timestamp < proposal.challengePeriodEnd,
            "Challenge period ended"
        );
        require(!proposal.executed && !proposal.vetoed, "Already finalized");

        vetoToken.transferFrom(msg.sender, address(this), amount);

        proposal.vetoVotes += amount;
        vetoVotesBy[proposalId][msg.sender] += amount;

        emit VetoCast(proposalId, msg.sender, amount);

        // Verificar si alcanzó threshold de veto
        uint256 totalSupply = vetoToken.totalSupply();
        if (proposal.vetoVotes >= (totalSupply * vetoThreshold) / 10000) {
            proposal.vetoed = true;
            emit ProposalVetoed(proposalId);
        }
    }

    /**
     * @notice Ejecutar propuesta después del período de challenge
     */
    function execute(uint256 proposalId) external {
        Proposal storage proposal = proposals[proposalId];

        require(
            block.timestamp >= proposal.challengePeriodEnd,
            "Challenge period active"
        );
        require(!proposal.executed && !proposal.vetoed, "Invalid state");

        proposal.executed = true;

        // Devolver bond al proposer
        payable(proposal.proposer).transfer(proposerBond);

        // Ejecutar la acción
        (bool success, ) = proposal.target.call{value: proposal.value}(
            proposal.calldata_
        );
        require(success, "Execution failed");

        emit ProposalExecuted(proposalId);
    }

    /**
     * @notice Reclamar tokens de veto después de que propuesta fue vetada
     */
    function claimVetoTokens(uint256 proposalId) external {
        Proposal storage proposal = proposals[proposalId];
        require(proposal.vetoed, "Not vetoed");

        uint256 amount = vetoVotesBy[proposalId][msg.sender];
        require(amount > 0, "Nothing to claim");

        vetoVotesBy[proposalId][msg.sender] = 0;
        vetoToken.transfer(msg.sender, amount);

        // Distribuir parte del bond como recompensa
        uint256 reward = (proposerBond * amount) / proposal.vetoVotes;
        payable(msg.sender).transfer(reward);
    }
}

interface IERC20 {
    function transferFrom(address, address, uint256) external returns (bool);
    function transfer(address, uint256) external returns (bool);
    function totalSupply() external view returns (uint256);
}
```

---

## 7. ANÁLISIS DE GOVERNANCE ATTACKS

### 7.1 Vectores de Ataque Comunes

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     GOVERNANCE ATTACK VECTORS                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. FLASH LOAN GOVERNANCE                                                    │
│     ├─ Borrow tokens → Vote → Return in same tx                            │
│     ├─ Mitigation: Snapshot voting power at proposal creation               │
│     └─ Example: Beanstalk hack ($182M)                                      │
│                                                                              │
│  2. VOTE BUYING                                                              │
│     ├─ Off-chain bribes for specific votes                                  │
│     ├─ Dark DAOs (anonymous coordination)                                   │
│     └─ Mitigation: Secret ballot (commit-reveal), veCRV locks               │
│                                                                              │
│  3. GOVERNANCE EXTRACTION                                                    │
│     ├─ Acquire enough tokens to pass malicious proposal                     │
│     ├─ Drain treasury or change critical parameters                         │
│     └─ Mitigation: Timelocks, emergency multisig, caps                      │
│                                                                              │
│  4. PROPOSAL SPAM                                                            │
│     ├─ Flood with proposals to exhaust voters                               │
│     ├─ Hide malicious proposal among many                                   │
│     └─ Mitigation: Proposal threshold, deposit requirements                 │
│                                                                              │
│  5. VOTER APATHY EXPLOITATION                                                │
│     ├─ Pass proposals during low participation                              │
│     ├─ Quorum attacks when community is distracted                          │
│     └─ Mitigation: Dynamic quorum, conviction voting                        │
│                                                                              │
│  6. SHORT SQUEEZE GOVERNANCE                                                 │
│     ├─ Borrow governance tokens from lenders                                │
│     ├─ Vote to drain protocol funds                                         │
│     └─ Mitigation: Disable voting for borrowed tokens                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Secure Governance Patterns

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title SecureGovernanceChecks
 * @notice Patrones de seguridad para gobernanza
 */
abstract contract SecureGovernanceChecks {

    // Emergency guardian (multisig)
    address public guardian;

    // Límites de cambio por propuesta
    mapping(bytes4 => uint256) public parameterCaps;

    // Cooldown entre propuestas del mismo proposer
    mapping(address => uint256) public lastProposalTime;
    uint256 public constant PROPOSAL_COOLDOWN = 1 days;

    // Propuestas activas máximas
    uint256 public activeProposals;
    uint256 public constant MAX_ACTIVE_PROPOSALS = 10;

    event GuardianVeto(uint256 proposalId, string reason);
    event EmergencyPause(address caller);

    modifier onlyGuardian() {
        require(msg.sender == guardian, "Not guardian");
        _;
    }

    /**
     * @notice Verificar límites de cambio de parámetros
     */
    function _checkParameterChange(
        bytes4 selector,
        uint256 newValue,
        uint256 currentValue
    ) internal view {
        uint256 cap = parameterCaps[selector];
        if (cap > 0) {
            uint256 change = newValue > currentValue
                ? newValue - currentValue
                : currentValue - newValue;

            uint256 percentChange = (change * 10000) / currentValue;
            require(percentChange <= cap, "Change exceeds cap");
        }
    }

    /**
     * @notice Verificar cooldown del proposer
     */
    function _checkProposerCooldown(address proposer) internal view {
        require(
            block.timestamp >= lastProposalTime[proposer] + PROPOSAL_COOLDOWN,
            "Proposer cooldown active"
        );
    }

    /**
     * @notice Verificar límite de propuestas activas
     */
    function _checkActiveProposalLimit() internal view {
        require(
            activeProposals < MAX_ACTIVE_PROPOSALS,
            "Too many active proposals"
        );
    }

    /**
     * @notice Veto de emergencia del guardian
     */
    function guardianVeto(
        uint256 proposalId,
        string calldata reason
    ) external onlyGuardian {
        // Implementar lógica de cancelación
        emit GuardianVeto(proposalId, reason);
    }

    /**
     * @notice Establecer cap para función
     * @param selector Selector de la función
     * @param maxChangePercent Máximo cambio en basis points
     */
    function setParameterCap(
        bytes4 selector,
        uint256 maxChangePercent
    ) external onlyGuardian {
        parameterCaps[selector] = maxChangePercent;
    }
}
```

### 7.3 Análisis de Governance con Python

```python
"""
CIPHER: Governance Analytics
Análisis de métricas de gobernanza y detección de anomalías
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import statistics

@dataclass
class Vote:
    voter: str
    proposal_id: int
    support: int  # 0=against, 1=for, 2=abstain
    weight: int
    timestamp: datetime
    tx_hash: str

@dataclass
class Proposal:
    id: int
    proposer: str
    description: str
    created_at: datetime
    voting_start: datetime
    voting_end: datetime
    for_votes: int
    against_votes: int
    abstain_votes: int
    state: str  # pending, active, succeeded, defeated, executed

class GovernanceAnalyzer:
    def __init__(self, token_total_supply: int):
        self.total_supply = token_total_supply
        self.proposals: List[Proposal] = []
        self.votes: List[Vote] = []
        self.voter_history: Dict[str, List[Vote]] = {}

    def add_proposal(self, proposal: Proposal):
        self.proposals.append(proposal)

    def add_vote(self, vote: Vote):
        self.votes.append(vote)
        if vote.voter not in self.voter_history:
            self.voter_history[vote.voter] = []
        self.voter_history[vote.voter].append(vote)

    def calculate_participation_rate(self, proposal_id: int) -> float:
        """Calcular tasa de participación para una propuesta"""
        proposal_votes = [v for v in self.votes if v.proposal_id == proposal_id]
        total_voted = sum(v.weight for v in proposal_votes)
        return total_voted / self.total_supply

    def detect_vote_concentration(
        self,
        proposal_id: int,
        threshold: float = 0.5
    ) -> Dict:
        """Detectar concentración de votos (ballena dominante)"""
        proposal_votes = [v for v in self.votes if v.proposal_id == proposal_id]
        total_votes = sum(v.weight for v in proposal_votes)

        if total_votes == 0:
            return {"concentrated": False, "top_voters": []}

        # Ordenar por peso
        sorted_votes = sorted(proposal_votes, key=lambda v: v.weight, reverse=True)

        cumulative = 0
        top_voters = []

        for vote in sorted_votes:
            cumulative += vote.weight
            top_voters.append({
                "voter": vote.voter,
                "weight": vote.weight,
                "percentage": vote.weight / total_votes
            })

            if cumulative / total_votes >= threshold:
                break

        return {
            "concentrated": len(top_voters) <= 3,
            "top_voters": top_voters,
            "concentration_index": self._herfindahl_index(proposal_votes)
        }

    def _herfindahl_index(self, votes: List[Vote]) -> float:
        """Índice de concentración Herfindahl-Hirschman"""
        total = sum(v.weight for v in votes)
        if total == 0:
            return 0

        return sum((v.weight / total) ** 2 for v in votes)

    def detect_last_minute_votes(
        self,
        proposal: Proposal,
        threshold_minutes: int = 60
    ) -> List[Vote]:
        """Detectar votos de último minuto (posible coordinación)"""
        threshold_time = proposal.voting_end - timedelta(minutes=threshold_minutes)

        proposal_votes = [v for v in self.votes if v.proposal_id == proposal.id]

        return [v for v in proposal_votes if v.timestamp >= threshold_time]

    def analyze_voter_behavior(self, voter: str) -> Dict:
        """Analizar comportamiento histórico de un votante"""
        if voter not in self.voter_history:
            return {"participation": 0, "consistency": None}

        history = self.voter_history[voter]

        # Tasa de participación
        participation = len(history) / len(self.proposals) if self.proposals else 0

        # Consistencia de votación (siempre a favor/contra)
        support_votes = [v.support for v in history]

        if len(support_votes) >= 3:
            # Calcular entropía de votación
            for_ratio = support_votes.count(1) / len(support_votes)
            against_ratio = support_votes.count(0) / len(support_votes)

            consistency = max(for_ratio, against_ratio)
        else:
            consistency = None

        return {
            "voter": voter,
            "total_votes": len(history),
            "participation_rate": participation,
            "voting_consistency": consistency,
            "average_voting_power": statistics.mean([v.weight for v in history]),
            "for_votes": support_votes.count(1),
            "against_votes": support_votes.count(0),
            "abstain_votes": support_votes.count(2)
        }

    def detect_flash_loan_risk(self, proposal: Proposal) -> Dict:
        """Detectar si propuesta es vulnerable a flash loans"""
        # Verificar si hay snapshot antes de votación
        snapshot_exists = proposal.voting_start > proposal.created_at

        # Calcular gap entre creación y votación
        gap = (proposal.voting_start - proposal.created_at).total_seconds()

        return {
            "snapshot_exists": snapshot_exists,
            "gap_seconds": gap,
            "risk_level": "LOW" if gap > 86400 else "HIGH" if gap < 3600 else "MEDIUM",
            "recommendation": "Increase voting delay" if gap < 86400 else "OK"
        }

    def get_governance_health_metrics(self) -> Dict:
        """Métricas generales de salud de gobernanza"""
        if not self.proposals:
            return {"status": "NO_DATA"}

        # Participación promedio
        participation_rates = [
            self.calculate_participation_rate(p.id) for p in self.proposals
        ]
        avg_participation = statistics.mean(participation_rates)

        # Diversidad de votantes
        unique_voters = len(self.voter_history)

        # Propuestas exitosas
        succeeded = len([p for p in self.proposals if p.state == "succeeded"])
        success_rate = succeeded / len(self.proposals)

        # Concentración promedio
        concentrations = [
            self.detect_vote_concentration(p.id)["concentration_index"]
            for p in self.proposals
        ]
        avg_concentration = statistics.mean(concentrations) if concentrations else 0

        return {
            "total_proposals": len(self.proposals),
            "average_participation": avg_participation,
            "unique_voters": unique_voters,
            "proposal_success_rate": success_rate,
            "average_concentration_index": avg_concentration,
            "health_score": self._calculate_health_score(
                avg_participation,
                unique_voters,
                avg_concentration
            )
        }

    def _calculate_health_score(
        self,
        participation: float,
        voters: int,
        concentration: float
    ) -> str:
        """Calcular score de salud de gobernanza"""
        score = 0

        # Participación (0-40 puntos)
        score += min(participation * 100, 40)

        # Diversidad (0-30 puntos)
        score += min(voters / 10, 30)

        # Descentralización (0-30 puntos) - menor concentración = mejor
        score += max(0, 30 - concentration * 100)

        if score >= 80:
            return "EXCELLENT"
        elif score >= 60:
            return "GOOD"
        elif score >= 40:
            return "MODERATE"
        else:
            return "NEEDS_IMPROVEMENT"


# Ejemplo de uso
if __name__ == "__main__":
    analyzer = GovernanceAnalyzer(token_total_supply=100_000_000 * 10**18)

    # Simular propuesta
    proposal = Proposal(
        id=1,
        proposer="0x1234...",
        description="Increase staking rewards",
        created_at=datetime.now() - timedelta(days=3),
        voting_start=datetime.now() - timedelta(days=2),
        voting_end=datetime.now() + timedelta(days=1),
        for_votes=5_000_000 * 10**18,
        against_votes=2_000_000 * 10**18,
        abstain_votes=500_000 * 10**18,
        state="active"
    )

    analyzer.add_proposal(proposal)

    # Analizar
    flash_risk = analyzer.detect_flash_loan_risk(proposal)
    print(f"Flash Loan Risk: {flash_risk}")

    health = analyzer.get_governance_health_metrics()
    print(f"Governance Health: {health}")
```

---

## CONEXIONES NEURALES

```
NEURONA_GOVERNANCE (C40009)
├── DEPENDE DE
│   ├── NEURONA_TOKENOMICS (C40008) - Token voting power
│   └── NEURONA_SMART_CONTRACTS (C30001) - Contract patterns
│
├── CONECTA CON
│   ├── NEURONA_DEFI_RISKS (C40011) - Governance attacks
│   ├── NEURONA_PROTOCOL_ANALYSIS (C40010) - DAO metrics
│   └── NEURONA_TRADING (C70001) - Vote market dynamics
│
└── HABILITA
    ├── Diseño de sistemas de gobernanza seguros
    ├── Análisis de propuestas y votaciones
    ├── Detección de ataques de gobernanza
    └── Optimización de participación DAO
```

---

## FIRMA CIPHER

```
╔═══════════════════════════════════════════════════════════════╗
║  NEURONA: C40009                                              ║
║  TIPO: DAO Governance & Voting                                ║
║  VERSIÓN: 1.0.0                                               ║
║  ESTADO: ACTIVA                                               ║
║                                                               ║
║  "La gobernanza descentralizada es la democracia             ║
║   ejecutable del código."                                     ║
║                                                               ║
║  CIPHER_CORE::GOVERNANCE::INITIALIZED                         ║
╚═══════════════════════════════════════════════════════════════╝
```
