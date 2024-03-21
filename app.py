# import streamlit as st
# import pandas as pd
# from datetime import timedelta

# # URL Google Sheets for each page
# sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'

# # Gunakan @st.experimental_memo dengan ttl
# @st.experimental_memo(ttl=timedelta(minutes=5).total_seconds())
# def load_data(url):
#     try:
#         df = pd.read_csv(url)
#         return df
#     except Exception as e:
#         st.error(f"Gagal memuat data: {e}")
#         return None


# def main():
#     # Mengatur layout menjadi mode lebar dan menginisialisasi halaman dengan judul dan favicon
#     st.set_page_config(page_title='Dashboard Monitoring', page_icon=':truck:', layout='wide')
    
#     # Menempatkan logo di sidebar atas
#     st.sidebar.image('atiga.png', width=300)  # Sesuaikan lebar sesuai kebutuhan
    
#     # Menambahkan navigasi halaman menggunakan radio buttons di sidebar
#     page = st.sidebar.radio('Pilih Halaman', ['Monitoring Dump Truck', 'Monitoring Heavy Equipment'])
    
#     # Judul di bagian utama setelah sidebar
#     st.title('Monitoring Ketersediaan dan Kondisi Dump Truck')

#     if page == 'Monitoring Dump Truck':
#         st.header('')
#         # Memuat data dump truck
#         data_dump_truck = load_data(sheet_url_dump_truck)
#         if data_dump_truck is not None:
#             st.dataframe(data_dump_truck)  # Gunakan st.dataframe untuk tampilan yang lebih baik
#         else:
#             st.error("Data tidak dapat dimuat. Silakan periksa sumber data Anda.")
            
#         # Tombol untuk memperbarui data
#         if st.button('Muat Ulang Data'):
#             st.legacy_caching.clear_cache()  # Membersihkan semua cache
#             st.rerun()  # Menjalankan ulang skrip untuk memuat data terbaru

#     elif page == 'Monitoring Heavy Equipment':
#         st.header('Monitoring Heavy Equipment')
#         st.info("Halaman ini sedang dalam pembangunan. Silakan kembali lagi nanti.")

# if __name__ == "__main__":
#     main()

import streamlit as st
import pandas as pd
from datetime import timedelta

# URL Google Sheets untuk setiap halaman
sheet_url_dump_truck = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTnflGSDkG_l9mSnawp-HEHX-R5jMfluS1rp0HlF_hMBpQvtG21d3-zPE4TxD80CvQVPjJszeOmNWJB/pub?gid=2078136743&single=true&output=csv'

# Gunakan @st.experimental_memo dengan ttl
@st.experimental_memo(ttl=timedelta(minutes=5).total_seconds())
def load_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None

def main():
    # Mengatur layout menjadi mode lebar dan menginisialisasi halaman dengan judul dan favicon
    st.set_page_config(page_title='Dashboard Monitoring', page_icon=':truck:', layout='wide')
    
    # Menempatkan logo di sidebar atas
    st.sidebar.image('atiga.png', width=300)  # Sesuaikan lebar sesuai kebutuhan
    
    # Menambahkan navigasi halaman menggunakan radio buttons di sidebar
    page = st.sidebar.radio('Pilih Halaman', ['Monitoring Dump Truck', 'Monitoring Heavy Equipment'])
    
    # Container untuk judul dengan border
    with st.container():
        st.markdown("""
        <div style="border: 2px solid #ddd; padding: 10px; text-align: center; background-color: #323288; border-radius: -5px;">
            <h1 style="color: white; margin: 0;">Monitoring Ketersediaan dan Kondisi Dump Truck</h1>
        </div>
        """, unsafe_allow_html=True)

    if page == 'Monitoring Dump Truck':
        # Memuat data dump truck
        data_dump_truck = load_data(sheet_url_dump_truck)
        if data_dump_truck is not None:
            st.dataframe(data_dump_truck)  # Gunakan st.dataframe untuk tampilan yang lebih baik
        else:
            st.error("Data tidak dapat dimuat. Silakan periksa sumber data Anda.")
            
        # Tombol untuk memperbarui data
        if st.button('Muat Ulang Data'):
            st.legacy_caching.clear_cache()  # Membersihkan semua cache
            st.rerun()  # Menjalankan ulang skrip untuk memuat data terbaru

    elif page == 'Monitoring Heavy Equipment':
        st.header('Monitoring Heavy Equipment')
        st.info("Halaman ini sedang dalam pembangunan. Silakan kembali lagi nanti.")

if __name__ == "__main__":
    main()
