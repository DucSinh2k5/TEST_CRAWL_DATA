import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


file_path = "BANG_CAU_THU_NGOAI_HANG_ANH_CO_SO_PHUT_THI_DAU_HON_90_PHUT.csv"
df = pd.read_csv(file_path)



if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])


df["Min"] = df["Min"].astype(str).str.replace(",", "").astype(int)


names = df["Player"]      
teams = df["Squad"]        
X = df.drop(columns=["Player", "Nation", "Pos", "Squad"]) 


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


pca2 = PCA(n_components=2)
X_pca2 = pca2.fit_transform(X_scaled)

df_pca2 = pd.DataFrame(X_pca2, columns=["PC1","PC2"])
df_pca2.insert(0, "Player", names)
df_pca2["Squad"] = teams


pca3 = PCA(n_components=3)
X_pca3 = pca3.fit_transform(X_scaled)

df_pca3 = pd.DataFrame(X_pca3, columns=["PC1","PC2","PC3"])
df_pca3.insert(0, "Player", names)
df_pca3["Squad"] = teams


df_pca2.to_csv("PCA_2D.csv", index=False)
df_pca3.to_csv("PCA_3D.csv", index=False)





plt.figure(figsize=(10,8))
scatter = plt.scatter(df_pca2["PC1"], df_pca2["PC2"], c=pd.factorize(df_pca2["Squad"])[0], cmap="tab20")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCA 2D (Premier League Players)")
plt.colorbar(scatter, label="Team index")

for i in range(0, len(df_pca2), 50): 
    plt.annotate(df_pca2["Player"].iloc[i],
                 (df_pca2["PC1"].iloc[i], df_pca2["PC2"].iloc[i]))

plt.show()


fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection="3d")
sc = ax.scatter(df_pca3["PC1"], df_pca3["PC2"], df_pca3["PC3"],
                c=pd.factorize(df_pca3["Squad"])[0], cmap="tab20")
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_zlabel("PC3")
plt.title("PCA 3D (Premier League Players)")
plt.colorbar(sc, label="Team index")

plt.show()
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt


inertias = []
sil_scores = []
K = range(2, 11)

for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
    sil_scores.append(silhouette_score(X_scaled, kmeans.labels_))


plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.plot(K, inertias, "o-")
plt.xlabel("Số cụm k")
plt.ylabel("Inertia (SSE)")
plt.title("Elbow Method")


plt.subplot(1,2,2)
plt.plot(K, sil_scores, "o-")
plt.xlabel("Số cụm k")
plt.ylabel("Silhouette Score")
plt.title("Silhouette Method")
plt.show()
