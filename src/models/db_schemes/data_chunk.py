# Importing necessary modules from Pydantic for data validation and model creation.
from pydantic import BaseModel, Field, validator

# Importing Optional for fields that are not mandatory, ObjectId from bson for MongoDB ID representation.
from typing import Optional
from bson.objectid import ObjectId


# Defining the DataChunk class to represent a chunk of data associated with a project or asset.
class DataChunk(BaseModel):
    """
    The DataChunk class represents a chunk of text data, its metadata, and the project/asset it belongs to.
    It validates the data, defines the structure, and provides database index configurations.
    """

    # Optional ObjectId field representing MongoDB's _id field, alias is set for compatibility with MongoDB.
    id: Optional[ObjectId] = Field(None, alias="_id")

    # Required field for storing the actual chunk of text data. It must have at least one character.
    chunk_text: str = Field(..., min_length=1)

    # Metadata associated with the chunk, stored as a dictionary.
    chunk_metadata: dict

    # Required field to specify the order of the chunk in a sequence. It must be greater than 0.
    chunk_order: int = Field(..., gt=0)

    # Required ObjectId field for referencing the project associated with the chunk.
    chunk_project_id: ObjectId

    # Required ObjectId field for referencing the asset associated with the chunk.
    chunk_asset_id: ObjectId

    # Config class for allowing non-Pydantic types like ObjectId in the model.
    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        """
        Defines the indexes for the DataChunk collection to optimize queries.
        
        Returns:
            list: A list of index definitions.
        """
        return [
            {
                "key": [
                    ("chunk_project_id", 1)  # Single index on chunk_project_id for fast querying by project ID.
                ],
                "name": "chunk_project_id_index_1",  # Index name
                "unique": False  # Non-unique index allows duplicate project IDs in the collection.
            }
        ]


# Defining the RetrievedDocument class to represent documents retrieved based on a query.
class RetrievedDocument(BaseModel):
    """
    The RetrievedDocument class represents a document retrieved from the system along with its relevance score.
    """

    # The text content of the retrieved document.
    text: str

    # The score representing the relevance or quality of the document. A higher score typically means better relevance.
    score: float
