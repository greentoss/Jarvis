import json
import os
import random

import docx
import psutil
import subprocess
import sys
import time
import webbrowser
import obswebsocket
from PIL import ImageGrab

from config import BOT_NAME
from wordsCollections import phrases_printNote

import voice
from app import setDevice, samplerate, device, sd, vosk, q, model, callbackToListen

try:
    import requests  # pip install requests
except:
    pass


def chrome():
    webbrowser.open('https://www.google.com', new=2)


def chromeGoogle():
    webbrowser.open('https:/google.com', new=2)


def chromeChatGPT():
    webbrowser.open('https://chat.openai.com/chat', new=2)


def offBot():
    """turn off the bot"""
    sys.exit()


def passive(reply):
    """shallow function just dialog vs bot"""
    print(f"{BOT_NAME}: {reply}")


def openTelegram():
    """Opens the Telegram application"""
    try:
        subprocess.Popen(r'C:/Users/vlady/AppData/Roaming/Telegram Desktop/Telegram.exe')
    except Exception as e:
        voice.speaker('Sorry i can not open Telegram')
        print(f"Error opening Telegram: {e}")


def closeTelegram():
    """Closes the Telegram application"""
    for proc in psutil.process_iter():
        try:
            # Look for the Telegram process by name
            if "Telegram.exe" in proc.name():
                proc.kill()
                print("Telegram closed successfully")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            voice.speaker('Sorry i can not close Telegram')
            pass
    print("Telegram process not found")
    return False


def takeScreenshot():
    """Takes a screenshot of the entire screen and saves it as a PNG image on the desktop"""
    try:
        # Capture a screenshot of the entire screen
        img = ImageGrab.grab()
        # Save the screenshot as a PNG image on the desktop with a timestamp in the filename
        img_name = time.strftime("screenshot_%Y%m%d-%H%M%S.png")
        img_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', img_name)
        img.save(img_path)
        print(f"Screenshot saved as {img_path}")
    except Exception as e:
        print(f"Error taking screenshot: {e}")


def abortExecution():
    """
    Listens for speech input and stops all ongoing functions if the phrase "abort execution" is detected
    """
    setDevice(0, 5)

    with sd.RawInputStream(samplerate=samplerate,
                           blocksize=12000,
                           device=device[0],
                           dtype='int16',
                           channels=1,
                           callback=callbackToListen):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                print(f"USER: {data}")
                if data.lower() == 'abort execution' or data.lower() == 'the abort execution':
                    # Stop all ongoing functions
                    return True


def writeTheNote():
    """
    Listens for speech input and prints the words that are spoken
    """
    setDevice(0, 5)
    data_array = []  # initialize an empty array to store the spoken words
    voice.speaker('im listening, stop command is: stop recording')

    with sd.RawInputStream(samplerate=samplerate,
                           blocksize=12000,
                           device=device[0],
                           dtype='int16',
                           channels=1,
                           callback=callbackToListen):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            if abortExecution():  # immediately Stop the function
                return
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                print(f"USER: {data}")
                data_array.append(data)  # add the spoken words to the array
                if data.lower() == 'stop recording' or data.lower() == 'the stop recording':
                    createDocAndWrite(data_array)  # pass the array to createDocAndWrite() function
                    data_array.clear()
                    break  # stop listening when phrase collected
                voice.speaker(random.choice(phrases_printNote))  # select a random prompt from the collection
            # else:
            #     print(rec.PartialResult())


def createDocAndWrite(data_array):
    try:
        # Create new Word document and add text from data
        doc = docx.Document()
        for data in data_array:
            doc.add_paragraph(data)

        # Save Word document to desktop
        note_name = time.strftime("document_%Y%m%d-%H%M%S.docx")
        note_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', note_name)
        doc.save(note_path)
        voice.speaker('all your notes has been saved on desktop')

        print("Transcription saved to 'transcription.docx'")
    except Exception as e:
        print(f"Error could not dave document: {e}")


def confirmCommand(action):
    """
    Listens for speech input and prints the words that are spoken
    """
    setDevice(0, 5)

    voice.speaker(f'confirm the action {action}, key phrase is: "yes i confirm" or "decline"')

    confirm = None

    with sd.RawInputStream(samplerate=samplerate,
                           blocksize=12000,
                           device=device[0],
                           dtype='int16',
                           channels=1,
                           callback=callbackToListen):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            if abortExecution():  # immediately Stop the function
                return
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                print(f"USER: {data}")
                if data.lower() == 'yes i confirm' or data.lower() == 'yes' or data.lower() == 'the confirm':
                    confirm = True
                    voice.speaker('confirm = true')
                    break  # stop listening when phrase collected
                if data.lower() == 'no i decline' or data.lower() == 'the decline' or data.lower() == 'no':
                    confirm = False
                    voice.speaker('confirm = false')
                    break  # stop listening when phrase collected
                voice.speaker('i did not get what you say, repeat pls')  # select a random prompt from the collection
            # else:
            #     print(rec.PartialResult())
    return confirm


def sleepComputer():
    """
    Listens for speech input for confirmation and makes computer sleep
    """
    confirmation = confirmCommand('sleep the computer')
    if confirmation:
        if abortExecution():  # immediately Stop the function
            return
        try:
            # ctypes.windll.PowrProf.SetSuspendState(0, 0, 0)
            print('sleep the PC')
        except Exception as e:
            print(f"Error going to sleep: {e}")
            voice.speaker('i cant execute this function, check the code')
    else:
        print("Aborted.")
        voice.speaker('cancel operation')


def offPc():
    """
    Listens for speech input for confirmation and turns off PC
    """
    confirmation = confirmCommand('turn off the computer')
    if confirmation:
        if abortExecution():  # immediately Stop the function
            return
        try:
            # os.system('shutdown \s')
            print('turn off PC')
        except Exception as e:
            print(f"Error doing turn off: {e}")
            voice.speaker('i cant execute this function, check the code')
    else:
        print("Aborted.")
        voice.speaker('cancel operation')


def getCurrentWeather():
    """
    This function uses the OpenWeatherMap API to get the weather information for Kyiv.
    """
    city_name = 'Kyiv'
    api_key = "f12828f8ec0437c8e5d17558fe5d2a0c"
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            # print(data)
            formatWeatherData(data)
    except Exception as e:
        print(f"Could not connect to API: {e}")


def formatWeatherData(weather_data):
    city = weather_data['name']
    weather = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    wind_direction = weather_data['wind']['deg']
    if 'rain' in weather_data:
        precipitation = 'raining'
    elif 'snow' in weather_data:
        precipitation = 'snowing'
    else:
        precipitation = 'no rain or snow'
    result = f"The weather in {city} is {weather}, {temperature:.1f} degrees Celsius. It feels like {feels_like:.1f} degrees Celsius. The humidity is {humidity}% and the wind speed is {wind_speed} m/s from {wind_direction} degrees. There is {precipitation}."
    print(result)
    voice.speaker(result)


