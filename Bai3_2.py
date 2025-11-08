import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# ĐỌC VÀ GỘP DỮ LIỆU

# Đọc dữ liệu từ 2 file CSV
players = pd.read_csv('bang1.csv')
prices = pd.read_csv('bang3.csv')

players_clean = players.drop(['Age', 'Team'], axis=1)
df = pd.merge(players_clean, prices, on='Name', how='inner')

print(f"Số lượng cầu thủ sau khi gộp dữ liệu: {len(df)}")

# LÀM SẠCH VÀ TIỀN XỬ LÝ DỮ LIỆU

# Hàm chuyển đổi giá từ dạng chuỗi sang số
def parse_price(price_value):
    if pd.isna(price_value): 
        return np.nan
    price_str = str(price_value).strip().upper().replace("€", "").replace("M", "")
    try:
        return float(price_str) * 1_000_000
    except:
        return np.nan

df['Price'] = df['Price'].apply(parse_price)

df = df.dropna(subset=['Price'])
print(f"Số lượng cầu thủ có giá hợp lệ: {len(df)}")

# Tạo biến vị trí chính từ cột Position (lấy 2 ký tự đầu)
df['MainPos'] = df['Position'].astype(str).str.strip().str[:2]

# CHUYỂN ĐỔI DỮ LIỆU SỐ

for column in df.columns:
    if column not in ['Name', 'Nation', 'Team', 'Position', 'MainPos']:
        df[column] = pd.to_numeric(df[column], errors='coerce')

# LỰA CHỌN ĐẶC TRƯNG (FEATURE SELECTION)

# Lấy danh sách tất cả các cột có kiểu số
numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
print(f"Tổng số cột số: {len(numeric_columns)}")

# Tạo danh sách các đặc trưng (loại bỏ cột Price vì đây là biến mục tiêu)
features = [col for col in numeric_columns if col != 'Price']
print(f"Số lượng đặc trưng ban đầu: {len(features)}")

# Điền các giá trị NaN bằng 0 để đảm bảo tính toán không bị lỗi
df[features] = df[features].fillna(0)

# Tính toán tương quan giữa các đặc trưng và giá
price_correlations = df[features].corrwith(df['Price']).abs()

# Chọn các đặc trưng có tương quan > 0.1 với giá
selected_features = price_correlations[price_correlations > 0.1].index.tolist()
print(f"\nSố lượng đặc trưng được chọn (tương quan > 0.1): {len(selected_features)}")

# XỬ LÝ ĐA CỘNG TUYẾN

# Tính ma trận tương quan giữa các đặc trưng được chọn
correlation_matrix = df[selected_features].corr().abs()

# Tìm các cặp đặc trưng có tương quan cao (> 0.7)
high_correlation_pairs = []
columns_to_remove = set()

# Duyệt qua ma trận tương quan để tìm các cặp có tương quan cao
for i in range(len(correlation_matrix.columns)):
    for j in range(i + 1, len(correlation_matrix.columns)):
        correlation_value = correlation_matrix.iloc[i, j]
        if correlation_value > 0.7:  # Ngưỡng tương quan
            feature1 = correlation_matrix.columns[i]
            feature2 = correlation_matrix.columns[j]
            high_correlation_pairs.append((feature1, feature2, correlation_value))

print(f"Tìm thấy {len(high_correlation_pairs)} cặp đặc trưng có tương quan > 0.7")

# Với mỗi cặp tương quan cao, giữ lại đặc trưng có tương quan cao hơn với Price
for feature1, feature2, corr_value in high_correlation_pairs:
    if feature1 in columns_to_remove or feature2 in columns_to_remove:
        continue  # Đã được chọn để loại bỏ
    
    # So sánh tương quan với Price, giữ lại đặc trưng có tương quan cao hơn
    corr1_with_price = price_correlations[feature1]
    corr2_with_price = price_correlations[feature2]
    
    if corr1_with_price >= corr2_with_price:
        columns_to_remove.add(feature2)
    else:
        columns_to_remove.add(feature1)

# Loại bỏ các đặc trưng đã chọn
final_features = [feature for feature in selected_features if feature not in columns_to_remove]
print(f"Số lượng đặc trưng sau khi xử lý đa cộng tuyến: {len(final_features)}")

# MÃ HÓA BIẾN PHÂN LOẠI (ONE-HOT ENCODING)

# Tạo biến giả (dummy variables) cho vị trí cầu thủ
# Ví dụ: MainPos = 'DF' sẽ tạo cột Pos_DF = 1, các cột Pos khác = 0
df_encoded = pd.get_dummies(df, columns=['MainPos'], prefix='Pos')

