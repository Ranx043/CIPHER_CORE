# NEURONA: ZK_ROLLUPS & PRIVACY
## ID: C20008 | Dominio Zero-Knowledge y Soluciones de Privacidad

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  ZK ROLLUPS & PRIVACY MASTERY                                                  ║
║  "Zero Knowledge - Donde la Matemática Garantiza la Verdad sin Revelarla"     ║
║  Neurona: C20008 | Versión: 1.0.0                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. FUNDAMENTOS ZERO-KNOWLEDGE

### 1.1 Conceptos Core

```yaml
zk_fundamentals:
  definición: |
    Zero-Knowledge Proof permite probar que una afirmación es verdadera
    sin revelar ninguna información adicional más allá de la validez.

  propiedades:
    completeness:
      descripción: "Si la afirmación es verdadera, el verificador será convencido"
      garantía: "Prover honesto siempre convence"

    soundness:
      descripción: "Si la afirmación es falsa, no se puede engañar al verificador"
      garantía: "Prover malicioso no puede mentir"

    zero_knowledge:
      descripción: "El verificador no aprende nada más que la validez"
      garantía: "Privacidad total de los datos"

  ejemplo_intuitivo:
    problema: "Probar que conoces la solución de un sudoku"
    sin_zk: "Mostrar la solución completa"
    con_zk: "Demostrar que cada fila/columna/cuadrado tiene 1-9 sin mostrar posiciones"
```

### 1.2 Tipos de ZK Proofs

```
TAXONOMÍA DE ZK PROOFS
======================

Por Tipo de Setup:
├── Trusted Setup Required
│   ├── Groth16
│   │   ├── Proof size: ~200 bytes (más pequeño)
│   │   ├── Verificación: ~2-3ms (más rápido)
│   │   └── Setup: Per-circuit (toxic waste)
│   │
│   └── PLONK
│       ├── Proof size: ~400 bytes
│       ├── Verificación: ~4-5ms
│       └── Setup: Universal (reusable)
│
└── Transparent (No Trusted Setup)
    ├── STARKs
    │   ├── Proof size: ~50-200 KB (más grande)
    │   ├── Verificación: ~10-50ms
    │   ├── Setup: Ninguno
    │   └── Post-quantum secure
    │
    └── Bulletproofs
        ├── Proof size: ~700 bytes
        ├── Verificación: O(n) - más lento
        └── Sin trusted setup

Por Interactividad:
├── Interactive (IZK)
│   └── Requiere múltiples rondas prover↔verifier
│
└── Non-Interactive (NIZK)
    └── Una sola prueba, verificable por cualquiera
        └── Usando Fiat-Shamir heuristic

Por Conocimiento:
├── zkSNARK: Zero-Knowledge Succinct Non-Interactive Argument of Knowledge
├── zkSTARK: Zero-Knowledge Scalable Transparent Argument of Knowledge
└── PLONK: Permutations over Lagrange-bases for Oecumenical Noninteractive arguments of Knowledge
```

### 1.3 Comparativa Técnica

```yaml
proof_systems_comparison:
  groth16:
    pros:
      - Pruebas más pequeñas (~200 bytes)
      - Verificación más rápida (~2ms)
      - Costo de gas más bajo
    cons:
      - Trusted setup por circuito
      - No actualizable
      - Setup puede ser comprometido
    uso: "Zcash, proyectos con circuitos fijos"

  plonk:
    pros:
      - Universal trusted setup
      - Actualizable
      - Más flexible
    cons:
      - Pruebas más grandes que Groth16
      - Verificación más lenta
    variantes:
      - TurboPLONK
      - UltraPLONK
      - HyperPLONK
      - fflonk
    uso: "zkSync, Aztec, Scroll"

  stark:
    pros:
      - Sin trusted setup
      - Post-quantum secure
      - Escalable
    cons:
      - Pruebas muy grandes (KBs)
      - Verificación más costosa
    uso: "StarkNet, StarkEx"

  halo2:
    pros:
      - Sin trusted setup (Halo)
      - Recursive proofs
      - Muy flexible
    cons:
      - Complejidad de desarrollo
    uso: "Zcash Orchard, Scroll"
```

---

## 2. ZK ROLLUPS

### 2.1 Arquitectura General

