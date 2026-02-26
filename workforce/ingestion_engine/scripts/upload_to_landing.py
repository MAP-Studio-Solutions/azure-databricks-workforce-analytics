import os
from pathlib import Path
from databricks.sdk.runtime import dbutils


def upload_to_landing(local_root: str, landing_root: str) -> None:
    """
    Upload all files under local_root into the ADLS landing_root,
    preserving subfolder structure.

    Parameters
    ----------
    local_root : str
        Local directory containing generated synthetic data.
    landing_root : str
        ADLS landing path (abfss://...).
    """

    local_root_path = Path(local_root)

    for root, _, files in os.walk(local_root_path):
        for f in files:
            local_path = Path(root) / f
            rel_path = local_path.relative_to(local_root_path).as_posix()
            dest_path = f"{landing_root}/{rel_path}"

            print(f"Uploading {local_path} → {dest_path}")
            dbutils.fs.cp(f"file:{local_path}", dest_path, True)
