import streamlit as st
import numpy as np
import librosa
import joblib
import os
from sklearn.ensemble import RandomForestClassifier

st.title("🎤 Deteksi Suara Buka / Tutup")

MODEL_PATH = "model_suara.pkl"

# Cek apakah model sudah ada, jika belum buat model dummy
if not os.path.exists(MODEL_PATH):
    st.warning("Model tidak ditemukan, membuat model dummy...")

    # buat data dummy (energi vs label)
    X_dummy = np.random.rand(20, 13)  # 20 sample, 13 fitur MFCC
    y_dummy = np.random.choice(["buka", "tutup"], size=20)

    clf = RandomForestClassifier()
    clf.fit(X_dummy, y_dummy)
    joblib.dump(clf, MODEL_PATH)
    st.success("Model dummy berhasil dibuat!")

# Load model
model = joblib.load(MODEL_PATH)

# Upload audio
audio_bytes = st.file_uploader("Upload file suara (.wav)", type=["wav"])

if audio_bytes is not None:
    # Simpan file audio ke sementara
    with open("temp.wav", "wb") as f:
        f.write(audio_bytes.read())

    # 🎧 Tambahkan fitur play audio di Streamlit
    st.audio("temp.wav", format="audio/wav")

    # Ekstraksi fitur MFCC
    y, sr = librosa.load("temp.wav", sr=16000)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfccs_mean = np.mean(mfccs.T, axis=0).reshape(1, -1)

    # Prediksi hasil
    pred = model.predict(mfccs_mean)[0]
    st.success(f"🔊 Terdeteksi: **{pred.upper()}**")

    # 🔹 Tampilkan probabilitas prediksi
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(mfccs_mean)[0]
        labels = model.classes_
        st.subheader("📊 Probabilitas:")
        for label, prob in zip(labels, probs):
            st.write(f"**{label}: {prob*100:.2f}%**")
            st.progress(float(prob))
