from django.shortcuts import render  #-------------
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden  #--------
from django.views.decorators.csrf import csrf_exempt  #----------------
from django.conf import settings  #-------------

from linebot import LineBotApi, WebhookParser  #---------------
from linebot.exceptions import InvalidSignatureError, LineBotApiError  #---------
from linebot.models import * #-------------------------

# image processing
import matplotlib.pyplot as pl
import pytesseract

# easyocr
#from easyocr import Reader
#import easyocr
from PIL import Image,ImageDraw


from tellingbot.mymoduel.translate import *
from tellingbot.mymoduel.img_to_text import *
from tellingbot.mymoduel.speech_to_text import *

# speech
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS


import os
import sys
import string
import random
import time
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
lang = "chi_tra+eng"



line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
 
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        message=[]
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                print(event.message.type)
                if event.message.type=='text':
                    result=translate(event.message.text)
                    print(type(result))
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text=result))
                elif event.message.type=='image':
                    image_content = line_bot_api.get_message_content(event.message.id)
                    image_name = '123.jpg'
                    path='./static/'+image_name
                    with open(path, 'wb') as fd:
                        for chunk in image_content.iter_content():
                            fd.write(chunk)
                    text1 = image_to_text(path) # use filename
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=text1)
                )
                elif event.message.type=='audio':
                    message.append(TextSendMessage(text='聲音訊息'))
                    # 將音訊檔案儲存
                    audio_content = line_bot_api.get_message_content(event.message.id) # 音訊訊息
                    audio_name = 'sound.wav'
                    path='./static/'+audio_name
                    with open(path, 'wb') as fd:
                        for chunk in audio_content.iter_content():  #將音訊訊息存成檔案
                            fd.write(chunk)
  
                    #進行語音轉文字處理
                    results=speech_to_text(path)
                    #將轉換的文字回傳給用戶 語音轉語音(未解)
                    #message.append(TextSendMessage(text=text))
                    #line_bot_api.reply_message(event.reply_token,message)

                    #out=ffmpeg.output(audio, video, 'out.m4a')

#                    message.append(TextSendMessage(text=results))
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=results))
                elif isinstance(event, PostbackEvent):
                    print('PostbackEvent')
                    
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()



    
