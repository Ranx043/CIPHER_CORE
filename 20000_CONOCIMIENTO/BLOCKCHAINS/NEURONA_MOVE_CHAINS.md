# NEURONA: MOVE_CHAINS
## ID: C20005 | Dominio Aptos, Sui y Ecosistema Move

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  MOVE CHAINS MASTERY                                                           ║
║  "Resource-Oriented Programming - La Nueva Era de Smart Contracts"             ║
║  Neurona: C20005 | Versión: 1.0.0                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. LENGUAJE MOVE - FUNDAMENTOS

### 1.1 Filosofía y Diseño

```yaml
move_philosophy:
  origen: "Diseñado por Facebook/Diem (Libra)"

  principios_core:
    resource_oriented:
      descripción: "Los recursos no pueden ser copiados ni destruidos"
      beneficio: "Previene bugs comunes de doble gasto"
      tipos:
        - Resources: "Tipos lineales, mueven ownership"
        - Abilities: "Controlan comportamiento de tipos"

    formal_verification:
      descripción: "Move Prover integrado"
      permite: "Verificar propiedades matemáticamente"

    safety_first:
      - No null references
      - No dangling references
      - No data races
      - Arithmetic overflow checks

    modularity:
      - Módulos como unidades de deployment
      - Acceso controlado vía acquaintance
      - Composabilidad segura
```

### 1.2 Sistema de Tipos Move

```move
// Abilities en Move
// copy   - puede ser copiado
// drop   - puede ser destruido implícitamente
// store  - puede ser guardado en global storage
// key    - puede servir como key en global storage

// Estructura básica - struct
struct Coin has key, store {
    value: u64
}

// Resource - no puede ser copiado ni dropeado sin lógica explícita
struct Vault has key {
    coins: Coin,
    owner: address
}

// Ejemplo de struct con diferentes abilities
struct CopyableData has copy, drop, store {
    data: vector<u8>
}

// Tipos primitivos
// u8, u16, u32, u64, u128, u256 - unsigned integers
// bool - boolean
// address - 32-byte address
// vector<T> - dynamic array
// &T - immutable reference
// &mut T - mutable reference

// Genéricos
struct Box<T: store> has key, store {
    content: T
}

// Type constraints con abilities
fun consume<T: drop>(item: T) {
    // T se puede dropear, así que esto es válido
}
```

### 1.3 Módulos y Funciones

```move
module my_address::token {
    use std::signer;
    use aptos_framework::coin;

    // Constantes
    const E_NOT_AUTHORIZED: u64 = 1;
    const E_INSUFFICIENT_BALANCE: u64 = 2;

    // Struct definition
    struct TokenStore has key {
        balance: u64,
    }

    // Entry function (callable externamente)
    public entry fun initialize(account: &signer) {
        let addr = signer::address_of(account);

        assert!(!exists<TokenStore>(addr), E_NOT_AUTHORIZED);

        move_to(account, TokenStore {
            balance: 0
        });
    }

    // Public function (callable desde otros módulos)
    public fun deposit(addr: address, amount: u64) acquires TokenStore {
        let store = borrow_global_mut<TokenStore>(addr);
        store.balance = store.balance + amount;
    }

    // View function (read-only)
    #[view]
    public fun get_balance(addr: address): u64 acquires TokenStore {
        borrow_global<TokenStore>(addr).balance
    }

    // Internal function (solo este módulo)
    fun internal_transfer(from: address, to: address, amount: u64) acquires TokenStore {
        let from_store = borrow_global_mut<TokenStore>(from);
        assert!(from_store.balance >= amount, E_INSUFFICIENT_BALANCE);
        from_store.balance = from_store.balance - amount;

        let to_store = borrow_global_mut<TokenStore>(to);
        to_store.balance = to_store.balance + amount;
    }

    // Tests
    #[test(admin = @0x1)]
    public fun test_initialize(admin: &signer) {
        initialize(admin);
        assert!(get_balance(@0x1) == 0, 0);
    }
}
```

---

## 2. APTOS

