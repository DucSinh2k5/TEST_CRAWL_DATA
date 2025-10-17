import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# --- Đọc và xử lý dữ liệu ---
file_path = "BANG_CAU_THU_NGOAI_HANG_ANH_CO_SO_PHUT_THI_DAU_HON_90_PHUT.csv"
df = pd.read_csv(file_path)

# Xóa cột thừa
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# Làm sạch cột 'Min'
df["Min"] = df["Min"].astype(str).str.replace(",", "").astype(float)

# Chọn dữ liệu số (loại bỏ các cột chuỗi)
X = df.drop(columns=["Player", "Nation", "Pos", "Squad"])

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- Phân cụm KMeans ---
n_clusters = 5
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=42)
labels = kmeans.fit_predict(X_scaled)

# --- Giảm chiều bằng PCA ---
pca_2d = PCA(n_components=2)
pca_3d = PCA(n_components=3)
X_pca_2d = pca_2d.fit_transform(X_scaled)
X_pca_3d = pca_3d.fit_transform(X_scaled)

# Tạo DataFrame PCA
df_pca_2d = pd.DataFrame(X_pca_2d, columns=["PC1", "PC2"])
df_pca_2d["Cluster"] = labels
df_pca_3d = pd.DataFrame(X_pca_3d, columns=["PC1", "PC2", "PC3"])
df_pca_3d["Cluster"] = labels

# --- Biểu đồ PCA 2D ---
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
for i in range(n_clusters):
    cluster_points = df_pca_2d[df_pca_2d["Cluster"] == i]
    plt.scatter(cluster_points["PC1"], cluster_points["PC2"], label=f"Cụm {i+1}", s=60)

centroids_2d = pca_2d.transform(kmeans.cluster_centers_)
plt.scatter(centroids_2d[:, 0], centroids_2d[:, 1], c='black', marker='X', s=200, label='Tâm cụm')

plt.title(f"Phân cụm KMeans (k={n_clusters}) - PCA 2D", fontsize=13)
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)

# --- Biểu đồ PCA 3D ---
ax = plt.subplot(1, 2, 2, projection='3d')
for i in range(n_clusters):
    cluster_points = df_pca_3d[df_pca_3d["Cluster"] == i]
    ax.scatter(cluster_points["PC1"], cluster_points["PC2"], cluster_points["PC3"], s=40, label=f"Cụm {i+1}")

centroids_3d = pca_3d.transform(kmeans.cluster_centers_)
ax.scatter(centroids_3d[:, 0], centroids_3d[:, 1], centroids_3d[:, 2],
           c='black', marker='X', s=200, label='Tâm cụm')

ax.set_title(f"Phân cụm KMeans (k={n_clusters}) - PCA 3D", fontsize=13)
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_zlabel("PC3")
ax.legend()
plt.tight_layout()
plt.show()