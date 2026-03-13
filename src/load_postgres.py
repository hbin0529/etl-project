import pandas as pd
from sqlalchemy import create_engine

from config import(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
)

def get_postgres_engine():
    """
    PostgreSQL SQLAlchemy 앤진 생성
    """
    db_url = (
        # postgresql+psycopg2://유저:비밀번호@호스트:포트/DB명
        # postgresql+psycopg2://postgres:postgres@localhost:5432/etl_db
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    engine = create_engine(db_url)
    return engine

def load_orders_to_postgres(
        df: pd.DataFrame, 
        table_name: str = "orders_processed",
        if_exists: str = "replace",
) -> None:
    """
    DataFrame을 PostgreSQL 테이블로 적재한다. 

    Parameters
    ----------
    df: pd.DataFrame
        적재할 데이터프레임
    table_name: str
        적재 대상 테이블명
    if_exists: str
        테이블이 이미 존재할 경우 처리 방식
        - replace: 기존 테이블 삭제 후 재생성
        - append: 기존 테이블에 데이터 추가
    """
    engine = get_postgres_engine()

    df.to_sql(
        name = table_name,
        con = engine,
        if_exists = if_exists,
        index = False,
    )

    print(f"[DB_LOAD_SUCCESS] table = {table_name} | rows = {len(df)} | mode = {if_exists}")