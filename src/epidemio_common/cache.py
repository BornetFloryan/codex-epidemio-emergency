from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_DB_PATH = "data/epidemio_cache.sqlite"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS api_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill TEXT NOT NULL,
                query TEXT NOT NULL,
                status TEXT NOT NULL,
                result_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_api_query(
    skill: str,
    query: str,
    status: str,
    result: dict[str, Any],
    db_path: str = DEFAULT_DB_PATH,
) -> bool:
    try:
        init_db(db_path)
        with sqlite3.connect(db_path) as conn:
            conn.execute(
                """
                INSERT INTO api_queries (skill, query, status, result_json, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    skill,
                    query,
                    status,
                    json.dumps(result, ensure_ascii=False),
                    utc_now_iso(),
                ),
            )
            conn.commit()
        return True
    except sqlite3.Error:
        return False


def list_recent_queries(limit: int = 10, db_path: str = DEFAULT_DB_PATH) -> list[dict[str, Any]]:
    init_db(db_path)

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT id, skill, query, status, result_json, created_at
            FROM api_queries
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    results = []
    for row in rows:
        results.append(
            {
                "id": row["id"],
                "skill": row["skill"],
                "query": row["query"],
                "status": row["status"],
                "result_json": json.loads(row["result_json"]),
                "created_at": row["created_at"],
            }
        )

    return results