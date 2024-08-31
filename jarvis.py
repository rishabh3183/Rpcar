import cv2
import webbrowser
import os
import pyttsx3
import datetime
import pywhatkit as kit
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import wikipedia
from colorama import init, Fore
from googlesearch import search
import platform
import subprocess
import openai  # Import OpenAI library
import ctypes
import random
import pyautogui

# Initialize colorama
init()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize a global variable to store the last response
last_response = ""

# Flag to control sleep mode
sleep_mode = False

# Set up OpenAI API key
openai.api_key = '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'  # Replace 'your-api-key' with your actual API key

# Function to close the web browser based on the platform
def close_web_browser():
    system_platform = platform.system()
    if system_platform == "Windows":
        os.system("taskkill /f /im chrome.exe")  # Close Google Chrome
        os.system("taskkill /f /im msedge.exe")  # Close Microsoft Edge
    elif system_platform == "Linux":
        os.system("pkill chrome")  # Adjust this command for your browser
        os.system("pkill msedge")  # Adjust this command for your browser
    elif system_platform == "Darwin":  # macOS
        os.system("pkill -a Safari")  # Adjust this command for your browser
    else:
        print("Unsupported platform.")

# Function to get image files from the wallpaper folder
def get_wallpaper_images(folder_path):
    image_files = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            image_files.append(os.path.join(folder_path, file_name))
    return image_files

# Function to change the desktop wallpaper
def change_wallpaper(image_path):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

# Function to speak out the given text
def speak(text, replay=False, close_webpage=False):
    global last_response
    if close_webpage:
        close_web_browser()
        last_response = ""
        return
    if replay and last_response:
        engine.say(last_response)
    else:
        engine.say(text)
        last_response = text
    engine.runAndWait()

# Function to greet the user
def greet():
    global sleep_mode
    if sleep_mode:
        speak("I'm awake now!")
        sleep_mode = False
    else:
        current_time = datetime.datetime.now()
        if current_time.hour < 12:
            speak("Good morning!")
        elif 12 <= current_time.hour < 18:
            speak("Good afternoon!")
        else:
            speak("Good evening!")
        speak("I am Jarvis. How can I assist you today?")

# Function to listen to the user's voice command
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(Fore.GREEN + "Listening..." + Fore.RESET)
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print(Fore.GREEN + "Recognizing..." + Fore.RESET)
        query = recognizer.recognize_google(audio, language='en')
        print(Fore.YELLOW + f"User said: {query}\n" + Fore.RESET)
        if 'sleep jarvis' in query:
            global sleep_mode
            speak("Going to sleep mode.")
            sleep_mode = True
        elif 'close' in query:  # Check for the command "close"
            speak("Closing webpage.", close_webpage=True)
        return query.lower()
    except Exception as e:
        print(Fore.RED + "Sorry, I couldn't understand that." + Fore.RESET)
        return ""

# Function to perform a Google search and speak the search results
def google_search(query):
    speak("Performing a Google search...")
    search_results = list(search(query))
    if search_results:
        speak("Here are the top search results:")
        for i, result in enumerate(search_results):
            try:
                # Extract title and description from the search result page
                response = requests.get(result)
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('title').text.strip()
                description = soup.find('meta', attrs={'name': 'description'})
                if description:
                    description = description.get('content').strip()
                    speak(f"Result {i + 1}: {title}. {description}")
                else:
                    speak(f"Result {i + 1}: {title}")
            except Exception as e:
                print(f"Error processing search result: {e}")
    else:
        speak("Sorry, I couldn't find any relevant results.")

# Function to search Wikipedia and speak the summary
def search_wikipedia(query):
    speak("Searching Wikipedia...")
    try:
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("There are multiple results. Can you be more specific?")
    except wikipedia.exceptions.PageError as e:
        speak("Sorry, I couldn't find any information on that topic.")
    except Exception as e:
        speak("Sorry, I encountered an error while searching Wikipedia.")

# Function to provide weather information
def consult_weather():
    # Replace with your weather API call or implementation
    weather_data = "The weather today is sunny with a temperature of 25 degrees Celsius."
    speak(weather_data)

# Function to suggest nearby restaurants
def consult_restaurants():
    # Replace with your restaurant recommendation logic
    restaurant_data = "I found a nearby Italian restaurant called Bella Italia. Would you like more suggestions?"
    speak(restaurant_data)

# Function to generate text using OpenAI
def generate_text(prompt):
    try:
        response = openai.Completion.create(
            engine="gpt-4-0125-preview",  # Choose the engine you want to use
            prompt=prompt,
            max_tokens=50  # Adjust the max tokens based on your requirements
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("Error:", e)
        return None

# Function to minimize the current window
def minimize_window():
    pyautogui.hotkey('win', 'down')

# Function to maximize the current window
def maximize_window():
    pyautogui.hotkey('win', 'up')

# Function to close the current window
def close_window():
    pyautogui.hotkey('alt', 'f4')

# Function to turn on Wi-Fi
def turn_on_wifi():
    system_platform = platform.system()
    if system_platform == "Windows":
        subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "enabled"])
        speak("Wi-Fi turned on.")
    else:
        speak("Sorry, Wi-Fi control is not supported on this platform.")

