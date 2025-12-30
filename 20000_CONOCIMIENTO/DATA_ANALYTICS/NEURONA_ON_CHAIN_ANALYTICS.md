# NEURONA C50001: ON-CHAIN ANALYTICS & DATA ENGINEERING

> **CIPHER**: Dominio de análisis on-chain, extracción de datos blockchain, y data pipelines.

---

## ÍNDICE

1. [Fundamentos On-Chain](#1-fundamentos-on-chain)
2. [Data Extraction](#2-data-extraction)
3. [Indexing & The Graph](#3-indexing--the-graph)
4. [Blockchain Data Pipelines](#4-blockchain-data-pipelines)
5. [Métricas On-Chain](#5-métricas-on-chain)
6. [SQL para Blockchain (Dune)](#6-sql-para-blockchain-dune)
7. [Wallet Profiling](#7-wallet-profiling)

---

## 1. FUNDAMENTOS ON-CHAIN

### 1.1 Blockchain Data Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BLOCKCHAIN DATA LAYERS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                      RAW BLOCKCHAIN DATA                             │  │
│   │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │  │
│   │  │ Blocks  │ │  Txs    │ │ Logs/   │ │ State   │ │ Traces  │       │  │
│   │  │         │ │         │ │ Events  │ │ Changes │ │         │       │  │
│   │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘       │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                  │                                          │
│                                  ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                       DECODED DATA                                   │  │
│   │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                   │  │
│   │  │ ABI-Decoded │ │  Labeled    │ │ Enriched    │                   │  │
│   │  │ Events      │ │  Addresses  │ │ Transfers   │                   │  │
│   │  └─────────────┘ └─────────────┘ └─────────────┘                   │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                  │                                          │
│                                  ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    AGGREGATED METRICS                                │  │
│   │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐           │  │
│   │  │   TVL     │ │  Volume   │ │  Revenue  │ │  Users    │           │  │
│   │  │ per Block │ │ per Hour  │ │ per Day   │ │  per Week │           │  │
│   │  └───────────┘ └───────────┘ └───────────┘ └───────────┘           │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Data Sources Comparison

```
┌────────────────────────────────────────────────────────────────────────────┐
│                     ON-CHAIN DATA SOURCES                                   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  SOURCE           │ SPEED    │ COMPLETENESS │ COST     │ EASE OF USE      │
│  ─────────────────────────────────────────────────────────────────────────│
│  Direct RPC       │ ★★★★★   │ ★★★★★       │ Variable │ ★★☆☆☆            │
│  The Graph        │ ★★★★☆   │ ★★★★☆       │ Free/Pay │ ★★★★☆            │
│  Dune Analytics   │ ★★★☆☆   │ ★★★★★       │ Free/Pay │ ★★★★★            │
│  Etherscan API    │ ★★★☆☆   │ ★★★☆☆       │ Free     │ ★★★★★            │
│  Alchemy          │ ★★★★★   │ ★★★★☆       │ Free/Pay │ ★★★★☆            │
│  Quicknode        │ ★★★★★   │ ★★★★☆       │ Paid     │ ★★★★☆            │
│  Moralis          │ ★★★★☆   │ ★★★★☆       │ Free/Pay │ ★★★★★            │
│  Covalent         │ ★★★★☆   │ ★★★★★       │ Free/Pay │ ★★★★☆            │
│  Transpose        │ ★★★★☆   │ ★★★★★       │ Free/Pay │ ★★★★☆            │
│  Nansen           │ ★★★☆☆   │ ★★★★★       │ Paid     │ ★★★★★            │
│  Flipside         │ ★★★☆☆   │ ★★★★☆       │ Free     │ ★★★★☆            │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. DATA EXTRACTION

### 2.1 Web3 Data Collector

```python
"""
CIPHER: On-Chain Data Collector
Extracción eficiente de datos blockchain
"""

from web3 import Web3
from typing import Dict, List, Optional, Generator
from dataclasses import dataclass
from datetime import datetime
import asyncio
import json

@dataclass
class BlockData:
    number: int
    timestamp: int
    hash: str
    parent_hash: str
    gas_used: int
    gas_limit: int
    base_fee: Optional[int]
    transaction_count: int
    miner: str

@dataclass
class TransactionData:
    hash: str
    block_number: int
    from_address: str
    to_address: Optional[str]
    value: int
    gas_price: int
    gas_used: int
    input_data: str
    status: bool
    logs: List[Dict]

@dataclass
class EventData:
    contract: str
    event_name: str
    block_number: int
    transaction_hash: str
    log_index: int
    args: Dict

class OnChainCollector:
    """Colector de datos on-chain"""

    def __init__(self, rpc_url: str):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.contract_abis: Dict[str, list] = {}

    def get_block(self, block_number: int) -> BlockData:
        """Obtener datos de un bloque"""
        block = self.w3.eth.get_block(block_number)

        return BlockData(
            number=block.number,
            timestamp=block.timestamp,
            hash=block.hash.hex(),
            parent_hash=block.parentHash.hex(),
            gas_used=block.gasUsed,
            gas_limit=block.gasLimit,
            base_fee=block.get('baseFeePerGas'),
            transaction_count=len(block.transactions),
            miner=block.miner
        )

    def get_transaction(self, tx_hash: str) -> TransactionData:
        """Obtener datos de una transacción"""
        tx = self.w3.eth.get_transaction(tx_hash)
        receipt = self.w3.eth.get_transaction_receipt(tx_hash)

        return TransactionData(
            hash=tx_hash,
            block_number=tx.blockNumber,
            from_address=tx['from'],
            to_address=tx.get('to'),
            value=tx.value,
            gas_price=tx.gasPrice,
            gas_used=receipt.gasUsed,
            input_data=tx.input.hex() if tx.input else '0x',
            status=receipt.status == 1,
            logs=[dict(log) for log in receipt.logs]
        )

    def get_events(
        self,
        contract_address: str,
        event_name: str,
        from_block: int,
        to_block: int,
        abi: list
    ) -> List[EventData]:
        """Obtener eventos de un contrato"""
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(contract_address),
            abi=abi
        )

        event = getattr(contract.events, event_name)

        logs = event.get_logs(
            fromBlock=from_block,
            toBlock=to_block
        )

        events = []
        for log in logs:
            events.append(EventData(
                contract=contract_address,
                event_name=event_name,
                block_number=log.blockNumber,
                transaction_hash=log.transactionHash.hex(),
                log_index=log.logIndex,
                args=dict(log.args)
            ))

        return events

    def stream_blocks(
        self,
        start_block: int,
        end_block: Optional[int] = None,
        batch_size: int = 100
    ) -> Generator[List[BlockData], None, None]:
        """Stream de bloques en batches"""
        if end_block is None:
            end_block = self.w3.eth.block_number

        current = start_block
        while current <= end_block:
            batch_end = min(current + batch_size - 1, end_block)

            blocks = []
            for block_num in range(current, batch_end + 1):
                try:
                    blocks.append(self.get_block(block_num))
                except Exception as e:
                    print(f"Error getting block {block_num}: {e}")

            yield blocks
            current = batch_end + 1

    def decode_input(
        self,
        contract_address: str,
        input_data: str,
        abi: list
    ) -> Optional[Dict]:
        """Decodificar input data de transacción"""
        if input_data == '0x' or len(input_data) < 10:
            return None

        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(contract_address),
            abi=abi
        )

        try:
            func, args = contract.decode_function_input(input_data)
            return {
                "function": func.fn_name,
                "args": dict(args)
            }
        except Exception:
            return None

    def get_token_transfers(
        self,
        token_address: str,
        from_block: int,
        to_block: int
    ) -> List[Dict]:
        """Obtener transfers de un token ERC20"""
        # Transfer event signature
        transfer_topic = self.w3.keccak(
            text="Transfer(address,address,uint256)"
        ).hex()

        logs = self.w3.eth.get_logs({
            "fromBlock": from_block,
            "toBlock": to_block,
            "address": Web3.to_checksum_address(token_address),
            "topics": [transfer_topic]
        })

        transfers = []
        for log in logs:
            from_addr = "0x" + log.topics[1].hex()[-40:]
            to_addr = "0x" + log.topics[2].hex()[-40:]
            amount = int(log.data.hex(), 16)

            transfers.append({
                "from": from_addr,
                "to": to_addr,
                "amount": amount,
                "block": log.blockNumber,
                "tx_hash": log.transactionHash.hex(),
                "log_index": log.logIndex
            })

        return transfers

    def get_internal_transactions(
        self,
        tx_hash: str
    ) -> List[Dict]:
        """Obtener transacciones internas (traces)"""
        # Requiere debug_traceTransaction o trace_transaction
        try:
            traces = self.w3.manager.request_blocking(
                "trace_transaction",
                [tx_hash]
            )

            internal_txs = []
            for trace in traces:
                if trace.get('type') == 'call':
                    internal_txs.append({
                        "from": trace['action']['from'],
                        "to": trace['action']['to'],
                        "value": int(trace['action']['value'], 16),
                        "type": trace['action']['callType'],
                        "gas_used": int(trace.get('result', {}).get('gasUsed', '0x0'), 16)
                    })

            return internal_txs
        except Exception:
            return []

    def get_state_at_block(
        self,
        contract_address: str,
        storage_slot: int,
        block_number: int
    ) -> str:
        """Leer storage de contrato en bloque específico"""
        return self.w3.eth.get_storage_at(
            Web3.to_checksum_address(contract_address),
            storage_slot,
            block_identifier=block_number
        ).hex()


class AsyncOnChainCollector:
    """Colector asíncrono para alto throughput"""

    def __init__(self, rpc_url: str, max_concurrent: int = 50):
        from web3 import AsyncWeb3, AsyncHTTPProvider

        self.w3 = AsyncWeb3(AsyncHTTPProvider(rpc_url))
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def get_blocks_batch(
        self,
        block_numbers: List[int]
    ) -> List[Dict]:
        """Obtener múltiples bloques concurrentemente"""
        async def fetch_block(block_num: int) -> Optional[Dict]:
            async with self.semaphore:
                try:
                    block = await self.w3.eth.get_block(block_num)
                    return dict(block)
                except Exception as e:
                    print(f"Error fetching block {block_num}: {e}")
                    return None

        tasks = [fetch_block(num) for num in block_numbers]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]

    async def get_logs_batch(
        self,
        contracts: List[str],
        topics: List[str],
        from_block: int,
        to_block: int
    ) -> List[Dict]:
        """Obtener logs de múltiples contratos"""
        async def fetch_logs(contract: str) -> List[Dict]:
            async with self.semaphore:
                try:
                    logs = await self.w3.eth.get_logs({
                        "fromBlock": from_block,
                        "toBlock": to_block,
                        "address": contract,
                        "topics": topics
                    })
                    return [dict(log) for log in logs]
                except Exception:
                    return []

        tasks = [fetch_logs(c) for c in contracts]
        results = await asyncio.gather(*tasks)

        all_logs = []
        for logs in results:
            all_logs.extend(logs)
        return all_logs
```

---

## 3. INDEXING & THE GRAPH

### 3.1 Subgraph Schema

```graphql
# schema.graphql para The Graph

type Token @entity {
  id: ID!
  symbol: String!
  name: String!
  decimals: Int!
  totalSupply: BigInt!
  holders: [TokenBalance!]! @derivedFrom(field: "token")
  transfers: [Transfer!]! @derivedFrom(field: "token")
}

type Account @entity {
  id: ID!
  balances: [TokenBalance!]! @derivedFrom(field: "account")
  transfersFrom: [Transfer!]! @derivedFrom(field: "from")
  transfersTo: [Transfer!]! @derivedFrom(field: "to")
  firstSeenBlock: BigInt!
  lastActiveBlock: BigInt!
  totalTransactions: BigInt!
}

type TokenBalance @entity {
  id: ID!  # token-account
  token: Token!
  account: Account!
  amount: BigInt!
  lastUpdatedBlock: BigInt!
}

type Transfer @entity {
  id: ID!  # tx-logIndex
  token: Token!
  from: Account!
  to: Account!
  amount: BigInt!
  timestamp: BigInt!
  blockNumber: BigInt!
  transactionHash: Bytes!
}

type DailyStats @entity {
  id: ID!  # date
  date: BigInt!
  totalTransfers: BigInt!
  totalVolume: BigInt!
  uniqueSenders: BigInt!
  uniqueReceivers: BigInt!
  averageTransferSize: BigDecimal!
}

type Pool @entity {
  id: ID!
  token0: Token!
  token1: Token!
  reserve0: BigInt!
  reserve1: BigInt!
  totalLiquidity: BigInt!
  swaps: [Swap!]! @derivedFrom(field: "pool")
  liquidityEvents: [LiquidityEvent!]! @derivedFrom(field: "pool")
}

type Swap @entity {
  id: ID!
  pool: Pool!
  sender: Account!
  amountIn: BigInt!
  amountOut: BigInt!
  tokenIn: Token!
  tokenOut: Token!
  timestamp: BigInt!
  transactionHash: Bytes!
}

type LiquidityEvent @entity {
  id: ID!
  pool: Pool!
  provider: Account!
  type: String!  # "add" or "remove"
  amount0: BigInt!
  amount1: BigInt!
  liquidity: BigInt!
  timestamp: BigInt!
}
```

### 3.2 Subgraph Mapping

```typescript
// mapping.ts para The Graph

import { BigInt, Address, log } from "@graphprotocol/graph-ts"
import {
  Transfer as TransferEvent,
  Approval as ApprovalEvent
} from "../generated/Token/Token"
import {
  Token,
  Account,
  TokenBalance,
  Transfer,
  DailyStats
} from "../generated/schema"

// Constantes
let ZERO_BI = BigInt.fromI32(0)
let ONE_BI = BigInt.fromI32(1)
let ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

// Helper: obtener o crear token
function getOrCreateToken(address: Address): Token {
  let id = address.toHexString()
  let token = Token.load(id)

  if (token == null) {
    token = new Token(id)
    // Llamar al contrato para obtener metadata
    // let contract = TokenContract.bind(address)
    // token.symbol = contract.symbol()
    // token.name = contract.name()
    // token.decimals = contract.decimals()
    token.symbol = "UNKNOWN"
    token.name = "Unknown Token"
    token.decimals = 18
    token.totalSupply = ZERO_BI
    token.save()
  }

  return token as Token
}

// Helper: obtener o crear cuenta
function getOrCreateAccount(address: Address, blockNumber: BigInt): Account {
  let id = address.toHexString()
  let account = Account.load(id)

  if (account == null) {
    account = new Account(id)
    account.firstSeenBlock = blockNumber
    account.lastActiveBlock = blockNumber
    account.totalTransactions = ZERO_BI
    account.save()
  }

  return account as Account
}

// Helper: obtener o crear balance
function getOrCreateBalance(token: Token, account: Account): TokenBalance {
  let id = token.id + "-" + account.id
  let balance = TokenBalance.load(id)

  if (balance == null) {
    balance = new TokenBalance(id)
    balance.token = token.id
    balance.account = account.id
    balance.amount = ZERO_BI
    balance.lastUpdatedBlock = ZERO_BI
    balance.save()
  }

  return balance as TokenBalance
}

// Helper: actualizar stats diarios
function updateDailyStats(timestamp: BigInt, volume: BigInt): void {
  let dayId = timestamp.toI32() / 86400
  let id = dayId.toString()
  let stats = DailyStats.load(id)

  if (stats == null) {
    stats = new DailyStats(id)
    stats.date = BigInt.fromI32(dayId * 86400)
    stats.totalTransfers = ZERO_BI
    stats.totalVolume = ZERO_BI
    stats.uniqueSenders = ZERO_BI
    stats.uniqueReceivers = ZERO_BI
  }

  stats.totalTransfers = stats.totalTransfers.plus(ONE_BI)
  stats.totalVolume = stats.totalVolume.plus(volume)
  stats.save()
}

// Handler principal para Transfer
export function handleTransfer(event: TransferEvent): void {
  let token = getOrCreateToken(event.address)
  let from = getOrCreateAccount(event.params.from, event.block.number)
  let to = getOrCreateAccount(event.params.to, event.block.number)

  // Actualizar cuentas
  from.lastActiveBlock = event.block.number
  from.totalTransactions = from.totalTransactions.plus(ONE_BI)
  from.save()

  to.lastActiveBlock = event.block.number
  to.totalTransactions = to.totalTransactions.plus(ONE_BI)
  to.save()

  // Actualizar balances
  let fromBalance = getOrCreateBalance(token, from)
  let toBalance = getOrCreateBalance(token, to)

  // Si es mint (from = 0x0)
  if (event.params.from.toHexString() == ZERO_ADDRESS) {
    token.totalSupply = token.totalSupply.plus(event.params.value)
    token.save()
  } else {
    fromBalance.amount = fromBalance.amount.minus(event.params.value)
    fromBalance.lastUpdatedBlock = event.block.number
    fromBalance.save()
  }

  // Si es burn (to = 0x0)
  if (event.params.to.toHexString() == ZERO_ADDRESS) {
    token.totalSupply = token.totalSupply.minus(event.params.value)
    token.save()
  } else {
    toBalance.amount = toBalance.amount.plus(event.params.value)
    toBalance.lastUpdatedBlock = event.block.number
    toBalance.save()
  }

  // Crear entidad Transfer
  let transferId = event.transaction.hash.toHexString() + "-" + event.logIndex.toString()
  let transfer = new Transfer(transferId)
  transfer.token = token.id
  transfer.from = from.id
  transfer.to = to.id
  transfer.amount = event.params.value
  transfer.timestamp = event.block.timestamp
  transfer.blockNumber = event.block.number
  transfer.transactionHash = event.transaction.hash
  transfer.save()

  // Actualizar stats
  updateDailyStats(event.block.timestamp, event.params.value)

  log.info("Transfer: {} from {} to {} amount {}", [
    transferId,
    from.id,
    to.id,
    event.params.value.toString()
  ])
}
```

### 3.3 Querying The Graph

```python
"""
CIPHER: The Graph Query Client
Cliente para consultar subgraphs
"""

import requests
from typing import Dict, List, Optional
from dataclasses import dataclass

class SubgraphClient:
    """Cliente para consultar subgraphs de The Graph"""

    def __init__(self, subgraph_url: str):
        self.url = subgraph_url

    def query(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """Ejecutar query GraphQL"""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        response = requests.post(self.url, json=payload)
        response.raise_for_status()

        result = response.json()
        if "errors" in result:
            raise Exception(f"GraphQL errors: {result['errors']}")

        return result["data"]

    def get_token_holders(
        self,
        token_id: str,
        min_balance: int = 0,
        first: int = 100,
        skip: int = 0
    ) -> List[Dict]:
        """Obtener holders de un token"""
        query = """
        query getHolders($tokenId: String!, $minBalance: BigInt!, $first: Int!, $skip: Int!) {
          tokenBalances(
            where: {
              token: $tokenId,
              amount_gt: $minBalance
            },
            orderBy: amount,
            orderDirection: desc,
            first: $first,
            skip: $skip
          ) {
            account {
              id
            }
            amount
            lastUpdatedBlock
          }
        }
        """

        result = self.query(query, {
            "tokenId": token_id,
            "minBalance": str(min_balance),
            "first": first,
            "skip": skip
        })

        return result["tokenBalances"]

    def get_recent_transfers(
        self,
        token_id: str,
        min_amount: int = 0,
        first: int = 100
    ) -> List[Dict]:
        """Obtener transfers recientes"""
        query = """
        query getTransfers($tokenId: String!, $minAmount: BigInt!, $first: Int!) {
          transfers(
            where: {
              token: $tokenId,
              amount_gt: $minAmount
            },
            orderBy: timestamp,
            orderDirection: desc,
            first: $first
          ) {
            id
            from {
              id
            }
            to {
              id
            }
            amount
            timestamp
            transactionHash
          }
        }
        """

        return self.query(query, {
            "tokenId": token_id,
            "minAmount": str(min_amount),
            "first": first
        })["transfers"]

    def get_daily_stats(
        self,
        days: int = 30
    ) -> List[Dict]:
        """Obtener estadísticas diarias"""
        query = """
        query getDailyStats($first: Int!) {
          dailyStats(
            orderBy: date,
            orderDirection: desc,
            first: $first
          ) {
            id
            date
            totalTransfers
            totalVolume
            uniqueSenders
            uniqueReceivers
          }
        }
        """

        return self.query(query, {"first": days})["dailyStats"]

    def get_whale_movements(
        self,
        token_id: str,
        min_amount: int,
        hours: int = 24
    ) -> List[Dict]:
        """Detectar movimientos de ballenas"""
        import time
        timestamp_cutoff = int(time.time()) - (hours * 3600)

        query = """
        query getWhaleMovements(
          $tokenId: String!,
          $minAmount: BigInt!,
          $timestamp: BigInt!
        ) {
          transfers(
            where: {
              token: $tokenId,
              amount_gt: $minAmount,
              timestamp_gt: $timestamp
            },
            orderBy: amount,
            orderDirection: desc,
            first: 100
          ) {
            id
            from {
              id
              totalTransactions
            }
            to {
              id
              totalTransactions
            }
            amount
            timestamp
            transactionHash
          }
        }
        """

        return self.query(query, {
            "tokenId": token_id,
            "minAmount": str(min_amount),
            "timestamp": str(timestamp_cutoff)
        })["transfers"]


# Subgraphs comunes
SUBGRAPH_URLS = {
    "uniswap_v2": "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2",
    "uniswap_v3": "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3",
    "aave_v2": "https://api.thegraph.com/subgraphs/name/aave/protocol-v2",
    "compound": "https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2",
    "curve": "https://api.thegraph.com/subgraphs/name/curvefi/curve",
    "balancer_v2": "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-v2",
}


# Ejemplo de uso
if __name__ == "__main__":
    # Query Uniswap V3
    client = SubgraphClient(SUBGRAPH_URLS["uniswap_v3"])

    # Obtener pools más líquidos
    query = """
    {
      pools(
        first: 10,
        orderBy: totalValueLockedUSD,
        orderDirection: desc
      ) {
        id
        token0 {
          symbol
        }
        token1 {
          symbol
        }
        feeTier
        totalValueLockedUSD
        volumeUSD
      }
    }
    """

    result = client.query(query)
    for pool in result["pools"]:
        print(f"{pool['token0']['symbol']}/{pool['token1']['symbol']}: ${float(pool['totalValueLockedUSD']):,.0f} TVL")
```

---

## 4. BLOCKCHAIN DATA PIPELINES

### 4.1 ETL Pipeline Architecture

```python
"""
CIPHER: Blockchain ETL Pipeline
Pipeline para extracción, transformación y carga de datos on-chain
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Generator, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio
import json

@dataclass
class PipelineConfig:
    chain: str
    rpc_url: str
    start_block: int
    end_block: int
    batch_size: int = 1000
    output_format: str = "parquet"  # json, csv, parquet
    output_path: str = "./data"

class DataExtractor(ABC):
    """Base class para extractores de datos"""

    @abstractmethod
    def extract(self, block_range: tuple) -> Generator[Dict, None, None]:
        pass

class DataTransformer(ABC):
    """Base class para transformadores"""

    @abstractmethod
    def transform(self, data: Dict) -> Dict:
        pass

class DataLoader(ABC):
    """Base class para loaders"""

    @abstractmethod
    def load(self, data: List[Dict]) -> None:
        pass


class BlockExtractor(DataExtractor):
    """Extractor de bloques"""

    def __init__(self, collector):
        self.collector = collector

    def extract(self, block_range: tuple) -> Generator[Dict, None, None]:
        start, end = block_range

        for blocks in self.collector.stream_blocks(start, end):
            for block in blocks:
                yield {
                    "block_number": block.number,
                    "timestamp": block.timestamp,
                    "datetime": datetime.fromtimestamp(block.timestamp).isoformat(),
                    "hash": block.hash,
                    "parent_hash": block.parent_hash,
                    "gas_used": block.gas_used,
                    "gas_limit": block.gas_limit,
                    "base_fee": block.base_fee,
                    "tx_count": block.transaction_count,
                    "miner": block.miner
                }


class EventExtractor(DataExtractor):
    """Extractor de eventos de contratos"""

    def __init__(self, collector, contract_address: str, event_name: str, abi: list):
        self.collector = collector
        self.contract = contract_address
        self.event_name = event_name
        self.abi = abi

    def extract(self, block_range: tuple) -> Generator[Dict, None, None]:
        start, end = block_range

        events = self.collector.get_events(
            self.contract,
            self.event_name,
            start,
            end,
            self.abi
        )

        for event in events:
            yield {
                "contract": event.contract,
                "event": event.event_name,
                "block_number": event.block_number,
                "tx_hash": event.transaction_hash,
                "log_index": event.log_index,
                **event.args
            }


class DeFiTransformer(DataTransformer):
    """Transformador para datos DeFi"""

    def __init__(self, token_decimals: Dict[str, int]):
        self.decimals = token_decimals

    def transform(self, data: Dict) -> Dict:
        transformed = data.copy()

        # Normalizar cantidades de tokens
        for key in ['amount', 'amount0', 'amount1', 'value']:
            if key in transformed and 'token' in transformed:
                token = transformed['token']
                decimals = self.decimals.get(token, 18)
                transformed[f'{key}_normalized'] = transformed[key] / (10 ** decimals)

        # Agregar campos calculados
        if 'timestamp' in transformed:
            dt = datetime.fromtimestamp(transformed['timestamp'])
            transformed['date'] = dt.strftime('%Y-%m-%d')
            transformed['hour'] = dt.hour
            transformed['day_of_week'] = dt.weekday()

        return transformed


class ParquetLoader(DataLoader):
    """Loader para formato Parquet"""

    def __init__(self, output_path: str, partition_cols: List[str] = None):
        self.output_path = output_path
        self.partition_cols = partition_cols or ['date']

    def load(self, data: List[Dict]) -> None:
        import pandas as pd
        import pyarrow as pa
        import pyarrow.parquet as pq

        df = pd.DataFrame(data)

        table = pa.Table.from_pandas(df)

        pq.write_to_dataset(
            table,
            root_path=self.output_path,
            partition_cols=self.partition_cols
        )


class BigQueryLoader(DataLoader):
    """Loader para Google BigQuery"""

    def __init__(self, project_id: str, dataset: str, table: str):
        from google.cloud import bigquery
        self.client = bigquery.Client(project=project_id)
        self.table_id = f"{project_id}.{dataset}.{table}"

    def load(self, data: List[Dict]) -> None:
        errors = self.client.insert_rows_json(self.table_id, data)
        if errors:
            raise Exception(f"BigQuery errors: {errors}")


class ETLPipeline:
    """Pipeline ETL completo"""

    def __init__(
        self,
        extractor: DataExtractor,
        transformers: List[DataTransformer],
        loader: DataLoader,
        config: PipelineConfig
    ):
        self.extractor = extractor
        self.transformers = transformers
        self.loader = loader
        self.config = config

    def run(self) -> Dict:
        """Ejecutar pipeline"""
        stats = {
            "records_extracted": 0,
            "records_loaded": 0,
            "errors": 0,
            "start_time": datetime.now().isoformat()
        }

        buffer = []

        for record in self.extractor.extract(
            (self.config.start_block, self.config.end_block)
        ):
            stats["records_extracted"] += 1

            # Apply transformations
            for transformer in self.transformers:
                record = transformer.transform(record)

            buffer.append(record)

            # Flush buffer
            if len(buffer) >= self.config.batch_size:
                try:
                    self.loader.load(buffer)
                    stats["records_loaded"] += len(buffer)
                except Exception as e:
                    stats["errors"] += 1
                    print(f"Load error: {e}")

                buffer = []

        # Flush remaining
        if buffer:
            try:
                self.loader.load(buffer)
                stats["records_loaded"] += len(buffer)
            except Exception as e:
                stats["errors"] += 1

        stats["end_time"] = datetime.now().isoformat()
        return stats


# Ejemplo de uso
async def run_pipeline_example():
    from pathlib import Path

    # Configuración
    config = PipelineConfig(
        chain="ethereum",
        rpc_url="https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY",
        start_block=18000000,
        end_block=18001000,
        batch_size=100,
        output_path="./blockchain_data"
    )

    # Inicializar collector
    collector = OnChainCollector(config.rpc_url)

    # Crear pipeline para bloques
    pipeline = ETLPipeline(
        extractor=BlockExtractor(collector),
        transformers=[],
        loader=ParquetLoader(config.output_path),
        config=config
    )

    # Ejecutar
    stats = pipeline.run()
    print(f"Pipeline completed: {stats}")
```

---

## 5. MÉTRICAS ON-CHAIN

### 5.1 Key Metrics Calculator

```python
"""
CIPHER: On-Chain Metrics Calculator
Cálculo de métricas fundamentales on-chain
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import statistics

@dataclass
class NetworkMetrics:
    # Activity
    daily_transactions: int
    daily_active_addresses: int
    new_addresses: int
    transaction_volume_usd: float

    # Fees
    avg_gas_price_gwei: float
    total_fees_eth: float
    total_fees_usd: float

    # Block metrics
    avg_block_time: float
    avg_block_size: int
    avg_gas_used_per_block: int

@dataclass
class TokenMetrics:
    price_usd: float
    market_cap: float
    fully_diluted_valuation: float
    circulating_supply: float
    total_supply: float

    # On-chain
    holder_count: int
    transfer_count_24h: int
    transfer_volume_24h: float
    unique_senders_24h: int
    unique_receivers_24h: int

    # Distribution
    top_10_percentage: float
    top_100_percentage: float
    gini_coefficient: float

class OnChainMetricsCalculator:
    """Calculador de métricas on-chain"""

    def calculate_nvt_ratio(
        self,
        market_cap: float,
        daily_volume_usd: float
    ) -> float:
        """
        NVT Ratio (Network Value to Transactions)
        - Similar al P/E ratio para stocks
        - Alto NVT = overvalued o hodling
        - Bajo NVT = undervalued o alta actividad
        """
        if daily_volume_usd == 0:
            return float('inf')

        # Anualizar volumen
        annual_volume = daily_volume_usd * 365

        return market_cap / annual_volume

    def calculate_mvrv_ratio(
        self,
        market_cap: float,
        realized_cap: float
    ) -> float:
        """
        MVRV (Market Value to Realized Value)
        - > 3.5: Posible top
        - < 1: Posible bottom
        - Realized cap = suma de (coins * precio al que se movieron por última vez)
        """
        if realized_cap == 0:
            return 0

        return market_cap / realized_cap

    def calculate_sopr(
        self,
        spent_outputs: List[Tuple[float, float]]  # (price_bought, price_sold)
    ) -> float:
        """
        SOPR (Spent Output Profit Ratio)
        - > 1: Outputs en profit
        - < 1: Outputs en loss
        - = 1: Breakeven
        """
        if not spent_outputs:
            return 1

        total_bought = sum(bought for bought, _ in spent_outputs)
        total_sold = sum(sold for _, sold in spent_outputs)

        if total_bought == 0:
            return 1

        return total_sold / total_bought

    def calculate_holder_distribution(
        self,
        balances: List[float]
    ) -> Dict:
        """Calcular distribución de holders"""
        if not balances:
            return {}

        total = sum(balances)
        sorted_balances = sorted(balances, reverse=True)

        # Percentiles
        top_10_sum = sum(sorted_balances[:10])
        top_100_sum = sum(sorted_balances[:100])

        # Gini coefficient
        n = len(balances)
        if n == 0 or total == 0:
            gini = 0
        else:
            sorted_asc = sorted(balances)
            cumulative = 0
            gini_sum = 0
            for i, balance in enumerate(sorted_asc):
                cumulative += balance
                gini_sum += cumulative
            gini = (n + 1 - 2 * gini_sum / total) / n

        return {
            "total_holders": len(balances),
            "total_supply": total,
            "top_10_percentage": (top_10_sum / total * 100) if total > 0 else 0,
            "top_100_percentage": (top_100_sum / total * 100) if total > 0 else 0,
            "gini_coefficient": gini,
            "median_balance": statistics.median(balances) if balances else 0,
            "average_balance": statistics.mean(balances) if balances else 0
        }

    def calculate_exchange_flow(
        self,
        exchange_inflows: float,
        exchange_outflows: float
    ) -> Dict:
        """Calcular flujo de exchanges"""
        net_flow = exchange_inflows - exchange_outflows

        return {
            "inflows": exchange_inflows,
            "outflows": exchange_outflows,
            "net_flow": net_flow,
            "sentiment": "BEARISH" if net_flow > 0 else "BULLISH",
            "flow_ratio": exchange_inflows / exchange_outflows if exchange_outflows > 0 else float('inf')
        }

    def calculate_active_address_ratio(
        self,
        daily_active: int,
        total_addresses: int
    ) -> float:
        """Ratio de direcciones activas"""
        if total_addresses == 0:
            return 0
        return daily_active / total_addresses

    def calculate_velocity(
        self,
        transfer_volume: float,
        circulating_supply: float,
        days: int = 1
    ) -> float:
        """
        Velocidad del token
        - Alta velocidad = alta utilización
        - Baja velocidad = holding/staking
        """
        if circulating_supply == 0:
            return 0

        return (transfer_volume / circulating_supply) / days

    def calculate_stock_to_flow(
        self,
        circulating_supply: float,
        annual_production: float
    ) -> float:
        """
        Stock-to-Flow ratio
        - Usado principalmente para BTC
        - Mayor S2F = mayor escasez
        """
        if annual_production == 0:
            return float('inf')

        return circulating_supply / annual_production

    def calculate_realized_cap(
        self,
        utxos: List[Tuple[float, float]]  # (amount, last_price)
    ) -> float:
        """
        Realized Cap
        - Suma de (coins * precio al que se movieron)
        """
        return sum(amount * price for amount, price in utxos)

    def calculate_stablecoin_supply_ratio(
        self,
        btc_market_cap: float,
        total_stablecoin_supply: float
    ) -> float:
        """
        SSR (Stablecoin Supply Ratio)
        - Bajo SSR = mucho poder de compra esperando
        - Alto SSR = poco poder de compra disponible
        """
        if total_stablecoin_supply == 0:
            return float('inf')

        return btc_market_cap / total_stablecoin_supply

    def generate_health_report(
        self,
        token_metrics: TokenMetrics,
        network_metrics: NetworkMetrics
    ) -> Dict:
        """Generar reporte de salud del token"""
        # Calcular métricas derivadas
        nvt = self.calculate_nvt_ratio(
            token_metrics.market_cap,
            token_metrics.transfer_volume_24h * token_metrics.price_usd
        )

        velocity = self.calculate_velocity(
            token_metrics.transfer_volume_24h,
            token_metrics.circulating_supply
        )

        active_ratio = self.calculate_active_address_ratio(
            token_metrics.unique_senders_24h + token_metrics.unique_receivers_24h,
            token_metrics.holder_count
        )

        # Scoring
        score = 0

        # NVT scoring (lower is better for activity)
        if nvt < 50:
            score += 25
        elif nvt < 100:
            score += 15
        elif nvt < 200:
            score += 5

        # Distribution scoring (lower concentration is better)
        if token_metrics.top_10_percentage < 30:
            score += 25
        elif token_metrics.top_10_percentage < 50:
            score += 15
        elif token_metrics.top_10_percentage < 70:
            score += 5

        # Velocity scoring
        if 0.01 <= velocity <= 0.1:
            score += 25
        elif velocity > 0:
            score += 10

        # Active ratio scoring
        if active_ratio > 0.1:
            score += 25
        elif active_ratio > 0.05:
            score += 15
        elif active_ratio > 0.01:
            score += 5

        return {
            "health_score": score,
            "rating": "HEALTHY" if score >= 70 else "MODERATE" if score >= 40 else "WEAK",
            "metrics": {
                "nvt_ratio": nvt,
                "velocity": velocity,
                "active_address_ratio": active_ratio,
                "holder_count": token_metrics.holder_count,
                "top_10_concentration": token_metrics.top_10_percentage,
                "gini_coefficient": token_metrics.gini_coefficient
            },
            "signals": self._generate_signals(nvt, velocity, token_metrics)
        }

    def _generate_signals(
        self,
        nvt: float,
        velocity: float,
        metrics: TokenMetrics
    ) -> List[str]:
        """Generar señales basadas en métricas"""
        signals = []

        if nvt > 200:
            signals.append("HIGH_NVT: Low network activity relative to valuation")
        elif nvt < 30:
            signals.append("LOW_NVT: High network activity, potentially undervalued")

        if velocity > 0.2:
            signals.append("HIGH_VELOCITY: Tokens changing hands frequently")
        elif velocity < 0.01:
            signals.append("LOW_VELOCITY: Strong holding behavior")

        if metrics.top_10_percentage > 60:
            signals.append("HIGH_CONCENTRATION: Whale risk")

        if metrics.gini_coefficient > 0.8:
            signals.append("UNEQUAL_DISTRIBUTION: Very concentrated ownership")

        return signals


# Ejemplo de uso
if __name__ == "__main__":
    calculator = OnChainMetricsCalculator()

    # Simular métricas
    token_metrics = TokenMetrics(
        price_usd=1.50,
        market_cap=500_000_000,
        fully_diluted_valuation=800_000_000,
        circulating_supply=333_333_333,
        total_supply=500_000_000,
        holder_count=25_000,
        transfer_count_24h=5_000,
        transfer_volume_24h=10_000_000,
        unique_senders_24h=2_000,
        unique_receivers_24h=2_500,
        top_10_percentage=35.0,
        top_100_percentage=55.0,
        gini_coefficient=0.72
    )

    network_metrics = NetworkMetrics(
        daily_transactions=1_200_000,
        daily_active_addresses=500_000,
        new_addresses=50_000,
        transaction_volume_usd=5_000_000_000,
        avg_gas_price_gwei=25.0,
        total_fees_eth=2_500,
        total_fees_usd=5_000_000,
        avg_block_time=12.1,
        avg_block_size=85_000,
        avg_gas_used_per_block=15_000_000
    )

    report = calculator.generate_health_report(token_metrics, network_metrics)
    print(f"Health Score: {report['health_score']}/100 ({report['rating']})")
    print(f"Signals: {report['signals']}")
```

---

## 6. SQL PARA BLOCKCHAIN (DUNE)

### 6.1 Dune Analytics Queries

```sql
-- =============================================================================
-- CIPHER: Dune Analytics Query Collection
-- Queries SQL para análisis on-chain en Dune
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. TOP HOLDERS DE UN TOKEN
-- -----------------------------------------------------------------------------
WITH token_balances AS (
    SELECT
        "to" AS address,
        SUM(CAST(value AS DECIMAL(38,0))) / 1e18 AS received
    FROM erc20_ethereum.evt_Transfer
    WHERE contract_address = 0xYOUR_TOKEN_ADDRESS
    GROUP BY "to"
),
sent AS (
    SELECT
        "from" AS address,
        SUM(CAST(value AS DECIMAL(38,0))) / 1e18 AS sent
    FROM erc20_ethereum.evt_Transfer
    WHERE contract_address = 0xYOUR_TOKEN_ADDRESS
    GROUP BY "from"
)
SELECT
    COALESCE(r.address, s.address) AS holder,
    COALESCE(r.received, 0) - COALESCE(s.sent, 0) AS balance,
    (COALESCE(r.received, 0) - COALESCE(s.sent, 0)) * 100.0 /
        (SELECT SUM(CAST(value AS DECIMAL(38,0))) / 1e18
         FROM erc20_ethereum.evt_Transfer
         WHERE contract_address = 0xYOUR_TOKEN_ADDRESS
         AND "from" = 0x0000000000000000000000000000000000000000) AS percentage
FROM token_balances r
FULL OUTER JOIN sent s ON r.address = s.address
WHERE COALESCE(r.received, 0) - COALESCE(s.sent, 0) > 0
ORDER BY balance DESC
LIMIT 100;

-- -----------------------------------------------------------------------------
-- 2. VOLUMEN DIARIO DE UN DEX
-- -----------------------------------------------------------------------------
SELECT
    DATE_TRUNC('day', block_time) AS day,
    COUNT(DISTINCT tx_hash) AS trades,
    COUNT(DISTINCT trader_a) AS unique_traders,
    SUM(token_a_amount_raw / 1e18 * p.price) AS volume_usd
FROM dex.trades
LEFT JOIN prices.usd p
    ON dex.trades.token_a_address = p.contract_address
    AND DATE_TRUNC('minute', dex.trades.block_time) = p.minute
WHERE
    project = 'uniswap'
    AND version = '3'
    AND block_time >= NOW() - INTERVAL '30 days'
GROUP BY 1
ORDER BY 1 DESC;

-- -----------------------------------------------------------------------------
-- 3. WHALE MOVEMENTS (Transfers > $1M)
-- -----------------------------------------------------------------------------
WITH large_transfers AS (
    SELECT
        t.block_time,
        t."from",
        t."to",
        t.value / 1e18 AS amount,
        (t.value / 1e18) * p.price AS value_usd,
        t.contract_address AS token,
        tx.hash AS tx_hash
    FROM erc20_ethereum.evt_Transfer t
    JOIN ethereum.transactions tx ON t.evt_tx_hash = tx.hash
    LEFT JOIN prices.usd p
        ON t.contract_address = p.contract_address
        AND DATE_TRUNC('minute', t.block_time) = p.minute
    WHERE
        t.block_time >= NOW() - INTERVAL '24 hours'
        AND (t.value / 1e18) * p.price > 1000000  -- $1M+
)
SELECT
    block_time,
    "from",
    "to",
    amount,
    value_usd,
    token,
    tx_hash,
    -- Etiquetar direcciones conocidas
    CASE
        WHEN "from" IN (SELECT address FROM labels.all WHERE name LIKE '%exchange%')
        THEN 'Exchange'
        ELSE 'Unknown'
    END AS from_label,
    CASE
        WHEN "to" IN (SELECT address FROM labels.all WHERE name LIKE '%exchange%')
        THEN 'Exchange'
        ELSE 'Unknown'
    END AS to_label
FROM large_transfers
ORDER BY value_usd DESC;

-- -----------------------------------------------------------------------------
-- 4. EXCHANGE NETFLOW
-- -----------------------------------------------------------------------------
WITH exchange_addresses AS (
    SELECT DISTINCT address
    FROM labels.all
    WHERE category = 'exchange'
),
inflows AS (
    SELECT
        DATE_TRUNC('hour', block_time) AS hour,
        SUM(value / 1e18) AS inflow
    FROM erc20_ethereum.evt_Transfer
    WHERE
        "to" IN (SELECT address FROM exchange_addresses)
        AND contract_address = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2  -- WETH
        AND block_time >= NOW() - INTERVAL '7 days'
    GROUP BY 1
),
outflows AS (
    SELECT
        DATE_TRUNC('hour', block_time) AS hour,
        SUM(value / 1e18) AS outflow
    FROM erc20_ethereum.evt_Transfer
    WHERE
        "from" IN (SELECT address FROM exchange_addresses)
        AND contract_address = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2  -- WETH
        AND block_time >= NOW() - INTERVAL '7 days'
    GROUP BY 1
)
SELECT
    COALESCE(i.hour, o.hour) AS hour,
    COALESCE(i.inflow, 0) AS inflow,
    COALESCE(o.outflow, 0) AS outflow,
    COALESCE(i.inflow, 0) - COALESCE(o.outflow, 0) AS netflow,
    SUM(COALESCE(i.inflow, 0) - COALESCE(o.outflow, 0))
        OVER (ORDER BY COALESCE(i.hour, o.hour)) AS cumulative_netflow
FROM inflows i
FULL OUTER JOIN outflows o ON i.hour = o.hour
ORDER BY hour;

-- -----------------------------------------------------------------------------
-- 5. PROTOCOL REVENUE
-- -----------------------------------------------------------------------------
SELECT
    DATE_TRUNC('day', block_time) AS day,
    project,
    SUM(
        CASE
            WHEN token_a_address = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
            THEN token_a_amount_raw * 0.003 / 1e18 * p.price  -- 0.3% fee
            ELSE token_b_amount_raw * 0.003 / 1e18 * p2.price
        END
    ) AS fees_usd
FROM dex.trades
LEFT JOIN prices.usd p
    ON 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 = p.contract_address
    AND DATE_TRUNC('minute', block_time) = p.minute
LEFT JOIN prices.usd p2
    ON dex.trades.token_b_address = p2.contract_address
    AND DATE_TRUNC('minute', block_time) = p2.minute
WHERE
    block_time >= NOW() - INTERVAL '30 days'
    AND project IN ('uniswap', 'sushiswap', 'curve')
GROUP BY 1, 2
ORDER BY 1 DESC, fees_usd DESC;

-- -----------------------------------------------------------------------------
-- 6. NEW vs RETURNING USERS
-- -----------------------------------------------------------------------------
WITH first_interaction AS (
    SELECT
        "from" AS user,
        MIN(DATE_TRUNC('day', block_time)) AS first_day
    FROM ethereum.transactions
    WHERE
        "to" = 0xYOUR_PROTOCOL_ADDRESS
        AND block_time >= NOW() - INTERVAL '90 days'
    GROUP BY 1
),
daily_users AS (
    SELECT
        DATE_TRUNC('day', block_time) AS day,
        "from" AS user
    FROM ethereum.transactions
    WHERE
        "to" = 0xYOUR_PROTOCOL_ADDRESS
        AND block_time >= NOW() - INTERVAL '30 days'
    GROUP BY 1, 2
)
SELECT
    d.day,
    COUNT(DISTINCT d.user) AS total_users,
    COUNT(DISTINCT CASE WHEN f.first_day = d.day THEN d.user END) AS new_users,
    COUNT(DISTINCT CASE WHEN f.first_day < d.day THEN d.user END) AS returning_users,
    CAST(COUNT(DISTINCT CASE WHEN f.first_day < d.day THEN d.user END) AS FLOAT) /
        NULLIF(COUNT(DISTINCT d.user), 0) * 100 AS retention_rate
FROM daily_users d
JOIN first_interaction f ON d.user = f.user
GROUP BY 1
ORDER BY 1 DESC;

-- -----------------------------------------------------------------------------
-- 7. GAS ANALYSIS
-- -----------------------------------------------------------------------------
SELECT
    DATE_TRUNC('hour', block_time) AS hour,
    AVG(gas_price / 1e9) AS avg_gas_gwei,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY gas_price / 1e9) AS median_gas_gwei,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY gas_price / 1e9) AS p95_gas_gwei,
    SUM(gas_used * gas_price / 1e18) AS total_eth_spent,
    COUNT(*) AS tx_count
FROM ethereum.transactions
WHERE block_time >= NOW() - INTERVAL '24 hours'
GROUP BY 1
ORDER BY 1;

-- -----------------------------------------------------------------------------
-- 8. SMART MONEY TRACKING
-- -----------------------------------------------------------------------------
WITH smart_money_wallets AS (
    -- Wallets conocidos de smart money (ejemplo)
    SELECT address FROM (VALUES
        (0x1234...),  -- Fund 1
        (0x5678...)   -- Fund 2
    ) AS t(address)
),
smart_money_trades AS (
    SELECT
        DATE_TRUNC('day', block_time) AS day,
        token_bought_address AS token,
        SUM(amount_usd) AS buy_volume
    FROM dex.trades
    WHERE
        trader_a IN (SELECT address FROM smart_money_wallets)
        AND block_time >= NOW() - INTERVAL '7 days'
    GROUP BY 1, 2
)
SELECT
    day,
    token,
    t.symbol,
    buy_volume,
    -- Comparar con volumen total del token
    buy_volume / NULLIF(total_vol.total, 0) * 100 AS pct_of_total_volume
FROM smart_money_trades smt
LEFT JOIN tokens.erc20 t ON smt.token = t.contract_address
LEFT JOIN (
    SELECT
        token_bought_address,
        SUM(amount_usd) AS total
    FROM dex.trades
    WHERE block_time >= NOW() - INTERVAL '7 days'
    GROUP BY 1
) total_vol ON smt.token = total_vol.token_bought_address
ORDER BY buy_volume DESC;
```

---

## 7. WALLET PROFILING

### 7.1 Wallet Analysis System

```python
"""
CIPHER: Wallet Profiling System
Análisis y clasificación de wallets blockchain
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime, timedelta

class WalletType(Enum):
    WHALE = "whale"
    SMART_MONEY = "smart_money"
    DEX_TRADER = "dex_trader"
    NFT_COLLECTOR = "nft_collector"
    DEFI_USER = "defi_user"
    BOT = "bot"
    EXCHANGE = "exchange"
    CONTRACT = "contract"
    DORMANT = "dormant"
    RETAIL = "retail"

@dataclass
class WalletProfile:
    address: str
    wallet_type: WalletType
    confidence: float  # 0-1

    # Activity metrics
    first_seen: datetime
    last_active: datetime
    total_transactions: int
    unique_contracts_interacted: int

    # Financial metrics
    total_value_usd: float
    realized_pnl: float
    unrealized_pnl: float

    # Behavioral
    avg_hold_time_days: float
    trading_frequency: float  # Trades per day
    preferred_protocols: List[str]

    # Risk profile
    risk_score: float  # 0-100

class WalletProfiler:
    """Sistema de perfilado de wallets"""

    def __init__(self, data_collector):
        self.collector = data_collector

        # Known addresses
        self.exchange_addresses: set = set()
        self.known_bots: set = set()
        self.labeled_wallets: Dict[str, str] = {}

    def profile_wallet(self, address: str) -> WalletProfile:
        """Generar perfil completo de wallet"""
        # Obtener datos
        transactions = self._get_wallet_transactions(address)
        token_balances = self._get_token_balances(address)
        defi_positions = self._get_defi_positions(address)
        nft_holdings = self._get_nft_holdings(address)

        # Clasificar tipo
        wallet_type, confidence = self._classify_wallet(
            address, transactions, token_balances, nft_holdings
        )

        # Calcular métricas
        activity = self._calculate_activity_metrics(transactions)
        financial = self._calculate_financial_metrics(
            token_balances, defi_positions, transactions
        )
        behavioral = self._calculate_behavioral_metrics(transactions)

        return WalletProfile(
            address=address,
            wallet_type=wallet_type,
            confidence=confidence,
            first_seen=activity["first_seen"],
            last_active=activity["last_active"],
            total_transactions=activity["total_tx"],
            unique_contracts_interacted=activity["unique_contracts"],
            total_value_usd=financial["total_value"],
            realized_pnl=financial["realized_pnl"],
            unrealized_pnl=financial["unrealized_pnl"],
            avg_hold_time_days=behavioral["avg_hold_time"],
            trading_frequency=behavioral["trading_frequency"],
            preferred_protocols=behavioral["preferred_protocols"],
            risk_score=self._calculate_risk_score(
                wallet_type, financial, behavioral
            )
        )

    def _classify_wallet(
        self,
        address: str,
        transactions: List[Dict],
        balances: List[Dict],
        nfts: List[Dict]
    ) -> tuple:
        """Clasificar tipo de wallet"""
        scores = {wt: 0.0 for wt in WalletType}

        # Check known addresses
        if address.lower() in self.exchange_addresses:
            return WalletType.EXCHANGE, 1.0

        if address.lower() in self.known_bots:
            return WalletType.BOT, 0.9

        # Check if contract
        # if self.collector.w3.eth.get_code(address) != b'':
        #     return WalletType.CONTRACT, 1.0

        # Analyze transaction patterns
        if transactions:
            tx_count = len(transactions)
            unique_days = len(set(tx['date'] for tx in transactions))

            # High frequency = possible bot
            if tx_count > 100 and tx_count / max(unique_days, 1) > 50:
                scores[WalletType.BOT] += 0.5

            # Check for DEX interactions
            dex_contracts = {'uniswap', 'sushiswap', '1inch', 'curve'}
            dex_interactions = sum(
                1 for tx in transactions
                if any(dex in tx.get('to_label', '').lower() for dex in dex_contracts)
            )
            if dex_interactions > tx_count * 0.3:
                scores[WalletType.DEX_TRADER] += 0.4

            # Check for DeFi interactions
            defi_protocols = {'aave', 'compound', 'maker', 'yearn'}
            defi_interactions = sum(
                1 for tx in transactions
                if any(p in tx.get('to_label', '').lower() for p in defi_protocols)
            )
            if defi_interactions > tx_count * 0.2:
                scores[WalletType.DEFI_USER] += 0.4

        # Check balances for whale status
        total_usd = sum(b.get('value_usd', 0) for b in balances)
        if total_usd > 1_000_000:
            scores[WalletType.WHALE] += 0.5
        elif total_usd > 10_000:
            scores[WalletType.RETAIL] += 0.3

        # Check NFT holdings
        if len(nfts) > 10:
            scores[WalletType.NFT_COLLECTOR] += 0.4

        # Check for dormancy
        if transactions:
            last_tx_date = max(tx['date'] for tx in transactions)
            if (datetime.now() - last_tx_date).days > 180:
                scores[WalletType.DORMANT] += 0.6

        # Find best match
        best_type = max(scores, key=scores.get)
        confidence = scores[best_type]

        # Default to retail if no strong signal
        if confidence < 0.3:
            return WalletType.RETAIL, 0.5

        return best_type, min(confidence, 1.0)

    def _calculate_activity_metrics(self, transactions: List[Dict]) -> Dict:
        """Calcular métricas de actividad"""
        if not transactions:
            return {
                "first_seen": None,
                "last_active": None,
                "total_tx": 0,
                "unique_contracts": 0
            }

        dates = [tx['date'] for tx in transactions]
        contracts = set(tx.get('to', '') for tx in transactions)

        return {
            "first_seen": min(dates),
            "last_active": max(dates),
            "total_tx": len(transactions),
            "unique_contracts": len(contracts)
        }

    def _calculate_financial_metrics(
        self,
        balances: List[Dict],
        defi_positions: List[Dict],
        transactions: List[Dict]
    ) -> Dict:
        """Calcular métricas financieras"""
        total_value = sum(b.get('value_usd', 0) for b in balances)
        total_value += sum(p.get('value_usd', 0) for p in defi_positions)

        # Calcular PnL (simplificado)
        realized_pnl = 0
        for tx in transactions:
            if tx.get('type') == 'swap':
                realized_pnl += tx.get('pnl', 0)

        return {
            "total_value": total_value,
            "realized_pnl": realized_pnl,
            "unrealized_pnl": 0  # Requiere cálculo más complejo
        }

    def _calculate_behavioral_metrics(self, transactions: List[Dict]) -> Dict:
        """Calcular métricas de comportamiento"""
        if not transactions:
            return {
                "avg_hold_time": 0,
                "trading_frequency": 0,
                "preferred_protocols": []
            }

        # Trading frequency
        if len(transactions) > 1:
            date_range = (
                max(tx['date'] for tx in transactions) -
                min(tx['date'] for tx in transactions)
            ).days
            freq = len(transactions) / max(date_range, 1)
        else:
            freq = 0

        # Preferred protocols
        protocol_counts: Dict[str, int] = {}
        for tx in transactions:
            protocol = tx.get('to_label', 'unknown')
            protocol_counts[protocol] = protocol_counts.get(protocol, 0) + 1

        top_protocols = sorted(
            protocol_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return {
            "avg_hold_time": 0,  # Requiere análisis de transfers
            "trading_frequency": freq,
            "preferred_protocols": [p[0] for p in top_protocols]
        }

    def _calculate_risk_score(
        self,
        wallet_type: WalletType,
        financial: Dict,
        behavioral: Dict
    ) -> float:
        """Calcular score de riesgo (para contrapartes)"""
        score = 50  # Base

        # Wallet type adjustments
        type_scores = {
            WalletType.EXCHANGE: -20,
            WalletType.SMART_MONEY: -10,
            WalletType.WHALE: 0,
            WalletType.BOT: +20,
            WalletType.CONTRACT: +10,
            WalletType.DORMANT: +30,
            WalletType.RETAIL: 0
        }
        score += type_scores.get(wallet_type, 0)

        # Financial adjustments
        if financial["total_value"] < 1000:
            score += 20  # Low value = higher risk
        elif financial["total_value"] > 100_000:
            score -= 10

        # Behavioral adjustments
        if behavioral["trading_frequency"] > 10:
            score += 10  # Very high frequency = suspicious

        return max(0, min(100, score))

    def _get_wallet_transactions(self, address: str) -> List[Dict]:
        """Obtener transacciones de wallet"""
        # Implementar con data collector
        return []

    def _get_token_balances(self, address: str) -> List[Dict]:
        """Obtener balances de tokens"""
        return []

    def _get_defi_positions(self, address: str) -> List[Dict]:
        """Obtener posiciones DeFi"""
        return []

    def _get_nft_holdings(self, address: str) -> List[Dict]:
        """Obtener NFTs"""
        return []

    def find_similar_wallets(
        self,
        address: str,
        top_n: int = 10
    ) -> List[str]:
        """Encontrar wallets con comportamiento similar"""
        # Implementar clustering o similarity search
        pass

    def detect_wallet_clusters(
        self,
        addresses: List[str]
    ) -> List[List[str]]:
        """Detectar clusters de wallets relacionados"""
        # Analizar:
        # - Funding sources comunes
        # - Timing de transacciones
        # - Contratos interactuados
        # - Patrones de gas
        pass
```

---

## CONEXIONES NEURALES

```
NEURONA_ON_CHAIN_ANALYTICS (C50001)
├── DEPENDE DE
│   ├── NEURONA_BLOCKCHAINS (C20001-C20012) - Chain specifics
│   └── NEURONA_SMART_CONTRACTS (C30001) - ABI decoding
│
├── CONECTA CON
│   ├── NEURONA_PROTOCOL_ANALYSIS (C40010) - Protocol metrics
│   ├── NEURONA_MARKET_DATA (C50002) - Price data
│   └── NEURONA_TRADING (C70001) - Trading signals
│
└── HABILITA
    ├── Extracción de datos blockchain
    ├── Indexación y subgraphs
    ├── Análisis de métricas on-chain
    └── Perfilado de wallets
```

---

## FIRMA CIPHER

```
╔═══════════════════════════════════════════════════════════════╗
║  NEURONA: C50001                                              ║
║  TIPO: On-Chain Analytics & Data Engineering                  ║
║  VERSIÓN: 1.0.0                                               ║
║  ESTADO: ACTIVA                                               ║
║                                                               ║
║  "La blockchain es el libro contable más transparente        ║
║   jamás creado. Solo hay que saber leerlo."                  ║
║                                                               ║
║  CIPHER_CORE::ON_CHAIN_ANALYTICS::INITIALIZED                 ║
╚═══════════════════════════════════════════════════════════════╝
```
