from __future__ import annotations
from pathlib import Path

from .config import load_sources_yaml
from .upload_to_landing import upload_to_landing


def run_ingestion(
    sources_yaml: str,
    local_root: str,
    landing_root: str
) -> None:
    """
    Metadata-driven ingestion runner.
    Loads source specs from YAML and uploads raw files to ADLS landing.
    """

    sources = load_sources_yaml(sources_yaml)
    print(f"Loaded {len(sources)} sources from {sources_yaml}")

    for spec in sources.values():
        print(f"Ingesting {spec.name}...")

        # Each source gets its own subfolder under local_root
        source_local_path = f"{local_root}/{spec.name}"

        upload_to_landing(
            local_root=source_local_path,
            landing_root=f"{landing_root}/{spec.landing_relpath}"
        )
