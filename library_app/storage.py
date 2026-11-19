"""Validated JSON persistence with safe recovery and atomic writes."""
import json
import os
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_FILE = DATA_DIR / "library.json"

DEFAULT_DB = {"books": [], "members": [], "transactions": []}

def load_data(path=DB_FILE):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        save_data(DEFAULT_DB, path)
        return json.loads(json.dumps(DEFAULT_DB))
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("Database root must be an object.")
        for key in DEFAULT_DB:
            if key not in data or not isinstance(data[key], list):
                raise ValueError(f"Invalid or missing '{key}' collection.")
        return data
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
        backup = path.with_suffix(path.suffix + ".corrupt-" + datetime.now().strftime("%Y%m%d%H%M%S"))
        try:
            os.replace(path, backup)
        except OSError:
            pass
        print(f"\n[WARNING] Data file was invalid ({exc}). A fresh database was created.")
        print(f"[WARNING] Original file backup: {backup.name}")
        save_data(DEFAULT_DB, path)
        return json.loads(json.dumps(DEFAULT_DB))

def save_data(data, path=DB_FILE):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, path)
