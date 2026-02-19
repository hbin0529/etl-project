import pandas as pd
import numpy as np

# generate_orders 함수 정의
# 직접 데이터 입력
def generate_orders():
    pass

data = {
    # 주문번호
    "order_id": [1, 2, 3, 4, 5],

    # 주문자
    "customer_id": ["C001", "C002", "", "C004", None],

    # 주문일자:
    "order_date": [
        "2025-01-10",
        "2025-01-11",
        "",                 # 결측
        "2025-01-13",
        "2025-01-14"
    ],
    # 상품명
    "product": [
        "Laptop",
        "Mouse",
        "Keyboard",
        "Monitor",
        ""
    ],
    # 카테고리
    "category": [
        "Electronics",
        "Electronics",
        "Electronics",
        "",
        "Accessories"
    ],
    # 가격: 정상 + NaN
    "price": [
        1200.0,
        25.5,
        np.nan,   # NaN
        300.0,
        -50.0     # 이상값(음수)
    ],
    # 수량
    "quantity": [
        1,
        2,
        0,    # 이상값
        -1,   # 이상값
        3
    ],
    # 총 금액
    "total_amount": [
        1200.0,    # 정상
        51.0,      # 정상
        0.0,       # 계산 불가 (price NaN)
        -300.0,    # 잘못된 값
        None       # 결측
    ],
}

df = pd.DataFrame(data)

# save 함수 정의
def save():
    pass

# main 함수
def main():
    print(df)

if __name__ == "__main__":
    main()

####### 랜덤 데이터 전략 세우기 #######
# 날짜는 어떻게 랜덤 생성할 건가?

# 상품은 리스트로 둘 건가?

# 카테고리는 매핑할 건가?

# 가격은 정수? float?

# 수량 범위는?

# 일부 결측치는 어떻게 넣을 건가?