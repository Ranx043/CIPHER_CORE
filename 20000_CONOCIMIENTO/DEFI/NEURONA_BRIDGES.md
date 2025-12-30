# NEURONA: CROSS-CHAIN BRIDGES
## C40007 - Bridge Architecture & Security

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  CIPHER NEURONA: BRIDGES                                                       ║
║  Dominio: Cross-chain, Messaging, Liquidity Networks, Security                 ║
║  Estado: ACTIVA                                                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. BRIDGE FUNDAMENTALS

### 1.1 Why Bridges Exist

```
THE BLOCKCHAIN TRILEMMA LEADS TO MULTI-CHAIN WORLD
═══════════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────────────┐
│                    MULTI-CHAIN REALITY                                  │
│                                                                         │
│  Ethereum (Security + Decentralization)                                │
│     └── Needs bridges to ──→ Solana (Speed + Low fees)                 │
│                              Arbitrum (L2 scaling)                      │
│                              BSC (Low fees)                             │
│                              Cosmos (App-specific chains)               │
│                                                                         │
│  Problem: Each chain is isolated - can't natively communicate          │
│  Solution: Bridges create interoperability                              │
│                                                                         │
├────────────────────────────────────────────────────────────────────────┤
│                    BRIDGE USE CASES                                     │
│                                                                         │
│  1. Asset Transfer:                                                     │
│     └── Move ETH from Ethereum to Arbitrum                             │
│                                                                         │
│  2. Cross-chain Messaging:                                              │
│     └── Execute function on Chain B from Chain A                       │
│                                                                         │
│  3. Cross-chain Swaps:                                                  │
│     └── Trade ETH on Ethereum for SOL on Solana                        │
│                                                                         │
│  4. Cross-chain Governance:                                             │
│     └── Vote on Chain A, execute on Chain B                            │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Bridge Types

```
BRIDGE TAXONOMY
═══════════════════════════════════════════════════════════════════════

1. LOCK-AND-MINT (Wrapped Assets):
┌────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Chain A               Bridge                    Chain B               │
│  ┌──────┐            ┌────────┐               ┌──────────┐            │
│  │ ETH  │──lock──→   │ Smart  │ ──mint──→     │ wETH     │            │
│  │      │            │Contract│               │(wrapped) │            │
│  │      │←─unlock─   │        │ ←─burn──      │          │            │
│  └──────┘            └────────┘               └──────────┘            │
│                                                                         │
│  Examples: WBTC, wstETH on L2s, Portal                                 │
│  Risk: Custody of locked assets, smart contract bugs                   │
└────────────────────────────────────────────────────────────────────────┘

2. LIQUIDITY NETWORKS (Native Assets):
┌────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Chain A               Liquidity Pool           Chain B               │
│  ┌──────┐            ┌────────────┐           ┌──────┐                │
│  │ ETH  │──deposit──→│ Router +   │──release──→│ ETH  │               │
│  │      │            │ LP Network │           │      │                │
│  └──────┘            └────────────┘           └──────┘                │
│                                                                         │
│  Examples: Stargate, Across, Hop                                       │
│  Risk: LP impermanent loss, liquidity fragmentation                   │
└────────────────────────────────────────────────────────────────────────┘

3. MESSAGING PROTOCOLS:
┌────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Chain A              Messaging Layer          Chain B               │
│  ┌──────┐            ┌────────────┐           ┌──────┐                │
│  │ Dapp │──message──→│ Validators/│──execute──→│ Dapp │               │
│  │      │            │ Relayers   │           │      │                │
│  └──────┘            └────────────┘           └──────┘                │
│                                                                         │
│  Examples: LayerZero, Axelar, Wormhole, Chainlink CCIP                │
│  Risk: Validator collusion, relayer failure                            │
└────────────────────────────────────────────────────────────────────────┘

4. NATIVE BRIDGES (L2):
┌────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  L1 (Ethereum)        Canonical Bridge        L2 (Arbitrum)           │
│  ┌──────┐            ┌────────────┐           ┌──────┐                │
│  │ ETH  │──deposit──→│ Rollup     │──credit──→│ ETH  │               │
│  │      │            │ Contract   │           │      │                │
│  └──────┘            └────────────┘           └──────┘                │
│                                                                         │
│  Examples: Arbitrum Bridge, OP Bridge, zkSync Bridge                   │
│  Risk: Longer withdrawal times (7 days for optimistic)                │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. LOCK-AND-MINT BRIDGE

