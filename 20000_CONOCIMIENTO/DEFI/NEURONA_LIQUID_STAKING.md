# NEURONA: LIQUID STAKING & LSTs
## C40006 - Liquid Staking Derivatives

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  CIPHER NEURONA: LIQUID STAKING                                                ║
║  Dominio: LSTs, Restaking, LRTs, Staking Derivatives                           ║
║  Estado: ACTIVA                                                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. LIQUID STAKING FUNDAMENTALS

### 1.1 El Problema que Resuelve

```
STAKING TRADICIONAL vs LIQUID STAKING
═══════════════════════════════════════════════════════════════════════

TRADITIONAL STAKING:
┌────────────────────────────────────────────────────────────────────────┐
│  User deposits 32 ETH ──→ Validator ──→ Locked until withdrawal        │
│                                                                         │
│  Problems:                                                              │
│  ├── Capital locked (illiquid)                                         │
│  ├── High minimum (32 ETH = ~$60K+)                                    │
│  ├── Technical complexity (run validator)                               │
│  ├── Slashing risk (user bears all)                                    │
│  └── Opportunity cost (can't use in DeFi)                              │
└────────────────────────────────────────────────────────────────────────┘

LIQUID STAKING:
┌────────────────────────────────────────────────────────────────────────┐
│  User deposits ETH ──→ Protocol ──→ Receives LST (liquid token)        │
│                                                                         │
│  Benefits:                                                              │
│  ├── Liquid: Trade LST anytime                                         │
│  ├── Low minimum: Any amount                                           │
│  ├── No technical requirements                                         │
│  ├── Diversified slashing risk                                         │
│  └── DeFi composability: Use LST as collateral, LP, etc.               │
│                                                                         │
│  Trade-offs:                                                            │
│  ├── Smart contract risk                                               │
│  ├── Protocol fees (5-10%)                                             │
│  ├── LST/ETH peg risk                                                  │
│  └── Centralization concerns                                            │
└────────────────────────────────────────────────────────────────────────┘
```

### 1.2 LST Price Models

```
LST PRICING MECHANISMS
═══════════════════════════════════════════════════════════════════════

1. REBASING (stETH):
   ├── Balance increases daily
   ├── 1 stETH always = 1 stETH
   ├── Staking rewards reflected in balance
   └── Example: Deposit 10 stETH → Next day: 10.001 stETH

2. REWARD-BEARING (rETH, cbETH):
   ├── Balance stays same
   ├── Token value increases vs ETH
   ├── Exchange rate grows over time
   └── Example: 1 rETH = 1.05 ETH (and growing)

3. HYBRID (wstETH):
   ├── Wrapped rebasing token
   ├── Fixed supply, increasing value
   ├── DeFi-friendly (no balance changes)
   └── Example: wstETH wraps stETH for composability

EXCHANGE RATE CALCULATION (reward-bearing):
═══════════════════════════════════════════════════════════════════════

exchangeRate = totalPooledETH / totalShares

Where:
├── totalPooledETH = deposited ETH + accrued rewards - slashing losses
└── totalShares = total LST supply

Example (rETH):
├── Total ETH in protocol: 1,050,000 ETH
├── Total rETH supply: 1,000,000 rETH
└── Exchange rate: 1.05 (1 rETH = 1.05 ETH)
```

---

## 2. MAJOR LST PROTOCOLS

### 2.1 Lido (stETH)

