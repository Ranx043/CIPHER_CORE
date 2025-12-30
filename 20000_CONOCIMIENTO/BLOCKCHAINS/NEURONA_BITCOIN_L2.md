# NEURONA: BITCOIN & LAYER 2s
## C20003 | Dominio de Bitcoin y Ecosistema Layer 2

```
╔═══════════════════════════════════════════════════════════════╗
║  CIPHER BLOCKCHAIN DOMAIN                                     ║
║  Bitcoin Core & Layer 2 Solutions                             ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## METADATA

```yaml
neurona_id: C20003
categoria: BLOCKCHAINS
nombre: BITCOIN_L2
version: 1.0.0
estado: ACTIVA
prioridad: ALTA

tags:
  - bitcoin
  - lightning
  - ordinals
  - stacks
  - layer2
```

---

## 1. BITCOIN FUNDAMENTALS

### 1.1 Arquitectura Core

```
BITCOIN ARCHITECTURE
│
├── DATA STRUCTURES
│   ├── Blockchain
│   │   ├── Linked blocks via hash
│   │   ├── 10 min block time (average)
│   │   ├── 1MB base block size
│   │   └── ~4MB with SegWit
│   │
│   ├── UTXO Model
│   │   ├── Unspent Transaction Outputs
│   │   ├── No account balances
│   │   ├── Inputs consume UTXOs
│   │   └── Outputs create new UTXOs
│   │
│   └── Merkle Tree
│       ├── Transaction hashing
│       ├── SPV proofs
│       └── Block header commitment
│
├── CRYPTOGRAPHY
│   ├── SHA-256 (double hash)
│   ├── RIPEMD-160 (address)
│   ├── ECDSA (secp256k1)
│   └── Schnorr signatures (Taproot)
│
├── CONSENSUS
│   ├── Proof of Work
│   │   ├── SHA-256 mining
│   │   ├── Difficulty adjustment (2016 blocks)
│   │   └── Longest chain rule
│   │
│   └── Economic Incentives
│       ├── Block reward (halving every 210K blocks)
│       ├── Transaction fees
│       └── Current: 3.125 BTC/block
│
└── SCRIPTING
    ├── Bitcoin Script
    │   ├── Stack-based
    │   ├── Not Turing complete
    │   └── Limited opcodes
    │
    └── Script Types
        ├── P2PKH (Legacy)
        ├── P2SH (Script Hash)
        ├── P2WPKH (Native SegWit)
        ├── P2WSH (SegWit Script)
        └── P2TR (Taproot)
```

### 1.2 UTXO Model Deep Dive

```yaml
utxo_model:
  concept:
    description: Unspent Transaction Outputs
    analogy: Like physical cash, not account balances

  structure:
    utxo:
      - txid: Transaction that created it
      - vout: Output index in transaction
      - value: Amount in satoshis
      - scriptPubKey: Locking script

  transaction:
    inputs:
      - Reference UTXOs to spend
      - Provide unlocking script (scriptSig)
      - Must spend entire UTXO

    outputs:
      - Create new UTXOs
      - Define locking conditions
      - Change goes to new UTXO

  example: |
    Transaction spending 1 BTC to pay 0.3 BTC:

    Inputs:
      - UTXO worth 1 BTC (from previous tx)

    Outputs:
      - 0.3 BTC to recipient
      - 0.699 BTC back to sender (change)
      - 0.001 BTC fee (implicit, no output)

  benefits:
    - Privacy (new addresses per tx)
    - Parallelization
    - Simpler validation
    - No double-spend in single tx

  challenges:
    - UTXO management
    - Dust accumulation
    - Change address complexity
```

### 1.3 Script Types

```yaml
bitcoin_scripts:

  p2pkh:
    name: Pay to Public Key Hash
    format: "1..." addresses
    script: |
      OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG
    unlock: |
      <signature> <pubKey>

  p2sh:
    name: Pay to Script Hash
    format: "3..." addresses
    use_case: Multi-sig, complex scripts
    script: |
      OP_HASH160 <scriptHash> OP_EQUAL
    unlock: |
      <data> <redeemScript>

  p2wpkh:
    name: Pay to Witness Public Key Hash
    format: "bc1q..." addresses
    benefits: Lower fees, malleability fix
    witness: |
      <signature> <pubKey>

  p2wsh:
    name: Pay to Witness Script Hash
    format: "bc1q..." (longer)
    use_case: Complex SegWit scripts

  p2tr:
    name: Pay to Taproot
    format: "bc1p..." addresses
    features:
      - Schnorr signatures
      - MAST (Merkelized scripts)
      - Privacy for complex scripts
    benefits:
      - All spends look the same
      - Smaller multi-sig
      - Script privacy
```

---

## 2. BITCOIN UPGRADES

### 2.1 SegWit (2017)

```yaml
segwit:
  name: Segregated Witness
  bips: BIP141, BIP143, BIP144

  changes:
    - Witness data separated
    - New transaction format
    - Block weight (not just size)
    - 4MB effective capacity

  benefits:
    - Malleability fix
    - Lower fees
    - Enables Lightning
    - Script versioning

  adoption:
    - ~80% of transactions
    - Native > wrapped preference