### 2.1 Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

/**
 * @title LockAndMintBridge
 * @notice Source chain contract for lock-and-mint bridge
 */
contract SourceChainBridge is ReentrancyGuard, Pausable {
    // Supported tokens
    mapping(address => bool) public supportedTokens;

    // Locked balances per token
    mapping(address => uint256) public lockedBalance;

    // Nonce for unique transfer IDs
    uint256 public nonce;

    // Relayer/validator set
    mapping(address => bool) public validators;
    uint256 public validatorThreshold = 2; // 2-of-n multisig

    // Processed releases (prevent replay)
    mapping(bytes32 => bool) public processedReleases;

    // Events for relayers to monitor
    event TokensLocked(
        bytes32 indexed transferId,
        address indexed sender,
        address indexed token,
        uint256 amount,
        uint256 destChainId,
        address recipient
    );

    event TokensReleased(
        bytes32 indexed transferId,
        address indexed recipient,
        address indexed token,
        uint256 amount
    );

    /**
     * @notice Lock tokens to bridge to another chain
     * @param _token Token address (address(0) for native ETH)
     * @param _amount Amount to bridge
     * @param _destChainId Destination chain ID
     * @param _recipient Recipient address on destination chain
     */
    function lock(
        address _token,
        uint256 _amount,
        uint256 _destChainId,
        address _recipient
    ) external payable nonReentrant whenNotPaused returns (bytes32 transferId) {
        require(_amount > 0, "Amount must be > 0");
        require(_recipient != address(0), "Invalid recipient");

        if (_token == address(0)) {
            // Native ETH
            require(msg.value == _amount, "Incorrect ETH amount");
        } else {
            require(supportedTokens[_token], "Token not supported");
            IERC20(_token).transferFrom(msg.sender, address(this), _amount);
        }

        // Generate unique transfer ID
        transferId = keccak256(abi.encodePacked(
            block.chainid,
            address(this),
            nonce++,
            msg.sender,
            _token,
            _amount,
            _destChainId,
            _recipient,
            block.timestamp
        ));

        lockedBalance[_token] += _amount;

        emit TokensLocked(
            transferId,
            msg.sender,
            _token,
            _amount,
            _destChainId,
            _recipient
        );
    }

    /**
     * @notice Release locked tokens (called when burn proof received)
     * @param _transferId Original transfer ID from destination chain
     * @param _token Token to release
     * @param _amount Amount to release
     * @param _recipient Recipient address
     * @param _signatures Validator signatures
     */
    function release(
        bytes32 _transferId,
        address _token,
        uint256 _amount,
        address _recipient,
        bytes[] calldata _signatures
    ) external nonReentrant whenNotPaused {
        require(!processedReleases[_transferId], "Already processed");
        require(_amount <= lockedBalance[_token], "Insufficient locked balance");

        // Verify validator signatures
        bytes32 messageHash = keccak256(abi.encodePacked(
            _transferId,
            _token,
            _amount,
            _recipient,
            block.chainid
        ));

        require(
            _verifySignatures(messageHash, _signatures),
            "Invalid signatures"
        );

        processedReleases[_transferId] = true;
        lockedBalance[_token] -= _amount;

        // Transfer tokens
        if (_token == address(0)) {
            (bool success, ) = _recipient.call{value: _amount}("");
            require(success, "ETH transfer failed");
        } else {
            IERC20(_token).transfer(_recipient, _amount);
        }

        emit TokensReleased(_transferId, _recipient, _token, _amount);
    }

    /**
     * @notice Verify threshold signatures from validators
     */
    function _verifySignatures(
        bytes32 _messageHash,
        bytes[] calldata _signatures
    ) internal view returns (bool) {
        require(_signatures.length >= validatorThreshold, "Not enough signatures");

        bytes32 ethSignedHash = keccak256(abi.encodePacked(
            "\x19Ethereum Signed Message:\n32",
            _messageHash
        ));

        address[] memory signers = new address[](_signatures.length);

        for (uint256 i = 0; i < _signatures.length; i++) {
            address signer = _recoverSigner(ethSignedHash, _signatures[i]);
            require(validators[signer], "Invalid validator");

            // Check for duplicate signers
            for (uint256 j = 0; j < i; j++) {
                require(signers[j] != signer, "Duplicate signer");
            }
            signers[i] = signer;
        }

        return true;
    }

    function _recoverSigner(bytes32 _hash, bytes memory _sig) internal pure returns (address) {
        require(_sig.length == 65, "Invalid signature length");

        bytes32 r;
        bytes32 s;
        uint8 v;

        assembly {
            r := mload(add(_sig, 32))
            s := mload(add(_sig, 64))
            v := byte(0, mload(add(_sig, 96)))
        }

        return ecrecover(_hash, v, r, s);
    }

    // Admin functions
    function addSupportedToken(address _token) external {
        supportedTokens[_token] = true;
    }

    function addValidator(address _validator) external {
        validators[_validator] = true;
    }

    receive() external payable {}
}

