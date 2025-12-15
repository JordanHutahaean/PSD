import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib
from tensorflow.keras.models import load_model

# ==============================
# Load model & label encoder
# ==============================
model = load_model("cnn_twopatterns.h5")
le = joblib.load("label_encoder.pkl")

# ==============================
# UI Streamlit
# ==============================
st.title("Klasifikasi Time Series TwoPatterns (CNN 1D)")
st.write(
    "Upload file CSV berisi data time series. "
    "Data akan disesuaikan menjadi 128 titik."
)

# ==============================
# Upload CSV
# ==============================
uploaded_file = st.file_uploader(
    "Upload file CSV",
    type=["csv"]
)

# ==============================
# Prediksi
# ==============================
if uploaded_file is not None:
    try:
        # ==============================
        # BACA CSV
        # ==============================
        df = pd.read_csv(uploaded_file)

        st.write("Preview data CSV:")
        st.dataframe(df.head())

        # Ambil semua nilai numerik (kolom pertama)
        values = df.iloc[:, 0].values.astype(float)

        st.write("Jumlah data terbaca:", len(values))

        # ==============================
        # VALIDASI PANJANG DATA
        # ==============================
        if len(values) < 128:
            st.error("❌ Jumlah data kurang dari 128 nilai!")
            st.stop()
        elif len(values) > 128:
            st.warning("⚠️ Data lebih dari 128 nilai, diambil 128 pertama.")
            values = values[:128]

        # ==============================
        # RESHAPE UNTUK CNN
        # ==============================
        X_input = values.reshape(1, 128, 1)

        # ==============================
        # PREDIKSI + TEMPERATURE SCALING
        # ==============================
        logits = model.predict(X_input)

        temperature = 2.0
        logits = logits / temperature

        exp_logits = np.exp(logits)
        pred = exp_logits / np.sum(exp_logits, axis=1, keepdims=True)

        kelas = np.argmax(pred, axis=1)
        label = le.inverse_transform(kelas)[0]

        # ==============================
        # OUTPUT
        # ==============================
        st.success(f"✅ Hasil Prediksi Kelas: **{label}**")

        st.subheader("Probabilitas Kelas")
        for i, prob in enumerate(pred[0]):
            st.write(f"{le.classes_[i]} : {prob:.6f}")

        # ==============================
        # VISUALISASI
        # ==============================
        st.subheader("Visualisasi Time Series Input")
        fig, ax = plt.subplots()
        ax.plot(values)
        ax.set_xlabel("Time Step")
        ax.set_ylabel("Nilai")
        ax.set_title("Time Series Input")
        st.pyplot(fig)

    except Exception as e:
        st.error("❌ Gagal membaca file CSV. Pastikan hanya berisi angka.")
