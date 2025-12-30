# NEURONA: DERIVATIVES & PERPETUALS
## C40003 - DeFi Derivatives Mastery

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  CIPHER NEURONA: DERIVATIVES                                                   ║
║  Dominio: Perpetuals, Options, Futures, Synthetic Assets                       ║
║  Estado: ACTIVA                                                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. PERPETUAL FUTURES

### 1.1 Fundamentos de Perpetuals

```
PERPETUAL vs TRADITIONAL FUTURES
═══════════════════════════════════════════════════════════════════════

Traditional Futures:
├── Expiration date → Settlement required
├── Premium/discount to spot → Converges at expiry
├── Physical or cash settled
└── Rollover costs for long-term positions

Perpetual Swaps:
├── No expiration → Hold indefinitely
├── Funding rate mechanism → Price anchoring
├── Always cash settled
└── Continuous position management
```

### 1.2 Funding Rate Mechanism

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title PerpetualFundingRate
 * @notice Implementación del mecanismo de funding rate
 */
contract PerpetualFundingRate {
    // Funding rate interval (8 hours = 28800 seconds)
    uint256 public constant FUNDING_INTERVAL = 8 hours;

    // Funding rate cap (0.75% per interval max)
    int256 public constant MAX_FUNDING_RATE = 75; // basis points

    // Premium index cap
    int256 public constant PREMIUM_INDEX_CAP = 500; // basis points

    // Interest rate base (0.01% per 8h = 0.03% daily)
    int256 public constant INTEREST_RATE = 1; // basis points

    struct FundingData {
        int256 cumulativeFundingRate;
        int256 lastPremiumIndex;
        uint256 lastFundingTime;
        int256 currentFundingRate;
    }

    FundingData public fundingData;

    // Mark price from oracle
    int256 public markPrice;
    // Index price (spot reference)
    int256 public indexPrice;

    /**
     * @notice Calculate premium index
     * @dev Premium = (Mark Price - Index Price) / Index Price
     */
    function calculatePremiumIndex() public view returns (int256) {
        if (indexPrice == 0) return 0;

        // Premium in basis points
        int256 premium = ((markPrice - indexPrice) * 10000) / indexPrice;

        // Cap the premium index
        if (premium > PREMIUM_INDEX_CAP) return PREMIUM_INDEX_CAP;
        if (premium < -PREMIUM_INDEX_CAP) return -PREMIUM_INDEX_CAP;

        return premium;
    }

    /**
     * @notice Calculate funding rate
     * @dev Funding Rate = Premium Index + clamp(Interest Rate - Premium Index, 0.05%, -0.05%)
     */
    function calculateFundingRate() public view returns (int256) {
        int256 premiumIndex = calculatePremiumIndex();

        // Interest rate component
        int256 interestComponent = INTEREST_RATE - premiumIndex;

        // Clamp interest component to ±5 basis points
        if (interestComponent > 5) interestComponent = 5;
        if (interestComponent < -5) interestComponent = -5;

        int256 fundingRate = premiumIndex + interestComponent;

        // Cap funding rate
        if (fundingRate > MAX_FUNDING_RATE) return MAX_FUNDING_RATE;
        if (fundingRate < -MAX_FUNDING_RATE) return -MAX_FUNDING_RATE;

        return fundingRate;
    }

    /**
     * @notice Update funding rate
     * @dev Called every funding interval
     */
    function updateFunding() external {
        require(
            block.timestamp >= fundingData.lastFundingTime + FUNDING_INTERVAL,
            "Funding not due"
        );

        int256 newFundingRate = calculateFundingRate();

        fundingData.cumulativeFundingRate += newFundingRate;
        fundingData.currentFundingRate = newFundingRate;
        fundingData.lastPremiumIndex = calculatePremiumIndex();
        fundingData.lastFundingTime = block.timestamp;
    }

    /**
     * @notice Calculate funding payment for a position
     * @param positionSize Size in base currency (positive=long, negative=short)
     * @param entryFundingRate Cumulative funding at position open
     */
    function calculateFundingPayment(
        int256 positionSize,
        int256 entryFundingRate
    ) public view returns (int256) {
        int256 fundingDelta = fundingData.cumulativeFundingRate - entryFundingRate;

        // Funding payment = Position Size × Funding Delta
        // Positive funding: longs pay shorts
        // Negative funding: shorts pay longs
        return (positionSize * fundingDelta) / 10000; // basis points to decimal
    }
}
```

### 1.3 Virtual AMM (vAMM) Perpetuals

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title VirtualAMM
 * @notice vAMM for perpetual futures (Perpetual Protocol style)
 * @dev No actual liquidity - virtual reserves track positions
 */
contract VirtualAMM is ReentrancyGuard {
    // Virtual reserves
    uint256 public baseAssetReserve;  // ETH equivalent
    uint256 public quoteAssetReserve; // USD equivalent

    // Constant product
    uint256 public k;

    // Collateral token (USDC)
    IERC20 public collateral;

    // Position tracking
    struct Position {
        int256 size;           // Positive = long, negative = short
        uint256 margin;        // Collateral deposited
        uint256 openNotional;  // Value at entry
        int256 entryFundingIndex;
    }

    mapping(address => Position) public positions;

    // Global position tracking
    int256 public totalLongPositionSize;
    int256 public totalShortPositionSize;

    // Insurance fund
    uint256 public insuranceFund;

    // Leverage limits
    uint256 public constant MAX_LEVERAGE = 10;
    uint256 public constant MAINTENANCE_MARGIN_RATIO = 625; // 6.25%

    event PositionChanged(
        address indexed trader,
        int256 newSize,
        uint256 margin,
        uint256 openNotional
    );

    constructor(
        address _collateral,
        uint256 _baseReserve,
        uint256 _quoteReserve
    ) {
        collateral = IERC20(_collateral);
        baseAssetReserve = _baseReserve;
        quoteAssetReserve = _quoteReserve;
        k = _baseReserve * _quoteReserve;
    }

    /**
     * @notice Get current mark price from vAMM
     */
    function getMarkPrice() public view returns (uint256) {
        return (quoteAssetReserve * 1e18) / baseAssetReserve;
    }

    /**
     * @notice Open or increase long position
     * @param _margin Collateral to deposit
     * @param _leverage Leverage multiplier (1-10)
     */
    function openLong(
        uint256 _margin,
        uint256 _leverage
    ) external nonReentrant returns (uint256 baseAmount) {
        require(_leverage > 0 && _leverage <= MAX_LEVERAGE, "Invalid leverage");

        // Transfer collateral
        collateral.transferFrom(msg.sender, address(this), _margin);

        // Calculate notional value
        uint256 notional = _margin * _leverage;

        // Calculate base asset received (swap quote for base)
        baseAmount = _swapQuoteForBase(notional);

        // Update position
        Position storage pos = positions[msg.sender];
        pos.size += int256(baseAmount);
        pos.margin += _margin;
        pos.openNotional += notional;

        totalLongPositionSize += int256(baseAmount);

        emit PositionChanged(msg.sender, pos.size, pos.margin, pos.openNotional);
    }

    /**
     * @notice Open or increase short position
     */
    function openShort(
        uint256 _margin,
        uint256 _leverage
    ) external nonReentrant returns (uint256 baseAmount) {
        require(_leverage > 0 && _leverage <= MAX_LEVERAGE, "Invalid leverage");

        collateral.transferFrom(msg.sender, address(this), _margin);

        uint256 notional = _margin * _leverage;

        // Calculate base asset sold (swap base for quote)
        baseAmount = _swapBaseForQuote(notional);

        Position storage pos = positions[msg.sender];
        pos.size -= int256(baseAmount);
        pos.margin += _margin;
        pos.openNotional += notional;

        totalShortPositionSize += int256(baseAmount);

        emit PositionChanged(msg.sender, pos.size, pos.margin, pos.openNotional);
    }

    /**
     * @notice Close position fully or partially
     */
    function closePosition(uint256 _sizeToClose) external nonReentrant {
        Position storage pos = positions[msg.sender];
        require(pos.size != 0, "No position");

        uint256 absSize = pos.size > 0 ? uint256(pos.size) : uint256(-pos.size);
        require(_sizeToClose <= absSize, "Size exceeds position");

        // Calculate PnL
        int256 pnl = _calculatePnL(msg.sender, _sizeToClose);

        // Calculate margin to return
        uint256 marginToReturn = (pos.margin * _sizeToClose) / absSize;

        // Update position
        if (pos.size > 0) {
            pos.size -= int256(_sizeToClose);
            totalLongPositionSize -= int256(_sizeToClose);
            // Swap base back to quote (selling)
            _swapBaseForQuote(_sizeToClose);
        } else {
            pos.size += int256(_sizeToClose);
            totalShortPositionSize -= int256(_sizeToClose);
            // Swap quote back to base (buying to close)
            _swapQuoteForBase(_sizeToClose);
        }

        pos.margin -= marginToReturn;
        pos.openNotional -= (pos.openNotional * _sizeToClose) / absSize;

        // Transfer margin + PnL
        int256 totalReturn = int256(marginToReturn) + pnl;
        if (totalReturn > 0) {
            collateral.transfer(msg.sender, uint256(totalReturn));
        }

        emit PositionChanged(msg.sender, pos.size, pos.margin, pos.openNotional);
    }

    /**
     * @notice Liquidate undercollateralized position
     */
    function liquidate(address _trader) external nonReentrant {
        require(_isLiquidatable(_trader), "Position healthy");

        Position storage pos = positions[_trader];
        uint256 absSize = pos.size > 0 ? uint256(pos.size) : uint256(-pos.size);

        // Close entire position
        int256 pnl = _calculatePnL(_trader, absSize);

        // Liquidator reward (2.5% of position)
        uint256 liquidatorReward = (pos.margin * 250) / 10000;

        // Remaining goes to insurance fund (or covers bad debt)
        int256 remaining = int256(pos.margin) + pnl - int256(liquidatorReward);

        if (remaining > 0) {
            insuranceFund += uint256(remaining);
        } else {
            // Bad debt - covered by insurance fund
            if (insuranceFund >= uint256(-remaining)) {
                insuranceFund -= uint256(-remaining);
            }
        }

        // Update vAMM
        if (pos.size > 0) {
            totalLongPositionSize -= pos.size;
            _swapBaseForQuote(absSize);
        } else {
            totalShortPositionSize -= int256(absSize);
            _swapQuoteForBase(absSize);
        }

        // Clear position
        delete positions[_trader];

        // Pay liquidator
        collateral.transfer(msg.sender, liquidatorReward);
    }

    /**
     * @notice Check if position can be liquidated
     */
    function _isLiquidatable(address _trader) internal view returns (bool) {
        Position memory pos = positions[_trader];
        if (pos.size == 0) return false;

        uint256 absSize = pos.size > 0 ? uint256(pos.size) : uint256(-pos.size);
        int256 pnl = _calculatePnL(_trader, absSize);

        int256 accountValue = int256(pos.margin) + pnl;
        uint256 maintenanceMargin = (pos.openNotional * MAINTENANCE_MARGIN_RATIO) / 10000;

        return accountValue < int256(maintenanceMargin);
    }

    /**
     * @notice Calculate unrealized PnL
     */
    function _calculatePnL(address _trader, uint256 _size) internal view returns (int256) {
        Position memory pos = positions[_trader];
        uint256 absSize = pos.size > 0 ? uint256(pos.size) : uint256(-pos.size);

        uint256 entryPrice = (pos.openNotional * 1e18) / absSize;
        uint256 currentPrice = getMarkPrice();

        if (pos.size > 0) {
            // Long: profit if price up
            return int256((_size * currentPrice) / 1e18) - int256((_size * entryPrice) / 1e18);
        } else {
            // Short: profit if price down
            return int256((_size * entryPrice) / 1e18) - int256((_size * currentPrice) / 1e18);
        }
    }

    /**
     * @notice Swap quote for base (buy)
     */
    function _swapQuoteForBase(uint256 _quoteAmount) internal returns (uint256 baseAmount) {
        // x * y = k
        // (x - dx) * (y + dy) = k
        // dx = x - k/(y + dy)

        uint256 newQuoteReserve = quoteAssetReserve + _quoteAmount;
        uint256 newBaseReserve = k / newQuoteReserve;
        baseAmount = baseAssetReserve - newBaseReserve;

        baseAssetReserve = newBaseReserve;
        quoteAssetReserve = newQuoteReserve;
    }

    /**
     * @notice Swap base for quote (sell)
     */
    function _swapBaseForQuote(uint256 _baseAmount) internal returns (uint256 quoteAmount) {
        uint256 newBaseReserve = baseAssetReserve + _baseAmount;
        uint256 newQuoteReserve = k / newBaseReserve;
        quoteAmount = quoteAssetReserve - newQuoteReserve;

        baseAssetReserve = newBaseReserve;
        quoteAssetReserve = newQuoteReserve;
    }
}
```