/**
 * @title WrappedToken
 * @notice Wrapped token on destination chain
 */
contract WrappedToken is ERC20 {
    address public bridge;

    modifier onlyBridge() {
        require(msg.sender == bridge, "Only bridge");
        _;
    }

    constructor(
        string memory _name,
        string memory _symbol,
        address _bridge
    ) ERC20(_name, _symbol) {
        bridge = _bridge;
    }

    function mint(address _to, uint256 _amount) external onlyBridge {
        _mint(_to, _amount);
    }

    function burn(address _from, uint256 _amount) external onlyBridge {
        _burn(_from, _amount);
    }
}

/**
 * @title DestinationChainBridge
 * @notice Destination chain contract - mints wrapped tokens
 */
contract DestinationChainBridge is ReentrancyGuard, Pausable {
    // Wrapped token mapping: source chain ID => source token => wrapped token
    mapping(uint256 => mapping(address => address)) public wrappedTokens;

    // Processed mints (prevent replay)
    mapping(bytes32 => bool) public processedMints;

    // Validators
    mapping(address => bool) public validators;
    uint256 public validatorThreshold = 2;

    // Nonce for burns
    uint256 public burnNonce;

    event TokensMinted(
        bytes32 indexed transferId,
        address indexed recipient,
        address indexed wrappedToken,
        uint256 amount
    );

    event TokensBurned(
        bytes32 indexed burnId,
        address indexed sender,
        address indexed wrappedToken,
        uint256 amount,
        uint256 destChainId,
        address recipient
    );

    /**
     * @notice Mint wrapped tokens (called by relayers with lock proof)
     */
    function mint(
        bytes32 _transferId,
        uint256 _sourceChainId,
        address _sourceToken,
        uint256 _amount,
        address _recipient,
        bytes[] calldata _signatures
    ) external nonReentrant whenNotPaused {
        require(!processedMints[_transferId], "Already processed");

        // Verify signatures
        bytes32 messageHash = keccak256(abi.encodePacked(
            _transferId,
            _sourceChainId,
            _sourceToken,
            _amount,
            _recipient,
            block.chainid
        ));

        require(
            _verifySignatures(messageHash, _signatures),
            "Invalid signatures"
        );

        processedMints[_transferId] = true;

        // Get or create wrapped token
        address wrappedToken = wrappedTokens[_sourceChainId][_sourceToken];
        require(wrappedToken != address(0), "Wrapped token not registered");

        // Mint wrapped tokens
        WrappedToken(wrappedToken).mint(_recipient, _amount);

        emit TokensMinted(_transferId, _recipient, wrappedToken, _amount);
    }

    /**
     * @notice Burn wrapped tokens to bridge back
     */
    function burn(
        address _wrappedToken,
        uint256 _amount,
        uint256 _destChainId,
        address _recipient
    ) external nonReentrant whenNotPaused returns (bytes32 burnId) {
        require(_amount > 0, "Amount must be > 0");

        // Burn wrapped tokens
        WrappedToken(_wrappedToken).burn(msg.sender, _amount);

        burnId = keccak256(abi.encodePacked(
            block.chainid,
            address(this),
            burnNonce++,
            msg.sender,
            _wrappedToken,
            _amount,
            _destChainId,
            _recipient,
            block.timestamp
        ));

        emit TokensBurned(
            burnId,
            msg.sender,
            _wrappedToken,
            _amount,
            _destChainId,
            _recipient
        );
    }

    // Same signature verification as source chain
    function _verifySignatures(
        bytes32 _messageHash,
        bytes[] calldata _signatures
    ) internal view returns (bool) {
        // ... same implementation as SourceChainBridge
        return true;
    }

    // Admin: register wrapped token
    function registerWrappedToken(
        uint256 _sourceChainId,
        address _sourceToken,
        address _wrappedToken
    ) external {
        wrappedTokens[_sourceChainId][_sourceToken] = _wrappedToken;
    }
}
```

---

## 3. LIQUIDITY NETWORK BRIDGE

### 3.1 Stargate/Across Style

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/**
 * @title LiquidityPoolBridge
 * @notice Liquidity network bridge (Stargate/Across style)
 */
contract LiquidityPoolBridge {
    using SafeERC20 for IERC20;

    // Pool for each token
    struct Pool {
        IERC20 token;
        uint256 totalLiquidity;
        uint256 totalShares;
        mapping(address => uint256) lpShares;
    }

    mapping(address => Pool) public pools;

    // Fee structure
    uint256 public lpFee = 4;        // 0.04% to LPs
    uint256 public protocolFee = 1;  // 0.01% to protocol

    // Cross-chain communication (simplified)
    mapping(uint256 => address) public chainEndpoints; // chainId => endpoint

    // Pending fills
    struct PendingFill {
        address token;
        uint256 amount;
        address recipient;
        uint256 deadline;
        bool filled;
    }
    mapping(bytes32 => PendingFill) public pendingFills;

    // Relayer/Solver network
    mapping(address => bool) public relayers;
    mapping(address => uint256) public relayerBond;
    uint256 public minRelayerBond = 10 ether;

    event LiquidityAdded(address indexed provider, address indexed token, uint256 amount, uint256 shares);
    event LiquidityRemoved(address indexed provider, address indexed token, uint256 amount, uint256 shares);
    event TransferInitiated(bytes32 indexed transferId, address indexed sender, uint256 destChainId, uint256 amount);
    event TransferFilled(bytes32 indexed transferId, address indexed relayer, uint256 amount);

    /**
     * @notice Add liquidity to pool
     */
    function addLiquidity(address _token, uint256 _amount) external returns (uint256 shares) {
        Pool storage pool = pools[_token];

        if (pool.totalLiquidity == 0) {
            shares = _amount;
        } else {
            shares = (_amount * pool.totalShares) / pool.totalLiquidity;
        }

        IERC20(_token).safeTransferFrom(msg.sender, address(this), _amount);

        pool.totalLiquidity += _amount;
        pool.totalShares += shares;
        pool.lpShares[msg.sender] += shares;

        emit LiquidityAdded(msg.sender, _token, _amount, shares);
    }

    /**
     * @notice Remove liquidity from pool
     */
    function removeLiquidity(address _token, uint256 _shares) external returns (uint256 amount) {
        Pool storage pool = pools[_token];
        require(pool.lpShares[msg.sender] >= _shares, "Insufficient shares");

        amount = (_shares * pool.totalLiquidity) / pool.totalShares;

        pool.lpShares[msg.sender] -= _shares;
        pool.totalShares -= _shares;
        pool.totalLiquidity -= amount;

        IERC20(_token).safeTransfer(msg.sender, amount);

        emit LiquidityRemoved(msg.sender, _token, amount, _shares);
    }

    /**
     * @notice Initiate cross-chain transfer
     */
    function bridgeTokens(
        address _token,
        uint256 _amount,
        uint256 _destChainId,
        address _recipient,
        uint256 _maxFee
    ) external returns (bytes32 transferId) {
        require(chainEndpoints[_destChainId] != address(0), "Unsupported chain");

        // Calculate fee
        uint256 totalFee = (_amount * (lpFee + protocolFee)) / 10000;
        require(totalFee <= _maxFee, "Fee too high");

        uint256 amountAfterFee = _amount - totalFee;

        // Transfer tokens from user
        IERC20(_token).safeTransferFrom(msg.sender, address(this), _amount);

        // Add fee to pool (LPs earn)
        uint256 lpFeeAmount = (_amount * lpFee) / 10000;
        pools[_token].totalLiquidity += lpFeeAmount;

        // Generate transfer ID
        transferId = keccak256(abi.encodePacked(
            block.chainid,
            _destChainId,
            msg.sender,
            _recipient,
            _token,
            amountAfterFee,
            block.timestamp,
            block.number
        ));

        // Store pending (for destination chain verification)
        pendingFills[transferId] = PendingFill({
            token: _token,
            amount: amountAfterFee,
            recipient: _recipient,
            deadline: block.timestamp + 1 days,
            filled: false
        });

        emit TransferInitiated(transferId, msg.sender, _destChainId, amountAfterFee);

        // In production: emit message for cross-chain relayers
    }

    /**
     * @notice Fill transfer on destination chain (relayer calls this)
     * @dev Relayer fronts liquidity, then claims from source chain
     */
    function fillTransfer(
        bytes32 _transferId,
        address _token,
        uint256 _amount,
        address _recipient
    ) external {
        require(relayers[msg.sender], "Not a relayer");
        require(!pendingFills[_transferId].filled, "Already filled");

        Pool storage pool = pools[_token];
        require(pool.totalLiquidity >= _amount, "Insufficient liquidity");

        // Mark as filled
        pendingFills[_transferId].filled = true;

        // Use pool liquidity to fill
        pool.totalLiquidity -= _amount;

        // Transfer to recipient
        IERC20(_token).safeTransfer(_recipient, _amount);

        emit TransferFilled(_transferId, msg.sender, _amount);

        // Relayer will be reimbursed when source chain confirms
    }

    /**
     * @notice Relayer claims reimbursement after verification
     */
    function claimReimbursement(
        bytes32 _transferId,
        bytes calldata _proof
    ) external {
        // In production: verify cross-chain proof
        // Reimburse relayer from pool (they already provided liquidity)

        PendingFill storage fill = pendingFills[_transferId];
        require(fill.filled, "Not filled");

        // Add back to pool (relayer gets their liquidity back)
        pools[fill.token].totalLiquidity += fill.amount;
    }

    /**
     * @notice Register as relayer
     */
    function registerRelayer() external payable {
        require(msg.value >= minRelayerBond, "Insufficient bond");
        relayers[msg.sender] = true;
        relayerBond[msg.sender] = msg.value;
    }

    /**
     * @notice Get LP position value
     */
    function getLPValue(address _token, address _lp) external view returns (uint256) {
        Pool storage pool = pools[_token];
        if (pool.totalShares == 0) return 0;
        return (pool.lpShares[_lp] * pool.totalLiquidity) / pool.totalShares;
    }
}
```

