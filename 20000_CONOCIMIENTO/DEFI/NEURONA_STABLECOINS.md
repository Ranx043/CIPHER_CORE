# NEURONA: STABLECOINS & CDP SYSTEMS
## C40004 - Stablecoin Architectures

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  CIPHER NEURONA: STABLECOINS                                                   ║
║  Dominio: Algorithmic, Collateralized, CDP, Fiat-Backed                        ║
║  Estado: ACTIVA                                                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. TIPOS DE STABLECOINS

```
STABLECOIN CLASSIFICATION
══════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────┐
│                         STABLECOIN TAXONOMY                              │
├────────────────┬────────────────┬────────────────┬─────────────────────┤
│ FIAT-BACKED    │ CRYPTO-BACKED  │ ALGORITHMIC    │ HYBRID              │
├────────────────┼────────────────┼────────────────┼─────────────────────┤
│ USDT           │ DAI            │ UST (defunct)  │ FRAX                │
│ USDC           │ LUSD           │ AMPL           │ crvUSD              │
│ BUSD           │ sUSD           │ OHM            │ GHO                 │
│ TUSD           │ RAI            │ FLOAT          │ eUSD                │
├────────────────┼────────────────┼────────────────┼─────────────────────┤
│ Backing: 100%  │ Backing: >100% │ Backing: Algo  │ Backing: Partial    │
│ Trust: Central │ Trust: Smart   │ Trust: Algo    │ Trust: Mixed        │
│ Censorship: ✓  │ Censorship: ✗  │ Censorship: ✗  │ Censorship: Partial │
│ Capital Eff: ✓ │ Capital Eff: ✗ │ Capital Eff: ✓ │ Capital Eff: ✓      │
└────────────────┴────────────────┴────────────────┴─────────────────────┘

RISK SPECTRUM:
Centralization ──────────────────────────────────────→ Decentralization
USDC ──→ FRAX ──→ DAI ──→ LUSD ──→ RAI

Capital Efficiency ─────────────────────────────────→ Over-collateralized
Algo ──→ USDC (1:1) ──→ FRAX ──→ DAI (150%) ──→ LUSD (110%+)
```

---

## 2. FIAT-BACKED STABLECOINS

### 2.1 Arquitectura USDC/USDT

```
FIAT-BACKED ARCHITECTURE
═══════════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────────┐
│                         ISSUANCE FLOW                                 │
│                                                                       │
│  User ──USD──→ Bank ──confirm──→ Issuer ──mint──→ Smart Contract     │
│                                                                       │
│  User ←─USDC──← Smart Contract ←─approve──← Issuer ←─custody─→ Bank  │
│                                                                       │
├──────────────────────────────────────────────────────────────────────┤
│                         REDEMPTION FLOW                               │
│                                                                       │
│  User ──USDC──→ Smart Contract ──burn──→ Issuer ──release──→ Bank   │
│                                                                       │
│  User ←───────────────────USD───────────────────←─wire──← Bank       │
└──────────────────────────────────────────────────────────────────────┘

RESERVE COMPOSITION (USDC - Circle):
├── Cash: ~20%
├── US Treasuries: ~80%
└── Total: 100%+ (may include profit buffer)

BLACKLIST MECHANISM:
├── frozenBalances mapping
├── isBlacklisted modifier
└── Central control over funds
```

### 2.2 Contrato Simplificado

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

/**
 * @title FiatBackedStablecoin
 * @notice Simplified fiat-backed stablecoin (USDC-style)
 */
contract FiatBackedStablecoin is ERC20, AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant BLACKLISTER_ROLE = keccak256("BLACKLISTER_ROLE");

    // Blacklisted addresses
    mapping(address => bool) public blacklisted;

    // Frozen balances
    mapping(address => bool) public frozen;

    event Blacklisted(address indexed account);
    event UnBlacklisted(address indexed account);
    event Frozen(address indexed account);
    event Unfrozen(address indexed account);

    constructor() ERC20("USD Coin", "USDC") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
        _grantRole(BLACKLISTER_ROLE, msg.sender);
    }

    /**
     * @notice Mint new tokens (only minter)
     */
    function mint(address to, uint256 amount) external onlyRole(MINTER_ROLE) {
        require(!blacklisted[to], "Recipient blacklisted");
        _mint(to, amount);
    }

    /**
     * @notice Burn tokens (redemption)
     */
    function burn(uint256 amount) external {
        require(!blacklisted[msg.sender], "Sender blacklisted");
        _burn(msg.sender, amount);
    }

    /**
     * @notice Blacklist an address
     */
    function blacklist(address account) external onlyRole(BLACKLISTER_ROLE) {
        blacklisted[account] = true;
        emit Blacklisted(account);
    }

    /**
     * @notice Remove from blacklist
     */
    function unBlacklist(address account) external onlyRole(BLACKLISTER_ROLE) {
        blacklisted[account] = false;
        emit UnBlacklisted(account);
    }

    /**
     * @notice Freeze account (seize funds)
     */
    function freeze(address account) external onlyRole(BLACKLISTER_ROLE) {
        frozen[account] = true;
        emit Frozen(account);
    }

    /**
     * @dev Override transfer to check blacklist
     */
    function _update(address from, address to, uint256 amount) internal virtual override {
        require(!blacklisted[from], "Sender blacklisted");
        require(!blacklisted[to], "Recipient blacklisted");
        require(!frozen[from], "Sender frozen");
        super._update(from, to, amount);
    }

    /**
     * @notice 6 decimals (standard for USD stablecoins)
     */
    function decimals() public pure override returns (uint8) {
        return 6;
    }
}
```

---

## 3. CDP (COLLATERALIZED DEBT POSITION)

### 3.1 MakerDAO Architecture

```
MAKERDAO CDP SYSTEM
═══════════════════════════════════════════════════════════════════════