# Function to turn off Wi-Fi
def turn_off_wifi():
    system_platform = platform.system()
    if system_platform == "Windows":
        subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "disabled"])
        speak("Wi-Fi turned off.")
    else:
        speak("Sorry, Wi-Fi control is not supported on this platform.")

# Function to turn on Bluetooth
def turn_on_bluetooth():
    system_platform = platform.system()
    if system_platform == "Windows":
        subprocess.run(["btpair", "on"])
        speak("Bluetooth turned on.")
    else:
        speak("Sorry, Bluetooth control is not supported on this platform.")

# Function to turn off Bluetooth
def turn_off_bluetooth():
    system_platform = platform.system()
    if system_platform == "Windows":
        subprocess.run(["btpair", "off"])
        speak("Bluetooth turned off.")
    else:
        speak("Sorry, Bluetooth control is not supported on this platform.")

# Main function to handle user commands
def main():
    wallpaper_folder = "/path/to/wallpaper/folder"  # Update with your wallpaper folder path
    is_sleeping = False  # Variable to track sleep mode
    while True:
        if not is_sleeping:
            query = listen()
        else:
            query = "hello jarvis"  # Simulate saying "Hello Jarvis" to exit sleep mode
        if 'hello jarvis' in query:
            if is_sleeping:
                is_sleeping = False
                speak("Good to see you back! How can I assist you today?")
            else:
                greet()
        elif 'sleep jarvis' in query:
            is_sleeping = True
            speak("Going into sleep mode. Wake me up by saying 'Hello Jarvis'.")
        elif not is_sleeping:
            if 'search on google' in query:
                speak("What do you want to search on Google?")
                google_query = listen()
                google_search(google_query)
            elif 'open wikipedia' in query:
                speak("What do you want to search on Wikipedia?")
                wiki_query = listen()
                search_wikipedia(wiki_query)
            elif 'time' in query:
                current_time = datetime.datetime.now().strftime("%H:%M")
                speak(f"The current time is {current_time}")
            elif 'weather' in query:
                consult_weather()
            elif 'restaurants' in query:
                consult_restaurants()
            elif 'quit' in query or 'exit' in query:
                speak("Goodbye!")
                break
            elif "open camera" in query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break
                cap.release()
                cv2.destroyAllWindows() 
            elif "open youtube" in query:
                webbrowser.open("https://youtube.com")
            elif "open image generator" in query:
                 webbrowser.open("https://www.fotor.com/ai-image-generator/")
            elif "open facebook" in query:
                webbrowser.open("https://facebook.com")
            elif "open instagram" in query:
                webbrowser.open("https://instagram.com")
            elif "open google" in query:
                webbrowser.open("https://www.google.com/webhp")
            elif "open whatsapp" in query:
                webbrowser.open("https://web.whatsapp.com")
            elif "play songs on youtube" in query:
                kit.playonyt("Party Songs 2023")
            elif "shutdown the system" in query:
                speak("Shutting down the system. Goodbye!")
                os.system("shutdown /s /t 5")
            elif "open snapchat"  in query:
                webbrowser.open("https://www.snapchat.com")
            elif "close webpage" in query:
                speak("Closing webpage.", close_webpage=True)
            elif "generate text" in query:
                speak("What do you want me to generate?")
                prompt = listen()
                generated_text = generate_text(prompt)
                if generated_text:
                    speak(generated_text)
                else:
                    speak("Sorry, I couldn't generate text at the moment.")
            elif "change wallpaper" in query:
                # Get wallpaper images from the folder
                wallpaper_images = get_wallpaper_images(wallpaper_folder)
                if wallpaper_images:
                    selected_image = random.choice(wallpaper_images)
                    change_wallpaper(selected_image)
                    speak("Wallpaper changed successfully!")
                else:
                    speak("No wallpaper images found in the folder.")
            elif "minimize window" in query:
                minimize_window()
                speak("Window minimized.")
            elif "maximize window" in query:
                maximize_window()
                speak("Window maximized.")
            elif "close window" in query:
                close_window()
                speak("Window closed.")
            elif "turn on Wi-Fi" in query:
                turn_on_wifi()
            elif "turn off Wi-Fi" in query:
                turn_off_wifi()
            elif "turn on Bluetooth" in query:
                turn_on_bluetooth()
            elif "turn off Bluetooth" in query:
                turn_off_bluetooth()
            # Add other commands as needed
        else:
            speak("I'm in sleep mode. Wake me up by saying 'Hello Jarvis'.")

if __name__ == "__main__":
    main()
