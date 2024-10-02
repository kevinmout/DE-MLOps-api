from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os


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
    model = item.text[::-1] + " - processed by the model. It's working!"
    return model