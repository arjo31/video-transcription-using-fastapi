import os

import uvicorn
import whisper
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from moviepy.editor import VideoFileClip

app = FastAPI()

origins = ["http://localhost:8501"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...), id: str = Form(...), tags: str = Form(...), name: str = Form(...)):
    video_file_path = os.path.join(".", file.filename)
    audio_file_name = f"{os.path.splitext(file.filename)[0]}.mp3"
    audio_file_path = os.path.join(".", audio_file_name)

    with open(video_file_path, "wb") as video_file:
        video_file.write(await file.read())

    video_clip = VideoFileClip(video_file_path)
    video_clip.audio.write_audiofile(audio_file_path)
    video_clip.close()

    os.remove(video_file_path)

    model = whisper.load_model('base')

    result = model.transcribe(audio_file_path, verbose = True)

    print(file.filename, name, tags, id, audio_file_path)
    
    os.remove(audio_file_path)

    if file:
        return {'result' : result['text']}
    return {'result' : 'Error'}

if __name__=="__main__":
    uvicorn.run("backend_app:app", reload=True, host="127.0.0.1", port=8000)