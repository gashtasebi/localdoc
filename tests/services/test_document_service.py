from unittest.mock import Mock

import pytest

from src.services.document_service import DocumentService


def test_list_documents_delegates_to_database():
    database = Mock()
    database.list_documents.return_value = [
        {"id": 1, "title": "test"}
    ]

    service = DocumentService(database)

    result = service.list_documents()

    assert result == [
        {"id": 1, "title": "test"}
    ]
    database.list_documents.assert_called_once_with()


def test_get_document_delegates_to_database():
    database = Mock()
    database.get_document.return_value = {
        "id": 1,
        "title": "test",
    }

    service = DocumentService(database)

    result = service.get_document(1)

    assert result == {
        "id": 1,
        "title": "test",
    }
    database.get_document.assert_called_once_with(1)


def test_delete_document_delegates_to_database():
    database = Mock()
    database.delete_document.return_value = True

    service = DocumentService(database)

    result = service.delete_document(1)

    assert result is True
    database.delete_document.assert_called_once_with(1)


def test_load_document_returns_document():
    database = Mock()
    database.get_document.return_value = {
        "id": 1,
        "title": "test",
    }

    service = DocumentService(database)

    result = service.load_document(1)

    assert result == {
        "id": 1,
        "title": "test",
    }
    database.get_document.assert_called_once_with(1)


def test_load_document_raises_error_for_unknown_document():
    database = Mock()
    database.get_document.return_value = None

    service = DocumentService(database)

    with pytest.raises(
        ValueError,
        match="Document with ID 999 not found.",
    ):
        service.load_document(999)


def test_load_embedded_chunks_delegates_to_database():
    database = Mock()

    embedded_chunks = [
        "chunk-1",
        "chunk-2",
    ]

    database.get_document.return_value = {
        "id": 1,
        "title": "test",
    }
    database.load_embedded_chunks.return_value = embedded_chunks

    service = DocumentService(database)

    result = service.load_embedded_chunks(1)

    assert result == embedded_chunks
    database.get_document.assert_called_once_with(1)
    database.load_embedded_chunks.assert_called_once_with(1)


def test_load_embedded_chunks_raises_error_for_unknown_document():
    database = Mock()
    database.get_document.return_value = None

    service = DocumentService(database)

    with pytest.raises(
        ValueError,
        match="Document with ID 999 not found.",
    ):
        service.load_embedded_chunks(999)

    database.load_embedded_chunks.assert_not_called()


def test_import_pdf_rejects_duplicate_document(monkeypatch):
    database = Mock()

    database.find_document_by_hash.return_value = 7

    monkeypatch.setattr(
        "src.services.document_service.calculate_file_hash",
        lambda path: "existing-hash",
    )

    service = DocumentService(database)

    with pytest.raises(
        ValueError,
        match="Document already exists.",
    ):
        service.import_pdf("test.pdf")

    database.find_document_by_hash.assert_called_once_with(
        "existing-hash"
    )


def test_import_pdf_processes_new_document(monkeypatch):
    database = Mock()

    database.find_document_by_hash.side_effect = [
        None,
        7,
    ]

    monkeypatch.setattr(
        "src.services.document_service.calculate_file_hash",
        lambda path: "new-hash",
    )

    pipeline_mock = Mock()

    monkeypatch.setattr(
        "src.services.document_service.process_pdf_pipeline",
        pipeline_mock,
    )

    embedder = Mock()

    service = DocumentService(
        database=database,
        embedder=embedder,
    )

    result = service.import_pdf("test.pdf")

    assert result == 7

    pipeline_mock.assert_called_once_with(
        "test.pdf",
        embedder,
        chunk_size=5,
        overlap=1,
        database=database,
    )

    database.find_document_by_hash.assert_any_call(
        "new-hash"
    )


def test_import_pdf_raises_error_when_document_cannot_be_found(
    monkeypatch,
):
    database = Mock()

    database.find_document_by_hash.side_effect = [
        None,
        None,
    ]

    monkeypatch.setattr(
        "src.services.document_service.calculate_file_hash",
        lambda path: "new-hash",
    )

    pipeline_mock = Mock()

    monkeypatch.setattr(
        "src.services.document_service.process_pdf_pipeline",
        pipeline_mock,
    )

    embedder = Mock()

    service = DocumentService(
        database=database,
        embedder=embedder,
    )

    with pytest.raises(
        RuntimeError,
        match="Document was imported but could not be found.",
    ):
        service.import_pdf("test.pdf")

    pipeline_mock.assert_called_once_with(
        "test.pdf",
        embedder,
        chunk_size=5,
        overlap=1,
        database=database,
    )
