import pandas as pd
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import googletrans 
import datetime
import translate
import time as t
import calendar
import json
import re

now = datetime.datetime.now()
yesterday = datetime.datetime.now() + datetime.timedelta(-1)

translator_a = googletrans.Translator()
#translator_b = translate.Translator(to_lang = "zh-tw")

url = "https://www.bundesregierung.de/breg-de/bundesregierung/staatsministerin-fuer-kultur-und-medien/aktuelles"
raw_html = requests.get(url).text
target_text_re = re.compile(r'BPA.initialSearchResultsJson = (\{.+\]\});')
m = target_text_re.search(raw_html)
json_dict = json.loads(m[1])
title, link, translate = [], [], []
for i in json_dict["result"]["items"]:
    s = i["payload"]
    start = s.find("datetime=") + 10
    end = s.find('Z">\n') - 9
    if s[start:end] == f"{yesterday.year}-{(str(yesterday.month)).zfill(2)}-{(str(yesterday.day-1)).zfill(2)}":
        start = s.find("href=") + 6
        end = s.find("target") - 2
        link.append(s[start:end])
        start = s.find('text-inner">\n') + 13
        end = s.find("\n</span>")
        title.append(s[start:end].replace("<br/>", " "))
        try:
             translate.append(translator_a.translate(s[start:end].replace("<br/>", " "), dest = "zh-tw").text)
        except:
             translate.append(translator_b.translate(s[start:end].replace("<br/>", " ")))
result = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":f"{now.year}/{now.month}/{now.day}", "新聞日期":f"{yesterday.year}/{yesterday.month}/{yesterday.day}", "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"Staatsministerin für Kultur und Medien", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})

#googlenews
translator_a = googletrans.Translator()
#translator_b = translate.Translator(to_lang = "zh-tw")
title, publisher, link, translate = [], [], [], []
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
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":"", "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":publisher, "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)
#聯合國教科文組織(UNESCO)

title, publisher, link, date, translate = [], [], [], [], []

if t.localtime()[1] < 10:
    time = ('0' + str(t.localtime()[1]) + '/' + str(t.localtime()[2]-1) + '/' + str(t.localtime()[0]))
else:
    time = (str(t.localtime()[1]) + '/' + str(t.localtime()[2]-1) + '/' + str(t.localtime()[0]))
url = 'https://en.unesco.org/news'
re = requests.get(url)
soup = BeautifulSoup(re.text, 'html.parser')

for news in soup.findAll('div',{'class' : 'col-lg-4 col-md-4 col-sm-6 col-xs-12'}):
    if news.span.text == time:
        title.append(news.h4.text)
        link.append(news.article.a['href'])
        date.append(news.span.text)
        publisher.append('聯合國教科文組織(UNESCO)')
        try:
            translate.append(translator_a.translate(news.h4.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.h4.text))
        
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":publisher, "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#國際藝術理事會與文化機構聯盟(IFACCA)
title, publisher, link, date, translate, nation = [], [], [], [], [], []
time = (str(int(t.strftime('%d'))-1) + ' ' + t.strftime('%b %Y'))

url = 'https://ifacca.org/en/news/'
re = requests.get(url)
soup = BeautifulSoup(re.text, 'html.parser')