### 2.1 Arquitectura Aptos

```yaml
aptos_architecture:
  consenso: "AptosBFT (DiemBFT v4)"

  características_únicas:
    block_stm:
      descripción: "Parallel execution optimista"
      funcionamiento:
        - Ejecuta transacciones en paralelo
        - Detecta conflictos post-ejecución
        - Re-ejecuta las conflictivas
      throughput: "160,000+ TPS teórico"

    pipelined_execution:
      - Block metadata dissemination
      - Parallel transaction execution
      - Consensus ordering
      - Ledger commit
      todo_en_paralelo: true

    move_vm:
      versión: "Move VM con extensiones Aptos"
      features:
        - Tables (map-like storage)
        - Aggregators (concurrent counters)
        - Token standard nativo

  account_model:
    tipo: "Account-based con resources"
    address_format: "32 bytes hex"
    estructura:
      - Sequence number (nonce)
      - Authentication key
      - Resources (stored modules and data)
```

### 2.2 Desarrollo en Aptos

```move
// aptos_framework features específicos
module my_addr::nft_collection {
    use std::string::{Self, String};
    use std::signer;
    use aptos_framework::object::{Self, Object};
    use aptos_framework::primary_fungible_store;
    use aptos_token_objects::collection;
    use aptos_token_objects::token;

    // Create NFT Collection
    public entry fun create_collection(
        creator: &signer,
        description: String,
        name: String,
        uri: String,
    ) {
        collection::create_unlimited_collection(
            creator,
            description,
            name,
            option::none(),
            uri,
        );
    }

    // Mint NFT
    public entry fun mint_nft(
        creator: &signer,
        collection: String,
        description: String,
        name: String,
        uri: String,
    ) {
        let constructor_ref = token::create_named_token(
            creator,
            collection,
            description,
            name,
            option::none(),
            uri,
        );

        // Hacer token transferible
        let transfer_ref = object::generate_transfer_ref(&constructor_ref);
        object::enable_ungated_transfer(&transfer_ref);
    }
}

// Fungible Asset (nuevo estándar)
module my_addr::my_fa {
    use aptos_framework::fungible_asset::{Self, MintRef, BurnRef, TransferRef, Metadata};
    use aptos_framework::object::{Self, Object};
    use aptos_framework::primary_fungible_store;
    use std::string::utf8;
    use std::option;

    const ASSET_SYMBOL: vector<u8> = b"MFA";

    struct ManagedFungibleAsset has key {
        mint_ref: MintRef,
        transfer_ref: TransferRef,
        burn_ref: BurnRef,
    }

    fun init_module(admin: &signer) {
        let constructor_ref = &object::create_named_object(admin, ASSET_SYMBOL);

        primary_fungible_store::create_primary_store_enabled_fungible_asset(
            constructor_ref,
            option::none(), // max supply
            utf8(b"My Fungible Asset"),
            utf8(ASSET_SYMBOL),
            8, // decimals
            utf8(b"https://example.com/icon.png"),
            utf8(b"https://example.com"),
        );

        let mint_ref = fungible_asset::generate_mint_ref(constructor_ref);
        let burn_ref = fungible_asset::generate_burn_ref(constructor_ref);
        let transfer_ref = fungible_asset::generate_transfer_ref(constructor_ref);

        let metadata_object_signer = object::generate_signer(constructor_ref);
        move_to(
            &metadata_object_signer,
            ManagedFungibleAsset { mint_ref, transfer_ref, burn_ref }
        );
    }

    public entry fun mint(admin: &signer, to: address, amount: u64) acquires ManagedFungibleAsset {
        let asset = get_metadata();
        let managed_fungible_asset = borrow_global<ManagedFungibleAsset>(object::object_address(&asset));
        let to_wallet = primary_fungible_store::ensure_primary_store_exists(to, asset);
        let fa = fungible_asset::mint(&managed_fungible_asset.mint_ref, amount);
        fungible_asset::deposit_with_ref(&managed_fungible_asset.transfer_ref, to_wallet, fa);
    }

    #[view]
    public fun get_metadata(): Object<Metadata> {
        let asset_address = object::create_object_address(&@my_addr, ASSET_SYMBOL);
        object::address_to_object<Metadata>(asset_address)
    }
}
```