---

## 2. ORDER BOOK PERPETUALS

### 2.1 Central Limit Order Book (dYdX Style)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title PerpetualOrderBook
 * @notice On-chain order book for perpetuals
 */
contract PerpetualOrderBook {
    struct Order {
        address trader;
        bool isBuy;          // true = buy/long, false = sell/short
        uint256 price;       // Price in quote currency
        uint256 size;        // Size in base currency
        uint256 filled;      // Amount already filled
        uint256 timestamp;
        bool reduceOnly;     // Only reduces existing position
    }

    // Order ID counter
    uint256 public nextOrderId;

    // All orders
    mapping(uint256 => Order) public orders;

    // Order book structure (price => order IDs)
    // Bids sorted descending, asks sorted ascending
    mapping(uint256 => uint256[]) public bidsAtPrice;
    mapping(uint256 => uint256[]) public asksAtPrice;

    // Sorted price levels
    uint256[] public bidPrices;  // Descending
    uint256[] public askPrices;  // Ascending

    // Tick size (minimum price increment)
    uint256 public constant TICK_SIZE = 1e15; // 0.001 USD

    event OrderPlaced(uint256 indexed orderId, address indexed trader, bool isBuy, uint256 price, uint256 size);
    event OrderFilled(uint256 indexed orderId, uint256 filledAmount, uint256 price);
    event OrderCancelled(uint256 indexed orderId);

    /**
     * @notice Place limit order
     */
    function placeLimitOrder(
        bool _isBuy,
        uint256 _price,
        uint256 _size,
        bool _reduceOnly
    ) external returns (uint256 orderId) {
        require(_price % TICK_SIZE == 0, "Invalid tick");
        require(_size > 0, "Invalid size");

        orderId = nextOrderId++;

        orders[orderId] = Order({
            trader: msg.sender,
            isBuy: _isBuy,
            price: _price,
            size: _size,
            filled: 0,
            timestamp: block.timestamp,
            reduceOnly: _reduceOnly
        });

        // Try to match immediately
        uint256 remaining = _matchOrder(orderId);

        // Add remaining to book
        if (remaining > 0) {
            if (_isBuy) {
                _insertBid(orderId, _price);
            } else {
                _insertAsk(orderId, _price);
            }
        }

        emit OrderPlaced(orderId, msg.sender, _isBuy, _price, _size);
    }

    /**
     * @notice Match order against book
     */
    function _matchOrder(uint256 _orderId) internal returns (uint256 remaining) {
        Order storage order = orders[_orderId];
        remaining = order.size - order.filled;

        if (order.isBuy) {
            // Match against asks (lowest first)
            for (uint i = 0; i < askPrices.length && remaining > 0; ) {
                uint256 askPrice = askPrices[i];

                // Stop if best ask > order price
                if (askPrice > order.price) break;

                remaining = _matchAtPrice(order, askPrice, asksAtPrice[askPrice], remaining);

                // Remove empty price level
                if (asksAtPrice[askPrice].length == 0) {
                    _removeAskPrice(i);
                } else {
                    i++;
                }
            }
        } else {
            // Match against bids (highest first)
            for (uint i = 0; i < bidPrices.length && remaining > 0; ) {
                uint256 bidPrice = bidPrices[i];

                // Stop if best bid < order price
                if (bidPrice < order.price) break;

                remaining = _matchAtPrice(order, bidPrice, bidsAtPrice[bidPrice], remaining);

                if (bidsAtPrice[bidPrice].length == 0) {
                    _removeBidPrice(i);
                } else {
                    i++;
                }
            }
        }
    }

    /**
     * @notice Match against orders at specific price
     */
    function _matchAtPrice(
        Order storage _taker,
        uint256 _price,
        uint256[] storage _makerOrders,
        uint256 _remaining
    ) internal returns (uint256) {
        for (uint i = 0; i < _makerOrders.length && _remaining > 0; ) {
            Order storage maker = orders[_makerOrders[i]];

            uint256 makerAvailable = maker.size - maker.filled;
            uint256 fillAmount = _remaining < makerAvailable ? _remaining : makerAvailable;

            // Execute trade
            maker.filled += fillAmount;
            _taker.filled += fillAmount;
            _remaining -= fillAmount;

            emit OrderFilled(_makerOrders[i], fillAmount, _price);
            emit OrderFilled(0, fillAmount, _price); // Taker fill

            // Remove fully filled maker order
            if (maker.filled == maker.size) {
                _removeOrderFromArray(_makerOrders, i);
            } else {
                i++;
            }
        }

        return _remaining;
    }

    /**
     * @notice Cancel order
     */
    function cancelOrder(uint256 _orderId) external {
        Order storage order = orders[_orderId];
        require(order.trader == msg.sender, "Not owner");
        require(order.filled < order.size, "Already filled");

        // Remove from book
        if (order.isBuy) {
            _removeOrderFromArray(bidsAtPrice[order.price], _findOrderIndex(bidsAtPrice[order.price], _orderId));
        } else {
            _removeOrderFromArray(asksAtPrice[order.price], _findOrderIndex(asksAtPrice[order.price], _orderId));
        }

        emit OrderCancelled(_orderId);
    }

    /**
     * @notice Get best bid and ask
     */
    function getBestBidAsk() external view returns (uint256 bestBid, uint256 bestAsk) {
        bestBid = bidPrices.length > 0 ? bidPrices[0] : 0;
        bestAsk = askPrices.length > 0 ? askPrices[0] : type(uint256).max;
    }

    // Helper functions for sorted arrays...
    function _insertBid(uint256 _orderId, uint256 _price) internal {
        bidsAtPrice[_price].push(_orderId);
        // Insert price in sorted position (descending)
        // Implementation omitted for brevity
    }

    function _insertAsk(uint256 _orderId, uint256 _price) internal {
        asksAtPrice[_price].push(_orderId);
        // Insert price in sorted position (ascending)
    }

    function _removeBidPrice(uint256 _index) internal {
        bidPrices[_index] = bidPrices[bidPrices.length - 1];
        bidPrices.pop();
        // Re-sort array
    }

    function _removeAskPrice(uint256 _index) internal {
        askPrices[_index] = askPrices[askPrices.length - 1];
        askPrices.pop();
    }

    function _removeOrderFromArray(uint256[] storage _arr, uint256 _index) internal {
        _arr[_index] = _arr[_arr.length - 1];
        _arr.pop();
    }

    function _findOrderIndex(uint256[] storage _arr, uint256 _orderId) internal view returns (uint256) {
        for (uint i = 0; i < _arr.length; i++) {
            if (_arr[i] == _orderId) return i;
        }
        revert("Order not found");
    }
}
```

---

## 3. OPTIONS PROTOCOLS

### 3.1 European Options (Opyn Style)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/**
 * @title OptionsFactory
 * @notice Factory for European-style options
 */
contract OptionsFactory {
    struct OptionSeries {
        address underlying;     // ETH, BTC token
        address strikeAsset;    // USDC
        address collateralAsset;
        uint256 strikePrice;    // Strike in strikeAsset decimals
        uint256 expiry;         // Unix timestamp
        bool isPut;             // true = put, false = call
    }

    mapping(bytes32 => address) public optionTokens;

    event OptionCreated(
        bytes32 indexed seriesId,
        address optionToken,
        address underlying,
        uint256 strikePrice,
        uint256 expiry,
        bool isPut
    );

    /**
     * @notice Create new option series
     */
    function createOption(
        address _underlying,
        address _strikeAsset,
        address _collateralAsset,
        uint256 _strikePrice,
        uint256 _expiry,
        bool _isPut
    ) external returns (address optionToken) {
        require(_expiry > block.timestamp, "Expired");

        bytes32 seriesId = keccak256(abi.encode(
            _underlying,
            _strikeAsset,
            _strikePrice,
            _expiry,
            _isPut
        ));

        require(optionTokens[seriesId] == address(0), "Exists");

        optionToken = address(new OptionToken(
            OptionSeries({
                underlying: _underlying,
                strikeAsset: _strikeAsset,
                collateralAsset: _collateralAsset,
                strikePrice: _strikePrice,
                expiry: _expiry,
                isPut: _isPut
            })
        ));

        optionTokens[seriesId] = optionToken;

        emit OptionCreated(seriesId, optionToken, _underlying, _strikePrice, _expiry, _isPut);
    }
}

/**
 * @title OptionToken
 * @notice ERC20 token representing an option contract
 */
contract OptionToken is ERC20 {
    OptionsFactory.OptionSeries public series;

    // Collateral deposited by writers
    mapping(address => uint256) public collateralDeposited;

    // Oracle for settlement
    address public oracle;
    uint256 public settlementPrice;
    bool public settled;

    constructor(OptionsFactory.OptionSeries memory _series)
        ERC20(
            _generateName(_series),
            _generateSymbol(_series)
        )
    {
        series = _series;
    }

    /**
     * @notice Write options by depositing collateral
     * @dev Mints option tokens to writer
     */
    function write(uint256 _amount) external {
        require(block.timestamp < series.expiry, "Expired");

        uint256 collateralRequired = _calculateCollateral(_amount);

        // Transfer collateral
        IERC20(series.collateralAsset).transferFrom(
            msg.sender,
            address(this),
            collateralRequired
        );

        collateralDeposited[msg.sender] += collateralRequired;

        // Mint option tokens
        _mint(msg.sender, _amount);
    }

    /**
     * @notice Exercise options at expiry
     * @dev European style - only at expiry
     */
    function exercise(uint256 _amount) external {
        require(block.timestamp >= series.expiry, "Not expired");
        require(settled, "Not settled");
        require(balanceOf(msg.sender) >= _amount, "Insufficient balance");

        uint256 payout = _calculatePayout(_amount);
        require(payout > 0, "OTM");

        _burn(msg.sender, _amount);

        IERC20(series.strikeAsset).transfer(msg.sender, payout);
    }

    /**
     * @notice Settle option with oracle price
     */
    function settle(uint256 _price) external {
        require(block.timestamp >= series.expiry, "Not expired");
        require(!settled, "Already settled");
        // In production: verify oracle signature

        settlementPrice = _price;
        settled = true;
    }

    /**
     * @notice Calculate collateral required
     */
    function _calculateCollateral(uint256 _amount) internal view returns (uint256) {
        if (series.isPut) {
            // Put: collateral = strike price × amount
            return (series.strikePrice * _amount) / 1e18;
        } else {
            // Call: collateral = underlying amount
            return _amount;
        }
    }

    /**
     * @notice Calculate exercise payout
     */
    function _calculatePayout(uint256 _amount) internal view returns (uint256) {
        if (series.isPut) {
            // Put: payout if settlement < strike
            if (settlementPrice >= series.strikePrice) return 0;
            return ((series.strikePrice - settlementPrice) * _amount) / 1e18;
        } else {
            // Call: payout if settlement > strike
            if (settlementPrice <= series.strikePrice) return 0;
            return ((settlementPrice - series.strikePrice) * _amount) / 1e18;
        }
    }

    function _generateName(OptionsFactory.OptionSeries memory _s) internal pure returns (string memory) {
        return string(abi.encodePacked(
            "Option-",
            _s.isPut ? "PUT-" : "CALL-"
        ));
    }

    function _generateSymbol(OptionsFactory.OptionSeries memory _s) internal pure returns (string memory) {
        return _s.isPut ? "oPUT" : "oCALL";
    }
}
```

