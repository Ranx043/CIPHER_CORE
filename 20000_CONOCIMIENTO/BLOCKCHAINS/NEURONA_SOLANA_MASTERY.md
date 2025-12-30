# NEURONA: SOLANA MASTERY
## C20002 | Dominio Completo del Ecosistema Solana

```
╔═══════════════════════════════════════════════════════════════╗
║  CIPHER BLOCKCHAIN DOMAIN                                     ║
║  Solana Ecosystem - Complete Mastery                          ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## METADATA

```yaml
neurona_id: C20002
categoria: BLOCKCHAINS
nombre: SOLANA_MASTERY
version: 1.0.0
estado: ACTIVA
prioridad: CRITICA

tags:
  - solana
  - rust
  - anchor
  - spl
  - high-performance
```

---

## 1. ARQUITECTURA SOLANA

### 1.1 Innovaciones Core

```
SOLANA ARCHITECTURE
│
├── PROOF OF HISTORY (PoH)
│   ├── Cryptographic clock
│   ├── SHA-256 hash chain
│   ├── Verifiable delay function
│   ├── Orders transactions before consensus
│   └── Enables parallel processing
│
├── TOWER BFT
│   ├── PoH-optimized PBFT
│   ├── Reduces communication overhead
│   ├── Uses PoH as clock
│   └── Exponential lockout
│
├── TURBINE
│   ├── Block propagation protocol
│   ├── Breaks data into packets
│   ├── Reed-Solomon erasure coding
│   └── Reduces bandwidth requirements
│
├── GULF STREAM
│   ├── Mempool-less transaction forwarding
│   ├── Validators know next leaders
│   ├── Transactions sent ahead
│   └── Reduces confirmation times
│
├── SEALEVEL
│   ├── Parallel smart contract runtime
│   ├── Transactions specify accounts
│   ├── Non-overlapping can run parallel
│   └── Horizontal scaling
│
├── PIPELINING
│   ├── Transaction processing unit
│   ├── Different hardware stages
│   ├── GPU for signature verification
│   └── Optimized throughput
│
└── CLOUDBREAK
    ├── Horizontally-scaled accounts database
    ├── Memory-mapped files
    ├── Concurrent read/write
    └── SSD optimized
```

### 1.2 Account Model

```yaml
solana_account_model:

  account_structure:
    fields:
      lamports: Balance in lamports (1 SOL = 1B lamports)
      data: Byte array for storage
      owner: Program that owns account
      executable: Is this a program?
      rent_epoch: Next rent due

  account_types:
    system_accounts:
      - User wallets (EOA equivalent)
      - Owned by System Program

    program_accounts:
      - Executable code
      - Owned by BPF Loader
      - Immutable after deployment (usually)

    data_accounts:
      - Store program state
      - Owned by programs
      - Programs can modify

    pda: # Program Derived Address
      - Deterministic from seeds
      - No private key
      - Programs can sign for them
      derivation: |
        PDA = hash(seeds, program_id, "ProgramDerivedAddress")
        Must be off Ed25519 curve

  rent:
    concept: Storage cost over time
    rent_exempt: 2 years rent prepaid
    calculation: ~0.00089088 SOL per byte per epoch
    minimum: ~0.00203928 SOL for account

  ownership_rules:
    - Only owner program can modify data
    - Only owner can debit lamports
    - Anyone can credit lamports
    - System Program owns wallets
```

### 1.3 Transaction Model

```yaml
solana_transactions:

  structure:
    signatures: Array of Ed25519 signatures
    message:
      header:
        num_required_signatures: u8
        num_readonly_signed: u8
        num_readonly_unsigned: u8
      account_keys: Array of Pubkeys
      recent_blockhash: Hash
      instructions: Array

  instruction:
    program_id_index: Which program to call
    accounts: Indices into account_keys
    data: Program-specific bytes

  constraints:
    max_size: 1232 bytes
    max_accounts: 64 (was 32)
    max_signatures: Variable
    compute_units: 200,000 default (1.4M max)

  versioned_transactions:
    v0: Address Lookup Tables
    benefits:
      - More accounts per tx
      - Reduced size
      - Better composability

  priority_fees:
    base_fee: 5000 lamports per signature
    priority_fee: Additional, set by user
    compute_unit_price: Micro-lamports per CU
    formula: |
      fee = signatures * 5000 +
            compute_units * compute_unit_price
```

---

## 2. DESARROLLO EN SOLANA

### 2.1 Anchor Framework

```rust
// Anchor Program Example
use anchor_lang::prelude::*;

declare_id!("YourProgramId111111111111111111111111111111");

