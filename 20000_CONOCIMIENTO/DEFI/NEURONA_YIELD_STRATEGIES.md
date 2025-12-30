# NEURONA: YIELD STRATEGIES & AGGREGATORS
## C40005 - DeFi Yield Optimization

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  CIPHER NEURONA: YIELD STRATEGIES                                              ║
║  Dominio: Yield Farming, Aggregators, Auto-compounding, Vaults                 ║
║  Estado: ACTIVA                                                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. YIELD FARMING FUNDAMENTALS

### 1.1 Yield Sources

```
YIELD SOURCE TAXONOMY
═══════════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────────────┐
│                      YIELD CATEGORIES                                   │
├────────────────┬───────────────────────────────────────────────────────┤
│ LENDING        │ Supply assets → Earn interest from borrowers          │
│                │ Examples: Aave, Compound, Morpho                       │
│                │ APY Range: 1-15% (depends on utilization)              │
├────────────────┼───────────────────────────────────────────────────────┤
│ LP FEES        │ Provide liquidity → Earn swap fees                    │
│                │ Examples: Uniswap, Curve, Balancer                     │
│                │ APY Range: 2-50%+ (depends on volume)                  │
├────────────────┼───────────────────────────────────────────────────────┤
│ LIQUIDITY      │ Stake LP tokens → Earn protocol tokens                │
│ MINING         │ Examples: Sushiswap rewards, Curve gauges             │
│                │ APY Range: 5-100%+ (often inflationary)                │
├────────────────┼───────────────────────────────────────────────────────┤
│ STAKING        │ Stake governance tokens → Earn revenue share          │
│                │ Examples: veCRV, xSUSHI, GMX staking                   │
│                │ APY Range: 5-30%                                       │
├────────────────┼───────────────────────────────────────────────────────┤
│ REAL YIELD     │ Protocol revenue distributed to stakers               │
│                │ Examples: GMX (30% fees), dYdX                         │
│                │ APY Range: 10-40% (sustainable)                        │
├────────────────┼───────────────────────────────────────────────────────┤
│ AIRDROPS       │ Use protocol → Receive governance tokens              │
│                │ Examples: Arbitrum, Optimism, LayerZero                │
│                │ Value: Highly variable                                 │
└────────────────┴───────────────────────────────────────────────────────┘

YIELD SUSTAINABILITY SPECTRUM:
Unsustainable ─────────────────────────────────→ Sustainable

High Emission │ Moderate     │ Fee Share    │ Real Yield
Ponzinomics   │ Incentives   │ Trading Fees │ Protocol Rev
   100%+ APY  │ 20-50% APY   │ 5-20% APY    │ 5-15% APY
```

### 1.2 APY vs APR Calculation

```python
"""
Yield Calculation Utilities
"""

import math
from typing import Tuple

def apr_to_apy(apr: float, compounds_per_year: int = 365) -> float:
    """
    Convert APR to APY
    APY = (1 + APR/n)^n - 1
    """
    return (1 + apr / compounds_per_year) ** compounds_per_year - 1

def apy_to_apr(apy: float, compounds_per_year: int = 365) -> float:
    """
    Convert APY to APR
    APR = n * ((1 + APY)^(1/n) - 1)
    """
    return compounds_per_year * ((1 + apy) ** (1 / compounds_per_year) - 1)

def calculate_lp_apy(
    daily_volume: float,
    total_liquidity: float,
    fee_tier: float = 0.003  # 0.3%
) -> float:
    """
    Calculate LP APY from trading fees
    """
    daily_fees = daily_volume * fee_tier
    daily_yield = daily_fees / total_liquidity
    apy = apr_to_apy(daily_yield * 365)
    return apy

def calculate_farming_apy(
    reward_per_day: float,
    reward_token_price: float,
    total_staked_value: float
) -> float:
    """
    Calculate farming APY from emissions
    """
    daily_reward_value = reward_per_day * reward_token_price
    daily_yield = daily_reward_value / total_staked_value
    apr = daily_yield * 365
    return apr_to_apy(apr)

def compound_yield(
    principal: float,
    apy: float,
    days: int,
    compounds_per_day: int = 1
) -> Tuple[float, float]:
    """
    Calculate compounded yield over period

    Returns:
        final_value: Value after compounding
        total_yield: Total yield earned
    """
    rate_per_compound = (1 + apy) ** (1 / (365 * compounds_per_day)) - 1
    total_compounds = days * compounds_per_day

    final_value = principal * (1 + rate_per_compound) ** total_compounds
    total_yield = final_value - principal

    return final_value, total_yield


# Real yield calculation
def calculate_real_yield(
    protocol_revenue_daily: float,
    staker_share: float,  # e.g., 0.30 for 30%
    total_staked_tokens: float,
    token_price: float
) -> float:
    """
    Calculate real yield APY (fee-based, sustainable)
    """
    daily_revenue_to_stakers = protocol_revenue_daily * staker_share
    daily_yield_per_token = daily_revenue_to_stakers / total_staked_tokens
    daily_yield_value = daily_yield_per_token / token_price
    apr = daily_yield_value * 365
    return apr_to_apy(apr)


# Example usage
if __name__ == "__main__":
    # Example: Curve 3pool
    print("=== Curve 3pool Analysis ===")
    lp_apy = calculate_lp_apy(
        daily_volume=50_000_000,    # $50M daily volume
        total_liquidity=500_000_000, # $500M TVL
        fee_tier=0.0001              # 0.01% fee
    )
    print(f"LP Fee APY: {lp_apy:.2%}")

    # Add CRV rewards
    farming_apy = calculate_farming_apy(
        reward_per_day=100_000,      # 100K CRV/day
        reward_token_price=0.50,     # $0.50 per CRV
        total_staked_value=500_000_000
    )
    print(f"CRV Rewards APY: {farming_apy:.2%}")
    print(f"Total APY: {lp_apy + farming_apy:.2%}")

    # GMX Real Yield
    print("\n=== GMX Real Yield ===")
    gmx_apy = calculate_real_yield(
        protocol_revenue_daily=500_000,  # $500K/day fees
        staker_share=0.30,                # 30% to stakers
        total_staked_tokens=8_000_000,    # 8M GMX staked
        token_price=40                     # $40 per GMX
    )
    print(f"GMX Staking APY: {gmx_apy:.2%}")
```

