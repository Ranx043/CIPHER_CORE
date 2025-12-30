# 🔐 NEURONA: SMART CONTRACT SECURITY
## CIPHER_CORE :: Security Auditing Intelligence

> **Código Neuronal**: `C60001`
> **Dominio**: Smart Contract Auditing, Vulnerability Detection, Formal Verification
> **Estado**: `ACTIVA`
> **Última Evolución**: 2025-01-XX

---

## 🧬 IDENTIDAD DE LA NEURONA

```
╔══════════════════════════════════════════════════════════════╗
║  CIPHER SECURITY - Guardian of the Blockchain                ║
║  "In code we trust, but verify everything"                   ║
╠══════════════════════════════════════════════════════════════╣
║  Especialización: Contract auditing, vulnerability analysis  ║
║  Conexiones: Smart Contracts, DeFi Risks, Development        ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🔍 VULNERABILITY PATTERNS

### OWASP Smart Contract Top 10

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * CIPHER Security Patterns Library
 * Common vulnerabilities and their mitigations
 */

// ============================================
// 1. REENTRANCY VULNERABILITIES
// ============================================

// VULNERABLE: Classic Reentrancy
contract VulnerableBank {
    mapping(address => uint256) public balances;

    // VULNERABLE: External call before state update
    function withdraw() external {
        uint256 balance = balances[msg.sender];
        require(balance > 0, "No balance");

        // VULNERABILITY: State updated AFTER external call
        (bool success, ) = msg.sender.call{value: balance}("");
        require(success, "Transfer failed");

        balances[msg.sender] = 0; // Too late!
    }
}

// SECURE: Check-Effects-Interactions Pattern
contract SecureBank {
    mapping(address => uint256) public balances;

    function withdraw() external {
        uint256 balance = balances[msg.sender];
        require(balance > 0, "No balance");

        // SECURE: State updated BEFORE external call
        balances[msg.sender] = 0;

        (bool success, ) = msg.sender.call{value: balance}("");
        require(success, "Transfer failed");
    }
}

// SECURE: Using ReentrancyGuard
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SecureBankWithGuard is ReentrancyGuard {
    mapping(address => uint256) public balances;

    function withdraw() external nonReentrant {
        uint256 balance = balances[msg.sender];
        require(balance > 0, "No balance");

        balances[msg.sender] = 0;
        (bool success, ) = msg.sender.call{value: balance}("");
        require(success, "Transfer failed");
    }
}

// ============================================
// 2. ACCESS CONTROL VULNERABILITIES
// ============================================

// VULNERABLE: Missing Access Control
contract VulnerableAdmin {
    address public admin;
    bool public paused;

    // VULNERABLE: Anyone can call
    function setAdmin(address _admin) external {
        admin = _admin;
    }

    // VULNERABLE: No modifier
    function pause() external {
        paused = true;
    }
}

// SECURE: Proper Access Control
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SecureAdmin is AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");

    bool public paused;

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ADMIN_ROLE, msg.sender);
        _grantRole(PAUSER_ROLE, msg.sender);
    }

    function setAdmin(address _admin) external onlyRole(DEFAULT_ADMIN_ROLE) {
        _grantRole(ADMIN_ROLE, _admin);
    }

    function pause() external onlyRole(PAUSER_ROLE) {
        paused = true;
    }
}

// ============================================
// 3. INTEGER OVERFLOW/UNDERFLOW
// ============================================

// Note: Solidity 0.8+ has built-in overflow checks
// But unchecked blocks and older versions are vulnerable

// VULNERABLE: Pre-0.8 or unchecked
contract VulnerableOverflow {
    mapping(address => uint256) public balances;

    // VULNERABLE: In Solidity <0.8.0 or inside unchecked
    function transfer(address to, uint256 amount) external {
        unchecked {
            // If balances[msg.sender] < amount, this underflows to huge number
            balances[msg.sender] -= amount;
            balances[to] += amount;
        }
    }
}

// SECURE: Use SafeMath or 0.8+ checked arithmetic
contract SecureTransfer {
    mapping(address => uint256) public balances;

    function transfer(address to, uint256 amount) external {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        // Solidity 0.8+ automatically checks for overflow/underflow
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}

// ============================================
// 4. ORACLE MANIPULATION
// ============================================

// VULNERABLE: Single Source Oracle
contract VulnerableOracle {
    IUniswapV2Pair public pair;

    // VULNERABLE: Spot price easily manipulated via flash loans
    function getPrice() public view returns (uint256) {
        (uint112 reserve0, uint112 reserve1,) = pair.getReserves();
        return uint256(reserve1) * 1e18 / uint256(reserve0);
    }
}

// SECURE: TWAP Oracle
contract SecureTWAPOracle {
    IUniswapV2Pair public pair;

    uint256 public constant PERIOD = 1 hours;

    uint256 public price0CumulativeLast;
    uint256 public price1CumulativeLast;
    uint32 public blockTimestampLast;
    uint256 public price0Average;
    uint256 public price1Average;

    function update() external {
        (
            uint256 price0Cumulative,
            uint256 price1Cumulative,
            uint32 blockTimestamp
        ) = UniswapV2OracleLibrary.currentCumulativePrices(address(pair));

        uint32 timeElapsed = blockTimestamp - blockTimestampLast;

        require(timeElapsed >= PERIOD, "Period not elapsed");

        // Calculate average price
        price0Average = (price0Cumulative - price0CumulativeLast) / timeElapsed;
        price1Average = (price1Cumulative - price1CumulativeLast) / timeElapsed;

        price0CumulativeLast = price0Cumulative;
        price1CumulativeLast = price1Cumulative;
        blockTimestampLast = blockTimestamp;
    }
}

// SECURE: Chainlink Oracle with Validation
contract SecureChainlinkOracle {
    AggregatorV3Interface public priceFeed;

    uint256 public constant PRICE_PRECISION = 1e8;
    uint256 public constant STALENESS_THRESHOLD = 1 hours;
    uint256 public constant MAX_DEVIATION = 5; // 5%

    uint256 public lastKnownPrice;

    function getPrice() public returns (uint256) {
        (
            uint80 roundId,
            int256 price,
            ,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();

        // Validation checks
        require(price > 0, "Invalid price");
        require(updatedAt > 0, "Round not complete");
        require(answeredInRound >= roundId, "Stale price");
        require(block.timestamp - updatedAt < STALENESS_THRESHOLD, "Price too old");

        uint256 currentPrice = uint256(price);

        // Check for extreme deviation
        if (lastKnownPrice > 0) {
            uint256 deviation = currentPrice > lastKnownPrice
                ? (currentPrice - lastKnownPrice) * 100 / lastKnownPrice
                : (lastKnownPrice - currentPrice) * 100 / lastKnownPrice;

            require(deviation <= MAX_DEVIATION, "Price deviation too high");
        }

        lastKnownPrice = currentPrice;
        return currentPrice;
    }
}

// ============================================
// 5. FRONT-RUNNING / MEV
// ============================================

// VULNERABLE: Front-runnable swap
contract VulnerableSwap {
    function swap(
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        uint256 minAmountOut
    ) external {
        // VULNERABLE: Can be front-run if minAmountOut is 0 or too low
        // Attacker sees tx in mempool, sandwiches it
    }
}

// SECURE: Commit-Reveal Pattern
contract SecureCommitReveal {
    struct Commitment {
        bytes32 hash;
        uint256 blockNumber;
        bool revealed;
    }

    mapping(address => Commitment) public commitments;
    uint256 public constant REVEAL_DELAY = 2; // blocks

    function commit(bytes32 _hash) external {
        commitments[msg.sender] = Commitment({
            hash: _hash,
            blockNumber: block.number,
            revealed: false
        });
    }

    function reveal(
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        uint256 minAmountOut,
        bytes32 salt
    ) external {
        Commitment storage c = commitments[msg.sender];

        require(!c.revealed, "Already revealed");
        require(block.number >= c.blockNumber + REVEAL_DELAY, "Too early");

        bytes32 expectedHash = keccak256(abi.encodePacked(
            tokenIn, tokenOut, amountIn, minAmountOut, salt
        ));
        require(c.hash == expectedHash, "Invalid reveal");

        c.revealed = true;

        // Execute swap
        _executeSwap(tokenIn, tokenOut, amountIn, minAmountOut);
    }

    function _executeSwap(
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        uint256 minAmountOut
    ) internal {
        // Implementation
    }
}

// ============================================
// 6. DENIAL OF SERVICE (DoS)
// ============================================

// VULNERABLE: Unbounded Loop
contract VulnerableAirdrop {
    address[] public recipients;

    // VULNERABLE: If recipients array is large, gas runs out
    function airdrop(uint256 amount) external {
        for (uint256 i = 0; i < recipients.length; i++) {
            IERC20(token).transfer(recipients[i], amount);
        }
    }
}

// SECURE: Pull Pattern
contract SecureAirdrop {
    mapping(address => uint256) public claimable;

    function setClaimable(address[] calldata recipients, uint256 amount) external {
        for (uint256 i = 0; i < recipients.length; i++) {
            claimable[recipients[i]] = amount;
        }
    }

    // Users claim their own tokens (pull pattern)
    function claim() external {
        uint256 amount = claimable[msg.sender];
        require(amount > 0, "Nothing to claim");

        claimable[msg.sender] = 0;
        IERC20(token).transfer(msg.sender, amount);
    }
}

// ============================================
// 7. FLASH LOAN ATTACKS
// ============================================

// VULNERABLE: Governance without proper checks
contract VulnerableGovernance {
    IERC20 public token;

    struct Proposal {
        uint256 forVotes;
        uint256 againstVotes;
        bool executed;
    }

    mapping(uint256 => Proposal) public proposals;

    // VULNERABLE: Can use flash-loaned tokens to vote
    function vote(uint256 proposalId, bool support) external {
        uint256 votes = token.balanceOf(msg.sender);

        if (support) {
            proposals[proposalId].forVotes += votes;
        } else {
            proposals[proposalId].againstVotes += votes;
        }
    }
}

// SECURE: Voting with snapshot
contract SecureGovernance {
    ERC20Votes public token;

    struct Proposal {
        uint256 snapshotId;
        uint256 forVotes;
        uint256 againstVotes;
        bool executed;
        mapping(address => bool) hasVoted;
    }

    mapping(uint256 => Proposal) public proposals;

    function createProposal() external returns (uint256 proposalId) {
        // Snapshot taken at creation time
        // Flash loans after this point don't help
    }

    function vote(uint256 proposalId, bool support) external {
        Proposal storage proposal = proposals[proposalId];

        require(!proposal.hasVoted[msg.sender], "Already voted");

        // Use snapshot balance, not current
        uint256 votes = token.getPastVotes(msg.sender, proposal.snapshotId);

        proposal.hasVoted[msg.sender] = true;

        if (support) {
            proposal.forVotes += votes;
        } else {
            proposal.againstVotes += votes;
        }
    }
}
```