┌───────────────────────────────────────────────────────────────────────┐
│                        CDP LIFECYCLE                                   │
│                                                                        │
│  1. DEPOSIT        2. GENERATE        3. REPAY         4. WITHDRAW    │
│  ┌─────────┐      ┌─────────┐       ┌─────────┐      ┌─────────┐     │
│  │  ETH    │      │  DAI    │       │  DAI +  │      │  ETH    │     │
│  │   ↓     │      │   ↑     │       │  Fee    │      │   ↑     │     │
│  │  Vault  │ →→→  │  Vault  │ →→→   │   ↓     │ →→→  │  User   │     │
│  │  Lock   │      │  Mint   │       │  Vault  │      │  Return │     │
│  └─────────┘      └─────────┘       └─────────┘      └─────────┘     │
│                                                                        │
├───────────────────────────────────────────────────────────────────────┤
│                     COLLATERAL PARAMETERS                              │
│                                                                        │
│  ETH-A:                          ETH-B:                                │
│  ├── Min Ratio: 145%             ├── Min Ratio: 130%                   │
│  ├── Stability Fee: 2%           ├── Stability Fee: 4%                 │
│  ├── Debt Ceiling: 2B DAI        ├── Debt Ceiling: 500M DAI            │
│  └── Liq Penalty: 13%            └── Liq Penalty: 13%                  │
│                                                                        │
├───────────────────────────────────────────────────────────────────────┤
│                        LIQUIDATION FLOW                                │
│                                                                        │
│  Ratio < Min ──→ Bark() ──→ Auction ──→ Winner ──→ DAI burned         │
│       ↓              ↓           ↓                                     │
│    Oracle      Liquidator    Keepers                                   │
│                              (bid DAI)                                 │
└───────────────────────────────────────────────────────────────────────┘
```

### 3.2 Implementación CDP

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title SimpleCDP
 * @notice Simplified CDP system (MakerDAO-style)
 */
contract SimpleCDP is ReentrancyGuard {
    // Stablecoin token
    IERC20 public stablecoin;

    // Oracle interface
    interface IOracle {
        function getPrice() external view returns (uint256);
    }
    IOracle public oracle;

    // CDP structure
    struct CDP {
        uint256 collateral;     // ETH deposited
        uint256 debt;           // Stablecoin minted
        uint256 lastAccrual;    // Last fee accrual timestamp
    }

    mapping(address => CDP) public cdps;

    // System parameters
    uint256 public constant MIN_COLLATERAL_RATIO = 150; // 150%
    uint256 public constant LIQUIDATION_RATIO = 120;    // 120%
    uint256 public constant STABILITY_FEE = 200;        // 2% annual (basis points)
    uint256 public constant LIQUIDATION_PENALTY = 1300; // 13%
    uint256 public constant DUST = 100e18;              // Minimum debt

    // System debt tracking
    uint256 public totalDebt;
    uint256 public debtCeiling = 1000000e18; // 1M stablecoin

    event CDPOpened(address indexed owner, uint256 collateral, uint256 debt);
    event CDPModified(address indexed owner, int256 collateralDelta, int256 debtDelta);
    event CDPLiquidated(address indexed owner, address indexed liquidator, uint256 debt, uint256 collateral);

    constructor(address _stablecoin, address _oracle) {
        stablecoin = IERC20(_stablecoin);
        oracle = IOracle(_oracle);
    }

    /**
     * @notice Open new CDP with ETH collateral
     */
    function openCDP(uint256 _mintAmount) external payable nonReentrant {
        require(msg.value > 0, "No collateral");
        require(_mintAmount >= DUST, "Below dust");

        CDP storage cdp = cdps[msg.sender];
        require(cdp.debt == 0, "CDP exists");

        // Check collateral ratio
        uint256 price = oracle.getPrice();
        uint256 collateralValue = (msg.value * price) / 1e18;
        uint256 ratio = (collateralValue * 100) / _mintAmount;
        require(ratio >= MIN_COLLATERAL_RATIO, "Below min ratio");

        // Check debt ceiling
        require(totalDebt + _mintAmount <= debtCeiling, "Debt ceiling");

        // Create CDP
        cdp.collateral = msg.value;
        cdp.debt = _mintAmount;
        cdp.lastAccrual = block.timestamp;

        totalDebt += _mintAmount;

        // Mint stablecoin
        IMintable(address(stablecoin)).mint(msg.sender, _mintAmount);

        emit CDPOpened(msg.sender, msg.value, _mintAmount);
    }

    /**
     * @notice Add collateral to existing CDP
     */
    function addCollateral() external payable nonReentrant {
        require(msg.value > 0, "No collateral");

        CDP storage cdp = cdps[msg.sender];
        require(cdp.debt > 0, "No CDP");

        cdp.collateral += msg.value;

        emit CDPModified(msg.sender, int256(msg.value), 0);
    }

    /**
     * @notice Generate more stablecoin from CDP
     */
    function generateDebt(uint256 _amount) external nonReentrant {
        CDP storage cdp = cdps[msg.sender];
        require(cdp.collateral > 0, "No CDP");

        // Accrue fees first
        _accrueFees(msg.sender);

        // Check ratio after generating
        uint256 price = oracle.getPrice();
        uint256 collateralValue = (cdp.collateral * price) / 1e18;
        uint256 newDebt = cdp.debt + _amount;
        uint256 ratio = (collateralValue * 100) / newDebt;
        require(ratio >= MIN_COLLATERAL_RATIO, "Below min ratio");

        // Check ceiling
        require(totalDebt + _amount <= debtCeiling, "Debt ceiling");

        cdp.debt = newDebt;
        totalDebt += _amount;

        IMintable(address(stablecoin)).mint(msg.sender, _amount);

        emit CDPModified(msg.sender, 0, int256(_amount));
    }

    /**
     * @notice Repay debt and optionally withdraw collateral
     */
    function repayDebt(uint256 _amount, uint256 _withdrawCollateral) external nonReentrant {
        CDP storage cdp = cdps[msg.sender];
        require(cdp.debt > 0, "No CDP");

        // Accrue fees
        _accrueFees(msg.sender);

        // Repay
        uint256 repayAmount = _amount > cdp.debt ? cdp.debt : _amount;

        // Burn stablecoin
        stablecoin.transferFrom(msg.sender, address(this), repayAmount);
        IBurnable(address(stablecoin)).burn(repayAmount);

        cdp.debt -= repayAmount;
        totalDebt -= repayAmount;

        // Withdraw collateral if requested
        if (_withdrawCollateral > 0) {
            require(_withdrawCollateral <= cdp.collateral, "Insufficient collateral");

            // Check ratio after withdrawal
            if (cdp.debt > 0) {
                uint256 price = oracle.getPrice();
                uint256 remainingCollateralValue = ((cdp.collateral - _withdrawCollateral) * price) / 1e18;
                uint256 ratio = (remainingCollateralValue * 100) / cdp.debt;
                require(ratio >= MIN_COLLATERAL_RATIO, "Below min ratio");
            }

            cdp.collateral -= _withdrawCollateral;
            payable(msg.sender).transfer(_withdrawCollateral);
        }

        // Clean up if fully repaid
        if (cdp.debt == 0) {
            if (cdp.collateral > 0) {
                uint256 remaining = cdp.collateral;
                cdp.collateral = 0;
                payable(msg.sender).transfer(remaining);
            }
        }

        emit CDPModified(msg.sender, -int256(_withdrawCollateral), -int256(repayAmount));
    }

    /**
     * @notice Liquidate undercollateralized CDP
     */
    function liquidate(address _owner) external nonReentrant {
        CDP storage cdp = cdps[_owner];
        require(cdp.debt > 0, "No CDP");

        // Accrue fees
        _accrueFees(_owner);

        // Check if liquidatable
        uint256 price = oracle.getPrice();
        uint256 collateralValue = (cdp.collateral * price) / 1e18;
        uint256 ratio = (collateralValue * 100) / cdp.debt;
        require(ratio < LIQUIDATION_RATIO, "Not liquidatable");

        uint256 debt = cdp.debt;
        uint256 collateral = cdp.collateral;

        // Calculate liquidation incentive
        // Liquidator pays debt, receives collateral + penalty
        uint256 debtValue = debt;
        uint256 incentivizedValue = (debtValue * (10000 + LIQUIDATION_PENALTY)) / 10000;

        // Collateral to give liquidator
        uint256 collateralToLiquidator = (incentivizedValue * 1e18) / price;
        collateralToLiquidator = collateralToLiquidator > collateral ? collateral : collateralToLiquidator;

        // Burn liquidator's stablecoin
        stablecoin.transferFrom(msg.sender, address(this), debt);
        IBurnable(address(stablecoin)).burn(debt);

        // Transfer collateral to liquidator
        payable(msg.sender).transfer(collateralToLiquidator);

        // Any remaining collateral goes back to owner
        uint256 remainingCollateral = collateral - collateralToLiquidator;
        if (remainingCollateral > 0) {
            payable(_owner).transfer(remainingCollateral);
        }

        // Clear CDP
        totalDebt -= debt;
        delete cdps[_owner];

        emit CDPLiquidated(_owner, msg.sender, debt, collateralToLiquidator);
    }

    /**
     * @notice Accrue stability fees
     */
    function _accrueFees(address _owner) internal {
        CDP storage cdp = cdps[_owner];

        if (cdp.lastAccrual == 0 || cdp.debt == 0) {
            cdp.lastAccrual = block.timestamp;
            return;
        }

        uint256 timeElapsed = block.timestamp - cdp.lastAccrual;

        // Simple interest (annual rate / seconds per year)
        uint256 feeAmount = (cdp.debt * STABILITY_FEE * timeElapsed) / (10000 * 365 days);

        cdp.debt += feeAmount;
        totalDebt += feeAmount;
        cdp.lastAccrual = block.timestamp;
    }

    /**
     * @notice Get current collateral ratio
     */
    function getCollateralRatio(address _owner) external view returns (uint256) {
        CDP memory cdp = cdps[_owner];
        if (cdp.debt == 0) return type(uint256).max;

        uint256 price = oracle.getPrice();
        uint256 collateralValue = (cdp.collateral * price) / 1e18;
        return (collateralValue * 100) / cdp.debt;
    }
}

interface IMintable {
    function mint(address to, uint256 amount) external;
}

interface IBurnable {
    function burn(uint256 amount) external;
}
```

