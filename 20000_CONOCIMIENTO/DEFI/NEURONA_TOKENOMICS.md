# NEURONA: TOKENOMICS & TOKEN DESIGN
## C40008 - Crypto-Economic Design

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  CIPHER NEURONA: TOKENOMICS                                                    ║
║  Dominio: Token Design, Distribution, Vesting, Value Accrual                   ║
║  Estado: ACTIVA                                                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. TOKENOMICS FUNDAMENTALS

### 1.1 Token Functions

```
TOKEN UTILITY FRAMEWORK
═══════════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────────────┐
│                      TOKEN UTILITY TYPES                                │
├────────────────┬───────────────────────────────────────────────────────┤
│ GOVERNANCE     │ Vote on protocol decisions                            │
│                │ Examples: UNI, AAVE, CRV                              │
│                │ Value: Control over treasury and parameters           │
├────────────────┼───────────────────────────────────────────────────────┤
│ UTILITY        │ Required to use protocol features                     │
│                │ Examples: LINK (oracle payments), FIL (storage)       │
│                │ Value: Demand driven by protocol usage                │
├────────────────┼───────────────────────────────────────────────────────┤
│ STAKING        │ Stake for rewards or security                         │
│                │ Examples: ETH, ATOM, SOL                              │
│                │ Value: Yield + network security participation         │
├────────────────┼───────────────────────────────────────────────────────┤
│ FEE CAPTURE    │ Receive share of protocol fees                        │
│                │ Examples: GMX, dYdX, SNX                              │
│                │ Value: Direct cash flow from usage                    │
├────────────────┼───────────────────────────────────────────────────────┤
│ COLLATERAL     │ Use as collateral in DeFi                             │
│                │ Examples: ETH, WBTC                                   │
│                │ Value: Enables leverage and borrowing                 │
├────────────────┼───────────────────────────────────────────────────────┤
│ WORK TOKEN     │ Stake to perform work and earn fees                   │
│                │ Examples: KEEP, GRT, LPT                              │
│                │ Value: Revenue from providing service                 │
└────────────────┴───────────────────────────────────────────────────────┘
```

### 1.2 Supply Mechanics