### 3.2 Black-Scholes Pricing (Off-chain)

```python
"""
Black-Scholes Options Pricing
Used for off-chain premium calculation
"""

import math
from scipy.stats import norm
from typing import Tuple

def black_scholes(
    spot: float,        # Current price
    strike: float,      # Strike price
    time_to_expiry: float,  # Years to expiry
    volatility: float,  # Implied volatility (annualized)
    risk_free_rate: float,  # Risk-free rate (annualized)
    is_call: bool = True
) -> Tuple[float, dict]:
    """
    Calculate option price using Black-Scholes model

    Returns:
        price: Option premium
        greeks: Dictionary of option greeks
    """

    # Handle edge cases
    if time_to_expiry <= 0:
        # At expiry - intrinsic value only
        if is_call:
            return max(spot - strike, 0), {}
        return max(strike - spot, 0), {}

    # Calculate d1 and d2
    d1 = (math.log(spot / strike) + (risk_free_rate + 0.5 * volatility**2) * time_to_expiry) / \
         (volatility * math.sqrt(time_to_expiry))

    d2 = d1 - volatility * math.sqrt(time_to_expiry)

    # Calculate option price
    if is_call:
        price = spot * norm.cdf(d1) - strike * math.exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2)
    else:
        price = strike * math.exp(-risk_free_rate * time_to_expiry) * norm.cdf(-d2) - spot * norm.cdf(-d1)

    # Calculate Greeks
    greeks = {
        'delta': norm.cdf(d1) if is_call else norm.cdf(d1) - 1,
        'gamma': norm.pdf(d1) / (spot * volatility * math.sqrt(time_to_expiry)),
        'theta': _calculate_theta(spot, strike, time_to_expiry, volatility, risk_free_rate, d1, d2, is_call),
        'vega': spot * norm.pdf(d1) * math.sqrt(time_to_expiry) / 100,  # Per 1% IV change
        'rho': _calculate_rho(strike, time_to_expiry, risk_free_rate, d2, is_call)
    }

    return price, greeks

def _calculate_theta(spot, strike, t, vol, r, d1, d2, is_call):
    """Calculate theta (time decay per day)"""
    common = -(spot * norm.pdf(d1) * vol) / (2 * math.sqrt(t))

    if is_call:
        theta = common - r * strike * math.exp(-r * t) * norm.cdf(d2)
    else:
        theta = common + r * strike * math.exp(-r * t) * norm.cdf(-d2)

    return theta / 365  # Daily theta

def _calculate_rho(strike, t, r, d2, is_call):
    """Calculate rho (sensitivity to interest rate)"""
    if is_call:
        return strike * t * math.exp(-r * t) * norm.cdf(d2) / 100
    return -strike * t * math.exp(-r * t) * norm.cdf(-d2) / 100

def implied_volatility(
    option_price: float,
    spot: float,
    strike: float,
    time_to_expiry: float,
    risk_free_rate: float,
    is_call: bool,
    precision: float = 0.00001
) -> float:
    """
    Calculate implied volatility using Newton-Raphson method
    """
    vol = 0.5  # Initial guess

    for _ in range(100):  # Max iterations
        price, greeks = black_scholes(spot, strike, time_to_expiry, vol, risk_free_rate, is_call)

        diff = price - option_price

        if abs(diff) < precision:
            return vol

        # Newton-Raphson: vol_new = vol - f(vol)/f'(vol)
        vega = greeks['vega'] * 100  # Convert back from per 1%

        if vega < 1e-10:  # Avoid division by zero
            break

        vol = vol - diff / vega

        # Bounds
        vol = max(0.01, min(vol, 5.0))

    return vol


# Example usage
if __name__ == "__main__":
    # ETH Call Option
    spot = 2000          # ETH at $2000
    strike = 2200        # Strike $2200
    expiry = 30/365      # 30 days
    vol = 0.80           # 80% IV
    rate = 0.05          # 5% risk-free

    price, greeks = black_scholes(spot, strike, expiry, vol, rate, is_call=True)

    print(f"Call Premium: ${price:.2f}")
    print(f"Delta: {greeks['delta']:.4f}")
    print(f"Gamma: {greeks['gamma']:.6f}")
    print(f"Theta: ${greeks['theta']:.2f}/day")
    print(f"Vega: ${greeks['vega']:.2f}/1% IV")
```

