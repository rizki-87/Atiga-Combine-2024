import streamlit as st
import pandas as pd

# Fungsi untuk memuat data dari Google Sheets
def load_data(url):
    if url:
        df = pd.read_csv(url)
        return df
    else:
        return "Under Construction"

# URL Google Sheets untuk masing-masing halaman
sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'
sheet_url_alat_berat = None  # Link belum tersedia

# Memuat data
data_dump_truck = load_data(sheet_url_dump_truck)
data_alat_berat = load_data(sheet_url_alat_berat)

# Membuat halaman dengan Streamlit
def main():
    st.title('Dashboard Monitoring')

    # Menambahkan navigasi halaman menggunakan radio buttons
    page = st.sidebar.radio('Pilih Halaman', ['Monitoring Dump Truck', 'Monitoring Alat Berat'])

    if page == 'Monitoring Dump Truck':
        st.header('Monitoring Dump Truck')
        # Tampilkan data atau visualisasi untuk Dump Truck
        if data_dump_truck != "Under Construction":
            st.write(data_dump_truck)  # Contoh sederhana, menampilkan data saja

    elif page == 'Monitoring Alat Berat':
        st.header('Monitoring Alat Berat')
        # Tampilkan pesan under construction karena data belum tersedia
        if data_alat_berat == "Under Construction":
            st.error("Halaman ini sedang dalam pengembangan. Silakan kembali lagi nanti.")

if __name__ == "__main__":
    main()
