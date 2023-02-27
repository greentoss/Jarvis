import json
import queue
import random

import sounddevice as sd
import vosk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

import voice
import wordsCollections

# pip install vosk
# pip install sounddevice
# pip install scikit-learn
# pip install pyttsx3

BOT_NAME = 'JARVIS'

q = queue.Queue()
model = vosk.Model('model-en')

# Declare device and samplerate variables outside of functions
device = None
samplerate = None


# command: python -m sounddevice  #shows your devices indexes

# device = sd.default.device = 0, 5      #input, output [1, 4]
# samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])

def setDevice(input, output):
    global device, samplerate  # declare the variables as global to modify them
    device = sd.default.device = input, output
    samplerate = int(sd.query_devices(device[input], 'input')['default_samplerate'])


setDevice(0, 5)


def callbackToListen(indata, frames, time, status):
    q.put(bytes(indata))


def recognise(data, vectorizer, clf):
    '''
    Voice recognition analisys
    '''

    # check if botname trigger word is in data
    trigger = wordsCollections.TRIGGERS.intersection(data.split())
    if not trigger:
        return

    # delete bot name from text
    data.replace(list(trigger)[0], '')

    # get the vector of the text
    # compare with variants, getting the most sufficient answer
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    #     print(answer)

    # get the function name from collection data_set
    func_name = answer.split()[0]

    # voice acting of the answer from collection data_set
    reply = answer.replace(func_name, '')
    voice.speaker(reply)

    # starting the function from "functionality"
    func = globals()[func_name]
    if func.__code__.co_argcount > 0:
        func(reply)
    else:
        func()


def greetingMessage(messages):
    '''Speaks a random message from an array of strings from "wordsCollections"'''
    if isinstance(messages, list):
        message = random.choice(messages)
        print(f"{BOT_NAME}: {message}")
        voice.speaker(message)
    else:
        print("Error: messages parameter must be a list")


def main():
    '''
    Teaching matrix AI
    and listen to microphone continuously
    '''
    global device, samplerate  # declare the variables as global to access them

    greetingMessage(wordsCollections.greetMessages)

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(wordsCollections.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(wordsCollections.data_set.values()))

    del wordsCollections.data_set

    # continuously listen to microphone
    with sd.RawInputStream(samplerate=samplerate,  # how many times per second microphone takes data
                           blocksize=12000,  # how mani information is transferred
                           device=device[0],  # index of microphone
                           dtype='int16',
                           channels=1,
                           callback=callbackToListen):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                print(f"USER: {data}")
                recognise(data, vectorizer, clf)

            # else:
            #     print(rec.PartialResult())


#             data = json.loads(rec.PartialResult())['partial']
#             print(data)


if __name__ == '__main__':
    main()

# command: python app.py