---

## 4. SYNTHETIC ASSETS

### 4.1 Synthetix-Style Synthetics

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/**
 * @title SyntheticAssetSystem
 * @notice Create synthetic assets backed by collateral pool
 */
contract SyntheticAssetSystem {
    // Collateral token (SNX-style)
    IERC20 public collateralToken;

    // Oracle interface
    interface IOracle {
        function getPrice(bytes32 asset) external view returns (uint256);
    }
    IOracle public oracle;

    // Collateralization ratio (400% = 4x)
    uint256 public constant C_RATIO = 400;
    uint256 public constant LIQUIDATION_RATIO = 150;

    // User collateral
    mapping(address => uint256) public collateralBalance;

    // Synthetic assets
    mapping(bytes32 => address) public synths;

    // User debt
    mapping(address => uint256) public debtShares;
    uint256 public totalDebtShares;

    // Global debt pool (in USD)
    uint256 public totalSystemDebt;

    event SynthMinted(address indexed user, bytes32 indexed synth, uint256 amount);
    event SynthBurned(address indexed user, bytes32 indexed synth, uint256 amount);

    /**
     * @notice Deposit collateral
     */
    function depositCollateral(uint256 _amount) external {
        collateralToken.transferFrom(msg.sender, address(this), _amount);
        collateralBalance[msg.sender] += _amount;
    }

    /**
     * @notice Mint synthetic asset
     */
    function mintSynth(bytes32 _synthKey, uint256 _amount) external {
        // Check collateralization ratio
        uint256 newDebt = _amount; // Assuming 1:1 with USD
        require(
            _checkCRatio(msg.sender, newDebt),
            "Below c-ratio"
        );

        // Calculate debt shares
        uint256 shares;
        if (totalDebtShares == 0) {
            shares = newDebt;
        } else {
            shares = (newDebt * totalDebtShares) / totalSystemDebt;
        }

        debtShares[msg.sender] += shares;
        totalDebtShares += shares;
        totalSystemDebt += newDebt;

        // Mint synth
        SynthToken(synths[_synthKey]).mint(msg.sender, _amount);

        emit SynthMinted(msg.sender, _synthKey, _amount);
    }

    /**
     * @notice Burn synthetic asset to reduce debt
     */
    function burnSynth(bytes32 _synthKey, uint256 _amount) external {
        SynthToken synth = SynthToken(synths[_synthKey]);

        // Get synth value in USD
        uint256 synthPrice = oracle.getPrice(_synthKey);
        uint256 debtToBurn = (_amount * synthPrice) / 1e18;

        // Calculate shares to remove
        uint256 sharesToBurn = (debtToBurn * totalDebtShares) / totalSystemDebt;
        sharesToBurn = sharesToBurn > debtShares[msg.sender] ?
                       debtShares[msg.sender] : sharesToBurn;

        debtShares[msg.sender] -= sharesToBurn;
        totalDebtShares -= sharesToBurn;
        totalSystemDebt -= debtToBurn;

        // Burn synth
        synth.burn(msg.sender, _amount);

        emit SynthBurned(msg.sender, _synthKey, _amount);
    }

    /**
     * @notice Exchange one synth for another
     * @dev No slippage - pure oracle price exchange
     */
    function exchange(
        bytes32 _sourceSynth,
        uint256 _sourceAmount,
        bytes32 _destSynth
    ) external returns (uint256 destAmount) {
        uint256 sourcePrice = oracle.getPrice(_sourceSynth);
        uint256 destPrice = oracle.getPrice(_destSynth);

        // Calculate destination amount
        uint256 sourceValue = (_sourceAmount * sourcePrice) / 1e18;
        destAmount = (sourceValue * 1e18) / destPrice;

        // Apply exchange fee (0.3%)
        uint256 fee = (destAmount * 30) / 10000;
        destAmount -= fee;

        // Burn source, mint destination
        SynthToken(synths[_sourceSynth]).burn(msg.sender, _sourceAmount);
        SynthToken(synths[_destSynth]).mint(msg.sender, destAmount);

        // Fee goes to fee pool (stakers)
    }

    /**
     * @notice Check if user meets c-ratio
     */
    function _checkCRatio(address _user, uint256 _additionalDebt) internal view returns (bool) {
        uint256 collateralPrice = oracle.getPrice("COLLATERAL");
        uint256 collateralValue = (collateralBalance[_user] * collateralPrice) / 1e18;

        uint256 currentDebt = _getUserDebt(_user);
        uint256 totalDebt = currentDebt + _additionalDebt;

        if (totalDebt == 0) return true;

        uint256 ratio = (collateralValue * 100) / totalDebt;
        return ratio >= C_RATIO;
    }

    /**
     * @notice Get user's share of global debt
     */
    function _getUserDebt(address _user) internal view returns (uint256) {
        if (totalDebtShares == 0) return 0;
        return (debtShares[_user] * totalSystemDebt) / totalDebtShares;
    }

    /**
     * @notice Create new synthetic asset
     */
    function createSynth(bytes32 _key, string memory _name, string memory _symbol) external {
        require(synths[_key] == address(0), "Exists");
        synths[_key] = address(new SynthToken(_name, _symbol, address(this)));
    }
}

