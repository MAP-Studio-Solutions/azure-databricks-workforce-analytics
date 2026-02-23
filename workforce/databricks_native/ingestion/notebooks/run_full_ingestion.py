# Databricks notebook source
# COMMAND ----------
# Install dependencies (pinned versions for reproducibility)
%pip install pandas==2.2.1 PyYAML==6.0.1 faker==24.9.0

# COMMAND ----------
# Add repo_root to sys.path for imports
import sys
import os

repo_root = "/Workspace/Users/matthew@2matthewalgergmail.onmicrosoft.com/modern-analytics-platforms-demo"
if repo_root not in sys.path:
    sys.path.append(repo_root)


# COMMAND ----------
# Imports and path configuration

from workforce.databricks_native.ingestion.scripts.upload_to_landing import upload_to_landing
from workforce.databricks_native.ingestion.scripts.runner import run_ingestion
import subprocess

# Local temp directory for synthetic data
LOCAL_SYNTH_DATA = "/tmp/workforce_synth"

# ADLS paths
LANDING_PATH = "abfss://analytics@stanalyticsdl001.dfs.core.windows.net/workforce/landing"
BRONZE_PATH  = "abfss://analytics@stanalyticsdl001.dfs.core.windows.net/workforce/bronze"

# Path to metadata
SOURCES_YAML = "/Workspace/Repos/.../workforce/databricks-native/ingestion/sources.yaml"

# COMMAND ----------
# Generate synthetic data into /tmp (local to the cluster)

subprocess.run([
    "python",
    "/Workspace/Repos/.../workforce/databricks-native/ingestion/scripts/generate_synth_data.py",
    "--out", LOCAL_SYNTH_DATA
], check=True)

# COMMAND ----------
# Upload synthetic data → ADLS landing

upload_to_landing(
    local_path=LOCAL_SYNTH_DATA,
    landing_path=LANDING_PATH
)

# COMMAND ----------
# Run bronze ingestion

run_ingestion(
    sources_yaml=SOURCES_YAML,
    landing_path=LANDING_PATH,
    bronze_path=BRONZE_PATH
)

# COMMAND ----------
# (Optional) Future steps:
# - Run silver transformations
# - Run gold transformations
# - Add validation / DQ checks
# - Add PIT tables
# - Add lineage logging
# - Add workflow orchestration
