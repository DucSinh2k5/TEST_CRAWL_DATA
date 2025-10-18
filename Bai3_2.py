import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect('premier_league.db')
df_player = pd.read_sql_query('SELECT * FROM CauThu', conn)
df_value = pd.read_sql_query('SELECT * FROM CHUYEN_NHUONG', conn)
conn.close()

print(f"Đã đọc dữ liệu: {len(df_player)} cầu thủ, {len(df_value)} dữ liệu chuyển nhượng")

# Chuẩn hóa tên cầu thủ để ghép dữ liệu
df_player['Player'] = df_player['Player'].str.strip().str.lower()
df_value['Player'] = df_value['Player'].str.strip().str.lower()

# Làm sạch cột Price
def parse_price(p):
    if pd.isna(p): 
        return None
    p = str(p).strip().upper()
    if p == "FREE": return 0
    if "M" in p:
        try:
            return float(p.replace("M", "")) * 1_000_000
        except:
            return None
    if "K" in p:
        try:
            return float(p.replace("K", "")) * 1_000
        except:
            return None
    return None

df_value['Price'] = df_value['Price'].apply(parse_price)

# Gộp dữ liệu cầu thủ và giá chuyển nhượng
df = pd.merge(df_player, df_value, on='Player', how='left')
df = df.drop_duplicates(subset=['Player'], keep='first')

cols_num = [
    'Age', 'Min', 'Gls', 'Ast', 'xG', 'xAG',
    'PrgC', 'PrgP', 'CrdY', 'Price'
]

cols_num = [c for c in cols_num if c in df.columns]

for c in cols_num:
    df[c] = df[c].astype(str).str.replace(',', '', regex=False)
    df[c] = pd.to_numeric(df[c], errors='coerce')

df[cols_num] = df[cols_num].fillna(0)

# Hệ số điều chỉnh theo độ tuổi (đỉnh phong độ ~ 27 tuổi)
def age_factor(age):
    if pd.isna(age) or age <= 0:
        return 1
    return max(0.5, (30 - abs(age - 27)) / 30)

df['AgeFactor'] = df['Age'].apply(age_factor)

# Hàm định giá theo vị trí
def tinh_gia_tri(row):
    age_factor = row['AgeFactor']
    pos = str(row.get('Pos', '')).upper()

    # Tiền đạo (FW)
    if 'FW' in pos:
        val = (0.55 * row['Gls'] + 0.3 * row['xG'] + 0.15 * row['Ast']) * age_factor * 1_800_000

    # Tiền vệ (MF)
    elif 'MF' in pos:
        val = (0.45 * row['Ast'] + 0.35 * row['xAG'] + 0.2 * row['Gls']) * age_factor * 1_500_000

    # Hậu vệ (DF)
    elif 'DF' in pos:
        val = (0.4 * row['PrgC'] + 0.3 * row['PrgP'] + 0.3 * (1 - row['CrdY'] / 10)) * age_factor * 1_200_000

    # Thủ môn (GK)
    elif 'GK' in pos:
        val = (0.6 * (1 - row['CrdY'] / 10) + 0.4 * row['Min'] / 3000) * age_factor * 900_000

    # Vị trí không xác định
    else:
        val = (0.4 * row['Gls'] + 0.3 * row['Ast'] + 0.3 * row['xG']) * age_factor * 1_300_000

    return round(val, 1)

df['GiaTriUocLuong'] = df.apply(tinh_gia_tri, axis=1)

cols_out = [
    'Player', 'Pos', 'Squad', 'Age', 'Min', 'Gls', 'Ast', 'xG', 'xAG',
    'PrgC', 'PrgP', 'CrdY', 'Price', 'GiaTriUocLuong'
]
cols_out = [c for c in cols_out if c in df.columns]

df_out = df[cols_out]
df_out.to_csv('DINH_GIA_CAU_THU.csv', index=False, encoding='utf-8-sig')
print("Đã lưu file: DINH_GIA_CAU_THU.csv")