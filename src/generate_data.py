import pandas as pd
import numpy as np
from pathlib import Path
from utils import save

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
def save_old(df: pd.DataFrame, base_dir = "../data/raw", prefix = "dataset222", keep_last = 50) -> str:
    """    
    df를 base_dir에 prefix_YYYYMMDD_HHMMSS.csv 형태로 저장하고, 
    동일 prefix 파일이 keep_last 개수 초과하면 오래된 것부터 삭제한다.
    return: 저장된 파일 경로(str)
    """
    """
    저장 위치
    data/raw/

    저장 옵션 
    index = False
    encoding = "utf-8-sig" 고려
    """

    # 1. base_dir 폴더 준비
    base_path = Path(base_dir) # base_dir = data/raw
    base_path.mkdir(parents=True, exist_ok=True)
    # base_dir.mkdir(parents=True, exist_ok=True)

    # 2. timestamp 만들기(YYYYMMDD_HHMMSS)
    now = pd.Timestamp.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S") # 20260223_112542
    # timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    # now.strftime("%Y%m%d_%H%M%S")

    # 3. 파일명 / 경로 만들기
    filename = f"{prefix}_{timestamp}.csv"
    file_path = base_path / filename

    # 4. 저장 (인덱스 저장 안함)
    # utf-8-sig : BOM을 포함하여 눈에 보이지 않는 특정 byte를 넣은 다음 이것을 해석하여 
    #             정확히 어떤 인코딩 방식이 사용 되었는지 알아내는 방법을 나타냄
    df.to_csv(file_path, index=False, encoding="utf-8-sig") 

    # df.to_csv(filename)

    # 5. cleanup : prefix_*.csv 파일만 모아서 오래된 것 삭제
    files = list(base_dir.glob(f"{prefix}_*.csv"))
    files.sort()

    excess = len(files) - keep_last
    if excess > 0:
        for old_file in files[:excess]:
            old_file.unlink()
    
    # 6. 저장된 경로 반환
    
    return str(file_path)

# main 함수
def main():
    # df = generate_orders(1000)
    # print(df.head())
    orders = generate_orders(1000)
    # print(orders.head())
    # print(orders.shape)
    # print(orders.isna().sum())

    save_path = save(orders, prefix="orders")
    print(f"저장 완료: {save_path}")

if __name__ == "__main__":
    main()

####### 랜덤 데이터 전략 세우기 #######
# 날짜는 어떻게 랜덤 생성할 건가?

# 상품은 리스트로 둘 건가?

# 카테고리는 매핑할 건가?

# 가격은 정수? float?

# 수량 범위는?

# 일부 결측치는 어떻게 넣을 건가?