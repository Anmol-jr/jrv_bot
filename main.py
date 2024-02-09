import pyaudio
import pyttsx3
import speech_recognition as sr
import datetime
import os
import wikipedia
import webbrowser
import sys

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that. Please say that again.")
            return "None"
        except sr.RequestError as e:
            speak(f"Could not request results from Google API; {e}")
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception as e:
        speak("Say that again, please...")
        return "None"
    return query.lower()


def wish():
    try:
        hour = int(datetime.datetime.now().hour)
    except ValueError:
        speak("Sorry, I couldn't retrieve the current hour.")
        return

    if 0 <= hour < 12:
        speak("Good morning, sir.")
    elif 12 <= hour < 18:
        speak("Good afternoon, sir.")
    else:
        speak("Good evening, sir.")

    speak("I am Jarvis. Please tell me how may I help you.")

def open_application(query):
    applications = {
        "notepad": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories",
        "paint": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    }

    for app in applications:
        if app in query:
            os.startfile(applications[app])
            speak(f"Opening {app}")
            break
    else:
        speak("Application not found")

if __name__ == '__main__':
    wish()
    while True:
        query = take_command()

        if "open" in query:
            open_application(query)
        elif "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
                print(results)
            except wikipedia.DisambiguationError as e:
                speak(f"Multiple matches found. Please be more specific. {e}")
            except wikipedia.PageError as e:
                speak(f"Sorry, no results found. {e}")
        elif "open youtube" in query:
            webbrowser.open("https://www.youtube.com")
        elif "open google" in query:
            speak("Sir, what should I search on Google?")
            search_query = take_command()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
        elif "no thanks" in query:
            speak("Thanks for using me, sir. Have a good day!")
            speak("Sir, do you have any other work?")
            sys.exit()