/**
 * @title SynthToken
 * @notice ERC20 synthetic asset token
 */
contract SynthToken is ERC20 {
    address public system;

    modifier onlySystem() {
        require(msg.sender == system, "Only system");
        _;
    }

    constructor(string memory _name, string memory _symbol, address _system)
        ERC20(_name, _symbol)
    {
        system = _system;
    }

    function mint(address _to, uint256 _amount) external onlySystem {
        _mint(_to, _amount);
    }

    function burn(address _from, uint256 _amount) external onlySystem {
        _burn(_from, _amount);
    }
}
```

---

## 5. STRUCTURED PRODUCTS

### 5.1 Covered Calls Vault (Ribbon-Style)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/**
 * @title CoveredCallVault
 * @notice Automated covered call strategy vault
 */
contract CoveredCallVault is ERC20 {
    using SafeERC20 for IERC20;

    // Underlying asset (e.g., WETH)
    IERC20 public immutable asset;

    // Options protocol interface
    interface IOptionsProtocol {
        function writeCall(
            address underlying,
            uint256 strikePrice,
            uint256 expiry,
            uint256 amount
        ) external returns (uint256 premium);

        function settleOption(uint256 optionId) external returns (uint256 payout);
    }
    IOptionsProtocol public optionsProtocol;

    // Vault state
    enum VaultState { IDLE, ACTIVE, SETTLING }
    VaultState public state;

    // Current round
    uint256 public currentRound;

    struct RoundData {
        uint256 strikePrice;
        uint256 expiry;
        uint256 premiumCollected;
        uint256 lockedAmount;
        bool settled;
    }
    mapping(uint256 => RoundData) public rounds;

    // Pending deposits (processed next round)
    mapping(address => uint256) public pendingDeposits;
    uint256 public totalPendingDeposits;

    // Management fee (2% annually)
    uint256 public constant MANAGEMENT_FEE = 200;
    // Performance fee (10% of premium)
    uint256 public constant PERFORMANCE_FEE = 1000;

    address public keeper;
    address public feeRecipient;

    event RoundStarted(uint256 indexed round, uint256 strikePrice, uint256 expiry);
    event RoundSettled(uint256 indexed round, uint256 profit);
    event Deposit(address indexed user, uint256 amount);
    event Withdraw(address indexed user, uint256 shares, uint256 amount);

    constructor(
        address _asset,
        address _optionsProtocol,
        string memory _name,
        string memory _symbol
    ) ERC20(_name, _symbol) {
        asset = IERC20(_asset);
        optionsProtocol = IOptionsProtocol(_optionsProtocol);
        keeper = msg.sender;
        feeRecipient = msg.sender;
    }

    /**
     * @notice Deposit assets (processed next round)
     */
    function deposit(uint256 _amount) external {
        asset.safeTransferFrom(msg.sender, address(this), _amount);
        pendingDeposits[msg.sender] += _amount;
        totalPendingDeposits += _amount;

        emit Deposit(msg.sender, _amount);
    }

    /**
     * @notice Claim shares from pending deposits
     */
    function claimShares() external {
        require(pendingDeposits[msg.sender] > 0, "No pending");
        require(state == VaultState.IDLE, "Not idle");

        uint256 depositAmount = pendingDeposits[msg.sender];
        pendingDeposits[msg.sender] = 0;

        // Calculate shares based on current share price
        uint256 shares = _calculateShares(depositAmount);
        _mint(msg.sender, shares);
    }

    /**
     * @notice Request withdrawal (instant if idle, else queued)
     */
    function withdraw(uint256 _shares) external {
        require(balanceOf(msg.sender) >= _shares, "Insufficient shares");
        require(state == VaultState.IDLE, "Cannot withdraw during active round");

        uint256 assetAmount = _calculateAssets(_shares);
        _burn(msg.sender, _shares);

        asset.safeTransfer(msg.sender, assetAmount);

        emit Withdraw(msg.sender, _shares, assetAmount);
    }

    /**
     * @notice Start new round - write covered calls
     * @dev Called by keeper
     */
    function startRound(
        uint256 _strikePrice,
        uint256 _expiry
    ) external onlyKeeper {
        require(state == VaultState.IDLE, "Not idle");

        currentRound++;

        // Process pending deposits
        totalPendingDeposits = 0;

        // Calculate amount to lock
        uint256 vaultBalance = asset.balanceOf(address(this));

        // Approve options protocol
        asset.approve(address(optionsProtocol), vaultBalance);

        // Write covered calls
        uint256 premium = optionsProtocol.writeCall(
            address(asset),
            _strikePrice,
            _expiry,
            vaultBalance
        );

        // Store round data
        rounds[currentRound] = RoundData({
            strikePrice: _strikePrice,
            expiry: _expiry,
            premiumCollected: premium,
            lockedAmount: vaultBalance,
            settled: false
        });

        state = VaultState.ACTIVE;

        emit RoundStarted(currentRound, _strikePrice, _expiry);
    }

    /**
     * @notice Settle current round
     */
    function settleRound() external onlyKeeper {
        require(state == VaultState.ACTIVE, "Not active");

        RoundData storage round = rounds[currentRound];
        require(block.timestamp >= round.expiry, "Not expired");

        state = VaultState.SETTLING;

        // Settle options (get back collateral or exercise payout)
        uint256 payout = optionsProtocol.settleOption(currentRound);

        // Calculate fees
        uint256 performanceFee = (round.premiumCollected * PERFORMANCE_FEE) / 10000;
        uint256 managementFee = (round.lockedAmount * MANAGEMENT_FEE * 7) / (10000 * 365); // Weekly

        uint256 totalFees = performanceFee + managementFee;
        if (totalFees > 0) {
            asset.safeTransfer(feeRecipient, totalFees);
        }

        round.settled = true;
        state = VaultState.IDLE;

        emit RoundSettled(currentRound, payout);
    }

    /**
     * @notice Calculate shares for deposit amount
     */
    function _calculateShares(uint256 _amount) internal view returns (uint256) {
        uint256 totalAssets = _totalAssets();
        uint256 supply = totalSupply();

        if (supply == 0 || totalAssets == 0) {
            return _amount;
        }

        return (_amount * supply) / totalAssets;
    }

    /**
     * @notice Calculate assets for share amount
     */
    function _calculateAssets(uint256 _shares) internal view returns (uint256) {
        uint256 supply = totalSupply();
        if (supply == 0) return 0;

        return (_shares * _totalAssets()) / supply;
    }

    /**
     * @notice Get total assets under management
     */
    function _totalAssets() internal view returns (uint256) {
        return asset.balanceOf(address(this)) - totalPendingDeposits;
    }

    modifier onlyKeeper() {
        require(msg.sender == keeper, "Only keeper");
        _;
    }
}
```

