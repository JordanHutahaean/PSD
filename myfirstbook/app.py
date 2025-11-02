import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score, mean_absolute_percentage_error

st.title("🚀 KNN Regression untuk Data NO₂ Surabaya")

uploaded_file = st.file_uploader("Unggah file CSV data NO₂", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("### 📊 Data yang diunggah:")
    st.write(data.head())

    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    k = st.slider("Pilih nilai k:", 1, 20, 5)

    model = KNeighborsRegressor(n_neighbors=k)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred)

    st.write(f"**R² Score:** {r2:.3f}")
    st.write(f"**MAPE:** {mape:.3f}")
