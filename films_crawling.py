import requests
from bs4 import BeautifulSoup as BS
import csv
import json

import requests
import csv
import json
from bs4 import BeautifulSoup

def toJson(dict_data):
    with open('films_data.json', 'w', encoding='utf-8') as file :
        json.dump(dict_data, file, ensure_ascii=False, indent='\t')

temp_dict = {}
for i in range(1,5):
    url = "https://m.kinolights.com/title/"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    try: 
        res = requests.get(url + str(i), headers = headers)
        res.raise_for_status() # 문제시 종료
        soup = BeautifulSoup(res.text, "lxml")
        idx = i
        title_kr = soup.find("div", attrs = {"class":"movie-title-wrap"}).find("h3").get_text()
        title_en = soup.find("div", attrs = {"class":"movie-title-wrap"}).find("h4").get_text()
        genre = soup.find("div", attrs = {"class":"movie-title-wrap"}).find("span").get_text()
        genre_ = ''
        for i in genre:
            if i == " ":
                break
            else:
                genre_ += i
        release = soup.find("div", attrs = {"class":"movie-title-wrap"}).find("span").next_sibling.get_text()
        img_url = soup.find(
            "div", attrs={"class": "modal-container"}).find("img")["src"]
        ott = soup.find_all("li", attrs = {"class":"movie-price-item"})
        otts = []
        for item in ott:
            k = item.find("span", attrs = {"class":"cell provider-name"}).get_text()
            otts.append(k)

        person = soup.find_all("div", attrs = {"class":"person"})
        director = []
        actor = []
        for item in person:
            if item.find("div",attrs={"class":"character"}).get_text() == "감독":
                director.append(item.find("div",attrs={"class":"name"}).get_text())
            else:
                actor.append(item.find("div",attrs={"class":"name"}).get_text())
        synopsis = soup.find("p", attrs={"class":"synopsis"}).get_text(strip=True)
        temp_dict[str(idx)] = {"title_kr":title_kr, "title_en":title_en, "genre":genre_,
                                "release":release, "img":img_url, "ott":otts, "director":director,
                                 "actor":actor, "synopsis":synopsis}        
    except requests.exceptions.HTTPError:
        print("예외발생")
        continue
    except AttributeError:
        print("null값")
toJson(temp_dict)