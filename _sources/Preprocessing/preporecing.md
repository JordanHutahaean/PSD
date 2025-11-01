# Preprocessing Data(Iris)

## Remove Data Outlier
## Remove Data Outlier Hasil dari Metode ABOD

```python
import pandas as pd
from pycaret.anomaly import * 
import matplotlib.pyplot as plt

data = pd.read_csv("IRIS.csv")
data = data.drop(columns=["species"])

s = setup(data)

abod = create_model('abod', fraction=0.05) 
results = assign_model(abod)

results_sorted = results.sort_values(by="Anomaly", ascending=False)

# Ringkasan hasil outlier detection (tampilkan 10 baris pertama)
print("Ringkasan Hasil Outlier Detection (10 baris pertama):")
print(results_sorted[['sepal_length','sepal_width','petal_length','petal_width','Anomaly', 'Anomaly_Score']].head(10))

# Hitung jumlah outlier dan normal
outlier_count = results['Anomaly'].sum()
normal_count = len(results) - outlier_count
total_count = len(results)
outlier_percent = (outlier_count / total_count) * 100

print("\n Statistik Outlier:")
print(f"Total Data     : {total_count}")
print(f"Normal Data    : {normal_count}")
print(f"Outlier Data   : {outlier_count}")
print(f"Persentase Outlier : {outlier_percent:.2f}%")

# Visualisasi tabel ringkas (opsional, misalnya untuk notebook)
summary_df = pd.DataFrame({
    'Kategori': ['Normal', 'Outlier'],
    'Jumlah': [normal_count, outlier_count],
    'Persentase': [100 - outlier_percent, outlier_percent]
})
print("\n Ringkasan Jumlah Data:")
print(summary_df)


# Buat scatter plot dengan dua fitur utama
plt.figure(figsize=(8,6))
plt.scatter(
    results['sepal_length'], results['sepal_width'],
    c=results['Anomaly'], cmap='coolwarm', edgecolor='k'
)

# Tambahkan judul dan label
plt.title("Visualisasi Deteksi Outlier dengan ABOD")
plt.xlabel("Sepal Length")
plt.ylabel("Sepal Width")

# Tambahkan legenda
handles = [
    plt.Line2D([0], [0], marker='o', color='w', label='Normal',
               markerfacecolor='blue', markersize=8),
    plt.Line2D([0], [0], marker='o', color='w', label='Outlier',
               markerfacecolor='red', markersize=8)
]
plt.legend(handles=handles)

plt.show()
```

![abod](abod_.png)

Hasil Preprocessing dengan ABOD

Setelah dilakukan deteksi outlier menggunakan metode ABOD (Angle-Based Outlier Detection), data dibersihkan dengan cara menghapus baris yang teridentifikasi sebagai outlier


Jumlah data asli : 150 baris

Jumlah data setelah hapus outlier : 142 baris

Jumlah data yang terdeteksi sebagai outlier : 8 baris

Jadi, sekitar 5,33% data dianggap sebagai outlier dan dihapus dari dataset.

![abod](ABOD.png)

# KNN
## Remove Data Outlier Hasil dari Metode KNN

```python
import pandas as pd
from pycaret.anomaly import * 
import matplotlib.pyplot as plt

data = pd.read_csv("IRIS.csv")
data = data.drop(columns=["species"])

s = setup(data)

knn = create_model('knn', fraction=0.05) 
results = assign_model(knn)

results_sorted = results.sort_values(by="Anomaly", ascending=False)

# Ringkasan hasil outlier detection (tampilkan 10 baris pertama)
print("Ringkasan Hasil Outlier Detection (10 baris pertama):")
print(results_sorted[['sepal_length','sepal_width','petal_length','petal_width','Anomaly', 'Anomaly_Score']].head(10))

# Hitung jumlah outlier dan normal
outlier_count = results['Anomaly'].sum()
normal_count = len(results) - outlier_count
total_count = len(results)
outlier_percent = (outlier_count / total_count) * 100

print("\n Statistik Outlier:")
print(f"Total Data     : {total_count}")
print(f"Normal Data    : {normal_count}")
print(f"Outlier Data   : {outlier_count}")
print(f"Persentase Outlier : {outlier_percent:.2f}%")

# Visualisasi tabel ringkas (opsional, misalnya untuk notebook)
summary_df = pd.DataFrame({
    'Kategori': ['Normal', 'Outlier'],
    'Jumlah': [normal_count, outlier_count],
    'Persentase': [100 - outlier_percent, outlier_percent]
})
print("\n Ringkasan Jumlah Data:")
print(summary_df)


# Buat scatter plot dengan dua fitur utama
plt.figure(figsize=(8,6))
plt.scatter(
    results['sepal_length'], results['sepal_width'],
    c=results['Anomaly'], cmap='coolwarm', edgecolor='k'
)

# Tambahkan judul dan label
plt.title("Visualisasi Deteksi Outlier dengan knn")
plt.xlabel("Sepal Length")
plt.ylabel("Sepal Width")

# Tambahkan legenda
handles = [
    plt.Line2D([0], [0], marker='o', color='w', label='Normal',
               markerfacecolor='blue', markersize=8),
    plt.Line2D([0], [0], marker='o', color='w', label='Outlier',
               markerfacecolor='red', markersize=8)
]
plt.legend(handles=handles)

plt.show()
```
![knn](KNN_1.png)

