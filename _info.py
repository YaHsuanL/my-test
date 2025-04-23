import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

url = "https://www.easycamp.com.tw/Store_899.html"
headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}
response = requests.get(url,headers=headers)
if response.status_code != 200:
    print(f"請求失敗，status code: {response.status_code}")
    
soup = BeautifulSoup(response.text, "html.parser")
#營地名稱地點
location = soup.select_one("h3").text.strip()
h1_tag =  soup.select_one("h1")
name = h1_tag.contents[0].strip()
star_count = len(h1_tag.select("i.fa-star"))
reviews = h1_tag.select_one("h5.icon-font-color").text.strip()
#print(f"{location}\t{name}\t{star_count}\t{reviews}\n")

#營地相關資訊
camp_info = soup.select_one(".camp-info")
address = camp_info.select_one(".inline.block.camp-add").text.strip()
gps = camp_info.select_one(".inline.camp-gps span").text.strip()
phone = camp_info.select_one(".inline.camp-phone").text.strip()

#print(f"{address}\t{gps}\t{phone}\n")

#營地特色說明
h2_tags = soup.find_all('h2',class_='directions')
description = h2_tags[1].text.strip()
print(description)

#<div class="camp-info">
#   <div class="inline block camp-add"> (address)
#           苗栗縣南庄鄉南江村17鄰福南30號
#   <div class="inline camp-gps">
#            <span>24.572306,120.987278</span>  (gps)
#           </div>
#   <div class="inline camp-phone">   (phone)
#            02-2252-7966(露營樂訂位專線)

 # title = article.select_one(".title").text.strip()
    # # print(f"title: {title}")
    # # # # 取出連結
    # # # # 當標題為「本文已被刪除」則<a>為空值
    # a = article.select_one(".title > a")
    # # print(f"a: {a}")
    # link = a["href"] if a else ""
    # author = article.select_one(".author").text.strip()
    # date = article.select_one(".date").text.strip()
    # print(f"{title}\t{link}\n{author}\t{date}")


