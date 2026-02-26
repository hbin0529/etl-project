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