```
LIDO ARCHITECTURE
═══════════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────────────┐
│                         LIDO PROTOCOL                                   │
│                                                                         │
│  User ──deposit ETH──→ Lido Contract ──distribute──→ Node Operators    │
│    │                        │                              │            │
│    │                        │                              ▼            │
│    │                        │                      Ethereum Beacon      │
│    │                        │                         Chain             │
│    │                        │                              │            │
│    │                        ▼                              │            │
│    └──receive stETH──← Mint stETH                  Staking Rewards     │
│                              │                              │            │
│                              └──────────daily rebase────────┘            │
│                                                                         │
├────────────────────────────────────────────────────────────────────────┤
│                      NODE OPERATOR SET                                  │
│                                                                         │
│  30+ Professional Operators:                                            │
│  ├── Curated set (permissioned)                                        │
│  ├── Performance monitored                                              │
│  ├── Slashing insurance                                                 │
│  └── DVT integration (Obol, SSV)                                       │
│                                                                         │
├────────────────────────────────────────────────────────────────────────┤
│                         FEE STRUCTURE                                   │
│                                                                         │
│  Staking Rewards Distribution:                                          │
│  ├── 90% to stETH holders (rebase)                                     │
│  ├── 5% to Node Operators                                              │
│  └── 5% to Lido DAO Treasury                                           │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Lido Simplified Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title SimplifiedStETH
 * @notice Rebasing liquid staking token (Lido-style)
 */
contract SimplifiedStETH is ERC20, ReentrancyGuard {
    // Total shares (internal accounting)
    uint256 private _totalShares;

    // Share balances
    mapping(address => uint256) private _shares;

    // Total pooled ETH (deposits + rewards - slashing)
    uint256 public totalPooledEther;

    // Protocol fee (10% = 1000 basis points)
    uint256 public constant PROTOCOL_FEE = 1000;

    // Oracle for beacon chain balance updates
    address public oracle;

    // Treasury for protocol fees
    address public treasury;

    event Submitted(address indexed sender, uint256 amount, address referral);
    event ETHDistributed(uint256 rewardAmount, uint256 feeAmount);

    constructor() ERC20("Liquid staked Ether", "stETH") {
        oracle = msg.sender;
        treasury = msg.sender;
    }

    /**
     * @notice Submit ETH for staking
     */
    function submit(address _referral) external payable nonReentrant returns (uint256) {
        require(msg.value > 0, "Zero deposit");

        uint256 sharesToMint = getSharesByPooledEth(msg.value);
        if (sharesToMint == 0) {
            // First deposit: 1:1 shares
            sharesToMint = msg.value;
        }

        _mintShares(msg.sender, sharesToMint);
        totalPooledEther += msg.value;

        emit Submitted(msg.sender, msg.value, _referral);

        // In production: deposit to beacon chain via deposit contract
        // For demo: ETH held in contract

        return sharesToMint;
    }

    /**
     * @notice Request withdrawal (simplified - instant for demo)
     */
    function withdraw(uint256 _stETHAmount) external nonReentrant {
        uint256 sharesToBurn = getSharesByPooledEth(_stETHAmount);
        require(_shares[msg.sender] >= sharesToBurn, "Insufficient balance");

        uint256 ethToReturn = getPooledEthByShares(sharesToBurn);

        _burnShares(msg.sender, sharesToBurn);
        totalPooledEther -= ethToReturn;

        (bool success, ) = msg.sender.call{value: ethToReturn}("");
        require(success, "ETH transfer failed");
    }

    /**
     * @notice Oracle reports beacon chain balance (rewards/slashing)
     * @dev Called daily by oracle to update totalPooledEther
     */
    function handleOracleReport(
        uint256 _beaconBalance,
        uint256 _beaconValidators
    ) external onlyOracle {
        uint256 previousPooledEther = totalPooledEther;

        // New total = contract balance + beacon chain balance
        uint256 newPooledEther = address(this).balance + _beaconBalance;

        if (newPooledEther > previousPooledEther) {
            // Rewards! Distribute fee
            uint256 rewards = newPooledEther - previousPooledEther;
            uint256 feeAmount = (rewards * PROTOCOL_FEE) / 10000;

            // Mint shares to treasury (dilutes other holders = fee)
            uint256 feeShares = getSharesByPooledEth(feeAmount);
            _mintShares(treasury, feeShares);

            emit ETHDistributed(rewards - feeAmount, feeAmount);
        }

        totalPooledEther = newPooledEther;
    }

    // ============ ERC20 Overrides for Rebasing ============

    /**
     * @notice Get stETH balance (rebasing - changes daily)
     */
    function balanceOf(address _account) public view override returns (uint256) {
        return getPooledEthByShares(_shares[_account]);
    }

    /**
     * @notice Get total stETH supply (= total pooled ETH)
     */
    function totalSupply() public view override returns (uint256) {
        return totalPooledEther;
    }

    /**
     * @notice Transfer stETH (transfers shares internally)
     */
    function transfer(address _to, uint256 _amount) public override returns (bool) {
        uint256 sharesToTransfer = getSharesByPooledEth(_amount);
        _transferShares(msg.sender, _to, sharesToTransfer);
        emit Transfer(msg.sender, _to, _amount);
        return true;
    }

    /**
     * @notice TransferFrom stETH
     */
    function transferFrom(address _from, address _to, uint256 _amount) public override returns (bool) {
        uint256 sharesToTransfer = getSharesByPooledEth(_amount);
        _spendAllowance(_from, msg.sender, _amount);
        _transferShares(_from, _to, sharesToTransfer);
        emit Transfer(_from, _to, _amount);
        return true;
    }

    // ============ Share/ETH Conversion ============

    /**
     * @notice Get shares amount for given stETH amount
     */
    function getSharesByPooledEth(uint256 _ethAmount) public view returns (uint256) {
        if (totalPooledEther == 0) return 0;
        return (_ethAmount * _totalShares) / totalPooledEther;
    }

    /**
     * @notice Get stETH amount for given shares
     */
    function getPooledEthByShares(uint256 _sharesAmount) public view returns (uint256) {
        if (_totalShares == 0) return 0;
        return (_sharesAmount * totalPooledEther) / _totalShares;
    }

    /**
     * @notice Get user's shares (not stETH balance)
     */
    function sharesOf(address _account) external view returns (uint256) {
        return _shares[_account];
    }

    /**
     * @notice Get total shares
     */
    function getTotalShares() external view returns (uint256) {
        return _totalShares;
    }

    // ============ Internal Share Management ============

    function _mintShares(address _to, uint256 _amount) internal {
        _totalShares += _amount;
        _shares[_to] += _amount;
    }

    function _burnShares(address _from, uint256 _amount) internal {
        _shares[_from] -= _amount;
        _totalShares -= _amount;
    }

    function _transferShares(address _from, address _to, uint256 _amount) internal {
        _shares[_from] -= _amount;
        _shares[_to] += _amount;
    }

    modifier onlyOracle() {
        require(msg.sender == oracle, "Only oracle");
        _;
    }

    receive() external payable {}
}
```

