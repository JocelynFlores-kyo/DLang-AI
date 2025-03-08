import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DOCUMENT_PATH = BASE_DIR / "data/raw"  # 使用绝对路径更安全