

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.impute import SimpleImputer



# Đọc dữ liệu
df = pd.read_csv("bang1.csv")


feature = df.loc[:, 'Matches':].copy()
for col in feature.columns:
    if feature[col].dtype == 'object':
        feature[col] = feature[col].str.replace(',', '').replace('N/a', np.nan).astype(float)
    else:
        feature[col] = feature[col].astype(float)
feature = feature.fillna(0)


imputer = SimpleImputer(strategy='mean')
feature_imputed = pd.DataFrame(imputer.fit_transform(feature), columns=feature.columns, index=feature.index)

# Chuẩn hoá
sc = StandardScaler()
X_scaled = sc.fit_transform(feature_imputed)


max_k = 10
k_values = range(1, max_k + 1)
overall_mse_list = []
silhouette_list = []

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    centers = kmeans.cluster_centers_

   
    sq_dists = np.sum((X_scaled - centers[labels])**2, axis=1)
    overall_mse = sq_dists.mean()
    overall_mse_list.append(overall_mse)

  
    if k > 1:
        silhouette = silhouette_score(X_scaled, labels)
    else:
        silhouette = np.nan  
    silhouette_list.append(silhouette)
  


plt.figure(figsize=(8,6))
plt.plot(k_values, overall_mse_list, marker='o', linewidth=2, color='tab:blue')
plt.xlabel("Số cụm (k)", fontsize=12)
plt.ylabel("Overall MSE (avg squared distance)", fontsize=12)
plt.title("Biểu đồ Elbow - Đánh giá MSE theo số cụm", fontsize=14, fontweight='bold')
plt.grid(True, linestyle="--", alpha=0.6)
plt.xticks(np.arange(1, 11, 1))
plt.tight_layout()
plt.show()


plt.figure(figsize=(8,6))
plt.plot(k_values, silhouette_list, marker='s', linewidth=2, color='tab:orange')
plt.xlabel("Số cụm (k)", fontsize=12)
plt.ylabel("Silhouette Score", fontsize=12)
plt.title("Biểu đồ Silhouette - Đánh giá độ tách biệt cụm", fontsize=14, fontweight='bold')
plt.grid(True, linestyle="--", alpha=0.6)
plt.xticks(np.arange(1, 11, 1))
plt.tight_layout()
plt.show()