### 2.3 Rocket Pool (rETH)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/**
 * @title SimplifiedRETH
 * @notice Reward-bearing liquid staking token (Rocket Pool style)
 */
contract SimplifiedRETH is ERC20 {
    // Total ETH backing the rETH supply
    uint256 public totalEthBalance;

    // Minipool registry
    struct Minipool {
        address operator;
        uint256 userDeposit;      // 16 or 24 ETH from pool
        uint256 operatorDeposit;  // 16 or 8 ETH from operator
        bool active;
    }

    mapping(address => Minipool) public minipools;
    address[] public minipoolList;

    // Node operator registry
    mapping(address => bool) public registeredOperators;
    mapping(address => uint256) public operatorRPL; // RPL staked

    // Protocol token for insurance
    IERC20 public rplToken;

    // Minimum RPL stake (10% of borrowed ETH value)
    uint256 public constant MIN_RPL_STAKE_PERCENT = 1000; // 10%

    event Deposited(address indexed user, uint256 ethAmount, uint256 rethMinted);
    event MinipoolCreated(address indexed minipool, address indexed operator);

    constructor() ERC20("Rocket Pool ETH", "rETH") {}

    /**
     * @notice Deposit ETH and receive rETH
     */
    function deposit() external payable returns (uint256 rethMinted) {
        require(msg.value > 0, "Zero deposit");

        // Calculate rETH to mint based on exchange rate
        rethMinted = getRethValue(msg.value);

        _mint(msg.sender, rethMinted);
        totalEthBalance += msg.value;

        emit Deposited(msg.sender, msg.value, rethMinted);
    }

    /**
     * @notice Burn rETH and receive ETH
     */
    function burn(uint256 _rethAmount) external {
        uint256 ethValue = getEthValue(_rethAmount);
        require(address(this).balance >= ethValue, "Insufficient liquidity");

        _burn(msg.sender, _rethAmount);
        totalEthBalance -= ethValue;

        (bool success, ) = msg.sender.call{value: ethValue}("");
        require(success, "ETH transfer failed");
    }

    /**
     * @notice Register as node operator
     * @dev Must stake minimum RPL
     */
    function registerOperator(uint256 _rplAmount) external {
        require(!registeredOperators[msg.sender], "Already registered");

        // Stake RPL
        rplToken.transferFrom(msg.sender, address(this), _rplAmount);
        operatorRPL[msg.sender] = _rplAmount;

        registeredOperators[msg.sender] = true;
    }

    /**
     * @notice Create minipool (operator deposits 8-16 ETH, borrows rest from pool)
     */
    function createMinipool() external payable {
        require(registeredOperators[msg.sender], "Not registered");
        require(msg.value >= 8 ether && msg.value <= 16 ether, "Invalid deposit");

        // Check RPL stake is sufficient
        uint256 borrowedEth = 32 ether - msg.value;
        uint256 minRPL = (borrowedEth * MIN_RPL_STAKE_PERCENT) / 10000;
        require(operatorRPL[msg.sender] >= minRPL, "Insufficient RPL stake");

        // Create minipool contract (simplified - in production separate contract)
        address minipoolAddress = address(uint160(uint256(keccak256(abi.encodePacked(
            msg.sender,
            block.timestamp,
            minipoolList.length
        )))));

        minipools[minipoolAddress] = Minipool({
            operator: msg.sender,
            userDeposit: borrowedEth,
            operatorDeposit: msg.value,
            active: true
        });

        minipoolList.push(minipoolAddress);

        // Move ETH from deposit pool to minipool
        totalEthBalance -= borrowedEth;

        // In production: deposit to beacon chain
        emit MinipoolCreated(minipoolAddress, msg.sender);
    }

    /**
     * @notice Report rewards from beacon chain
     * @dev Called by oracle, increases totalEthBalance
     */
    function reportRewards(uint256 _rewardAmount) external {
        // In production: verify oracle signature
        totalEthBalance += _rewardAmount;

        // rETH holders automatically benefit through exchange rate
        // No new tokens minted - existing rETH now worth more ETH
    }

    // ============ Exchange Rate Functions ============

    /**
     * @notice Get exchange rate (ETH per rETH)
     */
    function getExchangeRate() public view returns (uint256) {
        uint256 supply = totalSupply();
        if (supply == 0) return 1 ether;
        return (totalEthBalance * 1 ether) / supply;
    }

    /**
     * @notice Get rETH value for ETH amount
     */
    function getRethValue(uint256 _ethAmount) public view returns (uint256) {
        uint256 supply = totalSupply();
        if (supply == 0 || totalEthBalance == 0) return _ethAmount;
        return (_ethAmount * supply) / totalEthBalance;
    }

    /**
     * @notice Get ETH value for rETH amount
     */
    function getEthValue(uint256 _rethAmount) public view returns (uint256) {
        uint256 supply = totalSupply();
        if (supply == 0) return 0;
        return (_rethAmount * totalEthBalance) / supply;
    }

    receive() external payable {
        totalEthBalance += msg.value;
    }
}
```

---

## 3. RESTAKING & EIGENLAYER

### 3.1 Restaking Concept

```
EIGENLAYER RESTAKING ARCHITECTURE
═══════════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────────────┐
│                        RESTAKING LAYERS                                 │
│                                                                         │
│  Layer 0: Ethereum PoS                                                  │
│  ├── Validators stake 32 ETH                                           │
│  └── Secures Ethereum consensus                                        │
│                              │                                          │
│                              ▼                                          │
│  Layer 1: EigenLayer                                                    │
│  ├── Restake ETH/LSTs to EigenLayer                                    │
│  ├── Same ETH secures multiple networks                                │
│  └── "Pooled security" for AVSs                                        │
│                              │                                          │
│                              ▼                                          │
│  Layer 2: AVS (Actively Validated Services)                            │
│  ├── Oracles (EigenDA)                                                 │
│  ├── Bridges                                                           │
│  ├── Rollup sequencers                                                 │
│  ├── Keeper networks                                                   │
│  └── Any service needing crypto-economic security                      │
│                                                                         │
├────────────────────────────────────────────────────────────────────────┤
│                         VALUE FLOW                                      │
│                                                                         │
│  ETH Staker ──restake──→ EigenLayer ──delegate──→ Operator             │
│       │                       │                        │                │
│       │                       │                        ▼                │
│       │                       │                   Validate AVS          │
│       │                       │                        │                │
│       │                       ▼                        │                │
│       └──receive rewards──← Reward Distribution ←──fees from AVS       │
│                                                                         │
│  Risk: Slashing for AVS misbehavior (in addition to ETH slashing)      │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

