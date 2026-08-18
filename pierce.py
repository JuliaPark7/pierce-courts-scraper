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

# a path to a folder called rosters. if it doesnt exist create it 
data_dir.mkdir(exist_ok=True)


# def scrape_detail_page(html):
  #  """Parse the HTML of an inmate detail page"""
   # pass

"""

def scrape_charges(charges)

    # NOW, grab the table with the charges in it 
    charges = soup.find_all("table", {"cols": "9"})
    if charges is None:
        print(f"Warning: no charges found in file")
        continue
    charges_rows = charges.find_all("tr")
        for charge_row in charges_rows:
        charge_cells = charge_row.find_all("td")
        charge_name = charge_cells[1].text
        print(charge_name)

"""


def scrape_inmate_details():
    data = []
    for roster in data_dir.iterdir():
        # create Path object 
        if roster.is_file():
            html_path = Path(roster)
            with open(html_path, "r", encoding='utf-8', errors='ignore') as file:
                html_content = file.read()
                soup = BeautifulSoup(html_content, 'html.parser')
                bookingID = soup.find('h1').text
                # print(bookingID)

                # grab the table with the inmate's details in it 
                details = soup.find("table", {"width": "730"})
                # grab the column with the inmate's name
                # if it doesn't exist for some reason, add an if statement
                if details is None:
                    print(f"Warning: no details found in file")
                    continue

                # grab the row with the inmate's name and target the name 
                inmate = details.find("td", {"width":"330"})
                inmate_name = inmate.text

                # grab the row with the booking date/time and target the date/time
                booking_row = details.find_all("tr")[1]
                booking_data = booking_row.find_all('td')
                booking_time = booking_data[1].text

                # grab the row with the arresting agency and target the agency
                agency_row = details.find_all("tr")[6]
                agency_data = agency_row.find_all("td")
                agency = agency_data[1].text
                # print(inmate_name, booking_time, agency)


                # grab the table with the charges in it and target each charge

                charges = soup.find("table", {"cols": "9"})
                if charges is None:
                    print(f"Warning: no charges found in file")
                    continue

                # grab the row with the charges in it 
                # need to grab more charges 
                charge_rows = charges.find_all("tr")[1::2]
                for charge_row in charge_rows:
                    charge = charge_row.find_all("td")
                    print(charge)
                    
                    # print(charge_data)

                jurisdiction_row = charges.find_all("tr")[2]
                jurisdiction_data = jurisdiction_row.find_all("td")
                cause_number = jurisdiction_data[4].text
                link_html = jurisdiction_data[4]
                case_link = link_html.find("a")
                targetURL = "https://linxonline.co.pierce.wa.us"
                         #  print(case_link)
               
                if case_link is not None:
                    href = case_link.get("href")
                else:
                    href = None
           
                if href:
                    full_url = urljoin(targetURL, case_link["href"])
                    # print(full_url)
                else: 
                    full_url = None

                scraped_details = {
                    "bookingID": bookingID,
                    "inmate_name": inmate_name,
                    "booking_time": booking_time,
                    "agency": agency,
                    # "charge": charge,
                    "cause_number": cause_number,
                    "full_url": full_url
                      }
                    
                data.append(scraped_details)
                df = pd.DataFrame(data)
                df.to_csv('output.csv', index=False)
    print("CSV done!")

                # turn that info into a DataFrame      

"""" 
                    if len(charge_data) > 0:
                        charge = charge_data[1].text
                        print(charge)
                    else:
                        charge = "No text found"
                        
"""
                    # charge = charge_data[1].text
                    # print(f"Charge {index}: {charge}")

"""
                charge_rows = charges.find_all("tr")[1]
                charge_data = charge_row.find_all("td")
                charge = charge_data[1].text
                """

                # grab the row with the jurisdiction in it 
              

if __name__ == "__main__":
    scrape_inmate_details()

        
                  
        # grab booking ID, inmate name, booking date/time, 
        # charges, warrant type, charging agency, 
        # court case number, court date, booking ID, court date,
        # sentence date/bail 

        # put it into a list

        # write that list to a dataframe 

        # export that list to a csv 

        # load that csv into a google sheet

        # have this function run every day 


#def scrape_detail_page(html)

""" 
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(URL)
    expect(page.get_by_text("Booked Less Than 24 Hours Ago")).to_be_visible()
    html = page.inner_html("body")
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find_all("table")[-1]

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
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

"""