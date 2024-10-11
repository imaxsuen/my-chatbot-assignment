import os
import pathlib
import google.generativeai as genai
import pyaudio
import wave
import pyttsx3

from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(
    api_key=API_KEY
)
model = genai.GenerativeModel('gemini-1.5-flash')






def transcribe():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []
    print("Recording... Use Keyboard Interrupt (Ctrl + C) to stop recording")
    try :
        while True :
            data = stream.read(1024)
            frames.append(data)
    except KeyboardInterrupt :
        print("Recording stopped")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

    sound_file = wave.open("recording.wav", "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()
    print("Recording saved as recording.wav")
    
    prompt = "Generate a transcript of the speech.\n"
    global response
    response = model.generate_content([
        prompt,
        {
            "mime_type": "audio/wav",
            "data": pathlib.Path('recording.wav').read_bytes()
        }
    ])






def speaker(text):
    engine = pyttsx3.init()
    rate = engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()






chat = model.start_chat(history=[])
instruction = "In this chat, respond only with less than 30 word summaries."

while(True):
    transcribe()
    question = response.text

    if(question.strip() == ''):
        break
    print(question)
    reply = chat.send_message(question)
    print('\n')
    print(f"Bot: {reply.text}")
    speaker(reply.text)