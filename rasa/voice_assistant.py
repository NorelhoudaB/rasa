import speech_recognition as sr
from gtts import gTTS
import os
import requests

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak...")
        audio = recognizer.listen(source)
    return recognizer.recognize_google(audio)

def speak(text):
    tts = gTTS(text=text)
    tts.save("response.mp3")
    os.system("mpg123 response.mp3")

def send_to_rasa(message):
    response = requests.post(
        "http://localhost:5005/webhooks/rest/webhook",
        json={"sender": "voice-user", "message": message}
    )
    return [r["text"] for r in response.json() if "text" in r]

while True:
    try:
        user_input = listen()
        print(f"You: {user_input}")
        responses = send_to_rasa(user_input)
        for r in responses:
            print(f"Bot: {r}")
            speak(r)
    except Exception as e:
        print("Error:", e)
