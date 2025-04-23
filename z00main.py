import requests
from bs4 import BeautifulSoup
import re
import json
import time

#主頁 ➜ 各分頁(各地區的露營場列表) ➜ 露營場 ➜ 詳細內容

headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}

urlstart = "https://www.easycamp.com.tw"

# 1. 抓出所有縣市的頁面連結



# 2. 抓出一個縣市頁面中所有露營場連結
def get_camp_links(city_url):
    res = requests.get(city_url)
    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.select("h2 a[href^='/Store_']")# 選出以 '/Store_' 開頭的
    #if  else: return[]
    #print("未找到任何營地連結")
    for link in links:
        print(link["href"])
    return [urlstart + link["href"] for link in links]
    

# 3. 擷取個別露營場的詳細資訊（你已經有寫很多函式）

#營地名稱地點 (info.py)
def get_camp_info(soup):
    h1_tag =  soup.select_one("h1")
    name = h1_tag.contents[0].strip()
    star_count = len(h1_tag.select("i.fa-star"))
    reviews = h1_tag.select_one("h5.icon-font-color").text.strip()
    # info = [location, name, star_count, reviews]
    info = {
        "營地名稱": name,
        "獲得星數": star_count,
        "評價": reviews
    }

    return info


#營地相關資訊
def get_address(soup):
    address_tag = soup.select_one(".inline.block.camp-add")
    return address_tag.text.strip() if address_tag else "無地址資訊"

def get_gps(soup):
    gps_tag = soup.select_one(".inline.camp-gps span")
    return gps_tag.text.strip() if gps_tag else "無GPS資訊"

def get_phone(soup):
    phone_tag = soup.select_one(".inline.camp-phone")
    return phone_tag.text.strip() if phone_tag else "無電話資訊"
    


def get_price(soup):#價格表
    table = soup.select_one("table.table.table-hover")
    if table:
        thead = [[th.text.strip() for th in table.select('thead th')] ]
        # rows = []
        for tr in table.select('tbody tr'):
            # row = [td.text.strip() for td in tr.select('td')]
            row = [re.sub(r'[\s\u200B\u200C\u200D\uFEFF]', '', td.text.strip()) for td in tr.select('td')]
            thead.append(row)
        # thead = [th.text.strip() for th in table.select('thead th')] 
        # rows = []
        # for tr in table.select('tbody tr'):
        #     # row = [td.text.strip() for td in tr.select('td')]
        #     row = [re.sub(r'[\s\u200B\u200C\u200D\uFEFF]', '', td.text.strip()) for td in tr.select('td')]
        #     rows.append(row)
        # print(thead)
        # print(rows)

        return thead
        # return thead, rows
    else:
        print("找不到價格表格")
        return []
    


def get_table_content(soup):#營區資訊介紹表格 
    results = {}
    for el in soup.select("div.classify"):
        title = el.select_one('div.title').text.strip() 
        values = [li.text.strip() for li in el.select('li')]
        results[title] = "、".join(values)
    # print(results)
    return results


#說明
def get_campsite_detail(soup):
    h2_tags = soup.find_all('h2',class_='directions')
    detail = h2_tags[1].text.strip()
    return detail



#其中一個網頁(899)主函式
def get_one_place_info(url):
    """獲得單一露營場各項資訊"""
    response = requests.get(url,headers=headers)
    if response.status_code != 200:
        print(f"請求失敗，status code: {response.status_code}")
    soup = BeautifulSoup(response.text, "html.parser")  
    return {
        "營地資訊": get_camp_info(soup),
        "營地地址": get_address(soup),
        "營地gps": get_gps(soup),
        "營地電話": get_phone(soup),
        "營地電話": get_price(soup),
        "營區介紹": get_table_content(soup),
        "營地須知": get_campsite_detail(soup)
    }
    camp={}
    camp["營地資訊"] = get_camp_info(soup)
    camp["營地資訊"].update({
        "地址": get_address(soup),
        "GPS": get_gps(soup),
        "電話": get_phone(soup)
    })
    camp["營區收費"] = get_price(soup)
    camp["營區介紹"] = get_table_content(soup)
    camp["營地須知"] = get_campsite_detail(soup)

def get_one_place_reviews(url):
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    


# ========== 主程式入口 ==========
def main():
    city_url = "https://www.easycamp.com.tw/Camp_0_7_0.html"  # 單一縣市的頁面網址
    camp_urls = get_camp_links(city_url)
    all_camps = []
    for camp_url in camp_urls:
        print(f"處理營地：{camp_url}")
        camp_info = get_one_place_info(camp_url)  # 擷取營地詳細資料
        all_camps.append(camp_info)
        time.sleep(1) 

    print(f"共蒐集 {len(all_camps)} 筆營地資料")
    
    with open("miaoli_camp.json", "w", encoding="utf-8") as f:
        json.dump(all_camps, f, indent=4, ensure_ascii=False)
    
     
  #找出評論的超連結
    review_link = soup.select("li role")




    # _KEY="營區收費"
    # print(f"=============={camp[_KEY][0]}==============")

if __name__ == "__main__":
    main()