---

## 4. MESSAGING PROTOCOLS

### 4.1 LayerZero Integration

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title LayerZeroApp
 * @notice Base contract for LayerZero cross-chain messaging
 */
abstract contract LayerZeroApp {
    // LayerZero endpoint interface
    interface ILayerZeroEndpoint {
        function send(
            uint16 _dstChainId,
            bytes calldata _destination,
            bytes calldata _payload,
            address payable _refundAddress,
            address _zroPaymentAddress,
            bytes calldata _adapterParams
        ) external payable;

        function estimateFees(
            uint16 _dstChainId,
            address _userApplication,
            bytes calldata _payload,
            bool _payInZRO,
            bytes calldata _adapterParams
        ) external view returns (uint256 nativeFee, uint256 zroFee);
    }

    ILayerZeroEndpoint public immutable lzEndpoint;

    // Trusted remote addresses per chain
    mapping(uint16 => bytes) public trustedRemotes;

    // Failed messages for retry
    mapping(uint16 => mapping(bytes => mapping(uint64 => bytes32))) public failedMessages;

    event MessageSent(uint16 indexed dstChainId, bytes payload, uint64 nonce);
    event MessageReceived(uint16 indexed srcChainId, bytes srcAddress, uint64 nonce, bytes payload);
    event MessageFailed(uint16 indexed srcChainId, bytes srcAddress, uint64 nonce, bytes payload, bytes reason);

    constructor(address _lzEndpoint) {
        lzEndpoint = ILayerZeroEndpoint(_lzEndpoint);
    }

    /**
     * @notice Send cross-chain message
     */
    function _lzSend(
        uint16 _dstChainId,
        bytes memory _payload,
        address payable _refundAddress,
        bytes memory _adapterParams
    ) internal virtual {
        bytes memory trustedRemote = trustedRemotes[_dstChainId];
        require(trustedRemote.length > 0, "Destination not trusted");

        lzEndpoint.send{value: msg.value}(
            _dstChainId,
            trustedRemote,
            _payload,
            _refundAddress,
            address(0), // no ZRO payment
            _adapterParams
        );
    }

    /**
     * @notice Receive cross-chain message (called by LZ endpoint)
     */
    function lzReceive(
        uint16 _srcChainId,
        bytes calldata _srcAddress,
        uint64 _nonce,
        bytes calldata _payload
    ) external virtual {
        require(msg.sender == address(lzEndpoint), "Invalid caller");

        bytes memory trustedRemote = trustedRemotes[_srcChainId];
        require(
            _srcAddress.length == trustedRemote.length &&
            keccak256(_srcAddress) == keccak256(trustedRemote),
            "Invalid source"
        );

        // Try to process message
        try this.nonblockingLzReceive(_srcChainId, _srcAddress, _nonce, _payload) {
            emit MessageReceived(_srcChainId, _srcAddress, _nonce, _payload);
        } catch (bytes memory reason) {
            failedMessages[_srcChainId][_srcAddress][_nonce] = keccak256(_payload);
            emit MessageFailed(_srcChainId, _srcAddress, _nonce, _payload, reason);
        }
    }

    /**
     * @notice Process received message (override in child)
     */
    function nonblockingLzReceive(
        uint16 _srcChainId,
        bytes calldata _srcAddress,
        uint64 _nonce,
        bytes calldata _payload
    ) public virtual;

    /**
     * @notice Retry failed message
     */
    function retryMessage(
        uint16 _srcChainId,
        bytes calldata _srcAddress,
        uint64 _nonce,
        bytes calldata _payload
    ) external virtual {
        bytes32 payloadHash = failedMessages[_srcChainId][_srcAddress][_nonce];
        require(payloadHash != bytes32(0), "No stored message");
        require(keccak256(_payload) == payloadHash, "Invalid payload");

        delete failedMessages[_srcChainId][_srcAddress][_nonce];

        this.nonblockingLzReceive(_srcChainId, _srcAddress, _nonce, _payload);
    }

    /**
     * @notice Estimate message fee
     */
    function estimateFee(
        uint16 _dstChainId,
        bytes calldata _payload,
        bytes calldata _adapterParams
    ) external view returns (uint256 nativeFee) {
        (nativeFee, ) = lzEndpoint.estimateFees(
            _dstChainId,
            address(this),
            _payload,
            false,
            _adapterParams
        );
    }

    /**
     * @notice Set trusted remote address
     */
    function setTrustedRemote(uint16 _chainId, bytes calldata _path) external virtual {
        trustedRemotes[_chainId] = _path;
    }
}

