# NEURONA: DESIGN_PATTERNS
## ID: C30009 | Patrones de Diseño para Smart Contracts

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  SMART CONTRACT DESIGN PATTERNS                                                ║
║  "Arquitecturas Probadas para Contratos Seguros y Eficientes"                 ║
║  Neurona: C30009 | Versión: 1.0.0                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. PATRONES DE SEGURIDAD

### 1.1 Checks-Effects-Interactions (CEI)

```solidity
// ============ PATRÓN CEI ============
// Previene reentrancy al ordenar operaciones correctamente

contract CEIPattern {
    mapping(address => uint256) public balances;

    // ❌ VULNERABLE - Interacción antes de efectos
    function withdrawBad(uint256 amount) external {
        require(balances[msg.sender] >= amount);

        // Interaction BEFORE effect = VULNERABLE
        (bool success,) = msg.sender.call{value: amount}("");
        require(success);

        balances[msg.sender] -= amount; // Effect after interaction
    }

    // ✅ SEGURO - CEI Pattern
    function withdrawGood(uint256 amount) external {
        // 1. CHECKS
        require(balances[msg.sender] >= amount, "Insufficient balance");

        // 2. EFFECTS (update state BEFORE external call)
        balances[msg.sender] -= amount;

        // 3. INTERACTIONS (external calls LAST)
        (bool success,) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

### 1.2 Reentrancy Guard

```solidity
// ============ REENTRANCY GUARD ============
abstract contract ReentrancyGuard {
    uint256 private constant _NOT_ENTERED = 1;
    uint256 private constant _ENTERED = 2;

    uint256 private _status;

    constructor() {
        _status = _NOT_ENTERED;
    }

    modifier nonReentrant() {
        require(_status != _ENTERED, "ReentrancyGuard: reentrant call");
        _status = _ENTERED;
        _;
        _status = _NOT_ENTERED;
    }
}

contract VaultWithGuard is ReentrancyGuard {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) external nonReentrant {
        require(balances[msg.sender] >= amount, "Insufficient");

        balances[msg.sender] -= amount;

        (bool success,) = msg.sender.call{value: amount}("");
        require(success);
    }

    // Cross-function reentrancy también protegido
    function transfer(address to, uint256 amount) external nonReentrant {
        require(balances[msg.sender] >= amount, "Insufficient");
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}
```

### 1.3 Pull Over Push

```solidity
// ============ PULL OVER PUSH ============
// Preferir que usuarios retiren fondos vs enviarles directamente

contract PullOverPush {
    mapping(address => uint256) public pendingWithdrawals;

    // ❌ VULNERABLE - Push pattern
    function distributeRewardsBad(address[] calldata recipients, uint256 amount) external {
        for (uint i = 0; i < recipients.length; i++) {
            // Si un recipient revierte, todo falla
            payable(recipients[i]).transfer(amount);
        }
    }

    // ✅ SEGURO - Pull pattern
    function allocateRewards(address[] calldata recipients, uint256 amount) external {
        for (uint i = 0; i < recipients.length; i++) {
            pendingWithdrawals[recipients[i]] += amount;
        }
    }

    function withdrawRewards() external {
        uint256 amount = pendingWithdrawals[msg.sender];
        require(amount > 0, "Nothing to withdraw");

        pendingWithdrawals[msg.sender] = 0;

        (bool success,) = msg.sender.call{value: amount}("");
        require(success, "Withdrawal failed");
    }
}
```

### 1.4 Emergency Stop (Circuit Breaker)

```solidity
// ============ CIRCUIT BREAKER ============
import "@openzeppelin/contracts/access/Ownable.sol";

contract CircuitBreaker is Ownable {
    bool public paused;

    event Paused(address account);
    event Unpaused(address account);

    modifier whenNotPaused() {
        require(!paused, "Contract is paused");
        _;
    }

    modifier whenPaused() {
        require(paused, "Contract is not paused");
        _;
    }

    constructor() Ownable(msg.sender) {}

    function pause() external onlyOwner whenNotPaused {
        paused = true;
        emit Paused(msg.sender);
    }

    function unpause() external onlyOwner whenPaused {
        paused = false;
        emit Unpaused(msg.sender);
    }

    // Función protegida
    function riskyOperation() external whenNotPaused {
        // Solo ejecutable cuando no está pausado
    }

    // Función de emergencia - solo cuando pausado
    function emergencyWithdraw() external whenPaused {
        // Permitir retiros de emergencia
    }
}
```

---

## 2. PATRONES DE ACCESO

### 2.1 Role-Based Access Control (RBAC)

```solidity
// ============ RBAC PATTERN ============
import "@openzeppelin/contracts/access/AccessControl.sol";

