from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnum


class ProcessController(BaseController):
    """
    Controller class to handle processing of project files (TXT, PDF).
    """

    def __init__(self, project_id: str):
        """
        Initialize the ProcessController with a specific project ID.

        Args:
            project_id (str): The ID of the project to be processed.

        Returns:
            None
        """
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str):
        """
        Get the file extension of the given file ID.

        Args:
            file_id (str): The file name or ID (e.g., 'document.pdf').

        Returns:
            str: The file extension (e.g., '.pdf', '.txt').
        """
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str):
        """
        Get an appropriate loader based on the file extension.

        Args:
            file_id (str): The file name or ID to load.

        Returns:
            object: A file loader instance (TextLoader or PyMuPDFLoader) or None if unsupported.
        """
        file_ext = self.get_file_extension(file_id=file_id)
        file_path = os.path.join(self.project_path, file_id)

        if not os.path.exists(file_path):
            return None

        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")

        if file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)

        return None

    def get_file_content(self, file_id: str):
        """
        Load the content of a file using the suitable loader.

        Args:
            file_id (str): The file name or ID to load.

        Returns:
            list: List of loaded documents (LangChain Document objects) or None if failed.
        """
        loader = self.get_file_loader(file_id=file_id)
        if loader:
            return loader.load()

        return None

    def process_file_content(self, file_content: list, file_id: str,
                              chunk_size: int = 100, overlap_size: int = 20):
        """
        Split loaded file content into smaller overlapping text chunks.

        Args:
            file_content (list): List of LangChain Documents loaded from the file.
            file_id (str): The file name or ID (used for metadata if needed).
            chunk_size (int, optional): Maximum size of each text chunk. Default is 100.
            overlap_size (int, optional): Overlapping size between consecutive chunks. Default is 20.

        Returns:
            list: List of smaller chunks (LangChain Document objects) with original metadata.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )

        file_content_texts = [rec.page_content for rec in file_content]
        file_content_metadata = [rec.metadata for rec in file_content]

        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )

        return chunks
