import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS

from googletrans import Translator  # text translator

import os

#AudioSegment.converter = r'C:\Users\jjopk\Desktop\AI\Django\mylinebot\static\ffmpeg\bin\ffmpeg.exe'#輸入自己的ffmpeg.exe路徑

def speech_to_text(path):
    r = sr.Recognizer()
    sound = AudioSegment.from_file_using_temporary_files(path)
    path = os.path.splitext(path)[0]+'.wav'
    sound.export(path, format="wav")
    with sr.AudioFile(path) as source:
        audio = r.record(source)
    text = r.recognize_google(audio,language='zh-Hant') # 設定要以什麼文字轉換
#    translator = Translator()
#    results = translator.translate(text,lang='ja')
#    print(type(results))
    return text
