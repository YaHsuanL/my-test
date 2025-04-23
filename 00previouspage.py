import requests
from bs4 import BeautifulSoup

url = "https://www.easycamp.com.tw/Camp_0_7_0.html"
headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}
response = requests.get(url,headers=headers)
    
soup = BeautifulSoup(response.text, "html.parser")

links = soup.select("h2 a[href]")
for link in links:
        print(link["href"])#取得20個網址

