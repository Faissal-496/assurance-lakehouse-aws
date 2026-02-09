from lakehouse.utils.logging import logger

# Wrapper for structured logging
def log_kpi_status(kpi_name, value, target, status):
    logger.info(f"KPI: {kpi_name} | Value: {value} | Target: {target} | Status: {status}")

def log_data_quality(table_name, total_rows, failed_checks):
    status = "PASS" if failed_checks == 0 else "FAIL"
    logger.info(f"Data Quality Check - {table_name}: Total Rows={total_rows}, Failed Checks={failed_checks}, Status={status}")
