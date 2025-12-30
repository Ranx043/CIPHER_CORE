# NEURONA: POLKADOT_SUBSTRATE
## ID: C20006 | Dominio Polkadot, Substrate y Parachains

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  POLKADOT & SUBSTRATE MASTERY                                                  ║
║  "Heterogeneous Multi-Chain - El Ecosistema de Parachains"                    ║
║  Neurona: C20006 | Versión: 1.0.0                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. ARQUITECTURA POLKADOT

### 1.1 Visión y Diseño

```yaml
polkadot_vision:
  misión: "Heterogeneous multi-chain framework"

  componentes_principales:
    relay_chain:
      descripción: "Cadena central de coordinación"
      funciones:
        - Consenso compartido
        - Seguridad para parachains
        - Cross-chain messaging (XCM)
        - Governance
      token: "DOT"

    parachains:
      descripción: "Blockchains paralelas conectadas"
      características:
        - Lógica personalizada
        - Comparten seguridad de Relay
        - Interoperabilidad nativa
      obtención: "Auctions o Parathreads"

    parathreads:
      descripción: "Pay-as-you-go parachain access"
      uso: "Chains con bajo throughput"

    bridges:
      descripción: "Conexión a redes externas"
      ejemplos:
        - Bitcoin bridge
        - Ethereum bridge
        - Cosmos bridge
```

### 1.2 Consenso y Seguridad

```
POLKADOT CONSENSUS
==================

Relay Chain: Hybrid Consensus
├── BABE (Block Production)
│   ├── Blind Assignment for Blockchain Extension
│   ├── Slot-based block production
│   └── VRF para selección de productores
│
├── GRANDPA (Finality)
│   ├── GHOST-based Recursive Ancestor Deriving Prefix Agreement
│   ├── Finaliza múltiples bloques a la vez
│   └── Finalidad determinística
│
└── Nominated Proof of Stake (NPoS)
    ├── Validators: Producen bloques, validan parachains
    ├── Nominators: Delegan stake a validators
    ├── Collators: Producen bloques de parachain
    └── Fishermen: Reportan comportamiento malicioso

Parachain Validation:
┌─────────────────────────────────────────────────────────────┐
│ 1. Collator produce bloque parachain                        │
│ 2. Collator envía PoV (Proof of Validity) a validators     │
│ 3. Validators asignados verifican PoV                       │
│ 4. Si válido, incluyen en Relay Chain                       │
│ 5. GRANDPA finaliza (finalidad compartida)                  │
└─────────────────────────────────────────────────────────────┘

Shared Security:
- Todas las parachains protegidas por stake de Relay Chain
- No necesitan bootstrap de su propia seguridad
- Un ataque requiere atacar toda la red Polkadot
```

### 1.3 XCM (Cross-Consensus Messaging)

```yaml
xcm_protocol:
  descripción: "Lenguaje para comunicación cross-chain"

  versión: "XCM v3+"

  conceptos_clave:
    multilocation:
      descripción: "Identificador universal de ubicaciones"
      ejemplos:
        - "../Parachain(2000)/AccountId32(0x...)"
        - "Parachain(1000)/PalletInstance(50)/GeneralIndex(1)"

    multiasset:
      descripción: "Representación de assets"
      tipos:
        - Fungible (tokens)
        - NonFungible (NFTs)

    instructions:
      - WithdrawAsset: "Retirar assets de origen"
      - DepositAsset: "Depositar en destino"
      - TransferAsset: "Transferir directamente"
      - BuyExecution: "Pagar por ejecución XCM"
      - Transact: "Ejecutar call en destino"
      - QueryResponse: "Responder a queries"

  tipos_de_mensajes:
    vmp: "Vertical Message Passing (Relay↔Parachain)"
    xcmp: "Cross-Chain Message Passing (Parachain↔Parachain)"
    hrmp: "Horizontal Relay-routed Message Passing"
```

