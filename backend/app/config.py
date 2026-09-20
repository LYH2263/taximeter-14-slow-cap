import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("DATA_DIR", Path(__file__).resolve().parent.parent / "data"))
DB_FILENAME = "app.db"

# 低速费上限默认值（正数）；设置缺失或非法时回退到此值
DEFAULT_SLOW_FEE_CAP = 50.0
