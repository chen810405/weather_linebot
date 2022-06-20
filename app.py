import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options #防止彈出警告
import webbrowser 

chrome_options = Options()
chrome_options.add_argument("--headless") # 啟動 Headless 無頭模式
chrome_options.add_argument("--disable-gpu") # 關閉 GPU 避免某些系統或是網頁出錯
browser = webdriver.Chrome('C:\\Users\\yiyin\\Desktop\\chromedriver.exe' , chrome_options=chrome_options)

def get_picture():
    res = requests.get("https://www.cwb.gov.tw/V8/C/") #到氣象局網站
    soup = BeautifulSoup(res.text)
    # print(soup)
    #找到衛星雲圖的連結
    weather_link = {}
    links = soup.find_all("div",class_="tab-default vision_2")[0].find_all("div",class_="col-xs-6 col-md-3 px-5p")
    weather_link["satellite"] = ["https://www.cwb.gov.tw"+ links[0].a.get("href")]
    weather_link["radar"] = ["https://www.cwb.gov.tw"+ links[1].a.get("href")]
    weather_link["rain"] = ["https://www.cwb.gov.tw"+ links[2].a.get("href")]
    weather_link["UVI"] = ["https://www.cwb.gov.tw"+ links[3].a.get("href")]
    weather_link["lightning"] = ["https://www.cwb.gov.tw"+ links[4].a.get("href")]
    weather_link["temperature"] = ["https://www.cwb.gov.tw"+ links[5].a.get("href")]
    weather_link["healthweather"] = [links[6].a.get("href") , "https://www.cwb.gov.tw"+ links[6].img.get("src")]

    # print(weather_link)

    #用selenium抓取網頁連結及天氣圖連結
    browser.get("https://www.cwb.gov.tw/V8/C/")
    #衛星雲圖
    browser.find_element_by_xpath("/html/body/main/section[1]/div[1]/div/div/div[2]/div/div[1]/a").click()
    soup_next_page = BeautifulSoup(browser.page_source, 'html.parser')
    satellite = ("https://www.cwb.gov.tw"+soup_next_page.find_all("div",id="link-1")[0].img.get("src"))
    weather_link["satellite"].append(satellite)
    # print(satellite)
    # print(weather_link)
    browser.back()

    #雷達迴波圖
    browser.find_element_by_xpath("/html/body/main/section[1]/div[1]/div/div/div[2]/div/div[2]/a").click()
    soup_next_page = BeautifulSoup(browser.page_source, 'html.parser')
    radar = ("https://www.cwb.gov.tw"+soup_next_page.find_all("div",id="link-1")[0].img.get("src"))
    weather_link["radar"].append(radar)
    # print(radar)
    # print(weather_link)
    browser.back()

    #雨量
    browser.find_element_by_xpath("/html/body/main/section[1]/div[1]/div/div/div[2]/div/div[3]/a").click()
    soup_next_page = BeautifulSoup(browser.page_source, 'html.parser')
    rainfall = ("https://www.cwb.gov.tw"+soup_next_page.find_all("div",id="link-1")[0].img.get("src"))
    weather_link["rain"].append(rainfall)
    # print(rainfall)
    browser.back()

    #紫外線
    browser.find_element_by_xpath("/html/body/main/section[1]/div[1]/div/div/div[2]/div/div[4]/a").click()
    soup_next_page = BeautifulSoup(browser.page_source, 'html.parser')
    UVI = ("https://www.cwb.gov.tw"+soup_next_page.find_all("div",id="tab-1")[0].img.get("src"))
    weather_link["UVI"].append(UVI)
    # print(UVI)
    browser.back()

    #即時閃電
    browser.find_element_by_xpath("/html/body/main/section[1]/div[1]/div/div/div[2]/div/div[5]/a").click()
    soup_next_page = BeautifulSoup(browser.page_source, 'html.parser')
    lightning = ("https://www.cwb.gov.tw"+soup_next_page.find_all("div",class_="zoomHolder")[0].img.get("src"))
    weather_link["lightning"].append(lightning)
    # print(lightning)
    browser.back()

    #溫度
    browser.find_element_by_xpath("/html/body/main/section[1]/div[1]/div/div/div[2]/div/div[6]/a").click()
    soup_next_page = BeautifulSoup(browser.page_source, 'html.parser')
    temperature = ("https://www.cwb.gov.tw"+soup_next_page.find_all("div",id="link-1")[0].img.get("src"))
    weather_link["temperature"].append(temperature)
    # print(temperature)
    browser.back()


    print(weather_link)
    return weather_link
#datetime.today()