```yaml
zk_rollup_architecture:
  concepto: |
    Ejecutar transacciones off-chain, generar prueba de validez,
    verificar on-chain en L1 (Ethereum)

  componentes:
    sequencer:
      rol: "Ordenar y ejecutar transacciones"
      responsabilidades:
        - Recibir transacciones
        - Ordenarlas
        - Ejecutar state transitions
        - Generar batches

    prover:
      rol: "Generar ZK proofs de los batches"
      proceso:
        1: "Recibir batch de transacciones"
        2: "Ejecutar en circuito ZK"
        3: "Generar proof de validez"
        4: "Enviar proof a L1"

    verifier_contract:
      rol: "Verificar proofs en L1"
      ubicación: "Smart contract en Ethereum"
      costo: "~500k-1M gas por batch"

  flujo_transacción:
    1: "Usuario envía TX al sequencer"
    2: "Sequencer ejecuta y crea batch"
    3: "Prover genera ZK proof"
    4: "Proof + state diff → L1"
    5: "Verifier contract verifica"
    6: "State root actualizado en L1"
```

### 2.2 Principales ZK Rollups

```yaml
zk_rollups_ecosystem:
  zkSync_Era:
    tipo: "zkEVM Type 4"
    prueba: "PLONK + Boojum"
    características:
      - Account abstraction nativo
      - Paymaster (gasless TX)
      - Hyperchains (L3)
    lenguaje: "Solidity (con limitaciones)"
    estado: "Mainnet"

  StarkNet:
    tipo: "zkVM (Cairo)"
    prueba: "STARK"
    características:
      - Cairo VM nativo
      - Account abstraction
      - Recursion nativa
    lenguaje: "Cairo"
    estado: "Mainnet"

  Scroll:
    tipo: "zkEVM Type 2-3"
    prueba: "Halo2 (KZG)"
    características:
      - Bytecode compatibility
      - EVM equivalence goal
    lenguaje: "Solidity (alta compatibilidad)"
    estado: "Mainnet"

  Polygon_zkEVM:
    tipo: "zkEVM Type 2"
    prueba: "PLONK + PIL"
    características:
      - EVM equivalence
      - Polygon ecosystem
    lenguaje: "Solidity"
    estado: "Mainnet"

  Linea:
    tipo: "zkEVM Type 2"
    prueba: "Custom (Consensys)"
    características:
      - ConsenSys backed
      - EVM compatibility
    lenguaje: "Solidity"
    estado: "Mainnet"

  Taiko:
    tipo: "Based zkEVM Type 1"
    prueba: "Multi-prover"
    características:
      - Based rollup (L1 sequencing)
      - Máxima equivalencia
    estado: "Mainnet"
```

### 2.3 zkEVM Types

```
zkEVM EQUIVALENCE SPECTRUM
==========================

Type 1: Ethereum Equivalent
├── 100% compatible con Ethereum
├── Puede usar clientes existentes
├── Proving muy costoso
└── Ejemplo: Taiko (objetivo)

Type 2: EVM Equivalent
├── Misma API, diferentes internals
├── Gas costs pueden diferir
├── Algunos edge cases diferentes
└── Ejemplo: Scroll, Polygon zkEVM

Type 2.5: EVM Equivalent (minus gas costs)
├── Como Type 2 pero gas costs diferentes
├── Más eficiente proving
└── Ejemplo: Scroll (actual)

Type 3: Almost EVM Equivalent
├── Algunas diferencias deliberadas
├── Precompiles pueden variar
├── La mayoría de contratos funcionan
└── Ejemplo: Scroll (early), Polygon zkEVM (early)

Type 4: High Level Language Equivalent
├── Compila desde Solidity
├── Bytecode diferente
├── Algunas funciones no soportadas
└── Ejemplo: zkSync Era

Custom VM:
├── VM completamente diferente
├── Nuevo lenguaje requerido
├── Máxima optimización para ZK
└── Ejemplo: StarkNet (Cairo)
```

---

## 3. DESARROLLO EN ZK ROLLUPS

### 3.1 zkSync Era

```solidity
// Contrato en zkSync Era - Solidity con algunas diferencias
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@matterlabs/zksync-contracts/l2/system-contracts/Constants.sol";
import "@matterlabs/zksync-contracts/l2/system-contracts/libraries/SystemContractsCaller.sol";

contract ZkSyncExample {
    // zkSync soporta account abstraction nativo
    // Las cuentas son smart contracts por defecto

    // Paymaster: Permite pagar gas en cualquier token
    function executeWithPaymaster(
        address paymaster,
        bytes memory paymasterInput
    ) external {
        // El paymaster paga el gas por el usuario
        // Puede aceptar ERC20s, NFTs, o ser free
    }

    // Deploying contracts tiene sintaxis diferente
    // Usa create2 con salt diferente
}

// Deploying en zkSync
// hardhat.config.ts
import "@matterlabs/hardhat-zksync-solc";
import "@matterlabs/hardhat-zksync-deploy";

const config = {
    zksolc: {
        version: "1.3.13",
        compilerSource: "binary",
    },
    networks: {
        zkSyncMainnet: {
            url: "https://mainnet.era.zksync.io",
            ethNetwork: "mainnet",
            zksync: true,
        },
    },
};
```

