import speech_recognition as sr
import pyttsx3
import pyperclip
import cv2
from PIL import ImageGrab
import os
import threading
import re

# Initialize speech recognition
r = sr.Recognizer()
r.dynamic_energy_threshold = False
r.energy_threshold = 400

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.8)

# Global flags for speaking and listening
speaking = threading.Event()

# Listen for speech and convert it to text
def listen_for_speech():
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, phrase_time_limit=10)  # Increased time limit for longer sentences
    try:
        text = r.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Could you please repeat?")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

# Convert text to speech
def speak(text):
    speaking.set()
    for sentence in re.split('(?<=[.!?]) +', text):
        engine.say(sentence)
        engine.runAndWait()
    speaking.clear()

# Take a screenshot
def take_screenshot():
    path = 'screenshot.jpg'
    screenshot = ImageGrab.grab()
    rgb_screenshot = screenshot.convert('RGB')
    rgb_screenshot.save(path, quality=15)
    return path

# Capture an image from the webcam
def web_cam_capture(web_cam):
    if not web_cam.isOpened():
        print('Error: camera not opening')
        return None

    path = 'webcam.jpg'
    ret, frame = web_cam.read()
    cv2.imwrite(path, frame)
    return path

# Get the clipboard content
def get_clipboard_text():
    clipboard_content = pyperclip.paste()
    if isinstance(clipboard_content, str):
        return clipboard_content
    else:
        print('Nothing found in clipboard')
        return None
# analyzing the intent
def analyze_user_intent():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    ret, frame = web_cam.read()
    if not ret:
        return "No camera feed available"
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) == 0:
        return "No face detected"
    
    # Analyze the largest face
    (x, y, w, h) = max(faces, key=lambda face: face[2] * face[3])
    face_roi = frame[y:y+h, x:x+w]
    
    # Simple heuristics for user intent (you might want to use a more sophisticated model)
    avg_pixel = cv2.mean(face_roi)[0]
    if avg_pixel < 100:  # Dark image, user might be looking away
        return "User might not be paying attention"
    elif avg_pixel > 200:  # Bright image, user might be engaged
        return "User seems engaged"
    else:
        return "User's intent unclear"

#opening apps
def open_app(app_name):
    app_map = {
        'youtube': 'https://www.youtube.com',
        'reddit': 'https://www.reddit.com',
        'twitter': 'https://www.twitter.com',
        'chrome': 'google-chrome',
        'vs code': 'code'  # Assuming 'code' is the command to open VS Code
    }
    
    if app_name in app_map:
        if app_name in ['youtube', 'reddit', 'twitter']:
            webbrowser.open(app_map[app_name])
        else:
            subprocess.Popen(app_map[app_name])
        speak(f"Opening {app_name}")
    else:
        speak(f"Sorry, I don't know how to open {app_name}")
