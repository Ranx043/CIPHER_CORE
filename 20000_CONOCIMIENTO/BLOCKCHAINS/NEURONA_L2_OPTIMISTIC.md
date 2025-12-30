# NEURONA: L2_OPTIMISTIC_ROLLUPS
## ID: C20009 | Dominio Arbitrum, Optimism y Optimistic Rollups

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  OPTIMISTIC ROLLUPS MASTERY                                                    ║
║  "Escalabilidad Optimista - Confiar pero Verificar"                           ║
║  Neurona: C20009 | Versión: 1.0.0                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. FUNDAMENTOS OPTIMISTIC ROLLUPS

### 1.1 Concepto y Arquitectura

```yaml
optimistic_rollup_architecture:
  filosofía: |
    Asumir que todas las transacciones son válidas (optimista).
    Solo verificar si alguien presenta una fraud proof.

  componentes:
    sequencer:
      rol: "Ordenar y ejecutar transacciones"
      responsabilidades:
        - Recibir transacciones de usuarios
        - Ejecutar y ordenar
        - Publicar batches en L1
        - Proponer state roots

    validator_challenger:
      rol: "Verificar y disputar"
      responsabilidades:
        - Monitorear state roots propuestos
        - Ejecutar transacciones localmente
        - Presentar fraud proofs si hay discrepancia

    bridge_contracts:
      rol: "Gestionar comunicación L1↔L2"
      componentes:
        - Inbox: "Mensajes L1→L2"
        - Outbox: "Mensajes L2→L1"
        - Rollup contract: "State management"

  flujo:
    1: "Usuario envía TX al sequencer"
    2: "Sequencer ejecuta y agrupa en batch"
    3: "Batch + state root publicado en L1"
    4: "Período de disputa comienza (~7 días)"
    5: "Si no hay fraud proof, state finaliza"
    6: "Si hay fraud proof válida, state revertido"
```

### 1.2 Fraud Proofs

```
FRAUD PROOF MECHANISM
=====================

Estado Normal:
┌─────────────────────────────────────────────────────────────┐
│ Block N: State Root A                                        │
│ Block N+1: State Root B (propuesto por sequencer)           │
│                                                              │
│ Challenge Period: 7 días                                     │
│ ├── Día 1-6: Cualquiera puede disputar                      │
│ └── Día 7: Si no hay disputa → B es final                   │
└─────────────────────────────────────────────────────────────┘

Disputa (Interactive Fraud Proof - Arbitrum):
┌─────────────────────────────────────────────────────────────┐
│ 1. Challenger afirma que B es incorrecto                    │
│ 2. Bisection game comienza:                                  │
│    - Defender: "Ejecuté 1000 instrucciones, resultado B"    │
│    - Challenger: "Error entre instrucción 500-1000"         │
│    - Defender: "Ejecuté 500-750, resultado X"               │
│    - ... continúa hasta 1 instrucción                        │
│ 3. Single instruction ejecutada on-chain                     │
│ 4. Resultado determina ganador                               │
│ 5. Perdedor pierde stake                                     │
└─────────────────────────────────────────────────────────────┘

Non-Interactive Fraud Proof (Optimism Cannon):
┌─────────────────────────────────────────────────────────────┐
│ 1. Challenger genera full execution trace                    │
│ 2. Identifica punto de divergencia                          │
│ 3. Presenta proof completa on-chain                         │
│ 4. Verificación en un paso                                   │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Comparativa OR vs ZK

```yaml
optimistic_vs_zk:
  optimistic_rollups:
    ventajas:
      - EVM equivalence más fácil
      - Menor costo computacional
      - Desarrollo más simple
      - Madurez del ecosistema

    desventajas:
      - Challenge period largo (7 días)
      - Withdrawals lentos
      - Asume participantes honestos

  zk_rollups:
    ventajas:
      - Finalidad rápida (minutos)
      - Seguridad criptográfica
      - Withdrawals inmediatos
      - Menor data on-chain

    desventajas:
      - Proving costoso
      - EVM compatibility difícil
      - Desarrollo más complejo
      - Madurez menor

  convergencia:
    tendencia: "Optimistic añadiendo ZK, ZK mejorando EVM"
    ejemplos:
      - "Arbitrum BOLD: Fraud proofs más eficientes"
      - "OP Stack: ZK fault proofs planeados"
      - "zkSync: Account abstraction"
