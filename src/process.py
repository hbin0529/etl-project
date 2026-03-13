import pandas as pd
import numpy as np

# raw -> processed 가공
"""
process_orders()
필요하면 나중에 summarize_orders() 같은 함수 추가

즉, 가공 / 품질 플래그 생성 담당
"""

def process_orders(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    raw 주문 데이터를 가공하고 품질 검증용 컬럼을 추가한다.
    """
    df = raw_df.copy()

    # is_quantity_invalid 컬럼 추가
    df["is_quantity_invalid"] = df["quantity"] <= 0
    df["is_price_missing"] = df["price"] < 0
    df["is_total_amount_invalid"] = df["total_amount"] < 0

    df["quality_flag"] = np.where(
        df["is_quantity_invalid"] |
        df["is_price_missing"] |
        df["is_total_amount_invalid"],
        "invalid",
        "valid"
    )

    return df