from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Settings class to load and manage configuration values from environment variables 
    or .env file for the application.

    Attributes:
        APP_NAME (str): Name of the application.
        APP_VERSION (str): Version of the application.
        OPENAI_API_KEY (str): API key for accessing OpenAI services.
        FILE_ALLOWED_TYPES (list): List of allowed file types for uploads.
        FILE_MAX_SIZE (int): Maximum allowed file size for uploads (in bytes).
        FILE_DEFAULT_CHUNK_SIZE (int): Default chunk size for file processing.
        MONGODB_URL (str): URL of the MongoDB instance.
        MONGODB_DATABASE (str): Name of the MongoDB database.
        GENERATION_BACKEND (str): Backend for text generation (e.g., OpenAI, Cohere).
        EMBEDDING_BACKEND (str): Backend for text embeddings (e.g., OpenAI, Cohere).
        OPENAI_API_KEY (str, optional): API key for OpenAI.
        OPENAI_API_URL (str, optional): URL for the OpenAI API.
        COHERE_API_KEY (str, optional): API key for Cohere service.
        GENERATION_MODEL_ID (str, optional): Model ID for text generation.
        EMBEDDING_MODEL_ID (str, optional): Model ID for text embedding.
        EMBEDDING_MODEL_SIZE (int, optional): Size of the embedding model.
        INPUT_DAFAULT_MAX_CHARACTERS (int, optional): Max number of characters for input.
        GENERATION_DAFAULT_MAX_TOKENS (int, optional): Max tokens for text generation.
        GENERATION_DAFAULT_TEMPERATURE (float, optional): Temperature for text generation.
        VECTOR_DB_BACKEND (str): Vector database backend (e.g., Qdrant, FAISS).
        VECTOR_DB_PATH (str): Path to the vector database.
        VECTOR_DB_DISTANCE_METHOD (str, optional): Method for distance calculation in vector DB.
        PRIMARY_LANG (str, default="en"): The primary language for the app (default is English).
        DEFAULT_LANG (str, default="en"): The default language for the app (default is English).
    """

    # Application settings
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str

    # File upload settings
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    # MongoDB settings
    MONGODB_URL: str
    MONGODB_DATABASE: str

    # Backend settings for Generation and Embedding
    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    # API keys for different services
    OPENAI_API_KEY: str = None  # Optional API key for OpenAI
    OPENAI_API_URL: str = None  # Optional API URL for OpenAI
    COHERE_API_KEY: str = None  # Optional API key for Cohere

    # Model and generation settings
    GENERATION_MODEL_ID: str = None  # Optional model ID for text generation
    EMBEDDING_MODEL_ID: str = None  # Optional model ID for text embeddings
    EMBEDDING_MODEL_SIZE: int = None  # Optional size of the embedding model
    INPUT_DAFAULT_MAX_CHARACTERS: int = None  # Max characters for input text
    GENERATION_DAFAULT_MAX_TOKENS: int = None  # Max tokens for text generation
    GENERATION_DAFAULT_TEMPERATURE: float = None  # Temperature for text generation

    # Vector DB settings
    VECTOR_DB_BACKEND: str  # Backend for the vector database (e.g., Qdrant, FAISS)
    VECTOR_DB_PATH: str  # Path where the vector DB is stored
    VECTOR_DB_DISTANCE_METHOD: str = None  # Distance method used in vector DB (optional)

    # Language settings
    PRIMARY_LANG: str = "en"  # Primary language of the application (default is English)
    DEFAULT_LANG: str = "en"  # Default language of the application (default is English)

    class Config:
        # Specify the environment file to load configuration from
        env_file = ".env"

def get_settings():
    """
    Fetches and returns an instance of the Settings class with the configuration values
    loaded from environment variables or the .env file.

    Args:
        None

    Returns:
        Settings: An instance of the Settings class containing the app's configuration.
    """
    return Settings()