```
TOKEN SUPPLY MODELS
═══════════════════════════════════════════════════════════════════════

1. FIXED SUPPLY (Deflationary potential):
┌────────────────────────────────────────────────────────────────────────┐
│  Total Supply: 21,000,000 (Bitcoin)                                    │
│  ├── No new issuance after cap                                        │
│  ├── Burns can make deflationary                                      │
│  └── Scarcity drives value if demand exists                           │
│                                                                         │
│  Examples: BTC, YFI (30,000), MKR (1,000,000)                         │
└────────────────────────────────────────────────────────────────────────┘

2. INFLATIONARY (Continuous emission):
┌────────────────────────────────────────────────────────────────────────┐
│  New tokens minted over time                                           │
│  ├── Rewards for staking/security                                     │
│  ├── Liquidity incentives                                             │
│  └── Dilutes holders if not staked                                    │
│                                                                         │
│  Examples: ETH (pre-merge), ATOM, DOT                                  │
│  Rate: Usually 2-10% annual                                           │
└────────────────────────────────────────────────────────────────────────┘

3. DUAL-TOKEN (Utility + Governance):
┌────────────────────────────────────────────────────────────────────────┐
│  Two tokens with different purposes                                    │
│  ├── Utility token: Pay for services (often stable/pegged)            │
│  └── Governance token: Capture protocol value                         │
│                                                                         │
│  Examples:                                                             │
│  ├── Axie: AXS (governance) + SLP (utility/earnings)                  │
│  ├── MakerDAO: MKR (governance) + DAI (stablecoin)                   │
│  └── GMX: GMX (governance) + GLP (liquidity token)                   │
└────────────────────────────────────────────────────────────────────────┘

4. ELASTIC/REBASE (Algorithmic supply):
┌────────────────────────────────────────────────────────────────────────┐
│  Supply adjusts based on price                                         │
│  ├── Price > target → Supply expands (reward holders)                 │
│  ├── Price < target → Supply contracts (dilute holders)               │
│  └── Goal: Maintain price stability                                   │
│                                                                         │
│  Examples: AMPL, OHM (rebasing + bonding)                             │
│  Risk: Reflexive death spirals                                        │
└────────────────────────────────────────────────────────────────────────┘

5. BURN MECHANISMS:
┌────────────────────────────────────────────────────────────────────────┐
│  Tokens destroyed, reducing supply                                     │
│                                                                         │
│  Types:                                                                │
│  ├── Fee burns: ETH EIP-1559, BNB quarterly burns                     │
│  ├── Buyback & burn: Protocol uses revenue to buy and burn           │
│  └── Usage burns: Tokens consumed on use (LUNA for UST minting)      │
│                                                                         │
│  Examples: ETH (~1.5%/year), BNB, SHIB                                │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. TOKEN DISTRIBUTION

### 2.1 Allocation Framework

```
TYPICAL TOKEN ALLOCATION
═══════════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────────────┐
│                    ALLOCATION BREAKDOWN                                 │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ COMMUNITY & ECOSYSTEM                         40-60%             │   │
│  │ ├── Community rewards/airdrops               10-20%              │   │
│  │ ├── Ecosystem fund                           10-20%              │   │
│  │ ├── Liquidity mining                         10-20%              │   │
│  │ └── Future incentives                         5-10%              │   │
│  │                                                                   │   │
│  │ TEAM & ADVISORS                               15-25%             │   │
│  │ ├── Core team                                10-20%              │   │
│  │ └── Advisors                                  2-5%               │   │
│  │                                                                   │   │
│  │ INVESTORS                                     15-30%             │   │
│  │ ├── Seed round                                5-10%              │   │
│  │ ├── Private round                             5-15%              │   │
│  │ └── Public sale                               2-10%              │   │
│  │                                                                   │   │
│  │ TREASURY/DAO                                  10-20%             │   │
│  │ └── Protocol-controlled funds                10-20%              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
├────────────────────────────────────────────────────────────────────────┤
│                    VESTING SCHEDULES                                    │
│                                                                         │
│  Team:     4-year vest, 1-year cliff, monthly/quarterly unlock        │
│  Investors: 1-3 year vest, 6-12 month cliff                            │
│  Community: Often no cliff, immediate or gradual unlock               │
│  Treasury: Unlocked but governance-controlled                          │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Vesting Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/**
 * @title TokenVesting
 * @notice Linear vesting with cliff for team/investor allocations
 */
