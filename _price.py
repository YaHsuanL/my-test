import requests
from bs4 import BeautifulSoup

import csv

url = "https://www.easycamp.com.tw/Store_899.html"
headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}
response = requests.get(url,headers=headers)
if response.status_code != 200:
    print(f"請求失敗，status code: {response.status_code}")
    
soup = BeautifulSoup(response.text, "html.parser")
#tables = soup.select("div.col-md-12 col-sm-12 col-xs-12>table")#找div直屬標籤table
#table = soup.select_one("table.table.table-hover")#所有有 class="table和table-hover" 的 <table> 標籤(是一個list)是一個list)
#print(tables)

# for row in tables.select('tr'):#????AttributeError: ResultSet object has no attribute "select". You're probably treating a list of elements like a single element. Did you call find_all() when you meant to call find()?
#     cells = [cell.get_text(strip=True) for cell in row.select('th, td')]
#     print('\t'.join(cells)) 
table = soup.select_one("table.table.table-hover")
thead = [th.text.strip() for th in table.select('thead th')]# 找所有 
#tbody = [[td.text.strip() for td in row.select('td')] for row in table.select('tbody tr')]
rows = []
for tr in table.select('tbody tr'):
    row = [td.text.strip() for td in tr.select('td')]
    rows.append(row)
print("----------------------------------")
print(thead)
print(rows)
# ['區域', '型態', '尺寸', '帳數', '平日', '假日', '連假', '過年', '詳細']

    #cells = [cell.get_text(strip=True) for cell in row.select('th, td')]

# for classify in soup.select('div.classify'):# 找所有 classify 區塊(標題+值) 的<li> 的文字（不管有沒有 <a>）
#     title = classify.select_one('div.title').text.strip() #標題
#     values = [li.text.strip() for li in classify.select('ul.list-inline li')]# 抓出所有 <li> 的文字（不管有沒有 <a>）
#     # 合併文字
#     results[title] = "、".join(values) 








# write_dir = Path("WebCrawler/MultiPagesSaveDemo")
# write_dir.mkdir(exist_ok=True)
#     # 存成CSV檔案
#     df.to_csv(
#         write_dir/"MultiPagesSaveDemo.csv",
#         header=True,
#         index=False
#     )