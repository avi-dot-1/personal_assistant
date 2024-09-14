import threading
import time
import queue
import cv2
import subprocess
import webbrowser
import os
import logging
from speech import listen_for_speech, speak
from ai import groq_prompt, function_call, handle_coding_task
from helper import take_screenshot, web_cam_capture, get_clipboard_text, analyze_user_intent, open_app
from memory import save_memory, delete_memory


logging.getLogger().setLevel(logging.ERROR)

# Initialize webcam
web_cam = cv2.VideoCapture(0)

# Global variables
speaking = threading.Event()
listening = threading.Event()
conversation_active = threading.Event()
interrupt_queue = queue.Queue()

def start_assistant():
    conversation_active.set()

    print("Say 'Hey Jarvis' to start the conversation, or 'Stop' to end it.")
    while conversation_active.is_set():
        text = listen_for_speech()
        if text and 'hey jarvis' in text:
            print("Jarvis activated. How can I help you?")
            speak("Hey there! How can I assist you today?")
            break
        elif text and 'stop' in text:
            print("Stopping the assistant.")
            conversation_active.clear()
            return

    while conversation_active.is_set():
        text = listen_for_speech()
        if text:
            if 'stop' in text:
                print("Stopping the assistant.")
                speak("Alright, it was great chatting with you. Take care!")
                conversation_active.clear()
                break

            print(f"USER: {text}")
            
            if 'delete memory' in text:
                delete_memory(0, time.time())
                continue
            
            if 'write code' in text or 'create a game' in text:
                handle_coding_task(text)
                continue
            
            if 'open' in text:
                app_name = text.split('open')[-1].strip()
                open_app(app_name)
                continue
            
            call = function_call(text)
            visual_context = None

            if 'take screenshot' in call:
                print('Taking screenshot')
                photo_path = take_screenshot()
                visual_context = None  # Add appropriate logic here
            elif 'capture webcam' in call:
                print('Capturing webcam')
                photo_path = web_cam_capture()
                visual_context = None  # Add appropriate logic here
            elif 'extract clipboard' in call:
                print('Copying clipboard text')
                paste = get_clipboard_text()
                text = f'{text}\n\n CLIPBOARD CONTENT: {paste}'
            elif 'coding task' in call:
                handle_coding_task(text)
                continue

            response = groq_prompt(prompt=text, img_context=visual_context)
            print(f'ASSISTANT: {response}')

            # Start a thread to check for interruptions
            interrupt_thread = threading.Thread(target=check_for_interruption)
            interrupt_thread.start()

            speak(response)

            if not interrupt_queue.empty():
                interrupted_text = interrupt_queue.get()
                print(f"Interrupted with: {interrupted_text}")
                continue

            user_intent = analyze_user_intent()
            print(f"User intent: {user_intent}")

        time.sleep(0.5)

    # Clean up
    web_cam.release()