contract TokenVesting {
    using SafeERC20 for IERC20;

    struct VestingSchedule {
        address beneficiary;
        uint256 totalAmount;
        uint256 releasedAmount;
        uint256 startTime;
        uint256 cliffDuration;
        uint256 vestingDuration;
        bool revocable;
        bool revoked;
    }

    IERC20 public immutable token;
    address public admin;

    mapping(bytes32 => VestingSchedule) public vestingSchedules;
    mapping(address => uint256) public vestingCount;

    // Total amount being vested
    uint256 public vestingSchedulesTotalAmount;

    event VestingScheduleCreated(
        bytes32 indexed vestingScheduleId,
        address indexed beneficiary,
        uint256 amount,
        uint256 startTime,
        uint256 cliff,
        uint256 duration
    );

    event Released(
        bytes32 indexed vestingScheduleId,
        address indexed beneficiary,
        uint256 amount
    );

    event Revoked(bytes32 indexed vestingScheduleId, uint256 refundAmount);

    constructor(address _token) {
        token = IERC20(_token);
        admin = msg.sender;
    }

    /**
     * @notice Create new vesting schedule
     */
    function createVestingSchedule(
        address _beneficiary,
        uint256 _amount,
        uint256 _startTime,
        uint256 _cliffDuration,
        uint256 _vestingDuration,
        bool _revocable
    ) external onlyAdmin returns (bytes32 vestingScheduleId) {
        require(_beneficiary != address(0), "Invalid beneficiary");
        require(_amount > 0, "Amount must be > 0");
        require(_vestingDuration > 0, "Duration must be > 0");
        require(_vestingDuration >= _cliffDuration, "Duration < cliff");

        // Transfer tokens to contract
        token.safeTransferFrom(msg.sender, address(this), _amount);

        vestingScheduleId = computeVestingScheduleId(
            _beneficiary,
            vestingCount[_beneficiary]
        );

        vestingSchedules[vestingScheduleId] = VestingSchedule({
            beneficiary: _beneficiary,
            totalAmount: _amount,
            releasedAmount: 0,
            startTime: _startTime,
            cliffDuration: _cliffDuration,
            vestingDuration: _vestingDuration,
            revocable: _revocable,
            revoked: false
        });

        vestingCount[_beneficiary]++;
        vestingSchedulesTotalAmount += _amount;

        emit VestingScheduleCreated(
            vestingScheduleId,
            _beneficiary,
            _amount,
            _startTime,
            _cliffDuration,
            _vestingDuration
        );
    }

    /**
     * @notice Release vested tokens
     */
    function release(bytes32 _vestingScheduleId) external {
        VestingSchedule storage schedule = vestingSchedules[_vestingScheduleId];

        require(!schedule.revoked, "Schedule revoked");
        require(
            msg.sender == schedule.beneficiary || msg.sender == admin,
            "Not authorized"
        );

        uint256 releasable = computeReleasableAmount(schedule);
        require(releasable > 0, "Nothing to release");

        schedule.releasedAmount += releasable;
        vestingSchedulesTotalAmount -= releasable;

        token.safeTransfer(schedule.beneficiary, releasable);

        emit Released(_vestingScheduleId, schedule.beneficiary, releasable);
    }

    /**
     * @notice Revoke vesting (admin only, if revocable)
     */
    function revoke(bytes32 _vestingScheduleId) external onlyAdmin {
        VestingSchedule storage schedule = vestingSchedules[_vestingScheduleId];

        require(schedule.revocable, "Not revocable");
        require(!schedule.revoked, "Already revoked");

        uint256 releasable = computeReleasableAmount(schedule);

        // Release vested portion to beneficiary
        if (releasable > 0) {
            schedule.releasedAmount += releasable;
            token.safeTransfer(schedule.beneficiary, releasable);
        }

        // Return unvested to admin
        uint256 refund = schedule.totalAmount - schedule.releasedAmount;

        schedule.revoked = true;
        vestingSchedulesTotalAmount -= refund;

        if (refund > 0) {
            token.safeTransfer(admin, refund);
        }

        emit Revoked(_vestingScheduleId, refund);
    }

    /**
     * @notice Compute releasable amount
     */
    function computeReleasableAmount(
        VestingSchedule memory _schedule
    ) public view returns (uint256) {
        return computeVestedAmount(_schedule) - _schedule.releasedAmount;
    }

    /**
     * @notice Compute vested amount based on time
     */
    function computeVestedAmount(
        VestingSchedule memory _schedule
    ) public view returns (uint256) {
        if (_schedule.revoked) {
            return _schedule.releasedAmount;
        }

        uint256 currentTime = block.timestamp;

        // Before cliff
        if (currentTime < _schedule.startTime + _schedule.cliffDuration) {
            return 0;
        }

        // After vesting complete
        if (currentTime >= _schedule.startTime + _schedule.vestingDuration) {
            return _schedule.totalAmount;
        }

        // Linear vesting
        uint256 timeFromStart = currentTime - _schedule.startTime;
        uint256 vestedAmount = (_schedule.totalAmount * timeFromStart) /
            _schedule.vestingDuration;

        return vestedAmount;
    }

    /**
     * @notice Get vesting schedule details
     */
    function getVestingSchedule(
        bytes32 _vestingScheduleId
    ) external view returns (VestingSchedule memory) {
        return vestingSchedules[_vestingScheduleId];
    }

    /**
     * @notice Compute vesting schedule ID
     */
    function computeVestingScheduleId(
        address _beneficiary,
        uint256 _index
    ) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(_beneficiary, _index));
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Not admin");
        _;
    }
}
```

---

## 3. VALUE ACCRUAL MECHANISMS

### 3.1 Fee Distribution Models

```
VALUE ACCRUAL PATTERNS
═══════════════════════════════════════════════════════════════════════