---

## 6. RISK MANAGEMENT

### 6.1 Derivatives Risk Framework

```yaml
DERIVATIVES RISK MATRIX:
══════════════════════════════════════════════════════════════════════════

PERPETUALS:
  Risks:
    - Funding Rate Risk:
        Description: Sustained negative/positive funding
        Mitigation: Monitor funding, adjust position timing
        Max Impact: -0.75% per 8h (capped)

    - Liquidation Risk:
        Description: Price moves against leveraged position
        Mitigation: Conservative leverage, stop losses
        Key Metric: Maintenance margin ratio

    - Oracle Manipulation:
        Description: Mark price manipulation
        Mitigation: TWAP oracles, multiple sources
        Example: dYdX uses Chainlink + internal TWAP

    - ADL (Auto-Deleveraging):
        Description: Forced position reduction
        Trigger: Insurance fund depletion
        Mitigation: Reduce position size in high volatility

OPTIONS:
  Risks:
    - Theta Decay:
        Description: Time value erosion
        Impact: Exponential near expiry
        Mitigation: Roll positions, sell premium

    - Volatility Risk:
        Description: IV changes affect premium
        Greeks: Vega exposure
        Mitigation: Hedge with underlying, spreads

    - Pin Risk:
        Description: At-expiry near strike
        Impact: Exercise uncertainty
        Mitigation: Close before expiry

    - Liquidity Risk:
        Description: Wide spreads, low volume
        Impact: Slippage, inability to exit
        Mitigation: Stick to liquid strikes/expiries

SYNTHETICS:
  Risks:
    - Global Debt Pool Risk:
        Description: All stakers share debt
        Impact: Others' trades affect your debt
        Example: ETH pumps → sETH holders gain → your debt increases

    - Oracle Dependency:
        Description: Complete reliance on price feeds
        Impact: Manipulation = arbitrage
        Mitigation: Aggregated oracles, circuit breakers

    - Collateral Ratio Risk:
        Description: C-ratio below minimum
        Impact: Forced liquidation
        Mitigation: Monitor, auto-rebalance

STRUCTURED PRODUCTS:
  Risks:
    - Strike Selection:
        Description: Wrong strike = loss
        Impact: Caps upside (calls) or doesn't protect (puts)
        Mitigation: Historical analysis, IV surface

    - Opportunity Cost:
        Description: Premiums < missed gains
        Impact: Underperformance vs holding
        Example: 2021 bull run punished covered call vaults

    - Smart Contract Risk:
        Description: Vault vulnerabilities
        Impact: Total loss possible
        Mitigation: Audits, insurance, diversification
```

