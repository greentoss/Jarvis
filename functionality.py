import os, webbrowser, sys, requests, subprocess, pyttsx3, psutil, time, ctypes
from PIL import ImageGrab

import voice

try:
	import requests		#pip install requests
except:
	pass

def chrome():
	'''Открывает браузер заданнный по уполчанию в системе с url указанным здесь'''
	webbrowser.open('https://www.google.com', new=2)

def chromeGoogle():
   	webbrowser.open('https:/google.com', new=2)

def chromeChatGPT():
   	webbrowser.open('https://chat.openai.com/chat', new=2)

def offBot():
	'''Отключает бота'''
	sys.exit()

def passive():
	'''Функция заглушка при простом диалоге с ботом'''
	pass

def passiveUpper(command):
    if command == "what is his name":
        # Respond with the name of your best friend
        return "His name is Valera."
    else:
        # If the command is not recognized, respond with an error message
        return "Sorry, I did not understand your question."

def openTelegram():
    '''Opens the Telegram application'''
    try:
        subprocess.Popen(r'C:/Users/vlady/AppData/Roaming/Telegram Desktop/Telegram.exe')
#         voice.speaker('the Telegram application has been opened')
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

def sleepComputer():
    print("You have 20 seconds to confirm the action.")
    voice.speaker('You have 20 seconds to confirm the action.')
    start_time = time.time()
    confirmation = "y"
    while time.time() - start_time < 20:
            confirmation = input("Are you sure you want to put the computer to sleep? (y/n): ")
            if confirmation.lower() == "y":
                try:
                    ctypes.windll.PowrProf.SetSuspendState(0, 0, 0)
                except Exception as e:
                    print(f"Error going to sleep: {e}")
                    voice.speaker('i cant execute this function, check the code')
            elif confirmation.lower() == "n":
                print("Aborted.")
                voice.speaker('cancel operation')
                break
    else:
        print("Aborted.")
        voice.speaker('Aborted operation')

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