1. DIRECT FEE SHARING (Real Yield):
┌────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Protocol Fees ──→ Distributed to Token Stakers                        │
│                                                                         │
│  Examples:                                                             │
│  ├── GMX: 30% of fees to GMX stakers in ETH/AVAX                      │
│  ├── dYdX: Trading fees to stakers                                    │
│  └── Curve: Trading fees to veCRV holders                             │
│                                                                         │
│  Pros: Direct cash flow, sustainable                                   │
│  Cons: Tax implications, requires usage                               │
└────────────────────────────────────────────────────────────────────────┘

2. BUYBACK & BURN:
┌────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Protocol Fees ──→ Buy Token ──→ Burn Token                            │
│                                                                         │
│  Examples:                                                             │
│  ├── Binance: Quarterly BNB burns                                     │
│  ├── MakerDAO: Buy & burn MKR from surplus                            │
│  └── SushiSwap: xSUSHI buybacks                                       │
│                                                                         │
│  Pros: Reduces supply, no tax event for holders                       │
│  Cons: Doesn't create direct yield                                    │
└────────────────────────────────────────────────────────────────────────┘

3. BUYBACK & DISTRIBUTE:
┌────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Protocol Fees ──→ Buy Token ──→ Distribute to Stakers                 │
│                                                                         │
│  Examples:                                                             │
│  ├── Olympus: OHM from bonds distributed to stakers                   │
│  └── Various: Compound rewards to stakers                              │
│                                                                         │
│  Pros: Increases token holdings                                        │
│  Cons: Can be dilutive, tax implications                              │
└────────────────────────────────────────────────────────────────────────┘

4. VOTE ESCROW (ve-Model):
┌────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Lock Token ──→ Receive veToken ──→ Voting Power + Boosted Rewards    │
│                                                                         │
│  Lock Duration → More veToken:                                         │
│  1 year lock: 1 CRV = 0.25 veCRV                                      │
│  4 year lock: 1 CRV = 1 veCRV                                         │
│                                                                         │
│  Benefits:                                                             │
│  ├── Governance voting power                                          │
│  ├── Trading fee share (proportional to veCRV)                        │
│  ├── Boosted liquidity mining rewards                                 │
│  └── Bribe income from other protocols                                │
│                                                                         │
│  Examples: Curve (veCRV), Balancer (veBAL), Frax (veFXS)              │
└────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Vote Escrow Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title VoteEscrow
 * @notice ve-token implementation (Curve-style)
 */
