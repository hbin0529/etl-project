from generate import generate_orders
from process import process_orders
from utils import save_csv
from load_postgres import load_orders_to_postgres
from config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from mart import build_daily_sales_summary

# 전체 ETL 실행 순서 제어
"""
main()

즉, 실행 순서 orchestration
"""

def main() -> None:
    # raw 생성
    raw_orders = generate_orders(n_rows = 1000, seed = 42)

    # raw 저장
    raw_path = save_csv(
        df = raw_orders, 
        base_dir = RAW_DATA_DIR, 
        prefix = "orders_raw",
    )

    # processed 생성
    processed_orders = process_orders(raw_orders)

    # processed 저장
    processed_path = save_csv(
        processed_orders, 
        base_dir = PROCESSED_DATA_DIR,
        prefix="orders_processed",
    )

    # PostgreSQL 적재
    load_orders_to_postgres(
        df = processed_orders, 
        table_name = "orders_processed",
        if_exists = "replace",
    )

    build_daily_sales_summary()

    # summary 로그 출력
    rows = processed_orders.shape[0]
    invalid_quantity_count = int(processed_orders["is_quantity_invalid"].sum())
    missing_price_count = int(processed_orders["price"].isna().sum())
    invalid_total_amount_count = int(processed_orders["is_total_amount_invalid"].sum())
    invalid_rows_count = int((processed_orders["quality_flag"] == "invalid").sum())

    # f-string 사용
    summary_log = (
        f"[SUMMARY] rows = {rows} | " 
        f"invalid_quantity = {invalid_quantity_count} | "
        f"missing_price = {missing_price_count} | " 
        f"invalid_total_amount_count = {invalid_total_amount_count} | "
        f"invalid_rows_count = {invalid_rows_count} "

    )
    
    print(f"[RAW_SAVED] {raw_path}")
    print(f"[PROCESSED_SAVED] {processed_path}")
    print(summary_log)


if __name__ == "__main__":
    main()
