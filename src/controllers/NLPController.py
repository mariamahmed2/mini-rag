# Import base class
from .BaseController import BaseController

# Import project and chunk models
from models.db_schemes import Project, DataChunk

# Import document types enum for embeddings
from stores.llm.LLMEnums import DocumentTypeEnum

# Typing for function signatures
from typing import List

# For serialization
import json

# NLPController class
class NLPController(BaseController):
    # Initialization method
    def __init__(self, vectordb_client, generation_client, 
                 embedding_client, template_parser):
        super().__init__()  # Initialize base class

        # Save references to clients and parsers
        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser

    # Create a collection name using project ID
    def create_collection_name(self, project_id: str):
        return f"collection_{project_id}".strip()
    
    # Reset (delete) a vector database collection for a project
    def reset_vector_db_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)
    
    # Get information about a vector database collection
    def get_vector_db_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name=collection_name)

        # Ensure that collection_info is JSON serializable
        # Use json.dumps + json.loads to convert objects to dictionary format
        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
    
    # Insert data chunks into the vector database
    def index_into_vector_db(self, project: Project, chunks: List[DataChunk],
                                   chunks_ids: List[int], 
                                   do_reset: bool = False):
        
        # Step 1: Get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # Step 2: Extract texts and metadata from chunks
        texts = [ c.chunk_text for c in chunks ]
        metadata = [ c.chunk_metadata for c in chunks ]

        # Step 3: Create vector embeddings for all texts
        vectors = [
            self.embedding_client.embed_text(
                text=text, 
                document_type=DocumentTypeEnum.DOCUMENT.value
            )
            for text in texts
        ]

        # Step 4: Create collection if it does not exist (or reset it)
        _ = self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset,
        )

        # Step 5: Insert the data into the vector database
        _ = self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            metadata=metadata,
            vectors=vectors,
            record_ids=chunks_ids,
        )

        return True  # Successfully indexed

    # Search inside the vector DB collection using a query text
    def search_vector_db_collection(self, project: Project, text: str, limit: int = 10):
        
        # Step 1: Get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # Step 2: Embed the search text (query) into a vector
        vector = self.embedding_client.embed_text(
            text=text, 
            document_type=DocumentTypeEnum.QUERY.value
        )

        # If embedding failed, return False
        if not vector or len(vector) == 0:
            return False

        # Step 3: Perform semantic search
        results = self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit
        )

        # If no results found, return False
        if not results:
            return False

        return results  # Return search results

    # Answer a question using RAG (Retrieval Augmented Generation)
    def answer_rag_question(self, project: Project, query: str, limit: int = 10):
        
        # Initialize variables
        answer, full_prompt, chat_history = None, None, None

        # Step 1: Retrieve related documents from vector database
        retrieved_documents = self.search_vector_db_collection(
            project=project,
            text=query,
            limit=limit,
        )

        # If no documents retrieved, return empty values
        if not retrieved_documents or len(retrieved_documents) == 0:
            return answer, full_prompt, chat_history
        
        # Step 2: Build the LLM prompt

        # Load system prompt template
        system_prompt = self.template_parser.get("rag", "system_prompt")

        # Build document prompts using retrieved documents
        documents_prompts = "\n".join([
            self.template_parser.get(
                "rag", 
                "document_prompt", 
                {
                    "doc_num": idx + 1,
                    "chunk_text": doc.text,
                }
            )
            for idx, doc in enumerate(retrieved_documents)
        ])

        # Footer prompt including the user query
        footer_prompt = self.template_parser.get(
            "rag", 
            "footer_prompt", 
            {
                "query": query
            }
        )

        # Step 3: Construct the conversation (chat history)

        # Add system prompt to chat history
        chat_history = [
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role=self.generation_client.enums.SYSTEM.value,
            )
        ]

        # Create the full user prompt by joining documents and footer
        full_prompt = "\n\n".join([documents_prompts, footer_prompt])

        # Step 4: Generate answer using LLM
        answer = self.generation_client.generate_text(
            prompt=full_prompt,
            chat_history=chat_history
        )

        # Return answer, prompt, and chat history
        return answer, full_prompt, chat_history