contract VoteEscrow is ReentrancyGuard {
    // Underlying token
    IERC20 public token;

    // Lock duration limits
    uint256 public constant MAXTIME = 4 * 365 days; // 4 years
    uint256 public constant MINTIME = 7 days;       // 1 week minimum

    // Point structure for balance tracking
    struct Point {
        int128 bias;      // Current balance
        int128 slope;     // Rate of decay
        uint256 ts;       // Timestamp
        uint256 blk;      // Block number
    }

    // Locked balance
    struct LockedBalance {
        int128 amount;
        uint256 end;
    }

    // User locks
    mapping(address => LockedBalance) public locked;

    // Global state
    uint256 public epoch;
    mapping(uint256 => Point) public pointHistory;
    mapping(address => mapping(uint256 => Point)) public userPointHistory;
    mapping(address => uint256) public userPointEpoch;

    // Slope changes at future timestamps
    mapping(uint256 => int128) public slopeChanges;

    // Total supply tracking
    uint256 public supply;

    event Deposit(
        address indexed provider,
        uint256 value,
        uint256 indexed locktime,
        uint256 ts
    );

    event Withdraw(address indexed provider, uint256 value, uint256 ts);

    constructor(address _token) {
        token = IERC20(_token);
        pointHistory[0].blk = block.number;
        pointHistory[0].ts = block.timestamp;
    }

    /**
     * @notice Create lock
     * @param _value Amount to lock
     * @param _unlockTime Future unlock timestamp
     */
    function createLock(
        uint256 _value,
        uint256 _unlockTime
    ) external nonReentrant {
        require(_value > 0, "Need non-zero value");

        LockedBalance memory existingLock = locked[msg.sender];
        require(existingLock.amount == 0, "Withdraw existing lock first");

        uint256 unlockTime = (_unlockTime / 1 weeks) * 1 weeks; // Round down to week
        require(unlockTime > block.timestamp, "Must be future");
        require(
            unlockTime <= block.timestamp + MAXTIME,
            "Exceeds max lock time"
        );

        _depositFor(msg.sender, _value, unlockTime, existingLock, 1);
    }

    /**
     * @notice Increase lock amount
     */
    function increaseAmount(uint256 _value) external nonReentrant {
        LockedBalance memory existingLock = locked[msg.sender];

        require(_value > 0, "Need non-zero value");
        require(existingLock.amount > 0, "No existing lock");
        require(existingLock.end > block.timestamp, "Lock expired");

        _depositFor(msg.sender, _value, 0, existingLock, 2);
    }

    /**
     * @notice Extend lock duration
     */
    function increaseUnlockTime(uint256 _unlockTime) external nonReentrant {
        LockedBalance memory existingLock = locked[msg.sender];

        uint256 unlockTime = (_unlockTime / 1 weeks) * 1 weeks;

        require(existingLock.amount > 0, "No existing lock");
        require(existingLock.end > block.timestamp, "Lock expired");
        require(unlockTime > existingLock.end, "Must increase");
        require(
            unlockTime <= block.timestamp + MAXTIME,
            "Exceeds max lock time"
        );

        _depositFor(msg.sender, 0, unlockTime, existingLock, 3);
    }

    /**
     * @notice Internal deposit logic
     */
    function _depositFor(
        address _addr,
        uint256 _value,
        uint256 _unlockTime,
        LockedBalance memory _oldLocked,
        uint256 _type
    ) internal {
        LockedBalance memory newLocked = LockedBalance({
            amount: _oldLocked.amount,
            end: _oldLocked.end
        });

        supply += _value;

        // Update lock
        newLocked.amount += int128(int256(_value));
        if (_unlockTime != 0) {
            newLocked.end = _unlockTime;
        }
        locked[_addr] = newLocked;

        // Update checkpoints
        _checkpoint(_addr, _oldLocked, newLocked);

        // Transfer tokens
        if (_value > 0) {
            token.transferFrom(_addr, address(this), _value);
        }

        emit Deposit(_addr, _value, newLocked.end, block.timestamp);
    }

    /**
     * @notice Withdraw all tokens after lock expires
     */
    function withdraw() external nonReentrant {
        LockedBalance memory existingLock = locked[msg.sender];

        require(block.timestamp >= existingLock.end, "Lock not expired");

        uint256 value = uint256(int256(existingLock.amount));

        LockedBalance memory emptyLock;
        locked[msg.sender] = emptyLock;
        supply -= value;

        _checkpoint(msg.sender, existingLock, emptyLock);

        token.transfer(msg.sender, value);

        emit Withdraw(msg.sender, value, block.timestamp);
    }

    /**
     * @notice Get current voting power
     */
    function balanceOf(address _addr) external view returns (uint256) {
        return balanceOfAt(_addr, block.timestamp);
    }

    /**
     * @notice Get voting power at timestamp
     */
    function balanceOfAt(
        address _addr,
        uint256 _t
    ) public view returns (uint256) {
        uint256 epoch_ = userPointEpoch[_addr];
        if (epoch_ == 0) return 0;

        Point memory lastPoint = userPointHistory[_addr][epoch_];

        // Calculate balance decay
        int128 biasDecay = lastPoint.slope *
            int128(int256(_t - lastPoint.ts));

        int128 balance = lastPoint.bias - biasDecay;

        return balance > 0 ? uint256(int256(balance)) : 0;
    }

    /**
     * @notice Get total voting power
     */
    function totalSupply() external view returns (uint256) {
        return totalSupplyAt(block.timestamp);
    }

    /**
     * @notice Get total voting power at timestamp
     */
    function totalSupplyAt(uint256 _t) public view returns (uint256) {
        Point memory lastPoint = pointHistory[epoch];

        int128 biasDecay = lastPoint.slope *
            int128(int256(_t - lastPoint.ts));

        int128 balance = lastPoint.bias - biasDecay;

        return balance > 0 ? uint256(int256(balance)) : 0;
    }

    /**
     * @notice Record global and user checkpoints
     */
    function _checkpoint(
        address _addr,
        LockedBalance memory _oldLocked,
        LockedBalance memory _newLocked
    ) internal {
        // Complex checkpoint logic for balance tracking
        // Simplified here - full implementation tracks decay curves

        Point memory userOldPoint;
        Point memory userNewPoint;

        // Calculate old and new slopes
        if (_oldLocked.end > block.timestamp && _oldLocked.amount > 0) {
            userOldPoint.slope = _oldLocked.amount / int128(int256(MAXTIME));
            userOldPoint.bias = userOldPoint.slope *
                int128(int256(_oldLocked.end - block.timestamp));
        }

        if (_newLocked.end > block.timestamp && _newLocked.amount > 0) {
            userNewPoint.slope = _newLocked.amount / int128(int256(MAXTIME));
            userNewPoint.bias = userNewPoint.slope *
                int128(int256(_newLocked.end - block.timestamp));
        }

        // Update user point
        uint256 userEpoch = userPointEpoch[_addr] + 1;
        userPointEpoch[_addr] = userEpoch;
        userNewPoint.ts = block.timestamp;
        userNewPoint.blk = block.number;
        userPointHistory[_addr][userEpoch] = userNewPoint;

        // Update global point
        epoch++;
        Point memory newPoint = pointHistory[epoch - 1];
        newPoint.bias += userNewPoint.bias - userOldPoint.bias;
        newPoint.slope += userNewPoint.slope - userOldPoint.slope;
        newPoint.ts = block.timestamp;
        newPoint.blk = block.number;
        pointHistory[epoch] = newPoint;

        // Schedule slope changes
        if (_oldLocked.end > block.timestamp) {
            slopeChanges[_oldLocked.end] += userOldPoint.slope;
        }
        if (_newLocked.end > block.timestamp) {
            slopeChanges[_newLocked.end] -= userNewPoint.slope;
        }
    }
}
```

---

## 4. EMISSION SCHEDULES

### 4.1 Emission Patterns

```
EMISSION SCHEDULE MODELS
═══════════════════════════════════════════════════════════════════════

