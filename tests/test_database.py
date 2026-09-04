import json
import sqlite3

from src.models import Chunk, Document, EmbeddedChunk, Page
from src.storage.database import LocalDatabase










def create_document():
    return Document(
        pages=[
            Page(
                page_number=1,
                text="First page text.",
            ),
            Page(
                page_number=2,
                text="Second page text.",
            ),
            Page(
                page_number=3,
                text="Third page text.",
            ),
        ]
    )


def create_embedded_chunks():
    return [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=1,
                text="First chunk.",
            ),
            vector=[0.1, 0.2, 0.3],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=2,
                page_number=2,
                text="Second chunk.",
            ),
            vector=[0.4, 0.5, 0.6],
        ),
    ]


def test_initialize_creates_database_tables(tmp_path):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    with sqlite3.connect(db_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                """
            ).fetchall()
        }

    assert "documents" in tables
    assert "chunks" in tables





def test_save_document_stores_chunks_and_vectors(tmp_path):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    document = create_document()
    embedded_chunks = create_embedded_chunks()

    document_id = database.save_document(
        document=document,
        embedded_chunks=embedded_chunks,
        file_path="test.pdf",
    )

    with sqlite3.connect(db_path) as connection:
        rows = connection.execute(
            """
            SELECT
                document_id,
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

    assert len(rows) == 2

    assert rows[0][0] == document_id
    assert rows[0][1] == 1
    assert rows[0][2] == 1
    assert rows[0][3] == "First chunk."
    assert json.loads(rows[0][4]) == [0.1, 0.2, 0.3]

    assert rows[1][0] == document_id
    assert rows[1][1] == 2
    assert rows[1][2] == 2
    assert rows[1][3] == "Second chunk."
    assert json.loads(rows[1][4]) == [0.4, 0.5, 0.6]






def test_load_embedded_chunks(tmp_path):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    document = create_document()
    embedded_chunks = create_embedded_chunks()

    document_id = database.save_document(
        document=document,
        embedded_chunks=embedded_chunks,
        file_path="test.pdf",
    )

    loaded_chunks = database.load_embedded_chunks(
        document_id
    )

    assert len(loaded_chunks) == 2

    assert loaded_chunks[0].chunk.chunk_id == 1
    assert loaded_chunks[0].chunk.page_number == 1
    assert loaded_chunks[0].chunk.text == "First chunk."
    assert loaded_chunks[0].vector == [0.1, 0.2, 0.3]

    assert loaded_chunks[1].chunk.chunk_id == 2
    assert loaded_chunks[1].chunk.page_number == 2
    assert loaded_chunks[1].chunk.text == "Second chunk."
    assert loaded_chunks[1].vector == [0.4, 0.5, 0.6]








def test_find_document_by_path(tmp_path):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    document_id = database.save_document(
        document=create_document(),
        embedded_chunks=create_embedded_chunks(),
        file_path="test.pdf",
    )

    result = database.find_document_by_path(
        "test.pdf"
    )

    assert result == document_id






def test_find_document_by_path_returns_none_for_unknown_file(
    tmp_path,
):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    result = database.find_document_by_path(
        "unknown.pdf"
    )

    assert result is None





def test_find_document_by_hash(tmp_path):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    document_id = database.save_document(
        document=create_document(),
        embedded_chunks=create_embedded_chunks(),
        file_path="test.pdf",
        file_hash="abc123",
    )

    result = database.find_document_by_hash(
        "abc123"
    )

    assert result == document_id






def test_find_document_by_hash_returns_none_for_unknown_hash(
    tmp_path,
):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    result = database.find_document_by_hash(
        "unknown-hash"
    )

    assert result is None






def test_list_documents(tmp_path):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    database.save_document(
        document=create_document(),
        embedded_chunks=create_embedded_chunks(),
        file_path="test.pdf",
    )

    documents = database.list_documents()

    assert len(documents) == 1
    assert documents[0]["file_path"] == "test.pdf"
    assert documents[0]["title"] == ""
    assert documents[0]["file_hash"] == ""
    assert documents[0]["page_count"] == 3
    assert documents[0]["chunk_count"] == 2







def test_list_documents_includes_chunk_count(tmp_path):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    database.save_document(
        document=create_document(),
        embedded_chunks=create_embedded_chunks(),
        file_path="test.pdf",
    )

    documents = database.list_documents()

    assert documents[0]["chunk_count"] == 2







def test_list_documents_includes_page_count(tmp_path):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    database.save_document(
        document=create_document(),
        embedded_chunks=create_embedded_chunks(),
        file_path="test.pdf",
    )

    documents = database.list_documents()

    assert documents[0]["page_count"] == 3







def test_list_documents_returns_empty_list_for_empty_database(
    tmp_path,
):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    documents = database.list_documents()

    assert documents == []







def test_save_document_with_title(tmp_path):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    database.save_document(
        document=create_document(),
        embedded_chunks=create_embedded_chunks(),
        file_path="test.pdf",
        title="My Test Document",
    )

    documents = database.list_documents()

    assert documents[0]["title"] == "My Test Document"







def test_get_document_returns_metadata(tmp_path):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    document_id = database.save_document(
        document=create_document(),
        embedded_chunks=create_embedded_chunks(),
        file_path="test.pdf",
        title="My Test Document",
        file_hash="abc123",
    )

    document = database.get_document(
        document_id
    )

    assert document is not None
    assert document["id"] == document_id
    assert document["file_path"] == "test.pdf"
    assert document["title"] == "My Test Document"
    assert document["file_hash"] == "abc123"
    assert document["page_count"] == 3






def test_get_document_returns_none_for_unknown_id(
    tmp_path,
):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    document = database.get_document(999)

    assert document is None






def test_delete_document(tmp_path):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    document_id = database.save_document(
        document=create_document(),
        embedded_chunks=create_embedded_chunks(),
        file_path="test.pdf",
    )

    deleted = database.delete_document(
        document_id
    )

    assert deleted is True
    assert database.get_document(document_id) is None
    assert database.load_embedded_chunks(document_id) == []






def test_delete_nonexistent_document(tmp_path):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    deleted = database.delete_document(999)

    assert deleted is False







def test_legacy_page_count_is_backfilled(tmp_path):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    with sqlite3.connect(db_path) as connection:
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
                "legacy.pdf",
                "Legacy Document",
                "legacy-hash",
                0,
            ),
        )

        document_id = cursor.lastrowid

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
                1,
                1,
                "Page one",
                json.dumps([0.1, 0.2]),
            ),
        )

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
                2,
                3,
                "Page three",
                json.dumps([0.3, 0.4]),
            ),
        )

    database.initialize()

    document = database.get_document(
        document_id
    )

    assert document is not None
    assert document["page_count"] == 3






