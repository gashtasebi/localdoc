import json

import sqlite3

from pathlib import Path

from src.file_utils import calculate_file_hash

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

                    file_path TEXT NOT NULL,

                    title TEXT NOT NULL DEFAULT '',

                    file_hash TEXT NOT NULL DEFAULT '',

                    page_count INTEGER NOT NULL DEFAULT 0

                )
                """
            )

            columns = connection.execute(
                "PRAGMA table_info(documents)"
            ).fetchall()

            column_names = {
                column[1]
                for column in columns
            }

            if "title" not in column_names:

                connection.execute(
                    """
                    ALTER TABLE documents

                    ADD COLUMN title TEXT NOT NULL DEFAULT ''
                    """
                )

            if "file_hash" not in column_names:

                connection.execute(
                    """
                    ALTER TABLE documents

                    ADD COLUMN file_hash TEXT NOT NULL DEFAULT ''
                    """
                )

            if "page_count" not in column_names:

                connection.execute(
                    """
                    ALTER TABLE documents

                    ADD COLUMN page_count INTEGER NOT NULL DEFAULT 0
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

            self._backfill_file_hashes(connection)

            self._backfill_page_counts(connection)

    def _backfill_file_hashes(

        self,

        connection: sqlite3.Connection,

    ):

        rows = connection.execute(
            """
            SELECT id, file_path

            FROM documents

            WHERE file_hash = ''
            """
        ).fetchall()

        for document_id, file_path in rows:

            path = Path(file_path)

            if not path.exists() or not path.is_file():

                continue

            file_hash = calculate_file_hash(path)

            connection.execute(
                """
                UPDATE documents

                SET file_hash = ?

                WHERE id = ?
                """,
                (
                    file_hash,
                    document_id,
                ),
            )

    def _backfill_page_counts(

        self,

        connection: sqlite3.Connection,

    ):

        rows = connection.execute(
            """
            SELECT id

            FROM documents

            WHERE page_count = 0
            """
        ).fetchall()

        for (document_id,) in rows:

            row = connection.execute(
                """
                SELECT MAX(page_number)

                FROM chunks

                WHERE document_id = ?
                """,
                (document_id,),
            ).fetchone()

            max_page_number = row[0]

            if max_page_number is None:

                continue

            connection.execute(
                """
                UPDATE documents

                SET page_count = ?

                WHERE id = ?
                """,
                (
                    max_page_number,
                    document_id,
                ),
            )

    def save_document(

        self,

        document: Document,

        embedded_chunks: list[EmbeddedChunk],

        file_path: str = "",

        title: str = "",

        file_hash: str = "",

    ) -> int:

        page_count = (

            len(document.pages)

            if document is not None

            else 0

        )

        with self.connect() as connection:

            cursor = connection.execute(
                """
                INSERT INTO documents (

                    file_path,

                    title,

                    file_hash,

                    page_count

                )

                VALUES (?, ?, ?, ?)
                """,
                (
                    file_path,

                    title,

                    file_hash,

                    page_count,

                ),
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

    def find_document_by_hash(

        self,

        file_hash: str,

    ) -> int | None:

        with self.connect() as connection:

            row = connection.execute(
                """
                SELECT id

                FROM documents

                WHERE file_hash = ?

                ORDER BY id DESC

                LIMIT 1
                """,
                (file_hash,),
            ).fetchone()

        if row is None:

            return None

        return row[0]

    def list_documents(self) -> list[dict]:

        with self.connect() as connection:

            rows = connection.execute(
                """
                SELECT

                    documents.id,

                    documents.file_path,

                    documents.title,

                    documents.file_hash,

                    documents.page_count,

                    COUNT(chunks.id) AS chunk_count

                FROM documents

                LEFT JOIN chunks

                    ON chunks.document_id = documents.id

                GROUP BY

                    documents.id,

                    documents.file_path,

                    documents.title,

                    documents.file_hash,

                    documents.page_count

                ORDER BY documents.id DESC

                """
            ).fetchall()

        return [

            {

                "id": row[0],

                "file_path": row[1],

                "title": row[2],

                "file_hash": row[3],

                "page_count": row[4],

                "chunk_count": row[5],

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
                SELECT

                    documents.id,

                    documents.file_path,

                    documents.title,

                    documents.file_hash,

                    documents.page_count,

                    COUNT(chunks.id) AS chunk_count

                FROM documents

                LEFT JOIN chunks

                    ON chunks.document_id = documents.id

                WHERE documents.id = ?

                GROUP BY

                    documents.id,

                    documents.file_path,

                    documents.title,

                    documents.file_hash,

                    documents.page_count

                """,
                (document_id,),
            ).fetchone()

        if row is None:

            return None

        return {

            "id": row[0],

            "file_path": row[1],

            "title": row[2],

            "file_hash": row[3],

            "page_count": row[4],

            "chunk_count": row[5],

        }

    def delete_document(

        self,

        document_id: int,

    ) -> bool:

        with self.connect() as connection:

            document = connection.execute(
                """
                SELECT id

                FROM documents

                WHERE id = ?
                """,
                (document_id,),
            ).fetchone()

            if document is None:

                return False

            connection.execute(
                """
                DELETE FROM chunks

                WHERE document_id = ?
                """,
                (document_id,),
            )

            connection.execute(
                """
                DELETE FROM documents

                WHERE id = ?
                """,
                (document_id,),
            )

        return True
