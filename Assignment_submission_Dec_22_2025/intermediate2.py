from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator

CSV_PATH = Path("data/sales.csv")

def main():
    spark = SparkSession.builder.appName("SparkMLlib").master("local[*]").getOrCreate()

    df = (
        spark.read
             .option("header", True)
             .option("inferSchema", True)
             .csv(str(CSV_PATH))
             .withColumn("revenue", col("price") * col("quantity"))
    )

    # Features: region (categorical), product (categorical), price & quantity (numeric)
    region_idx = StringIndexer(inputCol="region", outputCol="region_idx", handleInvalid="keep")
    product_idx = StringIndexer(inputCol="product", outputCol="product_idx", handleInvalid="keep")

    encoder = OneHotEncoder(
        inputCols=["region_idx", "product_idx"],
        outputCols=["region_ohe", "product_ohe"]
    )

    assembler = VectorAssembler(
        inputCols=["region_ohe", "product_ohe", "price", "quantity"],
        outputCol="features"
    )

    lr = LinearRegression(featuresCol="features", labelCol="revenue")

    pipeline = Pipeline(stages=[region_idx, product_idx, encoder, assembler, lr])

    train_df, test_df = df.randomSplit([0.7, 0.3], seed=42)
    model = pipeline.fit(train_df)

    preds = model.transform(test_df)

    evaluator = RegressionEvaluator(labelCol="revenue", predictionCol="prediction", metricName="mae")
    mae = evaluator.evaluate(preds)

    print("MAE (lower is better):", round(mae, 2))
    preds.select("region", "product", "price", "quantity", "revenue", "prediction").show(truncate=False)

    spark.stop()

if __name__ == "__main__":
    main()
