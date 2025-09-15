# Preporecing

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