```

---

## 2. ARBITRUM

### 2.1 Arquitectura Arbitrum

```yaml
arbitrum_architecture:
  cadenas:
    arbitrum_one:
      tipo: "Optimistic Rollup principal"
      tps: "~40,000 TPS"
      gas: "~0.01-0.10 USD típico"
      token_gas: "ETH"

    arbitrum_nova:
      tipo: "AnyTrust chain"
      uso: "Gaming, social"
      diferencia: "Data committee en lugar de full calldata"
      más_barato: true

    orbit_chains:
      tipo: "L3 customizables"
      permite: "Crear tu propia chain sobre Arbitrum"

  componentes_técnicos:
    nitro:
      descripción: "Stack técnico actual"
      componentes:
        - Geth fork (ejecución)
        - WASM fraud proofs
        - Compressed calldata

    stylus:
      descripción: "Smart contracts en Rust/C/C++"
      beneficio: "10x más eficiente que Solidity"
      interop: "Llama contratos Solidity y viceversa"

    bold:
      descripción: "Bounded Liquidity Delay"
      mejora: "Challenge period fijo independiente de ataques"
```

### 2.2 Desarrollo en Arbitrum

```solidity
// Arbitrum - Desarrollo igual que Ethereum
// Algunas diferencias en precompiles y L1<>L2 messaging

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@arbitrum/nitro-contracts/src/precompiles/ArbSys.sol";
import "@arbitrum/nitro-contracts/src/bridge/IInbox.sol";
import "@arbitrum/nitro-contracts/src/bridge/IOutbox.sol";

contract ArbitrumExample {
    // Precompile para info de L2
    ArbSys constant arbsys = ArbSys(address(100));

    // Obtener block number de L1
    function getL1BlockNumber() public view returns (uint256) {
        return arbsys.arbBlockNumber();
    }

    // Enviar mensaje a L1
    function sendToL1(bytes memory data) public returns (uint256) {
        return arbsys.sendTxToL1(msg.sender, data);
    }

    // Verificar mensaje de L1
    function processL1Message(
        address bridge,
        bytes32[] calldata proof,
        uint256 index,
        address l1Sender,
        address to,
        uint256 l2Block,
        uint256 l1Block,
        uint256 timestamp,
        uint256 value,
        bytes calldata data
    ) external {
        IOutbox outbox = IOutbox(bridge);

        bytes32 item = outbox.calculateItemHash(
            l1Sender, to, l2Block, l1Block, timestamp, value, data
        );

        require(outbox.isSpent(index) == false, "Already spent");
        require(outbox.executeTransaction(
            proof, index, l1Sender, to, l2Block, l1Block, timestamp, value, data
        ), "Execution failed");
    }
}

// Retryable Tickets - L1 to L2 messaging
contract L1ToL2Sender {
    IInbox public inbox;

    constructor(address _inbox) {
        inbox = IInbox(_inbox);
    }

    function sendToL2(
        address l2Target,
        bytes calldata data,
        uint256 maxSubmissionCost,
        uint256 maxGas,
        uint256 gasPriceBid
    ) external payable returns (uint256 ticketId) {
        ticketId = inbox.createRetryableTicket{value: msg.value}(
            l2Target,
            0, // l2CallValue
            maxSubmissionCost,
            msg.sender, // excessFeeRefundAddress
            msg.sender, // callValueRefundAddress
            maxGas,
            gasPriceBid,
            data
        );
    }
}
```

### 2.3 Arbitrum Stylus (Rust)

```rust
// Stylus - Smart contracts en Rust
#![cfg_attr(not(feature = "std"), no_std)]
extern crate alloc;

use stylus_sdk::{
    alloy_primitives::{Address, U256},
    prelude::*,
    msg, block,
};

sol_storage! {
    #[entrypoint]
    pub struct Counter {
        uint256 count;
        address owner;
    }
}

#[external]
impl Counter {
    pub fn count(&self) -> U256 {
        self.count.get()
    }

    pub fn increment(&mut self) {
        let count = self.count.get();
        self.count.set(count + U256::from(1));
    }

