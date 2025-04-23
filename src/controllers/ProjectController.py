from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
import os


class ProjectController(BaseController):
    """
    Controller class to handle project directory creation and management.
    """

    def __init__(self):
        """
        Initialize the ProjectController.

        Args:
            None

        Returns:
            None
        """
        super().__init__()

    def get_project_path(self, project_id: str):
        """
        Get or create the directory path for a given project ID.

        Args:
            project_id (str): The ID of the project.

        Returns:
            str: The full directory path for the project.
        """

        # Create the project directory path by joining the base files_dir with the project_id
        project_dir = os.path.join(
            self.files_dir,
            project_id
        )

        # If the project directory does not exist, create it
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        # Return the complete project directory path
        return project_dir
