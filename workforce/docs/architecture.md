# Architecture

## Goal
Demonstrate a modern Azure Databricks analytics platform with clear separation of
concerns across ingestion, transformation, and semantic layers — using ADLS for
raw data landing and Serverless SQL Warehouse + dbt for all modeling.

## High‑Level Flow
Landing (raw files in ADLS)
  → Bronze (dbt models in Unity Catalog)
    → Silver (clean/typed/deduped dbt models)
      → Gold (dimensional models + facts in Unity Catalog)

## Storage Paths (actual)
- `LANDING_PATH`: `abfss://analytics@stanalyticsdl001.dfs.core.windows.net/workforce/landing`
- `BRONZE` / `SILVER` / `GOLD`:
    These layers are **not stored as folders in ADLS**.
    They are **materialized as Unity Catalog tables** by dbt using Serverless SQL Warehouse.

## Layer Responsibilities

### Ingestion Layer (Python → ADLS Landing)
- Generates or receives raw files
- Uses YAML metadata to define landing locations
- Uploads files to ADLS landing
- No Spark, no Delta, no clusters
- Output: **raw files only**

### Transformation Layer (dbt + Serverless SQL Warehouse → Unity Catalog)
- Reads raw files from ADLS landing
- Creates Bronze tables in Unity Catalog
- Applies incremental logic, typing, deduplication (Silver)
- Builds dimensional models and facts (Gold)
- All compute is Serverless SQL Warehouse (pay‑per‑second)
- All tables governed in Unity Catalog

### Semantic Layer (Genie, optional)
- Exposes UC tables through a semantic/AI interface
- Provides business‑friendly access to curated models

## Why This Architecture
- Ingestion is lightweight, metadata‑driven, and cost‑efficient
- Modeling is fully serverless and SQL‑first
- Unity Catalog provides governance, lineage, and access control
- dbt provides declarative, testable, version‑controlled transformations
- No clusters are required for ingestion or modeling