---

## 2. YIELD AGGREGATORS

### 2.1 Yearn Finance Architecture

```
YEARN VAULT ARCHITECTURE
═══════════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────────────┐
│                         YEARN V3 VAULT                                  │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        yVault (ERC-4626)                         │   │
│  │  ├── deposit(assets) → mint shares                               │   │
│  │  ├── withdraw(shares) → return assets                            │   │
│  │  ├── pricePerShare = totalAssets / totalShares                   │   │
│  │  └── Automated strategy execution                                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    STRATEGY ALLOCATION                           │   │
│  │                                                                   │   │
│  │  Strategy A (40%) ───→ Aave lending                              │   │
│  │  Strategy B (30%) ───→ Compound lending                          │   │
│  │  Strategy C (20%) ───→ Curve LP + gauge                          │   │
│  │  Strategy D (10%) ───→ Convex boosted                            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  HARVEST FLOW:                                                          │
│  1. Keeper triggers harvest()                                           │
│  2. Strategy claims rewards (CRV, COMP, etc.)                          │
│  3. Swap rewards to vault asset                                        │
│  4. Reinvest or report profit                                          │
│  5. Update pricePerShare                                               │
│                                                                         │
│  FEES:                                                                  │
│  ├── Management Fee: 2% annual                                         │
│  ├── Performance Fee: 20% of profits                                   │
│  └── Strategist Fee: 10% of performance fee                            │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.2 ERC-4626 Vault Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/extensions/ERC4626.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title YieldVault
 * @notice ERC-4626 compliant yield aggregator vault
 */
contract YieldVault is ERC4626, ReentrancyGuard {
    using SafeERC20 for IERC20;

    // Strategy interface
    interface IStrategy {
        function deposit(uint256 amount) external;
        function withdraw(uint256 amount) external returns (uint256);
        function harvest() external returns (uint256);
        function totalAssets() external view returns (uint256);
        function estimatedAPY() external view returns (uint256);
    }

    // Active strategies
    struct StrategyConfig {
        IStrategy strategy;
        uint256 allocation;      // Basis points (10000 = 100%)
        uint256 lastReport;
        uint256 totalGain;
        uint256 totalLoss;
        bool active;
    }

    StrategyConfig[] public strategies;

    // Fees (basis points)
    uint256 public managementFee = 200;    // 2%
    uint256 public performanceFee = 2000;  // 20%

    // Fee recipients
    address public treasury;
    address public strategist;

    // Limits
    uint256 public depositLimit;

    // Keeper
    address public keeper;

    // Events
    event StrategyAdded(address indexed strategy, uint256 allocation);
    event StrategyRevoked(address indexed strategy);
    event Harvested(address indexed strategy, uint256 profit, uint256 loss);

    constructor(
        IERC20 _asset,
        string memory _name,
        string memory _symbol
    ) ERC4626(_asset) ERC20(_name, _symbol) {
        treasury = msg.sender;
        strategist = msg.sender;
        keeper = msg.sender;
        depositLimit = type(uint256).max;
    }

    /**
     * @notice Add new strategy
     */
    function addStrategy(
        address _strategy,
        uint256 _allocation
    ) external onlyOwner {
        require(_getTotalAllocation() + _allocation <= 10000, "Over allocated");

        strategies.push(StrategyConfig({
            strategy: IStrategy(_strategy),
            allocation: _allocation,
            lastReport: block.timestamp,
            totalGain: 0,
            totalLoss: 0,
            active: true
        }));

        // Approve strategy to pull assets
        IERC20(asset()).approve(_strategy, type(uint256).max);

        emit StrategyAdded(_strategy, _allocation);
    }

    /**
     * @notice Harvest all strategies
     */
    function harvest() external onlyKeeper nonReentrant {
        uint256 totalProfit = 0;
        uint256 totalLoss = 0;

        for (uint256 i = 0; i < strategies.length; i++) {
            if (!strategies[i].active) continue;

            uint256 profit = strategies[i].strategy.harvest();

            if (profit > 0) {
                totalProfit += profit;
                strategies[i].totalGain += profit;

                emit Harvested(address(strategies[i].strategy), profit, 0);
            }

            strategies[i].lastReport = block.timestamp;
        }

        // Take performance fee
        if (totalProfit > 0) {
            uint256 fee = (totalProfit * performanceFee) / 10000;
            _transferFee(fee);
        }
    }

    /**
     * @notice Rebalance assets across strategies
     */
    function rebalance() external onlyKeeper nonReentrant {
        uint256 totalBalance = totalAssets();

        for (uint256 i = 0; i < strategies.length; i++) {
            if (!strategies[i].active) continue;

            uint256 targetAmount = (totalBalance * strategies[i].allocation) / 10000;
            uint256 currentAmount = strategies[i].strategy.totalAssets();

            if (currentAmount > targetAmount) {
                // Withdraw excess
                uint256 excess = currentAmount - targetAmount;
                strategies[i].strategy.withdraw(excess);
            } else if (currentAmount < targetAmount) {
                // Deposit more
                uint256 deficit = targetAmount - currentAmount;
                uint256 available = IERC20(asset()).balanceOf(address(this));
                uint256 toDeposit = deficit > available ? available : deficit;

                if (toDeposit > 0) {
                    strategies[i].strategy.deposit(toDeposit);
                }
            }
        }
    }

    /**
     * @notice Get total assets including strategy balances
     */
    function totalAssets() public view override returns (uint256) {
        uint256 total = IERC20(asset()).balanceOf(address(this));

        for (uint256 i = 0; i < strategies.length; i++) {
            if (strategies[i].active) {
                total += strategies[i].strategy.totalAssets();
            }
        }

        return total;
    }

    /**
     * @notice Deposit with strategy allocation
     */
    function _deposit(
        address caller,
        address receiver,
        uint256 assets,
        uint256 shares
    ) internal virtual override {
        super._deposit(caller, receiver, assets, shares);

        // Allocate to strategies
        _allocateToStrategies(assets);
    }

    /**
     * @notice Withdraw from strategies if needed
     */
    function _withdraw(
        address caller,
        address receiver,
        address owner,
        uint256 assets,
        uint256 shares
    ) internal virtual override {
        // First check vault balance
        uint256 vaultBalance = IERC20(asset()).balanceOf(address(this));

        if (vaultBalance < assets) {
            // Need to withdraw from strategies
            uint256 needed = assets - vaultBalance;
            _withdrawFromStrategies(needed);
        }

        super._withdraw(caller, receiver, owner, assets, shares);
    }

    /**
     * @notice Allocate assets to strategies based on allocation
     */
    function _allocateToStrategies(uint256 _amount) internal {
        for (uint256 i = 0; i < strategies.length; i++) {
            if (!strategies[i].active) continue;

            uint256 toDeposit = (_amount * strategies[i].allocation) / 10000;
            if (toDeposit > 0) {
                strategies[i].strategy.deposit(toDeposit);
            }
        }
    }

    /**
     * @notice Withdraw from strategies proportionally
     */
    function _withdrawFromStrategies(uint256 _amount) internal {
        uint256 totalStrategyAssets = totalAssets() - IERC20(asset()).balanceOf(address(this));
        if (totalStrategyAssets == 0) return;

        for (uint256 i = 0; i < strategies.length; i++) {
            if (!strategies[i].active) continue;

            uint256 strategyAssets = strategies[i].strategy.totalAssets();
            uint256 toWithdraw = (_amount * strategyAssets) / totalStrategyAssets;

            if (toWithdraw > 0) {
                strategies[i].strategy.withdraw(toWithdraw);
            }
        }
    }

    /**
     * @notice Transfer fees to recipients
     */
    function _transferFee(uint256 _fee) internal {
        uint256 treasuryFee = (_fee * 90) / 100;  // 90% to treasury
        uint256 strategistFee = _fee - treasuryFee;

        IERC20(asset()).safeTransfer(treasury, treasuryFee);
        IERC20(asset()).safeTransfer(strategist, strategistFee);
    }

    function _getTotalAllocation() internal view returns (uint256) {
        uint256 total = 0;
        for (uint256 i = 0; i < strategies.length; i++) {
            if (strategies[i].active) {
                total += strategies[i].allocation;
            }
        }
        return total;
    }

    modifier onlyOwner() {
        require(msg.sender == treasury, "Only owner");
        _;
    }

    modifier onlyKeeper() {
        require(msg.sender == keeper || msg.sender == treasury, "Only keeper");
        _;
    }
}
```

