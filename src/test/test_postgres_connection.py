from sqlalchemy import create_engine, text
from config import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
)

def main():
    db_url = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    engine = create_engine(db_url)

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 AS connected"))
        row = result.fetchone()
        print(row)

if __name__ == "__main__":
    main()