#[program]
pub mod example_program {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>, data: u64) -> Result<()> {
        let my_account = &mut ctx.accounts.my_account;
        my_account.data = data;
        my_account.authority = ctx.accounts.authority.key();
        my_account.bump = ctx.bumps.my_account;

        msg!("Initialized with data: {}", data);
        Ok(())
    }

    pub fn update(ctx: Context<Update>, new_data: u64) -> Result<()> {
        let my_account = &mut ctx.accounts.my_account;
        my_account.data = new_data;

        emit!(DataUpdated {
            account: my_account.key(),
            old_data: my_account.data,
            new_data,
        });

        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        payer = authority,
        space = 8 + MyAccount::INIT_SPACE,
        seeds = [b"my-account", authority.key().as_ref()],
        bump
    )]
    pub my_account: Account<'info, MyAccount>,

    #[account(mut)]
    pub authority: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Update<'info> {
    #[account(
        mut,
        seeds = [b"my-account", authority.key().as_ref()],
        bump = my_account.bump,
        has_one = authority
    )]
    pub my_account: Account<'info, MyAccount>,

    pub authority: Signer<'info>,
}

#[account]
#[derive(InitSpace)]
pub struct MyAccount {
    pub data: u64,
    pub authority: Pubkey,
    pub bump: u8,
}

#[event]
pub struct DataUpdated {
    pub account: Pubkey,
    pub old_data: u64,
    pub new_data: u64,
}

#[error_code]
pub enum ErrorCode {
    #[msg("Unauthorized access")]
    Unauthorized,
    #[msg("Invalid data")]
    InvalidData,
}
```

### 2.2 Account Constraints (Anchor)

```yaml
anchor_constraints:

  initialization:
    init:
      - Creates new account
      - Requires payer
      - Requires space
    init_if_needed:
      - Creates if doesn't exist
      - Use with caution

  pda_seeds:
    seeds: Define PDA derivation
    bump: Store bump for efficiency

  validation:
    has_one: Check field matches
    constraint: Custom boolean check
    address: Check exact address

  account_types:
    Account: Deserializes data
    Signer: Must have signed
    Program: Executable account
    SystemAccount: Empty system owned
    UncheckedAccount: No validation

  example:
    code: |
      #[account(
          mut,
          seeds = [b"vault", user.key().as_ref()],
          bump = vault.bump,
          has_one = user,
          constraint = vault.amount >= withdrawal_amount @ ErrorCode::InsufficientFunds
      )]
      pub vault: Account<'info, Vault>,
```

### 2.3 Cross-Program Invocation (CPI)

```rust
// CPI Example - Calling Token Program
use anchor_lang::prelude::*;
use anchor_spl::token::{self, Token, TokenAccount, Transfer};

pub fn transfer_tokens(ctx: Context<TransferTokens>, amount: u64) -> Result<()> {
    let cpi_accounts = Transfer {
        from: ctx.accounts.from_ata.to_account_info(),
        to: ctx.accounts.to_ata.to_account_info(),
        authority: ctx.accounts.authority.to_account_info(),
    };

    let cpi_program = ctx.accounts.token_program.to_account_info();
    let cpi_ctx = CpiContext::new(cpi_program, cpi_accounts);

    token::transfer(cpi_ctx, amount)?;

    Ok(())
}

// CPI with PDA signer
pub fn transfer_from_pda(ctx: Context<TransferFromPda>, amount: u64) -> Result<()> {
    let seeds = &[
        b"vault".as_ref(),
        ctx.accounts.user.key.as_ref(),
        &[ctx.accounts.vault.bump],
    ];
    let signer_seeds = &[&seeds[..]];

    let cpi_accounts = Transfer {
        from: ctx.accounts.vault_ata.to_account_info(),
        to: ctx.accounts.user_ata.to_account_info(),
        authority: ctx.accounts.vault.to_account_info(),
    };

    let cpi_ctx = CpiContext::new_with_signer(
        ctx.accounts.token_program.to_account_info(),
        cpi_accounts,
        signer_seeds
    );

    token::transfer(cpi_ctx, amount)?;

    Ok(())
}
```

---

## 3. TOKEN STANDARDS

### 3.1 SPL Token Program

```yaml
spl_token:
  description: Standard fungible token program

  key_concepts:
    mint:
      - Defines token
      - Supply, decimals
      - Mint authority
      - Freeze authority

    token_account:
      - Holds tokens for owner
      - Associated with mint
      - Has owner (wallet)

    associated_token_account:
      - Deterministic derivation
      - Standard location per wallet/mint
      - derivation: ATA(wallet, mint)

  operations:
    - create_mint
    - mint_to
    - transfer
    - burn
    - approve (delegation)
    - freeze/thaw

