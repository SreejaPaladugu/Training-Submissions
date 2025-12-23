from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, avg

def main():
    spark = SparkSession.builder.appName("ToySparkExample").master("local[*]").getOrCreate()

    data = [
        ("alice", "US", 100),
        ("bob", "India", 200),
        ("alice", "US", 50),
        ("cathy", "EU", 300),
    ]
    df = spark.createDataFrame(data, ["name", "region", "amount"])

    # Transformations
    df2 = (
        df.withColumn("name_upper", upper(col("name")))
          .filter(col("amount") >= 100)
          .groupBy("region")
          .agg(avg("amount").alias("avg_amount"))
          .orderBy(col("avg_amount").desc())
    )

    # Action (triggers execution)
    df2.show(truncate=False)

    spark.stop()

if __name__ == "__main__":
    main()