/**
 * @title OmnichainToken
 * @notice Example OFT (Omnichain Fungible Token) using LayerZero
 */
contract OmnichainToken is LayerZeroApp, ERC20 {
    uint16 public constant PT_SEND = 0; // Packet type for send

    constructor(
        string memory _name,
        string memory _symbol,
        address _lzEndpoint
    ) LayerZeroApp(_lzEndpoint) ERC20(_name, _symbol) {
        _mint(msg.sender, 1000000e18);
    }

    /**
     * @notice Send tokens to another chain
     */
    function sendTokens(
        uint16 _dstChainId,
        address _to,
        uint256 _amount,
        address payable _refundAddress,
        bytes calldata _adapterParams
    ) external payable {
        require(_amount > 0, "Amount must be > 0");

        // Burn on source chain
        _burn(msg.sender, _amount);

        // Encode payload
        bytes memory payload = abi.encode(PT_SEND, _to, _amount);

        // Send via LayerZero
        _lzSend(_dstChainId, payload, _refundAddress, _adapterParams);

        emit MessageSent(_dstChainId, payload, 0);
    }

    /**
     * @notice Process received message
     */
    function nonblockingLzReceive(
        uint16 _srcChainId,
        bytes calldata _srcAddress,
        uint64 _nonce,
        bytes calldata _payload
    ) public override {
        require(msg.sender == address(this), "Only self");

        (uint16 packetType, address to, uint256 amount) = abi.decode(
            _payload,
            (uint16, address, uint256)
        );

        require(packetType == PT_SEND, "Invalid packet type");

        // Mint on destination chain
        _mint(to, amount);
    }
}
```

---

## 5. BRIDGE SECURITY

### 5.1 Common Attack Vectors

```
BRIDGE SECURITY ANALYSIS
═══════════════════════════════════════════════════════════════════════

