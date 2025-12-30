# NEURONA: ETHEREUM MASTERY
## C20001 | Dominio Completo del Ecosistema Ethereum

```
╔═══════════════════════════════════════════════════════════════╗
║  CIPHER BLOCKCHAIN DOMAIN                                     ║
║  Ethereum & EVM Ecosystem - Complete Mastery                  ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## METADATA

```yaml
neurona_id: C20001
categoria: BLOCKCHAINS
nombre: ETHEREUM_MASTERY
version: 1.0.0
estado: ACTIVA
prioridad: CRITICA

tags:
  - ethereum
  - evm
  - solidity
  - layer2
  - defi
```

---

## 1. ARQUITECTURA ETHEREUM

### 1.1 Componentes Core

```
ETHEREUM ARCHITECTURE
│
├── EXECUTION LAYER (Ex-Eth1)
│   ├── EVM (Ethereum Virtual Machine)
│   │   ├── Stack-based architecture
│   │   ├── 256-bit word size
│   │   ├── Deterministic execution
│   │   └── Gas metering
│   │
│   ├── State Management
│   │   ├── World State (accounts)
│   │   ├── Merkle Patricia Trie
│   │   ├── State root in blocks
│   │   └── Account types (EOA, Contract)
│   │
│   ├── Transaction Processing
│   │   ├── Mempool
│   │   ├── Gas pricing (EIP-1559)
│   │   ├── Transaction types (0, 1, 2)
│   │   └── Nonce management
│   │
│   └── Execution Clients
│       ├── Geth (Go)
│       ├── Erigon (Go)
│       ├── Nethermind (.NET)
│       ├── Besu (Java)
│       └── Reth (Rust)
│
├── CONSENSUS LAYER (Ex-Eth2)
│   ├── Proof of Stake
│   │   ├── 32 ETH validator stake
│   │   ├── Slots (12 sec) & Epochs (32 slots)
│   │   ├── Attestations
│   │   └── Finality (2 epochs)
│   │
│   ├── Beacon Chain
│   │   ├── Validator registry
│   │   ├── Randomness (RANDAO)
│   │   ├── Sync committees
│   │   └── Slashing conditions
│   │
│   └── Consensus Clients
│       ├── Prysm (Go)
│       ├── Lighthouse (Rust)
│       ├── Teku (Java)
│       ├── Nimbus (Nim)
│       └── Lodestar (TypeScript)
│
└── DATA LAYER
    ├── Blob Space (EIP-4844)
    │   ├── Proto-danksharding
    │   ├── 128KB blobs
    │   └── Rollup data availability
    │
    └── Future: Full Danksharding
```

### 1.2 EVM Deep Dive

```yaml
evm_architecture:
  stack:
    size: 1024 items max
    item_size: 256 bits
    operations: PUSH, POP, DUP, SWAP

  memory:
    type: Byte-addressable
    expansion: Paid via gas
    lifecycle: Per-execution

  storage:
    type: Key-value (256-bit → 256-bit)
    persistence: Permanent
    cost: SSTORE most expensive opcode

  gas_costs:
    categories:
      zero: STOP, RETURN, REVERT
      base: Most operations (2-3 gas)
      low: ADD, SUB, NOT, etc.
      mid: MUL, DIV, etc.
      high: BALANCE, EXTCODESIZE
      special: SSTORE, CREATE, CALL

    eip_1559:
      base_fee: Burned, algorithmic
      priority_fee: To validator
      max_fee: User's max willing
      formula: "gas_used * (base_fee + priority_fee)"

opcodes_importantes:
  storage:
    - SLOAD: Read storage (100-2100 gas)
    - SSTORE: Write storage (2900-20000 gas)

  calls:
    - CALL: External call
    - DELEGATECALL: Context-preserving call
    - STATICCALL: Read-only call
    - CREATE: Deploy contract
    - CREATE2: Deterministic deploy

  context:
    - CALLER: msg.sender
    - ORIGIN: tx.origin
    - CALLVALUE: msg.value
    - CALLDATALOAD: Input data
