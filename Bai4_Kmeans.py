import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# --- Đọc và xử lý dữ liệu ---
df = pd.read_csv("BANG_CAU_THU_NGOAI_HANG_ANH_CO_SO_PHUT_THI_DAU_HON_90_PHUT.csv")

# Xoá cột dư
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# Làm sạch cột "Min"
df["Min"] = df["Min"].astype(str).str.replace(",", "").astype(int)

# Loại bỏ cột không dùng cho phân cụm
X = df.drop(columns=["Player", "Nation", "Pos", "Squad"])

# Chuẩn hóa dữ liệu
sc = StandardScaler()
X_scaled = sc.fit_transform(X)

# --- Chạy KMeans và tính MSE & Silhouette ---
max_k = 10
k_values = range(2, max_k + 1)
overall_mse_list = []
silhouette_list = []

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    centers = kmeans.cluster_centers_

    # MSE (WCSS trung bình)
    sq_dists = np.sum((X_scaled - centers[labels])**2, axis=1)
    overall_mse = sq_dists.mean()
    overall_mse_list.append(overall_mse)

    # Silhouette score
    silhouette = silhouette_score(X_scaled, labels)
    silhouette_list.append(silhouette)

    # print(f"k={k}: Overall MSE={overall_mse:.6f}, Silhouette={silhouette:.6f}")

# --- Biểu đồ Elbow (Overall MSE) ---
plt.figure(figsize=(8,6))
plt.plot(k_values, overall_mse_list, marker='o', linewidth=2, color='tab:blue')
plt.xlabel("Số cụm (k)", fontsize=12)
plt.ylabel("Overall MSE (avg squared distance)", fontsize=12)
plt.title("Biểu đồ Elbow - Đánh giá MSE theo số cụm", fontsize=14, fontweight='bold')
plt.grid(True, linestyle="--", alpha=0.6)
plt.xticks(np.arange(1, 11, 1))
plt.tight_layout()
plt.show()

# --- Biểu đồ Silhouette ---
plt.figure(figsize=(8,6))
plt.plot(k_values, silhouette_list, marker='s', linewidth=2, color='tab:orange')
plt.xlabel("Số cụm (k)", fontsize=12)
plt.ylabel("Silhouette Score", fontsize=12)
plt.title("Biểu đồ Silhouette - Đánh giá độ tách biệt cụm", fontsize=14, fontweight='bold')
plt.grid(True, linestyle="--", alpha=0.6)
plt.xticks(np.arange(1, 11, 1))
plt.tight_layout()
plt.show()
