from decimal import Decimal


def high_value_transaction(transaction):
    if transaction.amount >= Decimal("10000"):
        return {
            "rule": "HIGH_VALUE_TRANSACTION",
            "score": 40,
            "reason": "Transaction amount exceeds 10,000",
        }


def stablecoin_large_transfer(transaction):
    if transaction.asset == "USDT" and transaction.amount >= Decimal("5000"):
        return {
            "rule": "LARGE_STABLECOIN_TRANSFER",
            "score": 30,
            "reason": "Large stablecoin transfer",
        }


def self_transfer(transaction):
    if transaction.from_address == transaction.to_address:
        return {
            "rule": "SELF_TRANSFER",
            "score": 20,
            "reason": "Sender and receiver are identical",
        }