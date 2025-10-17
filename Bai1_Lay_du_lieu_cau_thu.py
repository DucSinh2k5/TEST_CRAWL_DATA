
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

# for x in CauThu:
#     print(x)
conn = sqlite3.connect("premier_league.db")
cursor = conn.cursor()
columns_sql = ", ".join([f"'{col}' TEXT" for col in CauThu])
cursor.execute(f"CREATE TABLE IF NOT EXISTS CauThu ({columns_sql})")

conn.commit()
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
    c=0
    for x in ((CauThu)):
        cauthu[x] = cols[c].text.strip() if cols[c].text.strip() else 'N/a'
        c+=1
    minutes_value = cauthu['Min'].replace(',','')
    if(minutes_value != 'N/a' and int(minutes_value) > 90):
        data.append(cauthu)

for cauthu in data:
    
    values = [cauthu.get(col, "N/a") for col in CauThu]
    
    placeholders = ", ".join(["?"] * len(CauThu))
    cursor.execute(f"INSERT INTO CauThu VALUES ({placeholders})", values)

conn.commit()
conn.close()
print("DONE: Đã lưu vào SQLite")
#luu vao file csv
# df = pd.DataFrame(data, columns=CauThu)
# df.to_csv("BANG_CAU_THU_NGOAI_HANG_ANH_CO_SO_PHUT_THI_DAU_HON_90_PHUT")
# print("DONE")