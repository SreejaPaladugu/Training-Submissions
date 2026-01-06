from pathlib import Path
import csv
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, upper, sum as _sum, count as _count

DATA_DIR = Path("project_data")
OUT_DIR = Path("project_output")
DATA_DIR.mkdir(exist_ok=True)
OUT_DIR.mkdir(exist_ok=True)

RAW_CSV = DATA_DIR / "events.csv"
PARQUET_OUT = OUT_DIR / "curated_events_parquet"
REPORT_TXT = OUT_DIR / "report.txt"

def seed_events_if_missing():
    if RAW_CSV.exists():
        return
    rows = [
        ["event_id", "user_id", "event_type", "country", "value"],
        [1, 101, "click", " us ", 1],
        [2, 101, "purchase", "US", 120],
        [3, 102, "click", " india ", 1],
        [4, 103, "purchase", "EU", 80],
        [5, 102, "purchase", "INDIA", 60],
        [6, 104, "click", "US", 1],
    ]
    with open(RAW_CSV, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)

def main():
    seed_events_if_missing()

    spark = SparkSession.builder.appName("SparkMiniProject").master("local[*]").getOrCreate()

    # EXTRACT
    df = (spark.read.option("header", True).option("inferSchema", True).csv(str(RAW_CSV)))

    # TRANSFORM (clean + standardize)
    curated = (
        df.withColumn("event_type", trim(col("event_type")))
          .withColumn("country", upper(trim(col("country"))))
          .withColumn("value", col("value").cast("double"))
    )

    # DATA QUALITY CHECKS
    row_count = curated.count()
    null_counts = {c: curated.filter(col(c).isNull()).count() for c in curated.columns}

    # ANALYTICS: total purchase value by country + event counts
    purchases = curated.filter(col("event_type") == "purchase")
    purchase_value_by_country = (
        purchases.groupBy("country")
                 .agg(_sum("value").alias("total_purchase_value"), _count("*").alias("purchase_count"))
                 .orderBy(col("total_purchase_value").desc())
    )

    event_counts = (
        curated.groupBy("event_type")
               .agg(_count("*").alias("event_count"))
               .orderBy(col("event_count").desc())
    )

    # LOAD (write curated dataset)
    curated.write.mode("overwrite").parquet(str(PARQUET_OUT))

    # Write report
    report_lines = [
        "SPARK MINI PROJECT REPORT",
        f"Generated: {datetime.now()}",
        f"Row count: {row_count}",
        f"Null counts: {null_counts}",
        f"Curated parquet output: {PARQUET_OUT}",
        "",
        "Purchase value by country (top):"
    ]

    top_purchase_rows = purchase_value_by_country.limit(10).collect()
    for r in top_purchase_rows:
        report_lines.append(f"  {r['country']}: total={r['total_purchase_value']}, count={r['purchase_count']}")

    report_lines.append("")
    report_lines.append("Event counts:")
    for r in event_counts.collect():
        report_lines.append(f"  {r['event_type']}: {r['event_count']}")

    REPORT_TXT.write_text("\n".join(report_lines), encoding="utf-8")

    # Show output in console too
    print("Purchase value by country:")
    purchase_value_by_country.show(truncate=False)

    print("Event counts:")
    event_counts.show(truncate=False)

    print("Saved curated parquet to:", PARQUET_OUT)
    print("Saved report to:", REPORT_TXT)

    spark.stop()

if __name__ == "__main__":
    main()
