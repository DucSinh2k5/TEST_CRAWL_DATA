
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import sqlite3



options = webdriver.ChromeOptions()

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

CauThu = [
    'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born',
    'MP', 'Starts','Min','90s',
    'Gls','Ast','G+A', 'G-PK','PK', 'PKatt', 'CrdY', 'CrdR', 
    'xG', 'npxG', 'xAG', 'npxG+xAG',
    'PrgC', 'PrgP', 'PrgR',
    'Gls/90', 'Ast/90', 'G+A/90', 'G-PK/90','G+A-PK/90',
    'xG/90', 'xAG/90','xG+xAG/90','npxG/90','npxG+xAG/90'
]

# conn = sqlite3.connect("premier_league.db")
# cursor = conn.cursor()
# columns_sql = ", ".join([f"'{col}' TEXT" for col in CauThu])
# cursor.execute(f"CREATE TABLE IF NOT EXISTS CauThu ({columns_sql})")

# conn.commit()
#sleep : cho trang tai len
driver.get("https://fbref.com/en/comps/9/2024-2025/stats/2024-2025-Premier-League-Stats")
sleep(1)
#lay html va dung BeautifulSoup 

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

table = soup.find('table', {'id': 'stats_standard'})
data = []

rows = table.tbody.find_all('tr')

for row in rows:
    cols = row.find_all('td')
    if not cols:
        continue
    cauthu = {col: 'N/a' for col in CauThu}

    cauthu['Player'] = cols[0].text.strip() if cols[0].text.strip() else 'N/a'
    cauthu['Nation'] = cols[1].text.strip() if cols[1].text.strip() else 'N/a'
    cauthu['Pos'] = cols[2].text.strip() if cols[2].text.strip() else 'N/a'
    cauthu['Squad'] = cols[3].text.strip() if cols[3].text.strip() else 'N/a'
    cauthu['Age'] = cols[4].text.strip() if cols[4].text.strip() else 'N/a'
    cauthu['Born'] = cols[5].text.strip() if cols[5].text.strip() else 'N/a'
    cauthu['MP'] = cols[6].text.strip() if cols[6].text.strip() else 'N/a'
    cauthu['Starts'] = cols[7].text.strip() if cols[7].text.strip() else 'N/a'
    cauthu['Min'] = cols[8].text.strip() if cols[8].text.strip() else 'N/a'
    cauthu['90s'] = cols[9].text.strip() if cols[9].text.strip() else 'N/a'
    cauthu['Gls'] = cols[10].text.strip() if cols[10].text.strip() else 'N/a'
    cauthu['Ast'] = cols[11].text.strip() if cols[11].text.strip() else 'N/a'
    cauthu['G+A'] = cols[12].text.strip() if cols[12].text.strip() else 'N/a'
    cauthu['G-PK'] = cols[13].text.strip() if cols[13].text.strip() else 'N/a'
    cauthu['PK'] = cols[14].text.strip() if cols[14].text.strip() else 'N/a'
    cauthu['PKatt'] = cols[15].text.strip() if cols[15].text.strip() else 'N/a'
    cauthu['CrdY'] = cols[16].text.strip() if cols[16].text.strip() else 'N/a'
    cauthu['CrdR'] = cols[17].text.strip() if cols[17].text.strip() else 'N/a'
    cauthu['xG'] = cols[18].text.strip() if cols[18].text.strip() else 'N/a'
    cauthu['npxG'] = cols[19].text.strip() if cols[19].text.strip() else 'N/a'
    cauthu['xAG'] = cols[20].text.strip() if cols[20].text.strip() else 'N/a'
    cauthu['npxG+xAG'] = cols[21].text.strip() if cols[21].text.strip() else 'N/a'
    cauthu['PrgC'] = cols[22].text.strip() if cols[22].text.strip() else 'N/a'
    cauthu['PrgP'] = cols[23].text.strip() if cols[23].text.strip() else 'N/a'
    cauthu['PrgR'] = cols[24].text.strip() if cols[24].text.strip() else 'N/a'
    cauthu['Gls/90'] = cols[25].text.strip() if cols[25].text.strip() else 'N/a'
    cauthu['Ast/90'] = cols[26].text.strip() if cols[26].text.strip() else 'N/a'
    cauthu['G+A/90'] = cols[27].text.strip() if cols[27].text.strip() else 'N/a'
    cauthu['G-PK/90'] = cols[28].text.strip() if cols[28].text.strip() else 'N/a'
    cauthu['G+A-PK/90'] = cols[29].text.strip() if cols[29].text.strip() else 'N/a'
    cauthu['xG/90'] = cols[30].text.strip() if cols[30].text.strip() else 'N/a'
    cauthu['xAG/90'] = cols[31].text.strip() if cols[31].text.strip() else 'N/a'
    cauthu['xG+xAG/90'] = cols[32].text.strip() if cols[32].text.strip() else 'N/a'
    cauthu['npxG/90'] = cols[33].text.strip() if cols[33].text.strip() else 'N/a'
    cauthu['npxG+xAG/90'] = cols[34].text.strip() if cols[34].text.strip() else 'N/a'

    
    minutes_value = cauthu['Min'].replace(',','')
    if(minutes_value != 'N/a' and int(minutes_value) > 90):
        data.append(cauthu)




# for cauthu in data:
    
#     values = [cauthu.get(col, "N/a") for col in CauThu]
    
#     placeholders = ", ".join(["?"] * len(CauThu))
#     cursor.execute(f"INSERT INTO CauThu VALUES ({placeholders})", values)

# conn.commit()
# conn.close()
# print("DONE: Đã lưu vào SQLite")

df = pd.DataFrame(data, columns=CauThu)
df.to_csv("BANG_CAU_THU_NGOAI_HANG_ANH_CO_SO_PHUT_THI_DAU_HON_90_PHUT")
print("DONE")