### 3.2 EigenLayer Integration

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/**
 * @title SimplifiedEigenLayerStrategy
 * @notice Simplified EigenLayer restaking strategy
 */
contract SimplifiedEigenLayerStrategy {
    // Supported restaking tokens
    mapping(address => bool) public supportedTokens;

    // User deposits
    mapping(address => mapping(address => uint256)) public deposits; // user => token => amount

    // Total deposited per token
    mapping(address => uint256) public totalDeposited;

    // Operator delegations
    mapping(address => address) public delegatedTo; // staker => operator

    // Operator info
    struct Operator {
        bool registered;
        uint256 totalDelegated;
        address[] avsList;
    }
    mapping(address => Operator) public operators;

    // AVS registry
    struct AVS {
        bool active;
        uint256 slashingRisk; // basis points
        uint256 rewardRate;   // annual rate in basis points
    }
    mapping(address => AVS) public avsRegistry;

    // Slashing state
    mapping(address => uint256) public slashedAmount;

    event Deposited(address indexed staker, address indexed token, uint256 amount);
    event Delegated(address indexed staker, address indexed operator);
    event Slashed(address indexed operator, address indexed avs, uint256 amount);

    /**
     * @notice Deposit LST or native ETH restaking
     */
    function deposit(address _token, uint256 _amount) external {
        require(supportedTokens[_token], "Token not supported");

        IERC20(_token).transferFrom(msg.sender, address(this), _amount);

        deposits[msg.sender][_token] += _amount;
        totalDeposited[_token] += _amount;

        emit Deposited(msg.sender, _token, _amount);
    }

    /**
     * @notice Delegate restaked assets to operator
     */
    function delegateTo(address _operator) external {
        require(operators[_operator].registered, "Operator not registered");
        require(delegatedTo[msg.sender] == address(0), "Already delegated");

        delegatedTo[msg.sender] = _operator;

        // Calculate total delegation value
        uint256 totalValue = _calculateTotalValue(msg.sender);
        operators[_operator].totalDelegated += totalValue;

        emit Delegated(msg.sender, _operator);
    }

    /**
     * @notice Register as operator
     */
    function registerOperator() external {
        require(!operators[msg.sender].registered, "Already registered");

        operators[msg.sender] = Operator({
            registered: true,
            totalDelegated: 0,
            avsList: new address[](0)
        });
    }

    /**
     * @notice Operator opts into AVS
     */
    function optIntoAVS(address _avs) external {
        require(operators[msg.sender].registered, "Not an operator");
        require(avsRegistry[_avs].active, "AVS not active");

        operators[msg.sender].avsList.push(_avs);
    }

    /**
     * @notice Slash operator for AVS misbehavior
     * @dev Called by AVS slashing contract
     */
    function slash(
        address _operator,
        address _avs,
        uint256 _percentage // basis points
    ) external {
        // In production: verify caller is authorized AVS slasher
        require(avsRegistry[_avs].active, "Invalid AVS");

        Operator storage op = operators[_operator];

        uint256 slashAmount = (op.totalDelegated * _percentage) / 10000;

        // Reduce operator's delegation
        op.totalDelegated -= slashAmount;
        slashedAmount[_operator] += slashAmount;

        emit Slashed(_operator, _avs, slashAmount);

        // In production: distribute slashed funds or burn
    }

    /**
     * @notice Calculate staker's yield from AVS
     */
    function calculatePendingRewards(address _staker) external view returns (uint256) {
        address operator = delegatedTo[_staker];
        if (operator == address(0)) return 0;

        uint256 stakerValue = _calculateTotalValue(_staker);
        uint256 operatorTotal = operators[operator].totalDelegated;

        if (operatorTotal == 0) return 0;

        // Calculate share of operator's AVS rewards
        uint256 totalRewards = 0;
        address[] memory avsList = operators[operator].avsList;

        for (uint256 i = 0; i < avsList.length; i++) {
            AVS memory avs = avsRegistry[avsList[i]];
            // Simplified: annual reward rate applied to stake
            uint256 avsReward = (operatorTotal * avs.rewardRate) / 10000;
            totalRewards += avsReward;
        }

        // Staker's share
        return (totalRewards * stakerValue) / operatorTotal;
    }

    /**
     * @notice Calculate total value of staker's deposits
     */
    function _calculateTotalValue(address _staker) internal view returns (uint256) {
        // Simplified: sum all deposits (in production: use oracles for prices)
        uint256 total = 0;

        // Add stETH deposit
        total += deposits[_staker][address(0x1)]; // stETH placeholder

        // Add rETH deposit
        total += deposits[_staker][address(0x2)]; // rETH placeholder

        return total;
    }

    /**
     * @notice Add supported token (admin)
     */
    function addSupportedToken(address _token) external {
        supportedTokens[_token] = true;
    }

    /**
     * @notice Register AVS (admin)
     */
    function registerAVS(
        address _avs,
        uint256 _slashingRisk,
        uint256 _rewardRate
    ) external {
        avsRegistry[_avs] = AVS({
            active: true,
            slashingRisk: _slashingRisk,
            rewardRate: _rewardRate
        });
    }
}
```

---

## 4. LIQUID RESTAKING TOKENS (LRTs)

### 4.1 LRT Protocols

```
LRT ECOSYSTEM
═══════════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────────────┐
│                    LIQUID RESTAKING FLOW                                │
│                                                                         │
│  User deposits ETH/LST                                                  │
│           │                                                             │
│           ▼                                                             │
│  ┌─────────────────┐                                                   │
│  │   LRT Protocol  │ (Ether.fi, Renzo, Kelp, Puffer)                   │
│  │                 │                                                   │
│  │  ├─ Deposit     │                                                   │
│  │  ├─ Restake     │──→ EigenLayer                                     │
│  │  ├─ Delegate    │──→ Operators                                      │
│  │  └─ Mint LRT    │──→ User receives eETH/ezETH/rsETH/pufETH          │
│  └─────────────────┘                                                   │
│           │                                                             │
│           ▼                                                             │
│  User can use LRT in DeFi:                                             │
│  ├── Collateral on Aave                                                │
│  ├── LP on Curve/Balancer                                              │
│  ├── Leverage farming                                                  │
│  └── Trade on DEXs                                                      │
│                                                                         │
├────────────────────────────────────────────────────────────────────────┤
│                      LRT COMPARISON                                     │
│                                                                         │
│  ┌──────────┬──────────────┬──────────────┬──────────────┬───────────┐ │
│  │ Protocol │ Token        │ Backing      │ Points       │ Native    │ │
│  ├──────────┼──────────────┼──────────────┼──────────────┼───────────┤ │
│  │ Ether.fi │ eETH/weETH   │ ETH→EL       │ EigenLayer   │ Restaking │ │
│  │ Renzo    │ ezETH        │ ETH/LSTs→EL  │ Renzo Points │ Multi-AVS │ │
│  │ Kelp     │ rsETH        │ LSTs→EL      │ Kelp Miles   │ LST focus │ │
│  │ Puffer   │ pufETH       │ ETH→EL       │ Puffer Pts   │ Anti-slash│ │
│  │ Swell    │ rswETH       │ swETH→EL     │ Pearls       │ Voyage    │ │
│  └──────────┴──────────────┴──────────────┴──────────────┴───────────┘ │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

