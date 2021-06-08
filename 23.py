import requests
import csv
import json
from bs4 import BeautifulSoup

# def toJson(mnet_dict):
#     with open('mnet_chart.json', 'w', encoding='utf-8') as file :
#         json.dump(mnet_dict, file, ensure_ascii=False, indent='\t')


filename = "filmsdata.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)
header = ["idx","title_kr","title_en","genre","release","ott","director","actor","synopsis"]

writer.writerow(header)

for i in range(2,3):
    url = "https://m.kinolights.com/title/"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    try: 
        res = requests.get(url + str(i), headers = headers)
        res.raise_for_status() # 문제시 종료
        soup = BeautifulSoup(res.text, "lxml")
        rows = []
        idx = i
        rows.append(i)
        title_kr = soup.find("div", attrs = {"class":"movie-title-wrap"}).find("h3").get_text()
        rows.append(title_kr)

        title_en = soup.find("div", attrs = {"class":"movie-title-wrap"}).find("h4").get_text()
        rows.append(title_en)
        genre = soup.find("div", attrs = {"class":"movie-title-wrap"}).find("span").get_text()
        genre_ = ''
        for i in genre:
            if i == " ":
                break
            else:
                genre_ += i
        rows.append(genre_)
        release = soup.find("div", attrs = {"class":"movie-title-wrap"}).find("span").next_sibling.get_text()
        rows.append(release)
        # img_url = soup.find("div", attrs = {"class":"poster"}).find("img")
        # img_url2 = soup.find("div", attrs = {"class":"poster"}).find("img")["src"]
        # print(img_url2)
        imgUrl = soup.find_all("img")
        # print(imgUrl)
        ott = soup.find_all("li", attrs = {"class":"movie-price-item"})
        otts = []
        
        for item in ott:
            k = item.find("span", attrs = {"class":"cell provider-name"}).get_text()
            otts.append(k)
        rows.append(otts)
        person = soup.find_all("div", attrs = {"class":"person"})
        director = []
        actor = []
        for item in person:
            if item.find("div",attrs={"class":"character"}).get_text() == "감독":
                director.append(item.find("div",attrs={"class":"name"}).get_text())
            else:
                actor.append(item.find("div",attrs={"class":"name"}).get_text())
            # a = item.find("div",attrs={"class":"name"}).get_text()
            # b = item.find("div",attrs={"class":"character"}).get_text()
            # c = a + ':' + b
            # director.append(c)
        # print(director,actor)
        rows.append(director)
        rows.append(actor)
        synopsis = soup.find("p", attrs={"class":"synopsis"}).get_text()
        rows.append(synopsis)
        # print(title_kr, title_en, genre_, otts, data, synopsis)

        writer.writerow(rows)
    except requests.exceptions.HTTPError:
        print("예외발생")
        continue
import csv
import json
 
 
# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath):
     
    # create a dictionary
    data = {}
     
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
             
            # Assuming a column named 'No' to
            # be the primary key
            key = rows['No']
            data[key] = rows
 
    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
         
# Driver Code
 
# Decide the two file paths according to your
# computer system
csvFilePath = r'Names.csv'
jsonFilePath = r'Names.json'
 
# Call the make_json function
make_json(csvFilePath, jsonFilePath)