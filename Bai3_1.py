import sqlite3
import pandas as pd
import numpy as np

# ĐỌC DỮ LIỆU TỪ CƠ SỞ DỮ LIỆU
conn = sqlite3.connect('premier_league.db')
df = pd.read_sql_query('SELECT * FROM Cau_Thu', conn)
conn.close()

print(f"\nĐã đọc dữ liệu từ cơ sở dữ liệu: {len(df)} cầu thủ")


# CHUẨN HÓA DỮ LIỆU & XÁC ĐỊNH CÁC CỘT SỐ
# Loại bỏ các cột không phải dạng số (text như Name, Team, Nation, Position)
exclude_cols = ['Name', 'Nation', 'Team', 'Position']
cols_num = [c for c in df.columns if c not in exclude_cols]

# Chuyển đổi dữ liệu sang dạng số 
for c in cols_num:
    # Xóa dấu phẩy trong các số có định dạng "1,234"
    df[c] = df[c].astype(str).str.replace(',', '', regex=False)
    df[c] = pd.to_numeric(df[c], errors='coerce')


# NHÓM THEO ĐỘI BÓNG & TÍNH THỐNG KÊ
grouped = (
    df.groupby('Team')[cols_num]
      .agg(['median', 'mean', 'std'])
      .round(2)
)

# Làm phẳng tên cột: ví dụ ('Gls','mean') → 'Gls_mean'
grouped.columns = ['_'.join(col).strip() for col in grouped.columns.values]
grouped = grouped.copy()
grouped.reset_index(inplace=True)

# Xuất file CSV kết quả
grouped.to_csv('THONG_KE_CAU_THU_THEO_CLB.csv', encoding='utf-8-sig', index=False)
print("Đã lưu file: THONG_KE_CAU_THU_THEO_CLB.csv")


# TÌM ĐỘI CÓ CHỈ SỐ TRUNG BÌNH CAO NHẤT Ở MỖI CHỈ SỐ
# Chỉ chọn các cột kết thúc bằng "_mean"
mean_cols = [c for c in grouped.columns if (c.endswith('_mean') and not c.startswith('Age'))]

# Đặt Team làm index để dễ xử lý
mean_df = grouped.set_index('Team')[mean_cols]

# Tìm đội có giá trị trung bình cao nhất cho từng chỉ số
mean_df_valid = mean_df.dropna(axis=1, how='all')
max_teams = mean_df_valid.idxmax()
max_teams.index = [c[:-5] for c in max_teams.index]  # bỏ hậu tố "_mean"

# Xuất bảng kết quả
df_max = max_teams.reset_index()
df_max.columns = ['Chi_so', 'Doi_phong_do_tot_nhat']

print("\nĐội có chỉ số trung bình cao nhất ở từng chỉ số:")
print(df_max.to_string(index=False))

df_max.to_csv('DOI_PHONG_DO_TOT_NHAT.csv', encoding='utf-8-sig', index=False)
print("Đã lưu file: DOI_PHONG_DO_TOT_NHAT.csv")


# XẾP HẠNG PHONG ĐỘ TỔNG THỂ
ranking = grouped.copy()

# Tính thứ hạng cho từng chỉ số (1 = cao nhất)
for c in mean_cols:
    ranking[c] = ranking[c].rank(ascending=False)

# Tính trung bình thứ hạng => tổng phong độ
ranking = ranking.copy()
ranking['Tong_hang'] = ranking[mean_cols].mean(axis=1)

# Đội có tổng hạng thấp nhất là đội phong độ cao nhất
best_team = ranking.loc[ranking['Tong_hang'].idxmin(), 'Team']
print(f"\nĐội có phong độ tổng thể tốt nhất: {best_team}")

ranking.to_csv('XEP_HANG_TONG_THE.csv', encoding='utf-8-sig', index=False)
print("Đã lưu file: XEP_HANG_TONG_THE.csv")
