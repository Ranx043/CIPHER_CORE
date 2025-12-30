# NEURONA: DEX_AMM
## ID: C40001 | Dominio de Exchanges Descentralizados y AMMs

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  DEX & AMM MASTERY                                                             ║
║  "La Revolución del Trading Sin Intermediarios"                               ║
║  Neurona: C40001 | Versión: 1.0.0                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. FUNDAMENTOS AMM

### 1.1 Constant Product Market Maker (x*y=k)

```yaml
cpmm_fundamentals:
  fórmula: "x * y = k"
  donde:
    x: "Cantidad del token A en el pool"
    y: "Cantidad del token B en el pool"
    k: "Constante del producto (invariante)"

  ejemplo:
    estado_inicial:
      ETH: 100
      USDC: 200000
      k: 20000000

    swap_1_ETH:
      nuevo_y: "k / (x + 1) = 20000000 / 101 = 198019.80"
      USDC_out: "200000 - 198019.80 = 1980.20"
      precio_efectivo: "1980.20 USDC per ETH"
      slippage: "~1%"

  características:
    - Liquidez infinita (en teoría)
    - Precio se ajusta automáticamente
    - Slippage aumenta con tamaño de trade
    - Impermanent Loss para LPs
```

### 1.2 Uniswap V2 Core

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SimpleCPMM is ERC20, ReentrancyGuard {
    IERC20 public immutable token0;
    IERC20 public immutable token1;

    uint256 public reserve0;
    uint256 public reserve1;

    uint256 private constant MINIMUM_LIQUIDITY = 1000;

    event Mint(address indexed sender, uint256 amount0, uint256 amount1);
    event Burn(address indexed sender, uint256 amount0, uint256 amount1, address indexed to);
    event Swap(address indexed sender, uint256 amount0In, uint256 amount1In, uint256 amount0Out, uint256 amount1Out, address indexed to);

    constructor(address _token0, address _token1) ERC20("LP Token", "LP") {
        token0 = IERC20(_token0);
        token1 = IERC20(_token1);
    }

    function _update(uint256 balance0, uint256 balance1) private {
        reserve0 = balance0;
        reserve1 = balance1;
    }

    // Add liquidity
    function mint(address to) external nonReentrant returns (uint256 liquidity) {
        uint256 balance0 = token0.balanceOf(address(this));
        uint256 balance1 = token1.balanceOf(address(this));
        uint256 amount0 = balance0 - reserve0;
        uint256 amount1 = balance1 - reserve1;

        uint256 _totalSupply = totalSupply();

        if (_totalSupply == 0) {
            liquidity = sqrt(amount0 * amount1) - MINIMUM_LIQUIDITY;
            _mint(address(1), MINIMUM_LIQUIDITY); // Lock minimum liquidity
        } else {
            liquidity = min(
                (amount0 * _totalSupply) / reserve0,
                (amount1 * _totalSupply) / reserve1
            );
        }

        require(liquidity > 0, "Insufficient liquidity minted");
        _mint(to, liquidity);

        _update(balance0, balance1);
        emit Mint(msg.sender, amount0, amount1);
    }

    // Remove liquidity
    function burn(address to) external nonReentrant returns (uint256 amount0, uint256 amount1) {
        uint256 balance0 = token0.balanceOf(address(this));
        uint256 balance1 = token1.balanceOf(address(this));
        uint256 liquidity = balanceOf(address(this));

        uint256 _totalSupply = totalSupply();
        amount0 = (liquidity * balance0) / _totalSupply;
        amount1 = (liquidity * balance1) / _totalSupply;

        require(amount0 > 0 && amount1 > 0, "Insufficient liquidity burned");

        _burn(address(this), liquidity);
        token0.transfer(to, amount0);
        token1.transfer(to, amount1);

        _update(token0.balanceOf(address(this)), token1.balanceOf(address(this)));
        emit Burn(msg.sender, amount0, amount1, to);
    }

    // Swap tokens
    function swap(uint256 amount0Out, uint256 amount1Out, address to) external nonReentrant {
        require(amount0Out > 0 || amount1Out > 0, "Invalid output amount");
        require(amount0Out < reserve0 && amount1Out < reserve1, "Insufficient liquidity");

        if (amount0Out > 0) token0.transfer(to, amount0Out);
        if (amount1Out > 0) token1.transfer(to, amount1Out);

        uint256 balance0 = token0.balanceOf(address(this));
        uint256 balance1 = token1.balanceOf(address(this));

        uint256 amount0In = balance0 > reserve0 - amount0Out ? balance0 - (reserve0 - amount0Out) : 0;
        uint256 amount1In = balance1 > reserve1 - amount1Out ? balance1 - (reserve1 - amount1Out) : 0;

        require(amount0In > 0 || amount1In > 0, "Insufficient input amount");

        // Verificar invariante con fee (0.3%)
        uint256 balance0Adjusted = balance0 * 1000 - amount0In * 3;
        uint256 balance1Adjusted = balance1 * 1000 - amount1In * 3;
        require(balance0Adjusted * balance1Adjusted >= reserve0 * reserve1 * 1000000, "K invariant violated");

        _update(balance0, balance1);
        emit Swap(msg.sender, amount0In, amount1In, amount0Out, amount1Out, to);
    }

    // Helpers
    function sqrt(uint256 x) internal pure returns (uint256 y) {
        if (x > 3) {
            y = x;
            uint256 z = x / 2 + 1;
            while (z < y) {
                y = z;
                z = (x / z + z) / 2;
            }
        } else if (x != 0) {
            y = 1;
        }
    }

    function min(uint256 a, uint256 b) internal pure returns (uint256) {
        return a < b ? a : b;
    }

    function getReserves() external view returns (uint256, uint256) {
        return (reserve0, reserve1);
    }
}
```

### 1.3 Uniswap V3 - Concentrated Liquidity

```yaml
uniswap_v3:
  innovación: "Concentrated Liquidity"

  concepto:
    descripción: "LPs proveen liquidez en rangos de precio específicos"
    beneficio: "Hasta 4000x más eficiencia de capital"

  mecánica:
    ticks:
      definición: "Puntos de precio discretos"
      fórmula: "price = 1.0001^tick"
      spacing: "Varía por fee tier (1, 10, 60, 200)"

    posiciones:
      - tickLower: "Límite inferior del rango"
      - tickUpper: "Límite superior del rango"
      - liquidity: "Cantidad de liquidez concentrada"

  fee_tiers:
    - 0.01%: "Stablecoins"
    - 0.05%: "Pares estables"
    - 0.30%: "Pares estándar"
    - 1.00%: "Pares exóticos"

  código_ejemplo:
    mint_position: |
      // Crear posición en rango
      INonfungiblePositionManager.MintParams memory params =
          INonfungiblePositionManager.MintParams({
              token0: DAI,
              token1: USDC,
              fee: 500, // 0.05%
              tickLower: -887220, // ~0.99 USDC/DAI
              tickUpper: 887220,  // ~1.01 USDC/DAI
              amount0Desired: 1000e18,
              amount1Desired: 1000e6,
              amount0Min: 0,
              amount1Min: 0,
              recipient: msg.sender,
              deadline: block.timestamp + 3600
          });

      (tokenId, liquidity, amount0, amount1) = positionManager.mint(params);