### 4.2 LRT Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/**
 * @title SimplifiedLRT
 * @notice Liquid Restaking Token (Ether.fi/Renzo style)
 */
contract SimplifiedLRT is ERC20 {
    using SafeERC20 for IERC20;

    // Accepted deposit tokens
    mapping(address => bool) public acceptedTokens;

    // Native ETH address placeholder
    address public constant NATIVE_ETH = address(0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE);

    // EigenLayer strategy manager
    address public eigenLayerStrategyManager;

    // Restaking operator
    address public operator;

    // Total ETH value (deposits + rewards)
    uint256 public totalETHValue;

    // Points tracking for airdrop
    mapping(address => uint256) public pointsBalance;
    uint256 public pointsPerETHPerSecond = 1000; // Points emission rate

    // User deposit timestamps for points calculation
    mapping(address => uint256) public lastPointsUpdate;

    event Deposited(address indexed user, address indexed token, uint256 amount, uint256 lrtMinted);
    event Withdrawn(address indexed user, uint256 lrtBurned, uint256 ethReturned);
    event PointsClaimed(address indexed user, uint256 points);

    constructor() ERC20("Liquid Restaking ETH", "lrETH") {
        acceptedTokens[NATIVE_ETH] = true;
    }

    /**
     * @notice Deposit ETH and receive LRT
     */
    function deposit() external payable returns (uint256 lrtAmount) {
        require(msg.value > 0, "Zero deposit");

        // Update points before deposit
        _updatePoints(msg.sender);

        // Calculate LRT to mint
        lrtAmount = _calculateLRTForETH(msg.value);

        // Mint LRT
        _mint(msg.sender, lrtAmount);

        // Update total value
        totalETHValue += msg.value;

        // Restake to EigenLayer (simplified)
        _restakeToEigenLayer(msg.value);

        emit Deposited(msg.sender, NATIVE_ETH, msg.value, lrtAmount);
    }

    /**
     * @notice Deposit LST (stETH, rETH, etc.) and receive LRT
     */
    function depositLST(address _lst, uint256 _amount) external returns (uint256 lrtAmount) {
        require(acceptedTokens[_lst], "Token not accepted");

        // Update points
        _updatePoints(msg.sender);

        // Transfer LST
        IERC20(_lst).safeTransferFrom(msg.sender, address(this), _amount);

        // Get ETH value of LST (simplified - use oracle in production)
        uint256 ethValue = _getLSTValue(_lst, _amount);

        // Calculate LRT to mint
        lrtAmount = _calculateLRTForETH(ethValue);

        // Mint LRT
        _mint(msg.sender, lrtAmount);

        // Update total value
        totalETHValue += ethValue;

        // Restake LST to EigenLayer
        _restakeLSTToEigenLayer(_lst, _amount);

        emit Deposited(msg.sender, _lst, _amount, lrtAmount);
    }

    /**
     * @notice Request withdrawal (may have delay in production)
     */
    function withdraw(uint256 _lrtAmount) external returns (uint256 ethAmount) {
        require(balanceOf(msg.sender) >= _lrtAmount, "Insufficient balance");

        // Update points
        _updatePoints(msg.sender);

        // Calculate ETH to return
        ethAmount = _calculateETHForLRT(_lrtAmount);

        // Burn LRT
        _burn(msg.sender, _lrtAmount);

        // Update total value
        totalETHValue -= ethAmount;

        // In production: queue withdrawal from EigenLayer
        // For demo: instant withdrawal
        (bool success, ) = msg.sender.call{value: ethAmount}("");
        require(success, "ETH transfer failed");

        emit Withdrawn(msg.sender, _lrtAmount, ethAmount);
    }

    /**
     * @notice Claim accumulated points
     */
    function claimPoints() external returns (uint256 points) {
        _updatePoints(msg.sender);

        points = pointsBalance[msg.sender];
        pointsBalance[msg.sender] = 0;

        emit PointsClaimed(msg.sender, points);
    }

    /**
     * @notice Report rewards from EigenLayer (oracle)
     */
    function reportRewards(uint256 _rewardAmount) external {
        // In production: verify oracle signature
        totalETHValue += _rewardAmount;

        // LRT holders automatically benefit through exchange rate
    }

    // ============ Exchange Rate Functions ============

    function getExchangeRate() public view returns (uint256) {
        uint256 supply = totalSupply();
        if (supply == 0) return 1 ether;
        return (totalETHValue * 1 ether) / supply;
    }

    function _calculateLRTForETH(uint256 _ethAmount) internal view returns (uint256) {
        uint256 supply = totalSupply();
        if (supply == 0 || totalETHValue == 0) return _ethAmount;
        return (_ethAmount * supply) / totalETHValue;
    }

    function _calculateETHForLRT(uint256 _lrtAmount) internal view returns (uint256) {
        uint256 supply = totalSupply();
        if (supply == 0) return 0;
        return (_lrtAmount * totalETHValue) / supply;
    }

    // ============ Points System ============

    function _updatePoints(address _user) internal {
        if (lastPointsUpdate[_user] == 0) {
            lastPointsUpdate[_user] = block.timestamp;
            return;
        }

        uint256 timeElapsed = block.timestamp - lastPointsUpdate[_user];
        uint256 userBalance = balanceOf(_user);

        if (userBalance > 0 && timeElapsed > 0) {
            // Points = balance × time × rate
            uint256 newPoints = (userBalance * timeElapsed * pointsPerETHPerSecond) / 1 ether;
            pointsBalance[_user] += newPoints;
        }

        lastPointsUpdate[_user] = block.timestamp;
    }

    // ============ EigenLayer Integration (Simplified) ============

    function _restakeToEigenLayer(uint256 _amount) internal {
        // In production: deposit to EigenLayer StrategyManager
        // For demo: held in contract
    }

    function _restakeLSTToEigenLayer(address _lst, uint256 _amount) internal {
        // In production: deposit LST to EigenLayer strategy
        // For demo: held in contract
    }

    function _getLSTValue(address _lst, uint256 _amount) internal view returns (uint256) {
        // In production: query oracle for exchange rate
        // For demo: assume 1:1
        return _amount;
    }

    // ============ Admin Functions ============

    function addAcceptedToken(address _token) external {
        acceptedTokens[_token] = true;
    }

    function setOperator(address _operator) external {
        operator = _operator;
    }

    receive() external payable {
        totalETHValue += msg.value;
    }
}
```

---

## 5. LST/LRT DeFi STRATEGIES

### 5.1 Leverage Staking

```python
"""
Leveraged LST Strategies
"""