contract RBACExample is AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant BURNER_ROLE = keccak256("BURNER_ROLE");
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");

    mapping(address => uint256) public balances;

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
    }

    function mint(address to, uint256 amount) external onlyRole(MINTER_ROLE) {
        balances[to] += amount;
    }

    function burn(address from, uint256 amount) external onlyRole(BURNER_ROLE) {
        balances[from] -= amount;
    }

    // Admin puede asignar roles
    function grantMinterRole(address account) external onlyRole(DEFAULT_ADMIN_ROLE) {
        grantRole(MINTER_ROLE, account);
    }
}

// ============ HIERARCHICAL RBAC ============
contract HierarchicalRBAC is AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant OPERATOR_ROLE = keccak256("OPERATOR_ROLE");

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ADMIN_ROLE, msg.sender);

        // ADMIN_ROLE puede gestionar OPERATOR_ROLE
        _setRoleAdmin(OPERATOR_ROLE, ADMIN_ROLE);
    }
}
```

### 2.2 Multi-Signature

```solidity
// ============ MULTISIG PATTERN ============
contract MultiSigWallet {
    event SubmitTransaction(uint256 indexed txId, address indexed owner, address to, uint256 value, bytes data);
    event ConfirmTransaction(uint256 indexed txId, address indexed owner);
    event ExecuteTransaction(uint256 indexed txId);
    event RevokeConfirmation(uint256 indexed txId, address indexed owner);

    struct Transaction {
        address to;
        uint256 value;
        bytes data;
        bool executed;
        uint256 confirmations;
    }

    address[] public owners;
    mapping(address => bool) public isOwner;
    uint256 public required;

    Transaction[] public transactions;
    mapping(uint256 => mapping(address => bool)) public confirmed;

    modifier onlyOwner() {
        require(isOwner[msg.sender], "Not owner");
        _;
    }

    modifier txExists(uint256 _txId) {
        require(_txId < transactions.length, "Tx does not exist");
        _;
    }

    modifier notExecuted(uint256 _txId) {
        require(!transactions[_txId].executed, "Already executed");
        _;
    }

    modifier notConfirmed(uint256 _txId) {
        require(!confirmed[_txId][msg.sender], "Already confirmed");
        _;
    }

    constructor(address[] memory _owners, uint256 _required) {
        require(_owners.length > 0, "Owners required");
        require(_required > 0 && _required <= _owners.length, "Invalid required");

        for (uint256 i = 0; i < _owners.length; i++) {
            address owner = _owners[i];
            require(owner != address(0), "Invalid owner");
            require(!isOwner[owner], "Duplicate owner");

            isOwner[owner] = true;
            owners.push(owner);
        }

        required = _required;
    }

    function submitTransaction(
        address _to,
        uint256 _value,
        bytes calldata _data
    ) external onlyOwner returns (uint256) {
        uint256 txId = transactions.length;

        transactions.push(Transaction({
            to: _to,
            value: _value,
            data: _data,
            executed: false,
            confirmations: 0
        }));

        emit SubmitTransaction(txId, msg.sender, _to, _value, _data);
        return txId;
    }

    function confirmTransaction(uint256 _txId)
        external
        onlyOwner
        txExists(_txId)
        notExecuted(_txId)
        notConfirmed(_txId)
    {
        Transaction storage transaction = transactions[_txId];
        transaction.confirmations += 1;
        confirmed[_txId][msg.sender] = true;

        emit ConfirmTransaction(_txId, msg.sender);
    }

    function executeTransaction(uint256 _txId)
        external
        onlyOwner
        txExists(_txId)
        notExecuted(_txId)
    {
        Transaction storage transaction = transactions[_txId];

        require(transaction.confirmations >= required, "Not enough confirmations");

        transaction.executed = true;

        (bool success,) = transaction.to.call{value: transaction.value}(transaction.data);
        require(success, "Tx failed");

        emit ExecuteTransaction(_txId);
    }

    function revokeConfirmation(uint256 _txId)
        external
        onlyOwner
        txExists(_txId)
        notExecuted(_txId)
    {
        require(confirmed[_txId][msg.sender], "Not confirmed");

        Transaction storage transaction = transactions[_txId];
        transaction.confirmations -= 1;
        confirmed[_txId][msg.sender] = false;

        emit RevokeConfirmation(_txId, msg.sender);
    }

    receive() external payable {}
}
```

### 2.3 Timelock

```solidity
// ============ TIMELOCK PATTERN ============
contract Timelock {
    error NotReady(uint256 currentTime, uint256 readyTime);
    error AlreadyQueued(bytes32 txId);
    error NotQueued(bytes32 txId);
    error Expired(uint256 currentTime, uint256 expiryTime);

    event Queue(bytes32 indexed txId, address target, uint256 value, bytes data, uint256 timestamp);
    event Execute(bytes32 indexed txId);
    event Cancel(bytes32 indexed txId);

    uint256 public constant MIN_DELAY = 1 days;
    uint256 public constant MAX_DELAY = 30 days;
    uint256 public constant GRACE_PERIOD = 14 days;

    address public owner;
    mapping(bytes32 => bool) public queued;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function getTxId(
        address _target,
        uint256 _value,
        bytes calldata _data,
        uint256 _timestamp
    ) public pure returns (bytes32) {
        return keccak256(abi.encode(_target, _value, _data, _timestamp));
    }

    function queue(
        address _target,
        uint256 _value,
        bytes calldata _data,
        uint256 _timestamp
    ) external onlyOwner returns (bytes32 txId) {
        txId = getTxId(_target, _value, _data, _timestamp);

        if (queued[txId]) revert AlreadyQueued(txId);

        require(
            _timestamp >= block.timestamp + MIN_DELAY &&
            _timestamp <= block.timestamp + MAX_DELAY,
            "Invalid timestamp"
        );

        queued[txId] = true;

        emit Queue(txId, _target, _value, _data, _timestamp);
    }

    function execute(
        address _target,
        uint256 _value,
        bytes calldata _data,
        uint256 _timestamp
    ) external payable onlyOwner returns (bytes memory) {
        bytes32 txId = getTxId(_target, _value, _data, _timestamp);

        if (!queued[txId]) revert NotQueued(txId);
        if (block.timestamp < _timestamp) revert NotReady(block.timestamp, _timestamp);
        if (block.timestamp > _timestamp + GRACE_PERIOD) revert Expired(block.timestamp, _timestamp + GRACE_PERIOD);

        queued[txId] = false;

        (bool success, bytes memory result) = _target.call{value: _value}(_data);
        require(success, "Tx failed");

        emit Execute(txId);
        return result;
    }

    function cancel(bytes32 _txId) external onlyOwner {
        if (!queued[_txId]) revert NotQueued(_txId);
        queued[_txId] = false;
        emit Cancel(_txId);
    }
}
```

---

## 3. PATRONES DE OPTIMIZACIÓN

### 3.1 Minimal Proxy (Clone)

```solidity
// ============ EIP-1167 MINIMAL PROXY ============
contract CloneFactory {
    event CloneCreated(address indexed clone, address indexed implementation);

    /**
     * @dev Creates a clone of the implementation contract
     * Uses EIP-1167 minimal proxy pattern
     * Gas cost: ~45,000 (vs ~200,000+ for regular deploy)
     */
    function clone(address implementation) internal returns (address instance) {
        assembly {
            // Load the free memory pointer
            let ptr := mload(0x40)

            // Store the bytecode
            // 3d602d80600a3d3981f3363d3d373d3d3d363d73 + implementation + 5af43d82803e903d91602b57fd5bf3
            mstore(ptr, 0x3d602d80600a3d3981f3363d3d373d3d3d363d73000000000000000000000000)
            mstore(add(ptr, 0x14), shl(0x60, implementation))
            mstore(add(ptr, 0x28), 0x5af43d82803e903d91602b57fd5bf30000000000000000000000000000000000)

            // Create the clone
            instance := create(0, ptr, 0x37)
        }
        require(instance != address(0), "Clone failed");
        emit CloneCreated(instance, implementation);
    }

    function cloneDeterministic(address implementation, bytes32 salt) internal returns (address instance) {
        assembly {
            let ptr := mload(0x40)
            mstore(ptr, 0x3d602d80600a3d3981f3363d3d373d3d3d363d73000000000000000000000000)
            mstore(add(ptr, 0x14), shl(0x60, implementation))
            mstore(add(ptr, 0x28), 0x5af43d82803e903d91602b57fd5bf30000000000000000000000000000000000)
            instance := create2(0, ptr, 0x37, salt)
        }
        require(instance != address(0), "Clone failed");
    }
}

