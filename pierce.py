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
data_dir = Path("rosters")

# a path to a folder called rosters. if it doesnt exist create it 
data_dir.mkdir(exist_ok=True)


# def scrape_detail_page(html):
  #  """Parse the HTML of an inmate detail page"""
   # pass

def scrape_inmate_details():
    data = []
    for roster in data_dir.iterdir():
        # create Path object 
        if roster.is_file():
            html_path = Path(roster)
            with open(html_path, "r", encoding='utf-8', errors='ignore') as file:
                html_content = file.read()
                soup = BeautifulSoup(html_content, 'html.parser')

                bookingID = soup.find('h1')
                if bookingID: 
                    bookingID_text = bookingID.text
                else:
                    bookingID = None
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

                # create a dictionary to store the inmate's details
                inmate_dict = {
                    "bookingID": bookingID_text,
                    "inmate_name": inmate_name,
                    "booking_time": booking_time,
                    "arresting agency": agency
                }
             
                # grab the table with the charges in it and target each charge

                charges = soup.find("table", {"cols": "9"})

                # create a list to hold this inmate's charges

                charge_table = []

                if charges:
                    charge_idx = 1

                    charge_rows = charges.find_all("tr")
                    for row1, row2 in zip(charge_rows[1::3], charge_rows[2::3]):
                        cells1 = row1.find_all("td")

                        # ensure the row has enough <td> cells before grabbing by index
                        # this is necessary because the IndexError: list index out of range
                        # error occurs because table markup is rarely uniform across every row.
                        # some rows in your HTML might be empty, contain header cells, use merged
                        # cells (colspan) or serve as visual spacers with zero <td> elements.
                        if len(cells1) >= 2:
                            charge = cells1[1].get_text(strip=True)
                            charging_agency = cells1[3].get_text(strip=True)
                            jurisdiction = cells1[4].get_text(strip=True)
        
                            # print(f"charge: {charge} | agency: {charging_agency} | jurisdiction: {jurisdiction}")
                        else: 
                            # skips empty rows, header-only rows, or spacer rows
                            continue 
                            
                        cells2 = row2.find_all("td")
                        if len(cells1) >=2:
                            cause = cells2[4]
                            cause_number = cause.get_text(strip=True)
                            case_link = cause.find("a")
                            targetURL = "https://linxonline.co.pierce.wa.us"
                            if case_link:
                                href = case_link.get("href")
                            else:
                                href = None
                            if href:
                                full_url = urljoin(targetURL, case_link["href"])
                                # print(full_url)
                            else: 
                                full_url = None 
                           # print(f"cause_number: {cause_number} | full_url: {full_url}") 
                        else: 
                            # skips empty rows, header-only rows, or spacer rows
                            continue 
                    
                         # dynamically assign keys: charge1, charge2, charge3...
                    
                        inmate_dict[f"charge{charge_idx}_name"] = charge 
                        inmate_dict[f"charge{charge_idx}_agency"] = charging_agency
                        inmate_dict[f"charge{charge_idx}_cause_number"] = cause_number
                        inmate_dict[f"charge{charge_idx}_jurisdiction"] = jurisdiction
                        inmate_dict[f"charge{charge_idx}_full_URL"] = full_url
                        charge_idx +=1

            data.append(inmate_dict)
            df = pd.DataFrame(data)
            df.to_csv('output.csv', index=False)

    print("CSV done!")
    for roster in data_dir.iterdir():
            if roster.is_file():
                roster.unlink()
    print("all files deleted successfully!")
    
                        

   
        # grab booking ID, inmate name, booking date/time, 
        # charges, warrant type, charging agency, 
        # court case number, court date, booking ID, court date,
        # sentence date/bail 

        # put it into a list

        # write that list to a dataframe 

        # export that list to a csv 

        # load that csv into a google sheet

        # have this function run every day 


def scrape_asterisks():
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



if __name__ == "__main__":
    scrape_asterisks()
    scrape_inmate_details()