from dataclasses import dataclass
from typing import Tuple

@dataclass
class LeveragePosition:
    collateral_type: str  # "stETH", "rETH", etc.
    collateral_amount: float
    borrowed_amount: float  # ETH or stablecoin
    leverage: float
    health_factor: float
    net_apy: float

class LSTLeverageStrategy:
    """
    Recursive leveraged staking strategy

    Example:
    1. Deposit 10 stETH to Aave
    2. Borrow 7 ETH (70% LTV)
    3. Swap ETH → stETH
    4. Deposit new stETH
    5. Repeat until desired leverage
    """

    def __init__(
        self,
        lst_apy: float = 0.04,      # 4% stETH APY
        borrow_rate: float = 0.02,  # 2% ETH borrow rate
        max_ltv: float = 0.80,      # 80% LTV
        liquidation_threshold: float = 0.85
    ):
        self.lst_apy = lst_apy
        self.borrow_rate = borrow_rate
        self.max_ltv = max_ltv
        self.liq_threshold = liquidation_threshold

    def calculate_max_leverage(self, target_hf: float = 1.5) -> float:
        """
        Calculate maximum safe leverage for target health factor

        Health Factor = (collateral × liq_threshold) / debt
        Leverage = collateral / initial_deposit
        """
        # For recursive borrowing:
        # leverage = 1 / (1 - ltv)
        # With safety margin for health factor
        safe_ltv = self.liq_threshold / target_hf
        max_leverage = 1 / (1 - min(safe_ltv, self.max_ltv))

        return max_leverage

    def calculate_leveraged_apy(self, leverage: float) -> Tuple[float, float]:
        """
        Calculate net APY with leverage

        Returns:
            gross_apy: Total yield before borrow costs
            net_apy: Yield after borrow costs
        """
        # Gross APY = LST APY × Leverage
        gross_apy = self.lst_apy * leverage

        # Borrow cost = Borrow Rate × (Leverage - 1)
        borrow_cost = self.borrow_rate * (leverage - 1)

        # Net APY
        net_apy = gross_apy - borrow_cost

        return gross_apy, net_apy

    def simulate_position(
        self,
        initial_deposit: float,
        target_leverage: float
    ) -> LeveragePosition:
        """
        Simulate leveraged position
        """
        if target_leverage > self.calculate_max_leverage():
            raise ValueError("Leverage too high")

        # Total collateral = initial × leverage
        total_collateral = initial_deposit * target_leverage

        # Borrowed = collateral - initial
        borrowed = total_collateral - initial_deposit

        # Health factor
        hf = (total_collateral * self.liq_threshold) / borrowed

        # Net APY
        _, net_apy = self.calculate_leveraged_apy(target_leverage)

        return LeveragePosition(
            collateral_type="stETH",
            collateral_amount=total_collateral,
            borrowed_amount=borrowed,
            leverage=target_leverage,
            health_factor=hf,
            net_apy=net_apy
        )

    def calculate_liquidation_price(
        self,
        position: LeveragePosition,
        current_price: float = 1.0  # stETH/ETH
    ) -> float:
        """
        Calculate stETH/ETH price at which position gets liquidated
        """
        # Liquidation when: collateral × price × liq_threshold = debt
        # price = debt / (collateral × liq_threshold)
        liq_price = position.borrowed_amount / (
            position.collateral_amount * self.liq_threshold
        )

        return liq_price


