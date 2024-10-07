import logging
import os
from google.cloud import storage
from google.api_core.exceptions import GoogleAPIError

class GoogleCloudClient:
    
    def __init__(self):
        self.storage_client = self.initialize_storage_client()
        
    def initialize_storage_client(self) -> storage.Client:
        """Initialize and return a Google Cloud Storage client."""
        try:
            return storage.Client()
        except GoogleAPIError as e:
            logging.error(f"Failed to initialize Google Cloud Storage client: {e}")
            raise

    def get_bucket(self, bucket_name: str) -> storage.Bucket:
        """Get a specific bucket by its name."""
        try:
            bucket = self.storage_client.get_bucket(bucket_name)
            return bucket
        except GoogleAPIError as e:
            logging.error(f"Failed to get bucket {bucket_name}: {e}")
            raise

    def list_blobs(self, bucket_name: str) -> None:
        """Lists all the blobs in the specified bucket."""
        try:
            blobs = self.storage_client.list_blobs(bucket_name)
            return blobs
        except GoogleAPIError as e:
            logging.error(f"Failed to list blobs in bucket {bucket_name}: {e}")
            raise

    def get_blob_content(self, bucket_name: str, blob_name: str) -> str:
        """Fetches and returns the content of a blob (file) from the bucket."""
        try:
            bucket = self.get_bucket(bucket_name)
            blob = bucket.blob(blob_name)
            content = blob.download_as_text()  # Download as text
            logging.info(f"Content of {blob_name}: {content}")
            return content
        except GoogleAPIError as e:
            logging.error(f"Failed to fetch content for blob {blob_name}: {e}")
            raise

    def get_latest_blob(self, bucket_name: str, folder: str = None):
        """
        Fetch the most recent blob (file) from a specified Google Cloud Storage bucket and optional folder.
        
        Parameters:
        - bucket_name (str): Name of the GCS bucket.
        - folder (str): Optional, the folder (prefix) inside the bucket to search in.

        Returns:
        - full_path (str): Full path of the latest blob in the format 'gs://bucket-name/blob-name'.
        - file_name (str): The base name of the file.
        """

        
        # List blobs in the specified bucket and optional folder
        blobs = self.list_blobs(bucket_name)
        
        most_recent_blob = None
        max_created = None
        
        # Iterate over the blobs to find the most recent one
        for blob in blobs:
            if max_created is None or blob.time_created > max_created:
                most_recent_blob = blob
                max_created = blob.time_created

        # If a blob is found, return the full path and file name
        if most_recent_blob is not None:
            return self.get_blob_content(bucket_name, most_recent_blob.name)
        else:
            return None