import pandas as pd
import sqlite3

# đọc CSV
df1 = pd.read_csv("bang1.csv")
df2 = pd.read_csv("bang2.csv")
df3 = pd.read_csv("bang3.csv")

# chuẩn hóa tên cột
for df in [df1, df2, df3]:
    df.columns = df.columns.str.strip().str.title()

# merge
merged = pd.merge(df1, df2, on="Name", how="left")
merged2 = pd.merge(df1, df3, on="Name", how="left")

result = merged[['Name', 'Old_Team', 'New_Team', 'Price']].fillna("N/a")

result1 = merged2[['Name', 'Age_y', 'Team_y', 'Price']].fillna("N/a")
result1 = result1.rename(columns={'Age_y': 'Age', 'Team_y': 'Team'})

# lưu DB
conn = sqlite3.connect("premier_league.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS CHUYEN_NHUONG (
        Name TEXT,
        Old_team TEXT,
        New_team TEXT,
        Price TEXT
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS GIA_TRI_CAU_THU (
        Name TEXT,
        Age TEXT,
        Team TEXT,
        Price TEXT
    )
""")

for _, row in result.iterrows():
    cur.execute("INSERT INTO CHUYEN_NHUONG VALUES (?, ?, ?, ?)", tuple(row))

for _, row in result1.iterrows():
    cur.execute("INSERT INTO GIA_TRI_CAU_THU VALUES (?, ?, ?, ?)", tuple(row))

conn.commit()
conn.close()

print("DONE | transfers:", len(result), "| values:", len(result1))
