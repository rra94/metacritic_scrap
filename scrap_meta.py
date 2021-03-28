
import urllib.request as rqs
import csv
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import random

def sleep(func):
    def wrapper():
        sleeprandomtime = random.randrange(5, 15)
        print(f"Scrapper is going to sleep {sleeprandomtime} seconds.")
        time.sleep(sleeprandomtime)
        return func()
    return wrapper

@sleep
def SleepWakeUp():
    print("Scrapper woke up and continue the process.")

metacritic_base = "http://www.metacritic.com/browse/games/release-date/available/pc/metascore?view=detailed&page="
hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'User-Agent': "Magic Browser"}
# filepath="/Users/Zoli/Downloads/"
filepath = "data/"

# Creating timestamp for output plot filename
now = datetime.now()
current_time_abbrev = now.strftime("%Y%m%d-%H%M%S-%f")

# Export filename
filename_export = filepath + "gamenames-" + current_time_abbrev + ".csv"

# Written lines counter
written_lines = 0

for i in range(0, 64):

    if i % 10 == 0 and i > 0:
        SleepWakeUp()

    metacritic = metacritic_base + str(i)
    page = rqs.Request(metacritic, headers=hdr)
    content = rqs.urlopen(page).read()

    soup = BeautifulSoup(content, "html.parser")
    right_class = soup.find_all("tr")

    print(f"Scrapper read {len(right_class)} TR elements from the site page {i}.")

    counter = 0

    for item in right_class:

        try:
            spacer = item.find("div")
            if spacer == None:
                continue
        except:
            spacer = ""

        counter += 1

        try:
            rank = item.find("span", class_="title numbered")
            ra = rank.text
        except:
            ra = ""

        try:
            link = item.find("td", class_="clamp-image-wrap").find("a")
            g = "https://www.metacritic.com" + link.get("href")
        except:
            g = ""

        try:
            link = item.find("td", class_="clamp-image-wrap").find("img")
            n = link.get("alt")
        except:
            n = ""

        try:
            score = item.find("div", class_="metascore_w large game positive")
            s = score.text
        except:
            try:
                score = item.find("div", class_="metascore_w large game mixed")
                s = score.text
            except:
                try:
                    score = item.find("div", class_="metascore_w large game negative")
                    s = score.text
                except:
                    s = ""

        try:
            dt = item.find("span", class_="")
            d = dt.text
        except:
            d = ""

        try:
            platform = item.find("span", class_="data")
            gr = platform.text
        except:
            gr = ""

        try:
            user_score = item.find("div", class_="metascore_w user large game positive")
            u = user_score.text
        except:
            try:
                user_score = item.find("div", class_="metascore_w user large game mixed")
                u = user_score.text
            except:
                try:
                    user_score = item.find("div", class_="metascore_w user large game tbd")
                    u = user_score.text
                except:
                    try:
                        user_score = item.find("div", class_="metascore_w user large game negative")
                        u = user_score.text
                    except:
                        u = ""

        game = [ra.strip(), n, g, s, u, d, gr.strip()]
        df = pd.DataFrame([game])

        with open(filename_export, "a") as f:
            df.to_csv(f, header=False, index=False, quoting=csv.QUOTE_NONNUMERIC, sep=",")
            written_lines += 1

    print(f"Scrapper used {counter} lines from the site page {i}.")

print(f"Scrapper wrote out {written_lines} line in {filename_export} file.")