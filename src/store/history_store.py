from __future__ import annotations
import json
import os
import time
import hashlib
from dataclasses import dataclass, asdict
from typing import List, Optional
from filelock import FileLock

HISTORY_PATH = os.path.join("data", "history.jsonl")
LOCK_PATH = HISTORY_PATH + ".lock"

@dataclass
class HistoryItem:
    ts: int
    company: str
    source_name: str
    fulltext_sha: str
    model: str
    oibook_md: str

def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()[:16]

def append_history(company: str, source_name: str, fulltext: str, model: str, oibook_md: str) -> HistoryItem:
    os.makedirs("data", exist_ok=True)
    item = HistoryItem(
        ts=int(time.time()),
        company=company,
        source_name=source_name,
        fulltext_sha=_sha(fulltext),
        model=model,
        oibook_md=oibook_md,
    )
    with FileLock(LOCK_PATH):
        with open(HISTORY_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(item), ensure_ascii=False) + "\n")
    return item

def load_history(limit: int = 200) -> List[HistoryItem]:
    if not os.path.exists(HISTORY_PATH):
        return []
    items: List[HistoryItem] = []
    with FileLock(LOCK_PATH):
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    items.append(HistoryItem(**d))
                except Exception:
                    continue
    items.sort(key=lambda x: x.ts, reverse=True)
    return items[:limit]
