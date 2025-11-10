import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep

# setup chrome
options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

data = []


for page in range(1, 23):
    if page == 1:
        url = "https://www.footballtransfers.com/us/values/players/most-valuable-soccer-players/playing-in-uk-premier-league"
    else:
        url = f"https://www.footballtransfers.com/us/values/players/most-valuable-soccer-players/playing-in-uk-premier-league/{page}"


    driver.get(url)
    sleep(1)


    soup = BeautifulSoup(driver.page_source, "html.parser")
    rows = soup.select("tbody#player-table-body tr")


    for r in rows:
        name = r.select_one("td.td-player span.d-none")
        age = r.select_one("td.m-hide.age")
        team = r.select_one("td.td-team a[title]")
        price = r.select_one("span.player-tag")

        data.append({
            "Name": name.text.strip() if name else "N/a",
            "Age": age.text.strip() if age else "N/a",
            "Team": team["title"].strip() if team and team.has_attr("title") else "N/a",
            "Price": price.text.strip() if price else "N/a"
        })



driver.quit()


df = pd.DataFrame(data)
df.to_csv("bang3.csv", index=False, encoding="utf-8-sig")
print("DONE ✅")
