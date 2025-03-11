import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Analisis Penyewaan Sepeda",
    page_icon="🚲",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
    }
    .subheader {
        font-size: 1.8rem;
        color: #0D47A1;
    }
    .insight-box {
        background-color: #E3F2FD;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    day_df = pd.read_csv("data/day.csv")
    hour_df = pd.read_csv("data/hour.csv")
    
    # Convert date columns to datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Map season numbers to names
    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    day_df['season_name'] = day_df['season'].map(season_mapping)
    hour_df['season_name'] = hour_df['season'].map(season_mapping)
    
    # Map weathersit to descriptions
    weather_mapping = {
        1: "Clear/Few clouds", 
        2: "Mist/Cloudy", 
        3: "Light Snow/Rain", 
        4: "Heavy Rain/Snow"
    }
    day_df['weather_desc'] = day_df['weathersit'].map(weather_mapping)
    hour_df['weather_desc'] = hour_df['weathersit'].map(weather_mapping)
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Sidebar for filters
st.sidebar.markdown("## 🔍 Filter Data")

# Date range filter
min_date = day_df['dteday'].min().date()
max_date = day_df['dteday'].max().date()
date_range = st.sidebar.date_input(
    "Rentang Tanggal",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Season filter
selected_seasons = st.sidebar.multiselect(
    "Pilih Musim",
    options=["Spring", "Summer", "Fall", "Winter"],
    default=["Spring", "Summer", "Fall", "Winter"]
)

# Weather filter
selected_weather = st.sidebar.multiselect(
    "Kondisi Cuaca",
    options=day_df['weather_desc'].unique(),
    default=day_df['weather_desc'].unique()
)

# Apply filters
filtered_day_df = day_df.copy()
filtered_hour_df = hour_df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_day_df = filtered_day_df[(filtered_day_df['dteday'].dt.date >= start_date) & 
                                     (filtered_day_df['dteday'].dt.date <= end_date)]
    filtered_hour_df = filtered_hour_df[(filtered_hour_df['dteday'].dt.date >= start_date) & 
                                       (filtered_hour_df['dteday'].dt.date <= end_date)]

if selected_seasons:
    filtered_day_df = filtered_day_df[filtered_day_df['season_name'].isin(selected_seasons)]
    filtered_hour_df = filtered_hour_df[filtered_hour_df['season_name'].isin(selected_seasons)]

if selected_weather:
    filtered_day_df = filtered_day_df[filtered_day_df['weather_desc'].isin(selected_weather)]
    filtered_hour_df = filtered_hour_df[filtered_hour_df['weather_desc'].isin(selected_weather)]

# Main content
st.markdown("<h1 class='main-header'>Analisis Penyewaan Sepeda</h1>", unsafe_allow_html=True)
st.write("Laporan interaktif tentang tren penyewaan sepeda berdasarkan musim, jam dalam sehari, dan faktor lingkungan.")

# Key metrics in columns
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Penyewaan", f"{filtered_day_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Harian", f"{filtered_day_df['cnt'].mean():.0f}")
with col3:
    st.metric("Hari Tersibuk", filtered_day_df.loc[filtered_day_df['cnt'].idxmax(), 'dteday'].strftime('%d %b %Y'))
with col4:
    st.metric("Hari Tersepi", filtered_day_df.loc[filtered_day_df['cnt'].idxmin(), 'dteday'].strftime('%d %b %Y'))

# Create tabs for different visualizations
tab1, tab2, tab3, tab4 = st.tabs(["Tren Musiman", "Pola Harian", "Faktor Lingkungan", "Kesimpulan"])

with tab1:
    st.markdown("<h2 class='subheader'>Pengaruh Musim terhadap Penyewaan Sepeda</h2>", unsafe_allow_html=True)
    
    # Interactive chart with Plotly
    avg_rent_by_season = filtered_day_df.groupby("season_name")["cnt"].mean().reset_index()
    
    fig = px.bar(
        avg_rent_by_season, 
        x="season_name", 
        y="cnt",
        color="season_name",
        labels={"cnt": "Rata-rata Penyewaan", "season_name": "Musim"},
        title="Rata-rata Penyewaan Sepeda per Musim",
        color_discrete_map={"Spring": "blue", "Summer": "orange", "Fall": "green", "Winter": "red"}
    )
    fig.update_layout(xaxis_title="Musim", yaxis_title="Rata-rata Penyewaan Sepeda")
    st.plotly_chart(fig, use_container_width=True)
    
    # Trend over time by season
    daily_trend = filtered_day_df.groupby(['dteday', 'season_name'])['cnt'].sum().reset_index()
    
    fig2 = px.line(
        daily_trend, 
        x="dteday", 
        y="cnt", 
        color="season_name",
        labels={"cnt": "Total Penyewaan", "dteday": "Tanggal", "season_name": "Musim"},
        title="Tren Penyewaan Sepeda Sepanjang Waktu"
    )
    fig2.update_layout(xaxis_title="Tanggal", yaxis_title="Total Penyewaan")
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("<div class='insight-box'><b>Insight:</b> Penyewaan sepeda paling tinggi terjadi pada musim gugur, sedangkan musim semi memiliki penyewaan paling rendah.</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<h2 class='subheader'>Tren Penyewaan Berdasarkan Jam dalam Sehari</h2>", unsafe_allow_html=True)
    
    # Add day type selector (weekday/weekend)
    day_type = st.radio("Pilih Tipe Hari:", ["Semua Hari", "Hari Kerja", "Akhir Pekan"], horizontal=True)
    
    hour_filter = filtered_hour_df.copy()
    if day_type == "Hari Kerja":
        hour_filter = hour_filter[hour_filter['workingday'] == 1]
    elif day_type == "Akhir Pekan":
        hour_filter = hour_filter[hour_filter['workingday'] == 0]
    
    avg_rent_by_hour = hour_filter.groupby("hr")["cnt"].mean().reset_index()
    
    fig = px.line(
        avg_rent_by_hour, 
        x="hr", 
        y="cnt",
        markers=True,
        labels={"cnt": "Rata-rata Penyewaan", "hr": "Jam"},
        title="Pola Penyewaan Sepeda berdasarkan Jam"
    )
    fig.update_layout(
        xaxis=dict(tickmode='linear', tick0=0, dtick=1),
        xaxis_title="Jam dalam Sehari",
        yaxis_title="Rata-rata Penyewaan Sepeda"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap of hour vs day of week
    if st.checkbox("Tampilkan Heatmap Jam vs Hari dalam Seminggu"):
        hour_filter['weekday_name'] = hour_filter['weekday'].map({
            0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 
            4: "Kamis", 5: "Jumat", 6: "Sabtu"
        })
        
        heatmap_data = hour_filter.pivot_table(
            index='hr', 
            columns='weekday_name', 
            values='cnt', 
            aggfunc='mean'
        ).fillna(0)
        
        fig_heatmap = px.imshow(
            heatmap_data,
            labels=dict(x="Hari dalam Seminggu", y="Jam", color="Rata-rata Penyewaan"),
            x=heatmap_data.columns,
            y=heatmap_data.index,
            color_continuous_scale="Viridis",
            title="Pola Penyewaan berdasarkan Jam dan Hari dalam Seminggu"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.markdown("<div class='insight-box'><b>Insight:</b> Jam sibuk utama adalah pukul 07:00 - 09:00 dan 17:00 - 19:00, menunjukkan bahwa sepeda digunakan untuk perjalanan kerja/sekolah.</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<h2 class='subheader'>Korelasi Penyewaan Sepeda dengan Faktor Lingkungan</h2>", unsafe_allow_html=True)
    
    # Correlation heatmap
    corr_matrix = filtered_day_df[["temp", "hum", "windspeed", "cnt"]].corr()
    
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title="Matriks Korelasi Faktor Lingkungan dengan Penyewaan"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Scatter plots with regression line
    factor = st.selectbox("Pilih Faktor Lingkungan:", ["temp", "hum", "windspeed"])
    factor_labels = {"temp": "Suhu", "hum": "Kelembaban", "windspeed": "Kecepatan Angin"}
    
    # Check if statsmodels is available
    try:
        import statsmodels.api as sm
        has_statsmodels = True
    except ImportError:
        has_statsmodels = False
    
    # Create scatter plot with or without trendline
    if has_statsmodels:
        fig = px.scatter(
            filtered_day_df, 
            x=factor, 
            y="cnt",
            trendline="ols",
            labels={factor: factor_labels[factor], "cnt": "Total Penyewaan"},
            title=f"Hubungan antara {factor_labels[factor]} dan Penyewaan Sepeda"
        )
    else:
        fig = px.scatter(
            filtered_day_df, 
            x=factor, 
            y="cnt",
            labels={factor: factor_labels[factor], "cnt": "Total Penyewaan"},
            title=f"Hubungan antara {factor_labels[factor]} dan Penyewaan Sepeda"
        )
        st.info("Catatan: Garis tren regresi tidak ditampilkan karena package statsmodels tidak tersedia.")
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='insight-box'><b>Insight:</b> Suhu memiliki korelasi positif yang kuat dengan penyewaan sepeda, sedangkan kelembaban memiliki korelasi negatif ringan.</div>", unsafe_allow_html=True)

with tab4:
    st.markdown("<h2 class='subheader'>Kesimpulan & Rekomendasi</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Temuan Utama")
        st.markdown("""
        - **Musim gugur memiliki penyewaan tertinggi**, sementara **musim semi memiliki penyewaan terendah**.
        - **Jam sibuk utama adalah pagi (07:00 - 09:00) dan sore (17:00 - 19:00)**, menunjukkan penggunaan sebagai transportasi harian.
        - **Suhu memiliki pengaruh kuat terhadap penyewaan**, sedangkan kelembaban dan kecepatan angin tidak terlalu signifikan.
        - **Pola penyewaan berbeda antara hari kerja dan akhir pekan**, dengan akhir pekan menunjukkan distribusi yang lebih merata sepanjang hari.
        """)
    
    with col2:
        st.markdown("### Rekomendasi Bisnis")
        st.markdown("""
        ✅ Fokus promosi pada musim semi dengan diskon atau insentif tambahan.
        
        ✅ Optimalkan jumlah sepeda yang tersedia di musim gugur dan pada jam sibuk.
        
        ✅ Sediakan perlengkapan tambahan seperti jas hujan untuk meningkatkan kenyamanan di musim hujan.
        
        ✅ Sesuaikan strategi harga untuk meningkatkan penyewaan di luar jam sibuk.
        
        ✅ Kembangkan program khusus untuk akhir pekan yang menargetkan penggunaan rekreasi.
        """)
    
    # Download filtered data
    if st.button("Unduh Data Terfilter"):
        csv = filtered_day_df.to_csv(index=False)
        st.download_button(
            label="Klik untuk Mengunduh",
            data=csv,
            file_name="data_penyewaan_sepeda_terfilter.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("Dashboard dibuat dengan ❤️ menggunakan Streamlit")