```

### 1.3 Account Types

```yaml
account_types:

  eoa: # Externally Owned Account
    controlled_by: Private key
    components:
      - nonce (transaction count)
      - balance (ETH)
    capabilities:
      - Initiate transactions
      - Sign messages

  contract_account:
    controlled_by: Code
    components:
      - nonce (contracts created)
      - balance (ETH)
      - code_hash
      - storage_root
    capabilities:
      - Execute code
      - Hold assets
      - Call other contracts

  erc_4337_account: # Account Abstraction
    controlled_by: Custom logic
    features:
      - Social recovery
      - Batched transactions
      - Sponsored gas
      - Custom signature schemes
```

---

## 2. DESARROLLO EN ETHEREUM

### 2.1 Solidity Fundamentals

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title ExampleToken
 * @notice Ejemplo de token ERC20 con mejores prácticas
 */
contract ExampleToken is ERC20, Ownable, ReentrancyGuard {

    // Constants
    uint256 public constant MAX_SUPPLY = 100_000_000 * 10**18;

    // State variables
    mapping(address => bool) public blacklisted;

    // Events
    event Blacklisted(address indexed account);
    event Unblacklisted(address indexed account);

    // Errors (custom errors - gas efficient)
    error AccountBlacklisted(address account);
    error MaxSupplyExceeded();

    // Modifiers
    modifier notBlacklisted(address account) {
        if (blacklisted[account]) revert AccountBlacklisted(account);
        _;
    }

    constructor() ERC20("Example Token", "EXT") Ownable(msg.sender) {
        _mint(msg.sender, 10_000_000 * 10**18);
    }

    /**
     * @notice Mint new tokens (only owner)
     * @param to Recipient address
     * @param amount Amount to mint
     */
    function mint(address to, uint256 amount)
        external
        onlyOwner
        notBlacklisted(to)
    {
        if (totalSupply() + amount > MAX_SUPPLY) {
            revert MaxSupplyExceeded();
        }
        _mint(to, amount);
    }

    /**
     * @notice Override transfer with blacklist check
     */
    function _update(
        address from,
        address to,
        uint256 value
    ) internal virtual override notBlacklisted(from) notBlacklisted(to) {
        super._update(from, to, value);
    }

    // Admin functions
    function blacklist(address account) external onlyOwner {
        blacklisted[account] = true;
        emit Blacklisted(account);
    }

    function unblacklist(address account) external onlyOwner {
        blacklisted[account] = false;
        emit Unblacklisted(account);
    }
}
```

### 2.2 Frameworks de Desarrollo

```yaml
hardhat:
  descripcion: Framework más popular
  features:
    - TypeScript support
    - Local network (Hardhat Network)
    - Console.log debugging
    - Plugin ecosystem
    - Ethers.js integration

  estructura:
    - contracts/
    - scripts/
    - test/
    - hardhat.config.ts

  comandos:
    - npx hardhat compile
    - npx hardhat test
    - npx hardhat node
    - npx hardhat run scripts/deploy.ts

foundry:
  descripcion: Framework en Rust, muy rápido
  features:
    - Solidity tests (no JS)
    - Fuzz testing built-in
    - Invariant testing
    - Gas snapshots
    - Cast CLI for interactions

  herramientas:
    forge: Testing & building
    cast: CLI interactions
    anvil: Local node
    chisel: Solidity REPL

  comandos:
    - forge build
    - forge test
    - forge test --gas-report
    - cast send <contract> <function>
```

### 2.3 Testing Strategies

```solidity
// Foundry Test Example
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../src/ExampleToken.sol";

contract ExampleTokenTest is Test {
    ExampleToken token;
    address owner = address(1);
    address user = address(2);

    function setUp() public {
        vm.prank(owner);
        token = new ExampleToken();
    }

    function test_InitialSupply() public {
        assertEq(token.totalSupply(), 10_000_000 * 10**18);
        assertEq(token.balanceOf(owner), 10_000_000 * 10**18);
    }

    function test_Mint() public {
        vm.prank(owner);
        token.mint(user, 1000 * 10**18);
        assertEq(token.balanceOf(user), 1000 * 10**18);
    }

    function testFail_MintByNonOwner() public {
        vm.prank(user);
        token.mint(user, 1000 * 10**18);
    }

    // Fuzz test
    function testFuzz_Transfer(uint256 amount) public {
        amount = bound(amount, 0, token.balanceOf(owner));

        vm.prank(owner);
        token.transfer(user, amount);

        assertEq(token.balanceOf(user), amount);
    }

    // Invariant test
    function invariant_TotalSupply() public {
        assertLe(token.totalSupply(), token.MAX_SUPPLY());
    }
}
```