1. BITCOIN HALVING (Geometric Decay):
┌────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Emissions │████████████████                                           │
│            │        ████████                                           │
│            │            ████                                           │
│            │              ██                                           │
│            │               █                                           │
│            └──────────────────────────────────────→ Time              │
│                                                                         │
│  Formula: reward = initial_reward / 2^(blocks / halving_interval)     │
│  Example: 50 → 25 → 12.5 → 6.25 BTC per block                         │
└────────────────────────────────────────────────────────────────────────┘

2. LINEAR DECAY:
┌────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Emissions │████                                                       │
│            │███                                                        │
│            │██                                                         │
│            │█                                                          │
│            │                                                           │
│            └──────────────────────────────────────→ Time              │
│                                                                         │
│  Formula: reward = max(0, initial - decay_rate × time)                │
│  Example: 100 - 0.5 per day = 0 after 200 days                        │
└────────────────────────────────────────────────────────────────────────┘

3. EXPONENTIAL DECAY:
┌────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Emissions │██████████                                                 │
│            │  ████                                                     │
│            │    ██                                                     │
│            │     █                                                     │
│            │      ─────────                                            │
│            └──────────────────────────────────────→ Time              │
│                                                                         │
│  Formula: reward = initial × e^(-decay × time)                        │
│  Never reaches 0, but asymptotically approaches                       │
└────────────────────────────────────────────────────────────────────────┘