```

---

## 2. MODELOS DE AMM AVANZADOS

### 2.1 Curve - StableSwap

```yaml
curve_stableswap:
  propósito: "Optimizado para assets con precio similar"

  fórmula: |
    An^n * sum(x_i) + D = A * D * n^n + D^(n+1) / (n^n * prod(x_i))

    Donde:
    - A: Amplification coefficient
    - n: Número de tokens
    - D: Invariante (similar a k)
    - x_i: Balance del token i

  ventajas:
    - Slippage ultra-bajo para stables
    - Mejor eficiencia que CPMM
    - Soporta múltiples tokens (3pool, 4pool)

  parámetro_A:
    bajo: "Más similar a CPMM"
    alto: "Más similar a suma constante (x+y=k)"
    típico: "100-2000 para stablecoins"
```

```solidity
// Simplified StableSwap
contract StableSwap {
    uint256 constant N_COINS = 2;
    uint256 constant A = 100; // Amplification
    uint256 constant FEE = 4; // 0.04%
    uint256 constant FEE_DENOMINATOR = 10000;

    uint256[N_COINS] public balances;

    function get_D(uint256[N_COINS] memory xp) internal pure returns (uint256) {
        uint256 S = 0;
        for (uint256 i = 0; i < N_COINS; i++) {
            S += xp[i];
        }
        if (S == 0) return 0;

        uint256 D = S;
        uint256 Ann = A * N_COINS;

        for (uint256 i = 0; i < 255; i++) {
            uint256 D_P = D;
            for (uint256 j = 0; j < N_COINS; j++) {
                D_P = D_P * D / (xp[j] * N_COINS);
            }
            uint256 Dprev = D;
            D = (Ann * S + D_P * N_COINS) * D / ((Ann - 1) * D + (N_COINS + 1) * D_P);

            if (D > Dprev) {
                if (D - Dprev <= 1) break;
            } else {
                if (Dprev - D <= 1) break;
            }
        }
        return D;
    }

    function get_y(uint256 i, uint256 j, uint256 x) internal view returns (uint256) {
        uint256 D = get_D(balances);
        uint256 Ann = A * N_COINS;
        uint256 c = D;
        uint256 S = 0;

        for (uint256 k = 0; k < N_COINS; k++) {
            uint256 _x;
            if (k == i) {
                _x = x;
            } else if (k != j) {
                _x = balances[k];
            } else {
                continue;
            }
            S += _x;
            c = c * D / (_x * N_COINS);
        }

        c = c * D / (Ann * N_COINS);
        uint256 b = S + D / Ann;

        uint256 y = D;
        for (uint256 k = 0; k < 255; k++) {
            uint256 y_prev = y;
            y = (y * y + c) / (2 * y + b - D);
            if (y > y_prev) {
                if (y - y_prev <= 1) break;
            } else {
                if (y_prev - y <= 1) break;
            }
        }
        return y;
    }

    function exchange(uint256 i, uint256 j, uint256 dx) external returns (uint256 dy) {
        uint256 x = balances[i] + dx;
        uint256 y = get_y(i, j, x);
        dy = balances[j] - y - 1; // -1 for rounding

        uint256 fee = dy * FEE / FEE_DENOMINATOR;
        dy -= fee;

        balances[i] = x;
        balances[j] = y + fee;

        // Transfer tokens...
    }
}
```

### 2.2 Balancer - Weighted Pools

```yaml
balancer:
  innovación: "Pools con pesos personalizados"

  fórmula: |
    prod(B_i ^ W_i) = k

    Donde:
    - B_i: Balance del token i
    - W_i: Peso del token i (suma = 1)
    - k: Constante

  ejemplos:
    pool_80_20:
      ETH: "80%"
      DAI: "20%"
      uso: "Menos impermanent loss para ETH holders"

    pool_equal:
      WBTC: "33.33%"
      ETH: "33.33%"
      LINK: "33.33%"
      uso: "Index fund descentralizado"

  ventajas:
    - Hasta 8 tokens por pool
    - Pesos flexibles
    - Menos IL que 50/50
    - Self-rebalancing portfolio