token_2022:
  description: Extended token program

  extensions:
    transfer_fees:
      - Automatic fee on transfers
      - Configurable rate
      - Fee recipient

    interest_bearing:
      - Accrues interest over time
      - Rate configurable

    non_transferable:
      - Soulbound tokens
      - Cannot transfer

    permanent_delegate:
      - Always has delegate
      - Can burn/transfer

    confidential_transfers:
      - ZK-based privacy
      - Hidden amounts

    transfer_hooks:
      - Call external program on transfer
      - Custom validation logic

    metadata_pointer:
      - Point to metadata account
      - Standard metadata location
```

### 3.2 Metaplex NFT Standards

```yaml
metaplex_standards:

  token_metadata:
    description: Original NFT standard
    components:
      - Metadata account
      - Master Edition
      - Edition prints

  metaplex_core:
    description: New simplified standard
    features:
      - Single account
      - Plugins system
      - Lower rent
      - Better composability

  compressed_nfts:
    description: State compression for scale
    technology:
      - Merkle trees
      - Off-chain storage
      - On-chain root only
    cost: ~$0.0001 per NFT vs ~$2

  bubblegum:
    description: Program for compressed NFTs
    features:
      - Mint cNFTs
      - Transfer
      - Burn
      - Collection management

candy_machine:
  description: NFT minting program
  versions:
    v3:
      - Guards system
      - Flexible configuration
      - Multiple payment options
  guards:
    - Start/end time
    - Payment (SOL, SPL)
    - Allowlist
    - NFT gate
    - Limit per wallet
```

---

## 4. SOLANA DeFi

### 4.1 DEX Ecosystem

```yaml
dex_protocols:

  jupiter:
    type: Aggregator
    features:
      - Best price routing
      - Split routes
      - DCA orders
      - Limit orders
      - Perp trading
    market_share: Dominant aggregator

  raydium:
    type: AMM + CLMM
    features:
      - Concentrated liquidity (CLMM)
      - Legacy AMM pools
      - AcceleRaytor launchpad
    liquidity: High for major pairs

  orca:
    type: CLMM
    features:
      - Whirlpools (concentrated)
      - Low fees
      - Good UX
    focus: Capital efficiency

  phoenix:
    type: Order book
    features:
      - Fully on-chain orderbook
      - Atomic settlement
      - High throughput

  openbook:
    type: Order book (Serum fork)
    features:
      - Central limit order book
      - Permissioned markets
      - Foundation governed
```

### 4.2 Lending & Staking

```yaml
lending_protocols:

  kamino:
    features:
      - Lending/borrowing
      - Automated vaults
      - Multiply/leverage
      - K-tokens

  solend:
    features:
      - Algorithmic lending
      - Isolated pools
      - Main pool

  marginfi:
    features:
      - Lending/borrowing
      - Points system
      - Risk management

liquid_staking:

  marinade:
    token: mSOL
    features:
      - Stake delegation
      - Instant unstake
      - DeFi integration
    market_share: Largest LST

  jito:
    token: JitoSOL
    features:
      - MEV rewards
      - Validator selection
      - Higher APY from MEV

  blaze:
    token: bSOL
    features:
      - Decentralized
      - Custom delegation
```

### 4.3 Perpetuals

```yaml
perp_protocols:

  drift:
    type: vAMM Perpetuals
    features:
      - Cross-margin
      - Up to 20x leverage
      - Spot trading
      - Prediction markets
    volume: Top Solana perps

  jupiter_perps:
    type: Oracle-based
    features:
      - Jupiter integration
      - Simple UX
      - Up to 100x

  zeta_markets:
    type: Order book perps
    features:
      - Options + perps
      - On-chain orderbook
      - Cross-margin
```

---

## 5. INFRAESTRUCTURA

### 5.1 RPC & Nodes

```yaml
rpc_providers:
  helius:
    features:
      - DAS API (NFTs)
      - Webhooks
      - Enhanced APIs
      - RPC
    specialty: NFT data, webhooks

  quicknode:
    features:
      - Standard RPC
      - Add-ons
      - Global network

  triton:
    features:
      - High performance
      - Rate limits generous
      - Geyser plugin support

  alchemy:
    features:
      - Enhanced APIs
      - NFT API
      - Webhooks

node_types:
  validator:
    requirements:
      - 256GB+ RAM
      - 2TB+ NVMe
      - 10 Gbps network
      - High-end CPU
    purpose: Consensus participation

  rpc:
    requirements:
      - 512GB+ RAM
      - 2TB+ NVMe
      - Similar to validator
    purpose: Serve requests

  geyser_plugins:
    description: Stream account updates
    examples:
      - Yellowstone (Triton)
      - AccountsDB plugin
