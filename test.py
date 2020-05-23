from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from translate import Translator
translator = Translator(to_lang="zh-tw")
url = "https://news.google.com/search?q=coronavirus%20museum%20when%3A1d&hl=en-US&gl=US&ceid=US%3Aen"
driver = webdriver.Chrome()
driver.get(url)
js = "var action=document.documentElement.scrollTop=10000"
driver.execute_script(js)
response = requests.get(url)
title, publisher, url, translate = [], [], [], []
soup = BeautifulSoup(response.text, "lxml")
for i in soup.find_all("h3", class_ = "ipQwMb ekueJc gEATFF RD0gLb"):
    title_ = i.text
    sub = i.find_next("span", class_ = "xBbh9")
    subtitle = sub.text
    title.append(title_ + "/" + subtitle)
    translate.append(translator.translate(title_ + "/" + subtitle))
    url.append("https://news.google.com" + i.a["href"][1:])
    i = i.find_next(class_ = "wEwyrc AVN2gc uQIVzc Sksgp")
    publisher.append(i.text)
result = pd.DataFrame({"Title": title, "標題": translate, "Publisher": publisher, "Link": url})
# link = []
# for i in result["Link"]:
#     driver.get(i)
#     link.append(driver.current_url)
# result["Link"] = link
# def make_clickable(val):
#     # target _blank to open new window
#     return '<a target="_blank" href="{}">{}</a>'.format(val, val)
# result.style.format({'Link': make_clickable})
result.to_csv("output.csv", encoding = "utf_8_sig", index = False)
