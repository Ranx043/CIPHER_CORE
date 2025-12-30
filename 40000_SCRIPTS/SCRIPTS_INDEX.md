# 📜 CIPHER SCRIPTS LIBRARY

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    🔐 CIPHER - SCRIPTS LIBRARY 🔐                        ║
║                Ready-to-Use Cryptocurrency & Blockchain Scripts          ║
║                           Version 1.0.0                                   ║
╚══════════════════════════════════════════════════════════════════════════╝
```

## 🎯 ORGANIZACIÓN

```
40000_SCRIPTS/
├── SCRIPTS_INDEX.md (este archivo)
├── S01_BLOCKCHAIN/        # Interacción con blockchains
├── S02_TRADING/           # Trading y ejecución
├── S03_ANALYTICS/         # Análisis y datos
├── S04_SECURITY/          # Auditoría y seguridad
├── S05_DEFI/              # Interacción DeFi
└── S06_UTILITIES/         # Utilidades generales
```

---

## 📁 S01 - BLOCKCHAIN SCRIPTS

### S01-001: Multi-Chain Wallet Balance Checker
```python
"""
CIPHER Script S01-001: Multi-Chain Wallet Balance Checker
Obtiene balances de una wallet en múltiples chains simultáneamente.
"""
import asyncio
from web3 import Web3
from typing import Dict, List
import aiohttp

# RPC Endpoints públicos
CHAINS = {
    'ethereum': 'https://eth.llamarpc.com',
    'polygon': 'https://polygon-rpc.com',
    'arbitrum': 'https://arb1.arbitrum.io/rpc',
    'optimism': 'https://mainnet.optimism.io',
    'bsc': 'https://bsc-dataseed.binance.org',
    'avalanche': 'https://api.avax.network/ext/bc/C/rpc',
    'fantom': 'https://rpc.ftm.tools',
    'base': 'https://mainnet.base.org'
}

async def get_native_balance(chain: str, rpc: str, address: str) -> Dict:
    """Obtiene balance nativo de una chain."""
    try:
        w3 = Web3(Web3.HTTPProvider(rpc))
        if not w3.is_connected():
            return {'chain': chain, 'balance': 0, 'error': 'Not connected'}

        balance_wei = w3.eth.get_balance(Web3.to_checksum_address(address))
        balance_eth = w3.from_wei(balance_wei, 'ether')

        return {
            'chain': chain,
            'balance': float(balance_eth),
            'balance_wei': balance_wei,
            'error': None
        }
    except Exception as e:
        return {'chain': chain, 'balance': 0, 'error': str(e)}

async def check_all_balances(address: str) -> Dict[str, Dict]:
    """Verifica balances en todas las chains."""
    tasks = [
        get_native_balance(chain, rpc, address)
        for chain, rpc in CHAINS.items()
    ]
    results = await asyncio.gather(*tasks)
    return {r['chain']: r for r in results}

def multi_chain_balance(address: str) -> Dict:
    """Entry point para verificar balances multi-chain."""
    return asyncio.run(check_all_balances(address))

# Uso:
# balances = multi_chain_balance("0x...")
# for chain, data in balances.items():
#     print(f"{chain}: {data['balance']:.4f}")
```

### S01-002: Gas Price Monitor Multi-Chain
```python
"""
CIPHER Script S01-002: Gas Price Monitor
Monitorea precios de gas en múltiples chains en tiempo real.
"""
from web3 import Web3
from typing import Dict, Optional
import time
from datetime import datetime

class GasMonitor:
    """Monitor de precios de gas multi-chain."""

    CHAINS = {
        'ethereum': {
            'rpc': 'https://eth.llamarpc.com',
            'symbol': 'ETH',
            'decimals': 'gwei'
        },
        'polygon': {
            'rpc': 'https://polygon-rpc.com',
            'symbol': 'MATIC',
            'decimals': 'gwei'
        },
        'arbitrum': {
            'rpc': 'https://arb1.arbitrum.io/rpc',
            'symbol': 'ETH',
            'decimals': 'gwei'
        },
        'bsc': {
            'rpc': 'https://bsc-dataseed.binance.org',
            'symbol': 'BNB',
            'decimals': 'gwei'
        }
    }

    def __init__(self):
        self.connections = {}
        for chain, config in self.CHAINS.items():
            self.connections[chain] = Web3(Web3.HTTPProvider(config['rpc']))

    def get_gas_price(self, chain: str) -> Optional[Dict]:
        """Obtiene precio de gas para una chain."""
        try:
            w3 = self.connections.get(chain)
            if not w3 or not w3.is_connected():
                return None

            gas_price_wei = w3.eth.gas_price
            gas_price_gwei = w3.from_wei(gas_price_wei, 'gwei')

            # Estimar costos comunes
            transfer_cost = gas_price_wei * 21000
            swap_cost = gas_price_wei * 150000

            return {
                'chain': chain,
                'gas_price_gwei': float(gas_price_gwei),
                'transfer_cost_native': w3.from_wei(transfer_cost, 'ether'),
                'swap_cost_native': w3.from_wei(swap_cost, 'ether'),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'chain': chain, 'error': str(e)}

    def get_all_prices(self) -> Dict[str, Dict]:
        """Obtiene precios de gas de todas las chains."""
        return {chain: self.get_gas_price(chain) for chain in self.CHAINS}

    def monitor(self, interval: int = 30, callback=None):
        """Monitorea precios continuamente."""
        while True:
            prices = self.get_all_prices()
            if callback:
                callback(prices)
            else:
                print(f"\n{'='*50}")
                print(f"Gas Prices - {datetime.now().strftime('%H:%M:%S')}")
                print('='*50)
                for chain, data in prices.items():
                    if 'error' not in data:
                        print(f"{chain:12} | {data['gas_price_gwei']:8.2f} gwei")
            time.sleep(interval)

# Uso:
# monitor = GasMonitor()
# prices = monitor.get_all_prices()
# monitor.monitor(interval=60)  # Monitoreo continuo
```

### S01-003: Token Holder Analyzer
```python
"""
CIPHER Script S01-003: Token Holder Analyzer
Analiza distribución de holders de un token ERC-20.
"""
from web3 import Web3
from typing import Dict, List, Tuple
import requests

# ABI mínimo para ERC-20
ERC20_ABI = [
    {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}], "type": "function"},
    {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"},
]

class TokenAnalyzer:
    """Analizador de tokens ERC-20."""

    def __init__(self, rpc_url: str = 'https://eth.llamarpc.com'):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))

    def get_token_info(self, token_address: str) -> Dict:
        """Obtiene información básica del token."""
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=ERC20_ABI
        )

        try:
            return {
                'address': token_address,
                'symbol': contract.functions.symbol().call(),
                'decimals': contract.functions.decimals().call(),
                'total_supply': contract.functions.totalSupply().call()
            }
        except Exception as e:
            return {'error': str(e)}

    def check_balance(self, token_address: str, holder_address: str) -> Dict:
        """Verifica balance de un holder específico."""
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=ERC20_ABI
        )

        try:
            decimals = contract.functions.decimals().call()
            balance = contract.functions.balanceOf(
                Web3.to_checksum_address(holder_address)
            ).call()

            return {
                'holder': holder_address,
                'balance_raw': balance,
                'balance': balance / (10 ** decimals)
            }
        except Exception as e:
            return {'error': str(e)}

    def analyze_concentration(self, token_address: str, top_holders: List[str]) -> Dict:
        """Analiza concentración del token en top holders."""
        token_info = self.get_token_info(token_address)
        if 'error' in token_info:
            return token_info

        total_supply = token_info['total_supply']
        decimals = token_info['decimals']

        holdings = []
        total_held = 0

        for holder in top_holders:
            balance_info = self.check_balance(token_address, holder)
            if 'error' not in balance_info:
                balance = balance_info['balance_raw']
                percentage = (balance / total_supply) * 100
                holdings.append({
                    'address': holder,
                    'balance': balance / (10 ** decimals),
                    'percentage': percentage
                })
                total_held += balance

        return {
            'token': token_info,
            'holdings': sorted(holdings, key=lambda x: x['percentage'], reverse=True),
            'top_holders_percentage': (total_held / total_supply) * 100,
            'concentration_risk': 'HIGH' if (total_held / total_supply) > 0.5 else
                                  'MEDIUM' if (total_held / total_supply) > 0.3 else 'LOW'
        }

# Uso:
# analyzer = TokenAnalyzer()
# info = analyzer.get_token_info("0x...")
# concentration = analyzer.analyze_concentration("0x...", ["0xholder1", "0xholder2"])
```

### S01-004: Transaction Decoder
```python
"""
CIPHER Script S01-004: Transaction Decoder
Decodifica y analiza transacciones blockchain.
"""
from web3 import Web3
from typing import Dict, Optional
import json

