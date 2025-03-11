import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

# Streamlit Title
st.title("Analisis Penyewaan Sepeda")
st.write("Laporan interaktif tentang tren penyewaan sepeda berdasarkan musim, jam dalam sehari, dan faktor lingkungan.")

# Visualisasi Pengaruh Musim terhadap Penyewaan Sepeda
st.header("Pengaruh Musim terhadap Penyewaan Sepeda")
avg_rent_by_season = day_df.groupby("season")["cnt"].mean()

fig, ax = plt.subplots()
ax.bar(["Spring", "Summer", "Fall", "Winter"], avg_rent_by_season, color=['blue', 'orange', 'green', 'red'])
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_xlabel("Musim")
ax.set_title("Rata-rata Penyewaan Sepeda per Musim")
st.pyplot(fig)

st.write("**Insight:** Penyewaan sepeda paling tinggi terjadi pada musim gugur, sedangkan musim semi memiliki penyewaan paling rendah.")

# Visualisasi Tren Penyewaan Berdasarkan Jam dalam Sehari
st.header("Tren Penyewaan Sepeda Berdasarkan Jam dalam Sehari")
avg_rent_by_hour = hour_df.groupby("hr")["cnt"].mean()

fig, ax = plt.subplots()
ax.plot(avg_rent_by_hour.index, avg_rent_by_hour.values, marker='o', linestyle='-', color='purple')
ax.set_xticks(range(0, 24))
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_xlabel("Jam dalam Sehari")
ax.set_title("Pola Penyewaan Sepeda berdasarkan Jam")
st.pyplot(fig)

st.write("**Insight:** Jam sibuk utama adalah pukul 07:00 - 09:00 dan 17:00 - 19:00, menunjukkan bahwa sepeda digunakan untuk perjalanan kerja/sekolah.")

# Korelasi dengan Faktor Lingkungan
st.header("Korelasi Penyewaan Sepeda dengan Faktor Lingkungan")
corr_matrix = day_df[["temp", "hum", "windspeed", "cnt"]].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig)

st.write("**Insight:** Suhu memiliki korelasi positif yang kuat dengan penyewaan sepeda, sedangkan kelembaban memiliki korelasi negatif ringan.")

# Kesimpulan
st.header("Kesimpulan & Rekomendasi")
st.markdown("""
- **Musim gugur memiliki penyewaan tertinggi**, sementara **musim semi memiliki penyewaan terendah**.
- **Jam sibuk utama adalah pagi (07:00 - 09:00) dan sore (17:00 - 19:00)**, menunjukkan penggunaan sebagai transportasi harian.
- **Suhu memiliki pengaruh kuat terhadap penyewaan**, sedangkan kelembaban dan kecepatan angin tidak terlalu signifikan.

### **Rekomendasi Bisnis:**
✅ Fokus promosi pada musim semi dengan diskon atau insentif tambahan.
✅ Optimalkan jumlah sepeda yang tersedia di musim gugur dan pada jam sibuk.
✅ Sediakan perlengkapan tambahan seperti jas hujan untuk meningkatkan kenyamanan di musim hujan.
✅ Sesuaikan strategi harga untuk meningkatkan penyewaan di luar jam sibuk.
""")