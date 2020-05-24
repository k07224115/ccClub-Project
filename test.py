import pandas as pd
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import googletrans 
import datetime
import translate 
translator_a = googletrans.Translator()
translator_b = translate.Translator(to_lang = "zh-tw")
driver = webdriver.Chrome()
url1 = "https://news.google.com/search?q=coronavirus%20museum%20when%3A1d&hl=en-US&gl=US&ceid=US%3Aen"
url2 = "https://news.google.com/search?q=coronavirus%20art%20when%3A1d&hl=en-US&gl=US&ceid=US%3Aen"
url3 = "https://news.google.com/search?q=Coronavirus%20art%20industry%20when%3A1d&hl=en-US&gl=US&ceid=US%3Aen"
url4 = "https://news.google.com/search?q=Coronavirus%20cinema%20when%3A1d&hl=en-US&gl=US&ceid=US%3Aen"
url = [url1, url2, url3, url4]
title, publisher, link, translate = [], [], [], []
for i in url:
    driver.get(i)
    js = "var action=document.documentElement.scrollTop=10000"
    driver.execute_script(js)
    response = requests.get(i)
    soup = BeautifulSoup(response.text, "lxml")
    for j in soup.find_all("h3", class_ = "ipQwMb ekueJc gEATFF RD0gLb"):
        title_ = j.text
        if title_ not in title:
            sub = j.find_next("span", class_ = "xBbh9")
            subtitle = sub.text
            title.append(title_ + "/" + subtitle)
            try:
                translate.append(translator_a.translate(title_ + "/" + subtitle, dest = "zh-tw").text)
            except:
                translate.append(translator_b.translate(title_ + "/" + subtitle))
            link.append("https://news.google.com" + j.a["href"][1:])
            j = j.find_next(class_ = "wEwyrc AVN2gc uQIVzc Sksgp")
            publisher.append(j.text)
result = pd.DataFrame({"Title": title, "標題": translate, "Publisher": publisher, "Link": link})
now = datetime.datetime.now()
result.to_csv(f"{now.year}.{now.month}.{now.day - 1}.csv", encoding = "utf_8_sig", index = False)


# make clickable and shorten the url
# link = []
# for i in result["Link"]:
#     driver.get(i)
#     link.append(driver.current_url)
# result["Link"] = link
# def make_clickable(val):
#     return '<a target="_blank" href="{}">{}</a>'.format(val, val)
# result.style.format({'Link': make_clickable})