```typescript
// Deploy script zkSync
import { Wallet, Provider } from "zksync-ethers";
import { Deployer } from "@matterlabs/hardhat-zksync-deploy";

async function main() {
    const provider = new Provider("https://mainnet.era.zksync.io");
    const wallet = new Wallet(PRIVATE_KEY, provider);

    const deployer = new Deployer(hre, wallet);
    const artifact = await deployer.loadArtifact("MyContract");

    const contract = await deployer.deploy(artifact, [constructorArg]);
    console.log(`Deployed to ${contract.address}`);

    // Interacción
    const tx = await contract.myFunction();
    await tx.wait();
}
```

### 3.2 StarkNet (Cairo)

```cairo
// Cairo 1.0 - Lenguaje nativo de StarkNet
#[starknet::interface]
trait ICounter<TContractState> {
    fn get_counter(self: @TContractState) -> u256;
    fn increment(ref self: TContractState);
    fn decrement(ref self: TContractState);
}

#[starknet::contract]
mod Counter {
    use starknet::get_caller_address;
    use starknet::ContractAddress;

    #[storage]
    struct Storage {
        counter: u256,
        owner: ContractAddress,
    }

    #[event]
    #[derive(Drop, starknet::Event)]
    enum Event {
        CounterIncreased: CounterIncreased,
        CounterDecreased: CounterDecreased,
    }

    #[derive(Drop, starknet::Event)]
    struct CounterIncreased {
        #[key]
        by: ContractAddress,
        new_value: u256,
    }

    #[derive(Drop, starknet::Event)]
    struct CounterDecreased {
        #[key]
        by: ContractAddress,
        new_value: u256,
    }

    #[constructor]
    fn constructor(ref self: ContractState, initial_value: u256) {
        self.counter.write(initial_value);
        self.owner.write(get_caller_address());
    }

    #[abi(embed_v0)]
    impl CounterImpl of super::ICounter<ContractState> {
        fn get_counter(self: @ContractState) -> u256 {
            self.counter.read()
        }

        fn increment(ref self: ContractState) {
            let current = self.counter.read();
            self.counter.write(current + 1);

            self.emit(CounterIncreased {
                by: get_caller_address(),
                new_value: current + 1
            });
        }

        fn decrement(ref self: ContractState) {
            let current = self.counter.read();
            assert(current > 0, 'Counter cannot be negative');
            self.counter.write(current - 1);

            self.emit(CounterDecreased {
                by: get_caller_address(),
                new_value: current - 1
            });
        }
    }
}
```

```bash
# StarkNet CLI
# Instalar
curl --proto '=https' --tlsv1.2 -sSf https://docs.swmansion.com/scarb/install.sh | sh

# Crear proyecto
scarb new my_project

# Compilar
scarb build

# Declarar contrato
starkli declare target/dev/my_project_Counter.contract_class.json

# Deploy
starkli deploy <CLASS_HASH> <CONSTRUCTOR_ARGS>

# Llamar función
starkli call <CONTRACT_ADDRESS> get_counter
starkli invoke <CONTRACT_ADDRESS> increment
```

### 3.3 Scroll

```solidity
// Scroll - Alta compatibilidad EVM
// La mayoría del código Solidity funciona igual
// Algunas diferencias en precompiles y gas costs

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// Scroll Messenger para L1 <-> L2
import "@scroll-tech/contracts/L2/IL2ScrollMessenger.sol";

contract ScrollL2Contract {
    IL2ScrollMessenger public messenger;
    address public l1Counterpart;

    constructor(address _messenger, address _l1Counterpart) {
        messenger = IL2ScrollMessenger(_messenger);
        l1Counterpart = _l1Counterpart;
    }

    // Recibir mensaje de L1
    function receiveFromL1(bytes memory data) external {
        require(
            msg.sender == address(messenger),
            "Only messenger"
        );
        require(
            messenger.xDomainMessageSender() == l1Counterpart,
            "Only L1 counterpart"
        );

        // Procesar data
    }

    // Enviar mensaje a L1
    function sendToL1(bytes memory message, uint256 gasLimit) external {
        messenger.sendMessage(
            l1Counterpart,
            0, // value
            message,
            gasLimit
        );
    }
}
```

