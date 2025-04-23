# Importing the base model class from the BaseDataModel module, which provides common functionality for database interactions.
from .BaseDataModel import BaseDataModel

# Importing the DataChunk schema from the db_schemes module, which defines the structure of a chunk of data to be stored in the database.
from .db_schemes import DataChunk

# Importing DataBaseEnum from the enums module, which contains database-related constants like collection names.
from .enums.DataBaseEnum import DataBaseEnum

# Importing ObjectId from bson to work with MongoDB's unique identifier type for documents.
from bson.objectid import ObjectId

# Importing InsertOne from pymongo to perform bulk insert operations for adding multiple documents to the MongoDB collection.
from pymongo import InsertOne


class ChunkModel(BaseDataModel):
    """
    The ChunkModel class handles the interaction with the MongoDB collection for storing, retrieving, 
    and managing chunks of data related to a project. It inherits from the BaseDataModel class.
    """

    def __init__(self, db_client: object):
        """
        Initializes the ChunkModel with a given database client.

        Args:
            db_client (object): The database client used for interacting with MongoDB.
        """
        super().__init__(db_client=db_client)
        # Assigning the collection object from the database client based on the collection name for chunks.
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object):
        """
        Creates an instance of the ChunkModel, initializing its collection.

        Args:
            db_client (object): The database client to interact with MongoDB.

        Returns:
            ChunkModel: An instance of the ChunkModel class.
        """
        instance = cls(db_client)
        # Initializes the collection if it doesn't already exist in the database.
        await instance.init_collection()
        return instance

    async def init_collection(self):
        """
        Initializes the MongoDB collection for chunks if it doesn't exist and sets up indexes.
        """
        # List all collections in the database.
        all_collections = await self.db_client.list_collection_names()

        # If the collection for chunks doesn't exist, create it and set up necessary indexes.
        if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
            # Get indexes defined in the DataChunk schema.
            indexes = DataChunk.get_indexes()
            # Create indexes for the collection as defined in the schema.
            for index in indexes:
                await self.collection.create_index(
                    index["key"], 
                    name=index["name"], 
                    unique=index["unique"]
                )

    async def create_chunk(self, chunk: DataChunk):
        """
        Inserts a chunk document into the MongoDB collection.

        Args:
            chunk (DataChunk): The chunk of data to be inserted.

        Returns:
            DataChunk: The chunk object with the inserted ID populated.
        """
        result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_unset=True))
        # Assign the inserted ID to the chunk object.
        chunk._id = result.inserted_id
        return chunk

    async def get_chunk(self, chunk_id: str):
        """
        Retrieves a chunk from the MongoDB collection by its ID.

        Args:
            chunk_id (str): The ID of the chunk to retrieve.

        Returns:
            DataChunk | None: The chunk object if found, else None.
        """
        result = await self.collection.find_one({
            "_id": ObjectId(chunk_id)
        })

        if result is None:
            return None
        
        # Convert the MongoDB result to a DataChunk object and return it.
        return DataChunk(**result)

    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):
        """
        Inserts multiple chunks into the MongoDB collection in batches.

        Args:
            chunks (list): A list of DataChunk objects to be inserted.
            batch_size (int): The number of chunks to insert per batch. Default is 100.

        Returns:
            int: The total number of chunks inserted.
        """
        # Iterate over the chunks in batches.
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]

            # Create a list of bulk write operations for inserting each chunk.
            operations = [
                InsertOne(chunk.dict(by_alias=True, exclude_unset=True))
                for chunk in batch
            ]

            # Perform the bulk insert operation.
            await self.collection.bulk_write(operations)
        
        # Return the number of chunks inserted.
        return len(chunks)

    async def delete_chunks_by_project_id(self, project_id: ObjectId):
        """
        Deletes all chunks associated with a given project ID.

        Args:
            project_id (ObjectId): The ID of the project whose chunks should be deleted.

        Returns:
            int: The number of chunks deleted.
        """
        result = await self.collection.delete_many({
            "chunk_project_id": project_id
        })

        return result.deleted_count

    async def get_poject_chunks(self, project_id: ObjectId, page_no: int = 1, page_size: int = 50):
        """
        Retrieves chunks associated with a specific project ID, with pagination support.

        Args:
            project_id (ObjectId): The ID of the project to retrieve chunks for.
            page_no (int): The page number for pagination. Default is 1.
            page_size (int): The number of chunks to retrieve per page. Default is 50.

        Returns:
            list: A list of DataChunk objects for the specified project.
        """
        records = await self.collection.find({
            "chunk_project_id": project_id
        }).skip(  # Pagination step
            (page_no - 1) * page_size
        ).limit(page_size).to_list(length=None)

        # Convert the MongoDB records to DataChunk objects and return them.
        return [
            DataChunk(**record)
            for record in records
        ]
