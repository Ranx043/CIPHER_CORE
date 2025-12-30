# NEURONA: FUNDRAISING & LEGAL
## C90002 | Financiamiento y Marco Legal Crypto

```
╔═══════════════════════════════════════════════════════════════╗
║  CIPHER BUSINESS DOMAIN                                       ║
║  Fundraising Strategies & Legal Frameworks                    ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## METADATA

```yaml
neurona_id: C90002
categoria: BUSINESS
nombre: FUNDRAISING_LEGAL
version: 1.0.0
estado: ACTIVA
prioridad: ALTA

dependencias:
  - C90001_CRYPTO_ENTREPRENEURSHIP
  - C40008_TOKENOMICS

tags:
  - fundraising
  - legal
  - compliance
  - vc
  - tokenomics
```

---

## 1. ESTRATEGIAS DE FUNDRAISING

### 1.1 Etapas de Financiamiento

```
FUNDING JOURNEY
│
├── BOOTSTRAPPING (Pre-Funding)
│   ├── Self-funding
│   ├── Friends & Family
│   ├── Hackathon prizes
│   ├── Grants
│   └── Revenue (if applicable)
│
├── PRE-SEED ($100K - $500K)
│   ├── Angels
│   ├── Small crypto funds
│   ├── Accelerators
│   └── Valuation: $2M - $8M
│
├── SEED ($500K - $5M)
│   ├── Crypto VCs
│   ├── Strategic investors
│   ├── Token warrants/SAFTs
│   └── Valuation: $10M - $50M
│
├── SERIES A ($5M - $25M)
│   ├── Lead investors
│   ├── Institutional capital
│   ├── Clear metrics required
│   └── Valuation: $50M - $150M
│
├── SERIES B+ ($25M+)
│   ├── Growth capital
│   ├── Expansion funding
│   └── Valuation: $150M+
│
└── TOKEN LAUNCH (Alternative/Parallel)
    ├── Public sale / IDO
    ├── Liquidity mining
    └── Community distribution
```

### 1.2 Instrumentos de Inversión

```yaml
investment_instruments:

  equity_based:
    safe:
      name: Simple Agreement for Future Equity
      description: Converts to equity at future priced round
      terms:
        - Valuation cap
        - Discount (typically 20%)
        - MFN clause optional
      pros:
        - Simple documentation
        - Fast to close
        - No valuation negotiation
      cons:
        - Dilution uncertainty
        - Cap table complexity

    priced_round:
      description: Direct equity purchase
      terms:
        - Pre-money valuation
        - Share price
        - Liquidation preference
        - Anti-dilution protection
        - Board seats
        - Information rights
      when_used: Series A+

  token_based:
    saft:
      name: Simple Agreement for Future Tokens
      description: Right to receive tokens at TGE
      terms:
        - Token price or discount
        - Vesting schedule
        - Lock-up period
        - Network launch conditions
      regulatory: Securities implications

    token_warrant:
      description: Right to purchase tokens
      structure:
        - Attached to equity
        - Exercise price
        - Allocation amount
        - Vesting aligned with equity
      benefit: Investor gets both equity + tokens

    direct_token:
      description: Purchase tokens directly
      types:
        - Private sale
        - Strategic round
        - Pre-TGE allocation
      terms:
        - Discount to public price
        - Vesting schedule
        - Lock-up

  hybrid:
    safe_token_side_letter:
      structure:
        - SAFE for equity
        - Side letter for token rights
        - Most common structure
      terms:
        - Equity SAFE terms
        - Token allocation %
        - Token vesting

    convertible_note:
      description: Debt that converts
      terms:
        - Interest rate
        - Maturity date
        - Conversion discount
        - Valuation cap
      note: Less common in crypto
```

### 1.3 Deal Structure Examples

```yaml
seed_round_example:
  overview:
    round: Seed
    amount: $3,000,000
    valuation: $15,000,000 (post-money)

  equity_component:
    instrument: SAFE
    cap: $12,000,000 (pre-money)
    discount: 20%
    pro_rata: Yes

  token_component:
    instrument: Token Side Letter
    allocation: 3% of total supply
    price: $0.015 per token
    discount: 50% to expected TGE
    vesting:
      cliff: 6 months
      duration: 24 months
      tge_unlock: 0%

  investor_breakdown:
    - Lead VC: $1,500,000 (50%)
    - VC 2: $750,000 (25%)
    - VC 3: $500,000 (17%)
    - Angels: $250,000 (8%)

  documentation:
    - SAFE Agreement
    - Token Side Letter
    - Investor Rights Agreement
    - Board Observer Agreement (lead)

