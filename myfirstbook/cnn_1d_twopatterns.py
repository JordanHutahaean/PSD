import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib
import os
from tensorflow.keras.models import load_model

st.write("Model path:", MODEL_PATH)
st.write("File exists:", os.path.exists(MODEL_PATH))


# ==============================
# SET BASE DIRECTORY (BENAR)
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "cnn_twopatterns.h5")
ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")

# ==============================
# LOAD MODEL & ENCODER (AMAN)
# ==============================
if not os.path.exists(MODEL_PATH):
    st.error("❌ File cnn_twopatterns.h5 TIDAK ditemukan!")
    st.write("📁 Isi folder aplikasi:", os.listdir(BASE_DIR))
    st.stop()

if not os.path.exists(ENCODER_PATH):
    st.error("❌ File label_encoder.pkl TIDAK ditemukan!")
    st.write("📁 Isi folder aplikasi:", os.listdir(BASE_DIR))
    st.stop()

model = load_model(MODEL_PATH)
le = joblib.load(ENCODER_PATH)

# ==============================
# UI STREAMLIT
# ==============================
st.title("Klasifikasi Time Series TwoPatterns (CNN 1D)")
st.write(
    "Upload file CSV berisi data time series. "
    "Data akan disesuaikan menjadi 128 titik."
)

# ==============================
# UPLOAD CSV
# ==============================
uploaded_file = st.file_uploader(
    "Upload file CSV",
    type=["csv"]
)

# ==============================
# PREDIKSI
# ==============================
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        st.write("Preview data CSV:")
        st.dataframe(df.head())

        values = df.iloc[:, 0].astype(float).values
        st.write("Jumlah data terbaca:", len(values))

        if len(values) < 128:
            st.error("❌ Jumlah data kurang dari 128 nilai!")
            st.stop()
        elif len(values) > 128:
            st.warning("⚠️ Data lebih dari 128 nilai, diambil 128 pertama.")
            values = values[:128]

        X_input = values.reshape(1, 128, 1)

        logits = model.predict(X_input)
        temperature = 2.0
        logits = logits / temperature

        exp_logits = np.exp(logits)
        pred = exp_logits / np.sum(exp_logits, axis=1, keepdims=True)

        kelas = np.argmax(pred, axis=1)
        label = le.inverse_transform(kelas)[0]

        st.success(f"✅ Hasil Prediksi Kelas: **{label}**")

        st.subheader("Probabilitas Kelas")
        for i, prob in enumerate(pred[0]):
            st.write(f"{le.classes_[i]} : {prob:.6f}")

        st.subheader("Visualisasi Time Series Input")
        fig, ax = plt.subplots()
        ax.plot(values)
        ax.set_xlabel("Time Step")
        ax.set_ylabel("Nilai")
        ax.set_title("Time Series Input")
        st.pyplot(fig)

    except Exception as e:
        st.error("❌ Gagal membaca file CSV. Pastikan hanya berisi angka.")
        st.write(e)
