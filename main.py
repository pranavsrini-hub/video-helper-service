@app.post("/transcribe")
def transcribe_video(data: VideoRequest):
    try:
        os.makedirs("audio", exist_ok=True)

        file_id = str(uuid.uuid4())
        output_template = f"audio/{file_id}.%(ext)s"

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "noplaylist": True,
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.youtube_url, download=True)
            downloaded_file = ydl.prepare_filename(info)

        with open(downloaded_file, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file
            )

        return {
            "status": "transcribed",
            "youtube_url": data.youtube_url,
            "audio_file": downloaded_file,
            "transcript": transcript.text
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