strategic_round_example:
  overview:
    round: Strategic
    amount: $5,000,000
    structure: Token only

  token_terms:
    allocation: 5% of total supply
    price: $0.10 per token
    discount: 33% to expected public
    vesting:
      cliff: 3 months
      duration: 18 months
      tge_unlock: 10%

  strategic_value:
    - Protocol integration
    - Co-marketing
    - Technical support
    - Network effects

  investors:
    - Partner Protocol Treasury
    - Exchange Ventures
    - Infrastructure Provider
```

### 1.4 Investor Targeting

```yaml
investor_types:

  crypto_native_vcs:
    tier_1:
      - a16z Crypto
      - Paradigm
      - Polychain
      - Pantera
      - Multicoin
    characteristics:
      - Large checks ($5M+)
      - Long-term focused
      - Platform support
      - Brand value
    what_they_want:
      - Exceptional teams
      - Large markets
      - Technical innovation
      - Network effects

  specialist_funds:
    defi_focused:
      - Framework Ventures
      - DeFiance Capital
      - Mechanism Capital
    infra_focused:
      - Placeholder
      - Electric Capital
    gaming_nft:
      - Animoca Brands
      - Merit Circle
      - Sfermion

  accelerators:
    programs:
      - Alliance DAO
      - Seed Club
      - Outlier Ventures
      - Encode Club
    benefits:
      - Curriculum
      - Network
      - Initial capital
      - Credibility

  angels:
    categories:
      - Protocol founders
      - Successful operators
      - Crypto OGs
    how_to_find:
      - Twitter/X
      - Conferences
      - Warm intros
      - Angel networks

  strategic_investors:
    types:
      - Protocol treasuries
      - Exchange venture arms
      - Infrastructure providers
    benefits:
      - Partnership value
      - Integration priority
      - Distribution
    examples:
      - Coinbase Ventures
      - Binance Labs
      - Uniswap Ventures
```

---

## 2. LEGAL FRAMEWORKS

### 2.1 Entity Structuring

```yaml
entity_structures:

  foundation:
    jurisdictions:
      cayman_islands:
        type: Foundation Company
        benefits:
          - Tax neutral
          - Flexible governance
          - Token-friendly
        costs: $15K-25K setup, $10K+ annual

      switzerland:
        type: Stiftung (Foundation)
        benefits:
          - Crypto Valley ecosystem
          - Regulatory clarity
          - Strong reputation
        costs: $50K+ setup, higher ongoing

      singapore:
        type: Company Limited by Guarantee
        benefits:
          - Asian hub
          - Clear regulations
          - English common law
        costs: $10K-20K setup

    purpose:
      - Protocol governance
      - Token distribution
      - Grants programs
      - Community management

  operating_company:
    jurisdictions:
      delaware:
        type: C-Corp or LLC
        benefits:
          - VC familiar
          - Clear laws
          - Fast setup
        considerations:
          - US tax implications
          - Securities concerns

      singapore:
        type: Pte. Ltd.
        benefits:
          - Low taxes (17%)
          - Crypto-friendly banks
          - Asia presence

      dubai:
        type: DMCC or DIFC
        benefits:
          - 0% corporate tax
          - Crypto regulations (VARA)
          - No personal income tax

      british_virgin_islands:
        type: BVI Business Company
        benefits:
          - Tax neutral
          - Privacy
          - Fast setup

    purpose:
      - Development services
      - Employee contracts
      - Revenue generation
      - IP ownership

  typical_structure:
    diagram: |
      [Foundation - Cayman]
          |
          |-- Owns protocol/token
          |-- Receives protocol fees
          |-- Distributes grants
          |
      [Labs Company - Delaware/Singapore]
          |
          |-- Development services
          |-- Employs team
          |-- Service agreement with Foundation
          |
      [DAO - On-chain]
          |
          |-- Governance votes
          |-- Treasury management
          |-- Decentralized control
