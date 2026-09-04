from src.models import Chunk, Document, EmbeddedChunk
from src.storage.database import LocalDatabase


def test_initialize_creates_database_tables(tmp_path):
    db_path = tmp_path / "localdoc.db"
    database = LocalDatabase(db_path)

    database.initialize()

    assert db_path.exists()

    with database.connect() as connection:
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

    table_names = {table[0] for table in tables}

    assert "documents" in table_names
    assert "chunks" in table_names


def test_save_document_stores_chunks_and_vectors(tmp_path):
    db_path = tmp_path / "localdoc.db"
    database = LocalDatabase(db_path)

    database.initialize()

    document = Document(
        pages=[],
        chunks=[],
    )

    embedded_chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=2,
                text="Python is a programming language.",
            ),
            vector=[0.1, 0.2, 0.3],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=2,
                page_number=3,
                text="Python is widely used in NLP.",
            ),
            vector=[0.4, 0.5, 0.6],
        ),
    ]

    document_id = database.save_document(
        document,
        embedded_chunks,
    )

    assert document_id == 1

    with database.connect() as connection:
        rows = connection.execute(
            """
            SELECT
                document_id,
                chunk_id,
                page_number,
                text,
                vector
            FROM chunks
            ORDER BY chunk_id
            """
        ).fetchall()

    assert len(rows) == 2
    assert rows[0][0] == 1
    assert rows[0][1] == 1
    assert rows[0][2] == 2
    assert rows[0][3] == "Python is a programming language."
    assert rows[0][4] == "[0.1, 0.2, 0.3]"

    assert rows[1][0] == 1
    assert rows[1][1] == 2
    assert rows[1][2] == 3


def test_load_embedded_chunks(tmp_path):
    db_path = tmp_path / "localdoc.db"
    database = LocalDatabase(db_path)

    database.initialize()

    document = Document(
        pages=[],
        chunks=[],
    )

    embedded_chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=2,
                text="Python is a programming language.",
            ),
            vector=[0.1, 0.2, 0.3],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=2,
                page_number=3,
                text="Python is widely used in NLP.",
            ),
            vector=[0.4, 0.5, 0.6],
        ),
    ]

    document_id = database.save_document(
        document,
        embedded_chunks,
    )

    loaded_chunks = database.load_embedded_chunks(
        document_id
    )

    assert len(loaded_chunks) == 2

    assert loaded_chunks[0].chunk.chunk_id == 1
    assert loaded_chunks[0].chunk.page_number == 2
    assert loaded_chunks[0].chunk.text == (
        "Python is a programming language."
    )
    assert loaded_chunks[0].vector == [0.1, 0.2, 0.3]

    assert loaded_chunks[1].chunk.chunk_id == 2
    assert loaded_chunks[1].chunk.page_number == 3
    assert loaded_chunks[1].chunk.text == (
        "Python is widely used in NLP."
    )
    assert loaded_chunks[1].vector == [0.4, 0.5, 0.6]


def test_find_document_by_path(tmp_path):
    database = LocalDatabase(
        tmp_path / "localdoc.db"
    )

    database.initialize()

    document = Document(
        pages=[]
    )

    embedded_chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=1,
                text="Test document",
            ),
            vector=[0.1, 0.2, 0.3],
        )
    ]

    file_path = "/documents/test.pdf"

    document_id = database.save_document(
        document=document,
        embedded_chunks=embedded_chunks,
        file_path=file_path,
    )

    found_id = database.find_document_by_path(
        file_path
    )

    assert found_id == document_id


def test_find_document_by_path_returns_none_for_unknown_file(
    tmp_path,
):
    database = LocalDatabase(
        tmp_path / "localdoc.db"
    )

    database.initialize()

    result = database.find_document_by_path(
        "/documents/unknown.pdf"
    )

    assert result is None


def test_list_documents(tmp_path):
    database = LocalDatabase(
        tmp_path / "localdoc.db"
    )

    database.initialize()

    document1 = Document(pages=[])
    document2 = Document(pages=[])

    database.save_document(
        document=document1,
        embedded_chunks=[],
        file_path="/documents/manual1.pdf",
    )

    database.save_document(
        document=document2,
        embedded_chunks=[],
        file_path="/documents/manual2.pdf",
    )

    documents = database.list_documents()

    assert len(documents) == 2

    assert documents[0]["file_path"] == (
        "/documents/manual1.pdf"
    )

    assert documents[1]["file_path"] == (
        "/documents/manual2.pdf"
    )


def test_delete_document(tmp_path):
    database = LocalDatabase(
        tmp_path / "test.db"
    )

    database.initialize()

    document = Document(
        pages=[],
        chunks=[
            Chunk(
                chunk_id=1,
                page_number=1,
                text="Test document",
            )
        ],
    )

    embedded_chunks = [
        EmbeddedChunk(
            chunk=document.chunks[0],
            vector=[0.1, 0.2, 0.3],
        )
    ]

    document_id = database.save_document(
        document=document,
        embedded_chunks=embedded_chunks,
        file_path="test.pdf",
    )

    assert database.get_document(document_id) is not None

    deleted = database.delete_document(document_id)

    assert deleted is True
    assert database.get_document(document_id) is None
    assert database.load_embedded_chunks(document_id) == []


def test_save_document_with_title(tmp_path):
    database = LocalDatabase(
        tmp_path / "test.db"
    )

    database.initialize()

    document = Document(
        pages=[],
        chunks=[],
    )

    document_id = database.save_document(
        document=document,
        embedded_chunks=[],
        file_path="test.pdf",
        title="Test Document",
    )

    saved_document = database.get_document(
        document_id
    )

    assert saved_document is not None
    assert saved_document["title"] == "Test Document"


def test_list_documents_includes_chunk_count(tmp_path):
    database = LocalDatabase(
        tmp_path / "test.db"
    )

    database.initialize()

    document = Document(pages=[])

    embedded_chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=1,
                text="First chunk",
            ),
            vector=[0.1, 0.2, 0.3],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=2,
                page_number=2,
                text="Second chunk",
            ),
            vector=[0.4, 0.5, 0.6],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=3,
                page_number=2,
                text="Third chunk",
            ),
            vector=[0.7, 0.8, 0.9],
        ),
    ]

    document_id = database.save_document(
        document=document,
        embedded_chunks=embedded_chunks,
        file_path="/documents/manual.pdf",
        title="Manual",
    )

    documents = database.list_documents()

    assert len(documents) == 1
    assert documents[0]["id"] == document_id
    assert documents[0]["title"] == "Manual"
    assert documents[0]["chunk_count"] == 3


def test_get_document_returns_metadata(tmp_path):
    database = LocalDatabase(
        tmp_path / "test.db"
    )

    database.initialize()

    document = Document(pages=[])

    document_id = database.save_document(
        document=document,
        embedded_chunks=[],
        file_path="/documents/manual.pdf",
        title="User Manual",
        file_hash="abc123",
    )

    saved_document = database.get_document(
        document_id
    )

    assert saved_document is not None
    assert saved_document["id"] == document_id
    assert saved_document["file_path"] == (
        "/documents/manual.pdf"
    )
    assert saved_document["title"] == "User Manual"
    assert saved_document["file_hash"] == "abc123"



def test_list_documents_returns_empty_list_for_empty_database(
    tmp_path,
):
    database = LocalDatabase(
        tmp_path / "test.db"
    )
    database.initialize()

    documents = database.list_documents()

    assert documents == []
