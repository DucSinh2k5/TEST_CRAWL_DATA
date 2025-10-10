import pandas as pd
import sqlite3
df1 = pd.read_csv("BANG_CAU_THU_NGOAI_HANG_ANH_CO_SO_PHUT_THI_DAU_HON_90_PHUT.csv")
df2 = pd.read_csv("BANG_CHUYEN_NHUONG_CAU_THU_2024_2025.csv")


merged = pd.merge(df1, df2, left_on="Player", right_on="Name", how="left")


result = merged[["Player", "Price"]]


result["Price"] = result["Price"].fillna("N/a")

conn = sqlite3.connect("transfer_premier_league_2024_2025.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Transfers (
        Player TEXT,
        Price TEXT
    )
""")
cursor.execute("DELETE FROM Transfers")


for _, row in result.iterrows():
    cursor.execute("INSERT INTO Transfers (Player, Price) VALUES (?, ?)", (row["Player"], row["Price"]))

conn.commit()
conn.close()

print("DONE")