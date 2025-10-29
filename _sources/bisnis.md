# Business Understanding



## Judul Dataset
“Iris Flower Dataset” https://www.kaggle.com/datasets/arshid/iris-flower-dataset

## Menentukan Tujuan Bisnis
Tujuan Utama: Tujuan dari proyek ini adalah untuk memahami karakteristik fisik yang membedakan tiga spesies bunga Iris (Setosa, Versicolor, dan Virginica). Analisis ini bertujuan untuk memberikan dasar bagi sistem identifikasi otomatis atau untuk membantu ahli botani dalam mengklasifikasikan bunga Iris berdasarkan pengukuran kelopak (petal) dan mahkota (sepal).

Tujuan Teknis: Secara teknis, proyek ini bertujuan untuk:

Membangun alur kerja data dari database cloud (MySQL & PostgreSQL di Aiven) ke alat visualisasi (Power BI).

Melakukan analisis data eksplorasi untuk mengekstrak statistik deskriptif kunci (min, max, rata-rata).

Memvalidasi keseimbangan data antar kelas melalui visualisasi untuk memastikan setiap spesies terwakili dengan baik.

Kriteria Sukses: Proyek ini dianggap berhasil jika dasbor interaktif di Power BI berhasil dibuat, menampilkan semua metrik dan visualisasi yang diperlukan secara akurat, dengan data yang ditarik langsung dari kedua database.

## Membuat Rencana Proyek
Rencana proyek dibagi menjadi tahapan logis sebagai berikut:

Langkah 1: Membuat dan mengkonfigurasi database MySQL dan PostgreSQL pada platform Aiven.

Langkah 2: Membuat skema tabel iris di kedua database dan mengimpor data dari file CSV menggunakan DBeaver.

Langkah 3: Menghubungkan database ke Power BI agar data bisa divisualisasikan secara interaktif.

Langkah 4: Melakukan eksplorasi data:

Menghitung nilai minimum, maksimum, dan rata-rata tiap kolom numerik.

Membuat grafik batang jumlah data tiap kelas (Setosa, Versicolor, Virginica).

Langkah 5: Menyusun laporan insight dari hasil analisis.

## Menilai Situasi dan Kondisi
Sumber Daya:

Data: Dataset Iris klasik yang terdiri dari 150 sampel, yang merupakan data bersih dan terstruktur dengan baik.

Infrastruktur: Database MySQL dan PostgreSQL yang dihosting di platform cloud Aiven.

Perangkat Lunak: DBeaver untuk manajemen database dan Power BI untuk analisis serta visualisasi.

Risiko: Risiko utama dalam proyek ini adalah masalah konektivitas jaringan antara Power BI dan database cloud di Aiven, seperti timeout dan validasi sertifikat SSL. Risiko ini telah berhasil diidentifikasi dan diatasi selama tahap awal proyek.

Asumsi: Proyek ini mengasumsikan bahwa data yang disediakan dalam dataset Iris adalah akurat dan tidak memerlukan pembersihan data yang ekstensif (seperti penanganan nilai yang hilang atau outlier).