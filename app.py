from email.mime import image
import os
import re
import requests
import json
import urllib
from bs4 import BeautifulSoup
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

#設定一個全台的縣市list供比對
cities =["基隆市","新北市","臺北市","桃園市","新竹市","新竹縣","苗栗縣","臺中市","彰化縣","南投縣","雲林縣","嘉義市","嘉義縣","臺南市","高雄市","屏東縣","臺東縣","花蓮縣","宜蘭縣","澎湖縣","連江縣","金門縣"]

# city = input("輸入縣市")
def get_report(city): #得到xx縣市的未來36小時預報
    token="CWB-AE73C77F-25C6-4EDC-89C4-C86EC865B7C4"
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization="+ token +"&format=JSON&locationName=" + city
    response = requests.get(url) #拿到未來36小時的天氣資料
    data = (json.loads(response.text)) #轉換成json格式
    report = data["records"]["location"][0]["weatherElement"]
    all_weather_report=[] #36小時的天氣(每12小時放在一個dict再串成list)
    for info in range(3):
        weather_report={
            "city:":city,
            "Time_from:":(report[0]["time"][info]["startTime"]+"至"),
            "Time_to:":(report[0]["time"][info]["endTime"]), #預測時間
            "Weather_type:":(report[0]["time"][info]["parameter"]["parameterName"]), #天氣型態
            "MinT:":(report[2]["time"][info]["parameter"]['parameterName']+"度"), #最低溫
            "MaxT:":(report[4]["time"][info]["parameter"]["parameterName"]+"度"), #最高溫
            "Rain:":(report[1]["time"][info]["parameter"]["parameterName"]+"%"), #降雨機率
            "CI:":(report[3]["time"][info]["parameter"]["parameterName"]) #舒適度:CI

        }
        all_weather_report.append(weather_report) #串起來
    print(len(all_weather_report))
    print(all_weather_report)
    
    #打開flexmessage模板
    template_weather_report = json.load(
        open("template_weather_report.json",'r',encoding="utf-8"))
    
    #把抓取到的預報資料帶入flexmessage格式裡面
    for info2 in range(len(all_weather_report)):
        template_weather_report["contents"][info2]["body"]["contents"][0]["text"] = all_weather_report[info2]["city:"]#city
        template_weather_report["contents"][info2]["body"]["contents"][3]["contents"][1]["text"] = all_weather_report[info2]["Time_from:"]
        template_weather_report["contents"][info2]["body"]["contents"][4]["contents"][0]["text"] = all_weather_report[info2]["Time_to:"]
        template_weather_report["contents"][info2]["body"]["contents"][6]["contents"][1]["text"] = all_weather_report[info2]["Weather_type:"]
        template_weather_report["contents"][info2]["body"]["contents"][7]["contents"][1]["text"] = all_weather_report[info2]["MinT:"]
        template_weather_report["contents"][info2]["body"]["contents"][8]["contents"][1]["text"] = all_weather_report[info2]["MaxT:"]
        template_weather_report["contents"][info2]["body"]["contents"][9]["contents"][1]["text"] = all_weather_report[info2]["Rain:"]
        template_weather_report["contents"][info2]["body"]["contents"][10]["contents"][1]["text"] = all_weather_report[info2]["CI:"]

#     print("\n\n",template_weather_report)
    return template_weather_report

    
#利用api抓取雷達回測圖
def get_radar_picture():
    #打開api
    url = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-A0058-001?Authorization=CWB-AE73C77F-25C6-4EDC-89C4-C86EC865B7C4&downloadType=WEB&format=JSON"
    response = requests.get(url) 
    radar = (json.loads(response.text)) #轉換成json格式
    #打開flexmessage模板
    template_pic = json.load(open("template_pic.json",'r',encoding="utf-8"))
    template_pic["contents"][0]["body"]["contents"][0]["url"] = radar["cwbopendata"]["dataset"]["resource"]["uri"]

    #找到雷達回波圖的連結
    res = requests.get("https://www.cwb.gov.tw/V8/C/") #到氣象局網站
    soup = BeautifulSoup(res.text ,"lxml")
    links = soup.find_all("div",class_="tab-default vision_2")[0].find_all("div",class_="col-xs-6 col-md-3 px-5p")
    template_pic["contents"][0]["body"]["contents"][1]["contents"][0]["contents"][1]["contents"][1]["action"]["uri"] = ["https://www.cwb.gov.tw"+ links[1].a.get("href")]

    # pic["contents"][0]["body"]["contents"][2]["contents"][0]["text"] = datetime.date.today() #顯示天氣圖的時間
    print(template_pic["contents"][0]["body"]["contents"][0]["url"])
    print(template_pic["contents"][0]["body"]["contents"][1]["contents"][0]["contents"][1]["contents"][1]["action"]["uri"])
    
    return template_pic

    
    
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

    elif re.match("預測", message): #回傳圖片
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
    
#輸入"天氣縣市名">>查詢縣市天氣
    elif message[:2] == "天氣": #ex:使用者輸入"天氣台北市"
        city = message[2:] #縣市名稱
        city = city.replace("台","臺")#臺取代台
        if not (city in cities): #如果縣市清單裡找不到使用者輸入的縣市名
            line_bot_api.reply_message(event.reply_token, TextSendMessage("查詢格式錯誤!!\n請輸入正確格式:天氣縣市名,\n如:天氣臺北市"))
        else:
#             get_report(city) #開始取得天氣資料 
            #套入flex message格式
            template_weather_report = get_report(city)
            line_bot_api.reply_message(
                event.reply_token,FlexSendMessage(city + "未來36小時天氣預報",template_weather_report))
    
#回傳天氣圖
    elif message[:2] == "雷達":
        template_pic = get_radar_picture()
        
        
        line_bot_api.reply_message(
                event.reply_token,FlexSendMessage("雷達回波圖",template_pic))
    
    
    else: #學你說話
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

    



#主程式
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