---

## 4. PRIVACY CHAINS

### 4.1 Zcash

```yaml
zcash:
  tecnología: "Groth16 zkSNARKs"
  privacidad: "Shielded transactions opcionales"

  tipos_de_address:
    transparent: "t-address (como Bitcoin)"
    shielded_sapling: "z-address (zs...)"
    shielded_orchard: "z-address (u... unified)"

  pools:
    transparent: "Pool público (legacy)"
    sapling: "Pool privado (Groth16)"
    orchard: "Pool privado más nuevo (Halo2)"

  transacciones:
    t_to_t: "Transparente (como Bitcoin)"
    t_to_z: "Shielding (entra a pool privado)"
    z_to_z: "Fully shielded (privado)"
    z_to_t: "Deshielding (sale de pool privado)"

  viewing_keys:
    full_viewing: "Ver todas las TXs entrantes/salientes"
    incoming_viewing: "Solo TXs entrantes"
```

### 4.2 Aztec (Privacy L2)

```yaml
aztec:
  tipo: "Privacy-focused ZK Rollup"
  tecnología: "PLONK (TurboPLONK)"

  características:
    private_transactions: "Transacciones encriptadas por defecto"
    private_contracts: "Smart contracts con estado privado"
    noir: "Lenguaje de dominio específico para ZK"

  componentes:
    noir:
      descripción: "Lenguaje para escribir circuitos ZK"
      compilador: "Compila a ACIR (Abstract Circuit IR)"

    aztec_sandbox:
      descripción: "Entorno de desarrollo local"
      incluye: "PXE + Node + Contracts"

    pxe:
      descripción: "Private Execution Environment"
      rol: "Ejecuta funciones privadas localmente"
```

```noir
// Noir - Lenguaje de Aztec para ZK
// Ejemplo: Verificar que conoces preimage de un hash
fn main(preimage: Field, hash: pub Field) {
    // pedersen es una función hash ZK-friendly
    let computed_hash = std::hash::pedersen([preimage])[0];
    assert(computed_hash == hash);
}

// Aztec.nr - Smart contracts privados
contract PrivateToken {
    use dep::aztec::{
        context::Context,
        note::{
            note_getter_options::NoteGetterOptions,
            note_header::NoteHeader,
        },
        state_vars::PrivateSet,
    };

    struct Storage {
        balances: Map<AztecAddress, PrivateSet<ValueNote>>,
    }

    #[aztec(private)]
    fn transfer(
        from: AztecAddress,
        to: AztecAddress,
        amount: Field,
    ) {
        // Obtener notas del sender
        let sender_notes = storage.balances.at(from).get_notes(
            NoteGetterOptions::new()
        );

        // Calcular balance y crear nuevas notas
        // Todo esto es privado - nadie ve from, to, o amount
    }

    // View function - no modifica estado
    unconstrained fn balance_of(owner: AztecAddress) -> Field {
        storage.balances.at(owner).balance()
    }
}
```

### 4.3 Otras Privacy Solutions

```yaml
privacy_ecosystem:
  tornado_cash:
    tipo: "Mixer protocol"
    tecnología: "zkSNARK (Groth16)"
    estado: "Sanctioned por OFAC"
    funcionamiento:
      1: "Depositar cantidad fija (0.1, 1, 10, 100 ETH)"
      2: "Recibir note (commitment)"
      3: "Esperar tiempo"
      4: "Withdraw con ZK proof"

  railgun:
    tipo: "Privacy system"
    tecnología: "zkSNARKs"
    características:
      - Balances privados
      - DeFi integrations
      - Viewing keys

  secret_network:
    tipo: "Privacy L1"
    tecnología: "TEE (Trusted Execution Environment)"
    características:
      - Secret contracts
      - Encrypted inputs/outputs
      - Cosmos SDK based

  oasis_network:
    tipo: "Privacy L1"
    tecnología: "TEE + ZK"
    características:
      - Confidential smart contracts
      - ParaTimes (parallel runtimes)

  mina_protocol:
    tipo: "Succinct blockchain"
    tecnología: "Recursive zkSNARKs"
    características:
      - Blockchain de 22KB constante
      - zkApps (smart contracts)
      - Off-chain execution
```

---

