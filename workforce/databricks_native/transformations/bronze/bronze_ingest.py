from pyspark.sql import functions as F
from pyspark.sql import SparkSession

def ingest_to_bronze(spark: SparkSession, landing_path: str, bronze_path: str, spec):
    """
    Generic bronze ingestion:
    - Reads raw landing file
    - Adds ingestion metadata
    - Writes append-only Delta to bronze
    """

    full_landing = f"{landing_path}/{spec.landing_relpath}"
    full_bronze  = f"{bronze_path}/{spec.bronze_table}"

    df = (
        spark.read.format(spec.format)
            .option("header", "true")
            .load(full_landing)
            .withColumn("_ingest_ts", F.current_timestamp())
            .withColumn("_file_path", F.input_file_name())
            .withColumn("_load_id", F.expr("uuid()"))
    )

    (
        df.write
          .format("delta")
          .mode("append")
          .save(full_bronze)
    )

    print(f"Bronze load complete: {spec.name} → {full_bronze}")

