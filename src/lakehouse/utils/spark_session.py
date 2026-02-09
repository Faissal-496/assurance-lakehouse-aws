from pyspark.sql import SparkSession
from lakehouse.monitoring.logging import logger
import os

def get_spark_session(app_name="LakehouseApp", enable_hive=True):
    """
    Create or retrieve a Spark session with optimized configs for production.
    """
    logger.info(f"Initializing Spark Session for {app_name}...")
    
    builder = SparkSession.builder.appName(app_name)
    
    # Enable Hive if requested
    if enable_hive:
        builder = builder.enableHiveSupport()

    # Production configurations (later in YAML )
    builder = builder.config("spark.sql.shuffle.partitions", os.getenv("SPARK_SHUFFLE_PARTS", "200"))
    builder = builder.config("spark.driver.memory", os.getenv("SPARK_DRIVER_MEMORY", "4g"))
    builder = builder.config("spark.executor.memory", os.getenv("SPARK_EXECUTOR_MEMORY", "4g"))
    builder = builder.config("spark.sql.execution.arrow.pyspark.enabled", "true")

    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel(os.getenv("SPARK_LOG_LEVEL", "WARN"))
    
    logger.info("Spark Session initialized successfully")
    return spark
 