---

## 3. ESTÁNDARES EIP/ERC

### 3.1 Token Standards

```yaml
erc_20:
  nombre: Fungible Token Standard
  funciones:
    - totalSupply()
    - balanceOf(address)
    - transfer(address, uint256)
    - approve(address, uint256)
    - allowance(address, address)
    - transferFrom(address, address, uint256)
  eventos:
    - Transfer(from, to, value)
    - Approval(owner, spender, value)

erc_721:
  nombre: Non-Fungible Token Standard
  funciones:
    - balanceOf(address)
    - ownerOf(uint256)
    - safeTransferFrom(address, address, uint256)
    - transferFrom(address, address, uint256)
    - approve(address, uint256)
    - setApprovalForAll(address, bool)
    - getApproved(uint256)
    - isApprovedForAll(address, address)
  metadata:
    - name()
    - symbol()
    - tokenURI(uint256)

erc_1155:
  nombre: Multi-Token Standard
  features:
    - Fungible + Non-fungible
    - Batch transfers
    - Gas efficient
  funciones:
    - balanceOf(address, uint256)
    - balanceOfBatch(address[], uint256[])
    - safeTransferFrom(address, address, uint256, uint256, bytes)
    - safeBatchTransferFrom(...)

erc_4626:
  nombre: Tokenized Vault Standard
  use_case: Yield-bearing tokens
  funciones:
    - asset()
    - totalAssets()
    - convertToShares(uint256)
    - convertToAssets(uint256)
    - deposit(uint256, address)
    - withdraw(uint256, address, address)
```

### 3.2 Account Abstraction (ERC-4337)

```yaml
erc_4337:
  nombre: Account Abstraction
  componentes:
    entry_point:
      - Singleton contract
      - Validates UserOperations
      - Executes transactions

    user_operation:
      campos:
        - sender (smart account)
        - nonce
        - initCode (for deployment)
        - callData
        - callGasLimit
        - verificationGasLimit
        - preVerificationGas
        - maxFeePerGas
        - maxPriorityFeePerGas
        - paymasterAndData
        - signature

    smart_account:
      - Custom validation logic
      - Social recovery
      - Multi-sig
      - Session keys

    paymaster:
      - Sponsors gas
      - ERC20 payment
      - Subscription models

    bundler:
      - Aggregates UserOps
      - Submits to EntryPoint
      - Earns fees

  beneficios:
    - No need for ETH for gas
    - Batched transactions
    - Custom signature schemes
    - Account recovery
```

---

## 4. LAYER 2 ECOSYSTEM

### 4.1 Rollup Architecture