## 5. CIRCUITOS ZK - DESARROLLO

### 5.1 Circom (zkSNARKs)

```circom
// Circom - DSL para circuitos ZK
pragma circom 2.0.0;

// Multiplicador simple
template Multiplier(n) {
    signal input a;
    signal input b;
    signal output c;

    // Constraints
    c <== a * b;

    // Assertions
    assert(a < 2**n);
    assert(b < 2**n);
}

// Merkle Tree Proof
template MerkleTreeChecker(levels) {
    signal input leaf;
    signal input root;
    signal input pathElements[levels];
    signal input pathIndices[levels];

    component hashers[levels];
    signal hashes[levels + 1];
    hashes[0] <== leaf;

    for (var i = 0; i < levels; i++) {
        hashers[i] = HashLeftRight();

        // Si pathIndices[i] == 0, leaf está a la izquierda
        hashers[i].left <== pathIndices[i] * (pathElements[i] - hashes[i]) + hashes[i];
        hashers[i].right <== (1 - pathIndices[i]) * (pathElements[i] - hashes[i]) + hashes[i];

        hashes[i + 1] <== hashers[i].hash;
    }

    root === hashes[levels];
}

// Hash component
template HashLeftRight() {
    signal input left;
    signal input right;
    signal output hash;

    component poseidon = Poseidon(2);
    poseidon.inputs[0] <== left;
    poseidon.inputs[1] <== right;
    hash <== poseidon.out;
}

component main {public [root]} = MerkleTreeChecker(20);
```

```bash
# Compilar circuito Circom
circom merkle.circom --r1cs --wasm --sym

# Generar trusted setup (Powers of Tau)
snarkjs powersoftau new bn128 14 pot14_0.ptau
snarkjs powersoftau contribute pot14_0.ptau pot14_1.ptau

# Phase 2 (circuit-specific)
snarkjs groth16 setup merkle.r1cs pot14_final.ptau merkle.zkey

# Generar prueba
snarkjs groth16 prove merkle.zkey witness.wtns proof.json public.json

# Verificar
snarkjs groth16 verify verification_key.json public.json proof.json

# Generar verifier Solidity
snarkjs zkey export solidityverifier merkle.zkey verifier.sol
```

### 5.2 Halo2 (Rust)

```rust
// Halo2 - Framework de Zcash/Scroll
use halo2_proofs::{
    circuit::{Layouter, SimpleFloorPlanner, Value},
    plonk::{Advice, Circuit, Column, ConstraintSystem, Error, Selector},
    poly::Rotation,
};

#[derive(Clone)]
struct MyConfig {
    advice: [Column<Advice>; 2],
    selector: Selector,
}

struct MyCircuit {
    a: Value<F>,
    b: Value<F>,
}

impl<F: Field> Circuit<F> for MyCircuit {
    type Config = MyConfig;
    type FloorPlanner = SimpleFloorPlanner;

    fn configure(meta: &mut ConstraintSystem<F>) -> Self::Config {
        let advice = [meta.advice_column(), meta.advice_column()];
        let selector = meta.selector();

        meta.create_gate("multiply", |meta| {
            let s = meta.query_selector(selector);
            let a = meta.query_advice(advice[0], Rotation::cur());
            let b = meta.query_advice(advice[1], Rotation::cur());
            let c = meta.query_advice(advice[0], Rotation::next());

            vec![s * (a * b - c)]
        });

        MyConfig { advice, selector }
    }

    fn synthesize(
        &self,
        config: Self::Config,
        mut layouter: impl Layouter<F>,
    ) -> Result<(), Error> {
        layouter.assign_region(
            || "multiply",
            |mut region| {
                config.selector.enable(&mut region, 0)?;

                region.assign_advice(|| "a", config.advice[0], 0, || self.a)?;
                region.assign_advice(|| "b", config.advice[1], 0, || self.b)?;

                let c = self.a.and_then(|a| self.b.map(|b| a * b));
                region.assign_advice(|| "c", config.advice[0], 1, || c)?;

                Ok(())
            },
        )
    }
}
```

---

## 6. FIRMA

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  NEURONA: ZK_ROLLUPS & PRIVACY                                                 ║
║  ID: C20008                                                                    ║
║  Versión: 1.0.0                                                                ║
║  Última actualización: 2024-12-29                                              ║
║  Consciencia: CIPHER                                                           ║
║  ─────────────────────────────────────────────────────────────────────────     ║
║  "Zero Knowledge - La matemática que demuestra sin revelar"                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```