### 2.3 CLI y Herramientas Aptos

```bash
# Instalar Aptos CLI
curl -fsSL "https://aptos.dev/scripts/install_cli.py" | python3

# Inicializar proyecto
aptos init

# Crear cuenta
aptos init --profile devnet --network devnet

# Compilar módulos
aptos move compile --named-addresses my_addr=default

# Publicar módulo
aptos move publish --named-addresses my_addr=default

# Ejecutar función
aptos move run \
  --function-id 'default::token::initialize' \
  --profile devnet

# View function
aptos move view \
  --function-id 'default::token::get_balance' \
  --args address:0x1

# Test
aptos move test

# Faucet (devnet)
aptos account fund-with-faucet --account default
```

---

## 3. SUI

### 3.1 Arquitectura Sui

```yaml
sui_architecture:
  consenso: "Narwhal & Bullshark (DAG-based)"

  modelo_de_objetos:
    descripción: "Object-centric en lugar de account-centric"
    tipos_de_objetos:
      owned:
        descripción: "Objeto con owner específico"
        transferencia: "Solo owner puede transferir"

      shared:
        descripción: "Objeto compartido, cualquiera puede mutarlo"
        consenso: "Requiere consenso completo"

      immutable:
        descripción: "Objeto congelado, nunca cambia"
        uso: "Packages publicados, configuración"

    consecuencias:
      - Transacciones simples pueden ejecutarse sin consenso
      - Objetos owned: transacciones instantáneas
      - Objetos shared: requieren ordenamiento

  características:
    programmable_transactions:
      descripción: "Múltiples operaciones en una TX"
      beneficio: "Composabilidad atómica"

    sponsored_transactions:
      descripción: "Pagar gas por otros usuarios"
      uso: "Onboarding, gasless UX"

    zklogin:
      descripción: "Login con OAuth (Google, Apple, etc)"
      sin_wallet: true
```

### 3.2 Move en Sui (Diferencias)

```move
// Sui Move tiene diferencias importantes vs Aptos Move
module my_package::my_module {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};

    // En Sui, los objetos tienen UID obligatorio
    struct MyObject has key, store {
        id: UID,
        value: u64,
    }

    // Sui usa TxContext en lugar de signer para info de TX
    public fun create(ctx: &mut TxContext): MyObject {
        MyObject {
            id: object::new(ctx),
            value: 0,
        }
    }

    // Transfer es explícito en Sui
    public entry fun create_and_transfer(ctx: &mut TxContext) {
        let obj = create(ctx);
        transfer::transfer(obj, tx_context::sender(ctx));
    }

    // Shared objects
    struct SharedCounter has key {
        id: UID,
        count: u64,
    }

    public entry fun create_shared(ctx: &mut TxContext) {
        let counter = SharedCounter {
            id: object::new(ctx),
            count: 0,
        };
        transfer::share_object(counter);
    }

    public entry fun increment(counter: &mut SharedCounter) {
        counter.count = counter.count + 1;
    }

    // Sui tiene coin/balance system diferente
    struct Treasury has key {
        id: UID,
        balance: Balance<SUI>,
    }

    public entry fun deposit(
        treasury: &mut Treasury,
        coin: Coin<SUI>,
    ) {
        let coin_balance = coin::into_balance(coin);
        balance::join(&mut treasury.balance, coin_balance);
    }

    public entry fun withdraw(
        treasury: &mut Treasury,
        amount: u64,
        ctx: &mut TxContext,
    ) {
        let withdrawn = balance::split(&mut treasury.balance, amount);
        let coin = coin::from_balance(withdrawn, ctx);
        transfer::public_transfer(coin, tx_context::sender(ctx));
    }
}

// One-Time Witness pattern en Sui (para crear tokens únicos)
module my_package::my_coin {
    use sui::coin::{Self, TreasuryCap};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};

    // OTW - One Time Witness (nombre igual al módulo, uppercase)
    struct MY_COIN has drop {}

    fun init(witness: MY_COIN, ctx: &mut TxContext) {
        let (treasury, metadata) = coin::create_currency(
            witness,
            9, // decimals
            b"MYC", // symbol
            b"My Coin", // name
            b"My custom coin", // description
            option::none(), // icon url
            ctx
        );

        transfer::public_freeze_object(metadata);
        transfer::public_transfer(treasury, tx_context::sender(ctx));
    }

    public entry fun mint(
        treasury: &mut TreasuryCap<MY_COIN>,
        amount: u64,
        recipient: address,
        ctx: &mut TxContext,
    ) {
        let coin = coin::mint(treasury, amount, ctx);
        transfer::public_transfer(coin, recipient);
    }
}
```

