# 📘 Workforce Analytics — dbt‑Databricks Method

This folder contains the **dbt‑Databricks implementation** of the Workforce Analytics domain.  
It demonstrates how this domain is executed using:

- dbt models (staging → intermediate → marts)
- dbt sources + schema.yml metadata
- dbt tests (unique, not_null, relationships)
- dbt snapshots for SCD Type 2
- dbt DAG‑driven execution
- Databricks SQL warehouse or cluster as the execution engine

This README explains:

- what documents exist  
- which ones are actually used at runtime  
- how the dbt execution architecture works  
- how data flows from raw → staging → intermediate → marts  

---

## 1. Repository Layout (Method‑Specific)

```
workforce/
  dbt-databricks/
    README.md                ← You are here
    models/
      staging/               ← Source staging models (stg_*)
      intermediate/          ← SCD2 + PIT logic (int_*)
      marts/                 ← Dimensional + reporting models (dim_*, fct_*)
    snapshots/               ← dbt snapshots for SCD2
    seeds/                   ← Optional static reference data
    macros/                  ← Reusable SQL macros
    tests/                   ← Custom tests (if any)
    dbt_project.yml          ← dbt project configuration
    packages.yml             ← External dbt packages
  ingestion/
    config/
      sources.yaml           ← Runtime metadata input (optional for dbt)
  docs/                      ← Human documentation (not executed)
```

---

## 2. What Documents Are Actually Used at Runtime

| Document | Used By | Purpose |
|---------|---------|---------|
| `dbt_project.yml` | dbt CLI / dbt Cloud | Defines project structure, model paths, configs |
| `models/**/*.sql` | dbt | SQL transformations for staging, intermediate, marts |
| `models/**/*.yml` | dbt | Sources, tests, documentation |
| `snapshots/*.sql` | dbt | SCD Type 2 change tracking |
| `packages.yml` | dbt | External packages (dbt-utils, dbt-labs packages) |
| `macros/*.sql` | dbt | Reusable SQL logic |
| `seeds/*.csv` | dbt | Static reference data |
| `sources.yaml` | Optional | Can be used to generate dbt sources dynamically |
| `docs/*.md` | Humans only | Architecture, modeling, explanations |

Everything else is scaffolding.

---

## 3. Execution Architecture (dbt‑Databricks)

This method uses **dbt’s DAG‑driven SQL execution**, orchestrated by:

- dbt CLI  
- dbt Cloud  
- or Databricks Workflows calling `dbt run`  

### High‑Level Flow

```
dbt sources
    ↓
staging models (stg_*)
    ↓
intermediate models (int_*)
    ↓
snapshots (SCD2)
    ↓
marts (dim_*, fct_*)
```

dbt handles:

- dependency resolution  
- ordering  
- testing  
- documentation  
- incremental logic  
- snapshotting  

---

## 4. Detailed Flow Diagram

### 1. Source Definitions

```
models/staging/sources.yml
   └── defines:
         - raw tables
         - column descriptions
         - freshness tests
         - source-level constraints
```

### 2. Staging Layer (stg_*)

```
stg_employees.sql
   └── Clean + standardize raw data
   └── Rename columns to canonical naming
   └── Apply type casting
   └── Apply light business rules
```

### 3. Intermediate Layer (int_*)

```
int_employees_scd2.sql
   └── Apply SCD Type 2 logic
   └── Use dbt snapshots or custom SQL
   └── Build point-in-time reconstruction tables
```

### 4. Snapshots (SCD2)

```
snapshots/employees_snapshot.sql
   └── Tracks changes over time
   └── Maintains valid_from / valid_to windows
   └── Drives SCD2 logic for downstream models
```

### 5. Marts Layer (dim_*, fct_*)

```
dim_employee.sql
   └── Surrogate keys
   └── Slowly changing dimensions
   └── Conformed dimensions

fct_headcount.sql
   └── Fact tables
   └── Metrics + aggregations
   └── Joins to dimensions
```

---

## 5. Document Explanations

### `dbt_project.yml`  
Defines the dbt project structure, model paths, and configs.

### `models/staging/*.sql`  
Implements raw → staging transformations.

### `models/intermediate/*.sql`  
Implements SCD2, PIT logic, and intermediate transformations.

### `models/marts/*.sql`  
Implements dimensional models and fact tables.

### `models/**/*.yml`  
Defines sources, tests, and documentation.

### `snapshots/*.sql`  
Implements SCD Type 2 change tracking.

### `macros/*.sql`  
Reusable SQL logic for transformations.

### `seeds/*.csv`  
Static reference data loaded via `dbt seed`.

### `docs/*.md`  
Human‑readable explanations.  
Not used by code.

---

## 6. Why This README Matters

Each **method** (Databricks‑native, dbt, Genie) has a different execution architecture:

- Databricks‑native → SQL‑first, orchestrated by Workflows  
- dbt → model‑first, DAG‑driven, with tests + snapshots  
- Genie → semantic‑layer‑first, AI‑assisted querying  

This README ensures the **method folder** explains:

- what is executed  
- what is configuration  
- what is documentation  
- how the flow works end‑to‑end  

So when someone opens the folder, they immediately understand:

**“How does this method actually run?”**
