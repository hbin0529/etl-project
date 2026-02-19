import pandas as pd
import numpy as np

# generate_orders 함수 정의
# 직접 데이터 입력
products = np.array(["KeyBoard", "Mouse", "Computer", "Laptop"])
mapping = {
    "KeyBoard": "Electronics",
    "Mouse": "Electronics",
    "Computer": "Electronics",
    "Laptop": "Electronics",
}

def generate_orders(n_rows):
    order_id = np.arange(1, n_rows + 1)

    customer_id = np.random.randint(1, 101, n_rows)

    today = pd.Timestamp.today()
    random_days = np.random.randint(0, 365, n_rows)
    order_date = today - pd.to_timedelta(random_days, unit="D")

    product = np.random.choice(products, size = n_rows)

    category = pd.Series(product).map(mapping).values

    price = np.random.uniform(10, 10000, n_rows)
    mask = np.random.rand(n_rows) < 0.05
    price[mask] = np.nan

    quantity = np.random.randint(1, 6, n_rows)
    mask_zero = np.random.rand(n_rows) < 0.1
    quantity[mask_zero] = 0

    total_amount = price * quantity

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

# save 함수 정의
def save():
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