# Crypto Transaction Monitoring & Compliance API

Backend infrastructure modeling a **Transaction Monitoring System (TMS)** used in regulated crypto exchanges for:

- Anti-Money Laundering (AML)
- Fraud detection
- Compliance case management
- Forensic audit logging

Designed as a **deterministic, event-driven backend system** prioritizing:
- Idempotency
- Auditability
- Transaction integrity
- Explainable risk evaluation

---

## Problem Statement

Regulated crypto platforms must monitor on-chain activity, detect suspicious behavior deterministically, escalate risks to compliance teams, and retain tamper-proof audit records for regulatory scrutiny.

This project implements those backend primitives **without blockchain node integration**, focusing purely on decoded transaction compliance logic.

---

## System Overview

The service ingests decoded blockchain transactions from internal pipelines, validates and persists them, evaluates risk using deterministic rules, and escalates high-risk activity to compliance analysts.

All critical actions are recorded in an **append-only, immutable audit log**.

---

## Architecture

```
Ingest Service
      ↓
Transaction API
      ↓
Risk Engine
      ↓
Compliance Workflow
      ↓
Immutable Audit Log
```

---

## Transaction Processing Flow

1. Internal ingestion pipeline submits decoded blockchain transaction.
2. Transaction API validates schema and persists the transaction.
3. Risk engine evaluates deterministic compliance rules.
4. If risk level is HIGH, a compliance case is automatically created.
5. All actions emit immutable audit events.

   
---

## System Guarantees

The system enforces several invariants required for compliance infrastructure:

- **Deterministic risk scoring** — identical inputs always produce identical results.
- **Immutable audit events** — compliance actions cannot be modified or deleted once recorded.
- **Idempotent transaction ingestion** — duplicate blockchain events cannot create duplicate records due to database-level constraints.
- **Least-privilege service authentication** — only authorized services can ingest transactions or access compliance workflows.

---

## Core Entities

### Transaction
Represents a decoded blockchain transaction ingested from internal pipelines.

Fields:
- blockchain
- tx_hash
- from_address
- to_address
- amount
- asset
- block_number
- tx_timestamp
- status

---

### RiskAssessment
Represents the deterministic risk evaluation result for a transaction.

Fields:
- transaction
- risk_score
- risk_level
- triggered_rules
- assessed_at

---

### ComplianceCase
Represents a manual compliance investigation triggered by high-risk activity.

Fields:
- transaction
- assigned_to
- status
- notes
- created_at
- closed_at

---

### AuditEvent
Represents an append-only record of system activity for forensic traceability.

Fields:
- actor
- action
- timestamp
- metadata

---

### Scope Boundaries

- Internal backend service only  
- Stateless service-to-service authentication  
- Deterministic, rule-based business logic  

**Out of Scope**
- Blockchain node interaction  
- Trading or market functionality  
- End-user authentication  

---

## Technology Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT (SimpleJWT, stateless mode)

---

## Authentication Model

The system uses **service-to-service JWT authentication**, not end-user accounts.

JWT claims include:

| Claim | Description |
|-----|------------|
| `role` | Authorization role |
| `service` | Calling service identity |

### Defined Roles

| Role | Permissions |
|----|------------|
| `INGEST_SERVICE` | Ingest blockchain transactions |
| `COMPLIANCE_ANALYST` | Review and manage compliance cases |

**Authentication Class**
```
JWTStatelessUserAuthentication
```

---

## Issue Internal Service Token

**POST** `/api/internal/token/`

```json
{
  "role": "INGEST_SERVICE",
  "service_name": "tx_ingest_pipeline"
}
```

---

## Transaction Ingestion API

**POST** `/api/transactions/ingest/`  
**Required Role:** `INGEST_SERVICE`

```json
{
  "tx_hash": "0xabc123",
  "blockchain": "eth",
  "from_address": "0xfrom",
  "to_address": "0xto",
  "amount": "12000",
  "asset": "USDT",
  "block_number": 19123456,
  "tx_timestamp": "2025-01-03T12:00:00Z",
  "ingestion_source": "tx_ingest_pipeline"
}
```

### Behavior

- Validates request schema
- Enforces uniqueness `(tx_hash + blockchain)`
- Persists transaction data
- Executes deterministic risk scoring
- Automatically creates a compliance case if risk level is **HIGH**
- Emits audit events for traceability
- Duplicate transactions are rejected at the database level using a unique (tx_hash, blockchain) constraint.

---

## Risk Engine

The risk engine is **deterministic and rule-based** by design, prioritizing explainability and auditability over probabilistic scoring.

### Output

- Risk score (0–100)
- Risk level: `LOW`, `MEDIUM`, or `HIGH`
- Triggered rules with human-readable explanations

---

## Compliance Workflow

High-risk transactions automatically generate compliance cases for analyst review.

### List Compliance Cases

**GET** `/api/compliance/cases/`  
**Required Role:** `COMPLIANCE_ANALYST`

---

### Update Compliance Case

**PATCH** `/api/compliance/cases/{id}/`  
**Required Role:** `COMPLIANCE_ANALYST`

```json
{
  "status": "CLOSED",
  "assigned_to": "analyst_007",
  "notes": "Reviewed and confirmed as false positive"
}
```

---

## Audit Logging

All critical system actions generate audit events.

### Guarantees

- Append-only
- Immutable
- Protected against updates and deletion
- Forensic-grade traceability

---

## Design Philosophy 

- Deterministic and explainable logic
- Least-privilege access
- Immutable audit trail
- Compliance-first architecture

---

## Data Integrity Guarantees

The system enforces several integrity guarantees:

- Unique transaction constraint `(tx_hash, blockchain)` prevents duplicate ingestion.
- Risk assessments are deterministic and reproducible.
- Compliance case lifecycle changes generate immutable audit events.
- Audit records are append-only and protected from modification.

---

## Failure Scenarios Considered

### Duplicate Transaction Delivery
Blockchain ingestion pipelines may deliver duplicate events.

Mitigation:
Database-level uniqueness constraints prevent duplicate transaction records.

---

### Risk Engine Failure
Risk evaluation may fail due to unexpected rule conditions.

Mitigation:
Transactions remain persisted and can be reprocessed safely.

---

### Unauthorized Service Access
Misconfigured services could attempt to ingest transactions.

Mitigation:
JWT-based service authentication ensures only authorized internal services can interact with the API.

---

## Key Engineering Highlights

- Designed **idempotent ingestion pipeline** preventing duplicate transaction processing
- Implemented **deterministic risk engine** (reproducible compliance decisions)
- Built **append-only audit logging system** for forensic traceability
- Modeled **compliance case lifecycle workflows** (analyst-driven investigation)
- Enforced **database-level integrity constraints** for correctness under concurrency
- Implemented **stateless service-to-service authentication (JWT)**

---

## Future Improvements

- Asynchronous ingestion and scoring
- Rule versioning
- Sanctions and address risk lists
- Historical re-scoring

---

### Why This Project Exists

This project was built to model how regulated crypto exchanges monitor on-chain activity, enforce compliance workflows, and maintain forensic-grade audit trails without relying on blockchain node integrations.

The focus is on backend correctness, explainability, and security — not trading or UI features.

---

## Disclaimer

This project is for educational and architectural demonstration purposes only.
