import requests
from bs4 import BeautifulSoup as bs

from datetime import datetime, timedelta

def process_date(doc,date):
    nodes = doc.select('ul.list > li')
    data = list()

    for element_li in nodes:

        # check if is empty element
        if element_li.select_one('a') == None:
            continue

        # get link
        li_link = 'http://news.ltn.com.tw/' + element_li.select_one('a')['href']

        # request for document
        li_res = requests.get(li_link)
        li_doc = bs(li_res.text, 'lxml')

        # get date
        li_date = datetime.strptime(date, "%Y%m%d").strftime('%Y-%m-%d')

        #get title
        li_title = element_li.select_one('p').get_text()

        #get content
        li_content = ""
        for ele in li_doc.select('div.text > p'):
            if not 'appE1121' in ele.get('class', []):
                li_content += ele.get_text()

        # append new row
        data.append({
            'date' : li_date,
            'title': li_title,
            'link' : li_link,
            'content' : li_content,
            'tags' : []
        })
    return data

start_date = "2018-12-25"
stop_date = "2018-12-31"

start = datetime.strptime(start_date, "%Y-%m-%d")
stop = datetime.strptime(stop_date, "%Y-%m-%d")

dates = list()
while start <= stop:
    dates.append(start.strftime('%Y%m%d'))
    start = start + timedelta(days=1)



cnt = 0
all_data = list()
get_data = []

for date in dates:
    print('start crawling :', date)
    res = requests.get('https://news.ltn.com.tw/list/newspaper/politics/' + date)
    doc = bs(res.text, 'lxml')
    get_data.append((doc,date))

for data_touple in get_data:
    all_data += process_date(data_touple[0],data_touple[1])

print(all_data)