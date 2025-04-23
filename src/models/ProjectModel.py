# Importing the base model class from the BaseDataModel module, which provides common functionality for database interactions.
from .BaseDataModel import BaseDataModel

# Importing the Project schema from the db_schemes module, which defines the structure of a project to be stored in the database.
from .db_schemes import Project

# Importing DataBaseEnum from the enums module, which contains database-related constants like collection names.
from .enums.DataBaseEnum import DataBaseEnum


class ProjectModel(BaseDataModel):
    """
    The ProjectModel class handles the interaction with the MongoDB collection for storing, retrieving, 
    and managing projects in the database. It inherits from the BaseDataModel class.
    """

    def __init__(self, db_client: object):
        """
        Initializes the ProjectModel with a given database client.

        Args:
            db_client (object): The database client used for interacting with MongoDB.
        """
        super().__init__(db_client=db_client)
        # Assigning the collection object from the database client based on the collection name for projects.
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object):
        """
        Creates an instance of the ProjectModel, initializing its collection.

        Args:
            db_client (object): The database client to interact with MongoDB.

        Returns:
            ProjectModel: An instance of the ProjectModel class.
        """
        instance = cls(db_client)
        # Initializes the collection if it doesn't already exist in the database.
        await instance.init_collection()
        return instance

    async def init_collection(self):
        """
        Initializes the MongoDB collection for projects if it doesn't exist and sets up indexes.
        """
        # List all collections in the database.
        all_collections = await self.db_client.list_collection_names()

        # If the collection for projects doesn't exist, create it and set up necessary indexes.
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
            # Get indexes defined in the Project schema.
            indexes = Project.get_indexes()
            # Create indexes for the collection as defined in the schema.
            for index in indexes:
                await self.collection.create_index(
                    index["key"], 
                    name=index["name"], 
                    unique=index["unique"]
                )

    async def create_project(self, project: Project):
        """
        Inserts a project document into the MongoDB collection.

        Args:
            project (Project): The project to be inserted.

        Returns:
            Project: The project object with the inserted ID populated.
        """
        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True))
        # Assign the inserted ID to the project object.
        project.id = result.inserted_id
        return project

    async def get_project_or_create_one(self, project_id: str):
        """
        Retrieves a project from the MongoDB collection by its project ID. If not found, creates a new project.

        Args:
            project_id (str): The project ID to retrieve or create.

        Returns:
            Project: The found or newly created project.
        """
        record = await self.collection.find_one({
            "project_id": project_id
        })

        if record is None:
            # If project doesn't exist, create a new project.
            project = Project(project_id=project_id)
            # Insert the new project into the database.
            project = await self.create_project(project=project)

            return project
        
        # If project exists, return it as a Project object.
        return Project(**record)

    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        """
        Retrieves all projects from the collection with pagination.

        Args:
            page (int): The page number for pagination. Default is 1.
            page_size (int): The number of projects per page. Default is 10.

        Returns:
            tuple: A tuple containing the list of projects and the total number of pages.
        """
        # Count the total number of documents in the collection.
        total_documents = await self.collection.count_documents({})

        # Calculate the total number of pages based on the total documents and page size.
        total_pages = total_documents // page_size
        if total_documents % page_size > 0:
            total_pages += 1

        # Retrieve the documents based on pagination.
        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        projects = []
        # Iterate through the cursor and convert documents to Project objects.
        async for document in cursor:
            projects.append(
                Project(**document)
            )

        # Return the list of projects and the total number of pages.
        return projects, total_pages
