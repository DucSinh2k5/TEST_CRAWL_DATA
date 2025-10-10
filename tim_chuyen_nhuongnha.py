import pandas as pd

df1 = pd.read_csv("BANG_CAU_THU_NGOAI_HANG_ANH_CO_SO_PHUT_THI_DAU_HON_90_PHUT.csv")
df2 = pd.read_csv("BANG_CHUYEN_NHUONG_CAU_THU_2024_2025.csv")


merged = pd.merge(df1, df2, left_on="Player", right_on="Name", how="left")


result = merged[["Player", "Price"]]


result["Price"] = result["Price"].fillna("N/a")


result.to_csv("THU_THAP_GIA_CHUYEN_NHUONG_CAU_THU.csv", index=False)
print("DONE")
