from lakehouse.utils.spark_session import get_spark_session
from lakehouse.paths import PathResolver
from lakehouse.monitoring.logging import logger
from lakehouse.transformation import silver_to_gold

def main():
    logger.info("==== STARTING LAKEHOUSE PIPELINE ====")
    
    # Initialize Spark
    spark = get_spark_session("LakehouseMain")
    
    # Paths
    resolver = PathResolver()
    logger.info(f"Environment: {resolver.app_env}")
    
    # Run transformation
    silver_to_gold.run(spark, resolver)
    
    logger.info("==== PIPELINE COMPLETED SUCCESSFULLY ====")
    spark.stop()

if __name__ == "__main__":
    main()
