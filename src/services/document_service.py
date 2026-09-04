from pathlib import Path

from src.embedder import SentenceTransformerEmbedder
from src.file_utils import calculate_file_hash
from src.pipeline import process_pdf_pipeline
from src.storage.database import LocalDatabase


class DocumentService:
    def __init__(
        self,
        database: LocalDatabase,
        embedder: SentenceTransformerEmbedder | None = None,
    ):
        self.database = database
        self.embedder = embedder

    def list_documents(self):
        return self.database.list_documents()

    def get_document(self, document_id: int):
        return self.database.get_document(document_id)

    def delete_document(self, document_id: int) -> bool:
        return self.database.delete_document(document_id)

    def load_document(
        self,
        document_id: int,
    ):
        document = self.database.get_document(document_id)

        if document is None:
            raise ValueError(
                f"Document with ID {document_id} not found."
            )

        return document

    def load_embedded_chunks(self, document_id: int):
        self.load_document(document_id)

        return self.database.load_embedded_chunks(
            document_id
        )

    def import_pdf(self, pdf_path: str | Path) -> int:
        path = Path(pdf_path)

        file_hash = calculate_file_hash(path)

        existing_document_id = (
            self.database.find_document_by_hash(file_hash)
        )

        if existing_document_id is not None:
            raise ValueError("Document already exists.")

        if self.embedder is None:
            self.embedder = SentenceTransformerEmbedder()

        process_pdf_pipeline(
            str(path),
            self.embedder,
            chunk_size=5,
            overlap=1,
            database=self.database,
        )

        document_id = self.database.find_document_by_hash(
            file_hash
        )

        if document_id is None:
            raise RuntimeError(
                "Document was imported but could not be found."
            )

        return document_id

    def process_pdf(
        self,
        pdf_path: str | Path,
    ):
        if self.embedder is None:
            self.embedder = SentenceTransformerEmbedder()

        return process_pdf_pipeline(
            str(pdf_path),
            self.embedder,
            chunk_size=5,
            overlap=1,
            database=self.database,
        )