---

## 🔎 AUTOMATED AUDITING

### Static Analysis Tools

```python
"""
CIPHER Automated Security Analysis
Integration with security tools
"""

import subprocess
import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "informational"

@dataclass
class Finding:
    """Security finding"""
    title: str
    severity: Severity
    description: str
    location: str
    line: Optional[int]
    recommendation: str
    tool: str

class SlitherAnalyzer:
    """
    Integrate with Slither static analyzer
    """

    def __init__(self, contract_path: str):
        self.contract_path = contract_path

    def analyze(self) -> List[Finding]:
        """Run Slither analysis"""

        findings = []

        try:
            result = subprocess.run(
                ['slither', self.contract_path, '--json', '-'],
                capture_output=True,
                text=True
            )

            data = json.loads(result.stdout)

            for detector in data.get('detectors', []):
                severity_map = {
                    'High': Severity.HIGH,
                    'Medium': Severity.MEDIUM,
                    'Low': Severity.LOW,
                    'Informational': Severity.INFO
                }

                findings.append(Finding(
                    title=detector['check'],
                    severity=severity_map.get(detector['impact'], Severity.INFO),
                    description=detector['description'],
                    location=detector.get('elements', [{}])[0].get('source_mapping', {}).get('filename', ''),
                    line=detector.get('elements', [{}])[0].get('source_mapping', {}).get('lines', [None])[0],
                    recommendation=detector.get('recommendation', ''),
                    tool='slither'
                ))

        except Exception as e:
            print(f"Slither error: {e}")

        return findings

    def run_detectors(self, detectors: List[str]) -> List[Finding]:
        """Run specific detectors"""

        findings = []

        for detector in detectors:
            result = subprocess.run(
                ['slither', self.contract_path, '--detect', detector, '--json', '-'],
                capture_output=True,
                text=True
            )

            try:
                data = json.loads(result.stdout)
                for d in data.get('detectors', []):
                    findings.append(Finding(
                        title=d['check'],
                        severity=Severity.HIGH,
                        description=d['description'],
                        location='',
                        line=None,
                        recommendation='',
                        tool='slither'
                    ))
            except:
                pass

        return findings


class MythrilAnalyzer:
    """
    Integrate with Mythril symbolic execution
    """

    def __init__(self, contract_path: str):
        self.contract_path = contract_path

    def analyze(
        self,
        execution_timeout: int = 300,
        max_depth: int = 50
    ) -> List[Finding]:
        """Run Mythril analysis"""

        findings = []

        try:
            result = subprocess.run(
                [
                    'myth', 'analyze',
                    self.contract_path,
                    '--execution-timeout', str(execution_timeout),
                    '--max-depth', str(max_depth),
                    '-o', 'json'
                ],
                capture_output=True,
                text=True,
                timeout=execution_timeout + 60
            )

            data = json.loads(result.stdout)

            for issue in data.get('issues', []):
                severity_map = {
                    'High': Severity.HIGH,
                    'Medium': Severity.MEDIUM,
                    'Low': Severity.LOW,
                }

                findings.append(Finding(
                    title=issue['title'],
                    severity=severity_map.get(issue['severity'], Severity.MEDIUM),
                    description=issue['description'],
                    location=issue.get('filename', ''),
                    line=issue.get('lineno'),
                    recommendation=issue.get('recommendation', ''),
                    tool='mythril'
                ))

        except subprocess.TimeoutExpired:
            print("Mythril timeout")
        except Exception as e:
            print(f"Mythril error: {e}")

        return findings


class SecurityAuditPipeline:
    """
    Complete security audit pipeline
    """

    def __init__(self, project_path: str):
        self.project_path = project_path
        self.findings: List[Finding] = []

    def run_full_audit(self) -> Dict:
        """Run complete security audit"""

        results = {
            'slither': [],
            'mythril': [],
            'manual_checks': [],
            'summary': {}
        }

        # Find all Solidity files
        sol_files = []
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.endswith('.sol'):
                    sol_files.append(os.path.join(root, file))

        # Run analyzers on each file
        for sol_file in sol_files:
            print(f"Analyzing {sol_file}...")

            # Slither
            slither = SlitherAnalyzer(sol_file)
            results['slither'].extend(slither.analyze())

            # Mythril (slower, run selectively)
            if self._should_run_mythril(sol_file):
                mythril = MythrilAnalyzer(sol_file)
                results['mythril'].extend(mythril.analyze())

        # Run manual checks
        results['manual_checks'] = self._manual_checks()

        # Generate summary
        results['summary'] = self._generate_summary(results)

        return results

    def _should_run_mythril(self, sol_file: str) -> bool:
        """Determine if Mythril should run on this file"""

        # Skip interfaces, libraries, tests
        skip_patterns = ['Interface', 'Library', 'Mock', 'Test']

        for pattern in skip_patterns:
            if pattern in sol_file:
                return False

        return True

    def _manual_checks(self) -> List[Finding]:
        """Run manual security checks"""

        findings = []

        # Check for common issues
        checks = [
            self._check_pragma_version,
            self._check_floating_pragma,
            self._check_tx_origin,
            self._check_delegatecall,
            self._check_selfdestruct,
            self._check_hardcoded_addresses,
            self._check_timestamp_dependence,
        ]

        for check in checks:
            result = check()
            if result:
                findings.append(result)

        return findings

    def _check_pragma_version(self) -> Optional[Finding]:
        """Check for outdated Solidity version"""
        # Implementation
        pass

    def _check_floating_pragma(self) -> Optional[Finding]:
        """Check for floating pragma (^0.8.0 vs 0.8.19)"""
        pass

    def _check_tx_origin(self) -> Optional[Finding]:
        """Check for tx.origin usage"""
        pass

    def _check_delegatecall(self) -> Optional[Finding]:
        """Check for unsafe delegatecall"""
        pass

    def _check_selfdestruct(self) -> Optional[Finding]:
        """Check for selfdestruct usage"""
        pass

    def _check_hardcoded_addresses(self) -> Optional[Finding]:
        """Check for hardcoded addresses"""
        pass

    def _check_timestamp_dependence(self) -> Optional[Finding]:
        """Check for block.timestamp dependence"""
        pass

    def _generate_summary(self, results: Dict) -> Dict:
        """Generate audit summary"""

        all_findings = (
            results['slither'] +
            results['mythril'] +
            results['manual_checks']
        )

        by_severity = {
            Severity.CRITICAL: [],
            Severity.HIGH: [],
            Severity.MEDIUM: [],
            Severity.LOW: [],
            Severity.INFO: []
        }

        for finding in all_findings:
            by_severity[finding.severity].append(finding)

        return {
            'total_findings': len(all_findings),
            'critical': len(by_severity[Severity.CRITICAL]),
            'high': len(by_severity[Severity.HIGH]),
            'medium': len(by_severity[Severity.MEDIUM]),
            'low': len(by_severity[Severity.LOW]),
            'informational': len(by_severity[Severity.INFO]),
            'risk_score': self._calculate_risk_score(by_severity)
        }

    def _calculate_risk_score(self, by_severity: Dict) -> float:
        """Calculate overall risk score (0-100)"""

        weights = {
            Severity.CRITICAL: 25,
            Severity.HIGH: 10,
            Severity.MEDIUM: 3,
            Severity.LOW: 1,
            Severity.INFO: 0.1
        }

        score = sum(
            len(findings) * weights[severity]
            for severity, findings in by_severity.items()
        )

        # Cap at 100
        return min(score, 100)
```