# Example usage
if __name__ == "__main__":
    strategy = LSTLeverageStrategy(
        lst_apy=0.04,       # 4% stETH APY
        borrow_rate=0.02,   # 2% ETH borrow rate
        max_ltv=0.80,
        liquidation_threshold=0.85
    )

    print("=== Leveraged stETH Strategy ===\n")

    # Calculate max safe leverage
    max_lev = strategy.calculate_max_leverage(target_hf=1.5)
    print(f"Max safe leverage (HF=1.5): {max_lev:.2f}x\n")

    # Compare different leverage levels
    print("Leverage | Gross APY | Net APY | Health Factor")
    print("-" * 50)

    for leverage in [1.0, 2.0, 3.0, 4.0, 5.0]:
        if leverage > max_lev:
            continue

        gross, net = strategy.calculate_leveraged_apy(leverage)
        position = strategy.simulate_position(10.0, leverage)

        print(f"   {leverage:.1f}x   |  {gross:.1%}   | {net:.1%}  |    {position.health_factor:.2f}")

    # Detailed 3x position
    print("\n=== 3x Leveraged Position Details ===")
    pos = strategy.simulate_position(initial_deposit=10.0, target_leverage=3.0)

    print(f"Initial deposit: 10 ETH worth of stETH")
    print(f"Total collateral: {pos.collateral_amount:.2f} stETH")
    print(f"Borrowed: {pos.borrowed_amount:.2f} ETH")
    print(f"Health Factor: {pos.health_factor:.2f}")
    print(f"Net APY: {pos.net_apy:.2%}")

    liq_price = strategy.calculate_liquidation_price(pos)
    print(f"Liquidation price: {liq_price:.4f} stETH/ETH")
    print(f"Current stETH/ETH peg: 1.0000")
    print(f"Distance to liquidation: {(1 - liq_price) * 100:.1f}%")
