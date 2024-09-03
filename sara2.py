import speech_recognition as sr
import pyttsx3
import wikipedia
import datetime
import pywhatkit as kit
import requests
import webbrowser
import os
import random

Assistant= pyttsx3.init()
voice = Assistant.getProperty('voices')
Assistant.setProperty('voice', voice[1].id)

# Initialize the recognizer and the TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set SARA's voice to a female voice
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Function to make SARA speak
def sara_speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to voice input
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            sara_speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Sorry, the service is down.")
            sara_speak("Sorry, the service is down.")
            return None

# Function to get current time
def tell_time():
    time = datetime.datetime.now().strftime('%I:%M %p')
    sara_speak(f"The current time is {time}")

# Function to get weather updates
def get_weather(city):
    api_key = "your_api_key"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        main = data["main"]
        weather_desc = data["weather"][0]["description"]
        temp = main["temp"]
        sara_speak(f"The temperature in {city} is {temp} degrees Celsius with {weather_desc}.")
    else:
        sara_speak("City not found.")

# Function to play a song on YouTube
def play_song(song):
    sara_speak(f"Playing {song} on YouTube.")
    kit.playonyt(song)

# Function to search something on Google
def google_search(query):
    sara_speak(f"Searching Google for {query}.")
    kit.search(query)

# Function to tell a joke
def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the math book look sad? Because it had too many problems.",
        "What do you get if you cross a snowman with a vampire? Frostbite."
    ]
    joke = random.choice(jokes)
    sara_speak(joke)

# Function to open an application
def open_application(app_name):
    if "chrome" in app_name:
        sara_speak("Opening Google Chrome")
        webbrowser.open("https://www.google.com")
    elif "notepad" in app_name:
        sara_speak("Opening Notepad")
        os.system("notepad")
    # Add more applications as needed

# Function to set a reminder
def set_reminder(task, time):
    sara_speak(f"Setting a reminder for {task} at {time}.")
    # In a real-world scenario, you'd want to integrate with a task scheduler or calendar API

# Personal Introduction
def personal_introduction():
    introduction = (
        "Hello! My name is SARA, your personal voice assistant. "
        "I am here to help you with your daily tasks, whether it's getting the weather update, "
        "setting reminders, playing your favorite songs, or searching the web for you. "
        "Just ask, and I’ll do my best to assist you."
    )
    sara_speak(introduction)

# Main function to respond to queries
def sara_respond():
    personal_introduction()
    while True:
        query = listen()
        if query:
            if "time" in query:
                tell_time()
            elif "weather" in query:
                sara_speak("Which city?")
                city = listen()
                if city:
                    get_weather(city)
            elif "wikipedia" in query:
                sara_speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "")
                try:
                    results = wikipedia.summary(query, sentences=2)
                    sara_speak("According to Wikipedia")
                    sara_speak(results)
                except wikipedia.exceptions.DisambiguationError:
                    sara_speak("There are multiple results, please be more specific.")
                except wikipedia.exceptions.PageError:
                    sara_speak("I couldn't find anything on that topic.")
            elif "play" in query:
                song = query.replace("play", "")
                play_song(song)
            elif "search" in query:
                search_term = query.replace("search", "")
                google_search(search_term)
            elif "joke" in query:
                tell_joke()
            elif "open" in query:
                app_name = query.replace("open", "").strip()
                open_application(app_name)
            elif "reminder" in query:
                sara_speak("What should I remind you about?")
                task = listen()
                if task:
                    sara_speak("At what time?")
                    time = listen()
                    if time:
                        set_reminder(task, time)
            elif "exit" in query or "stop" or "sleep" in query:
                sara_speak("Goodbye!")
                break
            else:
                sara_speak("I am not sure how to respond to that.")

# Start the assistant
if __name__ == "__main__":
    sara_respond()
