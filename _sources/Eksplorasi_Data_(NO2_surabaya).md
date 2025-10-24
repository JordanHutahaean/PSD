# Eksplorasi Data (NO2 Surabaya)

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```


# Membaca Dataset

```python

import pandas as pd

# 1️⃣ Baca file hasil unduhan dari Copernicus
df = pd.read_csv("no2_results_surabaya/timeseries.csv")

# 2️⃣ Konversi kolom tanggal ke format datetime
df["date"] = pd.to_datetime(df["date"])

# 3️⃣ Urutkan berdasarkan tanggal
df = df.sort_values("date")

# 4️⃣ Tampilkan 5 baris pertama untuk memastikan hasilnya benar
print("Data awal dari Copernicus (5 baris teratas):")
print(df.head())


```

