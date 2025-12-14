import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
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
    "Masukkan data time series (bebas format), sistem akan menyesuaikan menjadi 128 titik. "
    "Probabilitas ditampilkan menggunakan temperature scaling agar lebih seimbang."
)

# Input data
input_data = st.text_area(
    "Input Time Series:",
    height=150
)

# ==============================
# Prediksi
# ==============================
if st.button("Prediksi"):
    try:
        # ==============================
        # PREPROCESS INPUT (ANTI ERROR)
        # ==============================
        cleaned = (
            input_data
            .replace("\n", "")
            .replace(";", ",")
            .split(",")
        )

        values = []
        for v in cleaned:
            v = v.strip()
            if v != "":
                values.append(float(v))

        values = np.array(values)

        # Debug info
        st.write("Jumlah nilai terbaca:", len(values))

        # Normalisasi panjang data
        if len(values) < 128:
            st.error("❌ Jumlah data kurang dari 128 nilai!")
            st.stop()
        elif len(values) > 128:
            st.warning("⚠️ Data lebih dari 128 nilai, diambil 128 pertama.")
            values = values[:128]

        # Reshape ke format CNN 1D
        X_input = values.reshape(1, 128, 1)

        # ==============================
        # PREDIKSI + TEMPERATURE SCALING
        # ==============================
        logits = model.predict(X_input)

        temperature = 2.0  # semakin besar → probabilitas makin merata
        logits = logits / temperature

        exp_logits = np.exp(logits)
        pred = exp_logits / np.sum(exp_logits, axis=1, keepdims=True)

        kelas = np.argmax(pred, axis=1)
        label = le.inverse_transform(kelas)[0]

        # ==============================
        # OUTPUT
        # ==============================
        st.success(f"✅ Hasil Prediksi Kelas: **{label}**")

        st.subheader("Probabilitas Kelas (Temperature Scaling)")
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
        st.error("❌ Input tidak valid. Pastikan hanya berisi angka.")
