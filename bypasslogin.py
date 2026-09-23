import requests

session = requests.Session()

session.cookies.set("session_id", "FBEFB90C-9769-1EC0-A9D75D27FD840E91")

response = session.get("https://linxonline.co.pierce.wa.us/linxweb/Booking/GetJailRoster.cfm")

print(response.text)