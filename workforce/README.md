# Workforce Analytics — Databricks‑Native Method

This folder contains the **Databricks‑native, SQL‑first implementation** of the Workforce Analytics domain.  
It demonstrates how this domain is executed using:

- metadata‑driven ingestion  
- medallion architecture  
- SQL transformations  
- SCD Type 2 modeling  
- point‑in‑time reconstruction  
- Databricks Workflows orchestration  

This README explains:

- What documents exist  
- Which ones are actually used at runtime  
- How the execution architecture works  
- How data flows from raw → bronze → silver → gold  

---

## 1. Repository Layout (Method‑Specific)

```
workforce/
  databricks-native/
    README.md                ← You are here
    sql/
      bronze/                ← Raw → bronze ingestion SQL
      silver/                ← SCD2 + PIT logic
      gold/                  ← Dimensional + reporting models
  ingestion/
    config/
      sources.yaml           ← Runtime metadata input
    python/workforce_ingest/
      config.py              ← Loads YAML → SourceSpec
      runner.py              ← Executes ingestion
      transformations/       ← Python helpers (optional)
  docs/                      ← Human documentation (not executed)
```

---

## 2. What Documents Are Actually Used at Runtime

| Document | Used By | Purpose |
|---------|---------|---------|
| `sources.yaml` | Python ingestion | Defines landing paths, formats, bronze/silver tables, keys |
| `config.py` | Python ingestion | Converts YAML → typed `SourceSpec` objects |
| `runner.py` | Databricks job | Executes ingestion for each source |
| `sql/bronze/*.sql` | Databricks SQL engine | Load raw → bronze |
| `sql/silver/*.sql` | Databricks SQL engine | SCD2 + PIT logic |
| `sql/gold/*.sql` | Databricks SQL engine | Final dimensional models |
| `docs/*.md` | Humans only | Architecture, modeling, explanations |

Everything else is scaffolding.

---

## 3. Execution Architecture (Databricks‑Native)

This method uses **SQL‑first ELT** orchestrated by Databricks Workflows.

### High‑Level Flow

```
sources.yaml
    ↓
config.py → SourceSpec objects
    ↓
runner.py (Databricks job)
    ↓
Bronze SQL (raw → bronze)
    ↓
Silver SQL (SCD2 + PIT)
    ↓
Gold SQL (dimensional models)
```

---

## 4. Detailed Flow Diagram

### 1. Metadata Loading

```
sources.yaml
   └── defines:
         - format
         - landing_relpath
         - bronze_table
         - silver_table
         - keys
```

### 2. Python Ingestion Layer

```
config.py
   └── load_sources_yaml()
         └── creates dict[str, SourceSpec]

runner.py
   └── for each source in SOURCES:
         └── executes bronze SQL
```

### 3. SQL Transformation Layer

```
Bronze Layer
   └── Ingest raw files
   └── Apply schema normalization
   └── Write bronze tables

Silver Layer
   └── SCD Type 2 logic
   └── Point-in-time reconstruction
   └── Surrogate keys

Gold Layer
   └── Dimensional models
   └── Fact tables
   └── Reporting views
```

---

## 5. Document Explanations

### `sources.yaml` (runtime input)  
Defines each dataset’s ingestion metadata.  
This is the *only* document that drives ingestion behavior.

### `config.py`  
Loads YAML → creates immutable `SourceSpec` objects.

### `runner.py`  
Loops through all sources and executes bronze ingestion SQL.

### `sql/bronze/*.sql`  
Implements raw → bronze ingestion using COPY INTO or MERGE.

### `sql/silver/*.sql`  
Implements SCD2 and PIT logic.

### `sql/gold/*.sql`  
Implements dimensional models and reporting tables.

### `docs/*.md`  
Human‑readable explanations.  
Not used by code.

---

## 6. Why This README Matters

Each **method** (Databricks‑native, dbt, Genie) has a different execution architecture:

- Databricks‑native → SQL‑first, orchestrated by Workflows  
- dbt → model‑first, orchestrated by dbt DAG  
- Genie → semantic‑layer‑first, AI‑assisted querying  

This README ensures each workflow method for a domain explains:

- What is executed  
- What is configuration  
- What is documentation  
- How the flow works end‑to‑end  

So when someone opens the folder, they immediately understand:

**“How does this method actually run?”**