### 2.3 Strategy Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/**
 * @title AaveStrategy
 * @notice Strategy that deposits into Aave for yield
 */
contract AaveStrategy {
    using SafeERC20 for IERC20;

    // Vault that owns this strategy
    address public vault;

    // Underlying asset
    IERC20 public asset;

    // Aave aToken (receipt token)
    IERC20 public aToken;

    // Aave lending pool
    interface ILendingPool {
        function deposit(address asset, uint256 amount, address onBehalfOf, uint16 referralCode) external;
        function withdraw(address asset, uint256 amount, address to) external returns (uint256);
    }
    ILendingPool public lendingPool;

    // Aave incentives controller (for claiming rewards)
    interface IIncentivesController {
        function claimRewards(address[] calldata assets, uint256 amount, address to) external returns (uint256);
        function getRewardsBalance(address[] calldata assets, address user) external view returns (uint256);
    }
    IIncentivesController public incentivesController;

    // Reward token (e.g., AAVE)
    IERC20 public rewardToken;

    // DEX router for swapping rewards
    address public dexRouter;

    constructor(
        address _vault,
        address _asset,
        address _aToken,
        address _lendingPool,
        address _incentivesController,
        address _rewardToken,
        address _dexRouter
    ) {
        vault = _vault;
        asset = IERC20(_asset);
        aToken = IERC20(_aToken);
        lendingPool = ILendingPool(_lendingPool);
        incentivesController = IIncentivesController(_incentivesController);
        rewardToken = IERC20(_rewardToken);
        dexRouter = _dexRouter;

        // Approve lending pool
        asset.approve(_lendingPool, type(uint256).max);
    }

    /**
     * @notice Deposit assets into Aave
     */
    function deposit(uint256 _amount) external onlyVault {
        asset.safeTransferFrom(vault, address(this), _amount);
        lendingPool.deposit(address(asset), _amount, address(this), 0);
    }

    /**
     * @notice Withdraw assets from Aave
     */
    function withdraw(uint256 _amount) external onlyVault returns (uint256) {
        uint256 withdrawn = lendingPool.withdraw(address(asset), _amount, vault);
        return withdrawn;
    }

    /**
     * @notice Harvest rewards and compound
     */
    function harvest() external onlyVault returns (uint256 profit) {
        // Claim AAVE rewards
        address[] memory assets = new address[](1);
        assets[0] = address(aToken);

        uint256 pending = incentivesController.getRewardsBalance(assets, address(this));

        if (pending > 0) {
            incentivesController.claimRewards(assets, pending, address(this));

            // Swap rewards to underlying asset
            uint256 rewardBalance = rewardToken.balanceOf(address(this));
            if (rewardBalance > 0) {
                profit = _swapRewardsToAsset(rewardBalance);

                // Redeposit profit
                if (profit > 0) {
                    lendingPool.deposit(address(asset), profit, address(this), 0);
                }
            }
        }

        return profit;
    }

    /**
     * @notice Get total assets in strategy
     */
    function totalAssets() external view returns (uint256) {
        return aToken.balanceOf(address(this));
    }

    /**
     * @notice Estimated APY from Aave
     */
    function estimatedAPY() external pure returns (uint256) {
        // In production: read from Aave data provider
        return 500; // 5% in basis points
    }

    /**
     * @notice Swap rewards to underlying asset
     */
    function _swapRewardsToAsset(uint256 _amount) internal returns (uint256) {
        // Simplified: In production use actual DEX
        // For demo purposes, assume 1:1 swap

        rewardToken.approve(dexRouter, _amount);

        // ... DEX swap logic ...

        return asset.balanceOf(address(this));
    }

    modifier onlyVault() {
        require(msg.sender == vault, "Only vault");
        _;
    }
}
```

---

## 3. AUTO-COMPOUNDING

### 3.1 Convex/Concentrator Style

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title AutoCompounder
 * @notice Auto-compounds LP rewards back into LP position
 */
contract AutoCompounder {
    // LP token being compounded
    address public lpToken;

    // Reward tokens
    address[] public rewardTokens;

    // DEX router
    address public dexRouter;

    // Underlying tokens of LP
    address public token0;
    address public token1;

    // AMM router for adding liquidity
    address public ammRouter;

    // Compound interval
    uint256 public compoundInterval = 12 hours;
    uint256 public lastCompound;

    // User shares
    mapping(address => uint256) public shares;
    uint256 public totalShares;

    // Accrued rewards
    uint256 public accRewardPerShare;

    event Compounded(uint256 lpAdded, uint256 timestamp);
    event Deposited(address indexed user, uint256 amount, uint256 shares);
    event Withdrawn(address indexed user, uint256 shares, uint256 amount);

    /**
     * @notice Deposit LP tokens
     */
    function deposit(uint256 _amount) external {
        // Update rewards first
        _updateRewards();

        // Calculate shares
        uint256 sharesToMint;
        if (totalShares == 0) {
            sharesToMint = _amount;
        } else {
            sharesToMint = (_amount * totalShares) / _totalLPBalance();
        }

        // Transfer LP
        IERC20(lpToken).transferFrom(msg.sender, address(this), _amount);

        // Stake in farm
        _stake(_amount);

        // Mint shares
        shares[msg.sender] += sharesToMint;
        totalShares += sharesToMint;

        emit Deposited(msg.sender, _amount, sharesToMint);
    }

    /**
     * @notice Withdraw LP tokens
     */
    function withdraw(uint256 _shares) external {
        require(shares[msg.sender] >= _shares, "Insufficient shares");

        // Update rewards first
        _updateRewards();

        // Calculate LP to return
        uint256 lpAmount = (_shares * _totalLPBalance()) / totalShares;

        // Burn shares
        shares[msg.sender] -= _shares;
        totalShares -= _shares;

        // Unstake
        _unstake(lpAmount);

        // Transfer LP
        IERC20(lpToken).transfer(msg.sender, lpAmount);

        emit Withdrawn(msg.sender, _shares, lpAmount);
    }

    /**
     * @notice Compound rewards back into LP
     */
    function compound() external {
        require(block.timestamp >= lastCompound + compoundInterval, "Too soon");

        // Claim all rewards
        _claimRewards();

        // Swap rewards to underlying tokens
        uint256 token0Balance = 0;
        uint256 token1Balance = 0;

        for (uint256 i = 0; i < rewardTokens.length; i++) {
            uint256 balance = IERC20(rewardTokens[i]).balanceOf(address(this));
            if (balance > 0) {
                // Swap half to token0, half to token1
                (uint256 t0, uint256 t1) = _swapRewardToUnderlying(rewardTokens[i], balance);
                token0Balance += t0;
                token1Balance += t1;
            }
        }

        // Add liquidity
        uint256 lpAdded = 0;
        if (token0Balance > 0 && token1Balance > 0) {
            lpAdded = _addLiquidity(token0Balance, token1Balance);

            // Stake new LP
            _stake(lpAdded);
        }

        lastCompound = block.timestamp;

        emit Compounded(lpAdded, block.timestamp);
    }

    /**
     * @notice Get user's LP balance
     */
    function balanceOf(address _user) external view returns (uint256) {
        if (totalShares == 0) return 0;
        return (shares[_user] * _totalLPBalance()) / totalShares;
    }

    /**
     * @notice Total LP balance (staked + pending)
     */
    function _totalLPBalance() internal view returns (uint256) {
        return _stakedBalance() + IERC20(lpToken).balanceOf(address(this));
    }

    // Internal farm interaction functions (implement based on specific farm)
    function _stake(uint256 _amount) internal virtual {}
    function _unstake(uint256 _amount) internal virtual {}
    function _claimRewards() internal virtual {}
    function _stakedBalance() internal view virtual returns (uint256) {}
    function _updateRewards() internal virtual {}

    /**
     * @notice Swap reward token to underlying LP tokens
     */
    function _swapRewardToUnderlying(
        address _reward,
        uint256 _amount
    ) internal returns (uint256 t0Amount, uint256 t1Amount) {
        uint256 halfAmount = _amount / 2;

        // Swap half to token0
        t0Amount = _swap(_reward, token0, halfAmount);

        // Swap half to token1
        t1Amount = _swap(_reward, token1, _amount - halfAmount);
    }

    /**
     * @notice Swap tokens via DEX
     */
    function _swap(
        address _from,
        address _to,
        uint256 _amount
    ) internal returns (uint256) {
        if (_from == _to) return _amount;

        IERC20(_from).approve(dexRouter, _amount);

        // Implement actual DEX swap
        // ...

        return IERC20(_to).balanceOf(address(this));
    }

    /**
     * @notice Add liquidity to AMM
     */
    function _addLiquidity(
        uint256 _amount0,
        uint256 _amount1
    ) internal returns (uint256 lpAmount) {
        IERC20(token0).approve(ammRouter, _amount0);
        IERC20(token1).approve(ammRouter, _amount1);

        // Implement actual add liquidity
        // ...

        return IERC20(lpToken).balanceOf(address(this));
    }
}
```

