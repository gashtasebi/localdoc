from unittest.mock import Mock

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

    try:
        service.load_document(999)
        assert False, "Expected ValueError"
    except ValueError as error:
        assert str(error) == "Document with ID 999 not found."



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

    try:
        service.load_embedded_chunks(999)
        assert False, "Expected ValueError"
    except ValueError as error:
        assert str(error) == "Document with ID 999 not found."

    database.load_embedded_chunks.assert_not_called()
