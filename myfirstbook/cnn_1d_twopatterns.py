import streamlit as st
import numpy as np
import tensorflow as tf
import joblib
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="CNN 1D TwoPatterns",
    layout="centered"
)

# =========================
# LOAD MODEL & ENCODER
# =========================
@st.cache_resource
def load_model_and_encoder():
    base_path = os.path.dirname(__file__)

    model_path = os.path.join(base_path, "cnn_1d_twopatterns.h5")
    encoder_path = os.path.join(base_path, "label_encoder.pkl")

    model = tf.keras.models.load_model(model_path)
    encoder = joblib.load(encoder_path)

    return model, encoder


model, le = load_model_and_encoder()

# =========================
# TITLE
# =========================
st.title("📊 CNN 1D – TwoPatterns Classification")
st.write("Klasifikasi time series (panjang 128) menggunakan CNN 1D.")

# =========================
# INPUT DATA
# =========================
st.subheader("🔢 Input Time Series")

st.write("Masukkan **128 angka**, dipisahkan dengan koma (,).")

input_series = st.text_area(
    "Contoh:",
    "0.2,0.3,0.1,-0.2,...",
    height=120
)

# =========================
# PREDICTION
# =========================
if st.button("🔍 Prediksi"):
    try:
        values = np.array([float(v) for v in input_series.split(",")])

        if len(values) != 10:
            st.error("❌ Jumlah data HARUS 128")
        else:
            X_input = values.reshape(1, 10, 1)
            prediction = model.predict(X_input)

            predicted_class = np.argmax(prediction, axis=1)
            label = le.inverse_transform(predicted_class)[0]

            st.success("✅ Prediksi Berhasil")
            st.write(f"**Kelas Prediksi:** `{label}`")
            st.write("**Probabilitas:**")
            st.write(prediction)

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("Deployment CNN 1D – CRISP-DM | TwoPatterns Dataset")
