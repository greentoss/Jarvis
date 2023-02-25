import queue
import sounddevice as sd
import vosk
import json
from sklearn.feature_extraction.text import CountVectorizer     #pip install scikit-learn
from sklearn.linear_model import LogisticRegression
from functionality import *
import words
import voice

# Требуется:
# pip install vosk
# pip install sounddevice
# pip install scikit-learn
# pip install pyttsx3
# Не обязательно:
# pip install requests

q = queue.Queue()

model = vosk.Model('model-en')

#command: python -m sounddevice  #shows your devices indexes

device = sd.default.device = 0, 5      #input, output [1, 4]
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def recognise(data, vectorizer, clf):
    '''
    Анализ распознанной речи
    '''

    #проверяем есть ли имя бота в data, если нет, то return
    trigger = words.TRIGGERS.intersection(data.split())
    if not trigger:
        return

    #удаляем имя бота из текста
    data.replace(list(trigger)[0], '')

    #получаем вектор полученного текста
    #сравниваем с вариантами, получая наиболее подходящий ответ
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    #     print(answer)
    #получение имени функции из ответа из data_set
    func_name = answer.split()[0]

    #озвучка ответа из модели data_set
    voice.speaker(answer.replace(func_name, ''))

    #запуск функции из skills
    exec(func_name + '()')



def main():
    '''
    Обучаем матрицу ИИ
    и постоянно слушаем микрофон
    '''
    voice.speaker('... hello, Vlady. JARVIS is online, and ready to serve!')

    #Обучение матрицы на data_set модели
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set

    #постоянная прослушка микрофона
    with sd.RawInputStream( samplerate = samplerate,   #how many times per second microphone takes data
        blocksize = 12000,           #how mani information is transferred
        device = device[0],            #index of microphone
        dtype = 'int16',
        channels = 1,
        callback = callback ):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                print(data)
                recognise(data, vectorizer, clf)
#             else:
    #             print(rec.PartialResult())

    #             data = json.loads(rec.PartialResult())['partial']
    #             print(data)



if __name__ == '__main__':
    main()

#command: python app.py
