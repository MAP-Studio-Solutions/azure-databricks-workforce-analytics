# Modeling (Gold)

## dim_employee (SCD Type 2)
- Natural key: `employee_id`
- Surrogate key: `employee_sk`
- SCD2: `effective_start_dt`, `effective_end_dt`, `is_current`
- Change detection: hash or explicit attribute comparison from incoming “current state” view

## dim_org
- Natural key: `org_id`
- Surrogate key: `org_sk`
- Hierarchy: `parent_org_id`

## fact_headcount_monthly
Grain: org_id x month  
Source: snapshots

## fact_attrition_monthly
Grain: org_id x month  
Source: termination events + headcount denominator

## Conventions
- Keep transformations small and readable
- Prefer idempotent builds
- Document assumptions and tradeoffs