def test_list_documents_returns_newest_document_first(tmp_path):
    db_path = tmp_path / "test.db"
    database = LocalDatabase(db_path)
    database.initialize()

    first_id = database.save_document(
        document=create_document(),
        embedded_chunks=create_embedded_chunks(),
        file_path="/documents/older.pdf",
        title="Older Document",
        file_hash="hash-older",
    )

    second_id = database.save_document(
        document=create_document(),
        embedded_chunks=create_embedded_chunks(),
        file_path="/documents/newer.pdf",
        title="Newer Document",
        file_hash="hash-newer",
    )

    documents = database.list_documents()

    assert documents[0]["id"] == second_id
    assert documents[1]["id"] == first_id







def test_get_document_returns_complete_document_metadata(tmp_path):
    db_path = tmp_path / "test.db"
    database = LocalDatabase(db_path)
    database.initialize()

    document_id = database.save_document(
        document=create_document(),
        embedded_chunks=create_embedded_chunks(),
        file_path="/documents/test.pdf",
        title="Test Document",
        file_hash="abc123",
    )

    document = database.get_document(document_id)

    assert document["id"] == document_id
    assert document["title"] == "Test Document"
    assert document["file_path"] == "/documents/test.pdf"
    assert document["file_hash"] == "abc123"
    assert document["page_count"] == 3
    assert document["chunk_count"] == 2





def test_load_embedded_chunks_is_isolated_per_document(tmp_path):
    db_path = tmp_path / "test.db"

    database = LocalDatabase(db_path)
    database.initialize()

    first_document = Document(
        pages=[
            Page(
                page_number=1,
                text="First document.",
            )
        ]
    )

    first_chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=1,
                text="First document chunk.",
            ),
            vector=[1.0, 0.0, 0.0],
        )
    ]

    second_document = Document(
        pages=[
            Page(
                page_number=1,
                text="Second document.",
            )
        ]
    )

    second_chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=1,
                text="Second document chunk.",
            ),
            vector=[0.0, 1.0, 0.0],
        )
    ]

    first_document_id = database.save_document(
        document=first_document,
        embedded_chunks=first_chunks,
        file_path="first.pdf",
        title="First Document",
        file_hash="hash-first",
    )

    second_document_id = database.save_document(
        document=second_document,
        embedded_chunks=second_chunks,
        file_path="second.pdf",
        title="Second Document",
        file_hash="hash-second",
    )

    first_loaded = database.load_embedded_chunks(
        first_document_id
    )

    second_loaded = database.load_embedded_chunks(
        second_document_id
    )

    assert len(first_loaded) == 1
    assert len(second_loaded) == 1

    assert (
        first_loaded[0].chunk.text
        == "First document chunk."
    )

    assert (
        second_loaded[0].chunk.text
        == "Second document chunk."
    )

    assert (
        first_loaded[0].chunk.text
        != second_loaded[0].chunk.text
    )