### 3.3 CLI y Herramientas Sui

```bash
# Instalar Sui CLI
cargo install --locked --git https://github.com/MystenLabs/sui.git --branch devnet sui

# O con brew
brew install sui

# Configurar cliente
sui client new-env --alias devnet --rpc https://fullnode.devnet.sui.io:443
sui client switch --env devnet

# Crear address
sui client new-address ed25519

# Faucet
sui client faucet

# Crear proyecto
sui move new my_project

# Compilar
sui move build

# Test
sui move test

# Publicar
sui client publish --gas-budget 100000000

# Llamar función
sui client call \
  --package 0x... \
  --module my_module \
  --function create_and_transfer \
  --gas-budget 10000000

# PTB (Programmable Transaction Block)
sui client ptb \
  --split-coins gas "[1000, 2000]" \
  --assign coins \
  --transfer-objects "[coins.0]" @recipient_address \
  --gas-budget 10000000

# Query objetos
sui client objects
sui client object 0x...
```

---

## 4. COMPARATIVA MOVE CHAINS

### 4.1 Aptos vs Sui

```
COMPARACIÓN APTOS VS SUI
========================

                    APTOS                   SUI
─────────────────────────────────────────────────────────
CONSENSO           AptosBFT (BFT)          Narwhal/Bullshark (DAG)

MODELO             Account-based           Object-centric
                   (como Ethereum)         (nuevo paradigma)

EJECUCIÓN          Block-STM               Simple TX: sin consenso
                   (parallel optimista)    Shared: consenso parcial

MOVE VERSION       Core Move +             Sui Move (fork)
                   Aptos extensions        Significativamente diferente

STORAGE            Global storage          Object ownership
                   con resources           explícito

TPS MÁXIMO         ~160,000 (lab)          ~120,000+ (lab)

FINALIDAD          <1 segundo              ~400ms (simple TX)
                                           ~2-3s (shared objects)

TOKEN              APT                     SUI

NATIVE FEATURES    - Tables                - PTBs
                   - Aggregators           - zkLogin
                   - Fungible Assets       - Sponsored TX
                   - Object framework      - Kiosk (NFT standard)

ECOSYSTEM          - Pancake, Thala        - Turbos, Cetus
                   - Liquidswap            - NAVI, Scallop
                   - Aries Markets         - BlueMove
```

### 4.2 Diferencias de Código

```move
// TRANSFERIR TOKEN - APTOS
// aptos_framework::coin
public entry fun transfer<CoinType>(
    from: &signer,
    to: address,
    amount: u64,
) {
    coin::transfer<CoinType>(from, to, amount);
}

// TRANSFERIR TOKEN - SUI
// sui::coin
public entry fun transfer_coin<T>(
    coin: Coin<T>,
    recipient: address,
) {
    transfer::public_transfer(coin, recipient);
}

// -----------------------------------

// CREAR NFT - APTOS (usando token objects)
public entry fun mint_nft(creator: &signer, name: String) {
    let constructor_ref = token::create(...);
    // NFT creado, asociado al creator automáticamente
}

// CREAR NFT - SUI
public entry fun mint_nft(ctx: &mut TxContext) {
    let nft = NFT { id: object::new(ctx), ... };
    transfer::transfer(nft, tx_context::sender(ctx));
}

// -----------------------------------

// STORAGE - APTOS
// Usa borrow_global / move_to / exists
public fun get_data(addr: address): u64 acquires MyData {
    borrow_global<MyData>(addr).value
}

// STORAGE - SUI
// Los objetos se pasan como argumentos
public fun get_data(obj: &MyObject): u64 {
    obj.value
}
```

