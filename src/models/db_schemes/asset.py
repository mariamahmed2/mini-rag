# Importing necessary modules from Pydantic for data validation and model creation.
from pydantic import BaseModel, Field, validator

# Importing optional typing for fields that are not mandatory and ObjectId from bson for MongoDB ID representation.
from typing import Optional
from bson.objectid import ObjectId

# Importing datetime module to handle timestamps in the model.
from datetime import datetime


# Defining the Asset class, which represents an asset document in the database.
class Asset(BaseModel):
    """
    The Asset class represents an asset in a project, with fields such as type, name, size, configuration, and timestamp.
    It also provides functionality to validate the input and generate necessary database indexes.
    """

    # Optional ObjectId field that maps to MongoDB's _id. Default is None, and alias is set for compatibility with MongoDB.
    id: Optional[ObjectId] = Field(None, alias="_id")

    # Required ObjectId field to represent the project the asset belongs to.
    asset_project_id: ObjectId

    # The type of the asset (e.g., "image", "model"). It must have at least one character.
    asset_type: str = Field(..., min_length=1)

    # The name of the asset. Must have at least one character.
    asset_name: str = Field(..., min_length=1)

    # The size of the asset, which must be a non-negative integer.
    asset_size: int = Field(ge=0, default=None)

    # A dictionary to hold the asset's configuration. Default is None.
    asset_config: dict = Field(default=None)

    # Timestamp for when the asset was pushed to the system, defaulting to the current UTC time.
    asset_pushed_at: datetime = Field(default=datetime.utcnow)

    # Config class to allow arbitrary types for fields like ObjectId
    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        """
        Defines the indexes for the Asset collection to optimize queries.

        Returns:
            list: A list of index definitions.
        """
        return [
            {
                "key": [
                    ("asset_project_id", 1)  # Single index on asset_project_id
                ],
                "name": "asset_project_id_index_1",  # Index name
                "unique": False  # This index allows duplicate values for asset_project_id
            },
            {
                "key": [
                    ("asset_project_id", 1),  # Composite index on asset_project_id and asset_name
                    ("asset_name", 1)
                ],
                "name": "asset_project_id_name_index_1",  # Index name
                "unique": True  # This index enforces unique combinations of asset_project_id and asset_name
            },
        ]
