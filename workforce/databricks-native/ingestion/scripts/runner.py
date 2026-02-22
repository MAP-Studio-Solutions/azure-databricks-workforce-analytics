from __future__ import annotations

# Databricks-side runner (skeleton).
# Implement inside Databricks with Spark and write bronze Delta tables (append-only).

from pathlib import Path
from .config import load_sources_yaml

def run_ingestion(sources_yaml: str, landing_path: str) -> None:
    sources = load_sources_yaml(sources_yaml)
    print(f"Loaded {len(sources)} sources from {sources_yaml}")
    for s in sources.values():
        print(f"[TODO] Ingest {s.name}: {Path(landing_path) / s.landing_relpath} -> {s.bronze_table}")
