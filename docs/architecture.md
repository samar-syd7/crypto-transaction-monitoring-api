# System Architecture

This service is an internal backend responsible for monitoring crypto transactions and enforcing compliance workflows.

Decoded blockchain transactions are ingested via a secured internal API and validated for schema and integrity. Valid transactions are persisted and passed through a deterministic, rule-based risk engine.

The risk engine assigns a numerical score and risk level to each transaction. High-risk transactions automatically trigger compliance case creation for analyst review.

Compliance analysts interact with the system via internal APIs to review, update, and close cases.

All critical system actions—including ingestion, scoring, escalation, and analyst updates—are recorded in an append-only, immutable audit log to ensure regulatory traceability.