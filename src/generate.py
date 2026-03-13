import pandas as pd
import numpy as np

from config import PRODUCTS, CATEGORY_MAPPING

# 원천 데이터 생성
"""
generate_orders()

즉, 데이터 생성만 담당
"""

def generate_orders(n_rows: int, seed: int | None = None) -> pd.DataFrame:
    """
    랜덤 주문 데이터를 생성한다.
     - 일부 price는 결축치
     - 일부 quantity는 0 
     - 일부 total_amount는 음수
    """
    if seed is not None:
        np.random.seed(seed)

    order_id = np.arange(1, n_rows + 1)

    customer_raw = np.random.randint(1, 101, n_rows)
    # 기존 customer_id : int -> str 변경 및 구조 변형
    customer_id = (
        pd.Series(customer_raw)
        .astype(str)
        .str.zfill(3)
        .radd("C")
    )

    today = pd.Timestamp.today().normalize() # .normalize() 추가 : 시간 제거(날짜만 유지)
    random_days = np.random.randint(0, 365, n_rows)
    order_date = today - pd.to_timedelta(random_days, unit="D")

    product = np.random.choice(PRODUCTS, size = n_rows)
    category = pd.Series(product).map(CATEGORY_MAPPING)

    price = np.random.uniform(10, 10000, n_rows)
    price[np.random.rand(n_rows) < 0.05] = np.nan

    quantity = np.random.randint(1, 6, n_rows)
    quantity[np.random.rand(n_rows) < 0.1] = 0

    total_amount = price * quantity
    total_amount[np.random.rand(n_rows) < 0.03] *= -1

    # DataFrame
    df = pd.DataFrame({
        "order_id": order_id,
        "customer_id": customer_id,
        "order_date": order_date,
        "product": product,
        "category": category,
        "price": price,
        "quantity": quantity,
        "total_amount": total_amount
    })

    return df