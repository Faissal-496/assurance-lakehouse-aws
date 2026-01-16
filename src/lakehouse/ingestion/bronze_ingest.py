#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import traceback
from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException

# -----------------------------
# Configuration
# -----------------------------
INPUT_PATH = "/opt/lakehouse/data/Contrat2.csv"  # CSV local
S3_BRONZE_PATH = "s3a://lakehouse-assurance-moto-dev1/bronze/"  # Bucket S3

def create_spark_session(app_name="BronzeIngestion"):
    """Créer et retourner une SparkSession"""
    try:
        spark = SparkSession.builder \
            .appName(app_name) \
            .getOrCreate()
        return spark
    except Exception as e:
        print("Erreur lors de la création de la SparkSession :", e)
        sys.exit(1)

def read_csv(spark, path):
    """Lecture sécurisée d'un CSV avec gestion des erreurs"""
    try:
        print(f"📥 Lecture du fichier CSV : {path}")
        df = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .option("nullValue", "") \
            .csv(path)
        print("Lecture terminée")
        print("Schéma détecté :")
        df.printSchema()
        return df
    except AnalysisException as ae:
        print(f"Analyse impossible : {ae}")
        sys.exit(1)
    except Exception as e:
        print("Erreur lors de la lecture du CSV :", e)
        traceback.print_exc()
        sys.exit(1)

def write_to_s3(df, s3_path):
    """Écriture sécurisée dans S3"""
    try:
        print(f"Écriture des données dans S3 : {s3_path}")
        df.write.mode("overwrite").parquet(s3_path)
        print("Écriture réussie")
    except Exception as e:
        print("Erreur lors de l'écriture sur S3 :", e)
        traceback.print_exc()
        sys.exit(1)

def main():
    spark = create_spark_session()

    # Lecture du CSV
    df = read_csv(spark, INPUT_PATH)

    # Écriture dans le bucket bronze S3
    write_to_s3(df, S3_BRONZE_PATH)

    spark.stop()
    print("Pipeline terminé avec succès")

if __name__ == "__main__":
    main()