### 6.2 Position Sizing & Leverage

```python
"""
Derivatives Position Sizing Calculator
"""

class DerivativesRiskManager:
    def __init__(self, account_balance: float, max_risk_per_trade: float = 0.02):
        """
        Args:
            account_balance: Total account value in USD
            max_risk_per_trade: Maximum risk per trade (default 2%)
        """
        self.balance = account_balance
        self.max_risk = max_risk_per_trade

    def perpetual_position_size(
        self,
        entry_price: float,
        stop_loss_price: float,
        leverage: int = 1
    ) -> dict:
        """
        Calculate safe position size for perpetual futures
        """
        # Risk amount in USD
        risk_amount = self.balance * self.max_risk

        # Distance to stop loss (%)
        if entry_price > stop_loss_price:  # Long
            stop_distance = (entry_price - stop_loss_price) / entry_price
        else:  # Short
            stop_distance = (stop_loss_price - entry_price) / entry_price

        # Position size (notional)
        position_notional = risk_amount / stop_distance

        # Required margin
        margin_required = position_notional / leverage

        # Check if margin fits in balance
        if margin_required > self.balance:
            # Scale down
            scale = self.balance / margin_required * 0.9  # 90% max
            position_notional *= scale
            margin_required = position_notional / leverage

        # Size in base asset
        position_size = position_notional / entry_price

        # Liquidation price
        if entry_price > stop_loss_price:  # Long
            liq_price = entry_price * (1 - 1/leverage * 0.9)  # ~90% of margin
        else:
            liq_price = entry_price * (1 + 1/leverage * 0.9)

        return {
            'position_size': position_size,
            'position_notional': position_notional,
            'margin_required': margin_required,
            'leverage': leverage,
            'effective_leverage': position_notional / margin_required,
            'risk_amount': risk_amount,
            'liquidation_price': liq_price,
            'distance_to_liq': abs(entry_price - liq_price) / entry_price * 100
        }

    def options_position_size(
        self,
        premium: float,
        max_contracts: int = 100
    ) -> dict:
        """
        Calculate position size for options (long)
        """
        risk_amount = self.balance * self.max_risk

        # Max contracts we can buy with risk budget
        contracts = int(risk_amount / premium)
        contracts = min(contracts, max_contracts)

        total_cost = contracts * premium

        return {
            'contracts': contracts,
            'total_premium': total_cost,
            'max_loss': total_cost,
            'percent_of_balance': total_cost / self.balance * 100
        }

    def calculate_margin_call_price(
        self,
        entry_price: float,
        position_size: float,
        margin: float,
        is_long: bool,
        maintenance_margin_ratio: float = 0.0625
    ) -> float:
        """
        Calculate price at which margin call occurs
        """
        notional = position_size * entry_price
        maintenance_margin = notional * maintenance_margin_ratio

        if is_long:
            # Price where equity = maintenance margin
            # margin + (price - entry)*size = maintenance
            # price = entry - (margin - maintenance) / size
            return entry_price - (margin - maintenance_margin) / position_size
        else:
            return entry_price + (margin - maintenance_margin) / position_size


# Example usage
if __name__ == "__main__":
    rm = DerivativesRiskManager(account_balance=10000, max_risk_per_trade=0.02)

    # Perpetual position sizing
    perp = rm.perpetual_position_size(
        entry_price=2000,      # Enter ETH long at $2000
        stop_loss_price=1900,  # Stop loss at $1900 (5% down)
        leverage=5
    )

    print("=== Perpetual Position ===")
    print(f"Size: {perp['position_size']:.4f} ETH")
    print(f"Notional: ${perp['position_notional']:.2f}")
    print(f"Margin Required: ${perp['margin_required']:.2f}")
    print(f"Liquidation Price: ${perp['liquidation_price']:.2f}")
    print(f"Distance to Liq: {perp['distance_to_liq']:.1f}%")
```

---

## 7. PRINCIPALES PROTOCOLOS

