# Risk Scoring Rules

The risk engine applies deterministic rules to each transaction. These rules are designed to be explainable, auditable, and regulator-friendly.

## Example Rules

### High Value Transaction
Transactions exceeding a predefined amount threshold are flagged due to increased financial risk exposure.

### Large Stablecoin Transfer
Large transfers involving stablecoins (e.g. USDT) are monitored closely due to their frequent use in settlement and laundering patterns.

### Self Transfer
Transactions where the sender and receiver addresses are identical are flagged as suspicious behavior.

### Cumulative Risk
Multiple low-severity rule triggers can combine to elevate a transaction’s overall risk level.

Each triggered rule contributes a fixed score, resulting in a final risk score and risk classification.