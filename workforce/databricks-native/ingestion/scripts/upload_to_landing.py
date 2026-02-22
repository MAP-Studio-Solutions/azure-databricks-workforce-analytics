import os
from pathlib import Path

def upload_to_landing(local_root: str, landing_root: str):
    for root, _, files in os.walk(local_root):
        for f in files:
            local_path = os.path.join(root, f)
            rel_path = os.path.relpath(local_path, local_root)
            dest_path = f"{landing_root}/{rel_path}"

            print(f"Uploading {local_path} → {dest_path}")
            dbutils.fs.cp(f"file:{local_path}", dest_path, True)
