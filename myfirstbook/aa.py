# app.py
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_percentage_error

# -----------------------------
# Judul Aplikasi
# -----------------------------
st.set_page_config(page_title="Forecasting NO2 Surabaya", layout="wide")
st.title("🌆 Forecasting NO2 - Surabaya (Demo Interaktif)")

# -----------------------------
# Path CSV lokal
# -----------------------------
DATA_FOLDER = "no2_results_surabaya"
DATA_FILE = "hasil_prediksi_knn.csv"
DATA_PATH = os.path.join(DATA_FOLDER, DATA_FILE)

# Baca CSV
if not os.path.exists(DATA_PATH):
    st.warning(f"File '{DATA_FILE}' tidak ditemukan di folder '{DATA_FOLDER}'.")
    st.stop()

data = pd.read_csv(DATA_PATH)

# -----------------------------
# Input interaktif
# -----------------------------
st.subheader("Pengaturan Interaktif")

# Slider untuk memilih range index (contoh: prediksi 0-3)
max_index = len(data) - 1
range_slider = st.slider("Pilih range index data untuk visualisasi:", 0, max_index, (0, max_index))

# Filter data sesuai range
data_filtered = data.iloc[range_slider[0]:range_slider[1]+1]

# Pilihan kolom actual/predicted (jika ada beberapa)
columns = data_filtered.columns.tolist()
actual_col = st.selectbox("Pilih kolom Actual:", columns, index=columns.index("NO2_Actual"))
predicted_col = st.selectbox("Pilih kolom Predicted:", columns, index=columns.index("NO2_Predicted"))

# -----------------------------
# Preview data filtered
# -----------------------------
st.subheader("Preview Data (Filtered)")
st.dataframe(data_filtered)

# -----------------------------
# Statistik deskriptif
# -----------------------------
st.subheader("Statistik Data (Filtered)")
st.write(data_filtered.describe())

# -----------------------------
# Visualisasi Actual vs Predicted
# -----------------------------
st.subheader("Visualisasi NO2 (Filtered)")
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(data_filtered.index, data_filtered[actual_col], label="Actual", marker='o')
ax.plot(data_filtered.index, data_filtered[predicted_col], label="Predicted", marker='x')
ax.set_xlabel("Index")
ax.set_ylabel("Konsentrasi NO2")
ax.set_title(f"{actual_col} vs {predicted_col}")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# -----------------------------
# Evaluasi MAPE
# -----------------------------
st.subheader("Evaluasi MAPE (Filtered)")
mape = mean_absolute_percentage_error(data_filtered[actual_col], data_filtered[predicted_col])
st.metric("MAPE", f"{mape*100:.2f}%")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("💡 Demo interaktif menggunakan dataset Surabaya (NO2)")
