from sqlalchemy import text

from load_postgres import get_postgres_engine

def build_daily_sales_summary() -> None:
    """
    orders_processed 테이블을 기준으로
    daily_sales_summary 마트 테이블을 생성한다.
    """
    engine = get_postgres_engine()

    drop_sql = """
    DROP TABLE IF EXISTS daily_sales_summary;
    """

    create_sql = """
    CREATE TABLE daily_sales_summary AS
    SELECT 
        order_date::date as order_date
      , COUNT(*) as total_orders
      , SUM(CASE WHEN quality_flag = 'valid' THEN 1 ELSE 0 END) AS valid_orders
      , SUM(CASE WHEN quality_flag = 'invalid' THEN 1 ELSE 0 END) AS invalid_orders
      , COALESCE(
            SUM(CASE WHEN quality_flag = 'valid' THEN total_amount ELSE 0 END ), 
            0
        ) AS total_revenue
      , COALESCE(
            AVG(CASE WHEN quality_flag = 'valid' THEN  total_amount END), 
            0
        ) AS avg_order_amount
    FROM orders_processed
    GROUP BY order_date::date
    ORDER BY order_date::date;
    """

    with engine.begin() as conn:
        conn.execute(text(drop_sql))
        conn.execute(text(create_sql))

    print("[MART_BUILD_SUCCESS] table = daily_sales_summary")