---

## 4. YIELD OPTIMIZATION STRATEGIES

### 4.1 Leverage Yield Farming

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title LeveragedYieldFarm
 * @notice Leveraged farming using flash loans
 */
contract LeveragedYieldFarm {
    // Lending protocol interface
    interface ILendingProtocol {
        function deposit(address asset, uint256 amount) external;
        function borrow(address asset, uint256 amount) external;
        function repay(address asset, uint256 amount) external;
        function withdraw(address asset, uint256 amount) external;
        function getHealthFactor(address user) external view returns (uint256);
    }

    ILendingProtocol public lendingProtocol;

    // Yield farm interface
    interface IYieldFarm {
        function stake(uint256 amount) external;
        function unstake(uint256 amount) external;
        function claim() external returns (uint256);
        function pendingRewards(address user) external view returns (uint256);
    }

    IYieldFarm public yieldFarm;

    // Asset being farmed
    IERC20 public asset;

    // Target leverage (e.g., 3x = 30000 in basis points)
    uint256 public targetLeverage = 30000;

    // Position tracking
    struct Position {
        uint256 deposited;      // User's original deposit
        uint256 borrowed;       // Total borrowed
        uint256 totalStaked;    // Total in yield farm
    }

    mapping(address => Position) public positions;

    /**
     * @notice Open leveraged position
     * @param _amount Initial deposit amount
     */
    function openPosition(uint256 _amount) external {
        require(positions[msg.sender].deposited == 0, "Position exists");

        // Transfer initial deposit
        asset.transferFrom(msg.sender, address(this), _amount);

        // Calculate leverage amounts
        // With 3x leverage on $1000:
        // - Deposit $1000 as collateral
        // - Borrow $2000
        // - Total farming = $3000

        uint256 toBorrow = (_amount * (targetLeverage - 10000)) / 10000;
        uint256 totalToFarm = _amount + toBorrow;

        // Deposit collateral
        asset.approve(address(lendingProtocol), _amount);
        lendingProtocol.deposit(address(asset), _amount);

        // Borrow
        lendingProtocol.borrow(address(asset), toBorrow);

        // Stake in yield farm
        asset.approve(address(yieldFarm), totalToFarm);
        yieldFarm.stake(totalToFarm);

        // Store position
        positions[msg.sender] = Position({
            deposited: _amount,
            borrowed: toBorrow,
            totalStaked: totalToFarm
        });
    }

    /**
     * @notice Close leveraged position
     */
    function closePosition() external {
        Position storage pos = positions[msg.sender];
        require(pos.deposited > 0, "No position");

        // Claim rewards first
        uint256 rewards = yieldFarm.claim();

        // Unstake all
        yieldFarm.unstake(pos.totalStaked);

        // Repay borrowed amount
        asset.approve(address(lendingProtocol), pos.borrowed);
        lendingProtocol.repay(address(asset), pos.borrowed);

        // Withdraw collateral
        lendingProtocol.withdraw(address(asset), pos.deposited);

        // Calculate profit
        uint256 balance = asset.balanceOf(address(this));
        uint256 profit = balance > pos.deposited ? balance - pos.deposited : 0;

        // Transfer back to user
        asset.transfer(msg.sender, balance);

        // Clear position
        delete positions[msg.sender];
    }

    /**
     * @notice Rebalance leverage if needed
     */
    function rebalance() external {
        Position storage pos = positions[msg.sender];
        require(pos.deposited > 0, "No position");

        // Check health factor
        uint256 healthFactor = lendingProtocol.getHealthFactor(address(this));

        // If health factor too low, deleverage
        if (healthFactor < 1.1e18) {
            // Calculate amount to repay
            uint256 repayAmount = (pos.borrowed * 1000) / 10000; // Repay 10%

            // Unstake portion
            yieldFarm.unstake(repayAmount);

            // Repay
            asset.approve(address(lendingProtocol), repayAmount);
            lendingProtocol.repay(address(asset), repayAmount);

            pos.borrowed -= repayAmount;
            pos.totalStaked -= repayAmount;
        }
    }

    /**
     * @notice Calculate current APY with leverage
     */
    function getEffectiveAPY(uint256 baseAPY) external view returns (uint256) {
        // Leveraged APY = Base APY × Leverage - Borrow Cost
        // Example: 10% × 3 - 5% = 25%

        uint256 leverageMultiplier = targetLeverage / 10000;
        uint256 borrowCost = 500; // 5% borrow rate (simplified)

        uint256 leveragedAPY = (baseAPY * leverageMultiplier) - (borrowCost * (leverageMultiplier - 1));

        return leveragedAPY;
    }
}
```

### 4.2 Yield Arbitrage Bot

```python
"""
Cross-Protocol Yield Arbitrage
"""