```
ROLLUP TYPES
│
├── OPTIMISTIC ROLLUPS
│   │
│   ├── Mechanism
│   │   ├── Transactions assumed valid
│   │   ├── Fraud proof window (~7 days)
│   │   ├── Challenger submits proof if invalid
│   │   └── Slashing if fraud proven
│   │
│   ├── Arbitrum
│   │   ├── Arbitrum One (main L2)
│   │   ├── Arbitrum Nova (AnyTrust)
│   │   ├── Nitro technology
│   │   ├── Stylus (Rust/C support)
│   │   └── Orbit (L3 framework)
│   │
│   ├── Optimism
│   │   ├── OP Mainnet
│   │   ├── OP Stack (framework)
│   │   ├── Superchain vision
│   │   └── Bedrock upgrade
│   │
│   └── Base
│       ├── By Coinbase
│       ├── OP Stack based
│       └── Consumer focus
│
└── ZK ROLLUPS
    │
    ├── Mechanism
    │   ├── Validity proofs
    │   ├── No challenge period
    │   ├── Cryptographic verification
    │   └── Instant finality (proof verified)
    │
    ├── zkSync Era
    │   ├── zkEVM (Type 4)
    │   ├── Native Account Abstraction
    │   ├── zkPorter (Validium mode)
    │   └── Boojum prover
    │
    ├── StarkNet
    │   ├── Cairo language
    │   ├── STARK proofs
    │   ├── Not EVM compatible
    │   └── Kakarot (EVM on StarkNet)
    │
    ├── Polygon zkEVM
    │   ├── Type 2 zkEVM
    │   ├── High EVM compatibility
    │   └── Polygon ecosystem
    │
    ├── Scroll
    │   ├── Type 2 zkEVM
    │   ├── Community focus
    │   └── EVM equivalence goal
    │
    └── Linea
        ├── By ConsenSys
        ├── Type 2 zkEVM
        └── MetaMask integration
```

### 4.2 Comparación L2s

```yaml
l2_comparison:
  arbitrum_one:
    type: Optimistic
    tps: ~40,000
    finality: ~7 days (fraud proof)
    gas_cost: ~$0.01-0.10
    evm: Full compatible
    tvl_rank: 1

  optimism:
    type: Optimistic
    tps: ~2,000
    finality: ~7 days
    gas_cost: ~$0.01-0.10
    evm: Full compatible (Bedrock)
    tvl_rank: 3

  base:
    type: Optimistic (OP Stack)
    tps: ~2,000
    finality: ~7 days
    gas_cost: ~$0.01-0.05
    evm: Full compatible
    tvl_rank: 2

  zksync_era:
    type: ZK Rollup
    tps: ~2,000+
    finality: ~24 hours (proof)
    gas_cost: ~$0.05-0.20
    evm: Type 4 (high level)
    tvl_rank: 4

  starknet:
    type: ZK Rollup (STARK)
    tps: Variable
    finality: Hours (STARK proof)
    gas_cost: ~$0.01-0.10
    evm: No (Cairo)
    tvl_rank: ~10

  polygon_zkevm:
    type: ZK Rollup
    tps: ~2,000
    finality: ~30 min
    gas_cost: ~$0.01-0.05
    evm: Type 2
    tvl_rank: ~8
```

---

## 5. DEFI EN ETHEREUM

### 5.1 Protocolos Principales

```yaml
uniswap:
  tipo: DEX/AMM
  versiones:
    v2: Constant product (x*y=k)
    v3: Concentrated liquidity
    v4: Hooks, singleton design
  innovaciones:
    - Flash swaps
    - Price oracles (TWAP)
    - LP NFTs (v3)

aave:
  tipo: Lending/Borrowing
  features:
    - Variable/stable rates
    - Flash loans
    - E-mode (efficiency)
    - Isolation mode
    - GHO stablecoin
  mecanismo:
    - aTokens (interest-bearing)
    - Debt tokens
    - Liquidations

makerdao:
  tipo: CDP / Stablecoin
  producto: DAI stablecoin
  mecanismo:
    - Collateralized debt positions
    - Stability fees
    - Liquidation auctions
    - PSM (stablecoin swaps)

lido:
  tipo: Liquid Staking
  producto: stETH
  features:
    - Stake ETH, receive stETH
    - Daily rebasing
    - DeFi composability
  market_share: ~30% of staked ETH

curve:
  tipo: DEX (stableswaps)
  innovaciones:
    - StableSwap invariant
    - Low slippage for pegged
    - veCRV tokenomics
    - Gauge voting

eigenlayer:
  tipo: Restaking
  concepto:
    - Re-use staked ETH
    - Secure other protocols
    - Additional yield
  riesgos:
    - Additional slashing
    - Systemic risk
```

### 5.2 MEV (Maximal Extractable Value)