```

### 2.2 Token Classification

```yaml
token_classification:

  howey_test:
    description: US test for securities
    elements:
      - Investment of money
      - Common enterprise
      - Expectation of profits
      - From efforts of others
    if_all_true: Likely a security

  utility_token:
    characteristics:
      - Functional at launch
      - Primary use is utility
      - Not marketed as investment
      - Decentralized network
    examples:
      - UNI (governance)
      - LINK (payment for oracle)
      - FIL (storage payment)

  security_token:
    characteristics:
      - Investment expectation
      - Profit from others' efforts
      - Pre-functional sale
      - Centralized development
    implications:
      - SEC registration required
      - Accredited investors only
      - Significant restrictions

  sufficient_decentralization:
    concept: SEC guidance (Hinman speech)
    factors:
      - No central party
      - Network is functional
      - Distributed development
      - Open participation
    examples:
      - BTC (decentralized)
      - ETH (sufficiently decentralized)

  regulatory_approaches:
    us_sec:
      - Very aggressive
      - Most tokens = securities
      - Enforcement actions common

    eu_mica:
      - New framework (2024)
      - Asset-Referenced Tokens
      - E-Money Tokens
      - Utility Tokens
      - Licensing required

    singapore_mas:
      - Payment tokens
      - Utility tokens
      - Security tokens
      - Clear categories

    switzerland_finma:
      - Payment tokens
      - Utility tokens
      - Asset tokens
      - ICO guidelines
```

### 2.3 Compliance Requirements

```yaml
compliance_framework:

  kyc_aml:
    when_required:
      - Token sales
      - Fiat on/off ramps
      - Centralized services
      - Certain DeFi activities

    implementation:
      kyc_providers:
        - Jumio
        - Onfido
        - Sumsub
        - Persona

      aml_screening:
        - Chainalysis
        - Elliptic
        - TRM Labs

      requirements:
        - Identity verification
        - Sanctions screening
        - PEP screening
        - Transaction monitoring

  geo_restrictions:
    typically_blocked:
      - United States (often)
      - China
      - North Korea
      - Iran
      - Cuba
      - Crimea region
      - Russia (increasingly)

    implementation:
      - Terms of Service exclusion
      - IP blocking
      - VPN detection
      - Wallet screening

  data_privacy:
    gdpr:
      scope: EU users
      requirements:
        - Lawful basis for processing
        - Data minimization
        - Right to access/delete
        - Privacy policy
        - DPO (if required)

    ccpa:
      scope: California residents
      requirements:
        - Privacy notice
        - Opt-out rights
        - Data access rights

  financial_licenses:
    may_need:
      - Money Transmitter License (US states)
      - Virtual Asset Service Provider (EU)
      - Payment Institution License
      - Exchange License

    when_exempt:
      - Truly decentralized
      - Non-custodial
      - No fiat handling
```

### 2.4 Legal Documentation

```yaml
legal_documents:

  user_facing:
    terms_of_service:
      contents:
        - Service description
        - User responsibilities
        - Prohibited activities
        - Disclaimers
        - Governing law
        - Dispute resolution

    privacy_policy:
      contents:
        - Data collected
        - How data used
        - Data sharing
        - User rights
        - Contact information

    token_terms:
      contents:
        - Token description
        - No investment expectation
        - Risks disclosure
        - Regulatory disclaimers

  fundraising:
    saft_agreement:
      contents:
        - Token rights
        - Purchase price
        - Network launch conditions
        - Vesting terms
        - Representations

    token_side_letter:
      contents:
        - Token allocation
        - Vesting schedule
        - Price/discount
        - Conditions

    investor_rights:
      contents:
        - Information rights
        - Pro-rata rights
        - Board rights
        - Registration rights

  corporate:
    service_agreement:
      purpose: Foundation ↔ Labs relationship
      contents:
        - Scope of services
        - Payment terms
        - IP assignment
        - Termination

    contributor_agreement:
      purpose: DAO contributors
      contents:
        - Work scope
        - IP assignment
        - Payment in tokens
        - Independent contractor status
```

---

## 3. TAX CONSIDERATIONS

### 3.1 Entity Taxation

```yaml
corporate_tax:

  us_delaware:
    federal: 21%
    state: 8.7% (Delaware)
    considerations:
      - CFC rules for foreign subs
      - GILTI on foreign income
      - Transfer pricing

  singapore:
    rate: 17%
    benefits:
      - Territorial system
      - Tax treaties
      - Startup exemptions
    crypto_specific:
      - Tokens as property
      - Trading gains may be taxable

  cayman:
    rate: 0%
    benefits:
      - No corporate tax
      - No withholding tax
      - Foundation structure
    substance_requirements:
      - Directors
      - Management
      - Decision making

  dubai:
    rate: 0% (on qualifying income)
    benefits:
      - No personal income tax
      - Free zones available
      - VARA regulation

  switzerland:
    rate: 11-24% (canton dependent)
    benefits:
      - Crypto Valley (Zug)
      - Clear guidelines
      - Holding company benefits