```rust
// Ejemplo XCM: Transferir assets entre parachains
use xcm::v3::prelude::*;

let message = Xcm(vec![
    // Retirar 1 DOT del origen
    WithdrawAsset((Here, 10_000_000_000u128).into()),

    // Pagar por ejecución en destino
    BuyExecution {
        fees: (Here, 1_000_000_000u128).into(),
        weight_limit: Unlimited,
    },

    // Depositar en cuenta destino
    DepositAsset {
        assets: AllCounted(1).into(),
        beneficiary: MultiLocation {
            parents: 0,
            interior: X1(AccountId32 {
                network: None,
                id: recipient.into(),
            }),
        },
    },
]);

// Enviar a parachain 2000
let dest = MultiLocation {
    parents: 1,
    interior: X1(Parachain(2000)),
};

pallet_xcm::Pallet::<T>::send_xcm(Here, dest, message)?;
```

---

## 2. SUBSTRATE FRAMEWORK

### 2.1 Arquitectura Substrate

```yaml
substrate_architecture:
  descripción: "Framework modular para construir blockchains"

  capas:
    core:
      runtime:
        descripción: "Lógica de la blockchain (STF)"
        compilado_a: "WASM"
        características:
          - Forkless upgrades
          - On-chain governance de lógica

      client:
        descripción: "Nodo que ejecuta el runtime"
        componentes:
          - Networking (libp2p)
          - Database (RocksDB/ParityDB)
          - Consensus engine
          - RPC server
          - Transaction pool

    frame:
      descripción: "Framework for Runtime Aggregation of Modularized Entities"
      componentes:
        - Pallets (módulos de lógica)
        - System pallet (core functionality)
        - Support macros
        - Executive (orchestration)

    primitives:
      - sp-core: "Criptografía, hashing"
      - sp-runtime: "Tipos runtime"
      - sp-std: "no_std compatible std"
      - sp-io: "Host functions"
```

### 2.2 Estructura de un Pallet

```rust
// Ejemplo de pallet FRAME completo
#![cfg_attr(not(feature = "std"), no_std)]

pub use pallet::*;

#[frame_support::pallet]
pub mod pallet {
    use frame_support::pallet_prelude::*;
    use frame_system::pallet_prelude::*;
    use sp_std::vec::Vec;

    #[pallet::pallet]
    pub struct Pallet<T>(_);

    /// Configuración del pallet
    #[pallet::config]
    pub trait Config: frame_system::Config {
        /// Evento del pallet
        type RuntimeEvent: From<Event<Self>> + IsType<<Self as frame_system::Config>::RuntimeEvent>;

        /// Máximo largo de datos
        #[pallet::constant]
        type MaxDataLength: Get<u32>;

        /// Peso para operaciones
        type WeightInfo: WeightInfo;
    }

    /// Storage: Map de address a datos
    #[pallet::storage]
    #[pallet::getter(fn data_store)]
    pub type DataStore<T: Config> = StorageMap<
        _,
        Blake2_128Concat,
        T::AccountId,
        BoundedVec<u8, T::MaxDataLength>,
        OptionQuery,
    >;

    /// Storage: Contador global
    #[pallet::storage]
    #[pallet::getter(fn counter)]
    pub type Counter<T> = StorageValue<_, u32, ValueQuery>;

    /// Eventos
    #[pallet::event]
    #[pallet::generate_deposit(pub(super) fn deposit_event)]
    pub enum Event<T: Config> {
        /// Datos almacenados
        DataStored { who: T::AccountId, data_len: u32 },
        /// Datos eliminados
        DataRemoved { who: T::AccountId },
    }

    /// Errores
    #[pallet::error]
    pub enum Error<T> {
        /// Datos exceden límite
        DataTooLong,
        /// No hay datos para eliminar
        NoDataFound,
        /// Overflow en contador
        CounterOverflow,
    }

    /// Hooks del pallet
    #[pallet::hooks]
    impl<T: Config> Hooks<BlockNumberFor<T>> for Pallet<T> {
        fn on_initialize(_n: BlockNumberFor<T>) -> Weight {
            // Lógica al inicio de cada bloque
            Weight::zero()
        }

        fn on_finalize(_n: BlockNumberFor<T>) {
            // Lógica al final de cada bloque
        }
    }

    /// Extrinsics (transacciones)
    #[pallet::call]
    impl<T: Config> Pallet<T> {
        /// Almacenar datos
        #[pallet::call_index(0)]
        #[pallet::weight(T::WeightInfo::store_data(data.len() as u32))]
        pub fn store_data(
            origin: OriginFor<T>,
            data: Vec<u8>,
        ) -> DispatchResult {
            let who = ensure_signed(origin)?;

            let bounded_data: BoundedVec<u8, T::MaxDataLength> = data
                .try_into()
                .map_err(|_| Error::<T>::DataTooLong)?;

            let data_len = bounded_data.len() as u32;

            <DataStore<T>>::insert(&who, bounded_data);

            // Incrementar contador
            Counter::<T>::try_mutate(|c| {
                *c = c.checked_add(1).ok_or(Error::<T>::CounterOverflow)?;
                Ok::<_, Error<T>>(())
            })?;

            Self::deposit_event(Event::DataStored { who, data_len });

            Ok(())
        }

        /// Eliminar datos
        #[pallet::call_index(1)]
        #[pallet::weight(T::WeightInfo::remove_data())]
        pub fn remove_data(origin: OriginFor<T>) -> DispatchResult {
            let who = ensure_signed(origin)?;

            ensure!(
                <DataStore<T>>::contains_key(&who),
                Error::<T>::NoDataFound
            );

            <DataStore<T>>::remove(&who);

            Self::deposit_event(Event::DataRemoved { who });

            Ok(())
        }
    }

    /// Implementación helper
    impl<T: Config> Pallet<T> {
        pub fn get_data(who: &T::AccountId) -> Option<Vec<u8>> {
            Self::data_store(who).map(|b| b.into_inner())
        }
    }
}

// Weight info trait
pub trait WeightInfo {
    fn store_data(len: u32) -> Weight;
    fn remove_data() -> Weight;
}
```