4. FIXED PERIOD PHASES:
┌────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Phase 1: Launch (3 months) - 40% emissions                           │
│  Phase 2: Growth (6 months) - 30% emissions                           │
│  Phase 3: Maturity (12 months) - 20% emissions                        │
│  Phase 4: Maintenance (ongoing) - 10% emissions                       │
│                                                                         │
│  Common in: New DeFi protocols, gaming tokens                         │
└────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Emission Controller

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title EmissionController
 * @notice Controls token emission schedule
 */
contract EmissionController {
    // Token to emit
    address public token;

    // Emission rate per second
    uint256 public emissionRate;

    // Decay rate (basis points per epoch)
    uint256 public decayRate = 100; // 1% per epoch

    // Epoch duration
    uint256 public epochDuration = 7 days;

    // Tracking
    uint256 public lastUpdateTime;
    uint256 public currentEpoch;
    uint256 public totalEmitted;

    // Max supply cap
    uint256 public maxSupply;

    // Emission recipients
    struct Recipient {
        address addr;
        uint256 share; // basis points out of 10000
    }
    Recipient[] public recipients;

    event EpochAdvanced(uint256 indexed epoch, uint256 newRate);
    event EmissionDistributed(address indexed recipient, uint256 amount);

    constructor(
        address _token,
        uint256 _initialRate,
        uint256 _maxSupply
    ) {
        token = _token;
        emissionRate = _initialRate;
        maxSupply = _maxSupply;
        lastUpdateTime = block.timestamp;
    }

    /**
     * @notice Advance to next epoch (reduces emission rate)
     */
    function advanceEpoch() external {
        require(
            block.timestamp >= lastUpdateTime + epochDuration,
            "Epoch not ended"
        );

        // Apply decay
        emissionRate = (emissionRate * (10000 - decayRate)) / 10000;

        currentEpoch++;
        lastUpdateTime = block.timestamp;

        emit EpochAdvanced(currentEpoch, emissionRate);
    }

    /**
     * @notice Distribute emissions to recipients
     */
    function distribute() external {
        uint256 elapsed = block.timestamp - lastUpdateTime;
        uint256 toEmit = elapsed * emissionRate;

        // Check max supply
        if (totalEmitted + toEmit > maxSupply) {
            toEmit = maxSupply - totalEmitted;
        }

        if (toEmit == 0) return;

        totalEmitted += toEmit;
        lastUpdateTime = block.timestamp;

        // Distribute to recipients
        for (uint i = 0; i < recipients.length; i++) {
            uint256 amount = (toEmit * recipients[i].share) / 10000;
            // Mint or transfer tokens
            // IMintable(token).mint(recipients[i].addr, amount);

            emit EmissionDistributed(recipients[i].addr, amount);
        }
    }

    /**
     * @notice Get pending emissions
     */
    function pendingEmissions() external view returns (uint256) {
        uint256 elapsed = block.timestamp - lastUpdateTime;
        uint256 pending = elapsed * emissionRate;

        if (totalEmitted + pending > maxSupply) {
            pending = maxSupply - totalEmitted;
        }

        return pending;
    }

    /**
     * @notice Calculate emissions for future epochs
     */
    function projectEmissions(
        uint256 _epochs
    ) external view returns (uint256 total, uint256[] memory perEpoch) {
        perEpoch = new uint256[](_epochs);
        uint256 rate = emissionRate;

        for (uint256 i = 0; i < _epochs; i++) {
            uint256 epochEmission = rate * epochDuration;
            perEpoch[i] = epochEmission;
            total += epochEmission;
            rate = (rate * (10000 - decayRate)) / 10000;
        }
    }

    /**
     * @notice Add emission recipient
     */
    function addRecipient(address _addr, uint256 _share) external {
        recipients.push(Recipient({
            addr: _addr,
            share: _share
        }));
    }
}
```

---

## 5. TOKENOMICS ANALYSIS FRAMEWORK

```yaml
TOKENOMICS EVALUATION CHECKLIST:
══════════════════════════════════════════════════════════════════════════

