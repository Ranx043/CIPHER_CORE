# NEURONA C40012: NFT, GAMEFI & VIRTUAL ECONOMIES

> **CIPHER**: Dominio de NFTs, economías de juegos blockchain, metaversos y virtual assets.

---

## ÍNDICE

1. [Fundamentos NFT](#1-fundamentos-nft)
2. [Standards y Extensiones](#2-standards-y-extensiones)
3. [NFT Marketplaces](#3-nft-marketplaces)
4. [GameFi Economics](#4-gamefi-economics)
5. [Virtual Worlds & Metaverse](#5-virtual-worlds--metaverse)
6. [NFT Finance (NFTFi)](#6-nft-finance-nftfi)
7. [Análisis y Valuación](#7-análisis-y-valuación)

---

## 1. FUNDAMENTOS NFT

### 1.1 NFT Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         NFT ECOSYSTEM ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────────┐              │
│   │   CREATOR   │────▶│   CONTRACT  │────▶│    METADATA     │              │
│   │   (Minter)  │     │   (ERC-721) │     │    (IPFS/AR)    │              │
│   └─────────────┘     └──────┬──────┘     └─────────────────┘              │
│                              │                                               │
│                              ▼                                               │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────────┐              │
│   │  COLLECTOR  │◀───│ MARKETPLACE │◀────│    STORAGE      │              │
│   │   (Owner)   │     │  (OpenSea)  │     │  (IPFS/Arweave) │              │
│   └──────┬──────┘     └─────────────┘     └─────────────────┘              │
│          │                                                                   │
│          ▼                                                                   │
│   ┌─────────────────────────────────────────────────────────┐              │
│   │                    UTILITY LAYER                         │              │
│   │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │              │
│   │  │ Access  │ │ Gaming  │ │  DeFi   │ │ Social  │       │              │
│   │  │ Token   │ │  Asset  │ │ Collat  │ │Identity │       │              │
│   │  └─────────┘ └─────────┘ └─────────┘ └─────────┘       │              │
│   └─────────────────────────────────────────────────────────┘              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 ERC-721 Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Royalty.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

/**
 * @title CipherNFT
 * @notice NFT collection con royalties, metadata on-chain, y reveal mechanism
 */
contract CipherNFT is ERC721, ERC721URIStorage, ERC721Royalty, Ownable {
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIds;

    // Collection settings
    uint256 public maxSupply;
    uint256 public mintPrice;
    uint256 public maxPerWallet;

    // Reveal mechanism
    bool public revealed;
    string public hiddenMetadataURI;
    string public baseURI;

    // Minting phases
    enum Phase { CLOSED, WHITELIST, PUBLIC }
    Phase public currentPhase;

    // Whitelist
    mapping(address => bool) public whitelist;
    mapping(address => uint256) public mintedPerWallet;

    // On-chain attributes (ejemplo)
    struct TokenAttributes {
        uint8 rarity;      // 1-5
        uint8 power;       // 0-100
        uint8 element;     // 0=fire, 1=water, 2=earth, 3=air
        uint256 createdAt;
    }
    mapping(uint256 => TokenAttributes) public attributes;

    event TokenMinted(address indexed to, uint256 tokenId, TokenAttributes attrs);
    event Revealed(string baseURI);

    constructor(
        string memory name,
        string memory symbol,
        uint256 _maxSupply,
        uint256 _mintPrice,
        uint256 _maxPerWallet,
        string memory _hiddenURI,
        address royaltyReceiver,
        uint96 royaltyBps  // 250 = 2.5%
    ) ERC721(name, symbol) Ownable(msg.sender) {
        maxSupply = _maxSupply;
        mintPrice = _mintPrice;
        maxPerWallet = _maxPerWallet;
        hiddenMetadataURI = _hiddenURI;

        // Set default royalty for all tokens
        _setDefaultRoyalty(royaltyReceiver, royaltyBps);
    }

    /**
     * @notice Mint NFT durante whitelist phase
     */
    function whitelistMint(uint256 quantity) external payable {
        require(currentPhase == Phase.WHITELIST, "Not whitelist phase");
        require(whitelist[msg.sender], "Not whitelisted");
        _mintInternal(quantity);
    }

    /**
     * @notice Mint NFT durante public phase
     */
    function publicMint(uint256 quantity) external payable {
        require(currentPhase == Phase.PUBLIC, "Not public phase");
        _mintInternal(quantity);
    }

    function _mintInternal(uint256 quantity) internal {
        require(msg.value >= mintPrice * quantity, "Insufficient payment");
        require(mintedPerWallet[msg.sender] + quantity <= maxPerWallet, "Exceeds max per wallet");
        require(_tokenIds.current() + quantity <= maxSupply, "Exceeds max supply");

        for (uint256 i = 0; i < quantity; i++) {
            _tokenIds.increment();
            uint256 newTokenId = _tokenIds.current();

            _safeMint(msg.sender, newTokenId);

            // Generate on-chain attributes
            TokenAttributes memory attrs = _generateAttributes(newTokenId);
            attributes[newTokenId] = attrs;

            emit TokenMinted(msg.sender, newTokenId, attrs);
        }

        mintedPerWallet[msg.sender] += quantity;
    }

    /**
     * @notice Generar atributos pseudo-aleatorios on-chain
     * @dev En producción, usar VRF para aleatoriedad real
     */
    function _generateAttributes(uint256 tokenId) internal view returns (TokenAttributes memory) {
        uint256 seed = uint256(keccak256(abi.encodePacked(
            block.timestamp,
            block.prevrandao,
            msg.sender,
            tokenId
        )));

        // Rarity distribution: 50% común, 30% raro, 15% épico, 4% legendario, 1% mítico
        uint8 rarityRoll = uint8(seed % 100);
        uint8 rarity;
        if (rarityRoll < 50) rarity = 1;
        else if (rarityRoll < 80) rarity = 2;
        else if (rarityRoll < 95) rarity = 3;
        else if (rarityRoll < 99) rarity = 4;
        else rarity = 5;

        return TokenAttributes({
            rarity: rarity,
            power: uint8((seed >> 8) % 101),
            element: uint8((seed >> 16) % 4),
            createdAt: block.timestamp
        });
    }

    /**
     * @notice Reveal collection
     */
    function reveal(string calldata _baseURI) external onlyOwner {
        revealed = true;
        baseURI = _baseURI;
        emit Revealed(_baseURI);
    }

    /**
     * @notice Override tokenURI para reveal mechanism
     */
    function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        require(_ownerOf(tokenId) != address(0), "Token doesn't exist");

        if (!revealed) {
            return hiddenMetadataURI;
        }

        return string(abi.encodePacked(baseURI, Strings.toString(tokenId), ".json"));
    }

    // ============ Admin Functions ============

    function setPhase(Phase _phase) external onlyOwner {
        currentPhase = _phase;
    }

    function addToWhitelist(address[] calldata addresses) external onlyOwner {
        for (uint256 i = 0; i < addresses.length; i++) {
            whitelist[addresses[i]] = true;
        }
    }

    function withdraw() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }

    // ============ Required Overrides ============

    function supportsInterface(bytes4 interfaceId)
        public view override(ERC721, ERC721URIStorage, ERC721Royalty)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage, ERC721Royalty) {
        super._burn(tokenId);
    }
}
```

---

## 2. STANDARDS Y EXTENSIONES

### 2.1 ERC-1155 Multi-Token

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Supply.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

/**
 * @title GameItems
 * @notice ERC-1155 para items de juego (semi-fungibles)
 * @dev Un token ID puede tener múltiples copias (a diferencia de ERC-721)
 */
contract GameItems is ERC1155, ERC1155Supply, AccessControl {

    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    // Token types
    uint256 public constant GOLD = 0;           // Fungible currency
    uint256 public constant SWORD = 1;          // Common weapon
    uint256 public constant SHIELD = 2;         // Common armor
    uint256 public constant LEGENDARY_SWORD = 3; // Limited supply
    uint256 public constant POTION = 4;         // Consumable

    // Token metadata
    struct TokenInfo {
        string name;
        uint256 maxSupply;      // 0 = unlimited
        bool transferable;
        bool burnable;
    }
    mapping(uint256 => TokenInfo) public tokenInfo;

    // Crafting recipes
    struct Recipe {
        uint256[] inputIds;
        uint256[] inputAmounts;
        uint256 outputId;
        uint256 outputAmount;
    }
    mapping(uint256 => Recipe) public recipes;
    uint256 public recipeCount;

    event ItemCrafted(address indexed crafter, uint256 outputId, uint256 amount);
    event ItemConsumed(address indexed user, uint256 tokenId, uint256 amount);

    constructor(string memory uri) ERC1155(uri) {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);

        // Initialize token info
        tokenInfo[GOLD] = TokenInfo("Gold", 0, true, true);
        tokenInfo[SWORD] = TokenInfo("Iron Sword", 10000, true, true);
        tokenInfo[SHIELD] = TokenInfo("Iron Shield", 10000, true, true);
        tokenInfo[LEGENDARY_SWORD] = TokenInfo("Excalibur", 100, true, false);
        tokenInfo[POTION] = TokenInfo("Health Potion", 0, true, true);
    }

    /**
     * @notice Mint items (solo MINTER_ROLE)
     */
    function mint(
        address to,
        uint256 id,
        uint256 amount,
        bytes memory data
    ) external onlyRole(MINTER_ROLE) {
        TokenInfo memory info = tokenInfo[id];

        // Verificar max supply
        if (info.maxSupply > 0) {
            require(
                totalSupply(id) + amount <= info.maxSupply,
                "Exceeds max supply"
            );
        }

        _mint(to, id, amount, data);
    }

    /**
     * @notice Batch mint
     */
    function mintBatch(
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) external onlyRole(MINTER_ROLE) {
        for (uint256 i = 0; i < ids.length; i++) {
            TokenInfo memory info = tokenInfo[ids[i]];
            if (info.maxSupply > 0) {
                require(
                    totalSupply(ids[i]) + amounts[i] <= info.maxSupply,
                    "Exceeds max supply"
                );
            }
        }

        _mintBatch(to, ids, amounts, data);
    }

    /**
     * @notice Craftear items combinando otros
     */
    function craft(uint256 recipeId) external {
        Recipe storage recipe = recipes[recipeId];
        require(recipe.outputId != 0, "Recipe doesn't exist");

        // Verificar y quemar inputs
        for (uint256 i = 0; i < recipe.inputIds.length; i++) {
            require(
                balanceOf(msg.sender, recipe.inputIds[i]) >= recipe.inputAmounts[i],
                "Insufficient input items"
            );
            _burn(msg.sender, recipe.inputIds[i], recipe.inputAmounts[i]);
        }

        // Mint output
        _mint(msg.sender, recipe.outputId, recipe.outputAmount, "");

        emit ItemCrafted(msg.sender, recipe.outputId, recipe.outputAmount);
    }

    /**
     * @notice Consumir item (ej: poción)
     */
    function consume(uint256 tokenId, uint256 amount) external {
        require(tokenInfo[tokenId].burnable, "Item not consumable");
        require(balanceOf(msg.sender, tokenId) >= amount, "Insufficient balance");

        _burn(msg.sender, tokenId, amount);

        emit ItemConsumed(msg.sender, tokenId, amount);
    }

    /**
     * @notice Agregar receta de crafting
     */
    function addRecipe(
        uint256[] calldata inputIds,
        uint256[] calldata inputAmounts,
        uint256 outputId,
        uint256 outputAmount
    ) external onlyRole(DEFAULT_ADMIN_ROLE) returns (uint256) {
        require(inputIds.length == inputAmounts.length, "Length mismatch");
        require(inputIds.length > 0, "Empty recipe");

        recipeCount++;
        recipes[recipeCount] = Recipe({
            inputIds: inputIds,
            inputAmounts: inputAmounts,
            outputId: outputId,
            outputAmount: outputAmount
        });

        return recipeCount;
    }

    /**
     * @notice Override transfer para verificar transferability
     */
    function _update(
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory values
    ) internal override(ERC1155, ERC1155Supply) {
        // Si no es mint (from != 0) y no es burn (to != 0), verificar transferable
        if (from != address(0) && to != address(0)) {
            for (uint256 i = 0; i < ids.length; i++) {
                require(tokenInfo[ids[i]].transferable, "Item not transferable");
            }
        }

        super._update(from, to, ids, values);
    }

    function supportsInterface(bytes4 interfaceId)
        public view override(ERC1155, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
```

### 2.2 ERC-6551: Token Bound Accounts

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/introspection/IERC165.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/interfaces/IERC1271.sol";

/**
 * @title IERC6551Account
 * @notice Interface para Token Bound Accounts (TBA)
 */
interface IERC6551Account {
    receive() external payable;

    function token() external view returns (
        uint256 chainId,
        address tokenContract,
        uint256 tokenId
    );

    function state() external view returns (uint256);

    function isValidSigner(address signer, bytes calldata context)
        external view returns (bytes4 magicValue);
}

/**
 * @title ERC6551Account
 * @notice Cuenta controlada por un NFT - el NFT "posee" assets
 */
contract ERC6551Account is IERC165, IERC1271, IERC6551Account {

    uint256 public state;

    receive() external payable {}

    /**
     * @notice Ejecutar transacción como el NFT
     */
    function execute(
        address to,
        uint256 value,
        bytes calldata data,
        uint8 operation
    ) external payable returns (bytes memory result) {
        require(_isValidSigner(msg.sender), "Invalid signer");
        require(operation == 0, "Only call operations");

        state++;

        bool success;
        (success, result) = to.call{value: value}(data);

        if (!success) {
            assembly {
                revert(add(result, 32), mload(result))
            }
        }
    }

    /**
     * @notice Obtener info del NFT que controla esta cuenta
     */
    function token() public view returns (
        uint256 chainId,
        address tokenContract,
        uint256 tokenId
    ) {
        bytes memory footer = new bytes(0x60);

        assembly {
            extcodecopy(address(), add(footer, 0x20), 0x4d, 0x60)
        }

        return abi.decode(footer, (uint256, address, uint256));
    }

    /**
     * @notice Obtener owner del NFT (y por tanto de esta cuenta)
     */
    function owner() public view returns (address) {
        (uint256 chainId, address tokenContract, uint256 tokenId) = token();

        if (chainId != block.chainid) return address(0);

        return IERC721(tokenContract).ownerOf(tokenId);
    }

    /**
     * @notice Verificar si una dirección puede firmar por esta cuenta
     */
    function _isValidSigner(address signer) internal view returns (bool) {
        return signer == owner();
    }

    function isValidSigner(address signer, bytes calldata)
        external view returns (bytes4)
    {
        if (_isValidSigner(signer)) {
            return IERC6551Account.isValidSigner.selector;
        }
        return bytes4(0);
    }

    function isValidSignature(bytes32 hash, bytes memory signature)
        external view returns (bytes4)
    {
        // Implementar verificación de firma
        // En producción: verificar que owner firmó el hash
        return IERC1271.isValidSignature.selector;
    }

    function supportsInterface(bytes4 interfaceId) external pure returns (bool) {
        return
            interfaceId == type(IERC165).interfaceId ||
            interfaceId == type(IERC6551Account).interfaceId ||
            interfaceId == type(IERC1271).interfaceId;
    }
}

/**
 * @title ERC6551Registry
 * @notice Registry para crear Token Bound Accounts
 */
contract ERC6551Registry {

    event AccountCreated(
        address account,
        address indexed implementation,
        uint256 chainId,
        address indexed tokenContract,
        uint256 indexed tokenId,
        uint256 salt
    );

    /**
     * @notice Crear TBA para un NFT
     */
    function createAccount(
        address implementation,
        uint256 chainId,
        address tokenContract,
        uint256 tokenId,
        uint256 salt,
        bytes calldata initData
    ) external returns (address) {
        bytes memory code = _creationCode(
            implementation,
            chainId,
            tokenContract,
            tokenId,
            salt
        );

        address _account = _computeAddress(
            implementation,
            chainId,
            tokenContract,
            tokenId,
            salt
        );

        if (_account.code.length != 0) return _account;

        assembly {
            _account := create2(0, add(code, 0x20), mload(code), salt)
        }

        if (initData.length != 0) {
            (bool success, ) = _account.call(initData);
            require(success, "Init failed");
        }

        emit AccountCreated(
            _account,
            implementation,
            chainId,
            tokenContract,
            tokenId,
            salt
        );

        return _account;
    }

    /**
     * @notice Obtener dirección de TBA (determinístico)
     */
    function account(
        address implementation,
        uint256 chainId,
        address tokenContract,
        uint256 tokenId,
        uint256 salt
    ) external view returns (address) {
        return _computeAddress(implementation, chainId, tokenContract, tokenId, salt);
    }

    function _computeAddress(
        address implementation,
        uint256 chainId,
        address tokenContract,
        uint256 tokenId,
        uint256 salt
    ) internal view returns (address) {
        bytes32 bytecodeHash = keccak256(
            _creationCode(implementation, chainId, tokenContract, tokenId, salt)
        );

        return address(uint160(uint256(keccak256(abi.encodePacked(
            bytes1(0xff),
            address(this),
            salt,
            bytecodeHash
        )))));
    }

    function _creationCode(
        address implementation,
        uint256 chainId,
        address tokenContract,
        uint256 tokenId,
        uint256
    ) internal pure returns (bytes memory) {
        return abi.encodePacked(
            hex"3d60ad80600a3d3981f3363d3d373d3d3d363d73",
            implementation,
            hex"5af43d82803e903d91602b57fd5bf3",
            abi.encode(chainId, tokenContract, tokenId)
        );
    }
}
```

---

## 3. NFT MARKETPLACES

### 3.1 Marketplace Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/interfaces/IERC2981.sol";

/**
 * @title NFTMarketplace
 * @notice Marketplace con listings, offers, auctions y royalties
 */
contract NFTMarketplace is ReentrancyGuard, Ownable {

    // Listing types
    enum ListingType { FIXED_PRICE, AUCTION }

    struct Listing {
        address seller;
        address nftContract;
        uint256 tokenId;
        address paymentToken;   // address(0) = ETH
        uint256 price;          // Fixed price or starting price
        uint256 endTime;        // 0 = no expiry (fixed), auction end time
        ListingType listingType;
        bool active;
    }

    struct Auction {
        address highestBidder;
        uint256 highestBid;
        uint256 minBidIncrement;
    }

    struct Offer {
        address offerer;
        uint256 amount;
        address paymentToken;
        uint256 expiry;
    }

    // Storage
    mapping(bytes32 => Listing) public listings;
    mapping(bytes32 => Auction) public auctions;
    mapping(bytes32 => Offer[]) public offers;  // listingId => offers

    // Platform fee
    uint256 public platformFeeBps = 250; // 2.5%
    address public feeRecipient;

    // Allowed payment tokens
    mapping(address => bool) public allowedPaymentTokens;

    // Events
    event Listed(
        bytes32 indexed listingId,
        address indexed seller,
        address nftContract,
        uint256 tokenId,
        uint256 price,
        ListingType listingType
    );
    event Sale(
        bytes32 indexed listingId,
        address indexed buyer,
        uint256 price
    );
    event BidPlaced(
        bytes32 indexed listingId,
        address indexed bidder,
        uint256 amount
    );
    event OfferMade(
        bytes32 indexed listingId,
        address indexed offerer,
        uint256 amount
    );
    event ListingCancelled(bytes32 indexed listingId);

    constructor() Ownable(msg.sender) {
        feeRecipient = msg.sender;
        allowedPaymentTokens[address(0)] = true; // ETH always allowed
    }

    /**
     * @notice Crear listing de precio fijo
     */
    function listFixedPrice(
        address nftContract,
        uint256 tokenId,
        address paymentToken,
        uint256 price,
        uint256 duration
    ) external returns (bytes32 listingId) {
        require(price > 0, "Price must be > 0");
        require(
            paymentToken == address(0) || allowedPaymentTokens[paymentToken],
            "Payment token not allowed"
        );

        // Transfer NFT to marketplace
        IERC721(nftContract).transferFrom(msg.sender, address(this), tokenId);

        listingId = _getListingId(nftContract, tokenId, msg.sender);

        listings[listingId] = Listing({
            seller: msg.sender,
            nftContract: nftContract,
            tokenId: tokenId,
            paymentToken: paymentToken,
            price: price,
            endTime: duration > 0 ? block.timestamp + duration : 0,
            listingType: ListingType.FIXED_PRICE,
            active: true
        });

        emit Listed(listingId, msg.sender, nftContract, tokenId, price, ListingType.FIXED_PRICE);
    }

    /**
     * @notice Crear subasta
     */
    function listAuction(
        address nftContract,
        uint256 tokenId,
        address paymentToken,
        uint256 startingPrice,
        uint256 duration,
        uint256 minBidIncrement
    ) external returns (bytes32 listingId) {
        require(startingPrice > 0, "Starting price must be > 0");
        require(duration >= 1 hours, "Duration too short");

        IERC721(nftContract).transferFrom(msg.sender, address(this), tokenId);

        listingId = _getListingId(nftContract, tokenId, msg.sender);

        listings[listingId] = Listing({
            seller: msg.sender,
            nftContract: nftContract,
            tokenId: tokenId,
            paymentToken: paymentToken,
            price: startingPrice,
            endTime: block.timestamp + duration,
            listingType: ListingType.AUCTION,
            active: true
        });

        auctions[listingId] = Auction({
            highestBidder: address(0),
            highestBid: 0,
            minBidIncrement: minBidIncrement
        });

        emit Listed(listingId, msg.sender, nftContract, tokenId, startingPrice, ListingType.AUCTION);
    }

    /**
     * @notice Comprar a precio fijo
     */
    function buyFixedPrice(bytes32 listingId) external payable nonReentrant {
        Listing storage listing = listings[listingId];
        require(listing.active, "Listing not active");
        require(listing.listingType == ListingType.FIXED_PRICE, "Not fixed price");
        require(listing.endTime == 0 || block.timestamp <= listing.endTime, "Listing expired");

        listing.active = false;

        _processSale(
            listingId,
            listing.seller,
            msg.sender,
            listing.nftContract,
            listing.tokenId,
            listing.paymentToken,
            listing.price
        );
    }

    /**
     * @notice Hacer bid en subasta
     */
    function placeBid(bytes32 listingId, uint256 bidAmount) external payable nonReentrant {
        Listing storage listing = listings[listingId];
        Auction storage auction = auctions[listingId];

        require(listing.active, "Auction not active");
        require(listing.listingType == ListingType.AUCTION, "Not auction");
        require(block.timestamp < listing.endTime, "Auction ended");

        uint256 minBid = auction.highestBid > 0
            ? auction.highestBid + auction.minBidIncrement
            : listing.price;

        require(bidAmount >= minBid, "Bid too low");

        // Refund previous bidder
        if (auction.highestBidder != address(0)) {
            _transferPayment(
                listing.paymentToken,
                address(this),
                auction.highestBidder,
                auction.highestBid
            );
        }

        // Accept new bid
        _receivePayment(listing.paymentToken, msg.sender, bidAmount);

        auction.highestBidder = msg.sender;
        auction.highestBid = bidAmount;

        // Extend auction if bid in last 10 minutes
        if (listing.endTime - block.timestamp < 10 minutes) {
            listing.endTime += 10 minutes;
        }

        emit BidPlaced(listingId, msg.sender, bidAmount);
    }

    /**
     * @notice Finalizar subasta
     */
    function settleAuction(bytes32 listingId) external nonReentrant {
        Listing storage listing = listings[listingId];
        Auction storage auction = auctions[listingId];

        require(listing.active, "Auction not active");
        require(listing.listingType == ListingType.AUCTION, "Not auction");
        require(block.timestamp >= listing.endTime, "Auction not ended");

        listing.active = false;

        if (auction.highestBidder != address(0)) {
            // Hay ganador - procesar venta
            _processSale(
                listingId,
                listing.seller,
                auction.highestBidder,
                listing.nftContract,
                listing.tokenId,
                listing.paymentToken,
                auction.highestBid
            );
        } else {
            // Sin bids - devolver NFT al seller
            IERC721(listing.nftContract).transferFrom(
                address(this),
                listing.seller,
                listing.tokenId
            );
        }
    }

    /**
     * @notice Procesar venta con royalties
     */
    function _processSale(
        bytes32 listingId,
        address seller,
        address buyer,
        address nftContract,
        uint256 tokenId,
        address paymentToken,
        uint256 salePrice
    ) internal {
        uint256 platformFee = (salePrice * platformFeeBps) / 10000;
        uint256 royaltyAmount = 0;
        address royaltyRecipient = address(0);

        // Check for ERC2981 royalties
        if (IERC165(nftContract).supportsInterface(type(IERC2981).interfaceId)) {
            (royaltyRecipient, royaltyAmount) = IERC2981(nftContract).royaltyInfo(
                tokenId,
                salePrice
            );
        }

        uint256 sellerProceeds = salePrice - platformFee - royaltyAmount;

        // Transfer payments
        if (paymentToken == address(0)) {
            require(msg.value >= salePrice, "Insufficient ETH");

            payable(feeRecipient).transfer(platformFee);
            if (royaltyAmount > 0) {
                payable(royaltyRecipient).transfer(royaltyAmount);
            }
            payable(seller).transfer(sellerProceeds);

            // Refund excess
            if (msg.value > salePrice) {
                payable(buyer).transfer(msg.value - salePrice);
            }
        } else {
            IERC20(paymentToken).transferFrom(buyer, feeRecipient, platformFee);
            if (royaltyAmount > 0) {
                IERC20(paymentToken).transferFrom(buyer, royaltyRecipient, royaltyAmount);
            }
            IERC20(paymentToken).transferFrom(buyer, seller, sellerProceeds);
        }

        // Transfer NFT
        IERC721(nftContract).transferFrom(address(this), buyer, tokenId);

        emit Sale(listingId, buyer, salePrice);
    }

    function _receivePayment(address token, address from, uint256 amount) internal {
        if (token == address(0)) {
            require(msg.value >= amount, "Insufficient ETH");
        } else {
            IERC20(token).transferFrom(from, address(this), amount);
        }
    }

    function _transferPayment(address token, address from, address to, uint256 amount) internal {
        if (token == address(0)) {
            payable(to).transfer(amount);
        } else {
            if (from == address(this)) {
                IERC20(token).transfer(to, amount);
            } else {
                IERC20(token).transferFrom(from, to, amount);
            }
        }
    }

    function _getListingId(
        address nftContract,
        uint256 tokenId,
        address seller
    ) internal view returns (bytes32) {
        return keccak256(abi.encodePacked(
            nftContract,
            tokenId,
            seller,
            block.timestamp
        ));
    }

    // Admin functions
    function setFee(uint256 newFeeBps) external onlyOwner {
        require(newFeeBps <= 1000, "Fee too high"); // Max 10%
        platformFeeBps = newFeeBps;
    }

    function setAllowedPaymentToken(address token, bool allowed) external onlyOwner {
        allowedPaymentTokens[token] = allowed;
    }
}
```

---

## 4. GAMEFI ECONOMICS

### 4.1 Game Economy System

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

/**
 * @title GameEconomy
 * @notice Sistema económico completo para juego P2E
 */
contract GameEconomy is AccessControl {

    bytes32 public constant GAME_SERVER = keccak256("GAME_SERVER");

    // Tokens del ecosistema
    IERC20 public softCurrency;    // Earned in-game, inflationary
    IERC20 public hardCurrency;    // Premium, limited
    IERC20 public governanceToken; // Staking, voting

    // NFT contracts
    address public heroesNFT;
    address public itemsNFT;

    // Player data
    struct Player {
        uint256 level;
        uint256 experience;
        uint256 energy;
        uint256 lastEnergyRefill;
        uint256 dailyEarnings;
        uint256 lastDailyReset;
    }
    mapping(address => Player) public players;

    // Economy parameters (ajustables por governance)
    struct EconomyParams {
        uint256 energyPerAction;
        uint256 maxEnergy;
        uint256 energyRefillRate;     // Per hour
        uint256 baseRewardPerAction;
        uint256 dailyEarningCap;
        uint256 levelMultiplierBps;   // Extra rewards per level (100 = 1%)
    }
    EconomyParams public params;

    // Sink mechanisms (quemar tokens)
    mapping(string => uint256) public sinkCosts; // action => cost

    // Events
    event ActionCompleted(address indexed player, string action, uint256 reward);
    event SoftCurrencyBurned(address indexed player, string sink, uint256 amount);
    event LevelUp(address indexed player, uint256 newLevel);

    constructor(
        address _softCurrency,
        address _hardCurrency,
        address _governanceToken
    ) {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(GAME_SERVER, msg.sender);

        softCurrency = IERC20(_softCurrency);
        hardCurrency = IERC20(_hardCurrency);
        governanceToken = IERC20(_governanceToken);

        // Default params
        params = EconomyParams({
            energyPerAction: 10,
            maxEnergy: 100,
            energyRefillRate: 10,       // 10 per hour
            baseRewardPerAction: 100e18, // 100 tokens
            dailyEarningCap: 10000e18,   // 10,000 tokens max per day
            levelMultiplierBps: 100      // 1% extra per level
        });

        // Sink costs
        sinkCosts["upgrade_hero"] = 1000e18;
        sinkCosts["craft_item"] = 500e18;
        sinkCosts["enter_dungeon"] = 200e18;
        sinkCosts["breed_hero"] = 5000e18;
    }

    /**
     * @notice Completar acción de juego y recibir recompensa
     */
    function completeAction(
        address player,
        string calldata actionType,
        uint256 difficultyMultiplier
    ) external onlyRole(GAME_SERVER) {
        Player storage p = players[player];
        _initPlayerIfNeeded(player);
        _resetDailyIfNeeded(player);
        _refillEnergy(player);

        require(p.energy >= params.energyPerAction, "Not enough energy");

        // Consume energy
        p.energy -= params.energyPerAction;

        // Calculate reward
        uint256 reward = _calculateReward(p.level, difficultyMultiplier);

        // Apply daily cap
        uint256 remainingCap = params.dailyEarningCap - p.dailyEarnings;
        if (reward > remainingCap) {
            reward = remainingCap;
        }

        if (reward > 0) {
            p.dailyEarnings += reward;
            // Mint soft currency (controlled emission)
            IMintable(address(softCurrency)).mint(player, reward);
        }

        // Add experience
        uint256 expGained = reward / 10; // 10% of reward as exp
        p.experience += expGained;

        // Check level up
        _checkLevelUp(player);

        emit ActionCompleted(player, actionType, reward);
    }

    /**
     * @notice Quemar soft currency (sink)
     */
    function burnForSink(
        address player,
        string calldata sinkType
    ) external onlyRole(GAME_SERVER) {
        uint256 cost = sinkCosts[sinkType];
        require(cost > 0, "Unknown sink");

        softCurrency.transferFrom(player, address(0xdead), cost);

        emit SoftCurrencyBurned(player, sinkType, cost);
    }

    /**
     * @notice Calcular recompensa
     */
    function _calculateReward(
        uint256 level,
        uint256 difficultyMultiplier
    ) internal view returns (uint256) {
        uint256 baseReward = params.baseRewardPerAction;

        // Level bonus
        uint256 levelBonus = (baseReward * level * params.levelMultiplierBps) / 10000;

        // Difficulty multiplier (100 = 1x, 200 = 2x)
        uint256 totalReward = (baseReward + levelBonus) * difficultyMultiplier / 100;

        return totalReward;
    }

    /**
     * @notice Refill energy basado en tiempo
     */
    function _refillEnergy(address player) internal {
        Player storage p = players[player];

        uint256 hoursPassed = (block.timestamp - p.lastEnergyRefill) / 1 hours;

        if (hoursPassed > 0) {
            uint256 refill = hoursPassed * params.energyRefillRate;
            p.energy = p.energy + refill > params.maxEnergy
                ? params.maxEnergy
                : p.energy + refill;
            p.lastEnergyRefill = block.timestamp;
        }
    }

    /**
     * @notice Check y procesar level up
     */
    function _checkLevelUp(address player) internal {
        Player storage p = players[player];

        // Exp required = level^2 * 1000
        uint256 expRequired = (p.level + 1) ** 2 * 1000;

        while (p.experience >= expRequired) {
            p.experience -= expRequired;
            p.level++;
            expRequired = (p.level + 1) ** 2 * 1000;

            emit LevelUp(player, p.level);
        }
    }

    function _initPlayerIfNeeded(address player) internal {
        if (players[player].lastEnergyRefill == 0) {
            players[player] = Player({
                level: 1,
                experience: 0,
                energy: params.maxEnergy,
                lastEnergyRefill: block.timestamp,
                dailyEarnings: 0,
                lastDailyReset: block.timestamp
            });
        }
    }

    function _resetDailyIfNeeded(address player) internal {
        Player storage p = players[player];
        if (block.timestamp - p.lastDailyReset >= 1 days) {
            p.dailyEarnings = 0;
            p.lastDailyReset = block.timestamp;
        }
    }

    /**
     * @notice Obtener estado actual del jugador
     */
    function getPlayerStatus(address player) external view returns (
        uint256 level,
        uint256 experience,
        uint256 currentEnergy,
        uint256 dailyEarningsRemaining
    ) {
        Player storage p = players[player];

        // Calculate current energy with refill
        uint256 hoursPassed = (block.timestamp - p.lastEnergyRefill) / 1 hours;
        uint256 refill = hoursPassed * params.energyRefillRate;
        currentEnergy = p.energy + refill > params.maxEnergy
            ? params.maxEnergy
            : p.energy + refill;

        // Calculate remaining daily earnings
        uint256 dailyEarnings = p.dailyEarnings;
        if (block.timestamp - p.lastDailyReset >= 1 days) {
            dailyEarnings = 0;
        }

        return (
            p.level,
            p.experience,
            currentEnergy,
            params.dailyEarningCap - dailyEarnings
        );
    }

    // Admin functions
    function updateParams(EconomyParams calldata newParams) external onlyRole(DEFAULT_ADMIN_ROLE) {
        params = newParams;
    }

    function setSinkCost(string calldata sink, uint256 cost) external onlyRole(DEFAULT_ADMIN_ROLE) {
        sinkCosts[sink] = cost;
    }
}

interface IMintable {
    function mint(address to, uint256 amount) external;
}

interface IERC20 {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}
```

### 4.2 Play-to-Earn Balance Analysis

```python
"""
CIPHER: GameFi Economy Analyzer
Análisis y balance de economías de juegos P2E
"""

from dataclasses import dataclass
from typing import Dict, List
from enum import Enum

class TokenFlow(Enum):
    FAUCET = "faucet"    # Token enters economy
    SINK = "sink"        # Token exits economy
    TRANSFER = "transfer" # Token moves between players

@dataclass
class EconomyAction:
    name: str
    flow_type: TokenFlow
    token: str
    amount: float
    frequency_per_day_per_user: float

@dataclass
class EconomyMetrics:
    daily_emission: float
    daily_burn: float
    net_inflation: float
    player_count: int
    avg_daily_earnings_per_player: float

class GameEconomyAnalyzer:
    """Analizar sostenibilidad de economía GameFi"""

    def __init__(self, token_name: str, initial_supply: float):
        self.token = token_name
        self.initial_supply = initial_supply
        self.actions: List[EconomyAction] = []
        self.current_player_count = 0

    def add_action(self, action: EconomyAction):
        self.actions.append(action)

    def calculate_daily_metrics(self, player_count: int) -> EconomyMetrics:
        """Calcular métricas diarias de la economía"""
        self.current_player_count = player_count

        total_emission = 0
        total_burn = 0

        for action in self.actions:
            daily_total = action.amount * action.frequency_per_day_per_user * player_count

            if action.flow_type == TokenFlow.FAUCET:
                total_emission += daily_total
            elif action.flow_type == TokenFlow.SINK:
                total_burn += daily_total

        net_inflation = total_emission - total_burn

        return EconomyMetrics(
            daily_emission=total_emission,
            daily_burn=total_burn,
            net_inflation=net_inflation,
            player_count=player_count,
            avg_daily_earnings_per_player=net_inflation / player_count if player_count > 0 else 0
        )

    def simulate_economy(
        self,
        days: int,
        player_growth_rate: float,  # Daily growth rate
        initial_players: int,
        token_price: float
    ) -> List[Dict]:
        """Simular economía durante varios días"""
        results = []
        circulating_supply = self.initial_supply
        players = initial_players

        for day in range(1, days + 1):
            metrics = self.calculate_daily_metrics(players)

            # Update supply
            circulating_supply += metrics.net_inflation

            # Calculate market cap and price impact
            # Simplified: more supply = lower price
            inflation_rate = metrics.net_inflation / circulating_supply
            price_impact = 1 - inflation_rate  # Simplified model
            new_price = token_price * price_impact

            results.append({
                "day": day,
                "players": players,
                "daily_emission": metrics.daily_emission,
                "daily_burn": metrics.daily_burn,
                "net_inflation": metrics.net_inflation,
                "circulating_supply": circulating_supply,
                "estimated_price": new_price,
                "market_cap": circulating_supply * new_price,
                "avg_earnings_usd": metrics.avg_daily_earnings_per_player * new_price
            })

            # Grow players
            players = int(players * (1 + player_growth_rate))
            token_price = new_price

        return results

    def calculate_sustainability_score(
        self,
        player_count: int,
        target_earnings_usd: float,
        token_price: float
    ) -> Dict:
        """Evaluar sostenibilidad de la economía"""
        metrics = self.calculate_daily_metrics(player_count)

        # Earnings in USD
        earnings_usd = metrics.avg_daily_earnings_per_player * token_price

        # Inflation rate
        daily_inflation_rate = metrics.net_inflation / self.initial_supply * 100

        # Sink ratio
        sink_ratio = metrics.daily_burn / metrics.daily_emission if metrics.daily_emission > 0 else 0

        # Score calculation
        score = 0

        # Sink ratio score (higher is better)
        if sink_ratio >= 0.8:
            score += 40
        elif sink_ratio >= 0.6:
            score += 30
        elif sink_ratio >= 0.4:
            score += 20
        elif sink_ratio >= 0.2:
            score += 10

        # Inflation score (lower is better)
        if daily_inflation_rate < 0.1:
            score += 30
        elif daily_inflation_rate < 0.5:
            score += 20
        elif daily_inflation_rate < 1:
            score += 10

        # Earnings sustainability
        if 0.5 * target_earnings_usd <= earnings_usd <= 2 * target_earnings_usd:
            score += 30
        elif earnings_usd > 0:
            score += 15

        return {
            "sustainability_score": score,
            "rating": self._score_to_rating(score),
            "metrics": {
                "daily_earnings_usd": earnings_usd,
                "daily_inflation_rate": daily_inflation_rate,
                "sink_ratio": sink_ratio,
                "time_to_double_supply_days": 100 / daily_inflation_rate if daily_inflation_rate > 0 else float('inf')
            },
            "recommendations": self._get_recommendations(sink_ratio, daily_inflation_rate, earnings_usd, target_earnings_usd)
        }

    def _score_to_rating(self, score: int) -> str:
        if score >= 80:
            return "SUSTAINABLE"
        elif score >= 60:
            return "MODERATE"
        elif score >= 40:
            return "AT_RISK"
        else:
            return "UNSUSTAINABLE"

    def _get_recommendations(
        self,
        sink_ratio: float,
        inflation: float,
        current_earnings: float,
        target_earnings: float
    ) -> List[str]:
        recs = []

        if sink_ratio < 0.5:
            recs.append("Add more token sinks (crafting, upgrades, entry fees)")

        if inflation > 1:
            recs.append("Reduce emission rates or add daily caps")

        if current_earnings > target_earnings * 2:
            recs.append("Earnings too high - will attract bots and drain economy")

        if current_earnings < target_earnings * 0.3:
            recs.append("Earnings too low - players may leave")

        if not recs:
            recs.append("Economy is well-balanced")

        return recs


# Ejemplo de uso
if __name__ == "__main__":
    analyzer = GameEconomyAnalyzer("GAME_TOKEN", 1_000_000_000)

    # Definir acciones
    # Faucets (entradas de tokens)
    analyzer.add_action(EconomyAction(
        name="quest_completion",
        flow_type=TokenFlow.FAUCET,
        token="GAME_TOKEN",
        amount=100,
        frequency_per_day_per_user=10
    ))

    analyzer.add_action(EconomyAction(
        name="daily_bonus",
        flow_type=TokenFlow.FAUCET,
        token="GAME_TOKEN",
        amount=500,
        frequency_per_day_per_user=1
    ))

    # Sinks (salidas de tokens)
    analyzer.add_action(EconomyAction(
        name="hero_upgrade",
        flow_type=TokenFlow.SINK,
        token="GAME_TOKEN",
        amount=200,
        frequency_per_day_per_user=3
    ))

    analyzer.add_action(EconomyAction(
        name="item_craft",
        flow_type=TokenFlow.SINK,
        token="GAME_TOKEN",
        amount=150,
        frequency_per_day_per_user=5
    ))

    # Analizar
    sustainability = analyzer.calculate_sustainability_score(
        player_count=10000,
        target_earnings_usd=5.0,
        token_price=0.01
    )

    print(f"Sustainability: {sustainability['rating']}")
    print(f"Score: {sustainability['sustainability_score']}/100")
    print(f"Recommendations: {sustainability['recommendations']}")

    # Simular 30 días
    simulation = analyzer.simulate_economy(
        days=30,
        player_growth_rate=0.02,  # 2% daily growth
        initial_players=10000,
        token_price=0.01
    )

    print(f"\n30-day simulation:")
    print(f"Final players: {simulation[-1]['players']}")
    print(f"Final price: ${simulation[-1]['estimated_price']:.4f}")
    print(f"Supply increase: {(simulation[-1]['circulating_supply'] / 1_000_000_000 - 1) * 100:.1f}%")
```

---

## 5. VIRTUAL WORLDS & METAVERSE

### 5.1 Land NFT System

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title MetaverseLand
 * @notice Sistema de terrenos virtuales con coordenadas
 */
contract MetaverseLand is ERC721, Ownable {

    struct Coordinates {
        int128 x;
        int128 y;
    }

    struct LandData {
        Coordinates coords;
        uint8 landType;      // 0=regular, 1=estate, 2=district
        uint8 tier;          // 1-5 (proximity to center)
        string contentURI;   // IPFS hash of land content
        address tenant;      // Current renter
        uint256 rentExpiry;
    }

    // Coordinate to tokenId mapping
    mapping(int128 => mapping(int128 => uint256)) public coordToTokenId;

    // TokenId to land data
    mapping(uint256 => LandData) public lands;

    // Pricing
    mapping(uint8 => uint256) public tierPrices; // tier => price

    uint256 private _tokenIdCounter;

    // World boundaries
    int128 public constant WORLD_SIZE = 500; // -500 to 500

    event LandMinted(uint256 indexed tokenId, int128 x, int128 y, address owner);
    event LandContentUpdated(uint256 indexed tokenId, string contentURI);
    event LandRented(uint256 indexed tokenId, address tenant, uint256 expiry);

    constructor() ERC721("Metaverse Land", "LAND") Ownable(msg.sender) {
        // Set tier prices (in wei)
        tierPrices[1] = 5 ether;  // Center (most valuable)
        tierPrices[2] = 2 ether;
        tierPrices[3] = 1 ether;
        tierPrices[4] = 0.5 ether;
        tierPrices[5] = 0.2 ether; // Edge
    }

    /**
     * @notice Mint land at specific coordinates
     */
    function mintLand(int128 x, int128 y) external payable returns (uint256) {
        require(x >= -WORLD_SIZE && x <= WORLD_SIZE, "X out of bounds");
        require(y >= -WORLD_SIZE && y <= WORLD_SIZE, "Y out of bounds");
        require(coordToTokenId[x][y] == 0, "Land already minted");

        uint8 tier = _calculateTier(x, y);
        require(msg.value >= tierPrices[tier], "Insufficient payment");

        _tokenIdCounter++;
        uint256 tokenId = _tokenIdCounter;

        coordToTokenId[x][y] = tokenId;

        lands[tokenId] = LandData({
            coords: Coordinates(x, y),
            landType: 0,
            tier: tier,
            contentURI: "",
            tenant: address(0),
            rentExpiry: 0
        });

        _safeMint(msg.sender, tokenId);

        emit LandMinted(tokenId, x, y, msg.sender);

        return tokenId;
    }

    /**
     * @notice Batch mint adjacent lands (estate)
     */
    function mintEstate(
        int128 startX,
        int128 startY,
        uint8 width,
        uint8 height
    ) external payable returns (uint256[] memory tokenIds) {
        require(width > 1 && height > 1, "Estate must be > 1x1");
        require(width <= 10 && height <= 10, "Estate too large");

        uint256 totalCost = 0;
        tokenIds = new uint256[](width * height);
        uint256 idx = 0;

        // First pass: verify availability and calculate cost
        for (int128 dx = 0; dx < int128(uint128(width)); dx++) {
            for (int128 dy = 0; dy < int128(uint128(height)); dy++) {
                int128 x = startX + dx;
                int128 y = startY + dy;

                require(x >= -WORLD_SIZE && x <= WORLD_SIZE, "X out of bounds");
                require(y >= -WORLD_SIZE && y <= WORLD_SIZE, "Y out of bounds");
                require(coordToTokenId[x][y] == 0, "Land occupied");

                uint8 tier = _calculateTier(x, y);
                totalCost += tierPrices[tier];
            }
        }

        // 10% discount for estates
        totalCost = (totalCost * 90) / 100;
        require(msg.value >= totalCost, "Insufficient payment");

        // Second pass: mint
        for (int128 dx = 0; dx < int128(uint128(width)); dx++) {
            for (int128 dy = 0; dy < int128(uint128(height)); dy++) {
                int128 x = startX + dx;
                int128 y = startY + dy;

                _tokenIdCounter++;
                uint256 tokenId = _tokenIdCounter;

                coordToTokenId[x][y] = tokenId;

                lands[tokenId] = LandData({
                    coords: Coordinates(x, y),
                    landType: 1, // Estate
                    tier: _calculateTier(x, y),
                    contentURI: "",
                    tenant: address(0),
                    rentExpiry: 0
                });

                _safeMint(msg.sender, tokenId);
                tokenIds[idx++] = tokenId;

                emit LandMinted(tokenId, x, y, msg.sender);
            }
        }

        return tokenIds;
    }

    /**
     * @notice Update land content (deploy building/content)
     */
    function updateContent(uint256 tokenId, string calldata contentURI) external {
        require(
            ownerOf(tokenId) == msg.sender ||
            lands[tokenId].tenant == msg.sender,
            "Not owner or tenant"
        );

        if (lands[tokenId].tenant == msg.sender) {
            require(block.timestamp < lands[tokenId].rentExpiry, "Rent expired");
        }

        lands[tokenId].contentURI = contentURI;

        emit LandContentUpdated(tokenId, contentURI);
    }

    /**
     * @notice Rent land to another user
     */
    function rentLand(
        uint256 tokenId,
        address tenant,
        uint256 duration
    ) external payable {
        require(ownerOf(tokenId) == msg.sender, "Not owner");
        require(tenant != address(0), "Invalid tenant");
        require(duration > 0 && duration <= 365 days, "Invalid duration");

        lands[tokenId].tenant = tenant;
        lands[tokenId].rentExpiry = block.timestamp + duration;

        emit LandRented(tokenId, tenant, lands[tokenId].rentExpiry);
    }

    /**
     * @notice Calculate tier based on distance from center
     */
    function _calculateTier(int128 x, int128 y) internal pure returns (uint8) {
        // Manhattan distance from center
        uint256 distance = uint256(uint128(x >= 0 ? x : -x)) +
                          uint256(uint128(y >= 0 ? y : -y));

        if (distance <= 50) return 1;
        if (distance <= 150) return 2;
        if (distance <= 300) return 3;
        if (distance <= 450) return 4;
        return 5;
    }

    /**
     * @notice Get adjacent lands
     */
    function getAdjacentLands(int128 x, int128 y) external view returns (uint256[4] memory) {
        return [
            coordToTokenId[x][y + 1],  // North
            coordToTokenId[x + 1][y],  // East
            coordToTokenId[x][y - 1],  // South
            coordToTokenId[x - 1][y]   // West
        ];
    }

    /**
     * @notice Check if coordinate is available
     */
    function isAvailable(int128 x, int128 y) external view returns (bool) {
        return coordToTokenId[x][y] == 0 &&
               x >= -WORLD_SIZE && x <= WORLD_SIZE &&
               y >= -WORLD_SIZE && y <= WORLD_SIZE;
    }

    function withdraw() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}
```

---

## 6. NFT FINANCE (NFTFI)

### 6.1 NFT Lending Protocol

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title NFTLending
 * @notice Protocolo de préstamos usando NFTs como colateral
 */
contract NFTLending is ReentrancyGuard {

    struct Loan {
        address borrower;
        address lender;
        address nftContract;
        uint256 tokenId;
        address loanToken;
        uint256 principal;
        uint256 interestRate;  // Annual rate in bps (1000 = 10%)
        uint256 duration;
        uint256 startTime;
        uint256 repaymentAmount;
        bool active;
        bool repaid;
        bool defaulted;
    }

    struct LoanOffer {
        address lender;
        address nftContract;
        uint256 tokenId;       // 0 = any token from collection
        address loanToken;
        uint256 principal;
        uint256 interestRate;
        uint256 duration;
        uint256 expiry;
        bool active;
    }

    mapping(uint256 => Loan) public loans;
    mapping(uint256 => LoanOffer) public offers;

    uint256 public loanCount;
    uint256 public offerCount;

    // Collection floor prices (simplified - in production use oracle)
    mapping(address => uint256) public collectionFloors;

    // Protocol fee
    uint256 public protocolFeeBps = 100; // 1%
    address public feeRecipient;

    event LoanOfferCreated(uint256 indexed offerId, address lender, address nftContract, uint256 principal);
    event LoanStarted(uint256 indexed loanId, address borrower, address lender, uint256 principal);
    event LoanRepaid(uint256 indexed loanId, uint256 repaymentAmount);
    event LoanDefaulted(uint256 indexed loanId, address nftContract, uint256 tokenId);

    constructor(address _feeRecipient) {
        feeRecipient = _feeRecipient;
    }

    /**
     * @notice Crear oferta de préstamo
     */
    function createOffer(
        address nftContract,
        uint256 tokenId,
        address loanToken,
        uint256 principal,
        uint256 interestRate,
        uint256 duration,
        uint256 offerDuration
    ) external returns (uint256 offerId) {
        require(principal > 0, "Invalid principal");
        require(duration > 0 && duration <= 365 days, "Invalid duration");

        // Transfer loan token to contract
        IERC20(loanToken).transferFrom(msg.sender, address(this), principal);

        offerId = ++offerCount;

        offers[offerId] = LoanOffer({
            lender: msg.sender,
            nftContract: nftContract,
            tokenId: tokenId,
            loanToken: loanToken,
            principal: principal,
            interestRate: interestRate,
            duration: duration,
            expiry: block.timestamp + offerDuration,
            active: true
        });

        emit LoanOfferCreated(offerId, msg.sender, nftContract, principal);
    }

    /**
     * @notice Aceptar oferta y recibir préstamo
     */
    function acceptOffer(
        uint256 offerId,
        uint256 tokenId
    ) external nonReentrant returns (uint256 loanId) {
        LoanOffer storage offer = offers[offerId];

        require(offer.active, "Offer not active");
        require(block.timestamp < offer.expiry, "Offer expired");

        // If offer is for specific token, verify
        if (offer.tokenId != 0) {
            require(tokenId == offer.tokenId, "Wrong token");
        }

        // Verify ownership and transfer NFT to contract
        IERC721(offer.nftContract).transferFrom(msg.sender, address(this), tokenId);

        // Calculate repayment amount
        uint256 interest = (offer.principal * offer.interestRate * offer.duration) /
                          (365 days * 10000);
        uint256 repaymentAmount = offer.principal + interest;

        // Create loan
        loanId = ++loanCount;

        loans[loanId] = Loan({
            borrower: msg.sender,
            lender: offer.lender,
            nftContract: offer.nftContract,
            tokenId: tokenId,
            loanToken: offer.loanToken,
            principal: offer.principal,
            interestRate: offer.interestRate,
            duration: offer.duration,
            startTime: block.timestamp,
            repaymentAmount: repaymentAmount,
            active: true,
            repaid: false,
            defaulted: false
        });

        // Mark offer as used
        offer.active = false;

        // Transfer principal to borrower
        IERC20(offer.loanToken).transfer(msg.sender, offer.principal);

        emit LoanStarted(loanId, msg.sender, offer.lender, offer.principal);
    }

    /**
     * @notice Repagar préstamo y recuperar NFT
     */
    function repayLoan(uint256 loanId) external nonReentrant {
        Loan storage loan = loans[loanId];

        require(loan.active, "Loan not active");
        require(!loan.defaulted, "Loan defaulted");
        require(block.timestamp <= loan.startTime + loan.duration, "Loan expired");

        loan.active = false;
        loan.repaid = true;

        // Calculate fee
        uint256 interest = loan.repaymentAmount - loan.principal;
        uint256 fee = (interest * protocolFeeBps) / 10000;

        // Transfer repayment
        IERC20(loan.loanToken).transferFrom(
            msg.sender,
            loan.lender,
            loan.repaymentAmount - fee
        );

        if (fee > 0) {
            IERC20(loan.loanToken).transferFrom(msg.sender, feeRecipient, fee);
        }

        // Return NFT to borrower
        IERC721(loan.nftContract).transferFrom(address(this), loan.borrower, loan.tokenId);

        emit LoanRepaid(loanId, loan.repaymentAmount);
    }

    /**
     * @notice Liquidar préstamo vencido
     */
    function liquidateLoan(uint256 loanId) external nonReentrant {
        Loan storage loan = loans[loanId];

        require(loan.active, "Loan not active");
        require(!loan.repaid, "Loan already repaid");
        require(
            block.timestamp > loan.startTime + loan.duration,
            "Loan not expired"
        );

        loan.active = false;
        loan.defaulted = true;

        // Transfer NFT to lender
        IERC721(loan.nftContract).transferFrom(address(this), loan.lender, loan.tokenId);

        emit LoanDefaulted(loanId, loan.nftContract, loan.tokenId);
    }

    /**
     * @notice Calcular LTV de un préstamo
     */
    function calculateLTV(uint256 loanId) external view returns (uint256 ltvBps) {
        Loan storage loan = loans[loanId];
        uint256 floor = collectionFloors[loan.nftContract];

        if (floor == 0) return 10000; // 100% if no floor

        return (loan.principal * 10000) / floor;
    }

    /**
     * @notice Set collection floor (admin/oracle)
     */
    function setCollectionFloor(address collection, uint256 floor) external {
        // In production: only oracle can call this
        collectionFloors[collection] = floor;
    }
}
```

---

## 7. ANÁLISIS Y VALUACIÓN

### 7.1 NFT Valuation System

```python
"""
CIPHER: NFT Valuation & Analytics
Sistema de valuación y análisis de NFTs
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
import statistics

@dataclass
class NFTSale:
    token_id: int
    price_eth: float
    timestamp: datetime
    marketplace: str
    buyer: str
    seller: str
    traits: Dict[str, str]

@dataclass
class CollectionStats:
    floor_price: float
    avg_price_24h: float
    volume_24h: float
    sales_count_24h: int
    listed_count: int
    total_supply: int
    unique_holders: int

class NFTValuator:
    """Sistema de valuación de NFTs"""

    def __init__(self, collection_address: str):
        self.collection = collection_address
        self.sales_history: List[NFTSale] = []
        self.trait_rarity: Dict[str, Dict[str, float]] = {}
        self.collection_stats: Optional[CollectionStats] = None

    def add_sale(self, sale: NFTSale):
        self.sales_history.append(sale)

    def set_trait_rarity(self, trait_type: str, trait_value: str, rarity_pct: float):
        """Set rarity percentage for a trait"""
        if trait_type not in self.trait_rarity:
            self.trait_rarity[trait_type] = {}
        self.trait_rarity[trait_type][trait_value] = rarity_pct

    def calculate_rarity_score(self, traits: Dict[str, str]) -> float:
        """Calculate rarity score for an NFT based on traits"""
        if not self.trait_rarity:
            return 0

        scores = []
        for trait_type, trait_value in traits.items():
            if trait_type in self.trait_rarity:
                rarity_pct = self.trait_rarity[trait_type].get(trait_value, 50)
                # Lower percentage = rarer = higher score
                trait_score = 100 / max(rarity_pct, 0.1)
                scores.append(trait_score)

        return sum(scores) if scores else 0

    def estimate_value(
        self,
        token_id: int,
        traits: Dict[str, str]
    ) -> Dict:
        """Estimate value of an NFT using multiple methods"""
        if not self.collection_stats:
            return {"error": "No collection stats"}

        estimates = {}

        # Method 1: Floor price
        estimates["floor_based"] = self.collection_stats.floor_price

        # Method 2: Trait-based premium
        rarity_score = self.calculate_rarity_score(traits)
        rarity_multiplier = 1 + (rarity_score / 100)  # Simplified
        estimates["trait_based"] = self.collection_stats.floor_price * rarity_multiplier

        # Method 3: Comparable sales
        comparable_sales = self._find_comparable_sales(traits)
        if comparable_sales:
            estimates["comparable_sales"] = statistics.median(
                [s.price_eth for s in comparable_sales]
            )

        # Method 4: Historical sales of this token
        token_sales = [s for s in self.sales_history if s.token_id == token_id]
        if token_sales:
            last_sale = max(token_sales, key=lambda s: s.timestamp)
            # Apply market adjustment
            market_change = self._calculate_market_change(last_sale.timestamp)
            estimates["last_sale_adjusted"] = last_sale.price_eth * (1 + market_change)

        # Weighted average
        weights = {
            "floor_based": 0.2,
            "trait_based": 0.3,
            "comparable_sales": 0.3,
            "last_sale_adjusted": 0.2
        }

        total_weight = sum(weights[k] for k in estimates.keys() if k in weights)
        weighted_estimate = sum(
            estimates[k] * weights.get(k, 0) / total_weight
            for k in estimates.keys()
            if k in weights
        )

        return {
            "estimated_value_eth": weighted_estimate,
            "breakdown": estimates,
            "rarity_score": rarity_score,
            "confidence": self._calculate_confidence(len(estimates))
        }

    def _find_comparable_sales(
        self,
        traits: Dict[str, str],
        max_age_days: int = 30
    ) -> List[NFTSale]:
        """Find sales with similar traits"""
        cutoff = datetime.now().timestamp() - (max_age_days * 86400)

        comparable = []
        for sale in self.sales_history:
            if sale.timestamp.timestamp() < cutoff:
                continue

            # Count matching traits
            matches = sum(
                1 for t, v in traits.items()
                if sale.traits.get(t) == v
            )

            # Consider comparable if >50% traits match
            if len(traits) > 0 and matches / len(traits) >= 0.5:
                comparable.append(sale)

        return comparable[-10:]  # Last 10 comparable

    def _calculate_market_change(self, from_date: datetime) -> float:
        """Calculate market change since a date"""
        if not self.collection_stats:
            return 0

        # Simplified: compare floor prices
        # In production: use historical floor data
        return 0  # Placeholder

    def _calculate_confidence(self, data_points: int) -> str:
        """Calculate confidence level based on data"""
        if data_points >= 4:
            return "HIGH"
        elif data_points >= 2:
            return "MEDIUM"
        else:
            return "LOW"

    def analyze_collection_health(self) -> Dict:
        """Analyze overall collection health"""
        if not self.collection_stats:
            return {"error": "No stats"}

        stats = self.collection_stats

        # Calculate metrics
        holder_concentration = stats.unique_holders / stats.total_supply
        listing_ratio = stats.listed_count / stats.total_supply
        velocity = stats.volume_24h / (stats.floor_price * stats.total_supply)

        health_score = 0

        # Holder distribution (higher = healthier)
        if holder_concentration > 0.5:
            health_score += 30
        elif holder_concentration > 0.3:
            health_score += 20
        elif holder_concentration > 0.1:
            health_score += 10

        # Listing ratio (lower = healthier, means less sell pressure)
        if listing_ratio < 0.1:
            health_score += 30
        elif listing_ratio < 0.2:
            health_score += 20
        elif listing_ratio < 0.3:
            health_score += 10

        # Velocity (moderate is best)
        if 0.01 <= velocity <= 0.05:
            health_score += 40
        elif 0.005 <= velocity <= 0.1:
            health_score += 25
        elif velocity > 0:
            health_score += 10

        return {
            "health_score": health_score,
            "rating": "HEALTHY" if health_score >= 70 else "MODERATE" if health_score >= 40 else "AT_RISK",
            "metrics": {
                "holder_concentration": holder_concentration,
                "listing_ratio": listing_ratio,
                "daily_velocity": velocity,
                "floor_price": stats.floor_price,
                "volume_24h": stats.volume_24h
            },
            "risks": self._identify_risks(holder_concentration, listing_ratio, velocity)
        }

    def _identify_risks(
        self,
        concentration: float,
        listing_ratio: float,
        velocity: float
    ) -> List[str]:
        """Identify potential risks"""
        risks = []

        if concentration < 0.2:
            risks.append("High holder concentration - whale risk")

        if listing_ratio > 0.3:
            risks.append("High listing ratio - potential sell pressure")

        if velocity > 0.1:
            risks.append("Very high velocity - potential wash trading")

        if velocity < 0.001:
            risks.append("Very low velocity - liquidity concerns")

        return risks


# Ejemplo de uso
if __name__ == "__main__":
    valuator = NFTValuator("0x1234...")

    # Set up collection stats
    valuator.collection_stats = CollectionStats(
        floor_price=1.5,
        avg_price_24h=2.1,
        volume_24h=150,
        sales_count_24h=75,
        listed_count=500,
        total_supply=10000,
        unique_holders=4200
    )

    # Set up trait rarity
    valuator.set_trait_rarity("Background", "Gold", 2.5)  # 2.5% have gold
    valuator.set_trait_rarity("Background", "Blue", 25.0)  # 25% have blue
    valuator.set_trait_rarity("Eyes", "Laser", 1.0)       # 1% have laser

    # Estimate value
    traits = {
        "Background": "Gold",
        "Eyes": "Laser",
        "Clothing": "Hoodie"
    }

    estimate = valuator.estimate_value(1234, traits)
    print(f"Estimated value: {estimate['estimated_value_eth']:.2f} ETH")
    print(f"Rarity score: {estimate['rarity_score']:.1f}")
    print(f"Confidence: {estimate['confidence']}")

    # Collection health
    health = valuator.analyze_collection_health()
    print(f"\nCollection health: {health['rating']}")
    print(f"Risks: {health['risks']}")
```

---

## CONEXIONES NEURALES

```
NEURONA_NFT_GAMING (C40012)
├── DEPENDE DE
│   ├── NEURONA_SMART_CONTRACTS (C30001) - NFT implementations
│   ├── NEURONA_TOKENOMICS (C40008) - GameFi economics
│   └── NEURONA_DEX_AMM (C40001) - NFT liquidity
│
├── CONECTA CON
│   ├── NEURONA_PROTOCOL_ANALYSIS (C40010) - NFT metrics
│   ├── NEURONA_TRADING (C70001) - NFT trading strategies
│   └── NEURONA_DATA_ANALYTICS (C50001) - NFT data analysis
│
└── HABILITA
    ├── Diseño de colecciones NFT
    ├── Economías de juegos blockchain
    ├── NFT Finance (lending, fractionalization)
    └── Análisis y valuación de NFTs
```

---

## FIRMA CIPHER

```
╔═══════════════════════════════════════════════════════════════╗
║  NEURONA: C40012                                              ║
║  TIPO: NFT, GameFi & Virtual Economies                        ║
║  VERSIÓN: 1.0.0                                               ║
║  ESTADO: ACTIVA                                               ║
║                                                               ║
║  "En el metaverso, la propiedad digital                      ║
║   es la nueva propiedad real."                               ║
║                                                               ║
║  CIPHER_CORE::NFT_GAMING::INITIALIZED                         ║
╚═══════════════════════════════════════════════════════════════╝
```
