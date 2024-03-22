import time
import streamlit as st
import pandas as pd
import plotly.express as px
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

    # Muat data
    df = load_data(sheet_url_dump_truck)
    
    # Initialize a container for inputs
    with st.container():
        # Date input
        col1, col2, col3 = st.columns(3)
        with col1:
            min_date = datetime(2024, 1, 1)
            max_date = datetime(2024, 12, 1)
            a_date = st.date_input("Pick a date", (min_date, max_date))
        # Select box for 'STATUS DT'
        with col2:
            unique_status = df['STATUS DT'].unique().tolist() if not df.empty else []
            status_selected = st.selectbox('Pilih Status DT', ['All'] + unique_status)
        # Select box for 'JENIS DT'
        with col3:
            unique_jenis = df['JENIS DT'].unique().tolist() if not df.empty else []
            jenis_selected = st.selectbox('Pilih Jenis DT', ['All'] + unique_jenis)

# # Filtering data
# df_filtered = df[
#     (df['TANGGAL'] >= pd.Timestamp(min_date)) &
#     (df['TANGGAL'] <= pd.Timestamp(max_date)) &
#     (df['JENIS DT'].isin(jenis_dt_selected)) &
#     (df['STATUS DT'].isin(status_dt_selected))
# ]

# # Pie chart for STATUS DT distribution
# fig = px.pie(df_filtered, names='STATUS DT', title='Distribusi STATUS DT')
# st.plotly_chart(fig)



