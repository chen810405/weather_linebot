import os
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

    #handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"



#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

#主程式
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