```
DERIVATIVES PROTOCOL COMPARISON
══════════════════════════════════════════════════════════════════════════

PERPETUALS:
┌────────────────┬────────────────┬────────────────┬────────────────┐
│ Protocol       │ dYdX v4        │ GMX            │ Hyperliquid    │
├────────────────┼────────────────┼────────────────┼────────────────┤
│ Chain          │ Cosmos (own)   │ Arbitrum       │ Own L1         │
│ Model          │ Order Book     │ Oracle/GLP     │ Order Book     │
│ Max Leverage   │ 20x            │ 50x            │ 50x            │
│ Fees           │ Maker: -0.02%  │ 0.1%           │ 0.02% maker    │
│                │ Taker: 0.05%   │                │ 0.05% taker    │
│ Funding        │ 8h             │ 1h             │ 8h             │
│ Insurance Fund │ Yes            │ GLP Pool       │ Yes            │
│ Decentralized  │ High           │ Medium         │ Medium         │
└────────────────┴────────────────┴────────────────┴────────────────┘

OPTIONS:
┌────────────────┬────────────────┬────────────────┬────────────────┐
│ Protocol       │ Opyn/Squeeth   │ Lyra           │ Dopex          │
├────────────────┼────────────────┼────────────────┼────────────────┤
│ Chain          │ Ethereum       │ Optimism       │ Arbitrum       │
│ Style          │ European       │ European       │ American       │
│ Settlement     │ Cash           │ Cash           │ Physical       │
│ Pricing        │ Black-Scholes  │ SABR           │ SSOV           │
│ Innovation     │ Squeeth (ETH²) │ AMM-based      │ Single Staking │
│ Use Case       │ Leverage/Hedge │ Directional    │ Yield + Hedge  │
└────────────────┴────────────────┴────────────────┴────────────────┘

SYNTHETICS:
┌────────────────┬────────────────┬────────────────┬────────────────┐
│ Protocol       │ Synthetix      │ Mirror (dead)  │ UXD            │
├────────────────┼────────────────┼────────────────┼────────────────┤
│ Chain          │ Ethereum/OP    │ Terra (dead)   │ Solana         │
│ Collateral     │ SNX Token      │ UST/LUNA       │ Multi-asset    │
│ C-Ratio        │ 400%           │ 150%           │ 100%           │
│ Assets         │ Forex, Crypto  │ Stocks         │ USD stablecoin │
│ Status         │ Active         │ Defunct        │ Active         │
└────────────────┴────────────────┴────────────────┴────────────────┘

STRUCTURED:
┌────────────────┬────────────────┬────────────────┬────────────────┐
│ Protocol       │ Ribbon/Aevo    │ Thetanuts      │ Jones DAO      │
├────────────────┼────────────────┼────────────────┼────────────────┤
│ Strategy       │ Covered Calls  │ Multi-strategy │ Advanced       │
│ Assets         │ ETH, BTC, AVAX │ Various        │ ETH, DPX       │
│ APY Range      │ 5-30%          │ 10-40%         │ Variable       │
│ Innovation     │ DOVs           │ Auto compound  │ Composability  │
└────────────────┴────────────────┴────────────────┴────────────────┘
```

---

## 8. ADVANCED STRATEGIES

### 8.1 Delta-Neutral Funding Farming

```python
"""
Delta-Neutral Funding Rate Strategy
Long spot + Short perp = Collect funding
"""

class FundingFarmStrategy:
    def __init__(self, capital: float):
        self.capital = capital
        self.position_size = 0
        self.entry_price = 0
        self.total_funding = 0

    def open_position(self, price: float, spot_fee: float = 0.001, perp_fee: float = 0.0005):
        """
        Open delta-neutral position:
        - Buy spot
        - Short perpetual
        """
        # Split capital (account for fees)
        spot_capital = self.capital * 0.5 * (1 - spot_fee)
        perp_margin = self.capital * 0.5

        # Position size based on spot purchase
        self.position_size = spot_capital / price
        self.entry_price = price

        # Calculate effective entry cost
        spot_cost = self.position_size * price * (1 + spot_fee)

        return {
            'position_size': self.position_size,
            'spot_cost': spot_cost,
            'perp_margin': perp_margin,
            'total_fees': spot_cost * spot_fee + self.position_size * price * perp_fee
        }

    def calculate_pnl(self, current_price: float, funding_collected: float) -> dict:
        """
        Calculate strategy PnL
        """
        # Spot PnL
        spot_value = self.position_size * current_price
        spot_pnl = spot_value - (self.position_size * self.entry_price)

        # Perp PnL (short)
        perp_pnl = (self.entry_price - current_price) * self.position_size

        # Net delta PnL (should be ~0)
        delta_pnl = spot_pnl + perp_pnl

        # Total PnL
        total_pnl = delta_pnl + funding_collected

        return {
            'spot_pnl': spot_pnl,
            'perp_pnl': perp_pnl,
            'delta_pnl': delta_pnl,  # Should be near 0
            'funding_collected': funding_collected,
            'total_pnl': total_pnl,
            'apy': (total_pnl / self.capital) * 365 * 3  # Assuming 8h funding periods
        }

    def estimate_funding_income(self, avg_funding_rate: float, days: int) -> float:
        """
        Estimate funding income over period
        Args:
            avg_funding_rate: Average 8h funding rate (e.g., 0.01% = 0.0001)
            days: Number of days
        """
        # 3 funding periods per day
        periods = days * 3

        # Position notional
        notional = self.position_size * self.entry_price

        # Total funding (positive = longs pay shorts)
        return notional * avg_funding_rate * periods


# Simulate strategy
if __name__ == "__main__":
    strategy = FundingFarmStrategy(capital=10000)

    # Open position
    position = strategy.open_position(price=2000)
    print(f"Position Size: {position['position_size']:.4f} ETH")

    # After 30 days with 0.01% avg funding (bullish market)
    funding = strategy.estimate_funding_income(
        avg_funding_rate=0.0001,  # 0.01%
        days=30
    )

    # Price moved 10% (to $2200)
    pnl = strategy.calculate_pnl(
        current_price=2200,
        funding_collected=funding
    )

    print(f"\n30-day Results:")
    print(f"Spot PnL: ${pnl['spot_pnl']:.2f}")
    print(f"Perp PnL: ${pnl['perp_pnl']:.2f}")
    print(f"Delta PnL: ${pnl['delta_pnl']:.2f} (should be ~0)")
    print(f"Funding Collected: ${pnl['funding_collected']:.2f}")
    print(f"Total PnL: ${pnl['total_pnl']:.2f}")
    print(f"Annualized APY: {pnl['apy']:.1f}%")
```

---

## FIRMA

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  NEURONA: DERIVATIVES & PERPETUALS                                             ║
║  Dominio: C40003 - DeFi Derivatives                                            ║
║  Versión: 1.0.0                                                                ║
║  Última actualización: 2024-12-29                                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```
