# Architecture

## Goal
Demonstrate an Azure Databricks analytics platform with clear layering, incremental logic, and dimensional modeling.

## High-Level Flow
Landing (raw files in ADLS/DBFS)
  → Bronze Delta tables (minimal parsing, append-only)
    → Silver Delta tables (clean/typed/deduped; incremental)
      → Gold (dimensional models + facts)

## Storage Paths (suggested)
- `LANDING_PATH`: `abfss://<container>@<account>.dfs.core.windows.net/landing`
- `BRONZE_PATH`:  `.../bronze`
- `SILVER_PATH`:  `.../silver`
- `GOLD_PATH`:    `.../gold`

## Orchestration
Databricks Workflows:
1) Landing → Bronze
2) Bronze → Silver (incremental)
3) Silver → Gold (dims then facts)
4) Basic DQ checks (nulls, duplicates, reconciliation)

## Incremental Strategy (MVP)
- Events: `event_ts`
- Snapshots: `snapshot_date`
MVP approach: partition by date, MERGE for dims/silver, rebuild partitions for facts if needed.

## Data Quality (MVP)
- Not-null checks on primary keys / natural keys
- Duplicate checks on key sets
- Reconciliation:
  - headcount totals vs fact totals
  - terminations vs attrition facts
