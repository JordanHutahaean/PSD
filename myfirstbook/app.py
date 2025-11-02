import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score, mean_absolute_percentage_error

# Judul aplikasi
st.title("🌤️ Prediksi Kadar NO₂ Besok di Surabaya (KNN Regression)")

# Upload data
uploaded_file = st.file_uploader("📂 Unggah file CSV data historis NO₂", type=["csv"])

if uploaded_file:
    # Membaca data
    data = pd.read_csv(uploaded_file)
    st.write("### 📊 Data yang diunggah:")
    st.write(data.head())

    # Pastikan kolom pertama adalah tanggal (opsional)
    if "tanggal" in data.columns[0].lower():
        st.info("Kolom pertama dianggap sebagai tanggal dan tidak digunakan untuk training.")
        data = data.iloc[:, 1:]

    # Pilih jumlah hari sebelumnya untuk memprediksi hari besok
    n_day = st.slider("Gunakan berapa hari sebelumnya untuk prediksi besok?", 2, 7, 3)

    # Membentuk fitur X dan target y
    X, y = [], []
    for i in range(len(data) - n_day):
        X.append(data.iloc[i:i + n_day, 0].values)
        y.append(data.iloc[i + n_day, 0])
    X = np.array(X)
    y = np.array(y)

    # Split data untuk evaluasi
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Pilih nilai k
    k = st.slider("Pilih nilai k untuk KNN:", 1, 20, 5)

    # Training model
    model = KNeighborsRegressor(n_neighbors=k)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Evaluasi performa
    r2 = r2_score(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred)

    st.write(f"**🎯 R² Score:** {r2:.3f}")
    st.write(f"**📉 MAPE:** {mape:.3f}")

    # Prediksi NO2 untuk besok (dari data terbaru)
    last_days = data.iloc[-n_day:, 0].values.reshape(1, -1)
    next_pred = model.predict(last_days)[0]

    st.success(f"🧠 Prediksi kadar NO₂ untuk BESOK adalah **{next_pred:.2f} µg/m³**")

    st.caption("Model menggunakan K-Nearest Neighbors Regression berdasarkan data historis NO₂.")