---

## 4. ALGORITHMIC STABLECOINS

### 4.1 Rebase Mechanism (AMPL-style)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/**
 * @title RebaseStablecoin
 * @notice Elastic supply stablecoin that rebases to maintain peg
 */
contract RebaseStablecoin is ERC20 {
    // Target price (1 USD = 1e18)
    uint256 public constant TARGET_PRICE = 1e18;

    // Rebase lag (smoothing factor)
    uint256 public constant REBASE_LAG = 10;

    // Deviation threshold for rebase (5%)
    uint256 public constant DEVIATION_THRESHOLD = 5e16;

    // Rebase cooldown
    uint256 public constant REBASE_COOLDOWN = 24 hours;
    uint256 public lastRebase;

    // Gons: internal unit for accounting rebases
    uint256 private constant MAX_UINT256 = type(uint256).max;
    uint256 private constant INITIAL_GONS_PER_FRAGMENT = 10**24;

    uint256 private _gonsPerFragment = INITIAL_GONS_PER_FRAGMENT;
    uint256 private _totalGons;

    mapping(address => uint256) private _gonBalances;

    // Oracle
    address public oracle;

    event Rebase(uint256 indexed epoch, uint256 supplyDelta, uint256 newSupply);

    constructor() ERC20("Ampleforth", "AMPL") {
        // Initial supply
        uint256 initialSupply = 50_000_000e18;
        _totalGons = initialSupply * INITIAL_GONS_PER_FRAGMENT;
        _gonBalances[msg.sender] = _totalGons;

        emit Transfer(address(0), msg.sender, initialSupply);
    }

    /**
     * @notice Execute rebase based on oracle price
     */
    function rebase() external returns (uint256) {
        require(block.timestamp >= lastRebase + REBASE_COOLDOWN, "Cooldown");

        uint256 currentPrice = _getOraclePrice();

        // Calculate deviation from peg
        int256 deviation = int256(currentPrice) - int256(TARGET_PRICE);
        int256 deviationPercent = (deviation * 1e18) / int256(TARGET_PRICE);

        // Only rebase if deviation exceeds threshold
        if (uint256(deviationPercent > 0 ? deviationPercent : -deviationPercent) < DEVIATION_THRESHOLD) {
            return 0;
        }

        // Calculate supply adjustment
        // supplyDelta = totalSupply * deviation / lag
        int256 supplyDelta = (int256(totalSupply()) * deviationPercent) / int256(REBASE_LAG * 1e18);

        // Apply rebase
        if (supplyDelta < 0) {
            // Contraction
            _gonsPerFragment = (_gonsPerFragment * (totalSupply() + uint256(-supplyDelta))) / totalSupply();
        } else {
            // Expansion
            uint256 newGonsPerFragment = (_gonsPerFragment * totalSupply()) / (totalSupply() + uint256(supplyDelta));
            // Prevent overflow
            if (newGonsPerFragment > 0) {
                _gonsPerFragment = newGonsPerFragment;
            }
        }

        lastRebase = block.timestamp;

        emit Rebase(block.timestamp, supplyDelta > 0 ? uint256(supplyDelta) : uint256(-supplyDelta), totalSupply());

        return supplyDelta > 0 ? uint256(supplyDelta) : uint256(-supplyDelta);
    }

    /**
     * @notice Get total supply (dynamic based on gonsPerFragment)
     */
    function totalSupply() public view override returns (uint256) {
        return _totalGons / _gonsPerFragment;
    }

    /**
     * @notice Get balance (dynamic based on gonsPerFragment)
     */
    function balanceOf(address account) public view override returns (uint256) {
        return _gonBalances[account] / _gonsPerFragment;
    }

    /**
     * @notice Transfer (operates on gons internally)
     */
    function transfer(address to, uint256 amount) public override returns (bool) {
        uint256 gonValue = amount * _gonsPerFragment;

        _gonBalances[msg.sender] -= gonValue;
        _gonBalances[to] += gonValue;

        emit Transfer(msg.sender, to, amount);
        return true;
    }

    /**
     * @notice Get price from oracle
     */
    function _getOraclePrice() internal view returns (uint256) {
        // In production: call Chainlink or TWAP oracle
        // For demo: return mock price
        return TARGET_PRICE;
    }
}
```

### 4.2 Fractional Algorithmic (FRAX-style)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title FractionalStablecoin
 * @notice Partially collateralized stablecoin (FRAX-style)
 */
contract FractionalStablecoin is ReentrancyGuard {
    // Stablecoin token
    IERC20 public stablecoin;

    // Governance/Share token (FXS equivalent)
    IERC20 public shareToken;

    // Collateral token (USDC)
    IERC20 public collateral;

    // Collateral ratio (0-100%)
    uint256 public collateralRatio = 85; // 85%

    // Target price
    uint256 public constant TARGET_PRICE = 1e18;

    // Ratio adjustment parameters
    uint256 public constant RATIO_STEP = 25; // 0.25%
    uint256 public constant PRICE_BAND = 5e15; // 0.5% from peg

    // Pools
    uint256 public collateralPool;

    // Oracles
    address public stablecoinOracle;
    address public shareOracle;

    event Minted(address indexed user, uint256 stablecoinAmount, uint256 collateralUsed, uint256 sharesBurned);
    event Redeemed(address indexed user, uint256 stablecoinAmount, uint256 collateralReturned, uint256 sharesMinted);
    event CollateralRatioAdjusted(uint256 oldRatio, uint256 newRatio);

    /**
     * @notice Mint stablecoin using collateral + shares
     * @param _stablecoinAmount Amount of stablecoin to mint
     */
    function mint(uint256 _stablecoinAmount) external nonReentrant {
        // Calculate collateral needed
        uint256 collateralNeeded = (_stablecoinAmount * collateralRatio) / 100;

        // Calculate shares to burn (remaining value)
        uint256 shareValue = _stablecoinAmount - collateralNeeded;
        uint256 sharePrice = _getSharePrice();
        uint256 sharesToBurn = (shareValue * 1e18) / sharePrice;

        // Transfer collateral
        collateral.transferFrom(msg.sender, address(this), collateralNeeded);
        collateralPool += collateralNeeded;

        // Burn shares
        if (sharesToBurn > 0) {
            IBurnable(address(shareToken)).burnFrom(msg.sender, sharesToBurn);
        }

        // Mint stablecoin
        IMintable(address(stablecoin)).mint(msg.sender, _stablecoinAmount);

        emit Minted(msg.sender, _stablecoinAmount, collateralNeeded, sharesToBurn);
    }

    /**
     * @notice Redeem stablecoin for collateral + shares
     * @param _stablecoinAmount Amount of stablecoin to redeem
     */
    function redeem(uint256 _stablecoinAmount) external nonReentrant {
        // Burn stablecoin
        stablecoin.transferFrom(msg.sender, address(this), _stablecoinAmount);
        IBurnable(address(stablecoin)).burn(_stablecoinAmount);

        // Calculate collateral to return
        uint256 collateralReturn = (_stablecoinAmount * collateralRatio) / 100;
        require(collateralReturn <= collateralPool, "Insufficient collateral");

        // Calculate shares to mint
        uint256 shareValue = _stablecoinAmount - collateralReturn;
        uint256 sharePrice = _getSharePrice();
        uint256 sharesToMint = (shareValue * 1e18) / sharePrice;

        // Transfer collateral
        collateralPool -= collateralReturn;
        collateral.transfer(msg.sender, collateralReturn);

        // Mint shares
        if (sharesToMint > 0) {
            IMintable(address(shareToken)).mint(msg.sender, sharesToMint);
        }

        emit Redeemed(msg.sender, _stablecoinAmount, collateralReturn, sharesToMint);
    }

    /**
     * @notice Adjust collateral ratio based on stablecoin price
     * @dev Called periodically by keeper
     */
    function adjustCollateralRatio() external {
        uint256 stablecoinPrice = _getStablecoinPrice();

        uint256 oldRatio = collateralRatio;

        if (stablecoinPrice > TARGET_PRICE + PRICE_BAND) {
            // Price above peg - decrease collateral ratio
            if (collateralRatio > RATIO_STEP) {
                collateralRatio -= RATIO_STEP;
            }
        } else if (stablecoinPrice < TARGET_PRICE - PRICE_BAND) {
            // Price below peg - increase collateral ratio
            if (collateralRatio + RATIO_STEP <= 100) {
                collateralRatio += RATIO_STEP;
            }
        }

        if (oldRatio != collateralRatio) {
            emit CollateralRatioAdjusted(oldRatio, collateralRatio);
        }
    }

    /**
     * @notice Recollateralize - add collateral when under-collateralized
     * @dev Users get bonus shares for providing collateral
     */
    function recollateralize(uint256 _collateralAmount) external nonReentrant {
        // Check if under target ratio
        uint256 totalStablecoin = stablecoin.totalSupply();
        uint256 targetCollateral = (totalStablecoin * collateralRatio) / 100;

        require(collateralPool < targetCollateral, "Fully collateralized");

        uint256 deficit = targetCollateral - collateralPool;
        uint256 actualDeposit = _collateralAmount > deficit ? deficit : _collateralAmount;

        // Transfer collateral
        collateral.transferFrom(msg.sender, address(this), actualDeposit);
        collateralPool += actualDeposit;

        // Mint bonus shares (0.2% bonus)
        uint256 sharePrice = _getSharePrice();
        uint256 bonusValue = (actualDeposit * 20) / 10000;
        uint256 sharesToMint = ((actualDeposit + bonusValue) * 1e18) / sharePrice;

        IMintable(address(shareToken)).mint(msg.sender, sharesToMint);
    }

    /**
     * @notice Buyback - remove excess collateral
     * @dev Users can buy shares with excess collateral
     */
    function buyback(uint256 _shareAmount) external nonReentrant {
        // Check if over target ratio
        uint256 totalStablecoin = stablecoin.totalSupply();
        uint256 targetCollateral = (totalStablecoin * collateralRatio) / 100;

        require(collateralPool > targetCollateral, "Not over-collateralized");

        uint256 excess = collateralPool - targetCollateral;
        uint256 sharePrice = _getSharePrice();
        uint256 collateralValue = (_shareAmount * sharePrice) / 1e18;

        // Apply discount (0.2%)
        uint256 collateralToReturn = (collateralValue * 10020) / 10000;
        collateralToReturn = collateralToReturn > excess ? excess : collateralToReturn;

        // Burn shares
        IBurnable(address(shareToken)).burnFrom(msg.sender, _shareAmount);

        // Return collateral
        collateralPool -= collateralToReturn;
        collateral.transfer(msg.sender, collateralToReturn);
    }

    // Oracle functions (simplified)
    function _getStablecoinPrice() internal view returns (uint256) {
        // In production: Chainlink/TWAP oracle
        return TARGET_PRICE;
    }

    function _getSharePrice() internal view returns (uint256) {
        // In production: Chainlink/TWAP oracle
        return 10e18; // $10 per share token
    }
}
```