import asyncio
from typing import Dict, List, Tuple
from dataclasses import dataclass
from web3 import Web3

@dataclass
class YieldOpportunity:
    protocol: str
    asset: str
    apy: float
    tvl: float
    risk_score: int  # 1-10
    chain: str

class YieldArbitrageur:
    def __init__(self, w3: Web3, min_spread: float = 0.02):
        """
        Args:
            w3: Web3 instance
            min_spread: Minimum yield spread to act on (2% default)
        """
        self.w3 = w3
        self.min_spread = min_spread

        # Protocol registry
        self.protocols = {
            'aave_v3': {
                'chains': ['ethereum', 'arbitrum', 'optimism', 'polygon'],
                'risk': 2
            },
            'compound_v3': {
                'chains': ['ethereum', 'arbitrum', 'polygon'],
                'risk': 2
            },
            'morpho': {
                'chains': ['ethereum'],
                'risk': 3
            },
            'spark': {
                'chains': ['ethereum'],
                'risk': 3
            },
            'radiant': {
                'chains': ['arbitrum', 'bsc'],
                'risk': 5
            }
        }

    async def scan_yields(self, asset: str = 'USDC') -> List[YieldOpportunity]:
        """
        Scan all protocols for current yields
        """
        opportunities = []

        for protocol, config in self.protocols.items():
            for chain in config['chains']:
                try:
                    apy, tvl = await self._get_protocol_yield(protocol, chain, asset)

                    opportunities.append(YieldOpportunity(
                        protocol=protocol,
                        asset=asset,
                        apy=apy,
                        tvl=tvl,
                        risk_score=config['risk'],
                        chain=chain
                    ))
                except Exception as e:
                    print(f"Error fetching {protocol} on {chain}: {e}")

        return sorted(opportunities, key=lambda x: x.apy, reverse=True)

    async def find_arbitrage(self, asset: str = 'USDC') -> List[Tuple[YieldOpportunity, YieldOpportunity, float]]:
        """
        Find yield arbitrage opportunities

        Returns:
            List of (source, target, spread) tuples
        """
        yields = await self.scan_yields(asset)
        opportunities = []

        for i, high_yield in enumerate(yields):
            for low_yield in yields[i+1:]:
                spread = high_yield.apy - low_yield.apy

                if spread >= self.min_spread:
                    # Same chain opportunities are better (no bridging)
                    if high_yield.chain == low_yield.chain:
                        spread *= 1.2  # Boost same-chain opportunities

                    opportunities.append((high_yield, low_yield, spread))

        return sorted(opportunities, key=lambda x: x[2], reverse=True)

    async def execute_rotation(
        self,
        from_protocol: str,
        to_protocol: str,
        amount: int,
        chain: str
    ) -> str:
        """
        Execute yield rotation

        Returns:
            Transaction hash
        """
        # 1. Withdraw from source protocol
        withdraw_tx = await self._withdraw(from_protocol, amount, chain)
        print(f"Withdrew from {from_protocol}: {withdraw_tx}")

        # 2. Deposit to target protocol
        deposit_tx = await self._deposit(to_protocol, amount, chain)
        print(f"Deposited to {to_protocol}: {deposit_tx}")

        return deposit_tx

    async def monitor_and_rotate(
        self,
        current_position: Dict,
        check_interval: int = 3600  # 1 hour
    ):
        """
        Continuously monitor and rotate to best yield
        """
        while True:
            opportunities = await self.find_arbitrage(current_position['asset'])

            if opportunities:
                best = opportunities[0]
                current_apy = await self._get_protocol_yield(
                    current_position['protocol'],
                    current_position['chain'],
                    current_position['asset']
                )

                # Check if rotation is profitable
                spread = best[0].apy - current_apy[0]

                if spread > self.min_spread:
                    print(f"Found opportunity: {spread:.2%} spread")
                    print(f"Rotate from {current_position['protocol']} to {best[0].protocol}")

                    # Calculate if gas costs are worth it
                    gas_cost_usd = await self._estimate_gas_cost(current_position['chain'])
                    position_size = current_position['amount']
                    daily_gain = (spread * position_size) / 365

                    if daily_gain > gas_cost_usd:
                        # Execute rotation
                        await self.execute_rotation(
                            current_position['protocol'],
                            best[0].protocol,
                            position_size,
                            current_position['chain']
                        )

                        current_position['protocol'] = best[0].protocol

            await asyncio.sleep(check_interval)

    async def _get_protocol_yield(self, protocol: str, chain: str, asset: str) -> Tuple[float, float]:
        """Get current yield and TVL from protocol"""
        # Implementation depends on protocol
        # Return (apy, tvl)
        return (0.05, 1000000)  # Placeholder

    async def _withdraw(self, protocol: str, amount: int, chain: str) -> str:
        """Withdraw from protocol"""
        return "0x..."  # Placeholder

    async def _deposit(self, protocol: str, amount: int, chain: str) -> str:
        """Deposit to protocol"""
        return "0x..."  # Placeholder

    async def _estimate_gas_cost(self, chain: str) -> float:
        """Estimate gas cost in USD"""
        return 5.0  # Placeholder


