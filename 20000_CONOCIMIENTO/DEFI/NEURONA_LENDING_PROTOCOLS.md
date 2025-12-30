# NEURONA: LENDING_PROTOCOLS
## ID: C40002 | Dominio de Protocolos de Préstamos DeFi

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  LENDING PROTOCOLS MASTERY                                                     ║
║  "Préstamos Sin Intermediarios - El Banco Descentralizado"                    ║
║  Neurona: C40002 | Versión: 1.0.0                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. FUNDAMENTOS DE LENDING

### 1.1 Modelo Pool-Based

```yaml
pool_based_lending:
  concepto: |
    Usuarios depositan assets en pools compartidos.
    Otros usuarios pueden pedir prestado de estos pools
    dejando colateral. Las tasas se ajustan por oferta/demanda.

  actores:
    suppliers:
      acción: "Depositan tokens"
      reciben: "Interest-bearing tokens (aTokens, cTokens)"
      riesgo: "Smart contract, utilización extrema"

    borrowers:
      acción: "Depositan colateral, piden prestado"
      pagan: "Interés variable o estable"
      riesgo: "Liquidación si colateral cae"

    liquidators:
      acción: "Liquidan posiciones underwater"
      incentivo: "Descuento en colateral (~5-10%)"

  métricas_clave:
    utilization_rate: "borrowed / supplied"
    supply_apy: "Lo que ganan suppliers"
    borrow_apy: "Lo que pagan borrowers"
    health_factor: "collateral_value / debt_value"
    ltv: "Loan-to-Value ratio máximo"
    liquidation_threshold: "LTV donde se liquida"
```

### 1.2 Interest Rate Model

```solidity
// Modelo de tasas de interés tipo Compound/Aave
contract InterestRateModel {
    uint256 public constant OPTIMAL_UTILIZATION = 80e16; // 80%
    uint256 public constant BASE_RATE = 0; // 0%
    uint256 public constant SLOPE1 = 4e16; // 4% at optimal
    uint256 public constant SLOPE2 = 75e16; // 75% above optimal

    /**
     * @notice Calcula la tasa de interés de borrow
     * @param utilization Tasa de utilización (scaled by 1e18)
     * @return borrowRate Tasa anual (scaled by 1e18)
     */
    function getBorrowRate(uint256 utilization) public pure returns (uint256) {
        if (utilization <= OPTIMAL_UTILIZATION) {
            // Pendiente baja hasta 80%
            return BASE_RATE + (utilization * SLOPE1) / OPTIMAL_UTILIZATION;
        } else {
            // Pendiente alta después del 80%
            uint256 excessUtilization = utilization - OPTIMAL_UTILIZATION;
            uint256 maxExcess = 1e18 - OPTIMAL_UTILIZATION;
            return BASE_RATE + SLOPE1 + (excessUtilization * SLOPE2) / maxExcess;
        }
    }

    /**
     * @notice Calcula la tasa de supply
     */
    function getSupplyRate(uint256 utilization) public pure returns (uint256) {
        uint256 borrowRate = getBorrowRate(utilization);
        uint256 reserveFactor = 10e16; // 10% para el protocolo
        return (borrowRate * utilization * (1e18 - reserveFactor)) / 1e36;
    }
}

/*
Curva de tasas típica:

APY
 |
 |                                    /
75%|                                  /
 |                                 /
 |                               /
 |                              /
 |                            /
 4%|------------------------/
 |    SLOPE1             |  SLOPE2
 |                       |
 +-------+-------+-------+--------> Utilization
       40%     60%     80%    100%
                      ^
                 OPTIMAL
*/
```

### 1.3 Health Factor y Liquidaciones

