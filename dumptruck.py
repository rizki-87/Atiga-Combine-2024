import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Fungsi utama untuk menampilkan halaman Monitoring Dump Truck
def show():
    st.markdown("""
        <div style="border: 2px solid #ddd; padding: 10px; text-align: center; background-color: #323288; border-radius: 0px;">
            <h1 style="color: white; margin: 0;">Monitoring Ketersediaan dan Kondisi Dump Truck</h1>
        </div>
        """, unsafe_allow_html=True)
  
# URL Google Sheets untuk data Dump Truck
sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'

@st.cache(ttl=300)
def load_data(url):
    try:
        df = pd.read_csv(url)
        df['TANGGAL'] = pd.to_datetime(df['TANGGAL'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

def filter_data(df, start_date, end_date):
    filtered_df = df[(df['TANGGAL'] >= start_date) & (df['TANGGAL'] <= end_date)]
    return filtered_df

def show():
    st.markdown("""
        <div style="border: 2px solid #ddd; padding: 10px; text-align: center; background-color: #323288; border-radius: 0px;">
            <h1 style="color: white; margin: 0;">Monitoring Ketersediaan dan Kondisi Dump Truck</h1>
        </div>
        """, unsafe_allow_html=True)

    # Muat data
    df = load_data(sheet_url_dump_truck)
    
    # Inisialisasi container untuk input
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input('Tanggal Mulai', datetime.today())
        with col2:
            end_date = st.date_input('Tanggal Akhir', datetime.today())

# Filter data berdasarkan tanggal yang dipilih pengguna
    if not df.empty:
        filtered_df = filter_data(df, start_date, end_date)

        # Tempatkan kode visualisasi/chart Anda di sini
        # ...
        # Misalnya, membuat pie chart untuk distribusi status dump truck
        status_counts = filtered_df['STATUS DT'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
        ax.set_title('Distribusi Status Dump Truck')
        st.pyplot(fig)