# Lấy danh sách các cột vị trí đã được mã hóa
position_features = [col for col in df_encoded.columns if col.startswith('Pos_')]

# Kết hợp đặc trưng số và đặc trưng vị trí
all_features = final_features + position_features
print(f"Tổng số đặc trưng cuối cùng: {len(all_features)}")

# CHUẨN BỊ DỮ LIỆU CHO MÔ HÌNH

# Tách biến độc lập (X) và biến phụ thuộc (y)
X = df_encoded[all_features] 
y = df_encoded['Price']  

print(f"\nKích thước dữ liệu:")
print(f"X (đặc trưng): {X.shape}")
print(f"y (giá trị): {y.shape}")

# Chia dữ liệu thành tập huấn luyện (80%) và tập kiểm tra (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,       # 20% cho kiểm tra
    random_state=42      # Seed cố định để kết quả có thể tái lập
)

print(f"\nChia dữ liệu thành:")
print(f"Tập huấn luyện: {X_train.shape[0]} mẫu")
print(f"Tập kiểm tra: {X_test.shape[0]} mẫu")

# HUẤN LUYỆN MÔ HÌNH HỒI QUY TUYẾN TÍNH

# Khởi tạo mô hình hồi quy tuyến tính
model = LinearRegression()

# Huấn luyện mô hình trên tập huấn luyện
model.fit(X_train, y_train)

# ĐÁNH GIÁ MÔ HÌNH

# Dự đoán giá trên tập kiểm tra
y_pred = model.predict(X_test)

# Tính các chỉ số đánh giá
r2 = r2_score(y_test, y_pred)              
mae = mean_absolute_error(y_test, y_pred)     

print("\nKẾT QUẢ MÔ HÌNH HỒI QUY TUYẾN TÍNH\n")
print(f"R² Score: {r2:.3f}")
print(f"MAE: {mae:,.0f}")
print(f"Số mẫu huấn luyện: {X_train.shape[0]}")
print(f"Số mẫu kiểm tra: {X_test.shape[0]}")
print(f"Số đặc trưng: {X_train.shape[1]}")

# # PHÂN TÍCH Ý NGHĨA CÁC HỆ SỐ

# print("\nTOP 10 ĐẶC TRƯNG QUAN TRỌNG NHẤT")

# # Tạo DataFrame để hiển thị hệ số của các đặc trưng
# feature_importance = pd.DataFrame({
#     'Đặc_trưng': all_features,
#     'Hệ_số': model.coef_,
#     'Tương_quan_với_giá': [price_correlations.get(feature, 0) if feature in price_correlations else 0 
#                           for feature in all_features]
# })

# # Sắp xếp theo giá trị tuyệt đối của hệ số (độ quan trọng)
# feature_importance['|Hệ_số|'] = np.abs(feature_importance['Hệ_số'])
# feature_importance = feature_importance.sort_values('|Hệ_số|', ascending=False)

# # Hiển thị top 10 đặc trưng quan trọng nhất
# print(feature_importance[['Đặc_trưng', 'Hệ_số', 'Tương_quan_với_giá']].head(10).to_string(index=False))

# Tạo bản sao dữ liệu để xuất
df_output = df.copy()

df_output['Age'] = df_output['Age'].astype('Int64')

# Tính giá dự đoán (euro)
df_output['Predict_Price'] = model.predict(df_encoded[all_features])

# Chuyển cả giá thật và giá dự đoán sang triệu euro (M€)
df_output['Price_M'] = df_output['Price'] / 1_000_000
df_output['Predict_Price_M'] = df_output['Predict_Price'] / 1_000_000

# Làm tròn 1 số sau dấu phẩy
df_output['Price_M'] = df_output['Price_M'].round(1)
df_output['Predict_Price_M'] = df_output['Predict_Price_M'].round(1)

# Định dạng sang kiểu "€xx.xM"
df_output['Price_M'] = df_output['Price_M'].apply(lambda x: f"€{x}M" if pd.notna(x) else "")
df_output['Predict_Price_M'] = df_output['Predict_Price_M'].apply(lambda x: f"€{x}M" if pd.notna(x) else "")

# Chọn các cột cần thiết
output_columns = ['Name', 'Nation', 'Team', 'MainPos', 'Age', 'Price_M', 'Predict_Price_M']
output_columns = [col for col in output_columns if col in df_output.columns]

# Xuất ra file CSV
df_output[output_columns].to_csv('bang4.csv', index=False, encoding='utf-8-sig')

print("\nĐã lưu file: bang4.csv")