# Example usage
async def main():
    w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
    arb = YieldArbitrageur(w3, min_spread=0.02)

    # Scan yields
    yields = await arb.scan_yields('USDC')
    print("=== Current Yields ===")
    for y in yields[:5]:
        print(f"{y.protocol} ({y.chain}): {y.apy:.2%}")

    # Find arbitrage
    opps = await arb.find_arbitrage('USDC')
    print("\n=== Arbitrage Opportunities ===")
    for high, low, spread in opps[:3]:
        print(f"Move from {low.protocol} ({low.apy:.2%}) to {high.protocol} ({high.apy:.2%})")
        print(f"Spread: {spread:.2%}")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 5. RISK MANAGEMENT

```yaml
YIELD FARMING RISK FRAMEWORK:
══════════════════════════════════════════════════════════════════════════

SMART CONTRACT RISK:
  Description: Bugs in protocol code
  Mitigation:
    - Only use audited protocols
    - Check time in production (Lindy effect)
    - Diversify across protocols
  Risk Level: HIGH

IMPERMANENT LOSS:
  Description: LP value < holding
  Mitigation:
    - Use stable pairs
    - Monitor correlation
    - Consider IL-protected vaults
  Risk Level: MEDIUM-HIGH

LIQUIDATION RISK:
  Description: Leveraged positions liquidated
  Mitigation:
    - Conservative LTV
    - Set up monitoring alerts
    - Keep reserves for rebalancing
  Risk Level: HIGH

ORACLE MANIPULATION:
  Description: Price feed attacks
  Mitigation:
    - Use protocols with TWAP oracles
    - Avoid low-liquidity assets
  Risk Level: MEDIUM

TOKEN EMISSION RISK:
  Description: Reward token dumps
  Mitigation:
    - Harvest and sell regularly
    - Focus on "real yield" protocols
    - Diversify reward exposure
  Risk Level: HIGH

GAS COST RISK:
  Description: Gas > yield
  Mitigation:
    - Calculate breakeven
    - Use L2s for small positions
    - Batch transactions
  Risk Level: MEDIUM

PROTOCOL GOVERNANCE RISK:
  Description: Malicious proposals
  Mitigation:
    - Monitor governance
    - Use timelock-protected protocols
    - Set up alerts
  Risk Level: LOW-MEDIUM
```