```

### 2.2 Taproot (2021)

```yaml
taproot:
  bips: BIP340 (Schnorr), BIP341 (Taproot), BIP342 (Tapscript)

  schnorr_signatures:
    benefits:
      - Smaller signatures
      - Batch verification
      - Key aggregation (MuSig2)
      - Multi-sig indistinguishable

  mast:
    name: Merkelized Alternative Script Trees
    concept:
      - Multiple spending conditions
      - Only reveal used path
      - Privacy for unused scripts

  tapscript:
    - New opcode versions
    - OP_CHECKSIGADD
    - Future upgradability

  use_cases:
    - Privacy for complex contracts
    - Efficient multi-sig
    - Time-locked contracts
    - Ordinals/Inscriptions
```

---

## 3. LIGHTNING NETWORK

### 3.1 Architecture

```
LIGHTNING NETWORK
│
├── PAYMENT CHANNELS
│   ├── 2-of-2 multisig on-chain
│   ├── Off-chain balance updates
│   ├── Commitment transactions
│   └── Revocation keys
│
├── HTLC (Hash Time-Locked Contracts)
│   ├── Conditional payments
│   ├── Hash preimage reveal
│   ├── Timeout fallback
│   └── Enables routing
│
├── ROUTING
│   ├── Multi-hop payments
│   ├── Source routing
│   ├── Onion encryption
│   └── Gossip protocol
│
├── CHANNEL LIFECYCLE
│   ├── Open (on-chain tx)
│   ├── Update (off-chain)
│   ├── Close (cooperative or forced)
│   └── Settlement (on-chain)
│
└── IMPLEMENTATIONS
    ├── LND (Lightning Labs)
    ├── c-lightning / CLN (Blockstream)
    ├── Eclair (ACINQ)
    └── LDK (Spiral)
```

### 3.2 Channel Operations

```yaml
channel_operations:

  opening:
    process:
      1: Create funding transaction (2-of-2 multisig)
      2: Exchange commitment transactions
      3: Broadcast funding tx
      4: Wait for confirmations
    cost: On-chain transaction fee

  updating:
    process:
      1: Create new commitment transactions
      2: Exchange signatures
      3: Revoke old state
    cost: Free (off-chain)

  closing:
    cooperative:
      - Both parties agree
      - Single on-chain tx
      - Fastest settlement

    force_close:
      - Unilateral close
      - Broadcast commitment tx
      - Time delay for dispute

  htlc_routing:
    mechanism:
      1: Sender creates hash secret
      2: Route found through network
      3: HTLCs chained along path
      4: Final recipient reveals preimage
      5: Payments settle backwards

  fees:
    base_fee: Fixed per forward (typical: 1 sat)
    fee_rate: Proportional (typical: 1 ppm)
```

### 3.3 Lightning Applications

```yaml
lightning_apps:

  wallets:
    custodial:
      - Wallet of Satoshi
      - Strike
      - Cash App
    non_custodial:
      - Phoenix
      - Breez
      - Muun
      - Zeus

  infrastructure:
    - Lightning Service Providers (LSP)
    - Channel liquidity providers
    - Routing nodes
    - Watchtowers

  protocols:
    lnurl:
      - Simplified payments
      - QR codes
      - Withdraw/pay/auth

    bolt11:
      - Standard invoices
      - Amount, description, expiry

    bolt12:
      - Offers (reusable invoices)
      - Blinded paths
      - Recurring payments

  use_cases:
    - Micropayments
    - Streaming payments
    - Point of sale
    - Gaming
    - Tipping
```

---

## 4. ORDINALS & BRC-20

### 4.1 Ordinal Theory

```yaml
ordinals:

  concept:
    description: Numbering individual satoshis
    mechanism: First-in-first-out across transactions
    purpose: NFTs on Bitcoin without changes

  inscriptions:
    description: Data attached to satoshis
    storage: Witness data (Taproot)
    types:
      - Images
      - Text
      - HTML/JS
      - Video (recursive)

  process:
    1: Choose satoshi to inscribe
    2: Create inscription content
    3: Commit transaction (hash of content)
    4: Reveal transaction (actual content)

  rarity:
    common: Any sat
    uncommon: First sat of block
    rare: First sat of difficulty adjustment
    epic: First sat of halving
    legendary: First sat of cycle
    mythic: First sat (sat 0)

  marketplaces:
    - Magic Eden (Ordinals)
    - Ordinals Market
    - Gamma
    - OKX Ordinals
```

### 4.2 BRC-20 Tokens

```yaml
brc_20:

  concept:
    description: Fungible tokens on Bitcoin
    mechanism: Inscription-based JSON
    standard: Not native, indexer-dependent

  operations:
    deploy: |
      {
        "p": "brc-20",
        "op": "deploy",
        "tick": "ordi",
        "max": "21000000",
        "lim": "1000"
      }

    mint: |
      {
        "p": "brc-20",
        "op": "mint",
        "tick": "ordi",
        "amt": "1000"
      }

    transfer: |
      {
        "p": "brc-20",
        "op": "transfer",
        "tick": "ordi",
        "amt": "500"
      }

  limitations:
    - Indexer dependent
    - No smart contracts
    - High fees during congestion
    - UTXO management

  notable_tokens:
    - ORDI (first BRC-20)
    - SATS
    - RATS
    - Various meme tokens