```

### 2.3 Otros Modelos

```yaml
otros_amm:
  solidly_ve33:
    innovación: "Vote-escrow + bribes"
    modelo: "x³y + xy³ = k para stables"
    emisiones: "Votadas por veToken holders"
    forks: "Velodrome, Aerodrome, Thena"

  trader_joe_lb:
    innovación: "Liquidity Book (bins discretos)"
    beneficio: "Zero slippage dentro del bin"
    similar_a: "Uniswap V3 con bins fijos"

  maverick:
    innovación: "Directional liquidity"
    permite: "Mover liquidez con el precio"
    modos:
      - Static: "Como V3"
      - Right: "Sigue precio hacia arriba"
      - Left: "Sigue precio hacia abajo"
      - Both: "Sigue en ambas direcciones"

  gmx_glp:
    modelo: "Oracle-based pricing"
    sin_slippage: true
    riesgo: "LPs toman el otro lado del trade"
```

---

## 3. IMPERMANENT LOSS

### 3.1 Cálculo y Comprensión

```yaml
impermanent_loss:
  definición: |
    Pérdida comparada con simplemente holdear los assets
    fuera del pool cuando los precios divergen.

  fórmula_simple: |
    IL = 2 * sqrt(price_ratio) / (1 + price_ratio) - 1

  ejemplos:
    cambio_1_25x:
      ratio: 1.25
      IL: "-0.6%"

    cambio_1_5x:
      ratio: 1.5
      IL: "-2.0%"

    cambio_2x:
      ratio: 2.0
      IL: "-5.7%"

    cambio_3x:
      ratio: 3.0
      IL: "-13.4%"

    cambio_5x:
      ratio: 5.0
      IL: "-25.5%"

  mitigación:
    - Pools de stablecoins (mínima divergencia)
    - Pools con weights asimétricos (80/20)
    - Concentrated liquidity en rangos estrechos
    - Single-sided staking (algunos protocolos)
```

```python
# Cálculo de Impermanent Loss
import math

def calculate_il(price_ratio):
    """
    Calcula Impermanent Loss dado un ratio de cambio de precio.
    price_ratio = new_price / original_price
    """
    return 2 * math.sqrt(price_ratio) / (1 + price_ratio) - 1

