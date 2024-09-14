import re
import pyttsx3
import speech_recognition as sr

# Initialize speech recognition
r = sr.Recognizer()
r.dynamic_energy_threshold = False
r.energy_threshold = 400

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.8)

def listen_for_speech():
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, phrase_time_limit=10)
    try:
        text = r.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Could you please repeat?")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

def speak(text):
    for sentence in re.split('(?<=[.!?]) +', text):
        engine.say(sentence)
        engine.runAndWait()