```yaml
mev_ecosystem:

  tipos_mev:
    arbitrage:
      description: Price differences across DEXs
      impact: Generally positive (efficiency)

    sandwich:
      description: Front + back run user trades
      impact: Harmful to users
      mechanism:
        1: Detect large swap in mempool
        2: Front-run (buy before)
        3: User trade executes (price moves)
        4: Back-run (sell after)

    liquidations:
      description: Execute DeFi liquidations
      impact: Necessary for protocol health

    nft_sniping:
      description: Snipe underpriced NFTs
      impact: Mixed

  mev_supply_chain:
    searchers:
      - Find MEV opportunities
      - Submit bundles to builders

    builders:
      - Construct optimal blocks
      - Bid for block space

    relays:
      - Connect builders to validators
      - Flashbots relay
      - BloXroute, etc.

    validators:
      - Select highest bid block
      - Receive MEV rewards

  mev_protection:
    flashbots_protect:
      - Private mempool
      - No sandwich attacks
    mev_blocker:
      - CoW Protocol solution
    private_pools:
      - Direct to builders
```

---

## 6. SEGURIDAD ETHEREUM

### 6.1 Vulnerabilidades Comunes

```yaml
vulnerabilities:

  reentrancy:
    severity: CRITICAL
    example: The DAO hack (2016)
    pattern: |
      function withdraw() external {
          uint256 amount = balances[msg.sender];
          (bool success,) = msg.sender.call{value: amount}("");
          balances[msg.sender] = 0; // TOO LATE!
      }
    fix: Checks-Effects-Interactions + ReentrancyGuard

  access_control:
    severity: CRITICAL
    examples:
      - Missing onlyOwner
      - Incorrect visibility
      - tx.origin vs msg.sender
    fix: OpenZeppelin AccessControl

  integer_overflow:
    severity: HIGH
    note: Fixed in Solidity 0.8+
    pre_0_8: Use SafeMath
    post_0_8: Built-in checks

  oracle_manipulation:
    severity: HIGH
    pattern: Using spot price for critical operations
    fix: TWAP oracles, Chainlink

  front_running:
    severity: MEDIUM
    types:
      - Sandwich attacks
      - Transaction ordering
    fix: Commit-reveal, slippage limits

  denial_of_service:
    severity: MEDIUM
    patterns:
      - Unbounded loops
      - External call failures
    fix: Pull over push, gas limits
```

### 6.2 Best Practices

```yaml
security_best_practices:

  development:
    - Use latest Solidity version
    - OpenZeppelin contracts
    - Custom errors (not require strings)
    - NatSpec documentation
    - Comprehensive tests

  patterns:
    - Checks-Effects-Interactions
    - Pull over Push payments
    - Emergency pause functionality
    - Timelock for critical changes
    - Multi-sig for admin functions

  auditing:
    - Multiple audits recommended
    - Top firms: Trail of Bits, OpenZeppelin, Consensys Diligence
    - Bug bounty programs
    - Formal verification for critical code

  deployment:
    - Testnet deployment first
    - Gradual rollout
    - Monitoring and alerts
    - Incident response plan
```

---

## 7. HERRAMIENTAS Y RECURSOS

### 7.1 Development Tools

```yaml
tools:
  ides:
    - VS Code + Solidity extension
    - Remix IDE (browser)

  testing:
    - Hardhat
    - Foundry
    - Tenderly (debugging)

  security:
    - Slither (static analysis)
    - Mythril (symbolic execution)
    - Echidna (fuzzing)
    - Certora (formal verification)

  monitoring:
    - Tenderly
    - OpenZeppelin Defender
    - Forta

  analytics:
    - Etherscan
    - Dune Analytics
    - Nansen
```

### 7.2 RPC & Infrastructure

```yaml
rpc_providers:
  - Alchemy
  - Infura
  - QuickNode
  - Ankr
  - Blast

node_clients:
  execution:
    - Geth
    - Erigon
    - Nethermind
    - Reth

  consensus:
    - Prysm
    - Lighthouse
    - Teku
```

---

## FIRMA

```
╔═══════════════════════════════════════════════════════════════╗
║  NEURONA: ETHEREUM_MASTERY | C20001                          ║
║  "The World Computer - Complete Understanding"                ║
╚═══════════════════════════════════════════════════════════════╝
```
