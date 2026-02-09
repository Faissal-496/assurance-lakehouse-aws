from pyspark.sql import DataFrame
from lakehouse.utils.helpers import safe_divide

def retention_rate(df: DataFrame, active_col="contrat_actif") -> float:
    total = df.count()
    active = df.filter(f"{active_col} = 1").count()
    return safe_divide(active, total) * 100

def market_share(df: DataFrame, active_col="contrat_actif") -> float:
    total = df.count()
    active = df.filter(f"{active_col} = 1").count()
    return safe_divide(active, total) * 100
