import pyttsx3  # pip install pyttsx3
from config import BOT_GENDER

# initialisation of voicee "engine" on program start
#
# Голос берется из системы, первый попавшийся
#
# additional materials:
# https://pypi.org/project/pyttsx3/
# https://pyttsx3.readthedocs.io/en/latest/
# https://github.com/nateshmbhat/pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 180)  # speed of the voice

"""VOICE"""
voices = engine.getProperty('voices')  # getting details of current voice
# engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
if BOT_GENDER == 'FEMALE':
    engine.setProperty('voice', voices[1].id)  # changing index, changes voices. 1 for female


def speaker(text):
    '''text voicing'''
    engine.say(text)
    engine.runAndWait()
