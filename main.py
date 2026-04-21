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
    try:
        ydl_opts = {
            "quiet": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.youtube_url, download=False)

        return {
            "status": "metadata_ok",
            "youtube_url": data.youtube_url,
            "title": info.get("title"),
            "duration_seconds": info.get("duration")
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
