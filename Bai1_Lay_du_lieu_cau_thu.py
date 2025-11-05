
import time
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CauThu = [
    'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born',
    'MP', 'Starts','Min','90s',
    'Gls','Ast','G+A', 'G-PK','PK', 'PKatt', 'CrdY', 'CrdR',
    'xG', 'npxG', 'xAG', 'npxG+xAG',
    'PrgC', 'PrgP', 'PrgR',
    'Gls/90', 'Ast/90', 'G+A/90', 'G-PK/90','G+A-PK/90',
    'xG/90', 'xAG/90','xG+xAG/90','npxG/90','npxG+xAG/90'
]

URL = "https://fbref.com/en/comps/9/2024-2025/stats/2024-2025-Premier-League-Stats"

def main():
    
    options = uc.ChromeOptions()
  
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

   
    driver = uc.Chrome(options=options)

    try:
       
        driver.get(URL)

        wait = WebDriverWait(driver, 120)
        try:
            wait.until(EC.presence_of_element_located((By.ID, "stats_standard")))
            print("Bảng stats đã xuất hiện — tiếp tục phân tích.")
        except Exception as e:
            print("Chưa thấy bảng trong 120s. Trang có thể đang ở Cloudflare challenge.")
           
            extra_wait = 120
            t0 = time.time()
            while time.time() - t0 < extra_wait:
                time.sleep(2)
                if driver.find_elements(By.ID, "stats_standard"):
                    print("Bảng đã xuất hiện (sau thời gian chờ thêm).")
                    break
            else:
                print("Hết thời gian chờ. Thoát và thử fallback CSV hoặc mở profile thật.")
              
        
      
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", {"id": "stats_standard"})
        data = []

        
        rows = table.tbody.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if not cols:
                continue

            cauthu = {col: "N/a" for col in CauThu}
            c = 0
            for x in CauThu:
                if c < len(cols):
                    text = cols[c].text.strip()
                    cauthu[x] = text if text != "" else "N/a"
                else:
                    cauthu[x] = "N/a"
                c += 1

            minutes_value = cauthu.get("Min", "N/a").replace(',', '')
            try:
                if minutes_value != "N/a" and int(minutes_value) > 90:
                    data.append(cauthu)
            except:
    
                data.append(cauthu)

        
        df = pd.DataFrame(data, columns=CauThu)
        csv_path = "BANG_CAU_THU_NGOAI_HANG_ANH_CO_SO_PHUT_THI_DAU_HON_90_PHUT.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"Lưu CSV: {csv_path}")

        
        conn = sqlite3.connect("premier_league.db")
        cursor = conn.cursor()
        columns_sql = ", ".join([f"'{col}' TEXT" for col in CauThu])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS CauThu ({columns_sql})")
        conn.commit()

        for cauthu in data:
            values = [cauthu.get(col, "N/a") for col in CauThu]
            placeholders = ", ".join(["?"] * len(CauThu))
            cursor.execute(f"INSERT INTO CauThu VALUES ({placeholders})", values)
        conn.commit()
        conn.close()
        print("DONE: Đã lưu vào SQLite")
      

       
        time.sleep(5)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
