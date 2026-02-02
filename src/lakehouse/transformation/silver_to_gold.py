# src/lakehouse/transformation/silver_to_gold.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, sum as spark_sum, count, avg, max as spark_max, 
    min as spark_min, round, lit, year, month, current_date, 
    coalesce, desc, percent_rank
)
from pyspark.sql.window import Window
import sys
from datetime import datetime

# =========================
# SPARK SESSION
# =========================
spark = (
    SparkSession.builder
    .appName("Gold_Dashboard_Transformation")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# =========================
# PATH RESOLVER
# =========================
sys.path.append("/opt/lakehouse/lakehouse")
from lakehouse.paths import PathResolver

resolver = PathResolver()

s3_silver_path_client_contrat = resolver.s3_layer_path(
    layer="silver",
    dataset="Client_contrat_silver"
)

s3_gold_path_kpi = resolver.s3_layer_path(
    layer="gold",
    dataset="kpi_dashboard"
)

s3_gold_path_client_profile = resolver.s3_layer_path(
    layer="gold",
    dataset="client_profile_analysis"
)

s3_gold_path_contract_analysis = resolver.s3_layer_path(
    layer="gold",
    dataset="contract_analysis"
)

# =========================
# READ SILVER DATA (Client_Contrat unified)
# =========================
print("\n" + "="*80)
print("🏗️  SILVER TO GOLD - ZENOR KPI DASHBOARD TRANSFORMATION")
print("="*80)

df_silver = spark.read.parquet(s3_silver_path_client_contrat)

total_records = df_silver.count()
print(f"\n📊 Silver data loaded: {total_records} records")
print(f"Columns: {len(df_silver.columns)}")






# =========================
# GOLD LAYER 1: CLIENT PROFILE ANALYSIS
# =========================
print("\n" + "-"*80)
print("📋 [GOLD 1] CLIENT PROFILE ANALYSIS")
print("-"*80)

# Get unique clients
df_client_profile = df_silver.select(
    "nusoc", "age_client", "client_jeune", "sexsoc", 
    "cspsoc", "sitmat", "sitpav1"
).dropDuplicates(["nusoc"])

total_clients = df_client_profile.count()
print(f"✅ Total unique clients: {total_clients}")

# Age distribution
print("\n📈 Age Distribution:")
age_dist = df_client_profile.groupBy("age_client").agg(
    count("nusoc").alias("nb_clients")
).orderBy(desc("nb_clients")).limit(10)
age_dist.show()

# Young customers (<30)
from pyspark.sql.functions import round as spark_round, lit

young_pct_df = df_client_profile.select(
    spark_round(
        (lit(young_count) / lit(total_clients) * 100), 2
    ).alias("young_pct")
)

young_pct_df.show()

# Gender distribution
print("\n👥 Gender Distribution:")
gender_dist = df_client_profile.groupBy("sexsoc").agg(
    count("nusoc").alias("nb_clients")
)
gender_dist.show()

# Save client profile
df_client_profile.write.mode("overwrite").parquet(s3_gold_path_client_profile)
print(f"✅ Client Profile saved to Gold")


# =========================
# GOLD LAYER 2: CONTRACT ANALYSIS
# =========================
print("\n" + "-"*80)
print("📋 [GOLD 2] CONTRACT ANALYSIS")
print("-"*80)

df_contract_analysis = df_silver.select(
    "nusoc", "nucon", "type_vehicule", "etat_contrat_libelle", "contrat_actif",
    "prmaco", "nb_garanties", "anciennete_contrat", 
    "annee_souscription", "age_client", "client_jeune", "jeune_moto"
)

total_contracts = df_contract_analysis.count()
print(f"✅ Total contracts: {total_contracts}")

# Vehicle type distribution
print("\n🚗 Vehicle Type Distribution:")
vehicle_dist = df_contract_analysis.groupBy("type_vehicule").agg(
    count("nucon").alias("nb_contrats"),
    round(avg("prmaco"), 2).alias("avg_premium"),
    round(avg("nb_garanties"), 2).alias("avg_garanties")
).orderBy(desc("nb_contrats"))
vehicle_dist.show()

# Contract status distribution
print("\n📊 Contract Status Distribution:")
status_dist = df_contract_analysis.groupBy("etat_contrat_libelle").agg(
    count("nucon").alias("nb_contrats"),
    round(avg("prmaco"), 2).alias("avg_premium")
).orderBy(desc("nb_contrats"))
status_dist.show()

# Save contract analysis
df_contract_analysis.write.mode("overwrite").parquet(s3_gold_path_contract_analysis)
print(f"✅ Contract Analysis saved to Gold")




# =========================
# GOLD LAYER 3: 5-KEY PERFORMANCE INDICATORS (KPI)
# =========================
from pyspark.sql.types import (
    StructType, StructField,
    IntegerType, LongType, DoubleType, StringType
)
kpi_schema = StructType([
    StructField("kpi_id", IntegerType(), False),
    StructField("kpi_name", StringType(), False),
    StructField("kpi_value", DoubleType(), False),      # 👈 TOUJOURS Double
    StructField("kpi_total", LongType(), False),
    StructField("kpi_percentage", DoubleType(), False),
    StructField("kpi_target", DoubleType(), False),
    StructField("kpi_status", StringType(), False),
    StructField("report_month", IntegerType(), False),
    StructField("report_year", IntegerType(), False)
])

import builtins
from datetime import datetime
from pyspark.sql.functions import col, avg

print("\n" + "="*80)
print("🎯 [GOLD 3] 5-KEY PERFORMANCE INDICATORS (KPI)")
print("="*80)

# =========================
# REPORT CONTEXT
# =========================
MONTH_REPORT = datetime.now().month
YEAR_REPORT = datetime.now().year

# =========================
# KPI 1: MARKET SHARE
# =========================
active_contracts = df_silver.filter(col("contrat_actif") == 1).count()

market_share_pct = float(
    builtins.round(active_contracts / total_records * 100, 2)
)

print(f"\n🎯 KPI 1: MARKET SHARE")
print(f"   Active Contracts: {active_contracts}/{total_records}")
print(f"   Market Share %: {market_share_pct}%")
print(f"   Target: ≥ 50%")
print(f"   Status: {'✅ ON TRACK' if market_share_pct >= 50 else '⚠️ AT RISK'}")

# =========================
# KPI 2: RETENTION RATE
# =========================
resigned_contracts = df_silver.filter(
    (col("etat_contrat_libelle").like("Résilié%")) |
    (col("etat_contrat_libelle") == "Annulé")
).count()

retention_rate = float(
    builtins.round((total_records - resigned_contracts) / total_records * 100, 2)
)

resignation_rate = float(
    builtins.round(resigned_contracts / total_records * 100, 2)
)

print(f"\n🎯 KPI 2: RETENTION RATE")
print(f"   Active Contracts: {total_records - resigned_contracts}/{total_records}")
print(f"   Retention Rate: {retention_rate}%")
print(f"   Resignation Rate: {resignation_rate}%")
print(f"   Target: ≥ 97%")
print(f"   Status: {'✅ ON TRACK' if retention_rate >= 97 else '⚠️ AT RISK'}")

# =========================
# KPI 3: YOUNG CUSTOMER RATIO
# =========================
young_total = df_silver.filter(col("client_jeune") == 1).count()

young_ratio_pct = float(
    builtins.round(young_total / total_records * 100, 2)
)

print(f"\n🎯 KPI 3: YOUNG CUSTOMER RATIO (<30 years)")
print(f"   Young Customers: {young_total}/{total_records}")
print(f"   Young Ratio %: {young_ratio_pct}%")
print(f"   Target: ≥ 35%")
print(f"   Status: {'✅ ON TRACK' if young_ratio_pct >= 35 else '⚠️ AT RISK'}")

# =========================
# KPI 4: AVERAGE PREMIUM
# =========================
avg_premium_value = df_silver.agg(avg("prmaco")).collect()[0][0]
avg_premium_all = float(builtins.round(avg_premium_value, 2))

print(f"\n🎯 KPI 4: AVERAGE PREMIUM")
print(f"   Average Premium: €{avg_premium_all}")
print(f"   Status: 📊 INFORMATIVE")

# =========================
# KPI 5: HIGH-RISK YOUNG DRIVERS
# =========================
high_risk_young_moto = df_silver.filter(col("jeune_moto") == 1).count()

high_risk_pct = float(
    builtins.round(high_risk_young_moto / total_records * 100, 2)
)

print(f"\n🎯 KPI 5: HIGH-RISK YOUNG DRIVERS (Young + Moto)")
print(f"   Young Moto Drivers: {high_risk_young_moto}/{total_records}")
print(f"   High-Risk %: {high_risk_pct}%")
print(
    f"   Status: "
    f"{'🟢 OK' if high_risk_pct < 10 else '🟡 WARNING' if high_risk_pct < 20 else '🔴 CRITICAL'}"
)

# =========================
# BUILD KPI DATAFRAME (SAFE TYPES)
# =========================
kpi_data = [
    (
        1,
        "Market Share (Active Contracts)",
        float(active_contracts),
        int(total_records),
        float(market_share_pct),
        float(50),
        "ON TRACK" if market_share_pct >= 50 else "AT RISK",
        MONTH_REPORT,
        YEAR_REPORT
    ),
    (
        2,
        "Retention Rate",
        float(total_records - resigned_contracts),
        int(total_records),
        float(retention_rate),
        float(97),
        "ON TRACK" if retention_rate >= 97 else "AT RISK",
        MONTH_REPORT,
        YEAR_REPORT
    ),
    (
        3,
        "Young Customer Ratio (<30)",
        float(young_total),
        int(total_records),
        float(young_ratio_pct),
        float(35),
        "ON TRACK" if young_ratio_pct >= 35 else "AT RISK",
        MONTH_REPORT,
        YEAR_REPORT
    ),
    (
        4,
        "Average Premium (EUR)",
        float(avg_premium_all),
        int(total_records),
        float(0.0),
        float(0.0),
        "INFORMATIVE",
        MONTH_REPORT,
        YEAR_REPORT
    ),
    (
        5,
        "High-Risk Young Drivers (Moto)",
        float(high_risk_young_moto),
        int(total_records),
        float(high_risk_pct),
        float(10),
        "CRITICAL" if high_risk_pct > 20 else "WARNING" if high_risk_pct > 10 else "OK",
        MONTH_REPORT,
        YEAR_REPORT
    )
]

df_kpi = spark.createDataFrame(kpi_data)

# =========================
# DISPLAY KPI DASHBOARD
# =========================
print("\n📊 KPI Dashboard Summary:")
df_kpi.show(truncate=False)



# =========================
# GOLD LAYER 4: SEGMENTED ANALYSIS
# =========================
print("\n" + "-"*80)
print("📊 [GOLD 4] SEGMENTED ANALYSIS BY AGE, VEHICLE, STATUS")
print("-"*80)

# By Vehicle Type
print("\n🚗 KPI by Vehicle Type:")
kpi_by_vehicle = df_silver.groupBy("type_vehicule").agg(
    count("nucon").alias("nb_contrats"),
    spark_sum("contrat_actif").alias("contrats_actifs"),
    avg("prmaco").alias("avg_premium_raw"),
    spark_sum(when(col("client_jeune") == 1, 1).otherwise(0)).alias("jeunes_conducteurs"),
    spark_sum("jeune_moto").alias("moto_jeunes")
).select(
    "type_vehicule",
    "nb_contrats",
    "contrats_actifs",
    col("avg_premium_raw").cast("decimal(10,2)").alias("avg_premium"),
    "jeunes_conducteurs",
    "moto_jeunes"
).orderBy(desc("nb_contrats"))
kpi_by_vehicle.show()

# By Contract Status
print("\n📋 KPI by Contract Status:")
kpi_by_status = df_silver.groupBy("etat_contrat_libelle").agg(
    count("nucon").alias("nb_contrats"),
    avg("prmaco").alias("avg_premium_raw"),
    spark_sum("contrat_actif").alias("actifs")
).select(
    "etat_contrat_libelle",
    "nb_contrats",
    col("avg_premium_raw").cast("decimal(10,2)").alias("avg_premium"),
    "actifs"
).orderBy(desc("nb_contrats"))
kpi_by_status.show()


 #=========================
# GOLD LAYER 5: ALERT CONDITIONS
# =========================
print("\n" + "-"*80)
print("⚠️  ALERT CONDITIONS & RECOMMENDATIONS")
print("-"*80)

print("\n🎯 ZENOR STRATEGIC OBJECTIVES STATUS:")
if resignation_rate <= 27:  # Target: reduce from 30% to 27% (-3 points)
    print(f"  ✅ KPI 2: Resignation {resignation_rate}% ≤ 27% TARGET")
else:
    print(f"  ⚠️ KPI 2: Resignation {resignation_rate}% > 27% TARGET - ACTION NEEDED")

if young_ratio_pct >= 35:  # TargeAt: +5 points
    print(f"  ✅ KPI 3: Young ratio {young_ratio_pct}% ≥ 35% TARGET")
else:
    print(f"  ⚠️ KPI 3: Young ratio {young_ratio_pct}% < 35% TARGET - ACTION NEEDED")

if market_share_pct >= 50:  # Target: 10% increase
    print(f"  ✅ KPI 1: Market share {market_share_pct}% ≥ 50% TARGET")
else:
    print(f"  ⚠️ KPI 1: Market share {market_share_pct}% < 50% TARGET - ACTION NEEDED")

if high_risk_pct <= 15:
    print(f"  🟢 KPI 5: High-risk {high_risk_pct}% ≤ 15% - ACCEPTABLE")
else:
    print(f"  🔴 KPI 5: High-risk {high_risk_pct}% > 15% - CRITICAL")
# =========================
# WRITE GOLD TABLES
# =========================
print("\n" + "="*80)
print("💾 WRITING GOLD LAYER TABLES")
print("="*80)

df_kpi.write.mode("overwrite").parquet(s3_gold_path_kpi)
print(f"✅ KPI Dashboard → Gold Layer")

print("\n" + "="*80)
print("✨ GOLD LAYER TRANSFORMATION COMPLETE")
print("="*80)

spark.stop()