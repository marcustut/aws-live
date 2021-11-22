import os
from dotenv import load_dotenv


def _get_env(key: str) -> str:
    """
    Get the environment variable from the given key. It will throw an error if
    an environment variable is not found with the given key.
    """
    var = os.getenv(key)
    if var is None:
        raise Exception(f"Unable to get '{key}' from environment")
    return var


class Config:
    """
    This is the config class where it will load the environment variables when
    initialized. 
    """

    def __init__(self) -> None:
        # load environment variables from .env
        load_dotenv()
        self.database_url = _get_env('DATABASE_URL')
        self.database_host = _get_env('DATABASE_HOST')
        self.database_user = _get_env('DATABASE_USER')
        self.database_password = _get_env('DATABASE_PASSWORD')
        self.database_db = _get_env('DATABASE_DB')
        self.s3_bucket_id = _get_env('S3_BUCKET_ID')
        self.s3_region = _get_env('S3_BUCKET_REGION')
