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

results = {}
for el in soup.select("div.classify"):# 找所有 classify 區塊(標題+值) 
    title = el.select_one('div.title').text.strip() 
    values = [li.text.strip() for li in el.select('li')]
    results[title] = "、".join(values)

print(results)

#更改前:
bigtable = soup.select_one("div.no_line.margin-top-20")
classify = bigtable.select("div.classify")#[><><><><>", "<><><>"] 
results = {}
for el in classify:# 找所有 classify 區塊(標題+值) 
    title = el.select_one('div.title').text.strip() #標題
    values = [li.text.strip() for li in el.select('li')]# 抓出所有 <li> 的文字（不管有沒有 <a>）
    # 合併文字
    results[title] = "、".join(values)

    


# for el2 in second_level:
#     third_level = el2.select("li")# ["<><><><><>", "<><><>"]  只拿表格內文
#     for el3 in third_level:
#         content = el3.text

#存成html檔


#去掉html標籤

