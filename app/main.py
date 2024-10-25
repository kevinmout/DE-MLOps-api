from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from helper import Helper
from classification import Prediction
from google_cloud_client import GoogleCloudClient
from feedback_manager import FeedbackManager



load_dotenv()

class Item(BaseModel):
    text: str

class Feedback(BaseModel):
    input_text: str
    predicted_class: str
    correct_class: str

app = FastAPI()

origins = [
    os.getenv("MY_APP_URL"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/post/feedback")
def upload_feedback(feedback: Feedback):
    # initialize a Google Cloud Storage client and a FeedbackManager
    google_client = GoogleCloudClient()
    feedback_manager = FeedbackManager(feedback)

    # paths and names for the feedback file
    local_feedback_file_path = os.getenv("LOCAL_FEEDBACK_FILE_PATH")
    google_feedback_file_path = os.getenv("GOOGLE_FEEDBACK_FILE_PATH")
    bucket_name = os.getenv("BUCKET_NAME")

    # get the latest feedback file, otherwise create a new one
    feedback_content = google_client.download_blob_content(bucket_name, google_feedback_file_path)

    if feedback_content is None:
        # create a new feedback file
        feedback_manager.create_feedback_df(local_feedback_file_path)

    else:
        # append the feedback to the existing feedback file
        feedback_manager.append_feedback_df(local_feedback_file_path, feedback_content)

    # upload the feedback file to GCS
    google_client.upload_file(bucket_name, google_feedback_file_path, local_feedback_file_path)

    # remove the local feedback file
    os.remove(local_feedback_file_path)

    return "Thank you for your feedback!"

@app.get("/api/v1/get/feedback")
def download_feedback():
    # initialize a Google Cloud Storage client
    google_client = GoogleCloudClient()

    # paths and names for the feedback file
    google_feedback_file_path = os.getenv("GOOGLE_FEEDBACK_FILE_PATH")
    bucket_name = os.getenv("BUCKET_NAME")

    # download the feedback file from GCS
    feedback_content = google_client.download_blob_content(bucket_name, google_feedback_file_path)

    if feedback_content is None:
        return "No feedback available."
    
    df = Helper.convert_str_to_df(feedback_content)

    return df.to_dict(orient="records")
    

@app.post("/api/v1/post/text")
def run_model(item: Item):
    outcome_model = Prediction.classification(item.text)
    return outcome_model