import sqlite3
import sqlite_vec
import numpy as np
import os
import json
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer

def _connect(db_path: str) -> sqlite3.Connection:
    db = sqlite3.connect(db_path, check_same_thread=False)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    return db

def create_db(
    db_path: str,
    texts: list[str],
    ids: list[str],
    metadatas: list[dict],
    vectors: np.ndarray,  # shape (N, dims)
    replace: bool=False,
) -> sqlite3.Connection:
    """ Create a database and return a connection """

    if os.path.exists(db_path):
        if not replace:
            raise Exception(f"database already exists: {db_path}")
        os.remove(db_path)

    db = _connect(db_path)
    dims = vectors.shape[1]
    vectors = vectors.astype(np.float32)

    db.executescript(f"""
        CREATE TABLE IF NOT EXISTS docs (
            id      TEXT PRIMARY KEY,
            text    TEXT NOT NULL,
            metadata TEXT NOT NULL   -- stored as JSON
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS vec_index USING vec0(
            id      TEXT PRIMARY KEY,
            embedding FLOAT[{dims}]
        );
    """)

    # Insert docs and vectors together in one transaction
    with db:
        db.executemany(
            "INSERT INTO docs(id, text, metadata) VALUES (?, ?, ?)",
            [
                (id_, text, json.dumps(meta))
                for id_, text, meta in zip(ids, texts, metadatas)
            ],
        )
        db.executemany(
            "INSERT INTO vec_index(id, embedding) VALUES (?, ?)",
            [
                (id_, vec)
                for id_, vec in zip(ids, vectors)
            ],
        )

    return db

def load_db(db_path: str) -> sqlite3.Connection:
    if not os.path.exists(db_path):
        raise Exception(f"vector db does not exist: \"{db_path}\"")
    return _connect(db_path)

@dataclass
class ChunkResult:
    id: str
    text: str
    metadata: dict
    distance: float

def similarity_search(
    db: sqlite3.Connection,
    model: SentenceTransformer,
    query: str,
    k: int = 5,
) -> list[ChunkResult]:
    """ Conduct similarity search """

    query_vector = model.encode(
        query,
        normalize_embeddings=True,
        convert_to_numpy=True,
    ).astype(np.float32)

    rows = db.execute(
        """
        SELECT
            docs.id,
            docs.text,
            docs.metadata,
            vec_index.distance
        FROM vec_index
        JOIN docs ON docs.id = vec_index.id
        WHERE embedding MATCH ?
          AND k = ?
        ORDER BY distance
        """,
        [query_vector, k],
    ).fetchall()

    return [
        ChunkResult(
            id = row[0],
            text = row[1],
            metadata = json.loads(row[2]) if row[2] else {},
            distance = row[3],
        )
        for row in rows
    ]
