import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep

options = webdriver.ChromeOptions()

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


data = []

for page in range(1,17):
    if page == 1:
        url = "https://www.footballtransfers.com/us/transfers/confirmed/most-recent/2024-2025/uk-premier-league"
    else :
        url = f"https://www.footballtransfers.com/us/transfers/confirmed/most-recent/2024-2025/uk-premier-league/{page}"
    
    driver.get(url)
    sleep(1)
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', {'class': 'table table-striped table-hover leaguetable mvp-table transfer-table mb-0'})
    #tr: lay thong tin tung cau thu 1

    rows = table.tbody.find_all('tr')

    for row in rows:
        #lay tung cot cua cau thu
        cols = row.find_all('td')
        if not cols:
            continue

        player = {'Name': 'N/a', 'Old_team' : 'N/a', 'New_team' : 'N/a', 'Price':'N/a'}

        name_span = cols[0].find('span', class_ = 'd-none') 
        if name_span:
            player['Name'] = name_span.text.strip()
            
        old_team_div = cols[1].find('div', class_ = 'transfer-club transfer-club--from')
        if old_team_div:
            old_team_name = old_team_div.find('div', class_ = 'transfer-club__name')
            player['Old_team'] = old_team_name.text.strip() if old_team_name else 'N/a'

        new_team_div = cols[1].find('div', class_ = 'transfer-club transfer-club--to')
        if new_team_div:
            new_team_name = new_team_div.find('div', class_ = 'transfer-club__name')
            player['New_team'] = new_team_name.text.strip() if new_team_name else 'N/a'
        
        price_pan = cols[3].find('span')
        if price_pan:
            price_text = price_pan.text.strip()

            if("Free" in price_text):
                player["Price"] = price_text
            else:
                player['Price'] = price_text.replace('€', '').replace('$','').strip()
        else:
            player['Price'] = 'N/a'
        
        data.append(player)
        
df= pd.DataFrame(data)
print(df)
df.to_csv("bang2.csv")
print("DONE")
         

        