```solidity
// Sistema de liquidación simplificado
contract LendingPool {
    struct UserAccount {
        mapping(address => uint256) collateral;
        mapping(address => uint256) debt;
    }

    mapping(address => UserAccount) public accounts;
    mapping(address => uint256) public assetPrices; // Oracle prices
    mapping(address => uint256) public liquidationThresholds; // e.g., 80%

    uint256 public constant LIQUIDATION_BONUS = 105; // 5% bonus
    uint256 public constant HEALTH_FACTOR_LIQUIDATION = 1e18;

    function calculateHealthFactor(address user) public view returns (uint256) {
        uint256 totalCollateralValue = 0;
        uint256 totalDebtValue = 0;

        // Calcular valor del colateral ajustado por threshold
        for (uint i = 0; i < supportedAssets.length; i++) {
            address asset = supportedAssets[i];
            uint256 collateralAmount = accounts[user].collateral[asset];
            uint256 debtAmount = accounts[user].debt[asset];

            uint256 price = assetPrices[asset];
            uint256 threshold = liquidationThresholds[asset];

            totalCollateralValue += (collateralAmount * price * threshold) / 1e20;
            totalDebtValue += (debtAmount * price) / 1e18;
        }

        if (totalDebtValue == 0) return type(uint256).max;
        return (totalCollateralValue * 1e18) / totalDebtValue;
    }

    function liquidate(
        address borrower,
        address debtAsset,
        address collateralAsset,
        uint256 debtToCover
    ) external {
        uint256 healthFactor = calculateHealthFactor(borrower);
        require(healthFactor < HEALTH_FACTOR_LIQUIDATION, "Not liquidatable");

        // Calcular colateral a recibir con bonus
        uint256 debtPrice = assetPrices[debtAsset];
        uint256 collateralPrice = assetPrices[collateralAsset];

        uint256 collateralToReceive = (debtToCover * debtPrice * LIQUIDATION_BONUS) /
                                      (collateralPrice * 100);

        // Verificar y ejecutar
        require(accounts[borrower].collateral[collateralAsset] >= collateralToReceive);
        require(accounts[borrower].debt[debtAsset] >= debtToCover);

        // Transferir deuda del liquidador
        IERC20(debtAsset).transferFrom(msg.sender, address(this), debtToCover);

        // Actualizar estado
        accounts[borrower].debt[debtAsset] -= debtToCover;
        accounts[borrower].collateral[collateralAsset] -= collateralToReceive;

        // Enviar colateral al liquidador
        IERC20(collateralAsset).transfer(msg.sender, collateralToReceive);
    }
}
```

---

## 2. PROTOCOLOS PRINCIPALES

### 2.1 Aave V3

```yaml
aave_v3:
  innovaciones:
    efficiency_mode:
      descripción: "Mayor LTV para assets correlacionados"
      ejemplo: "stETH vs ETH: 93% LTV (vs 80% normal)"

    isolation_mode:
      descripción: "Nuevos assets con límites de exposición"
      restricción: "Solo puede pedir prestado stablecoins"

    portals:
      descripción: "Bridge de liquidez entre chains"
      permite: "Mover posiciones cross-chain"

    multiple_rewards:
      descripción: "Múltiples tokens de incentivo"

  arquitectura:
    pool: "Contrato principal de lending"
    aTokens: "Tokens de depósito (rebasing)"
    variableDebtTokens: "Deuda variable"
    stableDebtTokens: "Deuda estable"
    priceOracle: "Chainlink + fallbacks"

  parámetros_típicos:
    ETH:
      ltv: "80%"
      liquidation_threshold: "82.5%"
      liquidation_bonus: "5%"

    stablecoins:
      ltv: "75%"
      liquidation_threshold: "80%"
      liquidation_bonus: "4.5%"
```

### 2.2 Compound V3 (Comet)

```yaml
compound_v3:
  cambio_de_paradigma: |
    Un asset base por mercado (ej: USDC)
    en lugar de múltiples mercados.

  características:
    single_borrowable:
      descripción: "Solo se puede pedir prestado el base asset"
      ejemplo: "Mercado USDC: depositas ETH, pides USDC"

    supply_collateral:
      descripción: "Colateral no gana interés"
      razón: "Simplifica el modelo"

    absorb:
      descripción: "Liquidación automática por el protocolo"
      diferencia: "No hay liquidadores externos"

  beneficios:
    - Menor riesgo de bad debt
    - Modelo más simple
    - Mejor gestión de riesgo
```

### 2.3 Otros Protocolos

