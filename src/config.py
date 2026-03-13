from pathlib import Path
import numpy as np
import os

# 경로, 상수, 기본 설정 관리
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

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

# PostgreSQL 연결 정보
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "etl_db")