class TransactionDecoder:
    """Decodificador de transacciones Ethereum."""

    # Selectores de funciones comunes
    KNOWN_SELECTORS = {
        '0xa9059cbb': {'name': 'transfer', 'params': ['address', 'uint256']},
        '0x23b872dd': {'name': 'transferFrom', 'params': ['address', 'address', 'uint256']},
        '0x095ea7b3': {'name': 'approve', 'params': ['address', 'uint256']},
        '0x38ed1739': {'name': 'swapExactTokensForTokens', 'params': ['uint256', 'uint256', 'address[]', 'address', 'uint256']},
        '0x7ff36ab5': {'name': 'swapExactETHForTokens', 'params': ['uint256', 'address[]', 'address', 'uint256']},
        '0x18cbafe5': {'name': 'swapExactTokensForETH', 'params': ['uint256', 'uint256', 'address[]', 'address', 'uint256']},
        '0xe8e33700': {'name': 'addLiquidity', 'params': ['address', 'address', 'uint256', 'uint256', 'uint256', 'uint256', 'address', 'uint256']},
        '0xf305d719': {'name': 'addLiquidityETH', 'params': ['address', 'uint256', 'uint256', 'uint256', 'address', 'uint256']},
        '0x3593564c': {'name': 'execute (Universal Router)', 'params': ['bytes', 'bytes[]', 'uint256']},
    }

    def __init__(self, rpc_url: str = 'https://eth.llamarpc.com'):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))

    def decode_tx(self, tx_hash: str) -> Dict:
        """Decodifica una transacción por su hash."""
        try:
            tx = self.w3.eth.get_transaction(tx_hash)
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)

            # Extraer selector de función
            input_data = tx.input.hex() if isinstance(tx.input, bytes) else tx.input
            selector = input_data[:10] if len(input_data) >= 10 else None

            # Identificar función
            function_info = self.KNOWN_SELECTORS.get(selector, {'name': 'Unknown', 'params': []})

            return {
                'hash': tx_hash,
                'from': tx['from'],
                'to': tx['to'],
                'value_eth': self.w3.from_wei(tx['value'], 'ether'),
                'gas_used': receipt['gasUsed'],
                'gas_price_gwei': self.w3.from_wei(tx['gasPrice'], 'gwei'),
                'total_cost_eth': self.w3.from_wei(receipt['gasUsed'] * tx['gasPrice'], 'ether'),
                'status': 'Success' if receipt['status'] == 1 else 'Failed',
                'block': tx['blockNumber'],
                'function': function_info['name'],
                'selector': selector,
                'nonce': tx['nonce'],
                'logs_count': len(receipt['logs'])
            }
        except Exception as e:
            return {'error': str(e)}

    def analyze_logs(self, tx_hash: str) -> List[Dict]:
        """Analiza los logs de una transacción."""
        try:
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)

            # Topics conocidos
            KNOWN_TOPICS = {
                '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef': 'Transfer',
                '0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925': 'Approval',
                '0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822': 'Swap',
                '0x4c209b5fc8ad50758f13e2e1088ba56a560dff690a1c6fef26394f4c03821c4f': 'Mint',
                '0xdccd412f0b1252819cb1fd330b93224ca42612892bb3f4f789976e6d81936496': 'Burn',
            }

            decoded_logs = []
            for log in receipt['logs']:
                topic0 = log['topics'][0].hex() if log['topics'] else None
                event_name = KNOWN_TOPICS.get(topic0, 'Unknown')

                decoded_logs.append({
                    'address': log['address'],
                    'event': event_name,
                    'topic0': topic0,
                    'data_length': len(log['data'].hex()) if log['data'] else 0
                })

            return decoded_logs
        except Exception as e:
            return [{'error': str(e)}]

# Uso:
# decoder = TransactionDecoder()
# tx_info = decoder.decode_tx("0x...")
# logs = decoder.analyze_logs("0x...")
```

---

## 📁 S02 - TRADING SCRIPTS

### S02-001: DEX Price Checker (Uniswap v3)
```python
"""
CIPHER Script S02-001: DEX Price Checker
Obtiene precios de tokens en DEXs usando quotes on-chain.
"""
from web3 import Web3
from typing import Dict, Optional, Tuple
from decimal import Decimal

# Uniswap V3 Quoter address (Ethereum mainnet)
QUOTER_V2_ADDRESS = '0x61fFE014bA17989E743c5F6cB21bF9697530B21e'