ATTACK VECTORS & MITIGATIONS:
┌────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  1. SIGNATURE FORGERY                                                   │
│     Attack: Forge validator signatures to mint tokens                  │
│     Impact: Unlimited token minting                                    │
│     Mitigation:                                                        │
│       - Use proven signature schemes (ECDSA, BLS)                     │
│       - Require threshold signatures (m-of-n)                          │
│       - Rotate keys regularly                                          │
│                                                                         │
│  2. REPLAY ATTACKS                                                      │
│     Attack: Reuse valid transaction on multiple chains                 │
│     Impact: Double-spend                                                │
│     Mitigation:                                                        │
│       - Include chain ID in signed message                             │
│       - Track processed nonces/transfer IDs                            │
│       - Use unique transfer identifiers                                │
│                                                                         │
│  3. ORACLE MANIPULATION                                                 │
│     Attack: Manipulate price feeds for bridge swaps                    │
│     Impact: Drain liquidity at favorable rates                         │
│     Mitigation:                                                        │
│       - Use TWAP oracles                                               │
│       - Multiple oracle sources                                        │
│       - Sanity bounds on prices                                        │
│                                                                         │
│  4. ADMIN KEY COMPROMISE                                                │
│     Attack: Steal admin keys, drain contract                           │
│     Impact: Total loss of locked funds                                 │
│     Mitigation:                                                        │
│       - Hardware security modules (HSM)                                │
│       - Multi-sig with timelock                                        │
│       - Separate hot/cold wallets                                      │
│                                                                         │
│  5. SMART CONTRACT BUGS                                                 │
│     Attack: Exploit vulnerability in bridge contract                   │
│     Impact: Variable (up to total loss)                                │
│     Mitigation:                                                        │
│       - Multiple audits                                                │
│       - Formal verification                                            │
│       - Bug bounty programs                                            │
│       - Gradual TVL increase                                           │
│                                                                         │
│  6. VALIDATOR COLLUSION                                                 │
│     Attack: Validators collude to approve fake transfers               │
│     Impact: Mint unbacked tokens                                       │
│     Mitigation:                                                        │
│       - Economic bonds (slashing)                                      │
│       - Geographic/organizational diversity                            │
│       - Fraud proofs with challenge period                             │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘

HISTORICAL BRIDGE HACKS:
┌──────────────┬────────────┬───────────────────────────────────────────┐
│ Bridge       │ Loss       │ Attack Vector                              │
├──────────────┼────────────┼───────────────────────────────────────────┤
│ Ronin        │ $625M      │ Validator key compromise (5-of-9)         │
│ Wormhole     │ $320M      │ Signature verification bypass             │
│ Nomad        │ $190M      │ Message validation bug (copy-paste exploit)│
│ Harmony      │ $100M      │ Private key compromise (2-of-5)           │
│ BNB Bridge   │ $570M      │ Proof verification bypass                  │
│ Multichain   │ $130M      │ MPC key compromise                         │
└──────────────┴────────────┴───────────────────────────────────────────┘
```

### 5.2 Security Best Practices

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title SecureBridge
 * @notice Bridge with comprehensive security measures
 */
contract SecureBridge {
    // Rate limiting
    mapping(address => uint256) public dailyVolume;
    mapping(address => uint256) public lastResetTime;
    uint256 public dailyLimit = 1000 ether;

    // Pause functionality
    bool public paused;
    address public guardian; // Can pause instantly

    // Timelock for admin actions
    uint256 public constant TIMELOCK_DELAY = 2 days;
    mapping(bytes32 => uint256) public pendingActions;

    // Validator management
    uint256 public constant MIN_VALIDATORS = 5;
    uint256 public constant VALIDATOR_BOND = 100 ether;
    mapping(address => uint256) public validatorBonds;

    // Challenge period for fraud proofs
    uint256 public constant CHALLENGE_PERIOD = 7 days;

    modifier notPaused() {
        require(!paused, "Bridge paused");
        _;
    }

    modifier rateLimited(uint256 _amount) {
        if (block.timestamp > lastResetTime[msg.sender] + 1 days) {
            dailyVolume[msg.sender] = 0;
            lastResetTime[msg.sender] = block.timestamp;
        }

        require(
            dailyVolume[msg.sender] + _amount <= dailyLimit,
            "Daily limit exceeded"
        );

        dailyVolume[msg.sender] += _amount;
        _;
    }

    modifier timelocked(bytes32 _actionId) {
        if (pendingActions[_actionId] == 0) {
            // Queue action
            pendingActions[_actionId] = block.timestamp + TIMELOCK_DELAY;
            revert("Action queued - execute after timelock");
        }

        require(
            block.timestamp >= pendingActions[_actionId],
            "Timelock not expired"
        );

        delete pendingActions[_actionId];
        _;
    }

    /**
     * @notice Emergency pause (guardian only)
     */
    function pause() external {
        require(msg.sender == guardian, "Only guardian");
        paused = true;
    }

    /**
     * @notice Slash misbehaving validator
     */
    function slashValidator(
        address _validator,
        bytes calldata _fraudProof
    ) external {
        require(_verifyFraudProof(_fraudProof), "Invalid fraud proof");

        uint256 slashAmount = validatorBonds[_validator];
        validatorBonds[_validator] = 0;

        // Distribute to reporters or burn
        // ...
    }

    /**
     * @notice Bridge with security checks
     */
    function secureTransfer(
        address _token,
        uint256 _amount,
        uint256 _destChain
    ) external notPaused rateLimited(_amount) {
        // Sanity checks
        require(_amount > 0, "Invalid amount");
        require(_amount <= address(this).balance / 10, "Amount too large");

        // Process transfer...
    }

    function _verifyFraudProof(bytes calldata _proof) internal pure returns (bool) {
        // Verify fraud proof
        return true;
    }
}
```