```

### 5.2 Indexing

```yaml
indexing_solutions:

  helius_das:
    description: Digital Asset Standard API
    features:
      - NFT metadata
      - Compressed NFT support
      - Fungible assets
      - Collections

  shyft:
    features:
      - NFT APIs
      - DeFi APIs
      - Webhooks
      - GraphQL

  simpleHash:
    features:
      - Multi-chain NFT API
      - Solana support
      - Metadata normalization

  hello_moon:
    features:
      - Analytics APIs
      - DeFi data
      - NFT data
```

---

## 6. DEVELOPMENT TOOLS

### 6.1 CLI & SDKs

```yaml
solana_cli:
  commands:
    wallet:
      - solana-keygen new
      - solana address
      - solana balance

    network:
      - solana config set --url <RPC>
      - solana cluster-version

    transactions:
      - solana transfer <to> <amount>
      - solana confirm <signature>

    programs:
      - solana program deploy <path>
      - solana program show <address>

anchor_cli:
  commands:
    - anchor init <project>
    - anchor build
    - anchor test
    - anchor deploy
    - anchor idl init/upgrade

sdks:
  javascript:
    - @solana/web3.js (core)
    - @solana/spl-token
    - @coral-xyz/anchor
    - @metaplex-foundation/js

  python:
    - solana-py
    - anchorpy

  rust:
    - solana-sdk
    - anchor-client
```

### 6.2 Testing

```yaml
testing_approaches:

  local_validator:
    command: solana-test-validator
    features:
      - Local blockchain
      - Fast iteration
      - Clone accounts from mainnet

  anchor_tests:
    framework: Mocha + Chai
    location: tests/*.ts
    example: |
      it("Initializes account", async () => {
        await program.methods
          .initialize(new BN(100))
          .accounts({
            myAccount: myAccountPda,
            authority: provider.wallet.publicKey,
            systemProgram: SystemProgram.programId,
          })
          .rpc();

        const account = await program.account.myAccount.fetch(myAccountPda);
        assert.equal(account.data.toNumber(), 100);
      });

  bankrun:
    description: Fast testing framework
    features:
      - No validator needed
      - Rust-based
      - Very fast

  amman:
    description: Local validator wrapper
    features:
      - Account cloning
      - State snapshots
      - Better DevX
```

---

## 7. SECURITY CONSIDERATIONS

### 7.1 Common Vulnerabilities

```yaml
solana_vulnerabilities:

  missing_signer_check:
    severity: CRITICAL
    description: Not verifying signer
    fix: Use Signer type in Anchor

  missing_owner_check:
    severity: CRITICAL
    description: Not verifying account owner
    fix: Anchor Account<> type validates

  pda_validation:
    severity: HIGH
    description: Not validating PDA seeds
    fix: Use seeds constraint in Anchor

  arbitrary_cpi:
    severity: HIGH
    description: CPI to attacker program
    fix: Validate program_id

  integer_overflow:
    severity: HIGH
    description: Rust doesn't panic by default in release
    fix: Use checked_* methods

  reinitialization:
    severity: MEDIUM
    description: Reinitializing accounts
    fix: Check is_initialized flag

  closing_accounts:
    severity: MEDIUM
    description: Improper account closing
    fix: Zero data, transfer lamports, reassign owner

best_practices:
  - Always use Anchor constraints
  - Validate all accounts
  - Use checked math
  - Proper account closing
  - Audit before mainnet
```

---

## 8. ECOSYSTEM

### 8.1 Major Projects

```yaml
ecosystem_map:

  defi:
    - Jupiter (aggregator)
    - Raydium (AMM)
    - Orca (CLMM)
    - Marinade (liquid staking)
    - Drift (perps)
    - Kamino (lending)

  nfts:
    - Magic Eden (marketplace)
    - Tensor (trading)
    - Metaplex (infrastructure)

  gaming:
    - Star Atlas
    - Aurory
    - Genopets

  infrastructure:
    - Helius (RPC, data)
    - Jito (MEV)
    - Pyth (oracles)
    - Wormhole (bridge)

  wallets:
    - Phantom
    - Solflare
    - Backpack
```

---

## FIRMA

```
╔═══════════════════════════════════════════════════════════════╗
║  NEURONA: SOLANA_MASTERY | C20002                            ║
║  "Speed meets scalability - Solana expertise"                 ║
╚═══════════════════════════════════════════════════════════════╝
```