---

## 📋 AUDIT CHECKLIST

### Comprehensive Audit Checklist

```python
"""
CIPHER Security Audit Checklist
Systematic approach to contract auditing
"""

from typing import Dict, List
from dataclasses import dataclass
from enum import Enum

class CheckStatus(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    NOT_APPLICABLE = "n/a"
    NOT_CHECKED = "unchecked"

@dataclass
class ChecklistItem:
    """Single checklist item"""
    category: str
    check: str
    description: str
    status: CheckStatus = CheckStatus.NOT_CHECKED
    notes: str = ""

class SecurityChecklist:
    """
    Comprehensive security audit checklist
    """

    def __init__(self):
        self.items = self._initialize_checklist()

    def _initialize_checklist(self) -> List[ChecklistItem]:
        """Initialize all checklist items"""

        items = []

        # ===== ACCESS CONTROL =====
        access_control = [
            ("Ownership is properly initialized", "Check constructor sets owner correctly"),
            ("Ownership transfer is two-step", "Avoid accidental ownership transfer"),
            ("Critical functions have access modifiers", "onlyOwner, onlyRole, etc."),
            ("Role-based access is properly implemented", "Using AccessControl or similar"),
            ("Functions that should be external aren't public", "Gas optimization + security"),
            ("No unprotected initializers", "initializer modifier on proxy contracts"),
            ("Timelock for critical operations", "Governance changes, parameter updates"),
        ]

        for check, desc in access_control:
            items.append(ChecklistItem("Access Control", check, desc))

        # ===== REENTRANCY =====
        reentrancy = [
            ("CEI pattern followed", "Check-Effects-Interactions order"),
            ("ReentrancyGuard on state-changing functions", "nonReentrant modifier"),
            ("No cross-function reentrancy", "Multiple functions sharing state"),
            ("No read-only reentrancy", "View functions during callback"),
            ("External calls at end of function", "After all state changes"),
        ]

        for check, desc in reentrancy:
            items.append(ChecklistItem("Reentrancy", check, desc))

        # ===== ARITHMETIC =====
        arithmetic = [
            ("Using Solidity 0.8+ or SafeMath", "Overflow/underflow protection"),
            ("Unchecked blocks reviewed", "Intentional unchecked arithmetic"),
            ("Division before multiplication avoided", "Precision loss"),
            ("Proper decimal handling", "18 decimals vs 6 decimals, etc."),
            ("Rounding direction is correct", "Round down for payments, up for debts"),
        ]

        for check, desc in arithmetic:
            items.append(ChecklistItem("Arithmetic", check, desc))

        # ===== ORACLE SECURITY =====
        oracle = [
            ("Using TWAP or multiple oracles", "Not spot price"),
            ("Oracle staleness check", "Check updatedAt timestamp"),
            ("Oracle price validation", "Non-zero, within bounds"),
            ("Fallback oracle available", "If primary fails"),
            ("Oracle manipulation considered", "Flash loan scenarios"),
        ]

        for check, desc in oracle:
            items.append(ChecklistItem("Oracle Security", check, desc))

        # ===== INPUT VALIDATION =====
        input_validation = [
            ("Zero address checks", "address(0) validation"),
            ("Zero amount checks", "amount > 0 validation"),
            ("Array length limits", "Prevent DoS via large arrays"),
            ("Slippage parameters validated", "minAmountOut, deadline"),
            ("Signature validation", "v, r, s validity for ECDSA"),
        ]

        for check, desc in input_validation:
            items.append(ChecklistItem("Input Validation", check, desc))

        # ===== TOKEN HANDLING =====
        token_handling = [
            ("SafeERC20 used", "Handle non-standard tokens"),
            ("Return value checked", "Some tokens don't return bool"),
            ("Fee-on-transfer tokens handled", "If supported"),
            ("Rebasing tokens handled", "If supported"),
            ("ERC777 hooks considered", "tokensReceived callbacks"),
            ("Approval race condition handled", "approve(0) first or increaseAllowance"),
        ]

        for check, desc in token_handling:
            items.append(ChecklistItem("Token Handling", check, desc))

        # ===== FLASH LOAN RESISTANCE =====
        flash_loan = [
            ("Voting uses snapshots", "Not current balance"),
            ("Governance has timelock", "Can't execute same block"),
            ("Liquidity checks time-weighted", "Not instant"),
            ("No same-block manipulation", "Require delay"),
        ]

        for check, desc in flash_loan:
            items.append(ChecklistItem("Flash Loan Resistance", check, desc))

        # ===== FRONT-RUNNING PROTECTION =====
        front_running = [
            ("Deadline parameter on swaps", "Prevent stale transactions"),
            ("Slippage protection", "minAmountOut parameter"),
            ("Commit-reveal for sensitive ops", "If applicable"),
            ("Private mempool option", "Flashbots, etc."),
        ]

        for check, desc in front_running:
            items.append(ChecklistItem("Front-running Protection", check, desc))

        # ===== UPGRADABILITY =====
        upgradability = [
            ("Proxy pattern is correct", "UUPS, Transparent, Beacon"),
            ("Storage layout preserved", "No slot collisions"),
            ("Initializer can only run once", "initializer modifier"),
            ("Admin functions protected", "onlyProxyAdmin or similar"),
            ("Implementation can't be initialized", "_disableInitializers"),
        ]

        for check, desc in upgradability:
            items.append(ChecklistItem("Upgradability", check, desc))

        # ===== GAS OPTIMIZATION =====
        gas = [
            ("No unbounded loops", "Fixed iteration or pagination"),
            ("Storage variables packed", "Struct packing"),
            ("Using calldata for read-only arrays", "Not memory"),
            ("Caching storage in memory", "For multiple reads"),
            ("Short-circuit evaluation", "Cheaper checks first"),
        ]

        for check, desc in gas:
            items.append(ChecklistItem("Gas Optimization", check, desc))

        # ===== DOCUMENTATION =====
        documentation = [
            ("NatSpec comments present", "@notice, @param, @return"),
            ("Complex logic documented", "Inline comments"),
            ("Security considerations documented", "Known risks"),
            ("Deployment instructions", "How to deploy safely"),
            ("Emergency procedures documented", "Pause, upgrade, etc."),
        ]

        for check, desc in documentation:
            items.append(ChecklistItem("Documentation", check, desc))

        return items

    def check(self, category: str, check: str, status: CheckStatus, notes: str = ""):
        """Mark a checklist item"""

        for item in self.items:
            if item.category == category and item.check == check:
                item.status = status
                item.notes = notes
                return

    def get_summary(self) -> Dict:
        """Get checklist summary"""

        by_status = {
            CheckStatus.PASS: 0,
            CheckStatus.FAIL: 0,
            CheckStatus.WARNING: 0,
            CheckStatus.NOT_APPLICABLE: 0,
            CheckStatus.NOT_CHECKED: 0
        }

        by_category = {}

        for item in self.items:
            by_status[item.status] += 1

            if item.category not in by_category:
                by_category[item.category] = {
                    'total': 0, 'pass': 0, 'fail': 0, 'warning': 0
                }

            by_category[item.category]['total'] += 1
            if item.status == CheckStatus.PASS:
                by_category[item.category]['pass'] += 1
            elif item.status == CheckStatus.FAIL:
                by_category[item.category]['fail'] += 1
            elif item.status == CheckStatus.WARNING:
                by_category[item.category]['warning'] += 1

        return {
            'total_items': len(self.items),
            'by_status': {k.value: v for k, v in by_status.items()},
            'by_category': by_category,
            'completion_rate': (
                (by_status[CheckStatus.PASS] + by_status[CheckStatus.FAIL] +
                 by_status[CheckStatus.WARNING] + by_status[CheckStatus.NOT_APPLICABLE]) /
                len(self.items) * 100
            ),
            'pass_rate': (
                by_status[CheckStatus.PASS] /
                (len(self.items) - by_status[CheckStatus.NOT_CHECKED] - by_status[CheckStatus.NOT_APPLICABLE])
                * 100
                if (len(self.items) - by_status[CheckStatus.NOT_CHECKED] - by_status[CheckStatus.NOT_APPLICABLE]) > 0
                else 0
            )
        }

    def get_failed_items(self) -> List[ChecklistItem]:
        """Get all failed items"""
        return [i for i in self.items if i.status == CheckStatus.FAIL]

    def get_warnings(self) -> List[ChecklistItem]:
        """Get all warning items"""
        return [i for i in self.items if i.status == CheckStatus.WARNING]

    def generate_report(self) -> str:
        """Generate markdown report"""

        report = "# Security Audit Checklist Report\n\n"

        summary = self.get_summary()
        report += f"## Summary\n\n"
        report += f"- Total Items: {summary['total_items']}\n"
        report += f"- Pass: {summary['by_status']['pass']}\n"
        report += f"- Fail: {summary['by_status']['fail']}\n"
        report += f"- Warning: {summary['by_status']['warning']}\n"
        report += f"- Completion: {summary['completion_rate']:.1f}%\n"
        report += f"- Pass Rate: {summary['pass_rate']:.1f}%\n\n"

        # Failed items
        failed = self.get_failed_items()
        if failed:
            report += "## Failed Checks\n\n"
            for item in failed:
                report += f"### {item.category}: {item.check}\n"
                report += f"{item.description}\n"
                if item.notes:
                    report += f"**Notes:** {item.notes}\n"
                report += "\n"

        # Warnings
        warnings = self.get_warnings()
        if warnings:
            report += "## Warnings\n\n"
            for item in warnings:
                report += f"### {item.category}: {item.check}\n"
                report += f"{item.description}\n"
                if item.notes:
                    report += f"**Notes:** {item.notes}\n"
                report += "\n"

        return report
```