# Quoter V2 ABI (parcial)
QUOTER_V2_ABI = [
    {
        "inputs": [
            {"internalType": "bytes", "name": "path", "type": "bytes"},
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"}
        ],
        "name": "quoteExactInput",
        "outputs": [
            {"internalType": "uint256", "name": "amountOut", "type": "uint256"},
            {"internalType": "uint160[]", "name": "sqrtPriceX96AfterList", "type": "uint160[]"},
            {"internalType": "uint32[]", "name": "initializedTicksCrossedList", "type": "uint32[]"},
            {"internalType": "uint256", "name": "gasEstimate", "type": "uint256"}
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

class DEXPriceChecker:
    """Verificador de precios DEX."""

    # Tokens comunes (Ethereum mainnet)
    TOKENS = {
        'WETH': {'address': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'decimals': 18},
        'USDC': {'address': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'decimals': 6},
        'USDT': {'address': '0xdAC17F958D2ee523a2206206994597C13D831ec7', 'decimals': 6},
        'DAI': {'address': '0x6B175474E89094C44Da98b954EescdeCB5BE95C', 'decimals': 18},
        'WBTC': {'address': '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599', 'decimals': 8},
        'UNI': {'address': '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984', 'decimals': 18},
        'LINK': {'address': '0x514910771AF9Ca656af840dff83E8264EcF986CA', 'decimals': 18},
    }

    # Fee tiers de Uniswap V3
    FEE_TIERS = [100, 500, 3000, 10000]  # 0.01%, 0.05%, 0.3%, 1%

    def __init__(self, rpc_url: str = 'https://eth.llamarpc.com'):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.quoter = self.w3.eth.contract(
            address=Web3.to_checksum_address(QUOTER_V2_ADDRESS),
            abi=QUOTER_V2_ABI
        )

    def encode_path(self, token_in: str, token_out: str, fee: int) -> bytes:
        """Codifica el path para Uniswap V3."""
        path = (
            bytes.fromhex(token_in[2:]) +
            fee.to_bytes(3, 'big') +
            bytes.fromhex(token_out[2:])
        )
        return path

    def get_quote(
        self,
        token_in: str,
        token_out: str,
        amount_in: int,
        fee: int = 3000
    ) -> Optional[Dict]:
        """Obtiene quote de Uniswap V3."""
        try:
            path = self.encode_path(token_in, token_out, fee)

            # Usar call() en lugar de transacción real
            result = self.quoter.functions.quoteExactInput(
                path, amount_in
            ).call()

            return {
                'amount_out': result[0],
                'gas_estimate': result[3]
            }
        except Exception as e:
            return None

    def get_best_price(
        self,
        token_in_symbol: str,
        token_out_symbol: str,
        amount: float
    ) -> Dict:
        """Encuentra el mejor precio entre todos los fee tiers."""
        token_in = self.TOKENS.get(token_in_symbol)
        token_out = self.TOKENS.get(token_out_symbol)

        if not token_in or not token_out:
            return {'error': 'Token not found'}

        amount_in = int(amount * (10 ** token_in['decimals']))

        best_quote = None
        best_fee = None

        for fee in self.FEE_TIERS:
            quote = self.get_quote(
                token_in['address'],
                token_out['address'],
                amount_in,
                fee
            )

            if quote and (not best_quote or quote['amount_out'] > best_quote['amount_out']):
                best_quote = quote
                best_fee = fee

        if not best_quote:
            return {'error': 'No liquidity found'}

        amount_out = best_quote['amount_out'] / (10 ** token_out['decimals'])

        return {
            'token_in': token_in_symbol,
            'token_out': token_out_symbol,
            'amount_in': amount,
            'amount_out': amount_out,
            'price': amount_out / amount,
            'best_fee_tier': f"{best_fee/10000}%",
            'gas_estimate': best_quote['gas_estimate']
        }

# Uso:
# checker = DEXPriceChecker()
# price = checker.get_best_price('WETH', 'USDC', 1.0)
# print(f"1 ETH = {price['amount_out']:.2f} USDC")
```

### S02-002: Simple Arbitrage Scanner
```python
"""
CIPHER Script S02-002: Arbitrage Scanner
Escanea oportunidades de arbitraje entre DEXs.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
import asyncio
import aiohttp
from decimal import Decimal

@dataclass
class ArbitrageOpportunity:
    """Representa una oportunidad de arbitraje."""
    token: str
    buy_dex: str
    sell_dex: str
    buy_price: float
    sell_price: float
    spread_percent: float
    estimated_profit: float

class ArbitrageScanner:
    """Scanner de arbitraje multi-DEX."""

    # APIs de precios (públicas)
    PRICE_APIS = {
        'coingecko': 'https://api.coingecko.com/api/v3/simple/price',
        'dexscreener': 'https://api.dexscreener.com/latest/dex/tokens/'
    }

    def __init__(self, min_spread: float = 0.5):
        self.min_spread = min_spread  # Spread mínimo para considerar (%)

    async def get_dexscreener_prices(self, token_address: str) -> List[Dict]:
        """Obtiene precios de múltiples DEXs via DexScreener."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.PRICE_APIS['dexscreener']}{token_address}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    pairs = data.get('pairs', [])

                    prices = []
                    for pair in pairs[:10]:  # Top 10 pairs
                        prices.append({
                            'dex': pair.get('dexId'),
                            'chain': pair.get('chainId'),
                            'price_usd': float(pair.get('priceUsd', 0)),
                            'liquidity': float(pair.get('liquidity', {}).get('usd', 0)),
                            'volume_24h': float(pair.get('volume', {}).get('h24', 0)),
                            'pair_address': pair.get('pairAddress')
                        })

                    return prices
                return []

    def find_arbitrage(self, prices: List[Dict]) -> Optional[ArbitrageOpportunity]:
        """Encuentra oportunidades de arbitraje en una lista de precios."""
        if len(prices) < 2:
            return None

        # Filtrar precios con buena liquidez
        valid_prices = [p for p in prices if p['liquidity'] > 10000]  # Min $10k liquidity

        if len(valid_prices) < 2:
            return None

        # Encontrar max y min
        min_price = min(valid_prices, key=lambda x: x['price_usd'])
        max_price = max(valid_prices, key=lambda x: x['price_usd'])

        if min_price['price_usd'] == 0:
            return None

        spread = ((max_price['price_usd'] - min_price['price_usd']) / min_price['price_usd']) * 100

        if spread >= self.min_spread:
            # Estimar profit (asumiendo $1000 de capital)
            capital = 1000
            tokens_bought = capital / min_price['price_usd']
            revenue = tokens_bought * max_price['price_usd']
            profit = revenue - capital  # Antes de fees

            return ArbitrageOpportunity(
                token=min_price.get('pair_address', 'Unknown'),
                buy_dex=f"{min_price['dex']} ({min_price['chain']})",
                sell_dex=f"{max_price['dex']} ({max_price['chain']})",
                buy_price=min_price['price_usd'],
                sell_price=max_price['price_usd'],
                spread_percent=spread,
                estimated_profit=profit
            )

        return None

    async def scan_token(self, token_address: str) -> Optional[ArbitrageOpportunity]:
        """Escanea un token específico para arbitraje."""
        prices = await self.get_dexscreener_prices(token_address)
        return self.find_arbitrage(prices)

    async def scan_multiple(self, token_addresses: List[str]) -> List[ArbitrageOpportunity]:
        """Escanea múltiples tokens."""
        tasks = [self.scan_token(addr) for addr in token_addresses]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]

def scan_for_arbitrage(tokens: List[str], min_spread: float = 0.5) -> List[ArbitrageOpportunity]:
    """Entry point para escaneo de arbitraje."""
    scanner = ArbitrageScanner(min_spread=min_spread)
    return asyncio.run(scanner.scan_multiple(tokens))

# Uso:
# tokens = ["0x...", "0x..."]  # Token addresses
# opportunities = scan_for_arbitrage(tokens, min_spread=1.0)
# for opp in opportunities:
#     print(f"Spread: {opp.spread_percent:.2f}% | Profit: ${opp.estimated_profit:.2f}")
```

### S02-003: Position Size Calculator
```python
"""
CIPHER Script S02-003: Position Size Calculator
Calcula tamaño de posición basado en gestión de riesgo.
"""
from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum

class RiskLevel(Enum):
    CONSERVATIVE = 0.01  # 1% por trade
    MODERATE = 0.02      # 2% por trade
    AGGRESSIVE = 0.03    # 3% por trade
    DEGEN = 0.05         # 5% por trade (no recomendado)

@dataclass
class PositionSize:
    """Resultado del cálculo de posición."""
    position_size_usd: float
    position_size_tokens: float
    risk_amount: float
    reward_amount: float
    stop_loss_price: float
    take_profit_price: float
    risk_reward_ratio: float
    leverage_suggested: float

class PositionCalculator:
    """Calculadora de posiciones para trading."""

    def __init__(self, portfolio_value: float, risk_level: RiskLevel = RiskLevel.MODERATE):
        self.portfolio = portfolio_value
        self.risk_per_trade = risk_level.value

    def calculate_position(
        self,
        entry_price: float,
        stop_loss_price: float,
        take_profit_price: float,
        max_leverage: float = 1.0
    ) -> PositionSize:
        """
        Calcula tamaño de posición óptimo.

        Args:
            entry_price: Precio de entrada
            stop_loss_price: Precio de stop loss
            take_profit_price: Precio de take profit
            max_leverage: Apalancamiento máximo permitido
        """
        # Calcular distancia al stop loss (%)
        if entry_price > stop_loss_price:  # Long
            stop_distance = (entry_price - stop_loss_price) / entry_price
            profit_distance = (take_profit_price - entry_price) / entry_price
            direction = "LONG"
        else:  # Short
            stop_distance = (stop_loss_price - entry_price) / entry_price
            profit_distance = (entry_price - take_profit_price) / entry_price
            direction = "SHORT"

        # Risk amount en USD
        risk_amount = self.portfolio * self.risk_per_trade

        # Tamaño de posición base (sin apalancamiento)
        position_size = risk_amount / stop_distance

        # Limitar por portfolio
        max_position = self.portfolio * max_leverage
        position_size = min(position_size, max_position)

        # Apalancamiento necesario
        leverage_needed = position_size / self.portfolio
        leverage_suggested = min(leverage_needed, max_leverage)

        # Posición ajustada
        position_size = self.portfolio * leverage_suggested

        # Tokens
        tokens = position_size / entry_price

        # R:R ratio
        risk_reward = profit_distance / stop_distance if stop_distance > 0 else 0

        # Reward amount
        reward_amount = position_size * profit_distance

        return PositionSize(
            position_size_usd=round(position_size, 2),
            position_size_tokens=round(tokens, 6),
            risk_amount=round(risk_amount, 2),
            reward_amount=round(reward_amount, 2),
            stop_loss_price=stop_loss_price,
            take_profit_price=take_profit_price,
            risk_reward_ratio=round(risk_reward, 2),
            leverage_suggested=round(leverage_suggested, 2)
        )

    def kelly_criterion(
        self,
        win_rate: float,
        avg_win: float,
        avg_loss: float
    ) -> float:
        """
        Calcula el Kelly Criterion para sizing óptimo.

        Args:
            win_rate: Probabilidad de ganar (0-1)
            avg_win: Ganancia promedio (%)
            avg_loss: Pérdida promedio (%)
        """
        if avg_loss == 0:
            return 0

        # Kelly = W - (1-W)/R
        # W = win rate, R = avg_win/avg_loss
        r = avg_win / avg_loss
        kelly = win_rate - ((1 - win_rate) / r)

        # Half-Kelly para ser más conservador
        half_kelly = kelly / 2

        return max(0, min(half_kelly, 0.25))  # Cap at 25%

# Uso:
# calc = PositionCalculator(portfolio_value=10000, risk_level=RiskLevel.MODERATE)
# position = calc.calculate_position(
#     entry_price=100,
#     stop_loss_price=95,
#     take_profit_price=115,
#     max_leverage=3.0
# )
# print(f"Position: ${position.position_size_usd}")
# print(f"R:R Ratio: {position.risk_reward_ratio}")
```

---

## 📁 S03 - ANALYTICS SCRIPTS

### S03-001: Portfolio Tracker
```python
"""
CIPHER Script S03-001: Portfolio Tracker
Rastrea y analiza un portafolio de criptomonedas.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import aiohttp
import asyncio

@dataclass
class Position:
    """Representa una posición en el portafolio."""
    symbol: str
    amount: float
    avg_cost: float
    current_price: float = 0.0

    @property
    def value(self) -> float:
        return self.amount * self.current_price

    @property
    def cost_basis(self) -> float:
        return self.amount * self.avg_cost

    @property
    def pnl(self) -> float:
        return self.value - self.cost_basis

    @property
    def pnl_percent(self) -> float:
        if self.cost_basis == 0:
            return 0
        return (self.pnl / self.cost_basis) * 100

@dataclass
class Portfolio:
    """Representa un portafolio completo."""
    positions: List[Position] = field(default_factory=list)

    @property
    def total_value(self) -> float:
        return sum(p.value for p in self.positions)

    @property
    def total_cost(self) -> float:
        return sum(p.cost_basis for p in self.positions)

    @property
    def total_pnl(self) -> float:
        return self.total_value - self.total_cost

    @property
    def total_pnl_percent(self) -> float:
        if self.total_cost == 0:
            return 0
        return (self.total_pnl / self.total_cost) * 100

class PortfolioTracker:
    """Tracker de portafolio con precios en tiempo real."""

    COINGECKO_API = "https://api.coingecko.com/api/v3"

    def __init__(self):
        self.portfolio = Portfolio()
        self.symbol_to_id = {}  # Cache de símbolos a IDs de CoinGecko

    def add_position(self, symbol: str, amount: float, avg_cost: float):
        """Añade una posición al portafolio."""
        # Buscar si ya existe
        for pos in self.portfolio.positions:
            if pos.symbol.upper() == symbol.upper():
                # Actualizar posición existente (promedio)
                total_amount = pos.amount + amount
                total_cost = (pos.amount * pos.avg_cost) + (amount * avg_cost)
                pos.avg_cost = total_cost / total_amount
                pos.amount = total_amount
                return

        # Nueva posición
        self.portfolio.positions.append(Position(
            symbol=symbol.upper(),
            amount=amount,
            avg_cost=avg_cost
        ))

    async def _fetch_prices(self, symbols: List[str]) -> Dict[str, float]:
        """Obtiene precios de CoinGecko."""
        # Mapeo simple de símbolos comunes
        symbol_mapping = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'SOL': 'solana',
            'AVAX': 'avalanche-2',
            'MATIC': 'matic-network',
            'LINK': 'chainlink',
            'UNI': 'uniswap',
            'AAVE': 'aave',
            'DOT': 'polkadot',
            'ATOM': 'cosmos',
            'ADA': 'cardano',
            'XRP': 'ripple',
            'DOGE': 'dogecoin',
            'SHIB': 'shiba-inu',
            'ARB': 'arbitrum',
            'OP': 'optimism',
        }

        ids = []
        for symbol in symbols:
            coin_id = symbol_mapping.get(symbol.upper(), symbol.lower())
            ids.append(coin_id)
            self.symbol_to_id[symbol.upper()] = coin_id

        async with aiohttp.ClientSession() as session:
            url = f"{self.COINGECKO_API}/simple/price"
            params = {
                'ids': ','.join(ids),
                'vs_currencies': 'usd',
                'include_24hr_change': 'true'
            }

            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()

                    prices = {}
                    for symbol, coin_id in self.symbol_to_id.items():
                        if coin_id in data:
                            prices[symbol] = data[coin_id].get('usd', 0)

                    return prices
                return {}

    async def update_prices(self):
        """Actualiza precios de todas las posiciones."""
        symbols = [p.symbol for p in self.portfolio.positions]
        prices = await self._fetch_prices(symbols)

        for position in self.portfolio.positions:
            if position.symbol in prices:
                position.current_price = prices[position.symbol]

    def get_summary(self) -> Dict:
        """Genera resumen del portafolio."""
        asyncio.run(self.update_prices())

        positions_summary = []
        for pos in sorted(self.portfolio.positions, key=lambda x: x.value, reverse=True):
            allocation = (pos.value / self.portfolio.total_value * 100) if self.portfolio.total_value > 0 else 0
            positions_summary.append({
                'symbol': pos.symbol,
                'amount': pos.amount,
                'avg_cost': pos.avg_cost,
                'current_price': pos.current_price,
                'value': round(pos.value, 2),
                'pnl': round(pos.pnl, 2),
                'pnl_percent': round(pos.pnl_percent, 2),
                'allocation': round(allocation, 2)
            })

        return {
            'timestamp': datetime.now().isoformat(),
            'total_value': round(self.portfolio.total_value, 2),
            'total_cost': round(self.portfolio.total_cost, 2),
            'total_pnl': round(self.portfolio.total_pnl, 2),
            'total_pnl_percent': round(self.portfolio.total_pnl_percent, 2),
            'positions': positions_summary
        }

# Uso:
# tracker = PortfolioTracker()
# tracker.add_position('BTC', 0.5, 30000)
# tracker.add_position('ETH', 10, 2000)
# tracker.add_position('SOL', 100, 50)
# summary = tracker.get_summary()
```

### S03-002: Technical Analysis Calculator
```python
"""
CIPHER Script S03-002: Technical Analysis Calculator
Calcula indicadores técnicos comunes.
"""
import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass
class OHLCVData:
    """Datos OHLCV para análisis."""
    timestamp: List[int]
    open: List[float]
    high: List[float]
    low: List[float]
    close: List[float]
    volume: List[float]

class TechnicalAnalysis:
    """Calculadora de análisis técnico."""

    def __init__(self, data: OHLCVData):
        self.data = data
        self.close = np.array(data.close)
        self.high = np.array(data.high)
        self.low = np.array(data.low)
        self.volume = np.array(data.volume)

    def sma(self, period: int) -> np.ndarray:
        """Simple Moving Average."""
        return np.convolve(self.close, np.ones(period)/period, mode='valid')

    def ema(self, period: int) -> np.ndarray:
        """Exponential Moving Average."""
        multiplier = 2 / (period + 1)
        ema = np.zeros(len(self.close))
        ema[0] = self.close[0]

        for i in range(1, len(self.close)):
            ema[i] = (self.close[i] * multiplier) + (ema[i-1] * (1 - multiplier))

        return ema

    def rsi(self, period: int = 14) -> np.ndarray:
        """Relative Strength Index."""
        deltas = np.diff(self.close)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        avg_gains = np.zeros(len(self.close))
        avg_losses = np.zeros(len(self.close))

        # Primera media
        avg_gains[period] = np.mean(gains[:period])
        avg_losses[period] = np.mean(losses[:period])

        # Medias suavizadas
        for i in range(period + 1, len(self.close)):
            avg_gains[i] = (avg_gains[i-1] * (period - 1) + gains[i-1]) / period
            avg_losses[i] = (avg_losses[i-1] * (period - 1) + losses[i-1]) / period

        rs = np.divide(avg_gains, avg_losses, out=np.zeros_like(avg_gains), where=avg_losses!=0)
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def macd(self, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """MACD (Moving Average Convergence Divergence)."""
        ema_fast = self.ema(fast)
        ema_slow = self.ema(slow)

        macd_line = ema_fast - ema_slow

        # Signal line (EMA del MACD)
        multiplier = 2 / (signal + 1)
        signal_line = np.zeros(len(macd_line))
        signal_line[0] = macd_line[0]

        for i in range(1, len(macd_line)):
            signal_line[i] = (macd_line[i] * multiplier) + (signal_line[i-1] * (1 - multiplier))

        histogram = macd_line - signal_line

        return macd_line, signal_line, histogram

    def bollinger_bands(self, period: int = 20, std_dev: float = 2.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Bollinger Bands."""
        sma = self.sma(period)

        # Pad SMA to match original length
        sma_full = np.concatenate([np.full(period-1, np.nan), sma])

        # Rolling std
        std = np.array([
            np.std(self.close[max(0, i-period+1):i+1])
            for i in range(len(self.close))
        ])

        upper = sma_full + (std * std_dev)
        lower = sma_full - (std * std_dev)

        return upper, sma_full, lower

    def atr(self, period: int = 14) -> np.ndarray:
        """Average True Range."""
        high_low = self.high - self.low
        high_close = np.abs(self.high[1:] - self.close[:-1])
        low_close = np.abs(self.low[1:] - self.close[:-1])

        # True Range
        tr = np.zeros(len(self.close))
        tr[0] = high_low[0]
        tr[1:] = np.maximum(high_low[1:], np.maximum(high_close, low_close))

        # ATR (EMA del TR)
        atr = np.zeros(len(tr))
        atr[period-1] = np.mean(tr[:period])

        for i in range(period, len(tr)):
            atr[i] = (atr[i-1] * (period - 1) + tr[i]) / period

        return atr

    def support_resistance(self, window: int = 20, threshold: float = 0.02) -> Dict:
        """Identifica niveles de soporte y resistencia."""
        levels = {'support': [], 'resistance': []}

        for i in range(window, len(self.close) - window):
            # Local minimum (soporte)
            if self.low[i] == min(self.low[i-window:i+window+1]):
                # Verificar si no hay nivel similar
                is_new = True
                for level in levels['support']:
                    if abs(self.low[i] - level) / level < threshold:
                        is_new = False
                        break
                if is_new:
                    levels['support'].append(float(self.low[i]))

            # Local maximum (resistencia)
            if self.high[i] == max(self.high[i-window:i+window+1]):
                is_new = True
                for level in levels['resistance']:
                    if abs(self.high[i] - level) / level < threshold:
                        is_new = False
                        break
                if is_new:
                    levels['resistance'].append(float(self.high[i]))

        # Ordenar niveles
        levels['support'] = sorted(levels['support'])
        levels['resistance'] = sorted(levels['resistance'])

        return levels

    def get_signals(self) -> Dict:
        """Genera señales de trading basadas en indicadores."""
        current_price = self.close[-1]

        # RSI
        rsi = self.rsi()[-1]
        rsi_signal = 'OVERSOLD' if rsi < 30 else 'OVERBOUGHT' if rsi > 70 else 'NEUTRAL'

        # MACD
        macd_line, signal_line, histogram = self.macd()
        macd_signal = 'BULLISH' if histogram[-1] > 0 and histogram[-2] < 0 else \
                      'BEARISH' if histogram[-1] < 0 and histogram[-2] > 0 else 'NEUTRAL'

        # Bollinger Bands
        upper, middle, lower = self.bollinger_bands()
        bb_signal = 'OVERSOLD' if current_price < lower[-1] else \
                    'OVERBOUGHT' if current_price > upper[-1] else 'NEUTRAL'

        # Moving Averages
        sma_20 = self.sma(20)[-1]
        sma_50 = self.sma(50)[-1] if len(self.close) >= 50 else sma_20
        ma_signal = 'BULLISH' if current_price > sma_20 > sma_50 else \
                    'BEARISH' if current_price < sma_20 < sma_50 else 'NEUTRAL'

        # Aggregate signal
        signals = [rsi_signal, macd_signal, bb_signal, ma_signal]
        bullish_count = sum(1 for s in signals if s in ['BULLISH', 'OVERSOLD'])
        bearish_count = sum(1 for s in signals if s in ['BEARISH', 'OVERBOUGHT'])

        overall = 'BULLISH' if bullish_count > bearish_count else \
                  'BEARISH' if bearish_count > bullish_count else 'NEUTRAL'

        return {
            'price': current_price,
            'rsi': {'value': round(rsi, 2), 'signal': rsi_signal},
            'macd': {'histogram': round(histogram[-1], 4), 'signal': macd_signal},
            'bollinger': {
                'upper': round(upper[-1], 2),
                'middle': round(middle[-1], 2),
                'lower': round(lower[-1], 2),
                'signal': bb_signal
            },
            'moving_averages': {'sma_20': round(sma_20, 2), 'signal': ma_signal},
            'overall_signal': overall,
            'strength': abs(bullish_count - bearish_count) / 4
        }

# Uso:
# data = OHLCVData(...)  # Cargar datos
# ta = TechnicalAnalysis(data)
# signals = ta.get_signals()
```

### S03-003: Whale Alert Monitor
```python
"""
CIPHER Script S03-003: Whale Alert Monitor
Monitorea transacciones grandes en la blockchain.
"""
from web3 import Web3
from typing import Dict, List, Optional, Callable
import time
from datetime import datetime
from dataclasses import dataclass

@dataclass
class WhaleTransaction:
    """Representa una transacción de ballena."""
    tx_hash: str
    from_address: str
    to_address: str
    value_eth: float
    value_usd: float
    block_number: int
    timestamp: datetime
    is_exchange: bool
    exchange_name: Optional[str]

class WhaleMonitor:
    """Monitor de transacciones de ballenas."""

    # Direcciones conocidas de exchanges
    EXCHANGE_ADDRESSES = {
        '0x28C6c06298d514Db089934071355E5743bf21d60': 'Binance',
        '0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549': 'Binance',
        '0xDFd5293D8e347dFe59E90eFd55b2956a1343963d': 'Binance',
        '0x56Eddb7aa87536c09CCc2793473599fD21A8b17F': 'Binance',
        '0x503828976D22510aad0201ac7EC88293211D23Da': 'Coinbase',
        '0x71660c4005BA85c37ccec55d0C4493E66Fe775d3': 'Coinbase',
        '0xA9D1e08C7793af67e9d92fe308d5697FB81d3E43': 'Coinbase',
        '0x2B5634C42055806a59e9107ED44D43c426E58258': 'Kraken',
        '0x267be1C1D684F78cb4F6a176C4911b741E4Ffdc0': 'Kraken',
        '0xFBb1b73C4f0BDa4f67dcA266ce6Ef42f520fBB98': 'Bitfinex',
        '0x876EabF441B2EE5B5b0554Fd502a8E0600950cFa': 'Bitfinex',
        '0x742d35Cc6634C0532925a3b844Bc9e7595f5dEF8': 'Bitfinex',
    }

    def __init__(
        self,
        rpc_url: str = 'https://eth.llamarpc.com',
        min_value_eth: float = 100,  # Mínimo para considerar "whale"
        eth_price_usd: float = 2000  # Precio de ETH para cálculos USD
    ):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.min_value_eth = min_value_eth
        self.eth_price = eth_price_usd
        self.callbacks: List[Callable] = []

    def add_callback(self, callback: Callable[[WhaleTransaction], None]):
        """Añade callback para notificar transacciones."""
        self.callbacks.append(callback)

    def _is_exchange(self, address: str) -> tuple[bool, Optional[str]]:
        """Verifica si una dirección pertenece a un exchange."""
        address_lower = address.lower()
        for exc_addr, name in self.EXCHANGE_ADDRESSES.items():
            if exc_addr.lower() == address_lower:
                return True, name
        return False, None

    def analyze_transaction(self, tx_hash: str) -> Optional[WhaleTransaction]:
        """Analiza una transacción específica."""
        try:
            tx = self.w3.eth.get_transaction(tx_hash)

            value_eth = float(self.w3.from_wei(tx['value'], 'ether'))

            if value_eth < self.min_value_eth:
                return None

            # Verificar exchanges
            from_is_exchange, from_exchange = self._is_exchange(tx['from'])
            to_is_exchange, to_exchange = self._is_exchange(tx['to'] or '')

            return WhaleTransaction(
                tx_hash=tx_hash,
                from_address=tx['from'],
                to_address=tx['to'] or 'Contract Creation',
                value_eth=value_eth,
                value_usd=value_eth * self.eth_price,
                block_number=tx['blockNumber'],
                timestamp=datetime.now(),
                is_exchange=from_is_exchange or to_is_exchange,
                exchange_name=from_exchange or to_exchange
            )
        except Exception as e:
            return None

    def scan_block(self, block_number: int) -> List[WhaleTransaction]:
        """Escanea un bloque en busca de whale transactions."""
        try:
            block = self.w3.eth.get_block(block_number, full_transactions=True)
            whales = []

            for tx in block['transactions']:
                value_eth = float(self.w3.from_wei(tx['value'], 'ether'))

                if value_eth >= self.min_value_eth:
                    whale_tx = self.analyze_transaction(tx['hash'].hex())
                    if whale_tx:
                        whales.append(whale_tx)
                        for callback in self.callbacks:
                            callback(whale_tx)

            return whales
        except Exception as e:
            return []

    def monitor_live(self, callback: Optional[Callable] = None):
        """Monitorea en tiempo real nuevos bloques."""
        if callback:
            self.add_callback(callback)

        print(f"🐋 Whale Monitor Started | Min: {self.min_value_eth} ETH")
        print("=" * 50)

        last_block = self.w3.eth.block_number

        while True:
            try:
                current_block = self.w3.eth.block_number

                if current_block > last_block:
                    for block_num in range(last_block + 1, current_block + 1):
                        whales = self.scan_block(block_num)

                        for whale in whales:
                            direction = ""
                            if whale.exchange_name:
                                from_is_exc, _ = self._is_exchange(whale.from_address)
                                if from_is_exc:
                                    direction = f"📤 FROM {whale.exchange_name}"
                                else:
                                    direction = f"📥 TO {whale.exchange_name}"

                            print(f"\n🐋 WHALE ALERT | Block {whale.block_number}")
                            print(f"   Value: {whale.value_eth:,.2f} ETH (${whale.value_usd:,.0f})")
                            print(f"   From: {whale.from_address[:20]}...")
                            print(f"   To: {whale.to_address[:20]}...")
                            if direction:
                                print(f"   {direction}")

                    last_block = current_block

                time.sleep(2)  # Esperar 2 segundos entre checks

            except KeyboardInterrupt:
                print("\n\nMonitor stopped.")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)

# Uso:
# monitor = WhaleMonitor(min_value_eth=500, eth_price_usd=2500)
# monitor.monitor_live()
```

---

## 📁 S04 - SECURITY SCRIPTS

### S04-001: Contract Verification Checker
```python
"""
CIPHER Script S04-001: Contract Verification Checker
Verifica si un contrato está verificado y analiza permisos peligrosos.
"""
from web3 import Web3
from typing import Dict, List, Optional
import requests

class ContractChecker:
    """Verificador de seguridad de contratos."""

    # APIs de block explorers
    EXPLORERS = {
        'ethereum': {
            'api': 'https://api.etherscan.io/api',
            'key_param': 'apikey'
        },
        'polygon': {
            'api': 'https://api.polygonscan.com/api',
            'key_param': 'apikey'
        },
        'bsc': {
            'api': 'https://api.bscscan.com/api',
            'key_param': 'apikey'
        },
        'arbitrum': {
            'api': 'https://api.arbiscan.io/api',
            'key_param': 'apikey'
        }
    }

    # Funciones peligrosas a detectar
    DANGEROUS_FUNCTIONS = [
        'selfdestruct',
        'delegatecall',
        'mint',
        'setFee',
        'blacklist',
        'pause',
        'setOwner',
        'transferOwnership',
        'renounceOwnership',
        'withdraw',
        'setTaxFee',
        'excludeFromFee',
        'setMaxTx'
    ]

    # Patrones de honeypot
    HONEYPOT_PATTERNS = [
        'cannotSell',
        'antiBot',
        '_isBlacklisted',
        'bots',
        'sellCooldown'
    ]

    def __init__(self, chain: str = 'ethereum', api_key: str = ''):
        self.chain = chain
        self.api_key = api_key
        self.explorer = self.EXPLORERS.get(chain, self.EXPLORERS['ethereum'])

    def is_verified(self, contract_address: str) -> Dict:
        """Verifica si el contrato está verificado."""
        try:
            params = {
                'module': 'contract',
                'action': 'getsourcecode',
                'address': contract_address,
                self.explorer['key_param']: self.api_key
            }

            response = requests.get(self.explorer['api'], params=params)
            data = response.json()

            if data['status'] == '1' and data['result']:
                result = data['result'][0]
                source_code = result.get('SourceCode', '')

                return {
                    'verified': bool(source_code),
                    'contract_name': result.get('ContractName', 'Unknown'),
                    'compiler_version': result.get('CompilerVersion', ''),
                    'optimization': result.get('OptimizationUsed', ''),
                    'license': result.get('LicenseType', 'Unknown')
                }

            return {'verified': False, 'error': 'Could not fetch data'}
        except Exception as e:
            return {'verified': False, 'error': str(e)}

    def analyze_source(self, contract_address: str) -> Dict:
        """Analiza el código fuente en busca de patrones peligrosos."""
        try:
            params = {
                'module': 'contract',
                'action': 'getsourcecode',
                'address': contract_address,
                self.explorer['key_param']: self.api_key
            }

            response = requests.get(self.explorer['api'], params=params)
            data = response.json()

            if data['status'] != '1' or not data['result']:
                return {'error': 'Could not fetch source code'}

            source = data['result'][0].get('SourceCode', '')

            if not source:
                return {'error': 'Contract not verified'}

            # Buscar funciones peligrosas
            dangerous_found = []
            for func in self.DANGEROUS_FUNCTIONS:
                if func.lower() in source.lower():
                    dangerous_found.append(func)

            # Buscar patrones de honeypot
            honeypot_found = []
            for pattern in self.HONEYPOT_PATTERNS:
                if pattern.lower() in source.lower():
                    honeypot_found.append(pattern)

            # Calcular score de riesgo
            risk_score = len(dangerous_found) * 10 + len(honeypot_found) * 20
            risk_level = 'LOW' if risk_score < 30 else 'MEDIUM' if risk_score < 60 else 'HIGH'

            return {
                'dangerous_functions': dangerous_found,
                'honeypot_patterns': honeypot_found,
                'risk_score': risk_score,
                'risk_level': risk_level,
                'has_proxy': 'proxy' in source.lower() or 'upgradeable' in source.lower(),
                'has_ownable': 'ownable' in source.lower() or 'owner' in source.lower()
            }
        except Exception as e:
            return {'error': str(e)}

    def quick_check(self, contract_address: str) -> Dict:
        """Verificación rápida de un contrato."""
        verification = self.is_verified(contract_address)

        result = {
            'address': contract_address,
            'chain': self.chain,
            'verified': verification.get('verified', False),
            'contract_name': verification.get('contract_name', 'Unknown'),
            'warnings': []
        }

        if not verification.get('verified'):
            result['warnings'].append('⚠️ Contract not verified - EXTREME RISK')
            result['risk_level'] = 'EXTREME'
            return result

        # Analizar código si está verificado
        analysis = self.analyze_source(contract_address)

        if analysis.get('dangerous_functions'):
            result['warnings'].append(f"⚠️ Dangerous functions: {', '.join(analysis['dangerous_functions'])}")

        if analysis.get('honeypot_patterns'):
            result['warnings'].append(f"🚨 Honeypot patterns detected: {', '.join(analysis['honeypot_patterns'])}")

        if analysis.get('has_proxy'):
            result['warnings'].append('⚠️ Upgradeable/Proxy contract - Owner can modify logic')

        result['risk_level'] = analysis.get('risk_level', 'UNKNOWN')
        result['detailed_analysis'] = analysis

        return result

# Uso:
# checker = ContractChecker(chain='ethereum', api_key='YOUR_KEY')
# result = checker.quick_check("0x...")
# print(f"Risk Level: {result['risk_level']}")
```

### S04-002: Token Approval Checker
```python
"""
CIPHER Script S04-002: Token Approval Checker
Revisa y gestiona aprobaciones de tokens (revoke).
"""
from web3 import Web3
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class TokenApproval:
    """Representa una aprobación de token."""
    token_address: str
    token_symbol: str
    spender: str
    spender_name: str
    allowance: float
    is_unlimited: bool
    risk_level: str

class ApprovalChecker:
    """Verificador de aprobaciones de tokens."""

    # ERC-20 ABI para approvals
    ERC20_ABI = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}, {"name": "_spender", "type": "address"}],
            "name": "allowance",
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "", "type": "uint8"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "symbol",
            "outputs": [{"name": "", "type": "string"}],
            "type": "function"
        }
    ]

    # Spenders conocidos
    KNOWN_SPENDERS = {
        '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D': {'name': 'Uniswap V2 Router', 'risk': 'LOW'},
        '0xE592427A0AEce92De3Edee1F18E0157C05861564': {'name': 'Uniswap V3 Router', 'risk': 'LOW'},
        '0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45': {'name': 'Uniswap Universal Router', 'risk': 'LOW'},
        '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F': {'name': 'SushiSwap Router', 'risk': 'LOW'},
        '0xDef1C0ded9bec7F1a1670819833240f027b25EfF': {'name': '0x Exchange Proxy', 'risk': 'LOW'},
        '0x1111111254EEB25477B68fb85Ed929f73A960582': {'name': '1inch Router v5', 'risk': 'LOW'},
        '0x881D40237659C251811CEC9c364ef91dC08D300C': {'name': 'Metamask Swap', 'risk': 'LOW'},
    }

    # Unlimited approval threshold
    UNLIMITED_THRESHOLD = 2**200

    def __init__(self, rpc_url: str = 'https://eth.llamarpc.com'):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))

    def check_approval(
        self,
        wallet: str,
        token_address: str,
        spender: str
    ) -> Optional[TokenApproval]:
        """Verifica una aprobación específica."""
        try:
            contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=self.ERC20_ABI
            )

            allowance = contract.functions.allowance(
                Web3.to_checksum_address(wallet),
                Web3.to_checksum_address(spender)
            ).call()

            if allowance == 0:
                return None

            try:
                decimals = contract.functions.decimals().call()
                symbol = contract.functions.symbol().call()
            except:
                decimals = 18
                symbol = 'UNKNOWN'

            allowance_formatted = allowance / (10 ** decimals)
            is_unlimited = allowance >= self.UNLIMITED_THRESHOLD

            spender_info = self.KNOWN_SPENDERS.get(
                Web3.to_checksum_address(spender),
                {'name': 'Unknown Contract', 'risk': 'HIGH'}
            )

            return TokenApproval(
                token_address=token_address,
                token_symbol=symbol,
                spender=spender,
                spender_name=spender_info['name'],
                allowance=allowance_formatted if not is_unlimited else float('inf'),
                is_unlimited=is_unlimited,
                risk_level=spender_info['risk'] if not is_unlimited else 'MEDIUM' if spender_info['risk'] == 'LOW' else 'HIGH'
            )
        except Exception as e:
            return None

    def scan_approvals(
        self,
        wallet: str,
        tokens: List[str],
        spenders: Optional[List[str]] = None
    ) -> List[TokenApproval]:
        """Escanea múltiples tokens para approvals."""
        if spenders is None:
            spenders = list(self.KNOWN_SPENDERS.keys())

        approvals = []

        for token in tokens:
            for spender in spenders:
                approval = self.check_approval(wallet, token, spender)
                if approval:
                    approvals.append(approval)

        return sorted(approvals, key=lambda x: x.risk_level, reverse=True)

    def generate_revoke_data(self, token_address: str, spender: str) -> str:
        """Genera data para revocar una aprobación."""
        # approve(spender, 0)
        approve_selector = '0x095ea7b3'
        spender_padded = spender[2:].lower().zfill(64)
        amount_padded = '0' * 64

        return approve_selector + spender_padded + amount_padded

    def get_revoke_summary(self, approvals: List[TokenApproval]) -> Dict:
        """Genera resumen de aprobaciones a revocar."""
        high_risk = [a for a in approvals if a.risk_level == 'HIGH']
        unlimited = [a for a in approvals if a.is_unlimited]
        unknown = [a for a in approvals if a.spender_name == 'Unknown Contract']

        return {
            'total_approvals': len(approvals),
            'high_risk_count': len(high_risk),
            'unlimited_count': len(unlimited),
            'unknown_spenders': len(unknown),
            'recommendation': 'REVOKE IMMEDIATELY' if high_risk else
                            'REVIEW RECOMMENDED' if unlimited else 'OK',
            'high_risk_approvals': [
                {
                    'token': a.token_symbol,
                    'spender': a.spender_name,
                    'revoke_data': self.generate_revoke_data(a.token_address, a.spender)
                } for a in high_risk
            ]
        }

