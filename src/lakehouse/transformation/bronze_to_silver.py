from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
import sys
from pyspark.sql.functions import expr
from pyspark.sql.functions import lit, col, year, current_date


# =========================
# SPARK SESSION
# =========================
spark = (
    SparkSession.builder
    .appName("Silver_Contrat_Transformation")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# =========================
# PATH RESOLVER (IDENTIQUE)
# =========================
sys.path.append("/opt/lakehouse/lakehouse")
from lakehouse.paths import PathResolver

resolver = PathResolver()

s3_bronze_path_Contrat2 = resolver.s3_layer_path(
    layer="bronze",
    dataset="Contrat2"
)

s3_bronze_path_contrat1 = resolver.s3_layer_path(
    layer="bronze",
    dataset="contrat1"
)

s3_silver_path = resolver.s3_layer_path(
    layer="silver",
    dataset="contrat_silver"
)

# =========================
# READ BRONZE DATA 
# =========================
df = spark.read.parquet(s3_bronze_path_Contrat2)
df1 = spark.read.parquet(s3_bronze_path_contrat1)

# =========================
# UNION contrat1 et Contrat2
# =========================
df_conc = df.unionByName(df1)

# =========================
# a- CAST TYPES 
# =========================
df_silver = (
    df_conc
    .withColumn("nusoc", col("nusoc").cast("int"))
    .withColumn("nucon", col("nucon").cast("int"))
    .withColumn("prmaco", col("prmaco").cast("double"))
    .withColumn("pfco", col("pfco").cast("int"))
    .withColumn("asaico", col("asaico").cast("int"))
)

# =========================
# b- Gestion des valeurs manquantes 
# =========================
df_silver = (
    df_silver
    .withColumn("pfco", when(col("pfco").isNull(), 0).otherwise(col("pfco")))
    .withColumn("etatco", when(col("etatco").isNull(), "UNKNOWN").otherwise(col("etatco")))
    .withColumn("prmaco", when(col("prmaco").isNull(), 0.0).otherwise(col("prmaco")))
)

# =========================
# c- Suppression des doublons contrat
# =========================
df_silver = df_silver.dropDuplicates(["nusoc", "nucon"])


                # =========================
                        #- ||  2--  Transformations SILVER MÉTIER  || 

                         #Décodage des variables métier
                # =========================     



# =========================
# a- TYPE VEHICULE 
# =========================
df_silver = df_silver.withColumn(
    "type_vehicule",
    when(col("cateco") == "A", "Auto")
    .when(col("cateco") == "M", "Moto")
    .when(col("cateco") == "C", "Cyclo")
    .otherwise("Inconnu")
)

# =========================
# b-ETAT CONTRAT 
# =========================
df_silver = df_silver.withColumn(
    "etat_contrat_libelle",
    when(col("etatco") == "0", "Annulé")
    .when(col("etatco") == "1", "En cours")
    .when(col("etatco") == "2", "Suspendu")
    .when(col("etatco") == "3", "Résilié sociétaire") 
    .when(col("etatco") == "4", "Résilié impayé") 
    .when(col("etatco") == "7", " Résilié article 25 (hausse tarifaire)") 
    .when(col("etatco") == "9", " Résilié Mutuelle") 
    
    .otherwise("Autre")
)


# =========================
# c-  Usage du véhicule
# =========================
df_silver = df_silver.withColumn(
    "usage_vehicule",
    when(col("usagco1") == 0, "Domicile-Travail")
    .when(col("usagco1") == 1, "Promenade")
    .when(col("usagco1") == 3, "Professionnel")
    .otherwise("Autre")
)

# =========================
# d - Regroupement des garanties
#Au lieu de 20 colonnes gXXco, on crée des indicateurs synthétiques.
# =========================

garanties = [
    "g01co","g02co","g03co","g04co","g05co","g06co","g09co",
    "g10co","g13co","g15co","g16co","g17co","g18co","g19co",
    "g21co","g22co","g23co","g25co","g26co","g28co"
]

df_silver = df_silver.withColumn(
    "nb_garanties",
    sum(col(g) for g in garanties)
)



                # =========================
                    # - ||| 3-- Création de variables analytiques clés  ||
                # =========================

# =========================
# a - Creation variable année souscription
# =========================

df_silver = df_silver.withColumnRenamed(
    "asaico", "annee_souscription"
)

# =========================
# b - Creation variable ancienneté contrat
# =========================

df_silver = df_silver.withColumn(
    "anciennete_contrat",
    year(current_date()) - col("annee_souscription")
)





# =========================
# WRITE SILVER
# =========================
df_silver.write \
    .mode("overwrite") \
    .parquet(s3_silver_path)

spark.stop()
