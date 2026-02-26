## 프로젝트의 목적
본 프로젝트는 파일 기반 ETL 파이프라인을 구현한 미니 데이터 엔지니어링 프로젝트입니다.
랜덤 주문 데이터를 생성하여 Raw 계층에 저장하고, Processed 계층에서 품질 플래그를 추가하여 데이터 이상 여부를 추적할 수 있도록 설계했습니다.
또한 실행 로그를 통해 데이터 품질 상태를 검증할 수 있습니다.

## 문제 정의
단순 CSV 데이터 생성이 아닌, 
실행 이력 관리 및 데이터 품질 검증이 가능한 
파일 기반 ETL 구조를 설계하는 것을 목표로 했습니다.

Raw 데이터를 보존하면서도, 
가공 계층에서 품질 상태를 추적할 수 있는 구조를 구현했습니다.

## 설계 의도
- Raw 계층과 Processed 계층을 분리하여 원천 데이터 보존 및 재처리 가능 구조를 설계했습니다.
- Processed 단계에서 품질 플래그(is_quantity_invalid)를 추가하여 데이터 이상 여부를 추적할 수 있도록 구현했습니다.
- 파일 보존 정책(keep_last)을 적용하여 실행 이력을 관리하고, 과도한 파일 적재를 방지하도록 설계했습니다.
- 실행 로그를 통해 데이터 건수 및 품질 상태를 요약하여 모니터링 가능하도록 구성했습니다.

## ETL 아키텍처 흐름도
```
generate_orders
   ↓
save (Raw)
   ↓
process_orders
   ↓
save (Processed)
   ↓
Summary Log 출력
```

## 실행 결과 예시
```
[RAW_SAVED] ..\data\raw\orders_raw\orders_raw_20260226_135023.csv
[PROCESSED_SAVED] ..\data\raw\orders_processed\orders_processed_20260226_135023.csv
[SUMMARY] rows = 1000 | invalid_quantity = 89 | missing_price = 46
```

## 데이터 품질 전략
- quantity ≤ 0 → is_quantity_invalid=True
- price 결측 허용
- 로그 기반 기대값 검증

## 향후 확장 계획
- customers / products 데이터셋 추가
- Processed 계층에 추가 품질 규칙 적용
- Parquet 저장 형식 확장
- Batch 실행 스케줄링 적용
- 고객 및 상품 엔티티를 분리하여 관계형 데이터 구조 확장

## 실행방법
``` bash
# 가상환경 활성화
python -m venv venv
venv\Scripts\activate

# 프로젝트 루트로 이동
cd etl-project
# ETL 실행
python src/generate_data.py
```

```
etl-project/
│
├─ src/
│   ├─ generate_data.py        # 데이터 생성 및 ETL 실행 진입점
│   ├─ utils.py                # 저장 및 파일 관리 로직
│
├─ data/
│   └─ raw/
│       ├─ orders_raw/         # Raw 계층 (원본 데이터)
│       └─ orders_processed/   # Processed 계층 (품질 플래그 추가 데이터)
│
└─ README.md
```