```

### 4.3 Runes Protocol

```yaml
runes:

  concept:
    description: Improved fungible tokens on Bitcoin
    creator: Casey Rodarmor (Ordinals creator)
    launch: Bitcoin halving 2024

  improvements_over_brc20:
    - UTXO-based (not inscription)
    - More efficient
    - Less blockchain bloat
    - Native-like feel

  mechanism:
    - Uses OP_RETURN
    - Embedded in transactions
    - No separate indexing needed

  etching:
    - Create new rune
    - Define supply, divisibility
    - Set minting rules

  operations:
    - Etch (create)
    - Mint
    - Transfer (via UTXO)
```

---

## 5. BITCOIN LAYER 2s

### 5.1 Stacks (STX)

```yaml
stacks:

  architecture:
    consensus: Proof of Transfer (PoX)
    mechanism:
      - Miners bid BTC for block rights
      - STX stakers earn BTC
      - Bitcoin finality

  smart_contracts:
    language: Clarity
    features:
      - Decidable
      - No reentrancy
      - Post-conditions
      - BTC visibility

  clarity_example: |
    (define-data-var counter uint u0)

    (define-public (increment)
      (begin
        (var-set counter (+ (var-get counter) u1))
        (ok (var-get counter))))

    (define-read-only (get-counter)
      (var-get counter))

  defi:
    - Alex (DEX)
    - Arkadiko (stablecoin)
    - STX20 tokens

  nakamoto_upgrade:
    - Faster blocks
    - Bitcoin finality
    - Improved security
```

### 5.2 RSK (Rootstock)

```yaml
rsk:

  architecture:
    consensus: Merged mining with Bitcoin
    compatibility: EVM compatible
    token: RBTC (pegged 1:1 to BTC)

  bridge:
    name: Powpeg
    mechanism:
      - Federation-based
      - Hardware security modules
      - 2-way peg

  development:
    - Solidity compatible
    - Ethereum tools work
    - Lower fees than mainnet ETH

  ecosystem:
    - Sovryn (DeFi)
    - Money on Chain (stablecoin)
    - RIF services
```

### 5.3 Liquid Network

```yaml
liquid:

  type: Federated sidechain
  operator: Blockstream

  features:
    - 1-minute blocks
    - Confidential transactions
    - Issued assets

  federation:
    - 15 functionaries
    - Multisig control
    - Watchmen for pegs

  use_cases:
    - Fast settlement
    - Confidential transfers
    - Security tokens
    - Exchange transfers

  assets:
    - L-BTC (pegged Bitcoin)
    - L-USDT (Tether)
    - Security tokens
```

### 5.4 BitVM

```yaml
bitvm:

  concept:
    description: Bitcoin smart contracts via fraud proofs
    approach: Optimistic computation

  mechanism:
    1: Off-chain computation
    2: Commitment on-chain
    3: Challenge period
    4: Fraud proof if disputed

  capabilities:
    - Turing complete computation
    - Trust-minimized bridges
    - Complex logic on Bitcoin

  limitations:
    - Complex setup
    - Challenge/response time
    - Early stage

  applications:
    - Trust-minimized BTC bridges
    - Complex escrows
    - Computation verification
```

---

## 6. BITCOIN DEVELOPMENT

### 6.1 Tools & Libraries

```yaml
development_tools:

  libraries:
    javascript:
      - bitcoinjs-lib
      - @scure/btc-signer
      - bip39, bip32

    python:
      - python-bitcoinlib
      - bip32utils

    rust:
      - rust-bitcoin
      - bdk (Bitcoin Dev Kit)

  apis:
    - Blockstream.info API
    - Mempool.space API
    - Blockchain.com API

  nodes:
    - Bitcoin Core
    - btcd (Go)
    - Libbitcoin

  lightning:
    - LND
    - c-lightning/CLN
    - Eclair
    - LDK
```

### 6.2 Best Practices

```yaml
bitcoin_best_practices:

  wallet:
    - Use HD wallets (BIP32/44/84)
    - Generate new addresses per transaction
    - Proper backup (seed phrase)
    - Hardware wallet for large amounts

  transactions:
    - Proper fee estimation
    - Coin selection algorithms
    - RBF for fee bumping
    - CPFP when needed

  security:
    - Multi-sig for high value
    - Cold storage
    - Time-locks for inheritance
    - Avoid address reuse
```

---

## FIRMA

```
╔═══════════════════════════════════════════════════════════════╗
║  NEURONA: BITCOIN_L2 | C20003                                ║
║  "The original blockchain - Bitcoin mastery"                  ║
╚═══════════════════════════════════════════════════════════════╝
```