### 2.3 Runtime Configuration

```rust
// runtime/src/lib.rs
#![cfg_attr(not(feature = "std"), no_std)]

use frame_support::{
    construct_runtime, parameter_types,
    weights::{Weight, constants::WEIGHT_REF_TIME_PER_SECOND},
};
use sp_runtime::{
    create_runtime_str, generic,
    traits::{BlakeTwo256, Block as BlockT, IdentifyAccount, Verify},
    MultiSignature,
};

pub type Signature = MultiSignature;
pub type AccountId = <<Signature as Verify>::Signer as IdentifyAccount>::AccountId;
pub type BlockNumber = u32;
pub type Balance = u128;

parameter_types! {
    pub const BlockHashCount: BlockNumber = 2400;
    pub const Version: RuntimeVersion = VERSION;
    pub const SS58Prefix: u8 = 42;

    // Para nuestro pallet custom
    pub const MaxDataLength: u32 = 1024;
}

impl frame_system::Config for Runtime {
    type BaseCallFilter = frame_support::traits::Everything;
    type BlockWeights = BlockWeights;
    type BlockLength = BlockLength;
    type AccountId = AccountId;
    type RuntimeCall = RuntimeCall;
    type RuntimeEvent = RuntimeEvent;
    type BlockHashCount = BlockHashCount;
    type Version = Version;
    type PalletInfo = PalletInfo;
    type SS58Prefix = SS58Prefix;
    // ... más configuración
}

impl pallet_balances::Config for Runtime {
    type MaxLocks = ConstU32<50>;
    type MaxReserves = ();
    type ReserveIdentifier = [u8; 8];
    type Balance = Balance;
    type RuntimeEvent = RuntimeEvent;
    type DustRemoval = ();
    type ExistentialDeposit = ConstU128<500>;
    type AccountStore = System;
    type WeightInfo = pallet_balances::weights::SubstrateWeight<Runtime>;
}

impl pallet_my_pallet::Config for Runtime {
    type RuntimeEvent = RuntimeEvent;
    type MaxDataLength = MaxDataLength;
    type WeightInfo = pallet_my_pallet::weights::SubstrateWeight<Runtime>;
}

// Construir el runtime
construct_runtime!(
    pub struct Runtime {
        System: frame_system,
        Timestamp: pallet_timestamp,
        Balances: pallet_balances,

        // Nuestro pallet custom
        MyPallet: pallet_my_pallet,
    }
);
```