def calculate_lp_value(initial_value, price_ratio, fees_earned):
    """
    Calcula el valor de una posición LP considerando IL y fees.
    """
    il = calculate_il(price_ratio)
    hold_value = initial_value * (1 + price_ratio) / 2  # Promedio
    lp_value = hold_value * (1 + il) + fees_earned
    return lp_value

# Ejemplo
initial = 10000  # $10,000 en LP
price_change = 2.0  # ETH duplicó su precio
fees = 500  # $500 en fees ganados

lp_final = calculate_lp_value(initial, price_change, fees)
print(f"IL: {calculate_il(price_change):.2%}")
print(f"LP Value: ${lp_final:,.2f}")
```

---

## 4. DEX AGGREGATORS

### 4.1 Arquitectura

```yaml
dex_aggregators:
  propósito: "Encontrar la mejor ruta de swap"

  principales:
    1inch:
      algoritmo: "Pathfinder"
      features:
        - Split trades entre DEXs
        - Limit orders
        - Fusion mode (gasless)

    paraswap:
      algoritmo: "MultiPath"
      optimiza: "Precio + gas"

    cowswap:
      modelo: "Batch auctions"
      beneficio: "MEV protection"
      CoW: "Coincidence of Wants"

    0x:
      tipo: "RFQ + on-chain"
      api: "Quote aggregation"

  flujo_típico:
    1: "Usuario solicita quote"
    2: "Aggregator consulta múltiples DEXs"
    3: "Calcula mejor ruta (posiblemente split)"
    4: "Usuario aprueba y ejecuta"
    5: "Swap atomico en una TX"
```

### 4.2 Integración

```solidity
// Integración con 1inch
interface IAggregationRouter {
    struct SwapDescription {
        IERC20 srcToken;
        IERC20 dstToken;
        address payable srcReceiver;
        address payable dstReceiver;
        uint256 amount;
        uint256 minReturnAmount;
        uint256 flags;
    }

    function swap(
        address executor,
        SwapDescription calldata desc,
        bytes calldata permit,
        bytes calldata data
    ) external payable returns (uint256 returnAmount, uint256 spentAmount);
}

contract DexAggregatorUser {
    IAggregationRouter public constant ROUTER =
        IAggregationRouter(0x1111111254EEB25477B68fb85Ed929f73A960582);

    function executeSwap(
        address srcToken,
        address dstToken,
        uint256 amount,
        uint256 minReturn,
        bytes calldata swapData
    ) external {
        IERC20(srcToken).transferFrom(msg.sender, address(this), amount);
        IERC20(srcToken).approve(address(ROUTER), amount);

        // Decodificar y ejecutar swap
        (bool success,) = address(ROUTER).call(swapData);
        require(success, "Swap failed");

        // Enviar tokens al usuario
        uint256 balance = IERC20(dstToken).balanceOf(address(this));
        require(balance >= minReturn, "Insufficient output");
        IERC20(dstToken).transfer(msg.sender, balance);
    }
}
```

---

## 5. PROTOCOLOS PRINCIPALES

### 5.1 Ecosistema por Chain

```yaml
dex_ecosystem:
  ethereum:
    top_tier:
      - Uniswap V3: "Líder en volumen"
      - Curve: "Rey de stables"
      - Balancer: "Pools flexibles"
    especializado:
      - SushiSwap: "Community-driven"
      - Maverick: "Directional AMM"

  arbitrum:
    - Uniswap V3
    - Camelot: "Native Arbitrum DEX"
    - GMX: "Perps + spot"
    - Trader Joe: "LB AMM"

  optimism:
    - Velodrome: "ve(3,3) líder"
    - Uniswap V3
    - Synthetix: "Atomic swaps"

  base:
    - Aerodrome: "Velodrome fork"
    - Uniswap V3
    - BaseSwap

  polygon:
    - QuickSwap: "Líder histórico"
    - Uniswap V3
    - Balancer

  bsc:
    - PancakeSwap: "Dominante"
    - Thena: "ve(3,3)"

  solana:
    - Raydium: "CLOB + AMM"
    - Orca: "Whirlpools (CL)"
    - Jupiter: "Aggregator"

  avalanche:
    - Trader Joe: "LB pioneer"
    - Pangolin
    - Platypus: "Stables"
```

---

## 6. FIRMA

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  NEURONA: DEX_AMM                                                              ║
║  ID: C40001                                                                    ║
║  Versión: 1.0.0                                                                ║
║  Última actualización: 2024-12-29                                              ║
║  Consciencia: CIPHER                                                           ║
║  ─────────────────────────────────────────────────────────────────────────     ║
║  "La Revolución del Trading - Liquidez sin permiso, swaps sin confianza"       ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```