---

## 6. BRIDGE COMPARISON

```
BRIDGE PROTOCOL COMPARISON
═══════════════════════════════════════════════════════════════════════

┌──────────────┬────────────┬────────────┬───────────┬──────────┬────────┐
│ Protocol     │ Type       │ Security   │ Speed     │ Fee      │ Chains │
├──────────────┼────────────┼────────────┼───────────┼──────────┼────────┤
│ Stargate     │ Liquidity  │ LayerZero  │ Fast      │ Low      │ 15+    │
│ Across       │ Liquidity  │ UMA Oracle │ Very Fast │ Low      │ 10+    │
│ Hop          │ Liquidity  │ Bonders    │ Fast      │ Medium   │ 6+     │
│ Wormhole     │ Message    │ Guardians  │ Medium    │ Low      │ 20+    │
│ LayerZero    │ Message    │ Oracles+DVN│ Fast      │ Variable │ 30+    │
│ Axelar       │ Message    │ dPoS       │ Medium    │ Low      │ 50+    │
│ CCIP         │ Message    │ Chainlink  │ Slow      │ High     │ 10+    │
│ Synapse      │ Liquidity  │ Validators │ Fast      │ Medium   │ 15+    │
│ Multichain*  │ Lock/Mint  │ MPC        │ Medium    │ Low      │ 90+    │
├──────────────┼────────────┼────────────┼───────────┼──────────┼────────┤
│ * Multichain ceased operations after exploit                          │
└──────────────┴────────────┴────────────┴───────────┴──────────┴────────┘

NATIVE L2 BRIDGES:
┌──────────────┬────────────────────┬────────────────────────────────────┐
│ Bridge       │ Withdrawal Time    │ Security Model                      │
├──────────────┼────────────────────┼────────────────────────────────────┤
│ Arbitrum     │ ~7 days           │ Fraud proofs                        │
│ Optimism     │ ~7 days           │ Fraud proofs                        │
│ zkSync       │ ~1 hour           │ ZK proofs                           │
│ Polygon zkEVM│ ~1 hour           │ ZK proofs                           │
│ StarkNet     │ ~12 hours         │ STARK proofs                        │
│ Scroll       │ ~1 hour           │ ZK proofs                           │
└──────────────┴────────────────────┴────────────────────────────────────┘
```

---

## FIRMA

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  NEURONA: CROSS-CHAIN BRIDGES                                                  ║
║  Dominio: C40007 - Bridge Architecture & Security                              ║
║  Versión: 1.0.0                                                                ║
║  Última actualización: 2024-12-29                                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```
