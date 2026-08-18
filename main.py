from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

import time

URL_FORMAT = "https://jobs.mo.gov/warn/{}"

# this tells python something is going into the curly brackets later

data = []

# in the context of this browser being open, we're going to use chromium 
# running a browser in headless mode means having it run in the background
# headless=False means it's actually going to launch a browser in the computer 
# we are running in here.
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

# remember in a range, the top number is exclusive
    for year in range (2019, 2027):
        page.goto(
            URL_FORMAT.format(year)
        ) 
# each year in the range goes into the (year) blank
        time.sleep(1) 

        html = page.inner_html("table")
        table = BeautifulSoup(html, "html.parser")
        rows = table.find_all("tr")
        for row in rows:
            cells = [x.text.strip() for x in row.find_all('td')]
            data.append(cells) 
    browser.close()

df = pd.DataFrame(data)


# in command-line: uv run main.py to run the script
# a package called playwright stealth does a little more complex stuff
# if it's a dot gov website, fair game for scraping (usually)



# does the page that I am interested in scraping from, iss it accessible from the 
# public internet 
# are the booking IDs unique? 
# Try to stay as little time on this brittle server 
# as possible. You can download the HTML and then work from there. That way 
# if they take something down you have a copy.



from urllib
URL = "jail roster link"

def scrape_detail_page(html):
    """Parse the html of an inmate detail page"""
    pass

with sync_playwright() as p:
    browser = p. chromium.launch(headless=False)
    page = browser.new_page()

    


