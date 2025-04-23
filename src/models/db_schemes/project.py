# Importing necessary modules from Pydantic for data validation and model creation.
from pydantic import BaseModel, Field, validator

# Importing Optional for fields that are not mandatory, ObjectId from bson for MongoDB ID representation.
from typing import Optional
from bson.objectid import ObjectId

# Defining the Project class to represent a project in the system.
class Project(BaseModel):
    """
    The Project class represents a project entity in the system.
    It validates the project_id to be alphanumeric and defines the database index configuration.
    """

    # Optional ObjectId field representing MongoDB's _id field, alias is set for compatibility with MongoDB.
    id: Optional[ObjectId] = Field(None, alias="_id")

    # Required field for the project identifier. It must be a non-empty string.
    project_id: str = Field(..., min_length=1)

    # Custom validator for the 'project_id' field to ensure it is alphanumeric.
    @validator('project_id')
    def validate_project_id(cls, value):
        """
        Validator method to ensure the project_id is alphanumeric.
        
        Args:
            value (str): The value of the project_id field.
        
        Raises:
            ValueError: If the project_id is not alphanumeric.
        
        Returns:
            str: The validated project_id value.
        """
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')  # Ensures project_id contains only letters and numbers.
        
        return value

    # Config class to allow non-Pydantic types like ObjectId to be used in the model.
    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        """
        Defines the indexes for the Project collection to optimize queries.
        
        Returns:
            list: A list of index definitions for the MongoDB collection.
        """
        return [
            {
                "key": [
                    ("project_id", 1)  # Single index on project_id for fast querying by project ID.
                ],
                "name": "project_id_index_1",  # Index name
                "unique": True  # Unique index ensures no duplicate project_ids in the collection.
            }
        ]
