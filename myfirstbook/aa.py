# app.py
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_percentage_error
import seaborn as sns

# -----------------------------
# Judul Aplikasi
# -----------------------------
st.set_page_config(page_title="KNN Regression NO2 Surabaya", layout="wide")
st.title("📈 KNN Regression NO2 - Surabaya")
st.markdown("Aplikasi Streamlit interaktif untuk prediksi NO2 menggunakan KNN Regression.")

# -----------------------------
# Path CSV default
# -----------------------------
DATA_FOLDER = "no2_results_surabaya"
DATA_FILE = "hasil_prediksi_knn.csv"
DATA_PATH = os.path.join(DATA_FOLDER, DATA_FILE)

# -----------------------------
# Upload CSV opsional
# -----------------------------
uploaded_file = st.file_uploader("Upload CSV NO2 (opsional)", type=["csv"])
if uploaded_file:
    data = pd.read_csv(uploaded_file)
else:
    # Buat folder & dummy CSV jika belum ada
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    if not os.path.exists(DATA_PATH):
        df_dummy = pd.DataFrame({
            "NO2_Actual": [50, 55, 60, 58, 62, 59, 61, 63, 60, 62],
            "NO2_Predicted": [52, 53, 61, 57, 63, 60, 60, 64, 61, 63]
        })
        df_dummy.to_csv(DATA_PATH, index=False)
    data = pd.read_csv(DATA_PATH)

# -----------------------------
# Sidebar interaktif
# -----------------------------
st.sidebar.header("Pengaturan Prediksi")
max_index = len(data) - 1
range_slider = st.sidebar.slider("Pilih range index/hari untuk visualisasi:", 0, max_index, (0, max_index))
data_filtered = data.iloc[range_slider[0]:range_slider[1]+1]

columns = data_filtered.columns.tolist()
actual_col = st.sidebar.selectbox("Kolom Actual:", columns, index=columns.index("NO2_Actual"))
predicted_col = st.sidebar.selectbox("Kolom Predicted:", columns, index=columns.index("NO2_Predicted"))

# -----------------------------
# Preview Data
# -----------------------------
st.subheader("📋 Preview Data")
st.dataframe(data_filtered)

# -----------------------------
# Statistik Deskriptif
# -----------------------------
st.subheader("📊 Statistik Data (Filtered)")
st.write(data_filtered.describe())

# -----------------------------
# Visualisasi Actual vs Predicted
# -----------------------------
st.subheader("📈 Visualisasi NO2")
sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(data_filtered.index, data_filtered[actual_col], label="Actual", marker='o', color="#1f77b4", linewidth=2)
ax.plot(data_filtered.index, data_filtered[predicted_col], label="Predicted", marker='x', color="#ff7f0e", linewidth=2)
ax.set_xlabel("Index / Hari")
ax.set_ylabel("Konsentrasi NO2")
ax.set_title(f"{actual_col} vs {predicted_col}")
ax.legend()
st.pyplot(fig)

# -----------------------------
# Evaluasi MAPE
# -----------------------------
st.subheader("📏 Evaluasi MAPE")
mape = mean_absolute_percentage_error(data_filtered[actual_col], data_filtered[predicted_col])
st.metric("MAPE", f"{mape*100:.2f}%")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("💡 Dibuat oleh Jordan Hutahaean - Demo KNN Regression NO2 Surabaya")
