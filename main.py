from fastapi import FastAPI
from pydantic import BaseModel
import yt_dlp
import os
import uuid
from openai import OpenAI

app = FastAPI()
client = OpenAI()


class VideoRequest(BaseModel):
    youtube_url: str


@app.get("/")
def home():
    return {"message": "video helper service is alive"}


@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/transcribe")
def transcribe_video(data: VideoRequest):
    return {
        "status": "received",
        "youtube_url": data.youtube_url
    }
