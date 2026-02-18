from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass(frozen=True)
class SourceSpec:
    name: str
    format: str
    landing_relpath: str
    bronze_table: str
    silver_table: str
    keys: list[str]

def load_sources_yaml(path: str | Path) -> dict[str, SourceSpec]:
    p = Path(path)
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    out: dict[str, SourceSpec] = {}
    for name, spec in data.get("sources", {}).items():
        out[name] = SourceSpec(
            name=name,
            format=spec["format"],
            landing_relpath=spec["landing_relpath"],
            bronze_table=spec["bronze_table"],
            silver_table=spec["silver_table"],
            keys=list(spec.get("keys", [])),
        )
    return out
