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
from workforce.ingestion_engine.scripts.upload_to_landing import upload_to_landing
from workforce.ingestion_engine.scripts.runner import run_ingestion
from workforce.ingestion_engine.scripts.generate_synth_data import generate_synth_data

# Local temp directory for synthetic data
LOCAL_SYNTH_DATA = "/tmp/workforce_synth"

# ADLS paths
LANDING_PATH = "abfss://analytics@stanalyticsdl001.dfs.core.windows.net/workforce/landing"
BRONZE_PATH  = "abfss://analytics@stanalyticsdl001.dfs.core.windows.net/workforce/bronze"

# Path to metadata
SOURCES_YAML = f"{repo_root}/workforce/ingestion_engine/sources.yaml"

# COMMAND ----------
# Generate synthetic data into /tmp (local to the cluster)
generate_synth_data(LOCAL_SYNTH_DATA)

# COMMAND ----------
# Upload synthetic data → ADLS landing
upload_to_landing(
    local_root=LOCAL_SYNTH_DATA,
    landing_root=LANDING_PATH
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