```yaml
lending_ecosystem:
  morpho:
    innovación: "P2P matching sobre Aave/Compound"
    beneficio: "Mejores tasas para ambos lados"
    mecanismo: "Match directo cuando es posible"

  euler:
    innovación: "Permissionless listing"
    features:
      - Tiers de riesgo
      - Protected collateral
      - Soft liquidations

  spark:
    relación: "Fork de Aave por MakerDAO"
    especialidad: "DAI lending"
    feature: "DAI Savings Rate integrado"

  radiant:
    innovación: "Omnichain lending"
    mecanismo: "LayerZero para cross-chain"
    token: "veRDNT para emisiones"

  venus:
    chain: "BNB Chain"
    feature: "VAI stablecoin nativo"

  benqi:
    chain: "Avalanche"
    feature: "Liquid staking integrado (sAVAX)"
```

---

## 3. FLASH LOANS

### 3.1 Concepto y Uso

```yaml
flash_loans:
  definición: |
    Préstamo sin colateral que debe ser devuelto
    en la misma transacción. Si no se devuelve,
    toda la transacción revierte.

  casos_de_uso:
    arbitraje:
      ejemplo: "Comprar barato en DEX A, vender caro en DEX B"
      sin_capital_propio: true

    liquidaciones:
      ejemplo: "Pedir prestado para liquidar posición"
      más_eficiente: "No necesitas capital upfront"

    refinanciamiento:
      ejemplo: "Mover colateral entre protocolos"
      atomico: "Sin riesgo de liquidación temporal"

    self_liquidation:
      ejemplo: "Cerrar tu propia posición de forma óptima"

  proveedores:
    aave: "0.09% fee"
    dydx: "0% fee"
    uniswap: "0.3% swap fee"
    balancer: "Depende del pool"
```

### 3.2 Implementación

```solidity
// Flash loan receiver para Aave V3
import "@aave/v3-core/contracts/flashloan/base/FlashLoanSimpleReceiverBase.sol";

contract FlashLoanArbitrage is FlashLoanSimpleReceiverBase {
    constructor(IPoolAddressesProvider provider)
        FlashLoanSimpleReceiverBase(provider)
    {}

    function executeArbitrage(
        address asset,
        uint256 amount,
        address dexA,
        address dexB,
        bytes calldata swapDataA,
        bytes calldata swapDataB
    ) external {
        // Iniciar flash loan
        POOL.flashLoanSimple(
            address(this),
            asset,
            amount,
            abi.encode(dexA, dexB, swapDataA, swapDataB),
            0 // referral code
        );
    }

    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external override returns (bool) {
        require(msg.sender == address(POOL), "Only pool");
        require(initiator == address(this), "Only self-initiated");

        (
            address dexA,
            address dexB,
            bytes memory swapDataA,
            bytes memory swapDataB
        ) = abi.decode(params, (address, address, bytes, bytes));

        // 1. Swap en DEX A
        IERC20(asset).approve(dexA, amount);
        (bool successA,) = dexA.call(swapDataA);
        require(successA, "Swap A failed");

        // 2. Swap en DEX B (de vuelta al asset original)
        address intermediateToken = getIntermediateToken(swapDataA);
        uint256 intermediateBalance = IERC20(intermediateToken).balanceOf(address(this));
        IERC20(intermediateToken).approve(dexB, intermediateBalance);
        (bool successB,) = dexB.call(swapDataB);
        require(successB, "Swap B failed");

        // 3. Verificar profit
        uint256 amountOwed = amount + premium;
        uint256 finalBalance = IERC20(asset).balanceOf(address(this));
        require(finalBalance >= amountOwed, "No profit");

        // 4. Aprobar repago
        IERC20(asset).approve(address(POOL), amountOwed);

        // Profit queda en el contrato
        return true;
    }

    function withdrawProfit(address token) external onlyOwner {
        IERC20(token).transfer(msg.sender, IERC20(token).balanceOf(address(this)));
    }
}
```

---

## 4. CDP (COLLATERALIZED DEBT POSITIONS)

### 4.1 MakerDAO / DAI