```

---

## 6. PROTOCOL COMPARISON

```
LST/LRT PROTOCOL COMPARISON
═══════════════════════════════════════════════════════════════════════

┌─────────────────┬───────────────┬───────────────┬───────────────┬──────────────┐
│ Protocol        │ Lido (stETH)  │ Rocket Pool   │ Coinbase      │ Frax         │
│                 │               │ (rETH)        │ (cbETH)       │ (sfrxETH)    │
├─────────────────┼───────────────┼───────────────┼───────────────┼──────────────┤
│ Market Share    │ ~70%          │ ~8%           │ ~10%          │ ~3%          │
│ TVL             │ ~$15B         │ ~$2B          │ ~$2.5B        │ ~$500M       │
│ Token Model     │ Rebasing      │ Reward-bearing│ Reward-bearing│ Reward-bearing│
│ Fee             │ 10%           │ 14%           │ 25%           │ 10%          │
│ Decentralization│ Medium        │ High          │ Low           │ Medium       │
│ Operators       │ 30+ curated   │ Permissionless│ Coinbase      │ Frax-managed │
│ Min Stake       │ Any           │ Any (or 8 ETH)│ Any           │ Any          │
│ DeFi Adoption   │ Excellent     │ Good          │ Good          │ Growing      │
│ Slashing Risk   │ Socialized    │ Per-operator  │ Coinbase      │ Socialized   │
└─────────────────┴───────────────┴───────────────┴───────────────┴──────────────┘

LRT COMPARISON:
┌─────────────────┬───────────────┬───────────────┬───────────────┬──────────────┐
│ Protocol        │ Ether.fi      │ Renzo         │ Kelp          │ Puffer       │
├─────────────────┼───────────────┼───────────────┼───────────────┼──────────────┤
│ Token           │ eETH/weETH    │ ezETH         │ rsETH         │ pufETH       │
│ TVL             │ ~$6B          │ ~$3B          │ ~$1B          │ ~$2B         │
│ Accepts         │ ETH           │ ETH, LSTs     │ LSTs          │ ETH          │
│ Points System   │ ✓             │ ✓             │ ✓             │ ✓            │
│ Native Restaking│ ✓             │ ✓             │ ✗             │ ✓            │
│ DVT Support     │ Planned       │ Partial       │ ✗             │ ✓            │
│ Anti-Slashing   │ Insurance     │ Insurance     │ Insurance     │ Native       │
└─────────────────┴───────────────┴───────────────┴───────────────┴──────────────┘
```

---

## 7. RISK CONSIDERATIONS

```yaml
LST/LRT RISK FRAMEWORK:
══════════════════════════════════════════════════════════════════════════

SLASHING RISK:
  Description: Validator misbehavior causes ETH loss
  LST Impact: Socialized across all holders
  LRT Impact: Additional AVS slashing exposure
  Mitigation:
    - Choose protocols with slashing insurance
    - Diversify across LST providers
    - Monitor operator performance

PEG DEVIATION RISK:
  Description: LST trades below ETH value
  Causes:
    - Large sellers (redemption queue)
    - Smart contract concerns
    - Market panic
  Historical:
    - stETH depegged to 0.93 during 3AC collapse
    - Recovered after withdrawals enabled
  Mitigation:
    - Maintain exit liquidity
    - Don't leverage during depegs
    - Use limit orders

SMART CONTRACT RISK:
  Description: Bugs in protocol code
  Impact: Total loss of funds
  Mitigation:
    - Use battle-tested protocols
    - Check audit history
    - Cover with Nexus Mutual

CENTRALIZATION RISK:
  Description: Single points of failure
  Examples:
    - Lido's curated operator set
    - Coinbase's centralized operation
  Mitigation:
    - Prefer permissionless protocols
    - Support decentralized alternatives

LIQUIDITY RISK:
  Description: Unable to exit position
  Scenarios:
    - Withdrawal queue delays
    - DEX liquidity dries up
  Mitigation:
    - Check redemption times
    - Monitor DEX liquidity
    - Maintain reserves

REGULATORY RISK:
  Description: Government restrictions
  Potential:
    - LSTs classified as securities
    - Staking banned in jurisdictions
  Mitigation:
    - Geographic diversification
    - Use non-custodial protocols
```

---

## FIRMA

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  NEURONA: LIQUID STAKING & LSTs                                                ║
║  Dominio: C40006 - Liquid Staking Derivatives                                  ║
║  Versión: 1.0.0                                                                ║
║  Última actualización: 2024-12-29                                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```
