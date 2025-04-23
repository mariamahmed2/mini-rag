from .BaseDataModel import BaseDataModel
from .db_schemes import Asset
from .enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId

class AssetModel(BaseDataModel):
    """
    AssetModel is a class for managing asset data in the database. It provides methods
    for creating, retrieving, and managing assets in a MongoDB collection.

    Attributes:
        collection (object): MongoDB collection instance for asset data.
    """

    def __init__(self, db_client: object):
        """
        Initializes an AssetModel instance.

        Args:
            db_client (object): The MongoDB client used to interact with the database.
        """
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object):
        """
        Creates and initializes an instance of the AssetModel class, ensuring the collection is ready.

        Args:
            db_client (object): The MongoDB client used to interact with the database.

        Returns:
            AssetModel: The newly created AssetModel instance.
        """
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        """
        Initializes the asset collection by checking if it exists. If it doesn't,
        it creates the collection and sets up necessary indexes.

        Returns:
            None
        """
        # Get all collections in the database
        all_collections = await self.db_client.list_collection_names()
        
        # Check if the asset collection exists; if not, create it
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
            # Get the required indexes for the collection from the Asset model
            indexes = Asset.get_indexes()
            # Create the indexes in the collection
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

    async def create_asset(self, asset: Asset):
        """
        Inserts a new asset into the collection.

        Args:
            asset (Asset): The asset instance to be inserted.

        Returns:
            Asset: The asset object with its new ID after insertion.
        """
        # Insert the asset into the collection and return the result
        result = await self.collection.insert_one(asset.dict(by_alias=True, exclude_unset=True))
        asset.id = result.inserted_id  # Set the asset's ID to the inserted document's ID

        return asset

    async def get_all_project_assets(self, asset_project_id: str, asset_type: str):
        """
        Retrieves all assets for a specific project and asset type.

        Args:
            asset_project_id (str): The project ID to filter assets by.
            asset_type (str): The asset type to filter assets by.

        Returns:
            List[Asset]: A list of Asset objects corresponding to the project and asset type.
        """
        # Fetch all assets matching the project ID and asset type
        records = await self.collection.find({
            "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id,
            "asset_type": asset_type,
        }).to_list(length=None)

        # Convert the raw records into Asset objects and return them
        return [
            Asset(**record)
            for record in records
        ]

    async def get_asset_record(self, asset_project_id: str, asset_name: str):
        """
        Retrieves a specific asset record based on project ID and asset name.

        Args:
            asset_project_id (str): The project ID to filter the asset by.
            asset_name (str): The name of the asset to retrieve.

        Returns:
            Asset: The asset object if found, otherwise None.
        """
        # Search for the asset record in the collection
        record = await self.collection.find_one({
            "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id,
            "asset_name": asset_name,
        })

        # If a record is found, return it as an Asset object
        if record:
            return Asset(**record)
        
        return None  # Return None if no record was found
