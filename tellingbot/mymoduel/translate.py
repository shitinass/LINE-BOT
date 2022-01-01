# text to text
from googletrans import Translator


def translate(text):
#text=input()
    translator = Translator()
    results = translator.translate(text, dest='en')
    result1 = translator.translate(text, dest='ja')
    result2 = translator.translate(text, dest='zh-tw')
    result3 = results.text + '\n' + result1.text + '\n' + result2.text
#print(result3)
    return result3