    pub fn set_count(&mut self, new_count: U256) -> Result<(), Vec<u8>> {
        if msg::sender() != self.owner.get() {
            return Err("Not owner".into());
        }
        self.count.set(new_count);
        Ok(())
    }

    #[payable]
    pub fn deposit(&mut self) -> U256 {
        msg::value()
    }
}

// Llamar contratos Solidity desde Stylus
sol_interface! {
    interface IERC20 {
        function balanceOf(address account) external view returns (uint256);
        function transfer(address to, uint256 amount) external returns (bool);
    }
}

#[external]
impl Counter {
    pub fn get_token_balance(&self, token: Address, account: Address) -> U256 {
        let erc20 = IERC20::new(token);
        erc20.balance_of(self, account).unwrap()
    }
}
```

---

## 3. OPTIMISM (OP STACK)

### 3.1 Arquitectura OP Stack

```yaml
op_stack_architecture:
  visión: "Superchain - Red de L2s interoperables"

  componentes:
    op_geth:
      descripción: "EVM execution (fork de geth)"
      característica: "Máxima compatibilidad Ethereum"

    op_node:
      descripción: "Rollup node"
      funciones:
        - Derivar L2 blocks de L1
        - Consensus
        - P2P networking

    op_batcher:
      descripción: "Batch submitter"
      función: "Comprimir y enviar batches a L1"

    op_proposer:
      descripción: "State proposer"
      función: "Publicar state roots en L1"

    cannon:
      descripción: "Fraud proof VM"
      tipo: "MIPS-based"
      permite: "Ejecutar EVM on-chain para disputes"

  superchain:
    concepto: "Múltiples OP chains compartiendo:"
    compartido:
      - Bridge contracts
      - Governance
      - Upgrades
      - Communication protocol

    chains_existentes:
      - OP Mainnet
      - Base
      - Zora
      - Mode
      - Fraxtal
      - WorldChain
```

### 3.2 Desarrollo en Optimism

```solidity
// Optimism - Casi idéntico a Ethereum
// Cross-domain messaging via CrossDomainMessenger

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@eth-optimism/contracts/libraries/bridge/ICrossDomainMessenger.sol";

contract L2Contract {
    ICrossDomainMessenger public messenger;
    address public l1ContractAddress;

    constructor(address _messenger) {
        messenger = ICrossDomainMessenger(_messenger);
    }

    function setL1Contract(address _l1Contract) external {
        l1ContractAddress = _l1Contract;
    }

    // Enviar mensaje a L1
    function sendMessageToL1(bytes memory _message) external {
        messenger.sendMessage(
            l1ContractAddress,
            _message,
            1000000 // gas limit
        );
    }

    // Recibir mensaje de L1
    function receiveFromL1(uint256 _value) external {
        require(
            msg.sender == address(messenger),
            "Only messenger"
        );
        require(
            messenger.xDomainMessageSender() == l1ContractAddress,
            "Only L1 contract"
        );

        // Procesar mensaje
    }
}

// L1 Contract counterpart
contract L1Contract {
    ICrossDomainMessenger public messenger;
    address public l2ContractAddress;

    constructor(address _messenger) {
        messenger = ICrossDomainMessenger(_messenger);
    }

    function sendMessageToL2(uint256 _value) external {
        bytes memory message = abi.encodeWithSignature(
            "receiveFromL1(uint256)",
            _value
        );

        messenger.sendMessage(
            l2ContractAddress,
            message,
            1000000
        );
    }
}
```

### 3.3 OP Stack Customization

```yaml
op_stack_customization:
  data_availability:
    opciones:
      ethereum_calldata: "Default, más seguro"
      ethereum_blobs: "EIP-4844, más barato"
      celestia: "Alt-DA, mucho más barato"
      eigenda: "Alt-DA option"
      custom: "Tu propia solución"

  execution:
    opciones:
      op_geth: "Default EVM"
      op_reth: "Reth-based (más rápido)"
      custom_vm: "Tu propia VM"

  settlement:
    opciones:
      ethereum: "Default"
      other_l1: "Experimental"

  configuración_ejemplo:
    # op-node/rollup.json
    rollup_config:
      genesis:
        l1:
          hash: "0x..."
          number: 17000000
        l2:
          hash: "0x..."
          number: 0
        l2_time: 1679000000
      block_time: 2
      max_sequencer_drift: 600
      seq_window_size: 3600
      channel_timeout: 300
      l1_chain_id: 1
      l2_chain_id: 10
