import pandas as pd
import sqlite3
df1 = pd.read_csv("BANG_CAU_THU_NGOAI_HANG_ANH_CO_SO_PHUT_THI_DAU_HON_90_PHUT.csv")
df2 = pd.read_csv("BANG_CHUYEN_NHUONG_CAU_THU_2024_2025.csv")


merged = pd.merge(df1, df2, left_on="Player", right_on="Name", how="left")


result = merged[["Player","Old_team", "New_team", "Price"]]


result[["Old_team", "New_team", "Price"]] = result[["Old_team", "New_team", "Price"]].fillna("N/a")

conn = sqlite3.connect("premier_league.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS CHUYEN_NHUONG (
        Player TEXT,
        Old_team TEXT,
        New_team TEXT,
        Price TEXT
    )
""")
# cursor.execute("DELETE FROM CHUYEN_NHUONG")

for _, row in result.iterrows():
    cursor.execute("""
        INSERT INTO CHUYEN_NHUONG (Player, Old_team, New_team, Price)
        VALUES (?, ?, ?, ?)
    """, (row["Player"], row["Old_team"], row["New_team"], row["Price"]))

conn.commit()
conn.close()

print("DONE")