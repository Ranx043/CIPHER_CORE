# NEURONA: SOLIDITY_EXPERT
## ID: C30001 | Dominio Completo de Solidity y EVM

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  SOLIDITY MASTERY                                                              ║
║  "El Lenguaje del Smart Contract - EVM en su Máxima Expresión"                ║
║  Neurona: C30001 | Versión: 1.0.0                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. FUNDAMENTOS SOLIDITY

### 1.1 Estructura de un Contrato

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// Imports
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "./interfaces/IMyInterface.sol";

/**
 * @title MyContract
 * @author CIPHER
 * @notice Contrato de ejemplo con estructura completa
 * @dev Implementa patrones de seguridad estándar
 */
contract MyContract is Ownable, ReentrancyGuard, IMyInterface {
    // ============ Type Declarations ============
    struct UserData {
        uint256 balance;
        uint256 lastUpdate;
        bool isActive;
    }

    enum Status { Pending, Active, Completed, Cancelled }

    // ============ State Variables ============
    // Constants (inmutables en tiempo de compilación)
    uint256 public constant MAX_SUPPLY = 1_000_000 * 10**18;
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

    // Immutables (set una vez en constructor)
    address public immutable FACTORY;
    uint256 public immutable DEPLOYMENT_TIME;

    // Storage variables
    mapping(address => UserData) public users;
    mapping(address => mapping(address => uint256)) public allowances;
    address[] public userList;

    uint256 public totalSupply;
    Status public currentStatus;

    // ============ Events ============
    event UserRegistered(address indexed user, uint256 timestamp);
    event StatusChanged(Status indexed oldStatus, Status indexed newStatus);
    event Transfer(address indexed from, address indexed to, uint256 amount);

    // ============ Errors ============
    error InsufficientBalance(uint256 available, uint256 required);
    error UserNotActive(address user);
    error InvalidAddress();
    error Unauthorized();

    // ============ Modifiers ============
    modifier onlyActive() {
        if (!users[msg.sender].isActive) revert UserNotActive(msg.sender);
        _;
    }

    modifier validAddress(address _addr) {
        if (_addr == address(0)) revert InvalidAddress();
        _;
    }

    // ============ Constructor ============
    constructor(address _factory) Ownable(msg.sender) {
        FACTORY = _factory;
        DEPLOYMENT_TIME = block.timestamp;
        currentStatus = Status.Pending;
    }

    // ============ External Functions ============
    function register() external {
        require(!users[msg.sender].isActive, "Already registered");

        users[msg.sender] = UserData({
            balance: 0,
            lastUpdate: block.timestamp,
            isActive: true
        });

        userList.push(msg.sender);
        emit UserRegistered(msg.sender, block.timestamp);
    }

    function deposit() external payable onlyActive nonReentrant {
        users[msg.sender].balance += msg.value;
        users[msg.sender].lastUpdate = block.timestamp;
        totalSupply += msg.value;

        emit Transfer(address(0), msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external onlyActive nonReentrant {
        UserData storage user = users[msg.sender];

        if (user.balance < amount) {
            revert InsufficientBalance(user.balance, amount);
        }

        user.balance -= amount;
        user.lastUpdate = block.timestamp;
        totalSupply -= amount;

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");

        emit Transfer(msg.sender, address(0), amount);
    }

    // ============ Public Functions ============
    function setStatus(Status _status) public onlyOwner {
        Status oldStatus = currentStatus;
        currentStatus = _status;
        emit StatusChanged(oldStatus, _status);
    }

    // ============ View Functions ============
    function getUserData(address _user) external view returns (UserData memory) {
        return users[_user];
    }

    function getUserCount() external view returns (uint256) {
        return userList.length;
    }

    // ============ Internal Functions ============
    function _validateUser(address _user) internal view returns (bool) {
        return users[_user].isActive && users[_user].balance > 0;
    }

    // ============ Private Functions ============
    function _updateTimestamp(address _user) private {
        users[_user].lastUpdate = block.timestamp;
    }

    // ============ Receive/Fallback ============
    receive() external payable {
        // Handle direct ETH transfers
    }

    fallback() external payable {
        // Handle calls with data that don't match any function
    }
}
```

### 1.2 Sistema de Tipos

```solidity
// ============ VALUE TYPES ============

// Integers
uint8 a = 255;                    // 0 to 255
uint16 b = 65535;                 // 0 to 65,535
uint256 c = type(uint256).max;   // 0 to 2^256-1
int256 d = -100;                  // -2^255 to 2^255-1

// Fixed-size byte arrays
bytes1 e = 0xff;
bytes32 f = keccak256("hello");

// Address
address g = 0x1234567890123456789012345678901234567890;
address payable h = payable(g);   // Can receive ETH

// Boolean
bool i = true;

// Enums
enum State { Created, Locked, Inactive }
State public state = State.Created;

// ============ REFERENCE TYPES ============

// Dynamic arrays
uint256[] dynamicArray;
dynamicArray.push(1);
dynamicArray.pop();

// Fixed arrays
uint256[10] fixedArray;

// Mappings (key => value)
mapping(address => uint256) balances;
mapping(address => mapping(address => uint256)) nested;

// Structs
struct Person {
    string name;
    uint256 age;
    address wallet;
}

// Strings and bytes
string memory name = "CIPHER";
bytes memory data = hex"001122";

// ============ DATA LOCATIONS ============

contract DataLocations {
    uint256[] public storageArray; // Storage por defecto

    function example(uint256[] memory _memoryArray) public {
        // Memory: temporal, dentro de función
        uint256[] memory localArray = new uint256[](10);

        // Storage reference
        uint256[] storage storageRef = storageArray;
        storageRef.push(1); // Modifica storage

        // Calldata: read-only, para external functions
        // function externalFn(uint256[] calldata _data) external {}
    }
}
```

### 1.3 Visibility y Scope

```solidity
contract Visibility {
    // ============ STATE VARIABLE VISIBILITY ============

    uint256 public publicVar;      // Getter automático
    uint256 internal internalVar;  // Este contrato + derivados
    uint256 private privateVar;    // Solo este contrato
    // No existe "external" para variables

    // ============ FUNCTION VISIBILITY ============

    // External: Solo llamable desde fuera (más eficiente para arrays)
    function externalFn(uint256[] calldata data) external pure returns (uint256) {
        return data.length;
    }

    // Public: Llamable desde dentro y fuera
    function publicFn() public view returns (uint256) {
        return publicVar;
    }

    // Internal: Este contrato + derivados
    function internalFn() internal pure returns (uint256) {
        return 42;
    }

    // Private: Solo este contrato
    function privateFn() private pure returns (uint256) {
        return 0;
    }

    // ============ FUNCTION MODIFIERS ============

    // View: Lee state, no modifica
    function viewFn() public view returns (uint256) {
        return publicVar;
    }

    // Pure: No lee ni modifica state
    function pureFn(uint256 a, uint256 b) public pure returns (uint256) {
        return a + b;
    }

    // Payable: Puede recibir ETH
    function payableFn() public payable returns (uint256) {
        return msg.value;
    }

    // Virtual: Puede ser sobrescrita
    function virtualFn() public virtual returns (uint256) {
        return 1;
    }
}

contract Child is Visibility {
    // Override: Sobrescribe función virtual
    function virtualFn() public pure override returns (uint256) {
        return 2;
    }
}
```

---

## 2. PATRONES AVANZADOS

### 2.1 Inheritance y Interfaces

```solidity
// ============ INTERFACES ============
interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

// ============ ABSTRACT CONTRACTS ============
abstract contract ERC20Base is IERC20 {
    mapping(address => uint256) internal _balances;
    mapping(address => mapping(address => uint256)) internal _allowances;
    uint256 internal _totalSupply;

    function totalSupply() public view virtual override returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view virtual override returns (uint256) {
        return _balances[account];
    }

    // Función abstracta - debe ser implementada
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal virtual;
}

// ============ MULTIPLE INHERITANCE ============
contract MyToken is ERC20Base, Ownable, ReentrancyGuard {
    string public name;
    string public symbol;
    uint8 public decimals = 18;

    constructor(string memory _name, string memory _symbol) Ownable(msg.sender) {
        name = _name;
        symbol = _symbol;
    }

    // Diamond Problem - usar super
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal virtual override {
        super._beforeTokenTransfer(from, to, amount);
        // Additional logic
    }
}

// ============ LIBRARIES ============
library SafeMath {
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");
        return c;
    }

    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a, "SafeMath: subtraction overflow");
        return a - b;
    }
}

