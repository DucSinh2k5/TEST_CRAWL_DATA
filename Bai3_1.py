import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect('premier_league.db')
df = pd.read_sql_query('SELECT * FROM CauThu', conn)
conn.close()

print('\nĐã đọc dữ liệu từ cơ sở dữ liệu (số cầu thủ):', len(df))

cols_int = [
    'Age', 'Born', 'MP', 'Starts', 'Min', 'Gls','Ast','G+A', 'G-PK',
    'PK', 'PKatt', 'CrdY', 'CrdR', 'PrgC', 'PrgP', 'PrgR'
]

cols_float = [
    '90s', 'xG', 'npxG', 'xAG', 'npxG+xAG',
    'Gls/90', 'Ast/90', 'G+A/90', 'G-PK/90','G+A-PK/90',
    'xG/90', 'xAG/90','xG+xAG/90','npxG/90','npxG+xAG/90'
]

cols_num = [c for c in cols_int + cols_float if c in df.columns]

for c in cols_num:
    df[c] = df[c].str.replace(',', '')
    if c in cols_int:
        df[c] = pd.to_numeric(df[c], errors='coerce').astype('Int64')
    else:
        df[c] = pd.to_numeric(df[c], errors='coerce').astype(float)

grouped = df.groupby('Squad')[cols_num].agg(['median', 'mean', 'std']).round(2)
grouped.columns = ['_'.join(col).strip() for col in grouped.columns.values]
grouped.reset_index(inplace=True)

grouped.to_csv('THONG_KE_CAU_THU_THEO_CLB.csv', encoding='utf-8-sig')
print('\nĐã lưu file THONG_KE_CAU_THU_THEO_CLB.csv')

mean_cols = [c for c in grouped.columns if (c.endswith('_mean') and not (c.startswith('Age') or c.startswith('Born')))]
mean_df = grouped.set_index('Squad')[mean_cols]

max_teams = mean_df.idxmax()
max_teams.index = [c[:-5] for c in max_teams.index]

df_max = max_teams.reset_index()
df_max.columns = ['Chi_so', 'Doi_phong_do_tot_nhat']

print('\nĐội có chỉ số trung bình cao nhất ở từng chỉ số:')
print(df_max.to_string(index=False))
df_max.to_csv('DOI_PHONG_DO_TOT_NHAT.csv', encoding='utf-8-sig')
print('\nĐã lưu file DOI_PHONG_DO_TOT_NHAT.csv')

# Xếp hạng các đội dựa trên giá trị trung bình của các chỉ số rồi quy ra điểm
# Tính trung bình điểm xếp hạng. Đội nào điểm thấp nhất sẽ có phong độ cao nhất

ranking = grouped.copy()
for c in mean_cols:
    ranking[c] = ranking[c].rank(ascending=False)

ranking['Tong_hang'] = ranking[mean_cols].mean(axis=1)
best_team = ranking.loc[ranking['Tong_hang'].idxmin(), 'Squad']
print(f'\nĐội có phong độ tổng thể tốt nhất: {best_team}')
# ranking.to_csv('Ranking.csv', encoding='utf-8-sig')