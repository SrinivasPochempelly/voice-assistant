import os
import webbrowser
import datetime
import speech_recognition as sr
import pyttsx3
import wikipedia
import pywhatkit as kit
import tkinter as tk
from threading import Thread

# Initialize TTS
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

# Your name for greetings
user_name = "Srinu"

# Assistant control
listening = False

def speak(text):
    status_label.config(text="Speaking...")
    engine.say(text)
    engine.runAndWait()
    status_label.config(text="Listening..." if listening else "Ready")

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak(f"How may I help you, {user_name}?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        r.pause_threshold = 0.5
        r.energy_threshold = 300
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            status_label.config(text="Timeout. Waiting for next...")
            return "none"
    try:
        status_label.config(text="Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        status_label.config(text=f"You said: {query}")
        return query.lower()
    except Exception:
        status_label.config(text="Didn't catch that.")
        return "none"

def handle_query(query):
    if query == "none":
        return

    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        try:
            results = wikipedia.summary(query.replace("wikipedia", ""), sentences=1)
            speak("According to Wikipedia")
            speak(results)
        except:
            speak("Couldn't fetch from Wikipedia.")

    elif 'open youtube' in query:
        webbrowser.open("https://youtube.com")

    elif 'open google' in query:
        webbrowser.open("https://google.com")

    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")

    elif query.startswith('search'):
        topic = query.replace('search', '').replace('about', '').strip()
        if topic:
            speak(f"Searching about {topic}")
            kit.search(topic)
        else:
            speak("What should I search?")
            content = take_command()
            if content != "none":
                kit.search(content)

    elif 'play song' in query or 'play music' in query:
        speak("Which song?")
        song = take_command()
        if song != "none":
            speak(f"Playing {song} on YouTube")
            kit.playonyt(song)

    elif 'hello' in query or 'hey' in query:
        speak(f"Hello {user_name}!")

    elif 'Good Job!' in query or 'Great!' in query :
        speak("Thank you!")

    elif 'who are you' in query:
        speak("I am your personal assistant, made by Srinu.")

    elif 'exit' in query or 'quit' in query:
        speak("Goodbye!")
        stop_listening()
        root.quit()
    else:
        speak("I didn't understand that.")

def start_listening():
    global listening
    listening = True
    status_label.config(text="Listening...")
    Thread(target=continuous_listen).start()

def stop_listening():
    global listening
    listening = False
    status_label.config(text="Stopped.")

def continuous_listen():
    wish_me()
    while listening:
        query = take_command()
        handle_query(query)

# -------------------- GUI --------------------
root = tk.Tk()
root.title("Voice Assistant by Srinu")
root.geometry("400x300")
root.config(bg="#222222")

title_label = tk.Label(root, text="🎙️ Voice Assistant", font=("Arial", 18), fg="white", bg="#222222")
title_label.pack(pady=20)

status_label = tk.Label(root, text="Click 'Speak' to start listening", font=("Arial", 12), fg="lightgray", bg="#222222")
status_label.pack(pady=10)

speak_button = tk.Button(root, text="🎤 Speak", font=("Arial", 14), bg="#5555FF", fg="white", command=start_listening)
speak_button.pack(pady=10)

stop_button = tk.Button(root, text="🛑 Stop", font=("Arial", 14), bg="#FF5555", fg="white", command=stop_listening)
stop_button.pack(pady=10)

root.mainloop()
