import pandas as pd
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from bs4 import BeautifulSoup 
from time import sleep
import undetected_chromedriver as uc
# Danh sách tất cả các cột thuộc tính
players = [
    'Name', 'Nation', 'Team', 'Position', 'Age',
    'Matches', 'Starts', 'Minutes',
    'non_penalty_goals', 'penalty_goals', 'assists', 'yellow_cards',
    'red_cards',
    'xG', 'npxG', 'xAG',
    'PrgC', 'PrgP', 'PrgR',
    'per90_Gls', 'per90_Ast', 'per90_G+A', 'per90_G-PK',
    'per90_G+A-PK', 'per90_xG', 'per90_xAG', 'per90_xG+xAG',
    'per90_npxG', 'per90_npxG+xAG',
    'GA', 'GA90', 'SoTA', 'Saves',
    'Save%', 'W', 'D', 'L', 'CS', 'CS%',
    'PKatt', 'PKA', 'PKSV', 'PKm', 'GK_Save%',
    'Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'FK', 'PK', 'PKatt',
    'xG_Shooting', 'npxG_Shooting', 'npxG/Sh', 'G-xG', 'np:G-xG',
    'Pass_Cmp', 'Pass_Att', 'Pass_Cmp%', 'TotDist', 'PrgDist',
    'Short_Cmp', 'Short_Att', 'Short_Cmp%', 'Medium_Cmp',
    'Medium_Att', 'Medium_Cmp%', 'Long_Cmp', 'Long_Att',
    'Long_Cmp%', 'Ast', 'xAG', 'xA', 'A-xAG', 'KP', '1/3', 'PPA',
    'CrsPA', 'PrgP', 'Pass_Live', 'Pass_Dead', 'Pass_FK',
    'Pass_TB', 'Pass_Sw', 'Pass_Crs', 'Pass_TI', 'Pass_CK',
    'Corner_In', 'Corner_Out', 'Corner_Str',
    'Pass_Cmp_Outcome', 'Pass_Off', 'Pass_Blocks',
    'SCA', 'SCA90', 'SCA_type_PassLive', 'SCA_type_PassDead', 'SCA_type_TO', 'SCA_type_Sh', 'SCA_type_Fld', 'SCA_type_Def',
    'GCA', 'GCA90', 'GCA_type_PassLive', 'GCA_type_PassDead', 'GCA_type_TO', 'GCA_type_Sh', 'GCA_type_Fld', 'GCA_type_Def',
    'Tkl', 'TklW', 'Def_3rd', 'Mid_3rd', 'Att_3rd',
    'Challenges_Tkl', 'Challenges_Att', 'Challenges_Tkl%', 'Challenges_Lost',
    'Blocks', 'Blocks_Sh', 'Blocks_Pass', 'Blocks_Int', 'Blocks_Tkl+Int', 'Blocks_Clr', 'Blocks_Err',
    'Touches', 'Def_Pen', 'Def_3rd', 'Mid_3rd', 'Att_3rd',
]

# === Cấu hình UC Chrome (hiện trình duyệt thật, không headless) ===
options = uc.ChromeOptions()
# Xóa các chế độ ẩn danh / headless
options.headless = False  
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")

# Khởi tạo UC Chrome
driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats")
sleep(30)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
table = soup.find('table', {'id': 'stats_standard'})
data = []

rows = table.tbody.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    if not cols:
        continue
    
    player = {col: "N/A" for col in players}
    
    player['Name'] = cols[0].text.strip() if cols[0].text.strip() else "N/A"
    player['Nation'] = cols[1].text.strip() if cols[1].text.strip() else "N/A"
    player['Position'] = cols[2].text.strip() if cols[2].text.strip() else "N/A"
    player['Team'] = cols[3].text.strip() if cols[3].text.strip() else "N/A"
    player['Age'] = cols[4].text.strip() if cols[4].text.strip() else "N/A"
    player['Matches'] = cols[5].text.strip() if cols[5].text.strip() else "N/A"
    player['Starts'] = cols[6].text.strip() if cols[6].text.strip() else "N/A"
    player['Minutes'] = cols[8].text.strip() if cols[8].text.strip() else "N/A"
    player['assists'] = cols[11].text.strip() if cols[11].text.strip() else "N/A"
    player['non_penalty_goals'] = cols[13].text.strip() if cols[13].text.strip() else "N/A"
    player['penalty_goals'] = cols[14].text.strip() if cols[14].text.strip() else "N/A"
    player['yellow_cards'] = cols[16].text.strip() if cols[16].text.strip() else "N/A"
    player['red_cards'] = cols[17].text.strip() if cols[17].text.strip() else "N/A"
    player['xG'] = cols[18].text.strip() if cols[18].text.strip() else "N/A"
    player['npxG'] = cols[19].text.strip() if cols[19].text.strip() else "N/A"
    player['xAG'] = cols[20].text.strip() if cols[20].text.strip() else "N/A"
    player['PrgC'] = cols[22].text.strip() if cols[22].text.strip() else "N/A"
    player['PrgP'] = cols[23].text.strip() if cols[23].text.strip() else "N/A"
    player['PrgR'] = cols[24].text.strip() if cols[24].text.strip() else "N/A"
    player['per90_Gls'] = cols[25].text.strip() if cols[25].text.strip() else "N/A"
    player['per90_Ast'] = cols[26].text.strip() if cols[26].text.strip() else "N/A"
    player['per90_G+A'] = cols[27].text.strip() if cols[27].text.strip() else "N/A"
    player['per90_G-PK'] = cols[28].text.strip() if cols[28].text.strip() else "N/A"
    player['per90_G+A-PK'] = cols[29].text.strip() if cols[29].text.strip() else "N/A"
    
    minutes_value = player['Minutes'].replace(',', '')
    if minutes_value != "N/A" and int(minutes_value) > 90:
        data.append(player)

