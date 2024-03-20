import streamlit as st
import pandas as pd
from datetime import timedelta

# Menggunakan st.experimental_memo untuk caching dengan ttl
@st.experimental_memo(ttl=timedelta(minutes=5))
def load_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None

# URL Google Sheets untuk masing-masing halaman
sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'
sheet_url_alat_berat = None  # Link belum tersedia

def main():
    st.title('Dashboard Monitoring')

    # Tombol untuk refresh data
    if st.button('Refresh Data'):
        st.experimental_memo.clear()  # Membersihkan semua cache
        st.experimental_rerun()       # Menjalankan ulang script untuk memuat data terbaru

    # Menambahkan navigasi halaman menggunakan radio buttons
    page = st.sidebar.radio('Pilih Halaman', ['Monitoring Dump Truck', 'Monitoring Alat Berat'])

    if page == 'Monitoring Dump Truck':
        st.header('Monitoring Dump Truck')
        # Memuat data dump truck
        data_dump_truck = load_data(sheet_url_dump_truck)
        if data_dump_truck is not None:
            st.write(data_dump_truck)
        else:
            st.error("Data tidak bisa dimuat. Silakan cek kembali sumber data Anda.")

    elif page == 'Monitoring Alat Berat':
        st.header('Monitoring Alat Berat')
        # Karena halaman ini belum tersedia, kita hanya menampilkan informasi.
        st.info("Halaman ini sedang dalam pengembangan. Silakan kembali lagi nanti.")

if __name__ == "__main__":
    main()