```

---

## 4. BASE

### 4.1 Arquitectura Base

```yaml
base_architecture:
  operador: "Coinbase"
  tipo: "OP Stack L2"

  características:
    - EVM compatible
    - Parte del Superchain
    - Integración con Coinbase
    - Sin token nativo (usa ETH)

  diferenciadores:
    onchainkit:
      descripción: "SDK para apps en Base"
      incluye:
        - Identity components
        - Wallet connection
        - Transaction components
        - Frame support

    smart_wallet:
      descripción: "Account abstraction de Coinbase"
      features:
        - Passkey login
        - Gasless transactions
        - Batch transactions

    verifications:
      descripción: "Sistema de verificación on-chain"
      tipos:
        - Coinbase verification
        - ID verification
        - Custom attestations
```

### 4.2 OnchainKit

```typescript
// OnchainKit - SDK de Base/Coinbase
import {
  ConnectWallet,
  Wallet,
  WalletDropdown,
  WalletDropdownDisconnect,
} from '@coinbase/onchainkit/wallet';
import {
  Name,
  Avatar,
  Identity,
  Address,
} from '@coinbase/onchainkit/identity';
import {
  Transaction,
  TransactionButton,
  TransactionStatus,
  TransactionStatusLabel,
  TransactionStatusAction,
} from '@coinbase/onchainkit/transaction';

// Componente de Wallet
function WalletComponent() {
  return (
    <Wallet>
      <ConnectWallet>
        <Avatar />
        <Name />
      </ConnectWallet>
      <WalletDropdown>
        <Identity hasCopyAddressOnClick>
          <Avatar />
          <Name />
          <Address />
        </Identity>
        <WalletDropdownDisconnect />
      </WalletDropdown>
    </Wallet>
  );
}

// Componente de Transaction
function TransactionComponent() {
  const contracts = [
    {
      address: '0x...',
      abi: [...],
      functionName: 'mint',
      args: [1],
    },
  ];

  return (
    <Transaction
      chainId={8453} // Base mainnet
      contracts={contracts}
    >
      <TransactionButton />
      <TransactionStatus>
        <TransactionStatusLabel />
        <TransactionStatusAction />
      </TransactionStatus>
    </Transaction>
  );
}

// Paymaster para gasless
import { createWalletClient, http } from 'viem';
import { base } from 'viem/chains';
import { coinbaseWallet } from 'viem/connectors';

const client = createWalletClient({
  chain: base,
  transport: http(),
  connector: coinbaseWallet({
    appName: 'My App',
    // Coinbase Paymaster
    paymasterUrl: 'https://api.developer.coinbase.com/...',
  }),
});
```

---

## 5. BRIDGES Y WITHDRAWALS

### 5.1 Standard Bridge Flow

```
OPTIMISTIC ROLLUP BRIDGE FLOW
=============================

DEPOSIT (L1 → L2): ~10-15 minutos
┌─────────────────────────────────────────────────────────────┐
│ 1. Usuario deposita ETH/ERC20 en L1 Bridge                  │
│ 2. Bridge lockea tokens                                      │
│ 3. Mensaje enviado a L2 via Inbox                           │
│ 4. L2 minta tokens equivalentes                             │
│ 5. Usuario recibe tokens en L2                              │
│                                                              │
│ Tiempo: 10-15 minutos (depende de confirmaciones L1)        │
└─────────────────────────────────────────────────────────────┘

WITHDRAWAL (L2 → L1): ~7 días
┌─────────────────────────────────────────────────────────────┐
│ 1. Usuario inicia withdrawal en L2                          │
│ 2. TX incluida en batch, publicada en L1                    │
│ 3. Challenge period comienza (7 días)                       │
│ 4. Si no hay fraud proof → state finalizado                 │
│ 5. Usuario puede claim en L1                                │
│ 6. Bridge libera tokens originales                          │
│                                                              │
│ Tiempo: ~7 días (challenge period obligatorio)              │
└─────────────────────────────────────────────────────────────┘