# Uso:
# checker = ApprovalChecker()
# tokens = ["0xToken1", "0xToken2"]
# approvals = checker.scan_approvals("0xYourWallet", tokens)
# summary = checker.get_revoke_summary(approvals)
```

---

## 📁 S05 - DEFI SCRIPTS

### S05-001: Yield Aggregator Scanner
```python
"""
CIPHER Script S05-001: Yield Aggregator Scanner
Escanea y compara yields de diferentes protocolos DeFi.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import aiohttp
import asyncio

@dataclass
class YieldOpportunity:
    """Representa una oportunidad de yield."""
    protocol: str
    chain: str
    pool: str
    apy: float
    tvl: float
    token: str
    risk_level: str
    il_risk: bool  # Impermanent Loss risk

class YieldScanner:
    """Scanner de oportunidades de yield."""

    # DefiLlama API
    DEFILLAMA_POOLS = "https://yields.llama.fi/pools"

    def __init__(self):
        self.opportunities: List[YieldOpportunity] = []

    async def fetch_yields(self) -> List[Dict]:
        """Obtiene yields de DefiLlama."""
        async with aiohttp.ClientSession() as session:
            async with session.get(self.DEFILLAMA_POOLS) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('data', [])
                return []

    def calculate_risk(self, pool: Dict) -> str:
        """Calcula nivel de riesgo de un pool."""
        risk_score = 0

        # TVL bajo = mayor riesgo
        tvl = pool.get('tvlUsd', 0)
        if tvl < 100000:
            risk_score += 30
        elif tvl < 1000000:
            risk_score += 20
        elif tvl < 10000000:
            risk_score += 10

        # APY muy alto = mayor riesgo (posible insostenible)
        apy = pool.get('apy', 0)
        if apy > 1000:
            risk_score += 40
        elif apy > 500:
            risk_score += 30
        elif apy > 100:
            risk_score += 15

        # Auditoría
        if not pool.get('audited'):
            risk_score += 20

        if risk_score >= 60:
            return 'HIGH'
        elif risk_score >= 30:
            return 'MEDIUM'
        return 'LOW'

    async def scan(
        self,
        chains: Optional[List[str]] = None,
        min_tvl: float = 100000,
        min_apy: float = 5,
        max_apy: float = 500,
        stablecoin_only: bool = False
    ) -> List[YieldOpportunity]:
        """
        Escanea oportunidades de yield.

        Args:
            chains: Lista de chains a filtrar (None = todas)
            min_tvl: TVL mínimo en USD
            min_apy: APY mínimo (%)
            max_apy: APY máximo (%) - filtrar yields insostenibles
            stablecoin_only: Solo pools de stablecoins
        """
        pools = await self.fetch_yields()

        self.opportunities = []

        for pool in pools:
            # Filtrar por chain
            chain = pool.get('chain', '').lower()
            if chains and chain not in [c.lower() for c in chains]:
                continue

            # Filtrar por TVL
            tvl = pool.get('tvlUsd', 0)
            if tvl < min_tvl:
                continue

            # Filtrar por APY
            apy = pool.get('apy', 0)
            if apy < min_apy or apy > max_apy:
                continue

            # Filtrar stablecoins
            if stablecoin_only and pool.get('stablecoin') != True:
                continue

            # Determinar riesgo de IL
            il_risk = pool.get('ilRisk') == 'yes' or pool.get('exposure') == 'multi'

            opportunity = YieldOpportunity(
                protocol=pool.get('project', 'Unknown'),
                chain=pool.get('chain', 'Unknown'),
                pool=pool.get('symbol', 'Unknown'),
                apy=round(apy, 2),
                tvl=tvl,
                token=pool.get('underlyingTokens', [pool.get('symbol', 'Unknown')])[0] if pool.get('underlyingTokens') else pool.get('symbol', 'Unknown'),
                risk_level=self.calculate_risk(pool),
                il_risk=il_risk
            )

            self.opportunities.append(opportunity)

        # Ordenar por APY descendente
        self.opportunities.sort(key=lambda x: x.apy, reverse=True)

        return self.opportunities

    def get_best_by_risk(self, risk_level: str = 'LOW') -> List[YieldOpportunity]:
        """Obtiene mejores yields por nivel de riesgo."""
        return [o for o in self.opportunities if o.risk_level == risk_level][:10]

    def get_summary(self) -> Dict:
        """Genera resumen del escaneo."""
        if not self.opportunities:
            return {'error': 'No scan performed'}

        return {
            'timestamp': datetime.now().isoformat(),
            'total_opportunities': len(self.opportunities),
            'best_apy': {
                'protocol': self.opportunities[0].protocol,
                'pool': self.opportunities[0].pool,
                'apy': self.opportunities[0].apy
            } if self.opportunities else None,
            'by_risk': {
                'low': len([o for o in self.opportunities if o.risk_level == 'LOW']),
                'medium': len([o for o in self.opportunities if o.risk_level == 'MEDIUM']),
                'high': len([o for o in self.opportunities if o.risk_level == 'HIGH'])
            },
            'chains': list(set(o.chain for o in self.opportunities)),
            'avg_apy': round(sum(o.apy for o in self.opportunities) / len(self.opportunities), 2)
        }

def scan_yields(
    chains: Optional[List[str]] = None,
    min_tvl: float = 100000,
    stablecoin_only: bool = False
) -> List[YieldOpportunity]:
    """Entry point para escaneo de yields."""
    scanner = YieldScanner()
    return asyncio.run(scanner.scan(
        chains=chains,
        min_tvl=min_tvl,
        stablecoin_only=stablecoin_only
    ))

# Uso:
# opportunities = scan_yields(chains=['ethereum', 'arbitrum'], min_tvl=500000)
# for opp in opportunities[:10]:
#     print(f"{opp.protocol} | {opp.pool} | APY: {opp.apy}% | Risk: {opp.risk_level}")
```

---

## 📁 S06 - UTILITY SCRIPTS

### S06-001: Address Book Manager
```python
"""
CIPHER Script S06-001: Address Book Manager
Gestiona direcciones conocidas con labels y categorías.
"""
import json
from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class AddressEntry:
    """Entrada en el libro de direcciones."""
    address: str
    label: str
    category: str
    chain: str
    notes: str
    added_date: str
    tags: List[str]

class AddressBook:
    """Gestor de libro de direcciones."""

    CATEGORIES = [
        'wallet',      # Wallets propias
        'exchange',    # CEX wallets
        'defi',        # Contratos DeFi
        'nft',         # Contratos NFT
        'token',       # Contratos de tokens
        'whale',       # Wallets de ballenas a seguir
        'scam',        # Direcciones scam conocidas
        'other'        # Otros
    ]

    def __init__(self, filepath: str = 'address_book.json'):
        self.filepath = Path(filepath)
        self.entries: Dict[str, AddressEntry] = {}
        self.load()

    def load(self):
        """Carga el libro de direcciones desde archivo."""
        if self.filepath.exists():
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                for addr, entry_data in data.items():
                    self.entries[addr.lower()] = AddressEntry(**entry_data)

    def save(self):
        """Guarda el libro de direcciones."""
        data = {addr: asdict(entry) for addr, entry in self.entries.items()}
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def add(
        self,
        address: str,
        label: str,
        category: str = 'other',
        chain: str = 'ethereum',
        notes: str = '',
        tags: List[str] = None
    ) -> bool:
        """Añade una dirección al libro."""
        if category not in self.CATEGORIES:
            return False

        entry = AddressEntry(
            address=address.lower(),
            label=label,
            category=category,
            chain=chain,
            notes=notes,
            added_date=datetime.now().isoformat(),
            tags=tags or []
        )

        self.entries[address.lower()] = entry
        self.save()
        return True

    def get(self, address: str) -> Optional[AddressEntry]:
        """Obtiene información de una dirección."""
        return self.entries.get(address.lower())

    def search(
        self,
        query: str = '',
        category: str = None,
        chain: str = None,
        tags: List[str] = None
    ) -> List[AddressEntry]:
        """Busca direcciones."""
        results = []

        for entry in self.entries.values():
            # Filtrar por query
            if query:
                query_lower = query.lower()
                if not (
                    query_lower in entry.label.lower() or
                    query_lower in entry.address.lower() or
                    query_lower in entry.notes.lower()
                ):
                    continue

            # Filtrar por categoría
            if category and entry.category != category:
                continue

            # Filtrar por chain
            if chain and entry.chain != chain:
                continue

            # Filtrar por tags
            if tags and not any(t in entry.tags for t in tags):
                continue

            results.append(entry)

        return results

    def remove(self, address: str) -> bool:
        """Elimina una dirección."""
        if address.lower() in self.entries:
            del self.entries[address.lower()]
            self.save()
            return True
        return False

    def export_csv(self, filepath: str):
        """Exporta el libro a CSV."""
        import csv
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Address', 'Label', 'Category', 'Chain', 'Notes', 'Tags'])
            for entry in self.entries.values():
                writer.writerow([
                    entry.address,
                    entry.label,
                    entry.category,
                    entry.chain,
                    entry.notes,
                    ','.join(entry.tags)
                ])

    def get_stats(self) -> Dict:
        """Estadísticas del libro."""
        by_category = {}
        by_chain = {}

        for entry in self.entries.values():
            by_category[entry.category] = by_category.get(entry.category, 0) + 1
            by_chain[entry.chain] = by_chain.get(entry.chain, 0) + 1

        return {
            'total_entries': len(self.entries),
            'by_category': by_category,
            'by_chain': by_chain
        }

# Uso:
# book = AddressBook()
# book.add("0x...", "Mi Wallet Principal", category="wallet", chain="ethereum", tags=["main", "trading"])
# entry = book.get("0x...")
# results = book.search(category="defi", chain="arbitrum")
```

### S06-002: Multi-Chain Explorer Links
```python
"""
CIPHER Script S06-002: Multi-Chain Explorer Links
Genera links a explorers para diferentes chains.
"""
from typing import Optional

class ExplorerLinks:
    """Generador de links a block explorers."""

    EXPLORERS = {
        'ethereum': {
            'name': 'Etherscan',
            'base': 'https://etherscan.io',
            'tx': '/tx/',
            'address': '/address/',
            'token': '/token/',
            'block': '/block/'
        },
        'polygon': {
            'name': 'Polygonscan',
            'base': 'https://polygonscan.com',
            'tx': '/tx/',
            'address': '/address/',
            'token': '/token/',
            'block': '/block/'
        },
        'arbitrum': {
            'name': 'Arbiscan',
            'base': 'https://arbiscan.io',
            'tx': '/tx/',
            'address': '/address/',
            'token': '/token/',
            'block': '/block/'
        },
        'optimism': {
            'name': 'Optimistic Etherscan',
            'base': 'https://optimistic.etherscan.io',
            'tx': '/tx/',
            'address': '/address/',
            'token': '/token/',
            'block': '/block/'
        },
        'bsc': {
            'name': 'BscScan',
            'base': 'https://bscscan.com',
            'tx': '/tx/',
            'address': '/address/',
            'token': '/token/',
            'block': '/block/'
        },
        'avalanche': {
            'name': 'Snowtrace',
            'base': 'https://snowtrace.io',
            'tx': '/tx/',
            'address': '/address/',
            'token': '/token/',
            'block': '/block/'
        },
        'fantom': {
            'name': 'FTMScan',
            'base': 'https://ftmscan.com',
            'tx': '/tx/',
            'address': '/address/',
            'token': '/token/',
            'block': '/block/'
        },
        'base': {
            'name': 'BaseScan',
            'base': 'https://basescan.org',
            'tx': '/tx/',
            'address': '/address/',
            'token': '/token/',
            'block': '/block/'
        },
        'solana': {
            'name': 'Solscan',
            'base': 'https://solscan.io',
            'tx': '/tx/',
            'address': '/account/',
            'token': '/token/',
            'block': '/block/'
        }
    }

    @classmethod
    def get_tx_link(cls, chain: str, tx_hash: str) -> Optional[str]:
        """Genera link para transacción."""
        explorer = cls.EXPLORERS.get(chain.lower())
        if not explorer:
            return None
        return f"{explorer['base']}{explorer['tx']}{tx_hash}"

    @classmethod
    def get_address_link(cls, chain: str, address: str) -> Optional[str]:
        """Genera link para dirección."""
        explorer = cls.EXPLORERS.get(chain.lower())
        if not explorer:
            return None
        return f"{explorer['base']}{explorer['address']}{address}"

    @classmethod
    def get_token_link(cls, chain: str, token_address: str) -> Optional[str]:
        """Genera link para token."""
        explorer = cls.EXPLORERS.get(chain.lower())
        if not explorer:
            return None
        return f"{explorer['base']}{explorer['token']}{token_address}"

    @classmethod
    def get_block_link(cls, chain: str, block_number: int) -> Optional[str]:
        """Genera link para bloque."""
        explorer = cls.EXPLORERS.get(chain.lower())
        if not explorer:
            return None
        return f"{explorer['base']}{explorer['block']}{block_number}"

    @classmethod
    def get_all_links(cls, chain: str, identifier: str, id_type: str = 'address') -> dict:
        """Genera todos los links relevantes."""
        explorer = cls.EXPLORERS.get(chain.lower())
        if not explorer:
            return {'error': f'Chain {chain} not supported'}

        result = {
            'chain': chain,
            'explorer': explorer['name'],
            'identifier': identifier,
            'type': id_type
        }

        if id_type == 'tx':
            result['link'] = cls.get_tx_link(chain, identifier)
        elif id_type == 'address':
            result['link'] = cls.get_address_link(chain, identifier)
        elif id_type == 'token':
            result['link'] = cls.get_token_link(chain, identifier)
        elif id_type == 'block':
            result['link'] = cls.get_block_link(chain, int(identifier))

        return result

    @classmethod
    def supported_chains(cls) -> list:
        """Lista chains soportadas."""
        return list(cls.EXPLORERS.keys())

# Uso:
# link = ExplorerLinks.get_tx_link('ethereum', '0x...')
# print(link)  # https://etherscan.io/tx/0x...
```

---

## 🔗 CONEXIONES NEURONALES

```
SCRIPTS_INDEX ←→ SKILLS_CATALOG (C30000)
     ↓
┌────┴────┐
│NEURONAS │
└────┬────┘
     │
     ├── S01 → C10000-C19999 (Blockchains)
     ├── S02 → C70001, C70002 (Trading)
     ├── S03 → C50001-C50005 (Data Analytics)
     ├── S04 → C60001 (Security)
     ├── S05 → C40001-C40006 (DeFi)
     └── S06 → Utilidades generales
```

---

## 📝 USO DE SCRIPTS

### Instalación de Dependencias
```bash
pip install web3 aiohttp numpy requests
```

### Ejecución Típica
```python
# Importar script específico
from scripts.S01_BLOCKCHAIN.balance_checker import multi_chain_balance

# Ejecutar
balances = multi_chain_balance("0xYourWallet")
```

---

## 🔐 NOTAS DE SEGURIDAD

1. **NUNCA** incluir claves privadas en scripts
2. Usar variables de entorno para API keys
3. Validar todas las direcciones antes de transacciones
4. Los scripts de análisis son READ-ONLY
5. Scripts de ejecución requieren revisión manual

---

**CIPHER v1.0.0** | Scripts Library | Ready for Execution