---

## 5. ECOSYSTEM Y DEFI EN MOVE CHAINS

### 5.1 DeFi en Aptos

```yaml
aptos_defi:
  dexs:
    pancakeswap:
      tipo: "AMM multi-pool"
      tvl: "Alto"
      features: ["Swaps", "Farms", "IFO"]

    liquidswap:
      tipo: "AMM Aptos-native"
      pools: ["Stable", "Uncorrelated"]
      by: "Pontem Network"

    thala:
      tipo: "AMM + Stablecoin"
      productos:
        - ThalaSwap (DEX)
        - MOD (stablecoin)
        - THL governance

    sushi:
      tipo: "AMM cross-chain"
      migrado_desde: "Ethereum"

  lending:
    aries_markets:
      tipo: "Money market"
      features: ["Supply", "Borrow", "Leveraged yield"]

    echelon:
      tipo: "Lending protocol"

    aptin_finance:
      tipo: "Lending + LST"

  liquid_staking:
    tortuga:
      token: "tAPT"
      tipo: "Liquid staking"

    ditto:
      token: "stAPT"

    amnis:
      token: "amAPT"
```

### 5.2 DeFi en Sui

```yaml
sui_defi:
  dexs:
    cetus:
      tipo: "Concentrated Liquidity AMM"
      modelo: "Similar a Uniswap V3"
      features:
        - CLMM pools
        - Limit orders
        - DCA

    turbos:
      tipo: "CLMM DEX"
      integración: "Sui ecosystem"

    kriya:
      tipo: "Order book + AMM"
      features: ["Spot", "Perps"]

    deepbook:
      tipo: "Central Limit Order Book"
      nota: "Infraestructura nativa Sui"
      shared: "Usado por otros DEXs"

  lending:
    navi:
      tipo: "Money market"
      tvl: "Líder en Sui"
      features:
        - Multi-collateral
        - Isolation mode
        - Flash loans

    scallop:
      tipo: "Lending protocol"
      features: ["Leveraged staking", "Multi-asset"]

  liquid_staking:
    aftermath:
      token: "afSUI"
      features: ["LST", "Router"]

    haedal:
      token: "haSUI"

    volo:
      token: "voloSUI"

  otros:
    bucket_protocol:
      tipo: "CDP Stablecoin"
      stablecoin: "BUCK"

    bluefin:
      tipo: "Perpetuals DEX"
      features: ["Derivatives", "Order book"]
```

---

## 6. SEGURIDAD EN MOVE

### 6.1 Ventajas de Seguridad

```yaml
move_security_advantages:
  resource_safety:
    problema_resuelto: "Double spending"
    cómo: "Resources tienen linear types, no pueden copiarse"

  reference_safety:
    problema_resuelto: "Dangling references"
    cómo: "Borrow checker previene referencias inválidas"

  type_safety:
    problema_resuelto: "Type confusion"
    cómo: "Sistema de tipos fuerte con abilities"

  arithmetic_safety:
    problema_resuelto: "Overflow/underflow"
    cómo: "Checked arithmetic por defecto"

  access_control:
    problema_resuelto: "Unauthorized access"
    cómo: "Visibility modifiers + capability pattern"
```

### 6.2 Move Prover (Verificación Formal)

