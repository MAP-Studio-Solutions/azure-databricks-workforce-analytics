from __future__ import annotations
from pathlib import Path
from pyspark.sql import SparkSession

from .config import load_sources_yaml
from .bronze_ingest import ingest_to_bronze

# Databricks-side runner (skeleton).
# Implement inside Databricks with Spark and write bronze Delta tables (append-only).

from pathlib import Path
from .config import load_sources_yaml

def run_ingestion(sources_yaml: str, landing_path: str) -> None:
    spark = SparkSession.builder.getOrCreate()

    sources = load_sources_yaml(sources_yaml)
    print(f"Loaded {len(sources)} sources from {sources_yaml}")

    for spec in sources.values():
        print(f"Ingesting {spec.name}...")
        ingest_to_bronze(spark, landing_path, bronze_path, spec)