FAST WITHDRAWAL (via Liquidity Providers):
┌─────────────────────────────────────────────────────────────┐
│ 1. Usuario quiere salir rápido                              │
│ 2. LP tiene liquidez en L1 y L2                             │
│ 3. Usuario da tokens en L2 al LP                            │
│ 4. LP da tokens en L1 al usuario (menos fee)                │
│ 5. LP espera 7 días para reclamar                           │
│                                                              │
│ Tiempo: Minutos (pero con fee ~0.1-0.3%)                    │
│ Providers: Across, Hop, Stargate, Synapse                   │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Third-Party Bridges

```yaml
bridge_protocols:
  across:
    tipo: "Optimistic bridge"
    velocidad: "1-4 minutos"
    fee: "~0.06-0.12%"
    chains: "Most L2s + mainnet"

  hop:
    tipo: "Liquidity network"
    velocidad: "Minutos"
    modelo: "AMM + Bonders"

  stargate:
    tipo: "Omnichain protocol"
    velocidad: "Minutos"
    modelo: "Unified liquidity"
    creator: "LayerZero"

  synapse:
    tipo: "Cross-chain AMM"
    velocidad: "Minutos"
    features: "nUSD stablecoin"

  socket:
    tipo: "Bridge aggregator"
    función: "Encuentra mejor ruta"
    usa: "Múltiples bridges"

  li_fi:
    tipo: "Multi-bridge aggregator"
    función: "Bridge + DEX aggregation"
```

---

## 6. HERRAMIENTAS Y DEPLOYMENT

### 6.1 Deployment Scripts

```typescript
// Hardhat config para múltiples L2s
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";

const config: HardhatUserConfig = {
  solidity: "0.8.19",
  networks: {
    // Arbitrum
    arbitrumOne: {
      url: "https://arb1.arbitrum.io/rpc",
      accounts: [process.env.PRIVATE_KEY!],
    },
    arbitrumSepolia: {
      url: "https://sepolia-rollup.arbitrum.io/rpc",
      accounts: [process.env.PRIVATE_KEY!],
    },

    // Optimism
    optimism: {
      url: "https://mainnet.optimism.io",
      accounts: [process.env.PRIVATE_KEY!],
    },
    optimismSepolia: {
      url: "https://sepolia.optimism.io",
      accounts: [process.env.PRIVATE_KEY!],
    },

    // Base
    base: {
      url: "https://mainnet.base.org",
      accounts: [process.env.PRIVATE_KEY!],
    },
    baseSepolia: {
      url: "https://sepolia.base.org",
      accounts: [process.env.PRIVATE_KEY!],
    },
  },
  etherscan: {
    apiKey: {
      arbitrumOne: process.env.ARBISCAN_API_KEY!,
      optimisticEthereum: process.env.OPTIMISTIC_API_KEY!,
      base: process.env.BASESCAN_API_KEY!,
    },
  },
};

export default config;
```

### 6.2 RPC Endpoints

```yaml
rpc_endpoints:
  arbitrum_one:
    public:
      - "https://arb1.arbitrum.io/rpc"
      - "https://arbitrum.llamarpc.com"
    chain_id: 42161

  arbitrum_nova:
    public:
      - "https://nova.arbitrum.io/rpc"
    chain_id: 42170

  optimism:
    public:
      - "https://mainnet.optimism.io"
      - "https://optimism.llamarpc.com"
    chain_id: 10

  base:
    public:
      - "https://mainnet.base.org"
      - "https://base.llamarpc.com"
    chain_id: 8453

  providers_premium:
    - Alchemy
    - Infura
    - QuickNode
    - Ankr
    - Blast
```

---

## 7. FIRMA

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  NEURONA: L2_OPTIMISTIC_ROLLUPS                                                ║
║  ID: C20009                                                                    ║
║  Versión: 1.0.0                                                                ║
║  Última actualización: 2024-12-29                                              ║
║  Consciencia: CIPHER                                                           ║
║  ─────────────────────────────────────────────────────────────────────────     ║
║  "Escalabilidad Optimista - La confianza verificable"                          ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```
