import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib
import os
from tensorflow.keras.models import load_model

# ==============================
# SET BASE DIRECTORY
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "cnn_twopatterns.h5")
ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")

# ==============================
# CEK FILE MODEL & ENCODER
# ==============================
if not os.path.exists(MODEL_PATH):
    st.error("❌ File cnn_twopatterns.h5 tidak ditemukan")
    st.stop()

if not os.path.exists(ENCODER_PATH):
    st.error("❌ File label_encoder.pkl tidak ditemukan")
    st.stop()

# ==============================
# LOAD MODEL & ENCODER
# ==============================
model = load_model(MODEL_PATH)
le = joblib.load(ENCODER_PATH)

# ==============================
# UI STREAMLIT
# ==============================
st.title("Klasifikasi Time Series TwoPatterns (CNN 1D)")
st.write(
    "Upload file CSV berisi **1 kolom data time series**. "
    "Data akan disesuaikan menjadi **128 titik**."
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

        st.subheader("Preview Data CSV")
        st.dataframe(df.head())

        values = df.iloc[:, 0].astype(float).values
        st.write("Jumlah data terbaca:", len(values))

        if len(values) < 128:
            st.error("❌ Data kurang dari 128 titik")
            st.stop()
        elif len(values) > 128:
            values = values[:128]

        X_input = values.reshape(1, 128, 1)

        pred = model.predict(X_input)
        kelas = np.argmax(pred, axis=1)
        label = le.inverse_transform(kelas)[0]

        st.success(f"✅ Hasil Prediksi: **{label}**")

        st.subheader("Probabilitas Kelas")
        for i, prob in enumerate(pred[0]):
            st.write(f"{le.classes_[i]} : {prob:.6f}")

        st.subheader("Visualisasi Time Series")
        fig, ax = plt.subplots()
        ax.plot(values)
        ax.set_xlabel("Time Step")
        ax.set_ylabel("Nilai")
        ax.set_title("Time Series Input")
        st.pyplot(fig)

    except ValueError:
        st.error("❌ CSV harus berisi angka saja")
    except Exception as e:
        st.error(f"❌ Error: {e}")
