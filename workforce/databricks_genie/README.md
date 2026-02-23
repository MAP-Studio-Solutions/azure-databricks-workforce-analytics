# 📘 Workforce Analytics — Genie Method (Databricks AI Assistant)

This folder contains the **Genie‑powered, semantic‑layer‑driven implementation** of the Workforce Analytics domain.  
It demonstrates how this domain is executed using:

- Databricks Genie (AI Assistant)
- Unity Catalog semantic models
- AI‑assisted querying over governed metadata
- Natural‑language → SQL translation
- Automatic documentation + lineage
- Optional dashboard embedding for interactive demos

This README explains:

- what documents exist  
- which ones are actually used at runtime  
- how Genie consumes metadata  
- how the semantic layer drives AI‑assisted analytics  
- how data flows from bronze → silver → gold → semantic model → Genie  

---

## 1. Repository Layout (Method‑Specific)

```
workforce/
  genie/
    README.md                ← You are here
    semantic-models/
      workforce.yml          ← Semantic model definitions (dimensions, measures)
    dashboards/
      workforce_genie.dbd    ← Optional Genie-powered dashboard
    prompts/
      examples.md            ← Example NL prompts for Genie
  databricks-native/
    sql/                     ← Underlying bronze/silver/gold tables
  ingestion/
    python/workforce_ingest/ ← Ingestion + medallion pipeline
  docs/                      ← Human documentation (not executed)
```

---

## 2. What Documents Are Actually Used at Runtime

| Document | Used By | Purpose |
|---------|---------|---------|
| `semantic-models/*.yml` | Genie / Unity Catalog | Defines dimensions, measures, entities, relationships |
| Gold tables | Genie | Queryable governed tables exposed to the semantic layer |
| `dashboards/*.dbd` | Databricks UI | Optional Genie‑powered dashboard |
| `prompts/examples.md` | Humans | Example natural‑language prompts |
| Bronze/Silver SQL | Upstream pipeline | Produces the data Genie queries |
| `docs/*.md` | Humans only | Architecture, modeling, explanations |

Genie does **not** read SQL files or YAML configs directly — it reads **Unity Catalog metadata + semantic models**.

---

## 3. Execution Architecture (Genie Method)

This method uses **semantic‑layer‑first analytics**, where Genie translates natural language into SQL using:

- Unity Catalog table metadata  
- Column descriptions  
- Semantic model definitions  
- Relationships + measures  

### High‑Level Flow

```
Bronze → Silver → Gold tables
        ↓
Unity Catalog (governed metadata)
        ↓
Semantic Model (dimensions + measures)
        ↓
Genie (AI Assistant)
        ↓
Natural language → SQL → Results
```

Genie does **not** run pipelines.  
It **sits on top** of your existing medallion architecture.

---

## 4. Detailed Flow Diagram

### 1. Medallion Tables (Upstream)

```
Bronze Layer
   └── Raw ingestion

Silver Layer
   └── SCD2 + PIT logic

Gold Layer
   └── Dimensional models
   └── Fact tables
```

These tables must exist before Genie can query them.

---

### 2. Unity Catalog Metadata

```
Unity Catalog
   └── Table + column descriptions
   └── Data types
   └── Constraints
   └── Lineage
```

Genie uses this metadata to understand the domain.

---

### 3. Semantic Model (Required for Genie)

```
semantic-models/workforce.yml
   └── entities:
         - employee
         - department
         - job
   └── dimensions:
         - employee attributes
         - department hierarchy
   └── measures:
         - headcount
         - turnover
         - tenure
   └── relationships:
         - employee → department
         - employee → job
```

This is the **core input** that makes Genie intelligent.

---

### 4. Genie Query Layer

```
User prompt:
   "Show me monthly headcount by department"

Genie:
   └── Interprets natural language
   └── Maps to semantic model
   └── Generates SQL
   └── Executes against gold tables
   └── Returns results + visualization
```

---

## 5. Document Explanations

### `semantic-models/*.yml` (runtime input)  
Defines the semantic layer Genie uses to interpret natural language.

### Gold Tables  
The actual data Genie queries.  
These must be clean, dimensional, and well‑described.

### `dashboards/*.dbd`  
Optional Genie‑powered dashboards for demos or portfolio embedding.

### `prompts/examples.md`  
Human‑readable examples of natural‑language queries.

### Bronze/Silver SQL  
Upstream transformations that produce the gold layer.  
Genie does not read these directly.

### `docs/*.md`  
Human‑readable explanations.  
Not used by Genie.

---

## 6. Why This README Matters

Each **method** (Databricks‑native, dbt, Genie) has a different execution architecture:

- Databricks‑native → SQL‑first, orchestrated by Workflows  
- dbt → model‑first, DAG‑driven, with tests + snapshots  
- Genie → semantic‑layer‑first, AI‑assisted querying  

This README ensures the **method folder** explains:

- what Genie actually uses  
- how the semantic model drives AI behavior  
- how the medallion tables feed the semantic layer  
- how natural‑language analytics works end‑to‑end  

So when someone opens the folder, they immediately understand:

**“How does Genie actually run this domain?”**
