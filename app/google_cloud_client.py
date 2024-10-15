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

    def download_blob_content(self, bucket_name: str, blob_name: str) -> str:
        """
        Downloads the content of a blob as text.
        
        Args:
            bucket_name: The name of the bucket.
            blob_name: The name of the blob in the bucket.
        
        Returns:
            The content of the blob as a string.
        """
        try:
            bucket = self.get_bucket(bucket_name)
            blob = bucket.blob(blob_name)
            
            # Download the content as text
            content = blob.download_as_text()
            logging.info(f"Downloaded content from {blob_name}: {content}")
            return content
        except GoogleAPIError as e:
            logging.error(f"Failed to download blob {blob_name}: {e}")
            return None

    def upload_file(self, bucket_name: str, blob_name: str, file_path: str):
        """
        Uploads a file to the specified bucket and blob.
        
        Args:
            bucket_name: The name of the Google Cloud Storage bucket.
            blob_name: The name of the blob (file) in the bucket.
            file_path: The local path to the CSV file to be uploaded.
        """
        try:
            bucket = self.get_bucket(bucket_name)
            blob = bucket.blob(blob_name)
            
            # Upload the CSV file from the local path
            blob.upload_from_filename(file_path)
            
            logging.info(f"Successfully uploaded {file_path} to {blob_name} in bucket {bucket_name}")
            print(f"Successfully uploaded {file_path} to {blob_name}")
        except GoogleAPIError as e:
            logging.error(f"Failed to upload CSV file to blob {blob_name}: {e}")
            print(f"Failed to upload CSV file {blob_name}: {e}")
    