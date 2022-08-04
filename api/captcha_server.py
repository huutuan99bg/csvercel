# %%
from os.path import dirname, join
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import speech_recognition as sr
import os
import requests
import random
import string
import nest_asyncio
import uvicorn
import subprocess
curdir = dirname(__file__)

def string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def recognize(mp3_path):
    try:
        ffmpeg = join(curdir, 'ffmpeg.exe')
        os.makedirs(join(curdir, 'audio_files'), exist_ok=True)
        wav_path = os.path.join(curdir, 'audio_files', string_generator(size=15).lower()+'.wav')
        subprocess.call([ffmpeg, '-i', mp3_path, wav_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        temp_audio = sr.AudioFile(wav_path)
        r = sr.Recognizer()
        with temp_audio as source:
            audio = r.record(source)
        # Recognizer
        key = r.recognize_google(audio)
        # Remove the audio
        if os.path.exists(mp3_path):
            os.remove(mp3_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)
        return key
    except:
        try:
            if os.path.exists(mp3_path):
                os.remove(mp3_path)
            if os.path.exists(wav_path):
                os.remove(wav_path)
        except:
            pass
        return False


def recognize_from_url(audio_url):
    try:
        os.makedirs(join(curdir, 'audio_files'), exist_ok=True)
        mp3_path = os.path.join(curdir, 'audio_files', string_generator(size=15).lower()+'.mp3')
        data = requests.get(audio_url, ) 
        print('Download audio status: '+str(data.status_code))
        if data.status_code != 200:
            return False
        with open(mp3_path, 'wb') as f:
            f.write(data.content)
        return recognize(mp3_path)
    except:
        return False

# Flask app
curdir = dirname(__file__)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root():
    return {"success": True, 'test': 'ok'}


@app.get("/api")
async def api_root():
    return {"success": True, 'message': 'API is working'}


@app.get("/api/server-ip")
async def api_root():
    res = requests.get("https://api4.ipify.org/?format=json")
    return {"success": True, 'ip': res.json()['ip']}


@app.get("/api/solver")
async def api_solver(audio_url):
    result = recognize_from_url(audio_url)
    if result != False:
        return {"success": True, 'key': result}
    else:
        return {"success": False}

# Run app
if __name__ == '__main__':
    nest_asyncio.apply()
    uvicorn.run(app=app, host="127.0.0.1", port=80)
    print("Server is running... 127.0.0.1:"+str(80))
