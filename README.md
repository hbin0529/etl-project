# ETL Project

## 프로젝트 개요
본 프로젝트는 **데이터 엔지니어 포트폴리오용 ETL 파이프라인 프로젝트**입니다.  
랜덤 주문 데이터를 생성한 뒤, Raw / Processed 계층으로 분리 저장하고,  
품질 검증 컬럼을 추가한 후 PostgreSQL에 적재하여 **분석용 데이터 마트**까지 생성하는 흐름을 구현했습니다.

단순 CSV 생성 스크립트가 아니라,  
**원천 데이터 보존 → 정제 → 적재 → 집계 마트 생성**의 흐름을 갖춘  
미니 데이터 파이프라인을 목표로 설계했습니다.

## 프로젝트 목적
이 프로젝트의 목적은 다음과 같습니다.

- 파일 기반 ETL 구조를 직접 설계하고 구현
- Raw / Processed 데이터 레이어 분리
- 데이터 품질 검증 로직 추가
- PostgreSQL 적재를 통한 서빙 계층 구성
- 집계 마트 생성 과정을 통해 데이터 엔지니어링 흐름 학습
- 추후 Spark / Airflow 기반 구조로 확장 가능한 포트폴리오 기반 마련

---

## 기술 스택
- Python
- pandas
- numpy
- PostgreSQL
- SQLAlchemy

## 문제 정의
단순 CSV 파일을 생성하고 끝내는 것이 아니라, 
다음곽 ㅏㅌ은 데이터 엔지니어링 관점의 문제를 해결하는 것을 목표로 했습니다.

1. **원천 데이터(raw)를 어떻게 보존할 것인가**
2. **가공 데이터(processed)에 품질 상태를 어떻게 반영할 것인가**
3. **가공된 데이터를 어떻게 PostgreSQL에 적재할 것인가**
4. **정제된 상세 데이터로부터 분석용 집계 마트를 어떻게 생성할 것인가**
5. **향후 Spark / Airflow 환경으로 확장 가능한 구조를 어떻게 미리 설계할 것인가**

---

## 현재 구현 범위

### 1. 주문 데이터 생성
- Python / pandas / numpy 기반 랜덤 주문 데이터 생성
- `order_id`, `customer_id`, `order_date`, `product`, `category`, `price`, `quantity`, `total_amount` 컬럼 구성

### 2. Raw / Processed 레이어 분리
- Raw 계층: 원천 주문 데이터 저장
- Processed 계층: 품질 검증 컬럼이 추가된 정제 데이터 저장

### 3. 데이터 품질 검증
Processed 단계에서 아래 품질 검증 컬럼을 생성합니다.

- `is_quantity_invalid`
- `is_price_missing`
- `is_total_amount_invalid`
- `quality_flag`

### 4. PostgreSQL 적재
- Processed 데이터를 PostgreSQL `orders_processed` 테이블에 적재
- 초기 단계에서는 `replace` 방식으로 전체 적재

### 5. 집계 마트 생성
- `orders_processed`를 기반으로 `daily_sales_summary` 테이블 생성
- 일자별 주문 수 / 유효 주문 수 / 비정상 주문 수 / 총매출 / 평균 주문금액 집계

### 6. Spark 설계 및 파일 초안 작성 완료
- Pandas 기반 처리 로직 구현 완료
- Spark DataFrame 기반 처리 초안 완성
- Windows 로컬 환경의 Hadoop dependency 이슈로 인해 실행 환경은 추후 macOS/WSL 기준으로 정리 예정
---

## 설계 의도

### Raw / Processed 분리
원천 데이터를 보존하여 재처리 가능성을 확보하고,  
가공 데이터와 원본 데이터를 명확히 분리하기 위해 Raw / Processed 레이어를 나눴습니다.

### 품질 검증 컬럼 추가
정제 과정에서 단순히 데이터를 제거하지 않고,  
**어떤 데이터가 왜 비정상인지 추적할 수 있도록** 품질 검증 컬럼을 별도로 추가했습니다.

### 파일 저장 이력 관리
실행 시점별 CSV 파일을 timestamp 기반으로 저장하고,  
`keep_last` 정책으로 과도한 파일 적재를 방지할 수 있도록 설계했습니다.

### PostgreSQL 적재
가공 결과를 파일로만 두지 않고,  
PostgreSQL에 적재하여 **조회 가능한 서빙 계층**을 구성했습니다.

### 데이터 마트 생성
정제된 상세 데이터(`orders_processed`)와  
분석용 집계 데이터(`daily_sales_summary`)를 분리함으로써  
데이터 레이어 개념을 반영했습니다.

---


## ETL 아키텍처 흐름

### 현재 구현 구조
```
generate_orders
   ↓
save_csv (Raw)
   ↓
process_orders
   ↓
save_csv (Processed)
   ↓
load_orders_to_postgres
   ↓
build_daily_sales_summary
   ↓
Summary Log 출력
```

### 목표 아키텍처 (확장 방향)
```
Log Generator (Python)
   ↓
Raw Layer
   ↓
Spark Processing
   ↓
PostgreSQL Data Mart
   ↓
Airflow DAG
```

## 프로젝트 구조
```text
etl-project/
│
├─ src/
│   ├─ config.py
│   ├─ generate.py
│   ├─ process.py
│   ├─ utils.py
│   ├─ load_postgres.py
│   ├─ mart.py
│   └─ main.py
│
├─ data/
│   ├─ raw/
│   │   └─ orders_raw/
│   └─ processed/
│       └─ orders_processed/
│
├─ requirements.txt
└─ README.md
```

## 실행 방법

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

## 실행 결과 예시
```
[DB_LOAD_SUCCESS] table=orders_processed | rows=1000 | mode=replace
[MART_BUILD_SUCCESS] table=daily_sales_summary
[RAW_SAVED] ..\data\raw\orders_raw\orders_raw_20260321_165939.csv
[PROCESSED_SAVED] ..\data\processed\orders_processed\orders_processed_20260321_165939.csv
[SUMMARY] rows=1000 | invalid_quantity=113 | missing_price=50 | invalid_total_amount=25 | invalid_rows=138
```
## 향후 확장 계획