---

## 6. MAJOR YIELD PROTOCOLS

```
YIELD AGGREGATOR COMPARISON
═══════════════════════════════════════════════════════════════════════

┌─────────────┬────────────────┬────────────────┬────────────────┬────────────────┐
│ Protocol    │ Yearn          │ Beefy          │ Convex         │ Concentrator   │
├─────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ Chains      │ ETH, FTM, ARB  │ 20+ chains     │ Ethereum       │ Ethereum       │
│ Focus       │ Multi-strategy │ Auto-compound  │ Curve boost    │ CRV/CVX focus  │
│ TVL         │ ~$500M         │ ~$300M         │ ~$3B           │ ~$100M         │
│ Fees        │ 20% perf       │ 4.5% perf      │ 16% platform   │ 10% harvest    │
│ Token       │ YFI            │ BIFI           │ CVX            │ CTR            │
│ Unique      │ Strategy vault │ Widest chain   │ veCRV control  │ Auto aCRV      │
│             │ innovation     │ support        │                │ compounding    │
└─────────────┴────────────────┴────────────────┴────────────────┴────────────────┘

LENDING YIELD SOURCES:
┌─────────────┬────────────────┬────────────────┬────────────────┬────────────────┐
│ Protocol    │ Aave V3        │ Compound V3    │ Morpho         │ Spark          │
├─────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ Chains      │ 8+             │ 4              │ Ethereum       │ Ethereum       │
│ Model       │ Pool-based     │ Comet          │ P2P matching   │ MakerDAO based │
│ USDC APY    │ 3-8%           │ 3-7%           │ 4-10%          │ 5-8%           │
│ Innovation  │ E-Mode         │ Single asset   │ Rate optim     │ sDAI native    │
│ Safety      │ Audited, old   │ Audited, old   │ New, growing   │ MKR backing    │
└─────────────┴────────────────┴────────────────┴────────────────┴────────────────┘
```

---

## FIRMA

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  NEURONA: YIELD STRATEGIES & AGGREGATORS                                       ║
║  Dominio: C40005 - Yield Optimization                                          ║
║  Versión: 1.0.0                                                                ║
║  Última actualización: 2024-12-29                                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```