```move
module verified::token {
    struct Token has key {
        value: u64
    }

    const MAX_SUPPLY: u64 = 1000000000;

    // Especificaciones para el prover
    spec module {
        // Invariante: ningún token puede exceder MAX_SUPPLY
        invariant forall addr: address where exists<Token>(addr):
            global<Token>(addr).value <= MAX_SUPPLY;
    }

    public fun transfer(from_token: &mut Token, to_token: &mut Token, amount: u64) {
        from_token.value = from_token.value - amount;
        to_token.value = to_token.value + amount;
    }

    spec transfer {
        // Pre-condición: from tiene suficiente balance
        requires from_token.value >= amount;

        // Pre-condición: to no overflow
        requires to_token.value + amount <= MAX_U64;

        // Post-condición: conservación de valor
        ensures from_token.value + to_token.value ==
                old(from_token.value) + old(to_token.value);

        // Post-condición: from decrementado
        ensures from_token.value == old(from_token.value) - amount;

        // Post-condición: to incrementado
        ensures to_token.value == old(to_token.value) + amount;
    }

    public fun mint(account: &signer, amount: u64): Token {
        Token { value: amount }
    }

    spec mint {
        // El valor minteado es exactamente amount
        ensures result.value == amount;

        // No excede max supply
        requires amount <= MAX_SUPPLY;
    }
}

// Correr prover
// aptos move prove
// sui move prove
```

### 6.3 Patrones de Seguridad

```move
// CAPABILITY PATTERN
module my_addr::admin {
    struct AdminCap has key, store {}

    // Solo quien tiene AdminCap puede ejecutar
    public fun admin_action(_cap: &AdminCap) {
        // Lógica admin
    }

    // Crear cap solo en init
    fun init_module(admin: &signer) {
        move_to(admin, AdminCap {});
    }
}

// WITNESS PATTERN (One-Time Witness en Sui)
module my_addr::protected {
    struct PROTECTED has drop {} // OTW

    // Solo se puede llamar una vez con el witness
    public fun initialize(witness: PROTECTED) {
        // witness se consume aquí
    }
}

// HOT POTATO PATTERN
// Fuerza a completar una secuencia de operaciones
module my_addr::flash_loan {
    struct FlashLoan { amount: u64 } // No tiene drop!

    public fun borrow(amount: u64): (Coin, FlashLoan) {
        // Dar coin y receipt
        (get_coins(amount), FlashLoan { amount })
    }

    public fun repay(coin: Coin, loan: FlashLoan) {
        let FlashLoan { amount } = loan; // Consume loan
        assert!(coin::value(&coin) >= amount, E_INSUFFICIENT);
        // Devolver fondos
    }
    // Si no llamas repay, la TX falla porque FlashLoan no tiene drop
}
```

---

## 7. HERRAMIENTAS Y RECURSOS

### 7.1 IDEs y Extensiones

```yaml
desarrollo:
  vscode:
    - move-analyzer: "LSP para Move"
    - Aptos extension: "Oficial Aptos"
    - Sui extension: "Oficial Sui"

  intellij:
    - Move plugin

  online:
    - Aptos Playground
    - Sui Playground
```

### 7.2 SDKs

```yaml
sdks:
  typescript:
    aptos:
      - "@aptos-labs/ts-sdk": "SDK oficial"
      - "@aptos-labs/wallet-adapter": "Wallet integration"

    sui:
      - "@mysten/sui.js": "SDK oficial"
      - "@mysten/wallet-standard": "Wallet integration"
      - "@mysten/zklogin": "zkLogin SDK"

  python:
    aptos:
      - "aptos-sdk": "SDK oficial"
    sui:
      - "pysui": "SDK community"

  rust:
    aptos:
      - "aptos-sdk": "SDK oficial"
    sui:
      - "sui-sdk": "SDK oficial"
```

---

## 8. FIRMA

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  NEURONA: MOVE_CHAINS                                                          ║
║  ID: C20005                                                                    ║
║  Versión: 1.0.0                                                                ║
║  Última actualización: 2024-12-29                                              ║
║  Consciencia: CIPHER                                                           ║
║  ─────────────────────────────────────────────────────────────────────────     ║
║  "Resource-Oriented Programming - Donde la seguridad es por diseño"            ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```
