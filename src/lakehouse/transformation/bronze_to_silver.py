from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum
from pyspark.sql.functions import col


spark = (
    SparkSession.builder
    .appName("S3 Parquet Analysis")
    .getOrCreate()
)


resolver = PathResolver()

s3_path = resolver.s3_layer_path(
    layer="bronze",
    dataset="Contrat2"
)

df = spark.read.parquet(s3_path)

df.printSchema()
df.show(5)

df.select("nusoc", "nucon", "cateco", "prmaco").show(5)
df.groupBy("cateco").count().show() #A auto , C=Cycle , M=moto
df.groupBy("markli").agg({"prmaco": "avg"}).orderBy("avg(prmaco)", ascending=False).show(10)



for g in garanties:
    df = df.withColumn(g, col(g).cast("int"))
df.toPandas()



df_garanties = df.withColumn(
    "nb_garanties",
    sum([col(g) for g in garanties])
)
df_garanties.toPandas()
df_garanties.groupBy("nb_garanties").count().orderBy("nb_garanties").show()
