
import urllib2
import csv
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import sys
from user_agent import generate_user_agent

from random import randint
from time import sleep

reload(sys)
sys.setdefaultencoding('utf8')
filepath=''
with open(filepath+'gamenames.txt', 'rb') as myfile:   
    reader = csv.reader(myfile)
    games = list(reader)

hdr= {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux', 'win'))}

games=games[0][544:]

lines=0
for game in games:
    g=[]
    print(game)
    for i in range(0,2000):
        review_page='http://www.metacritic.com/'+ game + '/user-reviews?page='+str(i)
        print(lines)
        sleep(randint(20,100))
        page = urllib2.Request(review_page, headers=hdr)
        content = urllib2.urlopen(page, timeout=15).read()
        soup = BeautifulSoup(content, 'html.parser')
        right_class=soup.find_all('li', class_="user_review")
        user_data=[]
        if right_class:
            for item in right_class:
                link=item.find('a')
                user = link.get('href')
                if item.find('div', class_="metascore_w"):
                    s= item.find('div', class_="metascore_w").text
                else: s=''
                if item.find("span", class_="blurb"):
                    reviews =item.find("span", class_="blurb")
                else: reviews =item.find("div", class_="review_body")
                r= reviews.text
                if item.find("span", class_="total_ups"):
                    h=item.find("span", class_="total_ups").text
                else: h=''
                if  item.find('span', class_="total_thumbs"):
                    t=item.find('span', class_="total_thumbs").text
                else: t=''
                if item.find("div", class_="date"):
                    dt=item.find("div", class_="date").text
                else: dt = ''
                user_data=[game,user[6:],s, r, h,t, dt] 
                g.append(user_data)
                lines=lines+1
            df = pd.DataFrame(g)
            with open(filepath+'game_review.csv', 'a') as f:
                df.to_csv(f, index=False, quoting=csv.QUOTE_NONNUMERIC, sep="|")
            g=[]
        else: break     