from .rules import (
    high_value_transaction,
    stablecoin_large_transfer,
    self_transfer,
)
from .models import RiskAssessment, ComplianceCase


RISK_RULES = [
    high_value_transaction,
    stablecoin_large_transfer,
    self_transfer,
]


def assess_transaction_risk(transaction):
    triggered = []
    total_score = 0

    for rule in RISK_RULES:
        result = rule(transaction)
        if result:
            triggered.append(result)
            total_score += result["score"]

    if total_score >= 70:
        level = RiskAssessment.RiskLevel.HIGH
    elif total_score >= 30:
        level = RiskAssessment.RiskLevel.MEDIUM
    else:
        level = RiskAssessment.RiskLevel.LOW

    assessment = RiskAssessment.objects.create(
        transaction=transaction,
        risk_score=min(total_score, 100),
        risk_level=level,
        triggered_rules=triggered,
    )
    
    if level == RiskAssessment.RiskLevel.HIGH:
        ComplianceCase.objects.create(transaction=transaction)

    return assessment