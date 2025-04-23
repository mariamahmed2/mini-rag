from helpers.config import get_settings, Settings
import os
import random
import string

class BaseController:
    
    def __init__(self):
        """
        Initialize the BaseController by setting up application settings
        and important directories for files and databases.
        """

        # Load application settings from helper
        self.app_settings = get_settings()
        
        # Get the base directory (parent of the current directory)
        self.base_dir = os.path.dirname(os.path.dirname(__file__))

        # Define path for storing asset files
        self.files_dir = os.path.join(
            self.base_dir,
            "assets/files"
        )

        # Define path for storing database files
        self.database_dir = os.path.join(
            self.base_dir,
            "assets/database"
        )
        
    def generate_random_string(self, length: int = 12):
        """
        Generate a random string of lowercase letters and digits.

        Args:
            length (int): The desired length of the random string. Default is 12.

        Returns:
            str: A randomly generated string.
        """
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def get_database_path(self, db_name: str):
        """
        Generate and ensure the path for a database directory.

        Args:
            db_name (str): The name of the database directory.

        Returns:
            str: The full path to the database directory.
        """

        # Build the full path to the database
        database_path = os.path.join(
            self.database_dir, db_name
        )

        # Create the database directory if it doesn't exist
        if not os.path.exists(database_path):
            os.makedirs(database_path)

        return database_path
