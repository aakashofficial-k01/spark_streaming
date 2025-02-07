from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, expr
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType


def create_spark_session():
    return SparkSession.builder \
        .appName("StreamJoins") \
        .config("spark.streaming.stopGracefullyOnShutdown", True) \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2") \
        .getOrCreate()


def create_kafka_read_stream(spark, topic, schema):
    return spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", topic) \
        .option("startingOffsets", "earliest") \
        .load() \
        .select(from_json(col("value").cast("string"), schema).alias("data")) \
        .selectExpr("data.*")


def main():
    spark = create_spark_session()

    # Define schemas
    order_schema = StructType([
        StructField("order_id", StringType()),
        StructField("amount", IntegerType()),
        StructField("timestamp", TimestampType())
    ])

    payment_schema = StructType([
        StructField("order_id", StringType()),
        StructField("payment_amount", IntegerType()),
        StructField("timestamp", TimestampType())
    ])

    # Create streams
    orders = create_kafka_read_stream(spark, "orders", order_schema) \
        .withWatermark("timestamp", "30 seconds")

    payments = create_kafka_read_stream(spark, "payments", payment_schema) \
        .withWatermark("timestamp", "30 seconds")

    # Inner Join
    inner_join = orders.alias("o").join(
        payments.alias("p"),
        expr("""
            o.order_id = p.order_id AND
            o.timestamp BETWEEN p.timestamp - INTERVAL 1 MINUTE AND p.timestamp + INTERVAL 1 MINUTE
        """),
        "inner"
    )

    # Left Outer Join
    left_join = orders.alias("o").join(
        payments.alias("p"),
        expr("""
            o.order_id = p.order_id AND
            o.timestamp BETWEEN p.timestamp - INTERVAL 1 MINUTES AND p.timestamp + INTERVAL 1 MINUTE
        """),
        "left_outer"
    )

    # left_join = left_join.filter("p.order_id = '3931'")
    # Choose which join to run
    query = left_join.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()


if __name__ == "__main__":
    main()