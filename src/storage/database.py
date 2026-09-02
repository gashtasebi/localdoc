import json
import sqlite3
from pathlib import Path

from src.models import Chunk, Document, EmbeddedChunk


class LocalDatabase:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)

    def connect(self):
        return sqlite3.connect(self.db_path)

    def initialize(self):
        with self.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS chunks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_id INTEGER NOT NULL,
                    chunk_id INTEGER NOT NULL,
                    page_number INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    vector TEXT NOT NULL,
                    FOREIGN KEY (document_id)
                        REFERENCES documents(id)
                )
                """
            )

    def save_document(
        self,
        document: Document,
        embedded_chunks: list[EmbeddedChunk],
        file_path: str = "",
    ) -> int:
        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO documents (file_path)
                VALUES (?)
                """,
                (file_path,),
            )

            document_id = cursor.lastrowid

            for item in embedded_chunks:
                connection.execute(
                    """
                    INSERT INTO chunks (
                        document_id,
                        chunk_id,
                        page_number,
                        text,
                        vector
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        document_id,
                        item.chunk.chunk_id,
                        item.chunk.page_number,
                        item.chunk.text,
                        json.dumps(item.vector),
                    ),
                )

        return document_id


    def find_document_by_path(
        self,
        file_path: str,
    ) -> int | None:
        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT id
                FROM documents
                WHERE file_path = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (file_path,),
            ).fetchone()

        if row is None:
            return None

        return row[0]



    def list_documents(self) -> list[dict]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT id, file_path
                FROM documents
                ORDER BY id
                """
            ).fetchall()

        return [
            {
                "id": row[0],
                "file_path": row[1],
            }
            for row in rows
        ]







    def load_embedded_chunks(
        self,
        document_id: int,
    ) -> list[EmbeddedChunk]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    chunk_id,
                    page_number,
                    text,
                    vector
                FROM chunks
                WHERE document_id = ?
                ORDER BY chunk_id
                """,
                (document_id,),
            ).fetchall()

        embedded_chunks = []

        for row in rows:
            chunk_id, page_number, text, vector_json = row

            embedded_chunks.append(
                EmbeddedChunk(
                    chunk=Chunk(
                        chunk_id=chunk_id,
                        page_number=page_number,
                        text=text,
                    ),
                    vector=json.loads(vector_json),
                )
            )

        return embedded_chunks



    def get_document(
        self,
        document_id: int,
    ) -> dict | None:
        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT id, file_path
                FROM documents
                WHERE id = ?
                """,
                (document_id,),
            ).fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "file_path": row[1],
        }