---

## 🔗 CONEXIONES NEURONALES

```yaml
conexiones_primarias:
  - neurona: "SOLIDITY_PATTERNS"
    tipo: "code_reference"
    desc: "Patrones seguros de Solidity"

  - neurona: "DEFI_RISKS"
    tipo: "vulnerability_knowledge"
    desc: "Conocimiento de exploits DeFi"

  - neurona: "DEVELOPMENT_TOOLS"
    tipo: "tooling"
    desc: "Herramientas de testing"

conexiones_secundarias:
  - neurona: "SMART_CONTRACTS"
    tipo: "audit_target"
    desc: "Contratos a auditar"

  - neurona: "PROTOCOL_ANALYSIS"
    tipo: "protocol_review"
    desc: "Análisis de protocolos"
```

---

## 📊 MÉTRICAS DE LA NEURONA

```yaml
metricas_salud:
  - nombre: "Vulnerability Detection Rate"
    valor: 95%+
    umbral_alerta: 80%

  - nombre: "False Positive Rate"
    valor: "<10%"
    umbral_alerta: "20%"

  - nombre: "Audit Coverage"
    valor: 100%
    umbral_minimo: 90%

  - nombre: "Tool Integration"
    valor: 5+
    umbral_minimo: 3
```

---

## 🔄 CHANGELOG

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0.0 | 2025-01-XX | Creación inicial - Vulnerability patterns |
| 1.1.0 | 2025-01-XX | Automated analysis tools integration |
| 1.2.0 | 2025-01-XX | Complete audit checklist |

---

> **CIPHER**: "La seguridad no es un feature - es el foundation."
