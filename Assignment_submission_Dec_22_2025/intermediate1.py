from pathlib import Path
import csv
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
CSV_PATH = DATA_DIR / "sales.csv"

def create_csv_if_missing():
    if CSV_PATH.exists():
        return
    rows = [
        ["order_id", "region", "product", "price", "quantity"],
        [1, "US", "Laptop", 900, 1],
        [2, "India", "Phone", 600, 2],
        [3, "US", "Laptop", 950, 1],
        [4, "India", "Tablet", 400, 1],
        [5, "EU", "Monitor", 300, 3],
        [6, "US", "Phone", 650, 1],
    ]
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def main():
    create_csv_if_missing()

    spark = SparkSession.builder.appName("SparkRealDataset").master("local[*]").getOrCreate()

    df = (
        spark.read
             .option("header", True)
             .option("inferSchema", True)
             .csv(str(CSV_PATH))
    )

    # Transform: compute revenue
    df2 = df.withColumn("revenue", col("price") * col("quantity"))

    # Results: revenue by region + top products
    revenue_by_region = (
        df2.groupBy("region")
           .agg(_sum("revenue").alias("total_revenue"))
           .orderBy(col("total_revenue").desc())
    )

    revenue_by_product = (
        df2.groupBy("product")
           .agg(_sum("revenue").alias("total_revenue"))
           .orderBy(col("total_revenue").desc())
    )

    print("Revenue by region:")
    revenue_by_region.show(truncate=False)

    print("Revenue by product:")
    revenue_by_product.show(truncate=False)

    spark.stop()

if __name__ == "__main__":
    main()