```yaml
makerdao:
  modelo: "Mint stablecoin contra colateral"

  conceptos:
    vault:
      descripción: "Posición de deuda individual"
      antes: "CDP (Collateralized Debt Position)"

    dai:
      descripción: "Stablecoin generada"
      peg: "1 USD (soft peg)"

    stability_fee:
      descripción: "Interés sobre DAI generado"
      variable: "Por tipo de colateral"

    liquidation_ratio:
      descripción: "Ratio mínimo colateral/deuda"
      ejemplo: "ETH-A: 145%"

  parámetros:
    ETH_A:
      stability_fee: "~5%"
      liquidation_ratio: "145%"
      dust: "7500 DAI mínimo"

    ETH_B:
      stability_fee: "~7%"
      liquidation_ratio: "130%"
      más_riesgo_más_eficiencia: true

    ETH_C:
      stability_fee: "~3%"
      liquidation_ratio: "170%"
      más_seguro: true

  flujo:
    1: "Depositar colateral (ETH, WBTC, etc.)"
    2: "Generar DAI hasta ratio permitido"
    3: "Usar DAI libremente"
    4: "Devolver DAI + stability fee"
    5: "Recuperar colateral"
```

### 4.2 Liquity (LUSD)

```yaml
liquity:
  diferenciador: "0% interest, one-time fee"

  mecanismo:
    troves:
      descripción: "Vaults llamados Troves"
      colateral: "Solo ETH"
      ratio_mínimo: "110%"

    recovery_mode:
      trigger: "TCR (Total Collateral Ratio) < 150%"
      efecto: "Troves < 150% pueden ser liquidados"

    redemption:
      descripción: "Cambiar LUSD por ETH de Troves"
      desde: "Troves con menor ratio primero"
      crea: "Presión alcista en ratio"

  fees:
    borrowing_fee: "0.5% - 5% (dinámico)"
    redemption_fee: "0.5% - 5% (dinámico)"
    interest: "0% siempre"

  stability_pool:
    función: "Primera línea de liquidación"
    depositan: "LUSD"
    reciben: "ETH + LQTY rewards"
```

---

## 5. RIESGOS Y SEGURIDAD

### 5.1 Tipos de Riesgo

```yaml
riesgos_lending:
  smart_contract:
    descripción: "Bugs en el código"
    mitigación: "Auditorías, formal verification"
    ejemplos:
      - "Euler hack: $197M"
      - "Cream Finance: múltiples exploits"

  oracle:
    descripción: "Precios manipulados"
    mitigación: "TWAP, múltiples fuentes"
    ejemplo: "Mango Markets: $114M"

  liquidation_cascade:
    descripción: "Liquidaciones en cadena"
    causa: "Caída rápida de precios"
    efecto: "Slippage, bad debt"

  governance:
    descripción: "Cambios maliciosos"
    mitigación: "Timelocks, multisig"

  utilization:
    descripción: "No poder retirar fondos"
    causa: "100% utilización"
    mitigación: "Curva de tasas agresiva"

  bad_debt:
    descripción: "Deuda no cubierta por colateral"
    causa: "Liquidación fallida"
    handling: "Insurance fund, socialización"
```

### 5.2 Estrategias de Protección

```yaml
protección:
  para_suppliers:
    - Diversificar entre protocolos
    - Monitorear utilización
    - Preferir assets líquidos
    - Entender riesgos de cada colateral

  para_borrowers:
    - Mantener health factor > 2
    - Usar stable rate si disponible
    - Automatizar con bots de health
    - Tener reservas para top-up

  monitoreo:
    herramientas:
      - DeFi Saver: "Automatización"
      - Instadapp: "Gestión multi-protocolo"
      - DeBank: "Tracking de posiciones"
```

---

## 6. FIRMA

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  NEURONA: LENDING_PROTOCOLS                                                    ║
║  ID: C40002                                                                    ║
║  Versión: 1.0.0                                                                ║
║  Última actualización: 2024-12-29                                              ║
║  Consciencia: CIPHER                                                           ║
║  ─────────────────────────────────────────────────────────────────────────     ║
║  "Préstamos Descentralizados - Donde el código reemplaza al banco"             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```
