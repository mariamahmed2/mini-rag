from helpers.config import get_settings, Settings

class BaseDataModel:
    """
    BaseDataModel is a base class for database models that interact with a MongoDB database.
    It initializes the database client and application settings, which are used by subclasses 
    to interact with the database.

    Attributes:
        db_client (object): The MongoDB client used to interact with the database.
        app_settings (Settings): The application settings retrieved from the configuration.
    """

    def __init__(self, db_client: object):
        """
        Initializes an instance of BaseDataModel with the provided database client.

        Args:
            db_client (object): The MongoDB client used to interact with the database.

        Sets:
            self.db_client: The MongoDB client passed as an argument.
            self.app_settings: The application settings retrieved using `get_settings()`.
        """
        # Initialize the database client
        self.db_client = db_client
        
        # Retrieve application settings from the configuration
        self.app_settings = get_settings()
