# 02_pyspark_cleaning.py
# Milestone 3: PySpark Data Cleaning and Feature Engineering
# Author: Aditya Mandlik

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import col, split, to_date, year, month, regexp_extract, when, size, trim

def main():
    # Initialize SparkSession on EMR
    spark = SparkSession.builder \
        .appName("NetflixDataCleaning") \
        .getOrCreate()

    # 1. Explicit Schema Definition
    schema = StructType([
        StructField("show_id", StringType(), True),
        StructField("type", StringType(), True),
        StructField("title", StringType(), True),
        StructField("director", StringType(), True),
        StructField("cast", StringType(), True),
        StructField("country", StringType(), True),
        StructField("date_added", StringType(), True),
        StructField("release_year", IntegerType(), True),
        StructField("rating", StringType(), True),
        StructField("duration", StringType(), True),
        StructField("listed_in", StringType(), True),
        StructField("description", StringType(), True)
    ])

    # Load raw dataset from HDFS
    raw_df = spark.read.csv("hdfs:///user/hadoop/data/netflix_titles.csv", header=True, schema=schema)

    # 2. Null Handling
    clean_df = raw_df.fillna({
        "director": "Unknown",
        "cast": "Unknown",
        "country": "Unknown"
    }).dropna(subset=["date_added", "rating", "duration"])

    # 3. Deduplication
    clean_df = clean_df.dropDuplicates(["show_id"])

    # 4. Date Parsing
    clean_df = clean_df.withColumn("date_added_parsed", to_date(trim(col("date_added")), "MMMM d, yyyy"))

    # 5. Feature Engineering (Adding 8 new columns)
    engineered_df = clean_df \
        .withColumn("year_added", year(col("date_added_parsed"))) \
        .withColumn("month_added", month(col("date_added_parsed"))) \
        .withColumn("country_primary", trim(split(col("country"), ",")[0])) \
        .withColumn("genre_primary", trim(split(col("listed_in"), ",")[0])) \
        .withColumn("genre_count", size(split(col("listed_in"), ","))) \
        .withColumn("duration_int", regexp_extract(col("duration"), "(\\d+)", 1).cast("int")) \
        .withColumn("duration_type", when(col("type") == "Movie", "minutes").otherwise("seasons"))
    
    # 6. Export Cleaned Dataset to HDFS
    # Using coalesce(1) to produce a single CSV file for downstream Tableau and Pandas consumption
    engineered_df.coalesce(1).write.csv("hdfs:///user/hadoop/netflix_processed/", header=True, mode="overwrite")

    print(f"Data cleaning complete. Total output rows: {engineered_df.count()}")
    spark.stop()

if __name__ == "__main__":
    main()
