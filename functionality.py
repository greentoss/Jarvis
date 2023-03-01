import json
import os
import random

import docx
import psutil
import subprocess
import sys
import time
import webbrowser
import datetime
import openai
from PIL import ImageGrab

from config import BOT_NAME
from wordsCollections import phrases_printNote

import voice
from app import setDevice, q
from dotenv import load_dotenv

try:
    import requests  # pip install requests
except:
    pass


def chrome():
    webbrowser.open('https://www.google.com', new=2)


def chromeAny(link):
    chrome_pid = None
    for p in psutil.process_iter(['pid', 'name']):
        if 'chrome' in p.name().lower():
            chrome_pid = p.pid
            break

    if chrome_pid is None:
        webbrowser.get('chrome').open(link, new=2)
    else:
        webbrowser.get('chrome').open_new_tab(link)


def showNatalia():
    webbrowser.open('https://www.instagram.com/ferocious.flu/?hl=af', new=2)


def chromeGoogle():
    webbrowser.open('https:/google.com', new=2)


def chromeChatGPT():
    webbrowser.open('https://chat.openai.com/chat', new=2)


def offBot():
    """turn off the bot"""
    sys.exit()


def restartBot():
    """restart the bot"""
    python = sys.executable
    os.execl(python, python, *sys.argv)


def muteBot():
    """makes bot temporary stop listening"""
    print('bot has been muted')


def unmuteBot():
    """makes bot temporary stop listening"""
    print('bot has been unmuted')


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


def writeTheNote(rec):
    """
    Listens for speech input and prints the words that are spoken
    """
    setDevice(0, 5)
    data_array = []  # initialize an empty array to store the spoken words
    voice.speaker('im listening, stop command is: stop recording')

    while True:
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


def confirmCommand(action, rec):
    """
    Listens for speech input and prints the words that are spoken
    """
    setDevice(0, 5)

    voice.speaker(f'confirm the action {action}, key phrase is: "yes i confirm" or "decline"')

    confirm = None

    while True:
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
    # confirmation = confirmCommand('sleep the computer')
    confirmation = True
    if confirmation:
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
    # confirmation = confirmCommand('turn off the computer')
    confirmation = True
    if confirmation:
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


def remindTaxSending():
    """
    This function checks the date every day at 8 am using the getCurrentDate function.
    If the date is the 1st day of the month, it prints a reminder message to pay taxes.
    """
    while True:
        now = datetime.datetime.now()
        if now.hour == 8 and now.day == 1:
            print("You need to send taxes values today.")
            voice.speaker("You need to send taxes values today.")
            chromeAny('https://my.kyiv.yasno.com.ua/accounts')
            chromeAny('https://kte.kmda.gov.ua/my-cabinet/send_counters/guest_send_current_new')
            time.sleep(24 * 60 * 60)  # wait for 24 hours before checking the date again
        else:
            # wait for 1 hour before checking the time again
            time.sleep(60 * 60)


def goodMorning():
    """
    This function checks the weather every day at 8 am using the getCurrentWeather function.
    """
    while True:
        now = datetime.datetime.now()
        if now.hour == 8:
            goodMorningGreetingUser()
            time.sleep(24 * 60 * 60)  # wait for 24 hours before checking the weather again
        else:
            # wait for 1 hour before checking the time again
            time.sleep(60 * 60)


def goodMorningGreetingUser():
    voice.speaker('Good Morning, Vlady! New day has come!')
    voice.speaker(sayDayOfWeek())
    getCurrentWeather()
    voice.speaker('Today you have 0 active tasks, 0 urgent tasks')


def sayDayOfWeek():
    """
    This function says what day of the week it is and reminds the user if it is a weekend.
    """
    today = datetime.datetime.today()
    day_of_week = today.strftime("%A")  # get the day of the week as a string

    if day_of_week == "Saturday" or day_of_week == "Sunday":
        message = f"Today is {day_of_week}, and it's the weekend! Enjoy your time off."
    else:
        message = f"Today is {day_of_week}. It's a workday, so let's get started!"
    return message


def askGPT(rec):
    """
    Listens for speech input and prints the words that are spoken
    """
    load_dotenv()
    openai.api_key = os.environ.get("OPEN_AI_API_KEY")

    setDevice(0, 5)

    voice.speaker('im listening, when you finish asking, say: stop asking')

    while True:
        result = ''
        data = q.get()
        if rec.AcceptWaveform(data):
            data = json.loads(rec.Result())['text']
            print(f"USER: {data}")
            result += data
            if data.lower() == 'stop asking' or 'the stop asking':
                words = result.split()
                trimmed_words = words[:-2]
                result = " ".join(trimmed_words)
                ask_question(result)
                break  # stop listening when phrase collected


def ask_question(question):
    prompt = f"Question: {question}\nAnswer:"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response.choices[0].text.strip()
    print(f"Q: {question}\nA: {answer}")
    voice.speaker(answer)


