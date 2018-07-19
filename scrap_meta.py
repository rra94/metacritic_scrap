import urllib2
import csv
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
from user_agent import generate_user_agent


metacritic_base = "http://www.metacritic.com/browse/games/release-date/available/pc/metascore?view=detailed&page="
hdr= {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux', 'win'))}

filepath=''

for i in range(0,54):
    game= []
    print(i)
    metacritic = metacritic_base+str(i)
    page = urllib2.Request(metacritic, headers=hdr )
    content = urllib2.urlopen(page).read()
    soup = BeautifulSoup(content, 'html.parser')
    right_class=soup.find_all('div', class_='product_wrap')
    for item in right_class:
        #print(item)
        try: 
            link=item.find('h3', class_="product_title").find("a")
            g=link.get('href')
        except: g=''
        try:
            score = item.find("span", class_="metascore_w")
            s=score.text
        except: s =''
        try:
            dt = item.find("li", class_="release_date").find("span", class_="data")
            d=dt.text
        except: dt=''
        try: 
            rating=item.find("li",class_="stat maturity_rating").find("span", class_="data")
            r= rating.text
        except: r=""
        try:
            pub =item.find("li",class_="stat publisher").find("span", class_="data")
            p= pub.text
        except: p=''
        try: 
            genre= item.find("li",class_="stat genre").find("span", class_="data")
            gr = genre.text
        except: gr=''
        try: 
            user_score=item.find("span", class_="textscore")
            u = user_score.text
        except: u=''
        game=[g,s,d,r,p,gr.strip(),u]
        df = pd.DataFrame([game])
        with open(filepath+'gamenames.csv', 'a') as f:
            df.to_csv(f, header=False, index=False, quoting=csv.QUOTE_NONNUMERIC, sep="|")
        game= []