---

## 5. CURVE STABLECOIN (crvUSD)

### 5.1 LLAMMA (Lending-Liquidating AMM Algorithm)

```
LLAMMA ARCHITECTURE
═══════════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────────────┐
│                    SOFT LIQUIDATION MECHANISM                           │
│                                                                         │
│  Traditional CDP:                                                       │
│  ├── Price drops → Ratio < Min → FULL LIQUIDATION                      │
│  └── User loses entire position + penalty                               │
│                                                                         │
│  LLAMMA (Curve):                                                        │
│  ├── Price drops → Collateral gradually converted to stablecoin        │
│  ├── Price rises → Stablecoin converted back to collateral             │
│  └── "Soft liquidation" = continuous rebalancing                        │
│                                                                         │
├────────────────────────────────────────────────────────────────────────┤
│                         BAND SYSTEM                                     │
│                                                                         │
│  Price Bands (N bands, e.g., 50):                                      │
│                                                                         │
│  Band 49: $2000-2020  [ETH only]          ← Current price above        │
│  Band 48: $1980-2000  [ETH only]                                       │
│  Band 47: $1960-1980  [Partial ETH/USD]   ← Soft liquidation zone      │
│  Band 46: $1940-1960  [Partial ETH/USD]                                │
│  Band 45: $1920-1940  [USD only]          ← Full conversion            │
│  ...                                                                    │
│                                                                         │
│  As price falls through bands:                                          │
│  ETH ──────────────────────────────────────────────────→ crvUSD        │
│                                                                         │
│  As price rises through bands:                                          │
│  crvUSD ←──────────────────────────────────────────────── ETH          │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Simplified LLAMMA Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title SimpleLLAMMA
 * @notice Simplified LLAMMA-style soft liquidation AMM
 */
contract SimpleLLAMMA {
    // Number of bands
    uint256 public constant N_BANDS = 50;

    // Band width (1% between bands)
    uint256 public constant BAND_WIDTH = 100; // basis points

    // Collateral and stablecoin
    address public collateral; // ETH/WETH
    address public stablecoin; // crvUSD

    // User position
    struct Position {
        uint256 collateralAmount;
        uint256 debtAmount;
        uint256 topBand;    // Highest band with collateral
        uint256 bottomBand; // Lowest band with collateral
    }

    mapping(address => Position) public positions;

    // Band state
    struct Band {
        uint256 collateralAmount;  // ETH in this band
        uint256 stablecoinAmount;  // crvUSD in this band
    }

    mapping(uint256 => Band) public bands;

    // Current oracle price
    uint256 public oraclePrice;

    // Active band (where current price falls)
    uint256 public activeBand;

    /**
     * @notice Create loan with collateral
     * @param _collateral Amount of ETH collateral
     * @param _debt Amount of crvUSD to borrow
     * @param _topBand Top band to start collateral
     * @param _numBands Number of bands to spread collateral
     */
    function createLoan(
        uint256 _collateral,
        uint256 _debt,
        uint256 _topBand,
        uint256 _numBands
    ) external payable {
        require(msg.value == _collateral, "Wrong collateral");
        require(_numBands >= 4, "Min 4 bands");
        require(_topBand + _numBands <= N_BANDS, "Invalid bands");

        Position storage pos = positions[msg.sender];
        require(pos.collateralAmount == 0, "Position exists");

        // Distribute collateral across bands
        uint256 perBand = _collateral / _numBands;

        for (uint256 i = 0; i < _numBands; i++) {
            uint256 bandId = _topBand + i;
            bands[bandId].collateralAmount += perBand;
        }

        // Store position
        pos.collateralAmount = _collateral;
        pos.debtAmount = _debt;
        pos.topBand = _topBand;
        pos.bottomBand = _topBand + _numBands - 1;

        // Mint stablecoin
        IMintable(stablecoin).mint(msg.sender, _debt);
    }

    /**
     * @notice Update bands based on price movement
     * @dev Called by keepers when price changes significantly
     */
    function updateBands(uint256 _newPrice) external {
        uint256 oldActiveBand = activeBand;
        activeBand = _priceToband(_newPrice);
        oraclePrice = _newPrice;

        // If price moved up (bands decrease)
        if (activeBand < oldActiveBand) {
            // Convert stablecoin back to collateral in affected bands
            for (uint256 i = activeBand; i < oldActiveBand; i++) {
                _convertToCollateral(i);
            }
        }
        // If price moved down (bands increase)
        else if (activeBand > oldActiveBand) {
            // Convert collateral to stablecoin in affected bands
            for (uint256 i = oldActiveBand; i < activeBand; i++) {
                _convertToStablecoin(i);
            }
        }
    }

    /**
     * @notice Convert collateral to stablecoin in a band (soft liquidation)
     */
    function _convertToStablecoin(uint256 _band) internal {
        Band storage band = bands[_band];

        if (band.collateralAmount == 0) return;

        // Get band price range
        (uint256 lowPrice, uint256 highPrice) = _getBandPrices(_band);
        uint256 midPrice = (lowPrice + highPrice) / 2;

        // Convert all collateral to stablecoin at mid price
        uint256 stablecoinValue = (band.collateralAmount * midPrice) / 1e18;

        band.stablecoinAmount += stablecoinValue;
        band.collateralAmount = 0;

        // In real implementation: swap through AMM
    }

    /**
     * @notice Convert stablecoin back to collateral (de-liquidation)
     */
    function _convertToCollateral(uint256 _band) internal {
        Band storage band = bands[_band];

        if (band.stablecoinAmount == 0) return;

        (uint256 lowPrice, uint256 highPrice) = _getBandPrices(_band);
        uint256 midPrice = (lowPrice + highPrice) / 2;

        // Convert stablecoin back to collateral
        uint256 collateralAmount = (band.stablecoinAmount * 1e18) / midPrice;

        band.collateralAmount += collateralAmount;
        band.stablecoinAmount = 0;
    }

    /**
     * @notice Calculate band from price
     */
    function _priceToband(uint256 _price) internal pure returns (uint256) {
        // Simplified: assume base price is $1000, 1% per band
        // Band 0 = $1000, Band 50 = $1500 (roughly)
        uint256 basePrice = 1000e18;

        if (_price <= basePrice) return 0;

        uint256 ratio = (_price * 10000) / basePrice;
        uint256 band = (ratio - 10000) / BAND_WIDTH;

        return band >= N_BANDS ? N_BANDS - 1 : band;
    }

    /**
     * @notice Get price range for a band
     */
    function _getBandPrices(uint256 _band) internal pure returns (uint256 low, uint256 high) {
        uint256 basePrice = 1000e18;

        low = (basePrice * (10000 + _band * BAND_WIDTH)) / 10000;
        high = (basePrice * (10000 + (_band + 1) * BAND_WIDTH)) / 10000;
    }

    /**
     * @notice Get user's health factor
     */
    function getHealth(address _user) external view returns (uint256) {
        Position memory pos = positions[_user];
        if (pos.debtAmount == 0) return type(uint256).max;

        // Calculate total collateral value across bands
        uint256 totalValue = 0;

        for (uint256 i = pos.topBand; i <= pos.bottomBand; i++) {
            (uint256 lowPrice, ) = _getBandPrices(i);

            totalValue += (bands[i].collateralAmount * lowPrice) / 1e18;
            totalValue += bands[i].stablecoinAmount;
        }

        // Health = collateral value / debt
        return (totalValue * 100) / pos.debtAmount;
    }
}
```