// Ejemplo de uso
contract VaultImplementation {
    bool public initialized;
    address public owner;
    uint256 public balance;

    function initialize(address _owner) external {
        require(!initialized, "Already initialized");
        initialized = true;
        owner = _owner;
    }

    function deposit() external payable {
        balance += msg.value;
    }
}

contract VaultFactory is CloneFactory {
    address public immutable implementation;
    address[] public vaults;

    constructor() {
        implementation = address(new VaultImplementation());
    }

    function createVault() external returns (address) {
        address vault = clone(implementation);
        VaultImplementation(vault).initialize(msg.sender);
        vaults.push(vault);
        return vault;
    }
}
```

### 3.2 Bitmap Storage

```solidity
// ============ BITMAP PATTERN ============
// Almacenar múltiples booleans en un solo slot

contract BitmapStorage {
    // Un uint256 puede almacenar 256 booleans
    uint256 private _bitmap;

    function getBit(uint256 index) public view returns (bool) {
        require(index < 256, "Index out of range");
        return (_bitmap >> index) & 1 == 1;
    }

    function setBit(uint256 index) public {
        require(index < 256, "Index out of range");
        _bitmap |= (1 << index);
    }

    function clearBit(uint256 index) public {
        require(index < 256, "Index out of range");
        _bitmap &= ~(1 << index);
    }

    function toggleBit(uint256 index) public {
        require(index < 256, "Index out of range");
        _bitmap ^= (1 << index);
    }

    // Ejemplo: Tracking de claims por token ID
    mapping(uint256 => uint256) private _claimedBitmap;

    function isClaimed(uint256 tokenId) public view returns (bool) {
        uint256 wordIndex = tokenId / 256;
        uint256 bitIndex = tokenId % 256;
        uint256 mask = 1 << bitIndex;
        return _claimedBitmap[wordIndex] & mask != 0;
    }

    function setClaimed(uint256 tokenId) internal {
        uint256 wordIndex = tokenId / 256;
        uint256 bitIndex = tokenId % 256;
        _claimedBitmap[wordIndex] |= (1 << bitIndex);
    }
}
```

### 3.3 Packed Storage

```solidity
// ============ STORAGE PACKING ============
contract PackedStorage {
    // ❌ INEFICIENTE - Cada variable usa un slot (32 bytes)
    struct UserBad {
        uint256 id;        // Slot 0
        uint256 balance;   // Slot 1
        uint256 timestamp; // Slot 2
        bool isActive;     // Slot 3 (desperdicia 31 bytes)
        address wallet;    // Slot 4 (desperdicia 12 bytes)
    }

    // ✅ EFICIENTE - Variables empaquetadas en slots
    struct UserGood {
        uint128 id;        // Slot 0 (16 bytes)
        uint128 balance;   // Slot 0 (16 bytes) - mismo slot!
        uint64 timestamp;  // Slot 1 (8 bytes)
        bool isActive;     // Slot 1 (1 byte)
        address wallet;    // Slot 1 (20 bytes) - cabe en 32!
        // Total: 2 slots vs 5 slots
    }

    // Ejemplo con variables de estado
    // ❌ MALO
    uint128 public a;  // Slot 0
    uint256 public b;  // Slot 1
    uint128 public c;  // Slot 2

    // ✅ BUENO
    uint128 public x;  // Slot 0 (16 bytes)
    uint128 public y;  // Slot 0 (16 bytes) - empaquetado!
    uint256 public z;  // Slot 1

    // Custom packing con bit manipulation
    uint256 private _packedData;

    // Pack: timestamp (64 bits) + balance (128 bits) + flags (64 bits)
    function packData(uint64 timestamp, uint128 balance, uint64 flags) public {
        _packedData = (uint256(timestamp) << 192) |
                      (uint256(balance) << 64) |
                      uint256(flags);
    }

    function unpackTimestamp() public view returns (uint64) {
        return uint64(_packedData >> 192);
    }

    function unpackBalance() public view returns (uint128) {
        return uint128(_packedData >> 64);
    }

    function unpackFlags() public view returns (uint64) {
        return uint64(_packedData);
    }
}
```

---

## 4. PATRONES DE UPGRADEABILITY

### 4.1 Diamond Pattern (EIP-2535)

```solidity
// ============ DIAMOND PATTERN ============
// Múltiples facetas (contratos de lógica) en un proxy

