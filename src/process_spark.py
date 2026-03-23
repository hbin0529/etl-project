from pathlib import Path

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F

from config import RAW_DATA_DIR, PROCESSED_DATA_DIR

def get_spark_session(app_name: str = "etl-project-spark") -> SparkSession:
    """
    SparkSession 생성
    """
    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .getOrCreate()
    )
    return spark
    

def process_orders_spark(df: DataFrame) -> DataFrame:
    """
    pandas process_orders()와 동일한 품질 검증 컬럼을 spark로 생성
    """
    processed_df = (
        df
        .withColumn("is_quantity_invalid", F.col("quantity") <= 0)
        .withColumn("is_price_missing", F.col("price").isNull())
        .withColumn("is_total_amount_invalid", F.col("total_amount") < 0)
        .withColumn(
            "quality_flag", 
            F.when(
                (F.col("quantity") <= 0)
                | (F.col("price").isNull())
                | (F.col("total_amount") < 0),
                F.lit("invalid")
            ).otherwise(F.lit("valid"))
        )
    )

    return processed_df

def find_latest_raw_orders_file() -> str:
    """
    data/raw/orders_raw/ 폴더에서 가장 최신 CSV 파일 경로를 반환
    """
    raw_dir = Path(RAW_DATA_DIR) / "orders_raw"
    files = sorted(raw_dir.glob("orders_raw_*.csv"))

    if not files:
        raise FileNotFoundError(f"raw orders 파일이 없습니다: {raw_dir}")
    
    return str(files[-1])

def save_spark_csv(df: DataFrame, output_dir: Path) -> str:
    """
    Spark DataFrame을 CSV로 저장
    Spark는 폴더 단위로 저장하므로 output_dir는 디렉토리 경로여야함.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    (
        df.write
        .mode("overwrite")
        .option("header", True)
        .csv(str(output_dir))
    )

    return str(output_dir)

def main() -> None:
    spark = get_spark_session()

    raw_file_path = find_latest_raw_orders_file()
    print(f"[SPARK_READ_RAW] {raw_file_path}")

    raw_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(raw_file_path)
    )

    processed_df = process_orders_spark(raw_df)

    output_dir = Path(PROCESSED_DATA_DIR) / "orders_processed_spark"
    saved_path = save_spark_csv(processed_df, output_dir)

    print(f"[SPARK_PROCESSED_SAVED] {saved_path}")
    print(f"[SPARK_ROW_COUNT] {processed_df.count()}")

    spark.stop()

if __name__ == "__main__":
    main()