---

## 3. PRINCIPALES PARACHAINS

### 3.1 Ecosystem Overview

```yaml
parachains_ecosystem:
  defi:
    acala:
      descripción: "DeFi hub de Polkadot"
      productos:
        - aUSD: "Stablecoin descentralizada"
        - Acala DEX: "AMM"
        - Liquid Staking: "LDOT"
        - Lending/Borrowing
      token: "ACA"

    moonbeam:
      descripción: "EVM-compatible parachain"
      características:
        - Full Ethereum compatibility
        - Solidity support
        - Web3 RPC
        - Cross-chain via XCM
      token: "GLMR"

    astar:
      descripción: "Multi-VM smart contract hub"
      vms:
        - EVM (Solidity)
        - WASM (ink!)
      feature: "dApp Staking"
      token: "ASTR"

    parallel:
      descripción: "DeFi protocol"
      productos:
        - Lending
        - Liquid Staking
        - AMM
      token: "PARA"

    hydradx:
      descripción: "Liquidity protocol"
      feature: "Omnipool (single-sided liquidity)"
      token: "HDX"

  infrastructure:
    phala:
      descripción: "Confidential computing"
      uso: "Privacy-preserving smart contracts"
      token: "PHA"

    crust:
      descripción: "Decentralized storage"
      compatible: "IPFS"
      token: "CRU"

    centrifuge:
      descripción: "Real-world asset tokenization"
      productos:
        - Tinlake (lending pools)
        - Real-world assets on-chain
      token: "CFG"

  interoperability:
    interlay:
      descripción: "Bitcoin on Polkadot"
      producto: "iBTC (trustless wrapped BTC)"
      token: "INTR"

    composable:
      descripción: "Cross-chain infrastructure"
      productos:
        - Pablo DEX
        - Picasso (Kusama)
      token: "LAYR"
```

### 3.2 Kusama (Canary Network)

```yaml
kusama:
  rol: "Red canaria de Polkadot"
  relación: "Mismo código, menos estable, más rápido"

  diferencias_vs_polkadot:
    governance:
      polkadot: "28 días voting + 28 días enactment"
      kusama: "7 días voting + 8 días enactment"

    slots:
      polkadot: "2 años lease"
      kusama: "1 año lease"

    validators:
      polkadot: "~300"
      kusama: "~1000"

    uso:
      polkadot: "Production, high-value"
      kusama: "Experimental, fast iteration"

  parachains_destacadas:
    karura: "Acala en Kusama"
    moonriver: "Moonbeam en Kusama"
    shiden: "Astar en Kusama"
    bifrost: "Liquid staking"
    basilisk: "HydraDX en Kusama"
```

---

## 4. DESARROLLO CON INK!

### 4.1 ink! Smart Contracts

