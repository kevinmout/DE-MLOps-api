from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from classification import Prediction
from google_cloud_client import GoogleCloudClient

load_dotenv()

class Item(BaseModel):
    text: str

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


@app.post("/api/v1/post/text")
def run_model(item: Item):
    outcome_model = Prediction.classification(item.text)
    if outcome_model == 0:
        return {"prediction": "written by a human"}
    else:
        return {"prediction": "AI generated"}