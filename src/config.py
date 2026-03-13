from pathlib import Path
import numpy as np

# 경로, 상수, 기본 설정 관리
"""
BASE_DIR
DATA_DIR
RAW_DATA_DIR
PROCESSED_DATA_DIR

상품 목록
카테고리 매핑

즉, 설정값 / 상수 전용
"""
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