```

### 3.2 Token Taxation

```yaml
token_tax_events:

  for_projects:
    token_creation:
      - Generally no tax event
      - Value at creation unclear

    token_sale:
      - Revenue recognition
      - SAFT treatment varies
      - Jurisdiction dependent

    airdrops_distribution:
      - May be taxable distribution
      - FMV at distribution

    treasury_operations:
      - Trading gains/losses
      - DeFi yields

  for_investors:
    token_purchase:
      - Cost basis establishment
      - Purchase price + fees

    token_sale:
      - Capital gain/loss
      - Holding period matters

    staking_rewards:
      - Income at receipt (US)
      - FMV at receipt

    airdrops:
      - Income at receipt
      - FMV at receipt
      - Cost basis = FMV
```

---

## 4. DAO LEGAL FRAMEWORKS

### 4.1 DAO Legal Wrappers

```yaml
dao_legal_structures:

  unincorporated:
    status: General partnership by default
    risks:
      - Unlimited liability
      - Tax pass-through
      - Member exposure
    when_appropriate:
      - Small DAOs
      - Limited activities
      - No real-world interaction

  wyoming_dao_llc:
    statute: Wyoming DAO LLC Act
    features:
      - Limited liability
      - Smart contract governance
      - Algorithmic management
    requirements:
      - Wyoming registered agent
      - DAO designation in name
      - Notice to members
    limitations:
      - Wyoming-specific
      - Untested in courts

  marshall_islands_dao_llc:
    features:
      - International recognition
      - Flexible governance
      - Token-based membership
    process:
      - Registration
      - Operating agreement
      - Smart contract reference

  foundation_wrapper:
    structure:
      - Foundation holds assets
      - DAO governs foundation
      - Legal personality
    jurisdictions:
      - Cayman
      - Switzerland
      - Singapore
```

### 4.2 DAO Governance Legal Issues

```yaml
dao_legal_issues:

  liability:
    questions:
      - Who is liable for DAO actions?
      - Are token holders partners?
      - What about delegators?
    mitigations:
      - Legal wrapper
      - Clear disclaimers
      - Insurance
      - Limited scope

  contracts:
    issues:
      - Can DAO sign contracts?
      - Who signs on behalf?
      - Enforcement questions
    solutions:
      - Foundation wrapper
      - Authorized signers
      - Clear governance

  employment:
    issues:
      - Contributors vs employees
      - Benefits and protections
      - Tax withholding
    structures:
      - Independent contractors
      - Contributor agreements
      - Employer of record services

  regulatory:
    issues:
      - Securities concerns
      - AML/KYC requirements
      - Cross-border compliance
    approaches:
      - Sufficient decentralization
      - Geographic restrictions
      - Compliance protocols
```

---

## 5. BEST PRACTICES

### 5.1 Fundraising Process

```yaml
fundraising_best_practices:

  preparation:
    materials:
      - Pitch deck (10-15 slides)
      - Financial model
      - Token model (if applicable)
      - Data room
      - Demo/product

    data_room:
      - Corporate documents
      - Team bios
      - Cap table
      - Financial statements
      - Key contracts
      - Technical docs

  process:
    timeline: 3-6 months typical
    steps:
      1_preparation:
        - Refine materials
        - Build target list
        - Get warm intros

      2_outreach:
        - Reach out to targets
        - Schedule meetings
        - Track in CRM

      3_meetings:
        - Initial pitch
        - Follow-up deep dives
        - Technical reviews

      4_term_sheet:
        - Negotiate terms
        - Select lead
        - Syndicate round

      5_due_diligence:
        - Legal DD
        - Technical DD
        - Background checks

      6_closing:
        - Documentation
        - Signatures
        - Wire transfers

  tips:
    - Create urgency (competing offers)
    - Be transparent about metrics
    - Know your numbers cold
    - Have references ready
    - Maintain momentum
```

### 5.2 Legal Best Practices

```yaml
legal_best_practices:

  early_stage:
    - Choose jurisdiction carefully
    - Get legal counsel early
    - Proper entity setup
    - Clean cap table
    - IP assignment

  fundraising:
    - Use standard documents
    - Get securities opinion
    - Proper disclosures
    - KYC for investors
    - Clean data room

  token_launch:
    - Legal opinion on classification
    - Terms of service
    - Risk disclosures
    - Geographic restrictions
    - Compliance procedures

  ongoing:
    - Regular legal reviews
    - Regulatory monitoring
    - Compliance updates
    - Documentation maintenance
```

---

## FIRMA

```
╔═══════════════════════════════════════════════════════════════╗
║  NEURONA: FUNDRAISING_LEGAL | C90002                         ║
║  "Navigate the legal landscape with confidence"               ║
╚═══════════════════════════════════════════════════════════════╝
```