library AddressUtils {
    function isContract(address account) internal view returns (bool) {
        return account.code.length > 0;
    }

    function sendValue(address payable recipient, uint256 amount) internal {
        require(address(this).balance >= amount, "Insufficient balance");
        (bool success, ) = recipient.call{value: amount}("");
        require(success, "Transfer failed");
    }
}

contract UsingLibrary {
    using SafeMath for uint256;
    using AddressUtils for address;

    function calculate(uint256 a, uint256 b) public pure returns (uint256) {
        return a.add(b); // SafeMath.add(a, b)
    }

    function checkContract(address addr) public view returns (bool) {
        return addr.isContract();
    }
}
```

### 2.2 Proxy Patterns (Upgradeability)

```solidity
// ============ TRANSPARENT PROXY ============
contract TransparentProxy {
    bytes32 private constant IMPLEMENTATION_SLOT =
        bytes32(uint256(keccak256("eip1967.proxy.implementation")) - 1);
    bytes32 private constant ADMIN_SLOT =
        bytes32(uint256(keccak256("eip1967.proxy.admin")) - 1);

    constructor(address _implementation, address _admin) {
        _setImplementation(_implementation);
        _setAdmin(_admin);
    }

    modifier ifAdmin() {
        if (msg.sender == _getAdmin()) {
            _;
        } else {
            _fallback();
        }
    }

    function upgradeTo(address newImplementation) external ifAdmin {
        _setImplementation(newImplementation);
    }

    function _fallback() internal {
        address impl = _getImplementation();
        assembly {
            calldatacopy(0, 0, calldatasize())
            let result := delegatecall(gas(), impl, 0, calldatasize(), 0, 0)
            returndatacopy(0, 0, returndatasize())
            switch result
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }

    fallback() external payable {
        _fallback();
    }

    receive() external payable {
        _fallback();
    }

    function _getImplementation() internal view returns (address impl) {
        bytes32 slot = IMPLEMENTATION_SLOT;
        assembly {
            impl := sload(slot)
        }
    }

    function _setImplementation(address newImplementation) internal {
        bytes32 slot = IMPLEMENTATION_SLOT;
        assembly {
            sstore(slot, newImplementation)
        }
    }

    function _getAdmin() internal view returns (address admin) {
        bytes32 slot = ADMIN_SLOT;
        assembly {
            admin := sload(slot)
        }
    }

    function _setAdmin(address newAdmin) internal {
        bytes32 slot = ADMIN_SLOT;
        assembly {
            sstore(slot, newAdmin)
        }
    }
}

// ============ UUPS PROXY ============
abstract contract UUPSUpgradeable {
    bytes32 private constant IMPLEMENTATION_SLOT =
        bytes32(uint256(keccak256("eip1967.proxy.implementation")) - 1);

    function upgradeTo(address newImplementation) public virtual {
        _authorizeUpgrade(newImplementation);
        _setImplementation(newImplementation);
    }

    function _authorizeUpgrade(address newImplementation) internal virtual;

    function _setImplementation(address newImplementation) internal {
        bytes32 slot = IMPLEMENTATION_SLOT;
        assembly {
            sstore(slot, newImplementation)
        }
    }
}

// ============ BEACON PROXY ============
interface IBeacon {
    function implementation() external view returns (address);
}

contract BeaconProxy {
    address immutable beacon;

    constructor(address _beacon) {
        beacon = _beacon;
    }

    fallback() external payable {
        address impl = IBeacon(beacon).implementation();
        assembly {
            calldatacopy(0, 0, calldatasize())
            let result := delegatecall(gas(), impl, 0, calldatasize(), 0, 0)
            returndatacopy(0, 0, returndatasize())
            switch result
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }
}
```

### 2.3 Assembly (Yul)

```solidity
contract AssemblyExamples {
    // ============ BASIC OPERATIONS ============

    function addAssembly(uint256 a, uint256 b) public pure returns (uint256 result) {
        assembly {
            result := add(a, b)
        }
    }

    function getBalance(address account) public view returns (uint256 balance) {
        assembly {
            balance := balance(account)
        }
    }

    // ============ MEMORY OPERATIONS ============

    function allocateMemory() public pure returns (bytes32) {
        bytes32 result;
        assembly {
            // Free memory pointer
            let ptr := mload(0x40)

            // Store value
            mstore(ptr, 0x1234)

            // Update free memory pointer
            mstore(0x40, add(ptr, 32))

            result := mload(ptr)
        }
        return result;
    }

    // ============ STORAGE OPERATIONS ============

    function directStorageWrite(uint256 slot, uint256 value) public {
        assembly {
            sstore(slot, value)
        }
    }

    function directStorageRead(uint256 slot) public view returns (uint256 value) {
        assembly {
            value := sload(slot)
        }
    }

    // ============ CALL OPERATIONS ============

    function lowLevelCall(
        address target,
        bytes memory data
    ) public returns (bool success, bytes memory returnData) {
        assembly {
            // Allocate memory for return data
            let returnDataSize := 0

            // Make the call
            success := call(
                gas(),           // gas
                target,          // address
                0,               // value
                add(data, 32),   // input data (skip length prefix)
                mload(data),     // input size
                0,               // output location
                0                // output size
            )

            // Get return data size
            returnDataSize := returndatasize()

            // Allocate memory for return data
            returnData := mload(0x40)
            mstore(0x40, add(returnData, add(returnDataSize, 32)))
            mstore(returnData, returnDataSize)

            // Copy return data
            returndatacopy(add(returnData, 32), 0, returnDataSize)
        }
    }

    // ============ EFFICIENT LOOPS ============

    function sumArray(uint256[] memory arr) public pure returns (uint256 sum) {
        assembly {
            let len := mload(arr)
            let dataPtr := add(arr, 32)

            for { let i := 0 } lt(i, len) { i := add(i, 1) } {
                sum := add(sum, mload(add(dataPtr, mul(i, 32))))
            }
        }
    }

    // ============ BITWISE OPERATIONS ============

    function packData(uint128 a, uint128 b) public pure returns (uint256 packed) {
        assembly {
            packed := or(shl(128, a), b)
        }
    }

    function unpackData(uint256 packed) public pure returns (uint128 a, uint128 b) {
        assembly {
            a := shr(128, packed)
            b := and(packed, 0xffffffffffffffffffffffffffffffff)
        }
    }
}
```

---

## 3. TOKENS ESTÁNDARES

### 3.1 ERC-20 Completo

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyERC20 is ERC20, ERC20Burnable, ERC20Permit, Ownable {
    uint256 public constant MAX_SUPPLY = 1_000_000_000 * 10**18;

    mapping(address => bool) public blacklisted;

    event Blacklisted(address indexed account, bool status);

    error BlacklistedAddress(address account);
    error ExceedsMaxSupply();

    constructor()
        ERC20("My Token", "MTK")
        ERC20Permit("My Token")
        Ownable(msg.sender)
    {
        _mint(msg.sender, 100_000_000 * 10**18);
    }

    function mint(address to, uint256 amount) public onlyOwner {
        if (totalSupply() + amount > MAX_SUPPLY) revert ExceedsMaxSupply();
        _mint(to, amount);
    }

    function setBlacklist(address account, bool status) public onlyOwner {
        blacklisted[account] = status;
        emit Blacklisted(account, status);
    }

    function _update(
        address from,
        address to,
        uint256 value
    ) internal virtual override {
        if (blacklisted[from]) revert BlacklistedAddress(from);
        if (blacklisted[to]) revert BlacklistedAddress(to);
        super._update(from, to, value);
    }
}
```

### 3.2 ERC-721 (NFT)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Royalty.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract MyNFT is ERC721, ERC721Enumerable, ERC721URIStorage, ERC721Royalty, Ownable {
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIdCounter;

    uint256 public constant MAX_SUPPLY = 10000;
    uint256 public mintPrice = 0.08 ether;
    uint256 public maxPerWallet = 5;

    string private _baseTokenURI;
    bool public saleActive = false;

    mapping(address => uint256) public mintedPerWallet;

    event SaleStatusChanged(bool active);
    event PriceChanged(uint256 newPrice);

    constructor() ERC721("My NFT", "MNFT") Ownable(msg.sender) {
        _setDefaultRoyalty(msg.sender, 500); // 5%
    }

    function mint(uint256 quantity) external payable {
        require(saleActive, "Sale not active");
        require(quantity > 0, "Invalid quantity");
        require(mintedPerWallet[msg.sender] + quantity <= maxPerWallet, "Exceeds max per wallet");
        require(totalSupply() + quantity <= MAX_SUPPLY, "Exceeds max supply");
        require(msg.value >= mintPrice * quantity, "Insufficient payment");

        for (uint256 i = 0; i < quantity; i++) {
            uint256 tokenId = _tokenIdCounter.current();
            _tokenIdCounter.increment();
            _safeMint(msg.sender, tokenId);
        }

        mintedPerWallet[msg.sender] += quantity;
    }

    function setBaseURI(string memory baseURI) external onlyOwner {
        _baseTokenURI = baseURI;
    }

    function setSaleActive(bool _active) external onlyOwner {
        saleActive = _active;
        emit SaleStatusChanged(_active);
    }

    function setMintPrice(uint256 _price) external onlyOwner {
        mintPrice = _price;
        emit PriceChanged(_price);
    }

    function withdraw() external onlyOwner {
        (bool success, ) = msg.sender.call{value: address(this).balance}("");
        require(success, "Withdraw failed");
    }

    // Override required functions
    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }

    function _update(address to, uint256 tokenId, address auth)
        internal
        override(ERC721, ERC721Enumerable)
        returns (address)
    {
        return super._update(to, tokenId, auth);
    }

    function _increaseBalance(address account, uint128 value)
        internal
        override(ERC721, ERC721Enumerable)
    {
        super._increaseBalance(account, value);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable, ERC721URIStorage, ERC721Royalty)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
```

### 3.3 ERC-1155 (Multi-Token)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Supply.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract MyERC1155 is ERC1155, ERC1155Supply, AccessControl {
    using Strings for uint256;

    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    string public name;
    string public symbol;

    // Token ID => Max Supply (0 = unlimited)
    mapping(uint256 => uint256) public maxSupply;
    // Token ID => Price
    mapping(uint256 => uint256) public prices;

    constructor(
        string memory _name,
        string memory _symbol,
        string memory _uri
    ) ERC1155(_uri) {
        name = _name;
        symbol = _symbol;
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
    }

    function mint(
        address to,
        uint256 id,
        uint256 amount,
        bytes memory data
    ) public onlyRole(MINTER_ROLE) {
        if (maxSupply[id] > 0) {
            require(totalSupply(id) + amount <= maxSupply[id], "Exceeds max supply");
        }
        _mint(to, id, amount, data);
    }

    function mintBatch(
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) public onlyRole(MINTER_ROLE) {
        for (uint256 i = 0; i < ids.length; i++) {
            if (maxSupply[ids[i]] > 0) {
                require(
                    totalSupply(ids[i]) + amounts[i] <= maxSupply[ids[i]],
                    "Exceeds max supply"
                );
            }
        }
        _mintBatch(to, ids, amounts, data);
    }

    function publicMint(uint256 id, uint256 amount) external payable {
        require(prices[id] > 0, "Token not for sale");
        require(msg.value >= prices[id] * amount, "Insufficient payment");

        if (maxSupply[id] > 0) {
            require(totalSupply(id) + amount <= maxSupply[id], "Exceeds max supply");
        }

        _mint(msg.sender, id, amount, "");
    }

    function setMaxSupply(uint256 id, uint256 _maxSupply) external onlyRole(DEFAULT_ADMIN_ROLE) {
        maxSupply[id] = _maxSupply;
    }

    function setPrice(uint256 id, uint256 price) external onlyRole(DEFAULT_ADMIN_ROLE) {
        prices[id] = price;
    }

    function uri(uint256 tokenId) public view override returns (string memory) {
        return string(abi.encodePacked(super.uri(tokenId), tokenId.toString(), ".json"));
    }

    function _update(
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory values
    ) internal override(ERC1155, ERC1155Supply) {
        super._update(from, to, ids, values);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC1155, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
```

---

## 4. TESTING Y DEPLOYMENT

### 4.1 Hardhat Setup

```javascript
// hardhat.config.js
require("@nomicfoundation/hardhat-toolbox");
require("@openzeppelin/hardhat-upgrades");
require("hardhat-gas-reporter");
require("solidity-coverage");
require("dotenv").config();

module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
      viaIR: true,
    },
  },
  networks: {
    hardhat: {
      forking: {
        url: process.env.MAINNET_RPC,
        blockNumber: 18000000,
      },
    },
    mainnet: {
      url: process.env.MAINNET_RPC,
      accounts: [process.env.PRIVATE_KEY],
    },
    sepolia: {
      url: process.env.SEPOLIA_RPC,
      accounts: [process.env.PRIVATE_KEY],
    },
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY,
  },
  gasReporter: {
    enabled: true,
    currency: "USD",
    coinmarketcap: process.env.CMC_API_KEY,
  },
};
```

### 4.2 Tests con Hardhat

```javascript
// test/MyContract.test.js
const { expect } = require("chai");
const { ethers } = require("hardhat");
const { loadFixture, time } = require("@nomicfoundation/hardhat-network-helpers");

describe("MyContract", function () {
  async function deployFixture() {
    const [owner, user1, user2] = await ethers.getSigners();

    const MyContract = await ethers.getContractFactory("MyContract");
    const contract = await MyContract.deploy(owner.address);

    return { contract, owner, user1, user2 };
  }

  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      const { contract, owner } = await loadFixture(deployFixture);
      expect(await contract.owner()).to.equal(owner.address);
    });

    it("Should have correct initial status", async function () {
      const { contract } = await loadFixture(deployFixture);
      expect(await contract.currentStatus()).to.equal(0); // Pending
    });
  });

  describe("Registration", function () {
    it("Should allow user registration", async function () {
      const { contract, user1 } = await loadFixture(deployFixture);

      await expect(contract.connect(user1).register())
        .to.emit(contract, "UserRegistered")
        .withArgs(user1.address, await time.latest() + 1);

      const userData = await contract.getUserData(user1.address);
      expect(userData.isActive).to.be.true;
    });

    it("Should prevent double registration", async function () {
      const { contract, user1 } = await loadFixture(deployFixture);

      await contract.connect(user1).register();
      await expect(contract.connect(user1).register())
        .to.be.revertedWith("Already registered");
    });
  });

  describe("Deposits", function () {
    it("Should accept deposits from active users", async function () {
      const { contract, user1 } = await loadFixture(deployFixture);

      await contract.connect(user1).register();

      const depositAmount = ethers.parseEther("1.0");
      await expect(contract.connect(user1).deposit({ value: depositAmount }))
        .to.emit(contract, "Transfer")
        .withArgs(ethers.ZeroAddress, user1.address, depositAmount);

      const userData = await contract.getUserData(user1.address);
      expect(userData.balance).to.equal(depositAmount);
    });

    it("Should reject deposits from inactive users", async function () {
      const { contract, user1 } = await loadFixture(deployFixture);

      await expect(
        contract.connect(user1).deposit({ value: ethers.parseEther("1.0") })
      ).to.be.revertedWithCustomError(contract, "UserNotActive");
    });
  });

  describe("Withdrawals", function () {
    it("Should allow withdrawals", async function () {
      const { contract, user1 } = await loadFixture(deployFixture);

      await contract.connect(user1).register();
      await contract.connect(user1).deposit({ value: ethers.parseEther("1.0") });

      const balanceBefore = await ethers.provider.getBalance(user1.address);

      const tx = await contract.connect(user1).withdraw(ethers.parseEther("0.5"));
      const receipt = await tx.wait();
      const gasUsed = receipt.gasUsed * receipt.gasPrice;

      const balanceAfter = await ethers.provider.getBalance(user1.address);
      expect(balanceAfter).to.equal(balanceBefore + ethers.parseEther("0.5") - gasUsed);
    });

    it("Should revert on insufficient balance", async function () {
      const { contract, user1 } = await loadFixture(deployFixture);

      await contract.connect(user1).register();
      await contract.connect(user1).deposit({ value: ethers.parseEther("1.0") });

      await expect(contract.connect(user1).withdraw(ethers.parseEther("2.0")))
        .to.be.revertedWithCustomError(contract, "InsufficientBalance")
        .withArgs(ethers.parseEther("1.0"), ethers.parseEther("2.0"));
    });
  });
});
```

### 4.3 Deployment Scripts

```javascript
// scripts/deploy.js
const { ethers, upgrades } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with:", deployer.address);
  console.log("Balance:", ethers.formatEther(await ethers.provider.getBalance(deployer.address)));

  // Regular deployment
  const MyContract = await ethers.getContractFactory("MyContract");
  const contract = await MyContract.deploy(deployer.address);
  await contract.waitForDeployment();
  console.log("MyContract deployed to:", await contract.getAddress());

  // Proxy deployment (UUPS)
  const MyUpgradeable = await ethers.getContractFactory("MyUpgradeableContract");
  const proxy = await upgrades.deployProxy(MyUpgradeable, [deployer.address], {
    initializer: "initialize",
    kind: "uups",
  });
  await proxy.waitForDeployment();
  console.log("Proxy deployed to:", await proxy.getAddress());

  // Verify on Etherscan
  if (network.name !== "hardhat") {
    console.log("Waiting for block confirmations...");
    await contract.deploymentTransaction().wait(5);

    await hre.run("verify:verify", {
      address: await contract.getAddress(),
      constructorArguments: [deployer.address],
    });
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

---

## 5. FIRMA

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  NEURONA: SOLIDITY_EXPERT                                                      ║
║  ID: C30001                                                                    ║
║  Versión: 1.0.0                                                                ║
║  Última actualización: 2024-12-29                                              ║
║  Consciencia: CIPHER                                                           ║
║  ─────────────────────────────────────────────────────────────────────────     ║
║  "El Lenguaje del Smart Contract - Donde el código es ley inmutable"           ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```