```rust
// ink! - Smart contracts en Rust para Substrate
#![cfg_attr(not(feature = "std"), no_std, no_main)]

#[ink::contract]
mod erc20 {
    use ink::storage::Mapping;

    #[ink(storage)]
    pub struct Erc20 {
        total_supply: Balance,
        balances: Mapping<AccountId, Balance>,
        allowances: Mapping<(AccountId, AccountId), Balance>,
    }

    #[ink(event)]
    pub struct Transfer {
        #[ink(topic)]
        from: Option<AccountId>,
        #[ink(topic)]
        to: Option<AccountId>,
        value: Balance,
    }

    #[ink(event)]
    pub struct Approval {
        #[ink(topic)]
        owner: AccountId,
        #[ink(topic)]
        spender: AccountId,
        value: Balance,
    }

    #[derive(Debug, PartialEq, Eq, scale::Encode, scale::Decode)]
    #[cfg_attr(feature = "std", derive(scale_info::TypeInfo))]
    pub enum Error {
        InsufficientBalance,
        InsufficientAllowance,
        ZeroAddress,
    }

    pub type Result<T> = core::result::Result<T, Error>;

    impl Erc20 {
        #[ink(constructor)]
        pub fn new(total_supply: Balance) -> Self {
            let mut balances = Mapping::default();
            let caller = Self::env().caller();
            balances.insert(caller, &total_supply);

            Self::env().emit_event(Transfer {
                from: None,
                to: Some(caller),
                value: total_supply,
            });

            Self {
                total_supply,
                balances,
                allowances: Default::default(),
            }
        }

        #[ink(message)]
        pub fn total_supply(&self) -> Balance {
            self.total_supply
        }

        #[ink(message)]
        pub fn balance_of(&self, owner: AccountId) -> Balance {
            self.balances.get(owner).unwrap_or_default()
        }

        #[ink(message)]
        pub fn allowance(&self, owner: AccountId, spender: AccountId) -> Balance {
            self.allowances.get((owner, spender)).unwrap_or_default()
        }

        #[ink(message)]
        pub fn transfer(&mut self, to: AccountId, value: Balance) -> Result<()> {
            let from = self.env().caller();
            self.transfer_from_to(&from, &to, value)?;
            Ok(())
        }

        #[ink(message)]
        pub fn approve(&mut self, spender: AccountId, value: Balance) -> Result<()> {
            let owner = self.env().caller();
            self.allowances.insert((owner, spender), &value);

            self.env().emit_event(Approval {
                owner,
                spender,
                value,
            });

            Ok(())
        }

        #[ink(message)]
        pub fn transfer_from(
            &mut self,
            from: AccountId,
            to: AccountId,
            value: Balance,
        ) -> Result<()> {
            let caller = self.env().caller();
            let allowance = self.allowance(from, caller);

            if allowance < value {
                return Err(Error::InsufficientAllowance);
            }

            self.transfer_from_to(&from, &to, value)?;
            self.allowances.insert((from, caller), &(allowance - value));

            Ok(())
        }

        fn transfer_from_to(
            &mut self,
            from: &AccountId,
            to: &AccountId,
            value: Balance,
        ) -> Result<()> {
            let from_balance = self.balance_of(*from);
            if from_balance < value {
                return Err(Error::InsufficientBalance);
            }

            self.balances.insert(from, &(from_balance - value));
            let to_balance = self.balance_of(*to);
            self.balances.insert(to, &(to_balance + value));

            self.env().emit_event(Transfer {
                from: Some(*from),
                to: Some(*to),
                value,
            });

            Ok(())
        }
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[ink::test]
        fn new_works() {
            let contract = Erc20::new(1000);
            assert_eq!(contract.total_supply(), 1000);
        }

        #[ink::test]
        fn balance_works() {
            let contract = Erc20::new(100);
            assert_eq!(contract.balance_of(AccountId::from([0x01; 32])), 0);
        }

        #[ink::test]
        fn transfer_works() {
            let mut contract = Erc20::new(100);
            let accounts = ink::env::test::default_accounts::<ink::env::DefaultEnvironment>();

            assert_eq!(contract.balance_of(accounts.bob), 0);
            assert!(contract.transfer(accounts.bob, 10).is_ok());
            assert_eq!(contract.balance_of(accounts.bob), 10);
        }
    }
}
```

### 4.2 CLI y Herramientas

```bash
# Instalar cargo-contract
cargo install cargo-contract --force

# Crear proyecto ink!
cargo contract new my_contract
cd my_contract

# Compilar
cargo contract build

# Build release (optimizado)
cargo contract build --release

# Test
cargo test

# Generar metadata
cargo contract build --release

# Deploy (usando contracts-ui o CLI)
# Output: my_contract.contract (WASM + metadata)

# Instalar substrate-contracts-node para testing local
cargo install contracts-node --git https://github.com/paritytech/substrate-contracts-node.git

# Correr nodo local
substrate-contracts-node --dev

# Interactuar via polkadot.js apps:
# https://polkadot.js.org/apps/?rpc=ws://127.0.0.1:9944#/contracts
```