SUPPLY ANALYSIS:
  □ Total supply and max supply
  □ Current circulating supply
  □ Emission schedule and inflation rate
  □ Burn mechanisms (if any)
  □ Unlock schedule and vesting cliffs

DISTRIBUTION:
  □ Team allocation and vesting
  □ Investor allocation and terms
  □ Community/ecosystem allocation
  □ Treasury size and control
  □ Initial circulating vs fully diluted

VALUE ACCRUAL:
  □ How does token capture protocol value?
  □ Fee distribution mechanism
  □ Buy-back or burn programs
  □ Staking rewards source
  □ Governance rights and value

DEMAND DRIVERS:
  □ Required for protocol use?
  □ Staking incentives (yield)
  □ Governance participation value
  □ Speculation potential
  □ Network effects

RED FLAGS:
  ⚠️ >30% team allocation
  ⚠️ Short vesting (<2 years)
  ⚠️ High inflation without burns
  ⚠️ No clear value accrual
  ⚠️ Large unlocks coming soon
  ⚠️ Token not needed for protocol

GREEN FLAGS:
  ✓ Long vesting (4+ years)
  ✓ Real yield from fees
  ✓ Deflationary mechanisms
  ✓ Strong governance rights
  ✓ Required for protocol function
  ✓ Transparent treasury management
```

---

## 6. CASE STUDIES

```
TOKENOMICS CASE STUDIES
═══════════════════════════════════════════════════════════════════════

CURVE (CRV) - Vote Escrow Pioneer:
┌────────────────────────────────────────────────────────────────────────┐
│ Supply: 3.03B max, inflationary schedule                               │
│ Value Accrual: veCRV receives 50% trading fees + governance           │
│ Lock: Up to 4 years for max voting power                              │
│ Innovation: ve-model adopted by 100+ protocols                        │
│ Result: $2B+ TVL in vote-locked CRV                                   │
└────────────────────────────────────────────────────────────────────────┘

GMX - Real Yield Model:
┌────────────────────────────────────────────────────────────────────────┐
│ Supply: 13.25M max, minimal inflation                                  │
│ Value Accrual: 30% platform fees to GMX stakers in ETH/AVAX          │
│ Dual Token: GMX (governance) + GLP (liquidity)                        │
│ Result: 15-25% real yield, sustainable model                          │
└────────────────────────────────────────────────────────────────────────┘

UNI - Governance Token:
┌────────────────────────────────────────────────────────────────────────┐
│ Supply: 1B total, 4-year emission schedule                            │
│ Value Accrual: Governance only (fee switch not activated)             │
│ Distribution: 60% community, 40% team/investors                       │
│ Challenge: Limited utility beyond governance                          │
└────────────────────────────────────────────────────────────────────────┘

OHM - Rebasing Innovation:
┌────────────────────────────────────────────────────────────────────────┐
│ Supply: Elastic (rebase mechanism)                                     │
│ Value Accrual: Bonding + staking rebases                              │
│ Innovation: Protocol-owned liquidity concept                          │
│ Result: Massive rise then 99% crash - experimental model              │
└────────────────────────────────────────────────────────────────────────┘
```

---

## FIRMA

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  NEURONA: TOKENOMICS & TOKEN DESIGN                                            ║
║  Dominio: C40008 - Crypto-Economic Design                                      ║
║  Versión: 1.0.0                                                                ║
║  Última actualización: 2024-12-29                                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```