# === PHẦN 4: CÀO DỮ LIỆU GOALKEEPING STATS ===
# reuse the existing driver and page source; do not create a second driver instance
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
table_gk = soup.find('table', {'id': 'stats_keeper'})
new_GK_data = []

# guard against missing or commented-out table to avoid AttributeError
if table_gk is not None and table_gk.tbody is not None:
    rows = table_gk.tbody.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if not cols:
            continue
        player = {}

        player['Name'] = cols[0].text.strip() if cols[0].text.strip() else "N/A"
        player['GA'] = cols[10].text.strip() if cols[10].text.strip() else "N/A"
        player['GA90'] = cols[11].text.strip() if cols[11].text.strip() else "N/A"
        player['SoTA'] = cols[12].text.strip() if cols[12].text.strip() else "N/A"
        player['Saves'] = cols[13].text.strip() if cols[13].text.strip() else "N/A"
        player['Save%'] = cols[14].text.strip() if cols[14].text.strip() else "N/A"
        player['W'] = cols[15].text.strip() if cols[15].text.strip() else "N/A"
        player['D'] = cols[16].text.strip() if cols[16].text.strip() else "N/A"
        player['L'] = cols[17].text.strip() if cols[17].text.strip() else "N/A"
        player['CS'] = cols[18].text.strip() if cols[18].text.strip() else "N/A"
        player['CS%'] = cols[19].text.strip() if cols[19].text.strip() else "N/A"
        player['PKatt'] = cols[20].text.strip() if cols[20].text.strip() else "N/A"
        player['PKA'] = cols[21].text.strip() if cols[21].text.strip() else "N/A"
        player['PKSV'] = cols[22].text.strip() if cols[22].text.strip() else "N/A"
        player['PKm'] = cols[23].text.strip() if cols[23].text.strip() else "N/A"
        player['GK_Save%'] = cols[24].text.strip() if cols[24].text.strip() else "N/A"

        new_GK_data.append(player)
else:
    # No goalkeeper table found on the page; continue with empty GK data
    new_GK_data = []



# === PHẦN 5: GỘP DỮ LIỆU ===
# (Code từ image_a9f9a6.png)
# Danh sách các thuộc tính cần cập nhật
GK_attributes_to_update = ['GA', 'GA90', 'SoTA', 'Saves',
                           'Save%', 'W', 'D', 'L', 'CS', 'CS%', 'PKatt', 'PKA', 'PKSV',
                           'PKm', 'GK_Save%']

# Cập nhật vào danh sách "data" hiện có
for player in data:
    # Tìm cầu thủ trong new_data dựa vào tên
    matching_player = next((p for p in new_GK_data if p['Name'] == player['Name']), None)
    
    # Nếu tìm thấy cầu thủ, cập nhật các thuộc tính
    if matching_player:
        for attr in GK_attributes_to_update:
            if attr in matching_player: 
                player[attr] = matching_player[attr]

# === PHẦN 6: XỬ LÝ DỮ LIỆU VÀ XUẤT FILE ===
# (Code từ các ảnh mới)

# Lưu dữ liệu vào DataFrame (từ image_a9f9a9.png)
df = pd.DataFrame(data)

# Tạo cột 'First_Name' bằng cách tách tên đầy đủ (từ image_a9f9ac.png)
df['First_Name'] = df['Name'].apply(lambda x: x.split()[-1])

# Chuyển đổi cột 'Age' sang kiểu số nguyên (int) (từ image_a9f9c4.png)
df['Age'] = df['Age'].astype(int)

# Sắp xếp theo 'First_Name' (A-Z) và sau đó theo 'Age' (lớn đến nhỏ) (từ image_a9fc94.png)
df = df.sort_values(by=['First_Name', 'Age'], ascending=[True, False])

# Xuất ra file CSV (từ image_a9fcaf.png)
df.to_csv('results.csv', index=False)

# === GHI VÀO SQLITE ===
import sqlite3
import os

# Tạo file DB trong cùng thư mục script (players.db)
db_path = os.path.join(os.path.dirname(__file__), 'players.db') if '__file__' in globals() else 'players.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Tạo bảng với tất cả cột là TEXT để tránh lỗi kiểu dữ liệu phức tạp;
# đặt tên cột trong dấu ngoặc kép để giữ nguyên các ký tự đặc biệt
columns = list(df.columns)
cols_ddl = ', '.join([f'"{c}" TEXT' for c in columns])
create_stmt = f'CREATE TABLE IF NOT EXISTS players ({cols_ddl});'
cur.execute(create_stmt)

# Xóa dữ liệu cũ trong bảng để mỗi lần chạy có dataset mới (tuỳ ý, có thể đổi thành append)
cur.execute('DELETE FROM players;')

# Chuẩn bị câu lệnh insert
placeholders = ','.join(['?'] * len(columns))
insert_stmt = f'INSERT INTO players ({", ".join([f"\"{c}\"" for c in columns])}) VALUES ({placeholders})'

# Chuyển DataFrame thành list of tuples và chèn
rows = []
for _, r in df.iterrows():
    vals = []
    for c in columns:
        v = r[c]
        # Biến NaN thành None
        if pd.isna(v):
            vals.append(None)
        else:
            vals.append(str(v))
    rows.append(tuple(vals))

if rows:
    cur.executemany(insert_stmt, rows)
    conn.commit()

conn.close()

print("✅ Đã cào xong dữ liệu và lưu vào results.csv + players.db (bảng 'players'). Trình duyệt sẽ đóng sau khi bạn nhấn Enter.")
input("Nhấn Enter để thoát...")
driver.quit()

