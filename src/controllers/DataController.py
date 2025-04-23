from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os

class DataController(BaseController):
    
    def __init__(self):
        """
        Initialize the DataController by calling the BaseController initializer
        and setting the size scaling factor (for MB to bytes conversion).
        """
        super().__init__()
        self.size_scale = 1048576  # 1 MB = 1048576 bytes

    def validate_uploaded_file(self, file: UploadFile):
        """
        Validate the uploaded file based on allowed types and maximum size.

        Args:
            file (UploadFile): The file uploaded by the user.

        Returns:
            tuple: (bool indicating validation success, corresponding ResponseSignal value)
        """

        # Check if file type is allowed
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        # Check if file size exceeds the allowed limit
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value

    def generate_unique_filepath(self, orig_file_name: str, project_id: str):
        """
        Generate a unique file path for saving an uploaded file inside the project directory.

        Args:
            orig_file_name (str): The original name of the uploaded file.
            project_id (str): The ID of the project where the file belongs.

        Returns:
            tuple: (Full path to save the file, new file name with random key prefix)
        """

        # Generate a random string to make the filename unique
        random_key = self.generate_random_string()

        # Get the project's directory path
        project_path = ProjectController().get_project_path(project_id=project_id)

        # Clean the original file name
        cleaned_file_name = self.get_clean_file_name(
            orig_file_name=orig_file_name
        )

        # Create the full path with the random key
        new_file_path = os.path.join(
            project_path,
            random_key + "_" + cleaned_file_name
        )

        # Ensure the generated file path is unique
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                random_key + "_" + cleaned_file_name
            )

        return new_file_path, random_key + "_" + cleaned_file_name

    def get_clean_file_name(self, orig_file_name: str):
        """
        Clean the original file name by removing unwanted characters and formatting it.

        Args:
            orig_file_name (str): The original file name.

        Returns:
            str: The cleaned and formatted file name.
        """

        # Remove any characters that are not alphanumeric, underscore, or dot
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # Replace spaces with underscores
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name
