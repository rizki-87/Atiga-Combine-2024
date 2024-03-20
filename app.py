import streamlit as st
import pandas as pd
import requests
from datetime import timedelta

# Fungsi untuk mengambil CSS dari file di GitHub dan menerapkannya
def remote_css(url):
    st.markdown(f'<style>{requests.get(url).text}</style>', unsafe_allow_html=True)

# Menggunakan st.experimental_memo untuk caching dengan ttl
@st.experimental_memo(ttl=timedelta(minutes=5))
def load_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None

def main():
    # Asumsikan URL berikut adalah URL mentah dari file style.css Anda di GitHub
    css_url = 'https://raw.githubusercontent.com/rizki-87/Atiga-Combine-2024/main/style.css'
    
    # Terapkan CSS Anda di awal main function
    remote_css(css_url)

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