Melalui tahap preprocessing dengan metode KNN, dilakukan pendeteksian outlier. Baris yang masuk kategori outlier dihilangkan dari dataset.

Jumlah data sebelum pembersihan: 150 baris

Jumlah data sesudah pembersihan: 142 baris

Outlier yang teridentifikasi: 8 baris

Artinya, kurang lebih 5,33% data dihapus karena dianggap menyimpang.
![knn](KNN1.png)

# LOF
## Remove Data Outlier Hasil dari Metode LOF

```python

import pandas as pd
from pycaret.anomaly import *
import matplotlib.pyplot as plt

# ========================================================
# 1. Load dataset
# ========================================================
data = pd.read_csv("IRIS.csv")

# Hapus kolom 'species'
if "species" in data.columns:
    data = data.drop(columns=["species"])

# ========================================================
# 2. Setup PyCaret
# ========================================================
s = setup(data, session_id=123)

# ========================================================
# 3. Buat model LOF untuk deteksi outlier
# ========================================================
lof = create_model('lof', fraction=0.05) 
results = assign_model(lof)

# Urutkan hasil berdasarkan Anomaly
results_sorted = results.sort_values(by="Anomaly", ascending=False)

# ========================================================
# 4. Ringkasan hasil
# ========================================================
print("Ringkasan Hasil Outlier Detection (10 baris pertama):")
print(results_sorted[['sepal_length','sepal_width','petal_length','petal_width','Anomaly','Anomaly_Score']].head(10))

# Hitung jumlah outlier dan normal
outlier_count = results['Anomaly'].sum()
normal_count = len(results) - outlier_count
total_count = len(results)
outlier_percent = (outlier_count / total_count) * 100

print("\nStatistik Outlier:")
print(f"Total Data     : {total_count}")
print(f"Normal Data    : {normal_count}")
print(f"Outlier Data   : {outlier_count}")
print(f"Persentase Outlier : {outlier_percent:.2f}%")

# ========================================================
# 5. Ringkasan tabel jumlah
# ========================================================
summary_df = pd.DataFrame({
    'Kategori': ['Normal', 'Outlier'],
    'Jumlah': [normal_count, outlier_count],
    'Persentase': [100 - outlier_percent, outlier_percent]
})
print("\nRingkasan Jumlah Data:")
print(summary_df)

# ========================================================
# 6. Visualisasi scatter plot sebelum hapus outlier
# ========================================================
plt.figure(figsize=(8,6))
plt.scatter(
    results['sepal_length'], results['sepal_width'],
    c=results['Anomaly'], cmap='coolwarm', edgecolor='k'
)

plt.title("Visualisasi Deteksi Outlier dengan LOF")
plt.xlabel("Sepal Length")
plt.ylabel("Sepal Width")

# Tambahkan legenda
handles = [
    plt.Line2D([0], [0], marker='o', color='w', label='Normal',
               markerfacecolor='blue', markersize=8),
    plt.Line2D([0], [0], marker='o', color='w', label='Outlier',
               markerfacecolor='red', markersize=8)
]
plt.legend(handles=handles)
plt.show()
```
![LOF](LOF_1.png)


Melalui deteksi outlier menggunakan algoritma LOF, sejumlah data yang tidak sesuai pola berhasil ditemukan dan dihilangkan dari dataset.

Data awal: 150 baris

Data setelah penghapusan outlier: 142 baris

Outlier yang terdeteksi: 8 baris

Artinya, 5,33% dari keseluruhan data dibersihkan karena terindikasi outlier.

![LOF](LOF_2.png)