---

## 6. STABLECOIN COMPARISON

```
STABLECOIN DEEP COMPARISON
═══════════════════════════════════════════════════════════════════════

┌─────────────┬───────────┬───────────┬───────────┬───────────┬──────────┐
│ Feature     │ USDC      │ DAI       │ FRAX      │ crvUSD    │ LUSD     │
├─────────────┼───────────┼───────────┼───────────┼───────────┼──────────┤
│ Type        │ Fiat      │ CDP       │ Hybrid    │ CDP+AMM   │ CDP      │
│ Backing     │ 100% USD  │ >150%     │ 85-100%   │ >100%     │ >110%    │
│ Governance  │ Circle    │ MKR DAO   │ FXS DAO   │ veCRV     │ None     │
│ Censorship  │ Yes       │ Partial   │ Partial   │ No        │ No       │
│ Oracle      │ N/A       │ Chainlink │ TWAP      │ Internal  │ Chainlink│
│ Peg Range   │ Perfect   │ $0.99-1.01│ $0.99-1.01│ $0.99-1.01│ $1.00+   │
├─────────────┼───────────┼───────────┼───────────┼───────────┼──────────┤
│ Yield       │ Via CeFi  │ DSR 5%    │ sfrxETH   │ Lending   │ Stability│
│ Supply Cap  │ No limit  │ Debt ceil │ Dynamic   │ Per vault │ No limit │
│ Liquidation │ N/A       │ 13% fee   │ Variable  │ Soft liq  │ <10%     │
│ Risk Level  │ Low       │ Medium    │ Medium    │ Medium    │ Low      │
└─────────────┴───────────┴───────────┴───────────┴───────────┴──────────┘

MARKET CAPS (Dec 2024):
1. USDT    ~$92B  (Tether - controversial reserves)
2. USDC    ~$25B  (Circle - regulated, transparent)
3. DAI     ~$5B   (MakerDAO - largest decentralized)
4. FRAX    ~$650M (Frax Finance - innovative hybrid)
5. LUSD    ~$500M (Liquity - most decentralized)
6. crvUSD  ~$150M (Curve - novel LLAMMA mechanism)

DEPEGGING EVENTS:
┌──────────────┬─────────────────────────────────────────────────────────┐
│ UST (2022)   │ Death spiral - algo stablecoin collapse                 │
│              │ Lost $40B+ market cap in days                           │
├──────────────┼─────────────────────────────────────────────────────────┤
│ USDC (2023)  │ Briefly depegged to $0.87 during SVB collapse          │
│              │ Recovered after FDIC intervention                       │
├──────────────┼─────────────────────────────────────────────────────────┤
│ DAI (2020)   │ Black Thursday - liquidation cascade                    │
│              │ Protocol lost $4M, reformed auction system              │
└──────────────┴─────────────────────────────────────────────────────────┘
```

