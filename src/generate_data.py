import pandas as pd
import numpy as np

# generate_orders 함수 정의
# 직접 데이터 입력
# 상수는 소문자 -> 대문자로 입력하기
PRODUCTS = np.array([
    "KeyBoard",
    "Mouse", 
    "Computer", 
    "Vacuum",
    "Ring", 
    "Necklace", 
    "Notebook", 
    "Sofa", 
    "Bed",
    ])
CATEGORY_MAPPING = {
    "KeyBoard": "Electronics",
    "Mouse": "Electronics",
    "Computer": "Electronics",
    "Vacuum": "Electronics",
    "Ring":"Accessories",
    "Necklace":"Accessories",
    "Notebook":"Office",
    "Sofa":"Furniture",
    "Bed":"Furniture",
}

def generate_orders(n_rows: int, seed: int | None = None) -> pd.DataFrame:
    if seed is not None:
        np.random.seed(seed)

    order_id = np.arange(1, n_rows + 1)

    customer_raw = np.random.randint(1, 101, n_rows)

    # 기존 customer_id : int -> str 변경 및 구조 변형
    # customer_id = np.random.randint(1, 101, n_rows)
    # customer_id = "C" + pd.Series(customer_id).astype(str).str.zfill(3)  # -> object
    customer_id = (
        pd.Series(customer_raw)
        .astype(str)
        .str.zfill(3)
        .radd("C")
    )
    # print('customer_id_str의 데이터 타입은 ?? :', customer_id_str.dtype)
    # print('customer_id_str2의 데이터 타입은 ?? :', customer_id_str2.dtype)
    # print('customer_id_str3의 데이터 타입은 ?? :', customer_id_str3.dtype)

    today = pd.Timestamp.today().normalize() # .normalize() 추가 : 시간 제거(날짜만 유지)
    random_days = np.random.randint(0, 365, n_rows)
    order_date = today - pd.to_timedelta(random_days, unit="D")

    product = np.random.choice(PRODUCTS, size = n_rows)

    category = pd.Series(product).map(CATEGORY_MAPPING)

    price = np.random.uniform(10, 10000, n_rows)
    price[np.random.rand(n_rows) < 0.05] = np.nan
    # mask = np.random.rand(n_rows) < 0.05
    # price[mask] = np.nan


    quantity = np.random.randint(1, 6, n_rows)
    # mask_zero = np.random.rand(n_rows) < 0.1
    # quantity[mask_zero] = 0
    quantity[np.random.rand(n_rows) < 0.1] = 0


    # mask_error = np.random.rand(n_rows) < 0.03
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
    # print(df.dtypes)
    # print(type(df["price"]))
    return df

# save 함수 정의
def save(df, base_dir = "data/raw/", prefix = "raw_orders", keep_last = 50):
    """
    저장 위치
    data/raw/

    파일명 규칙
    raw_orders_YYYYMMDD_HHMMSS.csv

    저장 옵션 
    index = False
    encoding = "utf-8-sig" 고려

    파일관리
    최근 N개만 유지 방식
    예: 최근 50개만 유지하고 나머지 삭제 -> 보통 실무에서 7일, 30일 단위로 유지
    """

    

    pass

# main 함수
def main():
    df = generate_orders(1000)
    print(df.head())

if __name__ == "__main__":
    main()

####### 랜덤 데이터 전략 세우기 #######
# 날짜는 어떻게 랜덤 생성할 건가?

# 상품은 리스트로 둘 건가?

# 카테고리는 매핑할 건가?

# 가격은 정수? float?

# 수량 범위는?

# 일부 결측치는 어떻게 넣을 건가?