from playwright.sync_api import sync_playwright, expect
from bs4 import BeautifulSoup
import pandas as pd
import requests

from urllib.parse import urljoin
import time
from datetime import datetime
from pathlib import Path 
import os

# landing page for the jail roster
URL = "https://linxonline.co.pierce.wa.us/linxweb/Booking/GetJailRoster.cfm"
data_dir = Path("rosters1")

# a path to a folder called rosters1. if it doesn't exist create it 
data_dir.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(URL)
    expect(page.get_by_text("Booked Less Than 72 Hours Ago")).to_be_visible()
    html = page.inner_html("body")
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find_all("table")[-1]

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        booked_24hrs = cells[0].text
        if "*" in booked_24hrs:
            name = cells[1].text
            booking_id = cells[2]
            detail_url = urljoin(
            URL,
            booking_id.find("a").get("href")
             )
            booking_id = booking_id.text.strip()
            location = cells[3].text
            release_date = cells[4].text.strip()
            if release_date:
                release_date = datetime.strptime(
                    cells[4].text, "%m/%d/%Y %I:%M %p"
                ).isoformat()
        # https://linxonline.co.pierce.wa.us/linxweb/Booking/GetBooking.cfm?booking_id=2026209028
            print(name, booking_id, detail_url, location, release_date)
            filepath = data_dir / f"{booking_id}.html"
            if not filepath.exists():
                page.goto(detail_url)

                time.sleep(2)

            # w means opening the file in write mode. 
            with open(filepath,"w") as out_file: 
                out_file.write(page.inner_html("body"))
            print(f"downloaded {filepath}")
            time.sleep(3)
            page.go_back()

    browser.close()
