import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

url = "https://www.easycamp.com.tw/store/purchase_rank/2649"
headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}
response = requests.get(url,headers=headers)    
soup = BeautifulSoup(response.text, "html.parser")



with open("no_reviews.html", "w", encoding="utf-8") as file:
    file.write(soup.prettify())

print("已存成html檔！")