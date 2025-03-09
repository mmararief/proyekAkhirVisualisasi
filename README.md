# Bike Sharing Data Dashboard

## Overview

Dashboard ini dibuat menggunakan Streamlit untuk menganalisis data penyewaan sepeda berdasarkan dataset yang tersedia.

## Installation

1. Pastikan Anda telah menginstal Python.
2. Install dependencies dengan perintah berikut:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Dashboard

Jalankan perintah berikut untuk memulai dashboard:

```bash
streamlit run dashboard.py
```

## Features

- Menampilkan dataset penyewaan sepeda.
- Visualisasi jumlah penyewaan sepeda berdasarkan waktu.
- Analisis hubungan cuaca dengan jumlah penyewaan.
- Tren penyewaan berdasarkan jam dalam sehari.

## Dataset

- `day.csv` : Data harian penyewaan sepeda.
- `hour.csv` : Data penyewaan berdasarkan jam.

## Deployment

Untuk mengunggah ke Streamlit Cloud, pastikan Anda memiliki akun Streamlit dan ikuti langkah berikut:

1. Commit kode ke GitHub.
2. Masuk ke [Streamlit Cloud](https://share.streamlit.io/).
3. Hubungkan dengan repositori GitHub dan jalankan aplikasi.
