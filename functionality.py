import os, webbrowser, sys, requests, subprocess, pyttsx3, psutil, time, ctypes
from PIL import ImageGrab

import voice
import obswebsocket
import sounddevice as sd
import queue
import vosk
import json

q = queue.Queue()
model = vosk.Model('model-en')

try:
	import requests		#pip install requests
except:
	pass

def chrome():
	webbrowser.open('https://www.google.com', new=2)

def chromeGoogle():
   	webbrowser.open('https:/google.com', new=2)

def chromeChatGPT():
   	webbrowser.open('https://chat.openai.com/chat', new=2)

def offBot():
	'''Отключает бота'''
	sys.exit()

def passive(reply):
	'''Функция заглушка при простом диалоге с ботом'''
	print(f"JARVIS: {reply}")
# 	pass

def openTelegram():
    '''Opens the Telegram application'''
    try:
        subprocess.Popen(r'C:/Users/vlady/AppData/Roaming/Telegram Desktop/Telegram.exe')
    except Exception as e:
        voice.speaker('Sorry i can not open Telegram')
        print(f"Error opening Telegram: {e}")

def closeTelegram():
    '''Closes the Telegram application'''
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

def startObsRecording():
    '''Starts recording a video inside OBS studio'''
    try:
        # Connect to the OBS WebSocket server
        print("Connecting to OBS WebSocket server...")
        obsws = obswebsocket.obsws("localhost", 4444, "12345678t")
        print(obws, 'obsws ')
        obsws.connect()

        # Start recording
        response = obsws.call(obswebsocket.requests.StartRecording())
        if not response.status:
            print("Failed to start recording")
        else:
            print("Recording started")
    except Exception as e:
        print(f"Error starting OBS recording: {e}")
    finally:
        obsws.disconnect()

def stopObsRecording():
    '''Stops the current recording in OBS studio'''
    try:
        # Connect to the OBS WebSocket server
        obsws = obswebsocket.obsws("localhost", 4455, "12345678t")
        obsws.connect()

        # Stop recording
        response = obsws.call(obswebsocket.requests.StopRecording())
        if not response.status:
            print("Failed to stop recording")
        else:
            print("Recording stopped")
    except Exception as e:
        print(f"Error stopping OBS recording: {e}")
    finally:
        obsws.disconnect()

def takeScreenshot():
    '''Takes a screenshot of the entire screen and saves it as a PNG image on the desktop'''
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

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def writeTheNote():
    '''
    Listens for speech input and prints the words that are spoken
    '''
    device = sd.default.device = 0, 5      #input, output [1, 4]
    samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])
    with sd.RawInputStream(samplerate=samplerate,
        blocksize=12000,
        device=device[0],
        dtype='int16',
        channels=1,
        callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                print(f"USER: {data}")
#                 createDocAndWrite(data)
                break
            else:
                print(rec.PartialResult())

def createDocAndWrite(data):
    try:
        # Create new Word document and add text from data
        doc = docx.Document()
        doc.add_paragraph(data)

        # Save Word document to current working directory
        doc.save("transcription.docx")

        print("Transcription saved to 'transcription.docx'")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Speech Recognition service; {e}")

# def sleepComputer():
#     confirmation = ""
#     while confirmation not in ["y", "n"]:
#         confirmation = input("Are you sure you want to put the computer to sleep? (y/n): ")
#     if confirmation.lower() == "y":
#         try:
# #             ctypes.windll.PowrProf.SetSuspendState(0, 0, 0)
#             print('sleep')
#         except Exception as e:
#             print(f"Error going to sleep: {e}")
#             voice.speaker('i cant execute this function, check the code')
#     else:
#         print("Aborted.")
#         voice.speaker('cancel operation')


# def sleepComputer():
#     print("You have 20 seconds to confirm the action.")
#     # voice.speaker('You have 20 seconds to confirm the action.')
#     r = sr.Recognizer()
#     mic = sr.Microphone()
#     with mic as source:
#         r.adjust_for_ambient_noise(source)
#         audio = r.listen(source, timeout=20)
#         try:
#             confirmation = r.recognize_google(audio)
#         except sr.UnknownValueError:
#             print("Could not understand audio")
#             return
#         except sr.RequestError as e:
#             print(f"Could not request results from Google Speech Recognition service; {e}")
#             return
#
#     if confirmation.lower() == "yes":
#         try:
#             ctypes.windll.PowrProf.SetSuspendState(0, 0, 0)
#         except Exception as e:
#             print(f"Error going to sleep: {e}")
#             # voice.speaker('i cant execute this function, check the code')
#     elif confirmation.lower() == "no":
#         print("Aborted.")
#         # voice.speaker('cancel operation')
#     else:
#         print("Invalid response.")
#         # voice.speaker('invalid response')

def checkWeather():
    '''This function uses the OpenWeatherMap API to get the weather information for Kyiv.'''
    try:
        params = {'q': 'Kyiv', 'units': 'metric', 'lang': 'en', 'appid': '2d44b0725ade625eede22d4c56bebb8e'}

#         response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params)
        response = requests.get('http://api.openweathermap.org/geo/1.0/direct?q=Kyiv&appid=2d44b0725ade625eede22d4c56bebb8e')
        print(response)
        if response.status_code != 200:
            raise Exception('Invalid response from API')

        weather = response.json()
        description = weather['weather'][0]['description']
        temperature = round(weather['main']['temp'])
        voice.speaker(f"Outside, it is {description} and {temperature} degrees Celsius.")
    except Exception as e:
        voice.speaker(f"Could not connect to API: {e}")

# def game():
# 	'''Нужно разместить путь к exe файлу любого вашего приложения'''
# 	try:
# 		subprocess.Popen('C:/Program Files/paint.net/PaintDotNet.exe')
# 	except:
# 		voice.speaker('Путь к файлу не найден, проверьте, правильный ли он')
#
#
# def offpc():
# 	#Эта команда отключает ПК под управлением Windows
#
# 	#os.system('shutdown \s')
# 	print('пк был бы выключен, но команде # в коде мешает;)))')