for news in soup.findAll('div',{'class' : 'news-block news-block-item col-xs-6'}):
    if news.find('span' , {'class' : 'date-n-place d-block'}).text.split(', ')[1] == time:
        link.append('https://ifacca.org' + news.a['href'])
        date.append(news.find('span' , {'class' : 'date-n-place d-block'}).text.split(', ')[1])
        nation.append(news.find('span' , {'class' : 'date-n-place d-block'}).text.split(', ')[2])
        publisher.append('國際藝術理事會與文化機構聯盟(IFACCA)' + news.find('span' , {'class' : 'date-n-place d-block'}).text.split(', ')[0])
        
        url2 = ('https://ifacca.org' + news.a['href'])
        re2 = requests.get(url2)
        soup2 = BeautifulSoup(re2.text, 'html.parser')
        title.append(soup2.find('p' , {'class' : 'news-header'}).text)
        try:
            translate.append(translator_a.translate(soup2.find('p' , {'class' : 'news-header'}).text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(nsoup2.find('p' , {'class' : 'news-header'}).text))
        
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":nation, "主題類別":"", "發佈機構/來源":publisher, "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#亞歐基金會(ASEF)
title, publisher, link, date, translate =[], [], [], [], []
time = (str(int(t.strftime('%d'))-1) + ' ' + t.strftime('%b %Y'))

url = 'https://www.asef.org/press/press-releases'
re = requests.get(url)
soup = BeautifulSoup(re.text, 'html.parser')

for news in soup.findAll('li',{'class' : 'doc-link doc-link-pdf'}):
    if news.find('p' , {'class' : 'note'}).text[0:11] == time:
        link.append('https://www.asef.org' + news.a['href'])
        date.append(news.find('p' , {'class' : 'note'}).text[0:11])
        publisher.append('亞歐基金會(ASEF)' + news.p.a.text)
        title.append(news.a.text)
        try:
            translate.append(translator_a.translate(news.a.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.a.text))
        
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":publisher, "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#歐盟國家文化機構(EUNIC)
title, publisher, link, date, translate, topic =[], [], [], [], [], []
if t.localtime()[1] < 10:
    time = ('0' + str(t.localtime()[2]-1) + '.' + str(t.localtime()[1]) + '.' + str(t.localtime()[0]))
    if (t.localtime()[2]-1) < 10:
        time = ('0' + str(t.localtime()[2]-1) + '.' + '0' + str(t.localtime()[1]) + '.' + str(t.localtime()[0]))
elif  t.localtime()[1] >= 10 and (t.localtime()[2]-1) < 10:
    time = (str(t.localtime()[2]-1) + '.' + '0' + str(t.localtime()[1]) + '.' + str(t.localtime()[0]))
else:
    time = (str(t.localtime()[2]-1) + '.' + str(t.localtime()[1]) + '.' + str(t.localtime()[0]))

url = 'https://www.eunicglobal.eu/news'
re = requests.get(url)
soup = BeautifulSoup(re.text, 'html.parser')

for news in soup.findAll('div',{'class' : 'c-card__content'}):
    if news.find('time' , {'class' : 'c-card__date t-gray'}).text == time:
        link.append(news.a['href'])
        date.append(news.find('time' , {'class' : 'c-card__date t-gray'}).text)
        publisher.append('歐盟國家文化機構(EUNIC)')
        topic.append(news.li.text)
        title.append(news.h3.text + " / " + news.p.text)
        title_trans = (news.h3.text + " / " + news.p.text)
        try:
            translate.append(translator_a.translate(title_trans, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(title_trans))
        
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":topic, "發佈機構/來源":publisher, "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#對外文化關係學院(IFA)
title, publisher, link, date, translate =[], [], [], [], []
if t.localtime()[1] < 10:
    time = ('0' + str(t.localtime()[2]-1) + '.' + str(t.localtime()[1]) + '.' + str(t.localtime()[0]))
    if (t.localtime()[2]-1) < 10:
        time = ('0' + str(t.localtime()[2]-1) + '.' + '0' + str(t.localtime()[1]) + '.' + str(t.localtime()[0]))
elif  t.localtime()[1] >= 10 and (t.localtime()[2]-1) < 10:
    time = (str(t.localtime()[2]-1) + '.' + '0' + str(t.localtime()[1]) + '.' + str(t.localtime()[0]))
else:
    time = (str(t.localtime()[2]-1) + '.' + str(t.localtime()[1]) + '.' + str(t.localtime()[0]))

url = 'https://www.ifa.de/en/press/#section1'
re = requests.get(url)
soup = BeautifulSoup(re.text, 'html.parser')

for news in soup.findAll('div',{'class' : 'news__teaser'}):
    if news.find('span', {'class' : 'news__date'}).text[17:27] == time:
        link.append('https://www.ifa.de' + news.a['href'])
        date.append(news.find('span', {'class' : 'news__date'}).text[17:27])
        publisher.append('對外文化關係學院(IFA)')
        title.append(news.a['title'] + " / " + news.p.text)
        title_trans = (news.a['title'] + " / " + news.p.text)
        try:
            translate.append(translator_a.translate(title_trans, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(title_trans))
        
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":publisher, "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#英國數位、文化、媒體暨體育部(Department for Digital, Culture, Media and Sport)
title, publisher, link, date, translate =[], [], [], [], []
time = time = (str(int(t.strftime('%d'))-1) + ' ' + t.strftime('%B %Y'))

url = 'https://www.gov.uk/search/news-and-communications?organisations%5B%5D=department-for-digital-culture-media-sport&parent=department-for-digital-culture-media-sport'
re = requests.get(url)
soup = BeautifulSoup(re.text, 'html.parser')

for news in soup.findAll('li',{'class' : 'gem-c-document-list__item'}):
    if news.time.text == time:
        link.append('https://www.gov.uk' + news.a['href'])
        date.append(news.time.text)
        publisher.append('英國數位、文化、媒體暨體育部(Department for Digital, Culture, Media and Sport)')
        title.append(news.a.text + " / " + news.p.text)
        title_trans = (news.a.text + " / " + news.p.text)
        try:
            translate.append(translator_a.translate(title_trans, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(title_trans))
        
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":publisher, "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#英格蘭藝術理事會(England Arts Council)
title, publisher, link, date, translate =[], [], [], [], []
if (int(t.strftime('%d'))-1) < 10:
    time = ('0' + str(int(t.strftime('%d'))-1) + ' ' + t.strftime('%B %Y'))
else:
    time = (str(int(t.strftime('%d'))-1) + ' ' + t.strftime('%b %Y'))

url = 'https://www.artscouncil.org.uk/news/explore-news'
re = requests.get(url)
soup = BeautifulSoup(re.text, 'html.parser')

news = soup.find('div',{'class' : 'views-row views-row-1 views-row-odd views-row-first'})
if news.find('span',{'class' : 'listing-date'}).text == time:
    link.append('https://www.artscouncil.org.uk' + news.a['href'])
    date.append(news.find('span',{'class' : 'listing-date'}).text)
    publisher.append('英格蘭藝術理事會(England Arts Council)')
    title.append(news.h3.a.text)
    try:
        translate.append(translator_a.translate(news.h3.a.text, dest = "zh-tw").text)
    except:
        translate.append(translator_b.translate(news.h3.a.text))
        
news = soup.find('div',{'class' : 'views-row views-row-2 views-row-even'})
if news.find('span',{'class' : 'listing-date'}).text == time:
    link.append('https://www.artscouncil.org.uk' + news.a['href'])
    date.append(news.find('span',{'class' : 'listing-date'}).text)
    publisher.append('英格蘭藝術理事會(England Arts Council)')
    title.append(news.h3.a.text)
    try:
        translate.append(translator_a.translate(news.h3.a.text, dest = "zh-tw").text)
    except:
        translate.append(translator_b.translate(news.h3.a.text))
        
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":publisher, "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#法國藝文推廣總會(Institut Francais)
title, publisher, link, date, translate, topic =[], [], [], [], [], []
if t.localtime()[1] < 10:
    time = ('0' + str(t.localtime()[2]-1) + '/' + str(t.localtime()[1]) + '/' + str(t.localtime()[0]))
    if (t.localtime()[2]-1) < 10:
        time = ('0' + str(t.localtime()[2]-1) + '/' + '0' + str(t.localtime()[1]) + '/' + str(t.localtime()[0]))
elif  t.localtime()[1] >= 10 and (t.localtime()[2]-1) < 10:
    time = (str(t.localtime()[2]-1) + '/' + '0' + str(t.localtime()[1]) + '/' + str(t.localtime()[0]))
else:
    time = (str(t.localtime()[2]-1) + '/' + str(t.localtime()[1]) + '/' + str(t.localtime()[0]))

url = 'https://www.if.institutfrancais.com/en/actualites-if'
re = requests.get(url)
soup = BeautifulSoup(re.text, 'html.parser')

for news in soup.findAll('article',{'class' : 'node node--type-actualite-if-pro-reseau node--promoted node--view-mode-listing-grande-image'}):
    url1 = news.a['href']
    re1 = requests.get(url1)
    soup1 = BeautifulSoup(re1.text, 'html.parser')
    if soup1.find('div' , {'class' : 'date'}).text[11:] == time:
        link.append(news.a['href'])
        date.append(soup1.find('div' , {'class' : 'date'}).text[11:])
        publisher.append('法國藝文推廣總會(Institut Francais)')
        topic.append(news.find('div' , {'class' : 'field field--name-field-thematiques field--type-entity-reference field--label-hidden field__items'}).text[1:-1])
        title.append(news.a['title'])
        try:
            translate.append(translator_a.translate(news.a['title'], dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.a['title']))
for news in soup.findAll('article',{'class' : 'node node--type-actualite-if-pro-reseau node--promoted node--view-mode-listing-petite-image'}):
    url2 = news.a['href']
    re2 = requests.get(url2)
    soup2 = BeautifulSoup(re2.text, 'html.parser')
    if soup2.find('div' , {'class' : 'date'}).text[11:] == time:
        link.append(news.a['href'])
        date.append(soup2.find('div' , {'class' : 'date'}).text[11:])
        publisher.append('法國藝文推廣總會(Institut Francais)')
        topic.append(news.find('div' , {'class' : 'field field--name-field-thematiques field--type-entity-reference field--label-hidden field__items'}).text[1:-1])
        title.append(news.a['title'])
        try:
            translate.append(translator_a.translate(news.a['title'], dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.a['title']))
        
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":topic, "發佈機構/來源":publisher, "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#美國藝術贊助基金會(National Endowment for Arts)
title, publisher, link, date, translate = [], [], [], [], []
time = (t.strftime('%B') + ' ' + str(int(t.strftime('%d'))-1) + ', ' + t.strftime('%Y'))

url = 'https://www.arts.gov/news/archives'
re = requests.get(url)
soup = BeautifulSoup(re.text, 'html.parser')

news = soup.find('div',{'class' : 'views-row views-row-1 views-row-odd views-row-first'})
if news.find('div',{'class' : 'field field-name-post-date field-type-ds field-label-hidden'}).text == time:
    link.append('https://www.arts.gov/news/archives' + news.a['href'])
    date.append(news.find('div',{'class' : 'field field-name-post-date field-type-ds field-label-hidden'}).text)
    publisher.append('美國藝術贊助基金會(National Endowment for Arts)')
    title.append(news.a.text)
    try:
        translate.append(translator_a.translate(news.a.text, dest = "zh-tw").text)
    except:
        translate.append(translator_b.translate(news.a.text))
        
news = soup.find('div',{'class' : 'views-row views-row-2 views-row-even'})
if news.find('div',{'class' : 'field field-name-post-date field-type-ds field-label-hidden'}).text == time:
    link.append('https://www.arts.gov/news/archives' + news.a['href'])
    date.append(news.find('div',{'class' : 'field field-name-post-date field-type-ds field-label-hidden'}).text)
    publisher.append('美國藝術贊助基金會(National Endowment for Arts)')
    title.append(news.a.text)
    try:
        translate.append(translator_a.translate(news.a.text, dest = "zh-tw").text)
    except:
        translate.append(translator_b.translate(news.a.text))
        
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":publisher, "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#歌德學院(Geothe Institute)
title, publisher, link, date, translate =[], [], [], [], []
if t.localtime()[1] < 10:
    time = ('0' + str(t.localtime()[2]-1) + '.' + str(t.localtime()[1]) + '.' + str(t.localtime()[0]))
    if (t.localtime()[2]-1) < 10:
        time = ('0' + str(t.localtime()[2]-1) + '.' + '0' + str(t.localtime()[1]) + '.' + str(t.localtime()[0]))
elif  t.localtime()[1] >= 10 and (t.localtime()[2]-1) < 10:
    time = (str(t.localtime()[2]-1) + '.' + '0' + str(t.localtime()[1]) + '.' + str(t.localtime()[0]))
else:
    time = (str(t.localtime()[2]-1) + '.' + str(t.localtime()[1]) + '.' + str(t.localtime()[0]))

url = 'https://www.goethe.de/de/uun/prs.html'
re = requests.get(url)
soup = BeautifulSoup(re.text, 'html.parser')

for news in soup.findAll('a', {'target' : '_self'}):
    if news.text[0:10] == time:
        link.append('https://www.goethe.de/' + news['href'][5:])
        date.append(news.text[0:10])
        publisher.append('歌德學院(Geothe Institute)')
        title.append(news.text[12:])
        try:
            translate.append(translator_a.translate(news.text[12:], dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.text[12:]))
        
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":publisher, "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#日本文部科學省
url = "https://www.mext.go.jp/b_menu/houdou/index.htm"
title, link, translate, date = [], [], [], []
response = requests.get(url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "lxml")
now = datetime.datetime.now()
for i in soup.find(class_ = "dateList icon").find_all(class_ = "information-date"):
    if f"{now.month}月{now.day - 1}日" in i.text:
        date.append(f"{now.year}/{now.month}/{now.day - 1}")
        j = i.find_next(class_ = "area_doc")
        title.append(j.a.text)
        link.append("https://www.mext.go.jp" + j.a["href"])
        try:
            translate.append(translator_a.translate(j.a.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(title_ + "/" + subtitle))
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":f"{now.year}/{now.month}/{now.day}", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"日本文部科學省", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#新加坡文化、社會與青年部(The Ministry of Culture, Community and Youth)
url = "https://www.mccy.gov.sg/about-us/news-and-resources"
title, link, translate, date = [], [], [], []
response = requests.get(url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "lxml")
now = datetime.datetime.now()
for i in soup.find_all("strong"):
    month = calendar.month_name[now.month]
    if f"{now.day-1} {month} {now.year}" in i.text:
        date.append(f"{now.year}/{now.month}/{now.day-1}")
        j = i.find_next("h4")
        title.append(j.a.text)
        link.append("https://www.mccy.gov.sg" + j.a["href"])
        try:
            translate.append(translator_a.translate(j.a.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(title_ + "/" + subtitle))
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":f"{now.year}/{now.month}/{now.day}", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"The Ministry of Culture, Community and Youth", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#澳洲藝術理事會(The Australia Council for the Arts)
url = "https://www.australiacouncil.gov.au/news/media-centre/media-releases/"
title, link, translate, date = [], [], [], []
response = requests.get(url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "lxml")
now = datetime.datetime.now()
yesterday = datetime.datetime.now() + datetime.timedelta(-1)
for i in soup.find_all("p", class_ = "date"):
    month = calendar.month_name[yesterday.month]
    if f"{yesterday.day} {month} {yesterday.year}" in i.text:
        date.append(f"{yesterday.year}/{yesterday.month}/{yesterday.day}")
        j = i.find_previous("h3")
        title.append(j.a.text)
        link.append(j.a["href"])
        try:
            translate.append(translator_a.translate(j.a.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(title_ + "/" + subtitle))
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":f"{now.year}/{now.month}/{now.day}", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"The Australia Council for the Arts", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#澳洲藝術部(Ministry for the Arts)
url = "https://www.communications.gov.au/departmental-news"
title, link, translate, date = [], [], [], []
response = requests.get(url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "lxml")
now = datetime.datetime.now()
yesterday = datetime.datetime.now() + datetime.timedelta(-1)
for i in soup.find_all(class_ = "date-display-single"):
    month = calendar.month_name[yesterday.month]
    if f"{yesterday.day} {month} {yesterday.year}" in i.text:
        date.append(f"{yesterday.year}/{yesterday.month}/{yesterday.day}")
        j = i.find_next(class_ = "news-list__title")
        title.append(j.a.text.strip())
        link.append("https://www.communications.gov.au" + j.a["href"])
        try:
            translate.append(translator_a.translate(j.a.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(title_ + "/" + subtitle))
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":f"{now.year}/{now.month}/{now.day}", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"Ministry for the Arts", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#IFPI: Analysis, insights, research and information on trends in the global recorded music market
url = "https://ifpi.org/news/"
title, link, translate, date = [], [], [], []
response = requests.get(url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "lxml")
now = datetime.datetime.now()
yesterday = datetime.datetime.now() + datetime.timedelta(-1)
for i in range(len(soup.find_all(class_ = "date"))):
    if i == 0:
        i = soup.find_all(class_ = "date")[i]
        month = calendar.month_name[yesterday.month]
        if str(yesterday.day) in i.text and month in i.text:
            date.append(f"{yesterday.year}/{yesterday.month}/{yesterday.day}")
            j = i.find_next("h2")
            title.append(j.text)
            k = j.find_next(class_ = "news-hero-link")
            link.append("https://ifpi.org" + k["href"])
            try:
                translate.append(translator_a.translate(j.text, dest = "zh-tw").text)
            except:
                translate.append(translator_b.translate(j.text))
    else:
        i = soup.find_all(class_ = "date")[i]
        month = calendar.month_name[yesterday.month]
        if str(yesterday.day) in i.text and month in i.text:
            date.append(f"{yesterday.year}/{yesterday.month}/{yesterday.day}")
            j = i.find_next("h3")
            title.append(j.text)
            k = j.find_next("a")
            link.append("https://ifpi.org" + k["href"])
            try:
                translate.append(translator_a.translate(j.text, dest = "zh-tw").text)
            except:
                translate.append(translator_b.translate(j.text))
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":f"{now.year}/{now.month}/{now.day}", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"IFPI", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#Culture 360: A platform for arts and cultural communities across Asia and Europe
url = "https://culture360.asef.org/news-events/news/"
title, link, translate, date = [], [], [], []
response = requests.get(url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "lxml")
now = datetime.datetime.now()
yesterday = datetime.datetime.now() + datetime.timedelta(-1)
for i in soup.find_all(class_ = "date"):
    month = calendar.month_name[yesterday.month]
    if f"{yesterday.day} {month} {yesterday.year}" in i.text:
        date.append(f"{yesterday.year}/{yesterday.month}/{yesterday.day}")
        j = i.find_next("a")
        link.append("https://culture360.asef.org" + j["href"])
        k = j.find_next(class_ = "item-title")
        title.append(k.text)
        try:
            translate.append(translator_a.translate(k.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(k.text))
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":f"{now.year}/{now.month}/{now.day}", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"Culture 360", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#The Apro: Information of performance arts
url = "https://www.theapro.kr:441/eng/now/data.asp"
title, link, translate, date = [], [], [], []
data = {
    "page": 1,
    "mode": 10,
    "pagesize": 9,
    "s1": "title",
    "od": 0
}
response = requests.post(url, verify = False, data = data)
soup = BeautifulSoup(response.text, "lxml")
now = datetime.datetime.now()
yesterday = datetime.datetime.now() + datetime.timedelta(-1)
soup = json.loads(soup.text)
for i in soup:
    if i["regdate"] == f"{yesterday.year}-{(str(yesterday.month)).zfill(2)}-{(str(yesterday.day).zfill(2))}":
        title.append(i["title"])
        try:
            translate.append(translator_a.translate(i["title"], dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(i["title"]))
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":f"{now.year}/{now.month}/{now.day}", "新聞日期":f"{yesterday.year}/{yesterday.month}/{yesterday.day}", "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"The Apro", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":"", "備註":""})
result = result.append(result1 , ignore_index=True)

#美國國務院教育文化局 (Bureau of Educational and Cultural Affairs)
url = "https://eca.state.gov/media-center"
title, link, translate = [], [], []
response = requests.get(url)
#response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "lxml")
now = datetime.datetime.now()
yesterday = datetime.datetime.now() + datetime.timedelta(-1)
for i in soup.find_all(typeof = "sioc:Item foaf:Document")[4:]:
    month = calendar.month_name[yesterday.month]
    if f"{month} {yesterday.day}, {yesterday.year}" in i.text:
        title.append(i.text.strip().strip(f"{month} {yesterday.day}, {yesterday.year}")[:-9])
        j = i.find_next("a")
        link.append("https://eca.state.gov" + j["href"])        
        try:
            translate.append(translator_a.translate(i.text.strip().strip(f"{month} {yesterday.day}, {yesterday.year}")[:-9], dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(i.text.strip().strip(f"{month} {yesterday.day}, {yesterday.year}")[:-9]))
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":f"{now.year}/{now.month}/{now.day}", "新聞日期":f"{yesterday.year}/{yesterday.month}/{yesterday.day}", "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"Bureau of Educational and Cultural Affairs", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#英國數位、文化、媒體暨體育部(Department for Digital, Culture, Media and Sport)
url = "https://www.gov.uk/search/all?organisations%5B%5D=department-for-digital-culture-media-sport&order=updated-newest&parent=department-for-digital-culture-media-sport"
title, link, translate = [], [], []
response = requests.get(url)
#response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "lxml")
now = datetime.datetime.now()
yesterday = datetime.datetime.now() + datetime.timedelta(-1)
for i in soup.find_all("time"):
    month = calendar.month_name[yesterday.month]
    if f"{yesterday.day} {month} {yesterday.year}" in i.text:
        j = i.find_previous("a")
        title.append(j.text)
        link.append("https://www.gov.uk" + j["href"])
        try:
            translate.append(translator_a.translate(j.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(j.text))
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":f"{now.year}/{now.month}/{now.day}", "新聞日期":f"{yesterday.year}/{yesterday.month}/{yesterday.day}", "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"Department for Digital, Culture, Media and Sport", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#法國文化部(Ministère de la Culture)
url = "https://www.culture.gouv.fr/Actualites"
title, link, translate = [], [], []
response = requests.get(url)
#response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "lxml")
now = datetime.datetime.now()
yesterday = datetime.datetime.now() + datetime.timedelta(-1)
for i in soup.find_all("time"):
    if f"{(str(yesterday.day)).zfill(2)}.{(str(yesterday.month)).zfill(2)}.{yesterday.year}" in i.text:
        j = i.find_next("a")
        title.append(j.text.strip())
        link.append("https://www.culture.gouv.fr" + j["href"])
        try:
            translate.append(translator_a.translate(j.text.strip(), dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(j.text.strip()))
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":f"{now.year}/{now.month}/{now.day}", "新聞日期":f"{yesterday.year}/{yesterday.month}/{yesterday.day}", "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"Ministère de la Culture", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#西澳地方政府體育與文化產業部門(Department of Local Government, Sport and Cultural Industries, Government of Western Australia)
title, link, date, translate = [], [], [], []
time = (t.strftime('%b') + ' ' + str(int(t.strftime('%d'))-1) + ', ' + t.strftime('%Y'))

url = 'https://www.dlgsc.wa.gov.au/department/news'
re = requests.get(url)
soup = BeautifulSoup(re.text, 'html.parser')

for news in soup.findAll('div',{'class' : 'sf_colsIn sf_4cols_1in_25'}):
    if news.find('span' , {'class' : 'text-muted'}).text[11:22] == time:
        link.append(news.a['href'])
        date.append(news.find('span' , {'class' : 'text-muted'}).text[11:22])
        title.append(news.a.text)
        try:
            translate.append(translator_a.translate(news.a.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.a.text))
for news in soup.findAll('div',{'class' : 'sf_colsIn sf_4cols_2in_25'}):
    if news.find('span' , {'class' : 'text-muted'}).text[11:22] == time:
        link.append(news.a['href'])
        date.append(news.find('span' , {'class' : 'text-muted'}).text[11:22])
        title.append(news.a.text)
        try:
            translate.append(translator_a.translate(news.a.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.a.text))
for news in soup.findAll('div',{'class' : 'sf_colsIn sf_4cols_3in_25'}):
    if news.find('span' , {'class' : 'text-muted'}).text[11:22] == time:
        link.append(news.a['href'])
        date.append(news.find('span' , {'class' : 'text-muted'}).text[11:22])
        title.append(news.a.text)
        try:
            translate.append(translator_a.translate(news.a.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.a.text))
for news in soup.findAll('div',{'class' : 'sf_colsIn sf_4cols_4in_25'}):
    if news.find('span' , {'class' : 'text-muted'}).text[11:22] == time:
        link.append(news.a['href'])
        date.append(news.find('span' , {'class' : 'text-muted'}).text[11:22])
        title.append(news.a.text)
        try:
            translate.append(translator_a.translate(news.a.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.a.text))
for news in soup.findAll('div',{'class' : 'sf_colsIn sf_4cols_5in_25'}):
    if news.find('span' , {'class' : 'text-muted'}).text[11:22] == time:
        link.append(news.a['href'])
        date.append(news.find('span' , {'class' : 'text-muted'}).text[11:22])
        title.append(news.a.text)
        try:
            translate.append(translator_a.translate(news.a.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.a.text))
for news in soup.findAll('div',{'class' : 'sf_colsIn sf_4cols_6in_25'}):
    if news.find('span' , {'class' : 'text-muted'}).text[11:22] == time:
        link.append(news.a['href'])
        date.append(news.find('span' , {'class' : 'text-muted'}).text[11:22])
        title.append(news.a.text)
        try:
            translate.append(translator_a.translate(news.a.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.a.text))
        
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"西澳地方政府體育與文化產業部門(Department of Local Government, Sport and Cultural Industries, Government of Western Australia)", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#印度文化部(Ministry of Culture, Government of India)
title, link, date, translate = [], [], [], []
url = 'http://www.indiaculture.nic.in/press-release'
re = requests.get(url)
soup = BeautifulSoup(re.text, 'html.parser')
time = (t.strftime('%B') + ' ' + str(int(t.strftime('%d'))-1) + ', ' + t.strftime('%Y'))

for news in soup.findAll('div' , {'class' : 'views-row views-row-1 views-row-odd views-row-first'}):
    if news.find('div' , {'class' : 'views-field views-field-created'}).text[8:-1] == time:
        try:
            link.append(news.a['href'])
        except:
            link.append("N/A")
        date.append(news.find('div' , {'class' : 'views-field views-field-created'}).text[8:-1])
        title.append(news.find('span' , {'class' : 'circularsTab'}).text)
        try:
            translate.append(translator_a.translate(news.find('span' , {'class' : 'circularsTab'}).text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.find('span' , {'class' : 'circularsTab'}).text))
for news in soup.findAll('div' , {'class' : 'views-row views-row-2 views-row-even'}):
    if news.find('div' , {'class' : 'views-field views-field-created'}).text[8:-1] == time:
        try:
            link.append(news.a['href'])
        except:
            link.append("N/A")
        date.append(news.find('div' , {'class' : 'views-field views-field-created'}).text[8:-1])
        title.append(news.find('span' , {'class' : 'circularsTab'}).text)
        try:
            translate.append(translator_a.translate(news.find('span' , {'class' : 'circularsTab'}).text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.find('span' , {'class' : 'circularsTab'}).text))
for news in soup.findAll('div' , {'class' : 'views-row views-row-3 views-row-odd'}):
    if news.find('div' , {'class' : 'views-field views-field-created'}).text[8:-1] == time:
        try:
            link.append(news.a['href'])
        except:
            link.append("N/A")
        date.append(news.find('div' , {'class' : 'views-field views-field-created'}).text[8:-1])
        title.append(news.find('span' , {'class' : 'circularsTab'}).text)
        try:
            translate.append(translator_a.translate(news.find('span' , {'class' : 'circularsTab'}).text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.find('span' , {'class' : 'circularsTab'}).text))
for news in soup.findAll('div' , {'class' : 'views-row views-row-4 views-row-even'}):
    if news.find('div' , {'class' : 'views-field views-field-created'}).text[8:-1] == time:
        try:
            link.append(news.a['href'])
        except:
            link.append("N/A")
        date.append(news.find('div' , {'class' : 'views-field views-field-created'}).text[8:-1])
        title.append(news.find('span' , {'class' : 'circularsTab'}).text)
        try:
            translate.append(translator_a.translate(news.find('span' , {'class' : 'circularsTab'}).text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.find('span' , {'class' : 'circularsTab'}).text))
for news in soup.findAll('div' , {'class' : 'views-row views-row-5 views-row-odd'}):
    if news.find('div' , {'class' : 'views-field views-field-created'}).text[8:-1] == time:
        try:
            link.append(news.a['href'])
        except:
            link.append("N/A")
        date.append(news.find('div' , {'class' : 'views-field views-field-created'}).text[8:-1])
        title.append(news.find('span' , {'class' : 'circularsTab'}).text)
        try:
            translate.append(translator_a.translate(news.find('span' , {'class' : 'circularsTab'}).text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.find('span' , {'class' : 'circularsTab'}).text))
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"印度文化部(Ministry of Culture, Government of India)", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#馬來西亞國家文化與藝術局(Jabatan Kebudayaan dan Kesenian Negara)
title, link, date, translate = [], [], [], []
url = 'http://www.jkkn.gov.my/en/press-releases'
re = requests.get(url)
soup = BeautifulSoup(re.text, 'html.parser')
time = (t.strftime('%b') + ' ' + str(int(t.strftime('%d'))-1) + ', ' + t.strftime('%Y'))

for news in soup.findAll('div' , {'class' : 'views-row views-row-1 views-row-odd views-row-first list-rows-item'}):
    if news.find('span' , {'class' : 'date'}).text == time:
        link.append(news.a['href'])
        date.append(news.find('span' , {'class' : 'date'}).text)
        title.append(news.h4.text)
        try:
            translate.append(translator_a.translate(news.h4.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.h4.text))
for news in soup.findAll('div' , {'class' : 'views-row views-row-2 views-row-even list-rows-item'}):
    if news.find('span' , {'class' : 'date'}).text == time:
        link.append(news.a['href'])
        date.append(news.find('span' , {'class' : 'date'}).text)
        title.append(news.h4.text)
        try:
            translate.append(translator_a.translate(news.h4.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.h4.text))
for news in soup.findAll('div' , {'class' : 'views-row views-row-3 views-row-odd list-rows-item'}):
    if news.find('span' , {'class' : 'date'}).text == time:
        link.append(news.a['href'])
        date.append(news.find('span' , {'class' : 'date'}).text)
        title.append(news.h4.text)
        try:
            translate.append(translator_a.translate(news.h4.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.h4.text))
for news in soup.findAll('div' , {'class' : 'views-row views-row-4 views-row-even list-rows-item'}):
    if news.find('span' , {'class' : 'date'}).text == time:
        link.append(news.a['href'])
        date.append(news.find('span' , {'class' : 'date'}).text)
        title.append(news.h4.text)
        try:
            translate.append(translator_a.translate(news.h4.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.h4.text))
for news in soup.findAll('div' , {'class' : 'views-row views-row-5 views-row-odd list-rows-item'}):
    if news.find('span' , {'class' : 'date'}).text == time:
        link.append(news.a['href'])
        date.append(news.find('span' , {'class' : 'date'}).text)
        title.append(news.h4.text)
        try:
            translate.append(translator_a.translate(news.h4.text, dest = "zh-tw").text)
        except:
            translate.append(translator_b.translate(news.h4.text))
            
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"馬來西亞國家文化與藝術局(Jabatan Kebudayaan dan Kesenian Negara)", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#香港特別行政區康樂及文化事務署
title, link, date, translate =[], [], [], []
if t.localtime()[1] < 10:
    time = (str(t.localtime()[0]) + '-' + str(t.localtime()[1]) + '-' + '0' + str(t.localtime()[2]-1))
    if (t.localtime()[2]-1) < 10:
        time = (str(t.localtime()[0]) + '-' + '0' + str(t.localtime()[1]) + '-' + '0' + str(t.localtime()[2]-1))
elif  t.localtime()[1] >= 10 and (t.localtime()[2]-1) < 10:
    time = (str(t.localtime()[0]) + '-' + '0' + str(t.localtime()[1]) + '-' + str(t.localtime()[2]-1))
else:
    time = (str(t.localtime()[0]) + '-' + str(t.localtime()[1]) + '-' + str(t.localtime()[2]-1))

url = 'https://www.lcsd.gov.hk/clpss/tc/webApp/News.do'
re = requests.get(url)
soup = BeautifulSoup(re.text, 'html.parser')
body = soup.tbody
for news in body.findAll('tr'):
    if news.td.text == time:
        link.append(news.a['href'])
        date.append(news.td.text)
        title.append(news.a.text[7:])
        translate.append(news.a.text[7:])
        
result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"香港特別行政區康樂及文化事務署", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

# 日本文化廳
resource_url = 'https://www.bunka.go.jp/whats_new.html'
re = requests.get(resource_url)
re.encoding = 'utf-8'
soup = BeautifulSoup(re.text, 'html.parser')
newslist = soup.find_all('ul', class_='news_list_tag')
yesterday = datetime.datetime.now() + datetime.timedelta(-1)
time = str(yesterday.year) + '年' + str(yesterday.month)+ '月' + str(yesterday.day) + '日'
everylist = newslist[0].find_all('li')

translator = googletrans.Translator()
title, link, translate, date = [], [], [], []
for i in everylist:
    if i.find_all('p', class_='news_list_date')[0].text == time:
        title.append(i.find_all('p', class_='news_list_ttl')[0].text)
        link.append('https://www.bunka.go.jp' + (i.a.get('href')))
        translate.append(translator.translate(i.find_all('p', class_='news_list_ttl')[0].text, src='ja', dest = 'zh-tw').text)
        date.append(i.find_all('p', class_='news_list_date')[0].text)
    else:
        continue

result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"日本文化廳", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

# 日本總務省
resource_url = 'https://www.soumu.go.jp/menu_news/s-news/index.html'
re = requests.get(resource_url)
re.encoding = "SHIFT_JIS"
soup = BeautifulSoup(re.text, 'html.parser')
yesterday = datetime.datetime.now() + datetime.timedelta(-1)
time = str(yesterday.year) + '年' + str(yesterday.month)+ '月' + str(yesterday.day) + '日'
table = soup.table
words = table.find_all('td')

translator = googletrans.Translator()
title, link, translate, date = [], [], [], []
for i in range(0, len(words), 3):
    if words[i].text.strip() == time:
        date.append(words[i].text.strip())
        title.append(words[i+1].text.strip())
        link.append('https://www.soumu.go.jp' + (words[i+1].a.get('href')))
        translate.append(translator.translate(words[i+1].text, src='ja', dest = 'zh-tw').text)
    else:
        continue

result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"日本總務省", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#俄羅斯聯邦文化部
resource_url = 'https://www.mkrf.ru/press/announcement/'
re = requests.get(resource_url)
soup = BeautifulSoup(re.text, 'html.parser')
newslist = soup.find_all('div', class_='b-news-list')[0]
month = ['一','二','三','四','五','六','七','八','九','十','十一','十二']
day = ['一','二','三','四','五','六','七','八','九','十',
       '十一','十二', '十三','十四','十五','十六','十七','十八','十九','二十',
       '二十一','二十二', '二十三','二十四','二十五','二十六','二十七','二十八','二十九','三十','三十一']
yesterday = datetime.datetime.now() + datetime.timedelta(-1)
time1 = str(month[yesterday.month-1])+ '月' + str(day[yesterday.day-1]) + '日'
time2 = str(yesterday.month)+ '月' + str(yesterday.day) + '日'

translator = googletrans.Translator()
title, link, translate, date = [], [], [], []

for i in newslist.find_all('a'):
    if translator.translate(i.find_all('div', class_='b-article__date')[0].text, src='ru', dest = 'zh-tw').text == time1 or translator.translate(i.find_all('div', class_='b-article__date')[0].text, src='ru', dest = 'zh-tw').text == time2:
        title.append(i.find_all('div', class_='b-default__title')[0].text)
        translate.append(translator.translate((i.find_all('div', class_='b-default__title')[0].text), src='ru', dest = 'zh-tw').text)
        link.append('https://www.mkrf.ru' + i.get('href'))
        date.append(translator.translate(i.find_all('div', class_='b-article__date')[0].text, src='ru', dest = 'zh-tw').text)
    else:
        continue

result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"俄羅斯聯邦文化部", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#西班牙文化部
resource_url = 'https://www.culturaydeporte.gob.es/portada.html'
re = requests.get(resource_url)
soup = BeautifulSoup(re.text, 'html.parser')
list = soup.find_all('div', class_='enlace')
time = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%d/%m/%Y')

translator = googletrans.Translator()
title, link, translate, date = [], [], [], []

for i in list:
    if i.find_all('span', class_='fecha')[0].text == time:
        title.append(i.find_all('p', class_='titulo')[0].text.strip())
        date.append(i.find_all('span', class_='fecha')[0].text)
        translate.append(translator.translate(i.find_all('p', class_='titulo')[0].text, src='es', dest = 'zh-tw').text)
        link.append('https://www.culturaydeporte.gob.es' + (i.a.get('href')))
    else:
        continue

result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"西班牙文化部", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#泰國美術部
resource_url = 'https://www.finearts.go.th/main/categorie/general-news'
re = requests.get(resource_url)
soup = BeautifulSoup(re.text, 'html.parser')
month = ['一','二','三','四','五','六','七','八','九','十','十一','十二']
yesterday = datetime.datetime.now() + datetime.timedelta(-1)
time = str(month[yesterday.month-1])+ '月' + (datetime.date.today() - datetime.timedelta(days=1)).strftime('%d')
newslist = soup.find_all('div', class_='card col-md-4 col-sm-12 col-xs-12')

translator = googletrans.Translator()
title, link, translate, date = [], [], [], []

for i in newslist:
    if i.find_all('div', class_='month_') == []:
        continue
    elif str(translator.translate(i.find_all('div', class_='month_')[0].text, dest = 'zh-tw').text) + str(i.find_all('div', class_='day_')[0].text) == time:
        date.append(str(translator.translate(i.find_all('div', class_='month_')[0].text, dest = 'zh-tw').text) + str((i.find_all('div', class_='day_')[0].text)))
        title.append(i.find_all('h5', class_='card-title _limitrow1')[0].text.strip())
        translate.append(translator.translate(i.find_all('h5', class_='card-title _limitrow1')[0].text, dest = 'zh-tw').text)
        link.append('https://www.mkrf.ru' + i.a.get('href'))
    else:
        continue

result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"泰國美術部", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#泰國文化部
resource_url = 'http://www.m-culture.go.th/en/more_news.php?cid=1'
re = requests.get(resource_url)
soup = BeautifulSoup(re.text, 'html.parser')
time = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%d/%m/%Y')
newslist = soup.find_all('div', class_='newsall-work-wrap newsall-comments')

translator = googletrans.Translator()
title, link, translate, date = [], [], [], []

for i in newslist:
    if i.find_all('p', class_='icon-purple')[1].text.strip() == time:
        title.append(i.h4.text.strip())
        translate.append(translator.translate(i.h4.text.strip(), dest = 'zh-tw').text)
        date.append(i.find_all('p', class_='icon-purple')[1].text.strip())
        link.append('http://www.m-culture.go.th/en/' + i.a.get('href'))
    else:
        continue

result1 = pd.DataFrame({"編號":"", "撰寫":"", "搜尋日期":"", "新聞日期":date, "地區別":"", "國家":"", "主題類別":"", "發佈機構/來源":"泰國文化部", "標題翻譯":translate, "標題原文":title, "關鍵字":"", "負責人":"", "連結":link, "備註":""})
result = result.append(result1 , ignore_index=True)

#result.to_csv(f"{now.year}.{now.month}.{now.day - 1}.csv", encoding = "utf_8_sig", index = False)
result
