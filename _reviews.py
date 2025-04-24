import requests
from bs4 import BeautifulSoup
import re
import json


#response = requests.get(url,headers=headers)
#soup = BeautifulSoup(response.text, "html.parser")



#住過露友評價網站 :
def get_overall_stars(soup):
    """營地獲得星數"""
    all_stars = soup.select_one("a.icon-star-position.assessment_scroll")#回傳一個tag物件
    # given_stars = len(all_stars.select("i.fa-star"))#得到幾個星星
    # return given_stars
    if all_stars:
        given_stars = len(all_stars.select("i.fa-star"))
        return given_stars
    return 0

#評價       <h5 class="icon-font-color">
def get_review_count(soup):
    """獲得評論數"""
    review_count = soup.select_one("h5.icon-font-color")
    if review_count:
        text = review_count.text.strip()
        #print(text)
        match = re.search(r'([\d,]+)', text)#抓出第一個包含數字與逗號的片段
        if match:
            number_str = match.group(1).replace(",", "")  # 不論千分位有無逗號都先移除
            return int(number_str)
    return 0

def get_score(soup):    #如果get_review_count=0 就不會有以下 
    """營地各項得分(未寫完)"""
    div = soup.select("div.col-md-9 col-sm-9 col-xs-9 text-center") 
    traffic_score = div[2].text.strip()
    bathroom_score = div[3].text.strip()
    view_score = div[4].text.strip()
    service_score = div[5].text.strip()
    facility_score = div[6].text.strip()


#顧客評論內容 如果get_review_count=0 就不會有以下
def get_customer_name(soup): #名子後有很多/t 林*男\t\t\t\t\t\t\t\t\t\t\t先生'
    """評論者姓名"""
    costumer_name = soup.select_one("div.col-md-12.col-sm-12.col-xs-12 > h3") #找出多個顧客名字
    return costumer_name .text.strip() if costumer_name else None
    #return [name.text.strip() for name in costumer_names] 不行這樣

def get_dates(soup):
    """入住日期&評論日期"""
    all_divs = soup.select("div.col-md-12.col-sm-12.col-xs-12.font-size-16px")
    checkin_date = None
    review_date = None
    for div in all_divs:
        text = div.text.strip()
        date_match = re.search(r"\d{4}/\d{2}/\d{2}", text)  # 找 YYYY/MM/DD 格式
        if "入住" in text and date_match:
            checkin_date = date_match.group()
        elif "評價" in text and date_match:
            review_date = date_match.group()
    return checkin_date, review_date


def get_customer_rating(soup):
    """評論者給予的星數""" #<div class="col-md-3 col-sm-3 col-xs-3 icon-star-padding">
    rating_div= soup.select_one("div.col-md-3.col-sm-3.col-xs-3.icon-star-padding")
    customer_rating = len(rating_div.select("i.fa-star"))
    return customer_rating


def get_customer_reviews(soup):
    """評論內容(有些只有標題，有些有內文)""" #評論 <div class="col-md-12 col-sm-12 col-xs-12 font-size-16px con-padding-5px">有兩個，底下分別有
    review_text_blocks = soup.select("div.col-md-12.col-sm-12.col-xs-12.font-size-16px.con-padding-5px")
    for text_block in review_text_blocks:
        review_title = text_block.select_one("div.title-font-size.english-break-word").text.strip()
        review_body = text_block.select_one("div.content-font-size.english-break-word").text.strip()
        if review_body:
            return review_title,review_body



 
 #評論標題	review_title(未寫)
 # 評論內容	review_content (未寫)




###--------------------試印
url = "https://www.easycamp.com.tw/store/purchase_rank/2356/3"
headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}
response = requests.get(url,headers=headers)
if response.status_code != 200:
    print(f"請求失敗，status code: {response.status_code}")
soup = BeautifulSoup(response.text, "html.parser")

stars = get_overall_stars(soup)  # soup 是整個頁面的 soup
review_count = get_review_count(soup)

print(f"⭐ 營地總星等：{stars} 顆星")
print(f"🧾 評論總數：{review_count} 則")
#2. 找出所有評論區塊
review_container = soup.select_one("#tab11")
all_reviews = []

if review_container:
    review_blocks = review_container.select("div.row")
  
    for block in review_blocks:#對每則評論建立獨立 soup 並提取資訊
        #review_soup = BeautifulSoup(str(block), "html.parser")
        name = get_customer_name(block)
        checkin_date, review_date = get_dates(block)
        customer_rating = get_customer_rating(block)
        #評論標題	review_title(未寫)
        # 評論內容	review_content (未寫)
        if name and (checkin_date or review_date):
            review_data = {
                "姓名": name,
                "入住日期": checkin_date,
                "評論日期": review_date,
                "給幾顆星": customer_rating,
                "評論標題": ,
                "評論內容":     
            }
            all_reviews.append(review_data)

# # 4. 印出結果
print("----------------------")
print(all_reviews)
# print()
# for i, r in enumerate(all_reviews, 1):
#     print(f"{i}. 姓名: {r['name']}, 入住: {r['checkin_date']}, 評價: {r['review_date']}")
# else:
#     print("找不到評論區塊")


#with open("reviews.json", "w", encoding="utf-8") as f:
#        json.dump(all_reviews, f, indent=4, ensure_ascii=False)

    #return {get_overall_stars(soup),get_score(soup),get_review_count(soup),get_dates(soup),get_review_content(soup)}

