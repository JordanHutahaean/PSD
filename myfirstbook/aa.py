import pandas as pd
import numpy as np
import streamlit as st
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_percentage_error
import matplotlib.pyplot as plt

st.header("📊 Prediksi NO₂ Surabaya")

uploaded_file = st.file_uploader("Unggah CSV data NO₂ Surabaya", type=["csv"], key="no2")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Preview data NO₂:")
    st.dataframe(data.head())

    if "NO2" not in data.columns:
        st.error("CSV harus memiliki kolom 'NO2'")
    else:
        # Buat fitur lag 1
        data["NO2_lag1"] = data["NO2"].shift(1)
        data = data.dropna()

        X = data[["NO2_lag1"]]
        y = data["NO2"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        r2 = r2_score(y_test, y_pred)
        mape = mean_absolute_percentage_error(y_test, y_pred)

        st.write(f"R² Score: {r2:.3f}")
        st.write(f"MAPE: {mape*100:.2f}%")

        # Plot hasil
        fig, ax = plt.subplots()
        ax.plot(y_test.values, label="Actual")
        ax.plot(y_pred, label="Predicted")
        ax.set_title("Prediksi NO₂ Surabaya")
        ax.set_ylabel("NO₂")
        ax.legend()
        st.pyplot(fig)

        # Prediksi hari berikutnya
        last_value = data["NO2"].iloc[-1]
        next_pred = model.predict(np.array([[last_value]]))[0]
        st.success(f"Prediksi NO₂ berikutnya: {next_pred:.2f}")
