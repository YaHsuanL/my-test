import requests
from bs4 import BeautifulSoup


url = "https://www.easycamp.com.tw/Store_899.html"
headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}
response = requests.get(url,headers=headers)
if response.status_code != 200:
    print(f"請求失敗，status code: {response.status_code}")
    
soup = BeautifulSoup(response.text, "html.parser")



with open("get899.html", "w", encoding="utf-8") as file:
    file.write(soup.prettify())

print("已存成html檔！")



# for el2 in second_level:
#     third_level = el2.select("li")# ["<><><><><>", "<><><>"]  只拿表格內文
#     for el3 in third_level:
#         content = el3.text



#去掉html標籤


    
    
    
    
    # # print(f"article:\n{article}")
    # # # 把標籤去除，取出標題
    # title = article.select_one(".title").text.strip()
    # # print(f"title: {title}")
    # # # # 取出連結
    # # # # 當標題為「本文已被刪除」則<a>為空值
    # a = article.select_one(".title > a")
    # # print(f"a: {a}")
    # link = a["href"] if a else ""
    # # 取出作者
    # author = article.select_one(".author").text.strip()
    # # 取出日期
    # date = article.select_one(".date").text.strip()
    # print(f"{title}\t{link}\n{author}\t{date}")
    # #print("----------------------------------")

