import pandas as pd
from pathlib import Path

# save 함수 정의
def save(df: pd.DataFrame, base_dir = "../data/raw", prefix = "dataset", keep_last = 1) -> str:
    """    
    df를 base_dir에 prefix_YYYYMMDD_HHMMSS.csv 형태로 저장하고, 
    동일 prefix 파일이 keep_last 개수 초과하면 오래된 것부터 삭제한다.
    return: 저장된 파일 경로(str)
    """
    # 1. base_dir 폴더 준비
    base_path = Path(base_dir) # base_dir = ../data/raw
    base_path.mkdir(parents=True, exist_ok=True)

    # 2. timestamp 만들기(YYYYMMDD_HHMMSS)
    now = pd.Timestamp.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S") # 20260223_112542
    # timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")

    # 3. 파일명 / 경로 만들기
    filename = f"{prefix}_{timestamp}.csv"
    file_path = base_path / filename

    # 4. 저장 (인덱스 저장 안함)
    # utf-8-sig : BOM을 포함 * 개발자노트 작성하라고좀
    df.to_csv(file_path, index=False, encoding="utf-8-sig") 

    # 5. cleanup : prefix_*.csv 파일만 모아서 오래된 것 삭제
    files = list(base_path.glob(f"{prefix}_*.csv"))
    files.sort()

    excess = len(files) - keep_last
    if excess > 0:
        for old_file in files[:excess]:
            old_file.unlink()
    
    # 6. 저장된 경로 반환
    return str(file_path)
    # df.to_csv(filename)
    
    # now.strftime("%Y%m%d_%H%M%S")
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
