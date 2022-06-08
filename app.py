from email.mime import image
import os
import re
import urllib
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


app = Flask(__name__)
line_bot_api = LineBotApi("+4c+TJ4dHfpEIsAY3L3LIdEmb8RZFTCDezGFjXQ1lltT6fGyDO5Nxbgx8FpRhkI3CGi43KU5sI79Xk75StU7ot95s/RAqcUcBDQwqBwf36W819plH7QckBa9C/IqN4Rl5uolz7mRo9ozGqu4KKzKkgdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("a7420fa246b9ca505639127a4d17a6b4")

line_bot_api.push_message("U0df021adfd3f8fe6ed8df8df5c331652",TextSendMessage(text="你可以開始了"))

#回報heroku和linebot是否串接成功
#監聽所有來自 /callback的Post Request
@app.route("/callback", methods=["POST"])
def callback():
    #get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    #get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    print(body) #檢查出錯的地方

    #handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"



#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if re.match("你是誰",message): #回覆訊息及回傳貼圖
        sticker_message = StickerMessage(
            package_id = "446",
            sticker_id = "2027"
        )
        line_bot_api.reply_message(event.reply_token,[sticker_message, TextSendMessage("才不告訴你呢!")])
        
    elif re.match("傻眼",message): #回傳貼圖
        sticker_message = StickerMessage(
            package_id = "446",
            sticker_id = "1995"
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)

    elif re.match("去哪裡", message): #回傳地點位置
        location_message = LocationSendMessage(
            title = "台北市立動物園",
            address = "116台北市文山區新光路二段30號",
            latitude = 24.99825495043049,
            longitude =  121.5816754546207 
        )
        line_bot_api.reply_message(event.reply_tpken, location_message)

    elif re.match("幹嘛", message): #回傳圖片
        image_message = ImageSendMessage(
            original_content_url = "https://www.publicdomainpictures.net/pictures/270000/velka/weather-forecast.jpg",
            preview_image_url = "https://www.publicdomainpictures.net/pictures/270000/velka/weather-forecast.jpg"
        )
        line_bot_api.reply_message(event.reply_token, image_message)

    elif re.match("晚安", message): #回傳貼圖
        sticker_message = StickerMessage(
            package_id = "6359",
            sticker_id = "11069871" 
        )    
        line_bot_api.reply_message(event.reply_token, sticker_message)

    elif re.match("笑死",message):
        sticker_message = StickerMessage(
            package_id = "1070",
            sticker_id = "17863"
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)

    if re.match("荳荳", message): #回傳影片
        video_message = VideoSendMessage(
            original_content_url ="https://i.imgur.com/k4bdGpQt.mp4",
            prewiew_image_url = "https://cdn.pixabay.com/photo/2021/10/19/12/28/shiba-6723441_1280.jpg"
        )
        line_bot_api.reply_message(event.reply_token, video_message)

    else: #學你說話
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

    



#主程式
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
