import pandas as pd
from pathlib import Path
import warnings

# 공통 저장 함수
"""
save_csv()

즉, 저장 기능만 담당
"""

# save 함수 정의
def save_csv(
    df: pd.DataFrame,
    base_dir = Path, 
    prefix = "dataset", 
    keep_last: int = 50
) -> str:
    """    
    df를 base_dir/prefix 폴더에 prefix_YYYYMMDD_HHMMSS.csv 형태로 저장하고,
    동일 prefix 파일이 keep_last 개수 초과하면 오래된 파일부터 삭제한다.
    """
    # keep_last 방어: 3 미만이면 3으로 보정 + 워닝
    if keep_last < 3:
        warnings.warn(
            f"keep_last={keep_last} 의 개수가 3 미만이므로 3으로 보정합니다. (최소 3개의 파일은 유지)",
            category=UserWarning
        )
        keep_last = 3

    # prefix 별 폴더 분리
    save_dir = Path(base_dir) / prefix
    save_dir.mkdir(parents=True, exist_ok=True)

    # 2. timestamp 만들기(YYYYMMDD_HHMMSS)
    # now = pd.Timestamp.now()
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S") # 20260223_112542
    # timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")

    # 3. 파일명 / 경로 만들기
    filename = f"{prefix}_{timestamp}.csv"
    file_path = save_dir / filename

    # 4. 저장 (인덱스 저장 안함)
    # utf-8-sig : BOM을 포함 * 개발자노트 작성하라고좀
    df.to_csv(file_path, index=False, encoding="utf-8-sig") 

    # 5. cleanup : 해당 prefix 폴더 안에서  prefix_*.csv 파일만 모아서 오래된 것 삭제
    files = sorted(save_dir.glob(f"{prefix}_*.csv"))
    excess = len(files) - keep_last

    if excess > 0:
        for old_file in files[:excess]:
            old_file.unlink()
    
    # 6. 저장된 경로 반환
    return str(file_path)