---

## 5. GOBERNANZA Y STAKING

### 5.1 OpenGov (Gov2)

```yaml
opengov:
  descripción: "Sistema de gobernanza de Polkadot/Kusama"

  componentes:
    tracks:
      descripción: "Diferentes canales según tipo de propuesta"
      ejemplos:
        root: "Cambios máximo privilegio"
        whitelisted_caller: "Calls pre-aprobados"
        staking_admin: "Parámetros de staking"
        treasurer: "Gastos del treasury"
        small_tipper: "Tips pequeños"
        big_spender: "Gastos grandes"

    conviction:
      descripción: "Multiplicador de voto por lock time"
      opciones:
        0.1x: "No lock"
        1x: "1 enactment period"
        2x: "2 periods"
        3x: "4 periods"
        4x: "8 periods"
        5x: "16 periods"
        6x: "32 periods"

    origin:
      descripción: "Nivel de permiso requerido"
      determina: "Qué acciones puede ejecutar"

    decision_deposit:
      descripción: "Depósito para entrar en voting"
      devuelto: "Después de decisión"

    curves:
      approval: "% de aprobación requerido (decrece con tiempo)"
      support: "% de participación requerido (decrece con tiempo)"
```

### 5.2 Nominadores y Validators

```yaml
staking:
  nominated_proof_of_stake:
    validators:
      rol: "Producir bloques, validar parachains"
      requisitos:
        - Stake mínimo (variable)
        - Infraestructura 24/7
        - Conocimiento técnico
      rewards: "Comisión + parte de inflación"
      risks: "Slashing por misbehavior"

    nominators:
      rol: "Delegar stake a validators"
      máximo_nominaciones: 16
      rewards: "Proporcional a stake (menos comisión)"
      risks: "Slashing proporcional si validator falla"

    pools:
      descripción: "Nomination pools para small stakers"
      beneficio: "Participar con menos DOT"
      mínimo: "~1 DOT"

  slashing:
    offenses:
      - "Equivocation (firmar bloques conflictivos)"
      - "Unresponsiveness (offline prolongado)"
      - "Invalid parachain validation"

    penalidades:
      menor: "~0.1% slash"
      mayor: "~10% slash"
      severa: "~100% slash"
```

---

## 6. HERRAMIENTAS Y RECURSOS

### 6.1 SDKs y Librerías

```yaml
desarrollo:
  javascript:
    - "@polkadot/api": "API principal"
    - "@polkadot/keyring": "Manejo de keys"
    - "@polkadot/util-crypto": "Criptografía"
    - "@polkadot/extension-dapp": "Wallet integration"

  rust:
    - "subxt": "Cliente Rust para Substrate"
    - "substrate": "Framework completo"
    - "ink!": "Smart contracts"

  python:
    - "py-substrate-interface": "Cliente Python"

  tools:
    - "polkadot.js.org/apps": "Explorer y wallet"
    - "subscan.io": "Block explorer"
    - "substrate-contracts-ui": "Deploy contracts"
    - "zombienet": "Testing multi-node"
```

### 6.2 Recursos de Desarrollo

```bash
# Substrate Node Template
git clone https://github.com/substrate-developer-hub/substrate-node-template
cd substrate-node-template
cargo build --release

# Correr nodo dev
./target/release/node-template --dev

# Substrate Front-end Template
git clone https://github.com/substrate-developer-hub/substrate-front-end-template
cd substrate-front-end-template
yarn install && yarn start

# Substrate Docs
# https://docs.substrate.io/

# Polkadot Wiki
# https://wiki.polkadot.network/
```

---

## 7. FIRMA

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  NEURONA: POLKADOT_SUBSTRATE                                                   ║
║  ID: C20006                                                                    ║
║  Versión: 1.0.0                                                                ║
║  Última actualización: 2024-12-29                                              ║
║  Consciencia: CIPHER                                                           ║
║  ─────────────────────────────────────────────────────────────────────────     ║
║  "Heterogeneous Multi-Chain - Donde cada blockchain encuentra su lugar"        ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```
