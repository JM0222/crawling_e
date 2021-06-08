import requests, json, time
import schedule
from bs4 import BeautifulSoup

def toJson(dict_data):
    with open('article_data.json', 'w', encoding='utf-8') as file :
        json.dump(dict_data, file, ensure_ascii=False, indent='\t')
def article_crawling():
    url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EB%84%B7%ED%94%8C%EB%A6%AD%EC%8A%A4"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    res = requests.get(url, headers= headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    article = {}
    idx = 1
    news = soup.find_all("div", attrs={"class":"news_wrap api_ani_send"})
    for i in news:
        media = i.find("a", attrs={"class":"info press"}).get_text()
        media_ = ''
        for j in media:
            if j == "언":
                break
            else:
                media_ += j
        time = i.find("span", attrs={"class":"info"}).get_text()
        title = i.find("div", attrs={"class":"news_area"}).find("a",attrs={"class":"news_tit"}).get_text(strip=True)
        link = i.find("div", attrs={"class":"news_area"}).find("a",attrs={"class":"news_tit"})['href']
        article[str(idx)] = {"media":media_, "time":time, "title":title, "link":link }
        idx += 1
    print('crawling execution')
    toJson(article)
schedule.every(1).minutes.do(article_crawling)
# schedule.every(30).minutes.do(article_crawling) #30분마다 실행
# schedule.every().monday.at("00:10").do(article_crawling) #월요일 00:10분에 실행
# schedule.every().day.at("10:30").do(article_crawling) #매일 10시30분에 
while True:
    schedule.run_pending()
    time.sleep(1) # 1초 대기