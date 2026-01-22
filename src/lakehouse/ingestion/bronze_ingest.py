#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import traceback
from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException
from lakehouse.paths import PathResolver
from lakehouse.ingestion.schema_registry import CONTRAT2_SCHEMA, CLIENT_SCHEMA


def create_spark_session(app_name="BronzeIngestion") -> SparkSession:
    """Créer et retourner une SparkSession Spark avec logs détaillés"""
    try:
        spark = SparkSession.builder.appName(app_name).getOrCreate()
        print(f"[INFO] SparkSession créée : {spark.version}")
        return spark
    except Exception as e:
        print(f"[ERROR] Erreur lors de la création de SparkSession : {e}")
        sys.exit(1)


def read_csv(spark: SparkSession, path: str, schema=None):
    """Lecture sécurisée d'un CSV avec logging et gestion des erreurs"""
    try:
        print(f"[INFO] Lecture du fichier CSV : {path}")
        df = spark.read.option("header", "true") \
                       .option("inferSchema", schema is None) \
                       .option("nullValue", "") \
                       .schema(schema) \
                       .csv(path)
        print(f"[INFO] Lecture terminée. Nombre de lignes : {df.count()}")
        print("[INFO] Schéma détecté / appliqué :")
        df.printSchema()
        return df
    except AnalysisException as ae:
        print(f"[ERROR] Analyse impossible : {ae}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Erreur lors de la lecture du CSV : {e}")
        traceback.print_exc()
        sys.exit(1)


def write_parquet(df, output_path: str):
    """Écriture sécurisée en Parquet sur S3 avec logs"""
    try:
        print(f"[INFO] Écriture des données dans S3 : {output_path}")
        df.write.mode("overwrite").parquet(output_path)
        print(f"[INFO] Écriture réussie dans {output_path}")
    except Exception as e:
        print(f"[ERROR] Erreur lors de l'écriture sur S3 : {e}")
        traceback.print_exc()
        sys.exit(1)


def main():
    print("[INFO] Initialisation du PathResolver")
    resolver = PathResolver()

    spark = create_spark_session()

    # Ingestion Contrat2
    input_contrat2 = resolver.local_input("Contrat2.csv")
    output_contrat2 = resolver.s3_layer_path("bronze", "Contrat2")
    print("[INFO] --- Ingestion Contrat2 ---")
    df_contrat2 = read_csv(spark, input_contrat2, schema=CONTRAT2_SCHEMA)
    write_parquet(df_contrat2, output_contrat2)

    # Ingestion Contrat1
    input_contrat1 = resolver.local_input("contrat1.csv")
    output_contrat1 = resolver.s3_layer_path("bronze", "contrat1")
    print("[INFO] --- Ingestion Contrat1 ---")
    df_contrat1 = read_csv(spark, input_contrat1, schema=CONTRAT2_SCHEMA)
    write_parquet(df_contrat1, output_contrat1)


    # Ingestion Client
    input_client = resolver.local_input("client.csv")
    output_client = resolver.s3_layer_path("bronze", "Client")
    print("[INFO] --- Ingestion Client ---")
    df_client = read_csv(spark, input_client, schema=CLIENT_SCHEMA)
    write_parquet(df_client, output_client)

    spark.stop()
    print("[INFO] Pipeline Bronze terminé avec succès")


if __name__ == "__main__":
    main()