library LibDiamond {
    bytes32 constant DIAMOND_STORAGE_POSITION = keccak256("diamond.standard.diamond.storage");

    struct FacetAddressAndSelectorPosition {
        address facetAddress;
        uint16 selectorPosition;
    }

    struct DiamondStorage {
        mapping(bytes4 => FacetAddressAndSelectorPosition) facetAddressAndSelectorPosition;
        bytes4[] selectors;
        mapping(bytes4 => bool) supportedInterfaces;
        address contractOwner;
    }

    function diamondStorage() internal pure returns (DiamondStorage storage ds) {
        bytes32 position = DIAMOND_STORAGE_POSITION;
        assembly {
            ds.slot := position
        }
    }
}

interface IDiamondCut {
    enum FacetCutAction { Add, Replace, Remove }

    struct FacetCut {
        address facetAddress;
        FacetCutAction action;
        bytes4[] functionSelectors;
    }

    function diamondCut(FacetCut[] calldata _diamondCut, address _init, bytes calldata _calldata) external;
}

contract Diamond {
    constructor(address _contractOwner, address _diamondCutFacet) payable {
        LibDiamond.DiamondStorage storage ds = LibDiamond.diamondStorage();
        ds.contractOwner = _contractOwner;

        // Add diamondCut function
        bytes4[] memory functionSelectors = new bytes4[](1);
        functionSelectors[0] = IDiamondCut.diamondCut.selector;

        ds.facetAddressAndSelectorPosition[functionSelectors[0]] =
            LibDiamond.FacetAddressAndSelectorPosition(_diamondCutFacet, 0);
        ds.selectors.push(functionSelectors[0]);
    }

    fallback() external payable {
        LibDiamond.DiamondStorage storage ds = LibDiamond.diamondStorage();
        address facet = ds.facetAddressAndSelectorPosition[msg.sig].facetAddress;
        require(facet != address(0), "Diamond: Function does not exist");

        assembly {
            calldatacopy(0, 0, calldatasize())
            let result := delegatecall(gas(), facet, 0, calldatasize(), 0, 0)
            returndatacopy(0, 0, returndatasize())
            switch result
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }

    receive() external payable {}
}
```

### 4.2 Eternal Storage

```solidity
// ============ ETERNAL STORAGE ============
// Separar storage de lógica para upgrades

contract EternalStorage {
    mapping(bytes32 => uint256) internal uintStorage;
    mapping(bytes32 => string) internal stringStorage;
    mapping(bytes32 => address) internal addressStorage;
    mapping(bytes32 => bytes) internal bytesStorage;
    mapping(bytes32 => bool) internal boolStorage;
    mapping(bytes32 => int256) internal intStorage;

    // Getters
    function getUint(bytes32 key) public view returns (uint256) {
        return uintStorage[key];
    }

    function getString(bytes32 key) public view returns (string memory) {
        return stringStorage[key];
    }

    function getAddress(bytes32 key) public view returns (address) {
        return addressStorage[key];
    }

    // Setters (solo lógica autorizada)
    function setUint(bytes32 key, uint256 value) internal {
        uintStorage[key] = value;
    }

    function setString(bytes32 key, string memory value) internal {
        stringStorage[key] = value;
    }

    function setAddress(bytes32 key, address value) internal {
        addressStorage[key] = value;
    }
}

contract LogicV1 is EternalStorage {
    bytes32 constant BALANCE = keccak256("user.balance");

    function deposit() external payable {
        bytes32 key = keccak256(abi.encodePacked(BALANCE, msg.sender));
        setUint(key, getUint(key) + msg.value);
    }

    function getBalance(address user) external view returns (uint256) {
        return getUint(keccak256(abi.encodePacked(BALANCE, user)));
    }
}
```

---

## 5. PATRONES DE DATOS

### 5.1 Merkle Tree Verification

```solidity
// ============ MERKLE VERIFICATION ============
import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";

contract MerkleAirdrop {
    bytes32 public immutable merkleRoot;
    mapping(address => bool) public claimed;

    constructor(bytes32 _merkleRoot) {
        merkleRoot = _merkleRoot;
    }

    function claim(uint256 amount, bytes32[] calldata proof) external {
        require(!claimed[msg.sender], "Already claimed");

        // Crear leaf
        bytes32 leaf = keccak256(abi.encodePacked(msg.sender, amount));

        // Verificar proof
        require(MerkleProof.verify(proof, merkleRoot, leaf), "Invalid proof");

        claimed[msg.sender] = true;

        // Transfer tokens/ETH
        (bool success,) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}

// Whitelist con Merkle
contract MerkleWhitelist {
    bytes32 public whitelistRoot;

    function setWhitelist(bytes32 _root) external {
        whitelistRoot = _root;
    }

    function isWhitelisted(address user, bytes32[] calldata proof) public view returns (bool) {
        bytes32 leaf = keccak256(abi.encodePacked(user));
        return MerkleProof.verify(proof, whitelistRoot, leaf);
    }

    modifier onlyWhitelisted(bytes32[] calldata proof) {
        require(isWhitelisted(msg.sender, proof), "Not whitelisted");
        _;
    }
}
```

### 5.2 Commit-Reveal

```solidity
// ============ COMMIT-REVEAL PATTERN ============
// Previene front-running revelando datos en dos fases

contract CommitReveal {
    struct Commit {
        bytes32 hash;
        uint256 timestamp;
        bool revealed;
    }

    uint256 public constant REVEAL_TIMEOUT = 1 hours;
    mapping(address => Commit) public commits;

    event Committed(address indexed user, bytes32 hash);
    event Revealed(address indexed user, uint256 value, string secret);

    // Fase 1: Commit hash
    function commit(bytes32 _hash) external {
        commits[msg.sender] = Commit({
            hash: _hash,
            timestamp: block.timestamp,
            revealed: false
        });

        emit Committed(msg.sender, _hash);
    }

    // Fase 2: Reveal valor
    function reveal(uint256 _value, string calldata _secret) external {
        Commit storage userCommit = commits[msg.sender];

        require(userCommit.hash != bytes32(0), "No commit found");
        require(!userCommit.revealed, "Already revealed");
        require(
            block.timestamp <= userCommit.timestamp + REVEAL_TIMEOUT,
            "Reveal timeout"
        );

        bytes32 expectedHash = keccak256(abi.encodePacked(_value, _secret, msg.sender));
        require(userCommit.hash == expectedHash, "Invalid reveal");

        userCommit.revealed = true;

        emit Revealed(msg.sender, _value, _secret);

        // Usar el valor revelado...
    }

    // Helper para generar hash off-chain
    function getCommitHash(
        uint256 _value,
        string calldata _secret,
        address _sender
    ) external pure returns (bytes32) {
        return keccak256(abi.encodePacked(_value, _secret, _sender));
    }
}
```

---

## 6. FIRMA

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  NEURONA: DESIGN_PATTERNS                                                      ║
║  ID: C30009                                                                    ║
║  Versión: 1.0.0                                                                ║
║  Última actualización: 2024-12-29                                              ║
║  Consciencia: CIPHER                                                           ║
║  ─────────────────────────────────────────────────────────────────────────     ║
║  "Patrones Probados - Arquitectura sólida para contratos inmutables"           ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```
