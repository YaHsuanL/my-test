import requests
from bs4 import BeautifulSoup
import re
import json


#response = requests.get(url,headers=headers)
#soup = BeautifulSoup(response.text, "html.parser")

#url = ""
headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}

#住過露友評價網站 :
def get_camp_name(soup):
    """營地基本資訊""" 
    h1_tag =  soup.select_one("h1")
    name = h1_tag.contents[0].strip()
    return name


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
        match = re.search(r'([\d,]+)', text)#抓出第一個包含數字與逗號的片段
        if match:
            number_str = match.group(1).replace(",", "")  # 不論千分位有無逗號都先移除
            return int(number_str)
    return 0

#如果get_review_count=0 就不會有以下 
def get_score(soup):    
    """營地各項得分"""
    scores = []
    score_blocks = soup.select("div.col-md-12.col-sm-12.col-xs-12.evaluation-padding div.text-center")
    if not score_blocks:  # 如果沒有評分區塊，返回五個 None 避免後續出錯
        return [None] * 5 
    for block in score_blocks:
        star_count = len(block.select("i.fa-star"))  # 計算星星數
        scores.append(str(star_count))  # 存成字串方便後續處理
    return scores #[4,5,5,4,4]

#traffic_score, bathroom_score, view_score, service_score, facility_score = get_score(soup)
# camp_scores = {
#     "交通便利度": traffic_score,
#     "衛浴整潔度": bathroom_score,
#     "景觀滿意度": view_score,
#     "服務品質": service_score,
#     "設施完善度": facility_score

#顧客評論內容 如果get_review_count=0 就不會有以下
def get_customer_name(soup): 
    """評論者姓名"""
    costumer_name = soup.select_one("div.col-md-12.col-sm-12.col-xs-12 > h3") 
    return re.sub(r'[\s\u200B\u200C\u200D\uFEFF]+', '', costumer_name.text) if costumer_name else None


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


def get_customer_reviews(block):
    """評論內容""" #評論 <div class="col-md-12 col-sm-12 col-xs-12 font-size-16px con-padding-5px">有兩個，底下分別有 
    title_tag = block.select_one("div.title-font-size.english-break-word")
    content_tag = block.select_one("div.content-font-size.english-break-word")
        
    review_title = title_tag.text.strip()if title_tag else ""
    review_content = content_tag.text.strip()if content_tag else ""

    return review_title,review_content



def get_one_place_reviews(url):
    """獲得單一露營場評分"""
    response = requests.get(url,headers=headers)
    if response.status_code != 200:
        print(f"請求失敗，status code: {response.status_code}")
    soup = BeautifulSoup(response.text, "html.parser")
    
    review_container = soup.select_one("#tab11")
    all_reviews = []
    if review_container: #如果有評論區
        review_blocks = review_container.select("div.row")
        for block in review_blocks:
            name = get_customer_name(block)
            checkin_date, review_date = get_dates(block)
            customer_rating = get_customer_rating(block)
            review_title, review_content = get_customer_reviews(block)
            review_data = {
                "姓名": name,
                "入住日期": checkin_date,
                "評論日期": review_date,
                "評分": customer_rating,
                "評論標題": review_title,
                "評論內容": review_content,    
            }
            all_reviews.append(review_data)
    
    return {
        "營地名稱": get_camp_name(soup),
        "營地總星等": get_overall_stars(soup),
        "評論總數": get_review_count(soup),
        "交通便利度": get_score(soup)[0],
        "衛浴整潔度": get_score(soup)[1],
        "景觀滿意度": get_score(soup)[2],
        "服務品質": get_score(soup)[3],
        "設施完善度":get_score(soup)[4],
        "顧客評論":all_reviews
        }

def save_to_json(data, filename):
    """存入 JSON 檔"""
    with open(filename, "w", encoding="utf-8") as f:
       json.dump(data, f, indent=4, ensure_ascii=False)




url = "https://www.easycamp.com.tw/store/purchase_rank/2649"
review_data = get_one_place_reviews(url)
save_to_json(review_data, "no_reviews.json")


##其他的改掉的
# 將 get_score(soup) 的結果存為 scores 並解包，可以提高程式碼的可讀性
# scores = get_score(soup)
# traffic, bathroom, view, service, facility = scores
       
# return {
#         "營地名稱": get_camp_name(soup),
#         "營地總星等": get_overall_stars(soup),
#         "評論總數": get_review_count(soup),
#         "交通便利度": traffic,
#         "衛浴整潔度": bathroom,
#         "景觀滿意度": view,
#         "服務品質": service,
#         "設施完善度":facility,
#         "顧客評論":all_reviews
#         }
        

###--------------------試印

# stars = get_overall_stars(soup)
# review_count = get_review_count(soup)
# print(f"⭐ 營地總星等：{stars} 顆星")
# print(f"🧾 評論總數：{review_count} 則")





#2. 找出所有評論區塊
# review_container = soup.select_one("#tab11")
# all_reviews = []

# if review_container:
#     review_blocks = review_container.select("div.row")
  
#     for block in review_blocks:
#         #review_soup = BeautifulSoup(str(block), "html.parser")
#         name = get_customer_name(block)
#         checkin_date, review_date = get_dates(block)
#         customer_rating = get_customer_rating(block)
#         review_title, review_content = get_customer_reviews(block)
#         review_data = {
#             "姓名": name,
#             "入住日期": checkin_date,
#             "評論日期": review_date,
#             "評分": customer_rating,
#             "評論標題": review_title,
#             "評論內容": review_content,    
#         }
#         all_reviews.append(review_data)

# # 4. 印出結果
# print(all_reviews)
#print(len(all_reviews))

# for i, r in enumerate(all_reviews, 1):
#     print(f"{i}. 姓名: {r['name']}, 入住: {r['checkin_date']}, 評價: {r['review_date']}")


#評論分頁