---

## 7. RISK ANALYSIS

```yaml
STABLECOIN RISK FRAMEWORK:
══════════════════════════════════════════════════════════════════════════

FIAT-BACKED:
  Risks:
    - Counterparty Risk:
        Description: Issuer insolvency or fraud
        Mitigation: Regular attestations, insurance
        Example: Tether reserve composition questions

    - Censorship Risk:
        Description: Blacklisting addresses
        Mitigation: Use decentralized alternatives
        Example: USDC blacklisted Tornado Cash addresses

    - Regulatory Risk:
        Description: Government restrictions
        Mitigation: Geographic diversification
        Example: BUSD ordered to stop minting

CDP-BASED:
  Risks:
    - Oracle Manipulation:
        Description: Price feed attacks
        Mitigation: Multiple sources, TWAP, delays
        Example: Various flash loan oracle attacks

    - Liquidation Cascade:
        Description: Mass liquidations in volatility
        Mitigation: Keeper incentives, gradual liquidation
        Example: MakerDAO Black Thursday 2020

    - Bad Debt:
        Description: Underwater positions
        Mitigation: Insurance fund, governance backstop
        Example: Various smaller protocols

ALGORITHMIC:
  Risks:
    - Death Spiral:
        Description: Bank run + depegging feedback loop
        Mitigation: Partial collateralization, circuit breakers
        Example: UST/LUNA collapse May 2022

    - Governance Attacks:
        Description: Manipulation of parameters
        Mitigation: Timelocks, multi-sig, emergency brakes
        Example: Beanstalk governance exploit

SMART CONTRACT:
  Risks:
    - Code Vulnerabilities:
        Description: Bugs in stablecoin logic
        Mitigation: Audits, formal verification, bug bounties
        Example: Various DeFi hacks

    - Composability Risk:
        Description: Failures in integrated protocols
        Mitigation: Protocol diversification, monitoring
        Example: Cascading liquidations across DeFi
```

---

## FIRMA

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  NEURONA: STABLECOINS & CDP SYSTEMS                                            ║
║  Dominio: C40004 - Stablecoin Architecture                                     ║
║  Versión: 1.0.0                                                                ║
║  Última actualización: 2024-12-29                                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```
